#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Modifications copyright 2016 Oleksii Shevchenko (shevaroller.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
        print body

class HTTPClient(object):
    def get_host_port(self,url):
        parsedUrl = urlparse(url)
        hostPort = parsedUrl.netloc.split(":")
        host = hostPort[0]
        if len(hostPort) > 1:
            port = int(hostPort[1])
        else:
            port = 80
        return host, port

    def connect(self, host, port):
        # Allocate a new socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        client.connect((host, port))
        return client


        return None

    def get_code(self, data):
        return data.split(' ')[1]

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return '\r\n\r\n'.join(data.split('\r\n\r\n')[1:])

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host, port = self.get_host_port(url)
        socket = self.connect(host, port)
        parsedUrl = urlparse(url)
        reqHeader = "GET "
        reqHeader += parsedUrl.path
        if  len(parsedUrl.query) > 0:
            reqHeader += "?" + parsedUrl.query
        reqHeader += " HTTP/1.1\r\n"
        reqHeader += "Host: " + parsedUrl.netloc + "\r\n\r\n"
        socket.sendall(reqHeader)
        data = self.recvall(socket)
        code = int(self.get_code(data))
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, port = self.get_host_port(url)
        socket = self.connect(host, port)
        parsedUrl = urlparse(url)
        if args != None:
            reqBodyArray = []
            for arg in args.iteritems():
                reqBodyArray.append(str(arg[0]) + "=" + str(arg[1]))
            reqBody = '&'.join(reqBodyArray)
        elif len(parsedUrl.query) > 0:
            reqBody = parsedUrl.query
        else:
            reqBody = ''
        reqHeader = "POST "
        reqHeader += parsedUrl.path
        reqHeader += " HTTP/1.1\r\n"
        reqHeader += "Host: " + parsedUrl.netloc + "\r\n"
        reqHeader += "Content-Type: application/x-www-form-urlencoded\r\n"
        reqHeader += "Content-Length: " + str(len(reqBody)) + "\r\n\r\n"
        request = reqHeader + reqBody
        try:
            socket.sendall(request)
            data = self.recvall(socket)
            code = int(self.get_code(data))
            body = self.get_body(data)
        except:
            code = 500
            body = ''
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
