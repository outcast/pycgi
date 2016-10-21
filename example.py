#!/usr/bin/python

activate_this = "/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
import os
from pycgi.handler import CGIHTTPRequestHandler

class MainHandler(CGIHTTPRequestHandler):

    def do_GET(self):
        message = "----Headers-----\n"
        for header in self.headers:
            message += header+"=>"+self.headers.get(header)
        message += "\n-----ENV-----\n"
        for x in os.environ:
            message += x+"=>"+os.getenv(x)
        message += "\n-----BODY-----\n"
        message += self.rfile.read()

        self.send_response(200)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(message)

handler = MainHandler(None,os.getenv("REMOTE_ADDR"),None)

def main():
    handler.handle()

if __name__ == "__main__":
    main()
