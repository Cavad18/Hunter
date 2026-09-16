#!/usr/bin/env python3

import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def check_path(base_url, path):
    url = urljoin(base_url.rstrip("/") + "/", path.strip())

    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False
        )

        if response.status_code in [200, 301, 302, 403]:
            print(
                f"{GREEN}[{response.status_code}]{RESET} "
                f"{url} "
                f"{YELLOW}({len(response.content)} bytes){RESET}"
            )

    except requests.RequestException:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Hunter - Web Content Discovery Tool"
    )

    parser.add_argument(
        "-u", "--url",
        required=True,
        help="Target URL"
    )

    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Wordlist"
    )

    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=10,
        help="Number of threads (default: 10)"
    )

    args = parser.parse_args()

    print(f"""
{CYAN}
 _   _             _
| | | |           | |
| |_| |_   _ _ __ | |_ ___ _ __
|  _  | | | | '_ \\| __/ _ \\ '__|
| | | | |_| | | | | ||  __/ |
\\_| |_/\\__,_|_| |_|\\__\\___|_|

        HUNTER v0.1
        Web Content Discovery
{RESET}
""")

    print(f"{CYAN}[+] Target:{RESET} {args.url}")
    print(f"{CYAN}[+] Wordlist:{RESET} {args.wordlist}")
    print(f"{CYAN}[+] Threads:{RESET} {args.threads}")
    print()

    try:
        with open(args.wordlist, "r", encoding="utf-8") as file:
            paths = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[-] Wordlist not found!{RESET}")
        return

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for path in paths:
            executor.submit(check_path, args.url, path)


if __name__ == "__main__":
    main()
