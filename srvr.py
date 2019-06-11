from http import server
from wifi import Cell, Scheme
def save_wifi(path):
    qstring = path.split('?')[1]
    print(qstring)
    qs = qstring.split('&')
    print(qs)
    qdict = {}
    for q in qs:
        w = q.split('=')
        qdict[w[0]] = w[1]
    print(qdict)
    block = ("""
network={
        ssid="%s"
        psk="%s"
        key_mgmt=WPA-PSK
}""" %(qdict['ssid'], qdict['passwd']))
    print(block)
    with open('/etc/wpa_supplicant/wpa_supplicant-wlan0.conf', 'a') as f:
        f.write(block)
        f.close()

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
        print(self.path)
        pth = self.path.split('/')[1:]
        print(pth)
        if(pth[0] == 'wifi'):
            self.wfile.write(str.encode("%s" %names))
            if(pth[1] == 'connect'):
                save_wifi(self.path)
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

