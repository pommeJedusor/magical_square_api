from http.server import BaseHTTPRequestHandler, HTTPServer
import re, json
from main import get_graph, get_moves_from_graph, get_path


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/get_moves/"):
            hash = self.path.removeprefix("/get_moves/")
            is_valid = re.compile("^\\d+$").match(hash)
            if not is_valid:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Hash not valid"}).encode())
                return

            hash = int(hash)
            graph = get_graph()
            try:
                moves = get_moves_from_graph(graph, hash)
            except:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Hash not valid"}).encode())
                return

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(moves).encode())

        elif self.path.startswith("/get_path/"):
            index = self.path.removeprefix("/get_path/")
            is_valid = re.compile("^\\d+$").match(index)
            if not is_valid or int(index) > 33938943:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "path index not valid"}).encode())
                return

            index = int(index)
            graph = get_graph()
            moves = get_path(graph, index)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(moves).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
