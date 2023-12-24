import requests, time, xbmc, re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread

base_url = ""
domain = ""
x = 0
# xbmc.log = print


class MyServer(BaseHTTPRequestHandler):
    def m3u8(self, req_type: str):
        global domain
        global base_url
        global x

        parse = urlparse(self.path)
        query = parse_qs(parse.query)
        if "url" not in query:
            self.send_response(400)
            self.end_headers()
            return
        url = query["url"][0]
        domain = urlparse(url).netloc
        headers = dict(self.headers)
        del headers["Host"]
        r = requests.get(url, headers=headers, stream=True) if req_type == "GET" else requests.head(url, headers=headers)
        if r.status_code in [403, 404]:
            xbmc.log(f"JetProxy: got status code {r.status_code}; start retrying (x = {x})", xbmc.LOGINFO)
            for i in range(20):
                headers["User-Agent"] = headers["User-Agent"] + str(x)
                x += 1
                r = requests.get(url, headers=headers) if req_type == "GET" else requests.head(url, headers=headers)
                if r.status_code == 200:
                    break
                xbmc.log(f"JetProxy: got status code {r.status_code}; retrying ({i + 1} / 20)", xbmc.LOGINFO)
                time.sleep(3)
        r_parse = urlparse(r.url)
        base_url = "http://" + r_parse.netloc
        self.send_response(r.status_code)
        for key, value in r.headers.items():
            if key in ["Server", "Date", "Connection", "Content-Length"]:
                continue
            self.send_header(key, value)
        self.end_headers()
        if req_type == "GET":
            if "mp2t" in r.headers["Content-Type"]:
                e = False
                while not e:
                    for chunk in r.iter_content(chunk_size=16384):
                        try:
                            self.wfile.write(chunk)
                        except:
                            print("except")
                            e = True
                            break
                    if not e:
                        xbmc.log(f"JetProxy: got EOF; retrying", xbmc.LOGINFO)
                        print("got eof")
                        r = requests.get(url, headers=headers, stream=True)    
            else:
                text = []
                for line in r.iter_lines():
                    text.append(line.decode("utf-8"))
                text = "\n".join(text)
                text = re.sub(r"http:\/\/", f"http://127.0.0.1:49777/?url=http://", text)
                self.wfile.write(text.encode("utf-8"))
                
                 
            # else:
            #     while True:
            #         r = requests.get(url, stream=True)
            #         self.send_response(r.status_code)
            #         for key, value in r.headers.items():
            #             if key in ["Server", "Date", "Connection"]:
            #                 continue
            #             self.send_header(key, value)
            #         self.end_headers()
            #         for chunk in r.iter_content(chunk_size=16384):
            #             self.wfile.write(chunk)
           
    
    def ts(self, req_type: str):
        global domain
        global base_url

        parse = urlparse(self.path)
        query = parse_qs(parse.query)
        if "url" not in query:
            url = base_url + self.path
        else:
            url = query["url"][0]
            domain = parse.netloc
        headers = dict(self.headers)
        del headers["Host"]
        r = requests.get(url, headers=headers) if req_type == "GET" else requests.head(url, headers=headers)
        self.send_response(r.status_code)
        for key, value in r.headers.items():
            if key in ["Server", "Date", "Connection"]:
                continue
            self.send_header(key, value)
        self.end_headers()
        if req_type == "GET":
            self.wfile.write(r.content)

    def do_HEAD(self):
        if "index.bdm" in self.path.lower() or "video_ts.ifo" in self.path.lower():
            self.send_response(404)
            self.end_headers()
            return
        if self.path.endswith(".m3u8"):
            self.m3u8("HEAD")
        elif self.path.endswith(".ts"):
            self.ts("HEAD")

    def do_GET(self):
        if "index.bdm" in self.path.lower() or "video_ts.ifo" in self.path.lower():
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/stop":
            self.send_response(200)
            self.end_headers()

            def shutdown(server):
                server.shutdown()
            thread = Thread(target=shutdown, args=(self.server,))
            thread.setDaemon(True)
            thread.start()
        elif self.path.endswith(".ts") or (self.path.startswith("/hls/") and not self.path.endswith(".ts") and not self.path.endswith(".m3u8")):
            self.ts("GET")
        else:
            self.m3u8("GET")

if __name__ == "__main__":
    webServer = HTTPServer(("127.0.0.1", 49777), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()