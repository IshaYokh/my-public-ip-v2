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
    # Checking if reconfiguration is necessary whether the script is running for the first time or the user has requested
    if take_args:
        run_config()

    # Getting IP address
    ip_address = get_ip()


# Runs commandline prompt to take credentials and other details from user
def run_config():
    # Dict object to store credentials and other details
    creds = {"SCRIPT_CONFIGURED":False}

    # Taking input for gmail credentials
    while(True):
        use_gmail = input("Do you want to use gmail to receive updates about your public IP address? (y/n): ")
        if(use_gmail.lower() == "y" or use_gmail.lower() == "n" or use_gmail.lower() == "yes" or use_gmail.lower() == "no"):
            break

    if(use_gmail.lower() == "y" or use_gmail.lower() == "yes"):
        gmail_username = input("Enter gmail username: ")
        gmail_password = getpass("Enter gmail password: ")
        gmail_rec_email = input("Enter receiver email: ")

        # Storing gmail credentials in creds to store later on in environment variables
        creds["USE_GMAIL"] = True
        creds["GMAIL_USERNAME"] = gmail_username
        creds["GMAIL_PASSWORD"] = gmail_password
        creds["GMAIL_REC_EMAIL"] = gmail_rec_email

    # Taking input for sms credentials
    while(True):
        use_sms = input("Do you want to use sms to receive updates about your public IP address? (y/n): ")
        if(use_sms.lower() == "y" or use_sms.lower() == "n" or use_sms.lower() == "yes" or use_sms.lower() == "no"):
            break

    if(use_sms.lower() == "y" or use_sms.lower() == "yes"):
        twilio_sid = getpass("Enter twilio account SID: ")
        twilio_token = getpass("Enter twilio account authentication token: ")
        twilio_sender_number = input("Enter twilio sender phone number: ")
        twilio_rec_number = input("Enter receiver phone number: ")

        # Storing sms credentials in creds to store later on in environment variables
        creds["USE_SMS"] = True
        creds["TWILIO_SID"] = twilio_sid
        creds["TWILIO_TOKEN"] = twilio_token
        creds["TWILIO_SENDER_NUMBER"] = twilio_sender_number
        creds["TWILIO_REC_NUMBER"] = twilio_rec_number

    script_schedule = input("How frequent would you like the script to run? (Enter amount in minutes): ")
    creds["SCRIPT_SCHEDULE"] = script_schedule

    store_credentials(creds)
        

# Stores credentials and other details in environment variables
def store_credentials(creds):
    # Validating operating system
    if os.name == "posix":
        for export in creds:
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write("export {variable}=\"{value}\"".format(variable=export, value=str(creds.get(export))))
            sys.exit()
    
    elif os.name == "nt":
        print(""" 
                [X] The script detected Windows as the operating system, the script is only able to automatically store environment on linux for now\n
                Manually save the below environment variables in your windows system and re-run the script again.

                \n1. SCRIPT_CONFIGURED = True
                \n2. USE_GMAIL = True or False (depends if you want to use email as your notification method)
                \n3. GMAIL_USERNAME = the username of the gmail account that you would to use to send email notifications
                \n4. GMAIL_PASSWORD = the password of the gmail account that you would to use to send email notifications
                \n5. GMAIL_REC_EMAIL = the email to receive notifications
                \n6. USE_SMS = True or False (depends if you want to use sms as your notification method)
                \n7. TWILIO_SID = the SID of your twilio account
                \n8. TWILIO_TOKEN = the authentication token of your twilio account
                \n9. TWILIO_SENDER_NUMBER = the phone number that will send the sms notifications
                \n10. TWILIO_REC_NUMBER = the phone number that will receive the sms notifications
                \n11. SCRIPT_SCHEDULE = an integer that defines how frequent you would like the script to run, the numbers must be in minutes
            """)

        sys.exit()


# Gets credentials and other details in environment variables
def get_credentials(cred=None):
    pass


# Takes commandline arguments
def take_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--reconfig", "--reconfigure", help="Reconfigure script, credentials and other details", required=False, action="store_true")
    args = argparser.parse_args()

    return args.reconfig


# Gets public ip address using ipify.org API
def get_ip():
    return requests.get("https://api.ipify.org").text


def send_notification():
    pass


# Creates an sqlite object, cursor and db table
def init_sqlite():
    sql_connection = sqlite3.connect("ip_addresses.db")
    sql_cursor = self.sql_connection.cursor()
    sql.cursor.execute(""" CREATE TABLE ip_addresses (ip_address string) """)

    return sql_connection, sql_cursor


# Closes connection to local database
def close_db():
    sql_connection, sql_cursor = init_sqlite()
    sql_connection.close()


# Adds data to local database
def add_to_db(ip_address):
    if(check_db(ip_address)):
        return

    # Adding given ip address to local database if it's not already stored
    command = """ INSERT INTO ip_addresses (ip_address) VALUES ("{ip_address}") """.format(ip_address=ip_address)
    sql_connection, sql_cursor = init_sqlite()
    sql_cursor.execute(command)
    sql_connection.commit()


# Checks if specific data exist in the local database
def check_db(ip_address):
    # Sending query to local database to check if the given ip address is already stored
    query = """ SELECT ip_address FROM ip_addresses WHERE ip_address = "{ip_address}" """.format(ip_address=ip_address)
    sql_connection, sql_cursor = init_sqlite()
    query_return = sql_cursor.execute(query)
    query_return = query_return.fetch_all()
    sql_connection.commit()

    if(query_return):
        return True

    return False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Program interrupted by user - Exiting")


# Author: @IshaYokh
# Code repo: https://github.com/IshaYokh/my-public-ip-v2