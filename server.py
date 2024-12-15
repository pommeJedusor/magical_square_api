from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
from time import sleep
from pyArango.connection import *
from pyArango.collection import Collection, Field

from dotenv import load_dotenv

sleep(10)

load_dotenv()
DB_URL = os.getenv("DB_URL") or "http://127.0.0.1:8529"
USERNAME = os.getenv("USERNAME") or "root"
PASSWORD = os.getenv("PASSWORD") or "root"

conn = Connection(arangoURL=DB_URL, username=USERNAME, password=PASSWORD)
db_name = "magical_square"

if db_name not in conn:
    db = conn.createDatabase(name=db_name)
else:
    db = conn[db_name]


class Nodes(Collection):
    _fields = {"hash": Field()}


class Edges(Collection):
    _fields = {"from_index": Field(), "to_index": Field()}


nodes = db["Nodes"]
edges = db["Edges"]


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            hash = int(self.path[1:])
            query = f"""
            FOR edge IN Edges
                FILTER edge._from == 'Nodes/{hash}'
                RETURN edge.to_index
            """
            cursor = db.AQLQuery(query, rawResults=True)
            moves = list(cursor)

            print(len(moves))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(moves).encode())
        except:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Hash not found"}).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
