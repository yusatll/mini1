#!/usr/bin/env python3
"""
iPad mini 1 Akıllı Medya ve Kitaplık Yerel Sunucusu (Güvenlik Sertleştirilmiş)
- ThreadingHTTPServer ile eşzamanlı video/medya desteği
- Güvenli dosya yükleme (Uzantı beyaz listesi + 50 MB boyut sınırı)
- Dosya adı dezenfeksiyonu (Path traversal ve XSS koruması)
- YouTube arama proxy desteği
"""

import http.server
from http.server import ThreadingHTTPServer
import os
import sys
import json
import socket
import urllib.parse
import urllib.request
import re
from email import policy
from email.parser import BytesParser

PORT = 8000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS_DIR = os.path.join(BASE_DIR, "books")

# Güvenlik Kısıtları
ALLOWED_EXTENSIONS = {'.pdf', '.epub', '.txt', '.cbr', '.cbz'}
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class HardenedHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def guess_type(self, path):
        if path.endswith(".der") or path.endswith(".crt"):
            return "application/x-x509-ca-cert"
        elif path.endswith(".mobileconfig"):
            return "application/x-apple-aspen-config"
        elif path.endswith(".appcache"):
            return "text/cache-manifest"
        elif path.endswith(".m3u8"):
            return "application/vnd.apple.mpegurl"
        elif path.endswith(".m3u"):
            return "audio/x-mpegurl"
        elif path.endswith(".pdf"):
            return "application/pdf"
        elif path.endswith(".epub"):
            return "application/epub+zip"
        return super().guess_type(path)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/" or parsed.path == "":
            self.send_response(302)
            self.send_header("Location", "/portal/index.html")
            self.end_headers()
            return

        if parsed.path == "/api/books":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            books = []
            if os.path.exists(BOOKS_DIR):
                for f in os.listdir(BOOKS_DIR):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in ALLOWED_EXTENSIONS:
                        fpath = os.path.join(BOOKS_DIR, f)
                        books.append({
                            "name": f,
                            "size": os.path.getsize(fpath),
                            "url": f"/books/{urllib.parse.quote(f)}"
                        })
            self.wfile.write(json.dumps(books, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/youtube":
            params = urllib.parse.parse_qs(parsed.query)
            q = params.get("q", [""])[0]
            if not q:
                self.send_response(400)
                self.end_headers()
                return

            results = self.search_youtube(q)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(results, ensure_ascii=False).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/upload-pdf":
            try:
                content_length = int(self.headers.get('content-length', 0))
                
                if content_length > MAX_UPLOAD_SIZE:
                    self.send_response(413, "Dosya boyutu çok büyük (Maksimum 50 MB)")
                    self.end_headers()
                    self.wfile.write(b'{"error": "Dosya boyutu cok buyuk. Maksimum 50 MB"}')
                    return

                body = self.rfile.read(content_length)
                content_type = self.headers.get('content-type', '')

                if 'multipart/form-data' in content_type:
                    msg_data = f"Content-Type: {content_type}\r\n\r\n".encode('latin1') + body
                    msg = BytesParser(policy=policy.default).parsebytes(msg_data)

                    for part in msg.iter_parts():
                        filename = part.get_filename()
                        if filename:
                            safe_name = os.path.basename(filename)
                            safe_name = re.sub(r'[^a-zA-Z0-9_.\-\u00C0-\u017F]', '_', safe_name)
                            
                            ext = os.path.splitext(safe_name)[1].lower()
                            if ext not in ALLOWED_EXTENSIONS:
                                self.send_response(400, "Gecersiz dosya uzantisi")
                                self.end_headers()
                                self.wfile.write(b'{"error": "Gecersiz uzanti. Sadece PDF, ePub, TXT, CBR yuklenebilir."}')
                                return

                            os.makedirs(BOOKS_DIR, exist_ok=True)
                            dest_path = os.path.join(BOOKS_DIR, safe_name)
                            with open(dest_path, "wb") as f_out:
                                f_out.write(part.get_payload(decode=True))

                            self.send_response(200)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps({"status": "ok", "file": safe_name}).encode("utf-8"))
                            return

                self.send_response(400)
                self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
            return

        return super().do_POST()

    def search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        })
        try:
            html = urllib.request.urlopen(req, timeout=6).read().decode("utf-8", errors="ignore")
            match = re.search(r"var ytInitialData = ({.*?});</script>", html)
            videos = []
            if match:
                data = json.loads(match.group(1))
                contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                for sec in contents:
                    items = sec.get("itemSectionRenderer", {}).get("contents", [])
                    for it in items:
                        v = it.get("videoRenderer")
                        if v and "videoId" in v:
                            vid = v["videoId"]
                            title = v.get("title", {}).get("runs", [{}])[0].get("text", "Video")
                            author = v.get("ownerText", {}).get("runs", [{}])[0].get("text", "Kanal")
                            videos.append({
                                "id": vid,
                                "title": title,
                                "author": author
                            })
                            if len(videos) >= 20:
                                break
            else:
                ids = re.findall(r"\"videoId\":\"([a-zA-Z0-9_-]{11})\"", html)
                titles = re.findall(r"\"title\":\{\"runs\":\[\{\"text\":\"([^\"]+)\"\}\]", html)
                seen = set()
                for i in range(min(len(ids), len(titles))):
                    if ids[i] not in seen:
                        seen.add(ids[i])
                        videos.append({"id": ids[i], "title": titles[i], "author": "YouTube"})
                        if len(videos) >= 20:
                            break
            return videos
        except Exception as e:
            print("YouTube Arama Hatası:", e)
            return []

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("=" * 60)
    print("🚀 iPad mini 1 Akıllı Medya ve Okuma Sunucusu (Sertleştirilmiş)")
    print(f"📡 Mac Yerel IP Adresi: {local_ip}")
    print(f"📱 iPad'de Safari'yi açıp şu adrese gidin:")
    print(f"\n👉  http://{local_ip}:{PORT}/portal/index.html  👈\n")
    print("🛡️  Güvenlik: ThreadingHTTPServer, Boyut Sınırı (50MB), Uzantı Filtresi Aktif")
    print("=" * 60)

    with ThreadingHTTPServer(("0.0.0.0", PORT), HardenedHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatıldı.")
