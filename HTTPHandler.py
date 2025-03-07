from http.server import BaseHTTPRequestHandler
import logging
from urllib.parse import parse_qs, urlparse
import LanguageModel


class Handler(BaseHTTPRequestHandler):

    def __init__(self, model:LanguageModel):
        self.lm = model

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(".icon", mode = "rb") as fp:
                self.wfile.write(fp.read())
            return None
        elif self.path == ("/" or "/index.html"):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(".default", mode = "rb") as fp:
                self.wfile.write(fp.read())
                return None
                
        parsed_path = urlparse(self.path)
        try:
            text = parse_qs(parsed_path.query)["text"][0]
            logging.info("Received: {}".format(text))
        except Exception as e:
            self.send_error(400)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('Invalid Request. {}'.format(e).encode("utf8"))
            logging.error(e)
            return None
        try:
            response = self.lm.generator(text)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response)
            logging.info("Respond: {}".format(response.decode('utf8')))
            return None
        except Exception as e:
            self.send_error(500)
            self.end_headers()
            self.wfile.write('Internal Server Error. {}'.format(e).encode("utf8"))
            logging.error(e)
            return None
