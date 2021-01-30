# Author: @IshaYokh
# Code repo: https://github.com/IshaYokh/my-public-ip-v2

import subprocess
import sys
import os
import argparse
import time
import socket
import requests
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import sqlite3
from getpass import getpass


# Contains the main logic and control flow of the program
def main():
    # Checking if reconfiguration is necessary if the script is running for the first time
    if not get_credentials("SCRIPT_CONFIGURED"):
        run_config()

    # Getting IP address
    num_attempts = 0
    while True:
        if num_attempts == 3:
            print("[X] Unable to obtain IP address, number of attempts: " + str(num_attempts))
            sys.exit()
        try:
            num_attempts += 1
            ip_address = get_ip()
            break
        except:
            print("[X] Unable to obtain IP address - will try again in 5 minutes")
            time.sleep(300)

    # Checking if current IP is already in the database, adding it if it doesn't and sending notification
    if not check_db(ip_address):
        num_attempts = 0
        while True:
            if num_attempts == 3:
                print("[X] Unable to send notification, number of attempts: " + str(num_attempts))
                break
            try:
                num_attempts += 1
                send_notification(ip_address)
                break
            except:
                print("[X] Unable to send notification - will try again in 5 minutes")
                time.sleep(300)

        add_to_db(ip_address)
    
    # Checking schedule
    check_schedule()


# Runs commandline prompt to take credentials and other details from user
def run_config():
    print("---------------------------------\n| my-public-ip-v2 configuration |\n---------------------------------")

    # Dict object to store credentials and other details
    creds = {"SCRIPT_CONFIGURED":False}

    # Taking input for gmail credentials
    while(True):
        use_gmail = input("[*] Do you want to use gmail to receive updates about your public IP address? (y/n): ")
        if(use_gmail.lower() == "y" or use_gmail.lower() == "n" or use_gmail.lower() == "yes" or use_gmail.lower() == "no"):
            break

    if(use_gmail.lower() == "y" or use_gmail.lower() == "yes"):
        # Storing gmail credentials in creds to store later on in environment variables
        creds["USE_GMAIL"] = True
        creds["GMAIL_USERNAME"] = input("[*] Enter gmail username: ")
        creds["GMAIL_PASSWORD"] = getpass("[*] Enter gmail password: ")
        creds["GMAIL_RECV_EMAIL"] = input("[*] Enter receiver email: ")

    # Taking input for sms credentials
    while(True):
        use_sms = input("[*] Do you want to use sms to receive updates about your public IP address? (y/n): ")
        if(use_sms.lower() == "y" or use_sms.lower() == "n" or use_sms.lower() == "yes" or use_sms.lower() == "no"):
            break

    if(use_sms.lower() == "y" or use_sms.lower() == "yes"):
        # Storing sms credentials in creds to store later on in environment variables
        creds["USE_SMS"] = True
        creds["TWILIO_SID"] = getpass("[*] Enter twilio account SID: ")
        creds["TWILIO_TOKEN"] = getpass("[*] Enter twilio account authentication token: ")
        creds["TWILIO_SENDER_NUMBER"] = input("[*] Enter twilio sender phone number: ")
        creds["TWILIO_RECV_NUMBER"] = input("[*] Enter receiver phone number: ")

    creds["SCRIPT_SCHEDULE"] = input("[*] How frequent would you like the script to run? (Enter amount in minutes): ")
    creds["SCRIPT_CONFIGURED"] = True

    store_credentials(creds)
        

# Stores credentials and other details in environment variables
def store_credentials(creds):
    print("[*] Storing credentials")

    # Validating operating system
    if os.name == "posix":
        for export in creds:
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("\nexport {variable}=\"{value}\"".format(variable=export, value=str(creds.get(export))))
                
        print("[!] Enviroment variables saved. Reboot your system and re-run the script")
        sys.exit()
    
    elif os.name == "nt":
        print(""" 
                [X] The script detected Windows as the operating system, the script is only able to automatically store environment on linux for now\n
                Manually save the below environment variables in your windows system, reboot the system and re-run the script again.

                \n1. SCRIPT_CONFIGURED = True (This tells the script that everything has been configured and there is no need to run the configuration prompt on next run)
                \n2. USE_GMAIL = True or False (depends if you want to use email as your notification method)
                \n3. GMAIL_USERNAME = the username of the gmail account that you would to use to send email notifications (only if email notifications will be used)
                \n4. GMAIL_PASSWORD = the password of the gmail account that you would to use to send email notifications (only if email notifications will be used)
                \n5. GMAIL_RECV_EMAIL = the email to receive notifications (only if email notifications will be used)
                \n6. USE_SMS = True or False (depends if you want to use sms as your notification method)
                \n7. TWILIO_SID = the SID of your twilio account (only if sms notifications will be used)
                \n8. TWILIO_TOKEN = the authentication token of your twilio account (only if sms notifications will be used)
                \n9. TWILIO_SENDER_NUMBER = the phone number that will send the sms notifications (only if sms notifications will be used)
                \n10. TWILIO_RECV_NUMBER = the phone number that will receive the sms notifications (only if sms notifications will be used)
                \n11. SCRIPT_SCHEDULE = an integer that defines how frequent you would like the script to run, the numbers must be in minutes
            """)

        sys.exit()


