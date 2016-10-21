#!/usr/bin/python

activate_this = "/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
import os
from pycgi.handler import CGIHTTPRequestHandler

class MainHandler(CGIHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write("----Headers-----")
        for header in self.headers:
            self.wfile.write(header+"=>"+self.headers.get(header))
        self.wfile.write("\n-----ENV-----")
        for x in os.environ:
            self.wfile.write(x+"=>"+os.getenv(x))
        self.wfile.write("\n-----BODY-----")
        self.wfile.write(self.rfile.read())

handler = MainHandler(None,os.getenv("REMOTE_ADDR"),None)

def main():
    handler.handle()

if __name__ == "__main__":
    main()
