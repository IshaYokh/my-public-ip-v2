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


def get_ip():
    pass


def send_notification():
    pass


def add_to_db():
    pass


def check_db():
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Program interrupted by user - Exiting")


# Author: @IshaYokh
# Code repo: https://github.com/IshaYokh/my-public-ip-v2