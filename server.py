import sys
from socketserver import ThreadingMixIn
from http.server import HTTPServer
import HTTPHandler
import LanguageModel

class MultiThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run_server(model_name):
    handler = HTTPHandler.Handler(LanguageModel.LanguageModel(model_name))
    
    address = ('', 8080)
    with MultiThreadHTTPServer(address, handler) as server:
        print(f"Server is running on port 8080 with model: {model_name}...")
        server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <model_name>")
        sys.exit(1)

    model_name = sys.argv[1]
    run_server(model_name)
