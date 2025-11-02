import socket, base64, sys

host = "192.168.20.2"
port = 81
path = "/ictsc.html"
auth = base64.b64encode(b"ictsc:ictsc").decode()

try:
    s = socket.create_connection((host, port), timeout=3)
    req = f"GET {path} HTTP/1.1\r\nAuthorization: Basic {auth}\r\n\r\n"
    s.sendall(req.encode())
    res = s.recv(16).decode()
    print(res)
    s.close()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
