from http import server
from wifi import Cell, Scheme
n = 'yo'
nets = list(Cell.all('wlan0'))
print(nets)
names = []
for net in nets:
    names.append(net.ssid)
class Handler(server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        pth = self.path.split('/')[1:]
        print(pth)
        if(pth[0] == 'wifi'):
            self.wfile.write(str.encode("%s" %names))
        else:
            self.wfile.write(b'You Have Reached The Pi, Congrats!')
    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")
httpd = server.HTTPServer(('', 9890), Handler)
httpd.serve_forever()

