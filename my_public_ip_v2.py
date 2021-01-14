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


def main():
    pass


def run_config():
    pass


# Takes commandline arguments
def take_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--reconfig", "--reconfigure", help="Reconfigure script, credentials and other details", required=False, action="store_true")
    args = argparser.parse_args()

    return args


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