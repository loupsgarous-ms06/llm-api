import logging
import sys
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import HTTPHandler
from LanguageModel import Model

class MultiThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(model_name):
    language_model:Model = Model(model_name)
    handlerModule = HTTPHandler
    handler = handlerModule.HTTPHandler
    # handler.set_model(language_model)
    
    address = ('', 8080)
    with MultiThreadHTTPServer(address, 
                               lambda *args, **kwargs: handler(*args, model=language_model, **kwargs)) as server:
        print(f"Server is running on port 8080 with model: {model_name}...")
        server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <model_name>")
        sys.exit(1)

    model_name = sys.argv[1]
    logging.basicConfig(filename = f"{model_name.split("/")[1]}.log", encoding='utf-8', level=logging.INFO)
    run_server(model_name)
