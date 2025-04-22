import argparse
import logging
import sys
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import HTTPHandler
from LanguageModel import Model

parser = argparse.ArgumentParser()
parser.add_argument("model_name", help="Language model name you want to host.")
parser.add_argument("-p", "--port", help="Port numper you want to host the API",type=int)
args = parser.parse_args()

class MultiThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(model_name:str, port_number:int = 8080, hostname:str = ""):
    language_model:Model = Model(model_name)
    handlerModule = HTTPHandler
    handler = handlerModule.HTTPHandler
    
    address = (hostname, port_number)
    with MultiThreadHTTPServer(address, 
                               lambda *args, **kwargs: handler(*args, model=language_model, **kwargs)) as server:
        print(f"Server is running on port {port_number} with model: {model_name}...")
        server.serve_forever()

if __name__ == "__main__":
    model_name:str = args.model_name
    port_number:int = args.port if args.port else None
    logging.basicConfig(filename = model_name.split("/")[1] +".log", encoding='utf-8', level=logging.INFO)
    run_server(model_name, args.port)if args.port else run_server(model_name)
