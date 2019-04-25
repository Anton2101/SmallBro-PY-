from http.server import BaseHTTPRequestHandler,HTTPServer
import codecs


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        if "/index.html?url=" in str(self.path):
            file = codecs.open('program.txt', 'a', "utf-8")
            url = str(self.path).replace("/index.html?url=", "")
            file.write("\n"+url)
            file.close()
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8080), Server)
while __name__ == "__main__":
    httpd.serve_forever()