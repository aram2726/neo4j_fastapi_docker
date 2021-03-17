#!/usr/bin/env python

import argparse
import asyncio
import csv
import sys

sys.path.append(".")

from src.app.infrastructure.controllers import CLIController

COMMAND_SYNCHRONIZE = "synchronize"
COMMAND_NEW_USER = "add_user"

HELP_TEXT = f"""
To create a user `{COMMAND_NEW_USER}`.
To synchronize data `{COMMAND_SYNCHRONIZE}`.
"""


def help_text():
    print(HELP_TEXT)


def create_user():
    customerID = input("\ncustomerID: ")
    companyName = input("\ncompanyName: ")
    contactName = input("\ncontactName: ")
    contactTitle = input("\ncontactTitle: ")
    address = input("\naddress: ")
    city = input("\ncity: ")
    region = input("\nregion: ")
    postalCode = input("\npostalCode: ")
    country = input("\ncountry: ")
    phone = input("\nphone: ")
    fax = input("\nfax: ")
    return {
        "customerID": customerID,
        "companyName": companyName,
        "contactName": contactName,
        "contactTitle": contactTitle,
        "address": address,
        "city": city,
        "region": region,
        "postalCode": postalCode,
        "country": country,
        "phone": phone,
        "fax": fax,
    }


def read_csv(path):
    data = []
    with open(path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data


def main():
    commands = (COMMAND_SYNCHRONIZE, COMMAND_NEW_USER,)
    parser = argparse.ArgumentParser(
        description="Enter command to execute.", usage=", ".join(commands)
    )
    parser.add_argument(
        "action", metavar="action", type=str, choices=commands, help=HELP_TEXT
    )
    parser.add_argument('path', nargs='?', default=".")

    args = parser.parse_args()

    handler_name = args.action
    controller = CLIController()
    loop = asyncio.get_event_loop()

    if handler_name == COMMAND_NEW_USER:
        data = create_user()
        loop.run_until_complete(controller.create_user(data))
        loop.close()
    elif handler_name == COMMAND_SYNCHRONIZE:
        csv_file_path = args.path
        data = read_csv(csv_file_path)

        loop.run_until_complete(controller.synchronize(data))
        loop.close()
    else:
        help_text()


if __name__ == "__main__":
    exit(main())
