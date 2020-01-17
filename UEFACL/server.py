# server.py
from wsgiref.simple_server import make_server
from uefacl import application 

server = make_server('localhost', 8080, application)
server.serve_forever()