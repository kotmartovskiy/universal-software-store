from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
WEB=ROOT/'web'
DATA=ROOT/'data'
class Handler(BaseHTTPRequestHandler):
    def send_body(self,status,body,ctype='application/json; charset=utf-8'):
        raw=body.encode('utf-8'); self.send_response(status); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/api/health': self.send_body(200,json.dumps({'status':'ok','project':'universal-software-store','schema':'0.1'})); return
        if self.path=='/api/devices': self.send_body(200,(DATA/'devices.json').read_text(encoding='utf-8')); return
        if self.path in ('/','/index.html'): self.send_body(200,(WEB/'index.html').read_text(encoding='utf-8'),'text/html; charset=utf-8'); return
        self.send_body(404,json.dumps({'error':'not_found'}))
if __name__=='__main__':
    print('Universal Software Store: http://127.0.0.1:8090/')
    ThreadingHTTPServer(('127.0.0.1',8090),Handler).serve_forever()
