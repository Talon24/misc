#!/usr/bin/env python3
"""Turn the streaming server on / off
Server was set up following this tutorial
https://obsproject.com/forum/resources/how-to-set-up-your-own-private-rtmp-server-using-nginx.50/
if server is started, prints the viewer link"""

# import os
# import argparse
from subprocess import Popen, PIPE

import requests

STREAM_KEY = "streamkey"
RTMP_URL = "rtmp://{ip}:1935/live/{key}"

def nginx_running():
    """is nginx already running"""
    term = Popen(["ps", "-A"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout = term.communicate()[0].decode()
    return "nginx" in stdout

def get_ip():
    """Look up external IP adress"""
    url = "https://api.ipify.org?format=json"
    return requests.get(url).json()["ip"]

def main():
    """Check if server is running, if yes, stop it.
    if not, start it up and print the url"""
    command = ["sudo", "/usr/local/nginx/sbin/nginx"]
    if nginx_running():
        command.extend(["-s", "stop"])
        print("Stopping streaming server...")
    else:
        print("Starting streaming server...\n" +
              RTMP_URL.format(ip=get_ip(), key=STREAM_KEY))
    term = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = term.communicate()
    if stdout != b"" or stderr != b"":
        print("Some Output from nginx:\n----stdout:\n{}\n----stderr:\n{}"
              "".format(stdout.decode(), stderr.decode()))

if __name__ == '__main__':
    main()
