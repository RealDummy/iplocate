
import requests
import argparse
import json
import sys
from ipaddress import ip_address

IPSTACK_URL_FORMAT = "http://api.ipstack.com/%s"


HTTP_OK = 200
IP_NOT_FOUND = 404
IPSTACK_BAD_KEY = 101
IPSTACK_MAX_USAGE_REACHED = 103

class ApiKeyException(Exception):
    pass

class ApiUsageException(Exception):
    pass

try:
    keyfile = open("apikey.txt")
    API_KEY = keyfile.read()
    keyfile.close()
except OSError:
    print("missing or invalid apikey.txt",file=sys.stderr)
    exit(1)

API_OPTIONS = {
    "access_key": API_KEY,
    "fields": "latitude,longitude",
}

#ip_address is anything that has a __repr__ / __str__
def locate_ip(ip_address):
    url = IPSTACK_URL_FORMAT % ip_address
    
    try:
        response = requests.get(url,params=API_OPTIONS)
        response_obj = json.loads(response.content)
        return (response_obj["latitude"], response_obj["longitude"])
    except KeyError:
        code = response_obj["error"]["code"]
        if code == IP_NOT_FOUND:
            raise ValueError
        elif code == IPSTACK_BAD_KEY:
            raise ApiKeyException
        elif code == IPSTACK_MAX_USAGE_REACHED:
            raise ApiUsageException
        raise Exception

def validate_ip(string_ip):
    try:
        return str(ip_address(string_ip))
    except ValueError:
        return None


def print_ip_location(ip_str):
    ip = validate_ip(ip_str)
    if ip is None:
        print(f"invalid ip: '{ip_str}'", file=sys.stderr)
        print("- -")
        return
    try:
        (lat, long) = locate_ip(ip)
        print(f"{lat} {long}")
    except ValueError:
        print(f"ip not found: {ip}", file=sys.stderr)
        print("- -")
        return
    except ApiKeyException:
        print("API key invalid", file=sys.stderr)
        exit(1)
    except ApiUsageException:
        print("max API usage reached", file=sys.stderr)
        exit(1)
    except Exception:
        print("Something went wrong :(", file=sys.stderr)
        exit(1)

def main():
    parser = argparse.ArgumentParser(
        prog="iplocate",
        description="Finds latitude and longitude of an IP using the ipstack API.\nIf no IP is given, reads newline seperated IPs from stdin."
    )
    parser.add_argument("ip", nargs='?', help="A valid IPv4 or IPv6 address")

    args = parser.parse_args()
    if not args.ip:
        for line in sys.stdin:
                print_ip_location(line.strip())
        return
    print_ip_location(args.ip)
                    

if __name__ == "__main__":
    main()