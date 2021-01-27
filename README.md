# my-public-ip-v2

## Table of contents
- [Description](#Description)
- [How it works](#How-it-works)
- [Requirements](#Requirements)
- [Usage guide](#Usage-guide)
- [Running the script](#Running-the-script)
- [LICENCE](#LICENCE)
- [Author](#Author)

## Description:
A simple tool that reports your dynamic public IP address to you via email and sms, it checks for new IP addresses based on a specified time interval and it stores and obtains credentials as enviroment variables. This tool comes in handy for people that are unable to obtain a static public IP address and don't want to get a domain name.

## How it works:
The tool runs automatically based on a specified time interval, it checks if the IP is in the databse then stores it if it's not and sends the notification. For Linux, It runs a configuration prompt on first time use then stores the values that are given by the user as enviroment variables. For windows, unfortunately, it doesn't store the credentials automatically so they must be defined manually.

## Requirements:
- Linux/Unix based system or Windows
- Python 3
- Pip3 (Python package manager)
- All libraries in requirements.txt which is Twilio (can be installed through pip, command depends on your operating system, "pip3 install requirements.txt" for Linux)
- Access privilege to environmental variables in your system
- Gmail username and password (only required if email notification option is selected in settings)
- Twilio API key, authentication token, and a phone number (only required if SMS option is selected in settings)

## Usage guide:
- Linux:
  - It is as simple as running the script and entering values accordingly based on the configuration prompt, rebooting the system and rerunning the script.
  
- Windows:
  - Required values must be manually set as enviroment variables for windows, after setting up the variables, a reboot might be needed. Below is an explanation of what each evniroment variable name should be and what values it must hold:
    - SCRIPT_CONFIGURED = True (This tells the script that everything has been configured and there is no need to run the configuration prompt on next run)
    - USE_GMAIL = True or False (depends if you want to use email as your notification method)
    - GMAIL_USERNAME = the username of the gmail account that you would to use to send email notifications
    - GMAIL_PASSWORD = the password of the gmail account that you would to use to send email notifications
    - GMAIL_RECV_EMAIL = the email to receive notifications
    - USE_SMS = True or False (depends if you want to use sms as your notification method)
    - TWILIO_SID = the SID of your twilio account
    - TWILIO_TOKEN = the authentication token of your twilio account
    - TWILIO_SENDER_NUMBER = the phone number that will send the sms notifications
    - TWILIO_RECV_NUMBER = the phone number that will receive the sms notifications
    - SCRIPT_SCHEDULE = an integer that defines how frequent you would like the script to run, the numbers must be in minutes


## Running the script:
After fully configuring and setting up all required values, the script can be simply run with the below commands in the terminal or CMD:

- Linux/Unix:
  - python3 my_public_ip_v2.py
  
- Windows:
  - python my_public_ip_v2.py

## LICENCE:
This project is licenced under the MIT Licence - see the [LICENSE.md](https://github.com/IshaYokh/my-public-ip-v2/blob/master/LICENSE) file for details

## Author:
- [Isha Yokh](https://github.com/IshaYokh)
- Repo for the project: https://github.com/IshaYokh/my-public-ip-v2
