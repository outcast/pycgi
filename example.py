#!/usr/bin/python

activate_this = "/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import os
from pycgi.handler import CGIHTTPRequestHandler

class MainHandler(CGIHTTPRequestHandler):

    def do_GET(self):
        self.do_handle()

    def do_POST(self):
        self.do_handle()

    def do_handle(self):

        message = "----Headers-----\n\n"
        for header in self.headers:
            message += header+"=>"+self.headers.get(header)+"\n"
        message += "\n-----ENV-----\n\n"
        for x in os.environ:
            message += x+"=>"+os.getenv(x)+"\n"
        message += "\n-----BODY-----\n\n"
        message += self.rfile.read()+"\n"

        self.send_response(200)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(message)

MainHandler(None,os.getenv("REMOTE_ADDR"),None)