# Gets credentials and other details in environment variables
def get_credentials(cred=None):
    # Returning a requested enviroment variable by itself
    if cred:
        try:
            return os.environ[cred]
        except KeyError:
            return ""
    
    """ Returning all requested enviromental variables for the configuration """

    env_vars = []
    env_vars_ids = ["SCRIPT_CONFIGURED","USE_GMAIL","GMAIL_USERNAME","GMAIL_PASSWORD", "GMAIL_RECV_EMAIL",
                    "USE_SMS","TWILIO_SID", "TWILIO_TOKEN", "TWILIO_SENDER_NUMBER",
                    "TWILIO_RECV_NUMBER","SCRIPT_SCHEDULE"
    ]

    # Iterating through the expected enviroment variable IDs
    for var_id in env_vars_ids:
        try:
            # Obtaining enviroment variable
            env_vars.append(os.environ[var_id])
        except KeyError:
            # Appending an empty string if the enviroment variable doesn't exist
            env_vars.append("")

    # Returning all requested enviromental variables for the configuration
    return env_vars[0],env_vars[1],env_vars[2],env_vars[3],env_vars[4], \
    env_vars[5],env_vars[6],env_vars[7],env_vars[8],env_vars[9],env_vars[10]


# Gets public ip address using ipify.org API
def get_ip():
    print("[*] Getting IP address")
    return requests.get("https://api.ipify.org").text


# Sends new IP address to email or sms
def send_notification(ip_address):
    script_configured, use_gmail, gmail_username, gmail_password, gmail_recv_email, use_sms, \
    twilio_sid, twilio_token, twilio_sender_number, twilio_recv_number, script_schedule = get_credentials()

    msg_body = "New public IP address: " + ip_address

    # Validating if the user has chosen email option and sending email using EmailMessage() and smtplib
    if use_gmail:
        print("[*] Sending email update notification")
        msg = EmailMessage()
        msg["Subject"] = "New Public IP address"
        msg["From"] = gmail_username
        msg["To"] = gmail_recv_email
        msg.set_content(msg_body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(gmail_username, gmail_password)
            smtp.send_message(msg)
            
    # Validating if the user has chosen sms option and sending sms using twilio API
    if use_sms:
        print("[*] Sending SMS update notification")
        twilio_client = Client(twilio_sid, twilio_token)
        twilio_client.messages \
            .create(
                body = msg_body,
                from_= twilio_sender_number,
                to = twilio_recv_number
            )


# Creates an sqlite object, cursor and db table
def init_sqlite():
    sql_connection = sqlite3.connect("ip_addresses.db")
    sql_cursor = sql_connection.cursor()

    try:
        sql_cursor.execute(""" CREATE TABLE ip_addresses (ip_address string) """)
    except sqlite3.OperationalError:
        pass

    return sql_connection, sql_cursor


# Closes connection to local database
def close_db():
    sql_connection, sql_cursor = init_sqlite()
    sql_connection.close()


# Adds data to local database
def add_to_db(ip_address):
    print("[*] Adding {ip} to database".format(ip=ip_address))

    if(check_db(ip_address)):
        return

    # Adding given ip address to local database if it's not already stored
    command = """ INSERT INTO ip_addresses (ip_address) VALUES ("{ip_address}") """.format(ip_address=ip_address)
    sql_connection, sql_cursor = init_sqlite()
    sql_cursor.execute(command)
    sql_connection.commit()


# Checks if specific data exist in the local database
def check_db(ip_address):
    print("[*] Checking {ip} in database".format(ip=ip_address))

    # Sending query to local database to check if the given ip address is already stored
    query = """ SELECT ip_address FROM ip_addresses WHERE ip_address = "{ip_address}" """.format(ip_address=ip_address)
    sql_connection, sql_cursor = init_sqlite()
    query_return = sql_cursor.execute(query)
    query_return = query_return.fetchall()
    sql_connection.commit()

    if(query_return):
        return True

    return False


# Runs checks if user has set a time for the script to automatically run again, then sleeps until next run
def check_schedule():
    script_schedule = get_credentials("SCRIPT_SCHEDULE")

    try:
        if float(script_schedule) > 0:
            print("[*] Sleeping until next run")
            while True:
                # Converting minutes to seconds and sleeping until next run
                time.sleep(float(script_schedule) * 60)
                main()
    except ValueError:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Program interrupted by user - Exiting")


# Author: @IshaYokh
# Code repo: https://github.com/IshaYokh/my-public-ip-v2
