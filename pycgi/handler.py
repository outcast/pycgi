from BaseHTTPServer import BaseHTTPRequestHandler, _quote_html
import os, sys
import cgitb

cgitb.enable()


class CGIHTTPRequestHandler(BaseHTTPRequestHandler):

    """HTTP request handler base class.
    This is a HTTP Reqest Handler. Primary meant to be used with CGI running under Apache Web Server
    """
    server_version = os.getenv("SERVER_SOFTWARE",BaseHTTPRequestHandler.sys_version)

    def setup(self):
        self.rfile = sys.stdin
        self.wfile = sys.stdout

    def finish(self):
        """
        Apache will take care close fds

        """
        print

    def get_headers(self):
        headers = {}
        for env in os.environ:
            if env.startswith("HTTP_"):
                headers[env.replace("HTTP_","")] = os.getenv(env)
        return headers


    def parse_request(self):
        self.command = os.getenv("REQUEST_METHOD")
        self.path = os.getenv("REQUEST_URI")
        self.request_version = os.getenv("SERVER_PROTOCOL")

        # Examine the headers and look for a Connection directive
        self.headers = self.get_headers()

        return True

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """

        if not self.parse_request():
            # An error code has been sent, just exit
            return
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()


    def handle(self):
        """Handle multiple requests if necessary."""
        self.handle_one_request()

    def send_response(self, code, message=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("Status: %d %s\r\n" %
                             (code, message))
            # print (self.protocol_version, code, message)

    def send_header(self, keyword, value):
        """Send a MIME header."""
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s: %s\r\n" % (keyword, value))

    def send_error(self, code, message=None):
        try:
            short, long = self.responses[code]
        except KeyError:
            short, long = '???', '???'
        if message is None:
            message = short
        explain = long
        self.log_error("code %d, message %s", code, message)
        # using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
        content = (self.error_message_format %
                   {'code': code, 'message': _quote_html(message), 'explain': explain})
        self.send_response(code, message)
        self.send_header("Content-Type", self.error_content_type)
        self.end_headers()
        if self.command != 'HEAD' and code >= 200 and code not in (204, 304):
            self.wfile.write(content)

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("\r\n")


    def log_request(self, code='-', size='-'):
        """Log an accepted request.

        This is called by send_response().

        """

        self.log_message('"%s %s %s" %s %s',
                         self.command, self.path, self.request_version, str(code), str(size))

    def address_string(self):
        return os.getenv("HTTP_HOST")
