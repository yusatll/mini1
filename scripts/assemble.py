with open("portal/style.css", "r", encoding="utf-8") as f:
    css = f.read()

with open("portal/channels.json", "r", encoding="utf-8") as f:
    channels_json = f.read()

with open("portal/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Make app.js prefer the in-memory allChannels
js_patched = js.replace(
    "function initTV() {",
    "function initTV() {\n    if (typeof allChannels !== \"undefined\" && allChannels && allChannels.length > 0) {\n      renderChannels(allChannels);\n      prepareTV(allChannels[0], null, false);\n      return;\n    }"
)

html_top = """<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="iPad Hub">
  <title>iPad Hub - Canlı TV, YouTube & Kitaplık</title>
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <style>
"""

html_middle = """
  </style>
</head>
<body>
  <div class="app-layout">
    <!-- Üst Bar -->
    <header class="top-nav">
      <div class="app-brand">
        <span class="brand-logo">📱</span>
        <span class="brand-name" id="current-view-title">Canlı TV</span>
      </div>
      <div class="status-indicator" id="global-status">Hazır</div>
    </header>

    <!-- Sekmeler -->
    <main class="content-viewport">
      <!-- 1. CANLI TV -->
      <section class="tab-pane active" id="tab-tv">
        <div class="player-box">
          <div class="video-aspect">
            <video id="tv-player" controls playsinline webkit-playsinline></video>
            <div class="player-overlay" id="tv-overlay">
              <span id="tv-playing-title">Bir kanal seçin</span>
            </div>
          </div>
        </div>

        <div class="search-wrap">
          <input type="text" id="tv-search" placeholder="🔍 Kanal ara (TRT, Haber, Spor, Belgesel)..." autocomplete="off">
        </div>

        <div class="channels-list-grid" id="tv-channels-grid"></div>
      </section>

      <!-- 2. LITE YOUTUBE -->
      <section class="tab-pane" id="tab-youtube">
        <div class="player-box">
          <div class="video-aspect" id="yt-player-container">
            <div class="yt-placeholder">
              <p>İzlemek istediğiniz videoyu arayın veya aşağıdan seçin.</p>
            </div>
          </div>
          <div class="yt-info-bar" id="yt-info-bar" style="display:none;">
            <h4 id="yt-current-title">Video Başlığı</h4>
            <span id="yt-current-author">Kanal</span>
          </div>
        </div>

        <form class="search-wrap yt-search-form" id="yt-search-form">
          <input type="text" id="yt-search-input" placeholder="🔍 YouTube'da video arayın..." autocomplete="off">
          <button type="submit" id="yt-search-btn">Ara</button>
        </form>

        <div class="quick-chips">
          <button class="chip-btn active" data-q="Müzik">Müzik</button>
          <button class="chip-btn" data-q="Belgesel">Belgesel</button>
          <button class="chip-btn" data-q="Haberler">Haberler</button>
          <button class="chip-btn" data-q="Nostalji Dizi">Nostalji</button>
          <button class="chip-btn" data-q="Çizgi Film">Çizgi Film</button>
        </div>

        <div class="videos-list-grid" id="yt-videos-grid"></div>
      </section>

      <!-- 3. PDF & KİTAPLIK -->
      <section class="tab-pane" id="tab-pdf">
        <div class="guide-box">
          <span class="guide-icon">💡</span>
          <div class="guide-desc">
            Aşağıdaki kitaba dokunduğunuzda Safari'de açılır; sağ üstteki <strong>"iBooks'ta Aç"</strong> butonuna basarsanız, kitap kalıcı olarak iPad hafızasına kaydedilir ve internetsiz/Mac'siz okunur.
          </div>
        </div>

        <h3 class="pane-subtitle">Kayıtlı Kitaplar</h3>
        <div class="books-container" id="books-list">
          <div class="book-row">
            <div class="book-meta">
              <span class="book-meta-icon">📕</span>
              <div>
                <div class="book-meta-name">iPad Mini 1 Hızlandırma Rehberi.pdf</div>
                <div class="book-meta-size">Dahili Belge (İnternetsiz Okunabilir)</div>
              </div>
            </div>
            <a class="btn-open" href="books/iPad_Mini_1_Rehberi.pdf" target="_blank">Aç / Oku</a>
          </div>
        </div>
      </section>

      <!-- 4. AYARLAR -->
      <section class="tab-pane" id="tab-settings">
        <h3 class="pane-subtitle">Sistem ve Güvenlik Araçları</h3>
        <div class="settings-list">
          <a href="certs/isrgrootx1.der" class="setting-item" download>
            <span class="item-icon">🔒</span>
            <div class="item-details">
              <strong>ISRG Root X1 SSL Sertifikasını Kur</strong>
              <span>iOS 9'da güncel sitelerin ve yayınların SSL hatasını çözer.</span>
            </div>
          </a>

          <a href="playlists/kanallar.m3u" class="setting-item" download>
            <span class="item-icon">📋</span>
            <div class="item-details">
              <strong>VLC M3U Çalma Listesini İndir</strong>
              <span>Harici IPTV veya VLC uygulamasında izlemek için.</span>
            </div>
          </a>
        </div>

        <h3 class="pane-subtitle" style="margin-top:20px;">iPad Hızlandırma Tüyoları (Ayarlar'dan)</h3>
        <div class="tip-card">
          <p><strong>1. Saydamlığı Azalt:</strong> <code>Ayarlar > Genel > Erişilebilirlik > Kontrastı Artır > Saydamlığı Azalt</code> (AÇIK)</p>
          <p><strong>2. Hareketi Azalt:</strong> <code>Ayarlar > Genel > Erişilebilirlik > Hareketi Azalt</code> (AÇIK)</p>
          <p><strong>3. Arka Plan Yenilemeyi Kapat:</strong> <code>Ayarlar > Genel > Arka Planda Uygulama Yenile</code> (KAPALI)</p>
        </div>
      </section>
    </main>

    <!-- Sabit Alt Sekme Barı -->
    <nav class="bottom-tab-bar">
      <button class="tab-btn active" data-tab="tab-tv" data-title="Canlı TV">
        <span class="tab-icon">📺</span>
        <span class="tab-label">Canlı TV</span>
      </button>

      <button class="tab-btn" data-tab="tab-youtube" data-title="Lite YouTube">
        <span class="tab-icon tab-yt">▶</span>
        <span class="tab-label">YouTube</span>
      </button>

      <button class="tab-btn" data-tab="tab-pdf" data-title="PDF Kitaplık">
        <span class="tab-icon">📚</span>
        <span class="tab-label">Kitaplık</span>
      </button>

      <button class="tab-btn" data-tab="tab-settings" data-title="Ayarlar & Sertifika">
        <span class="tab-icon">⚙️</span>
        <span class="tab-label">Ayarlar</span>
      </button>
    </nav>
  </div>

  <script>
  var allChannels = 
"""

html_bottom = """
  </script>
</body>
</html>
"""

full_html = html_top + css + html_middle + channels_json + ";\n" + js_patched + html_bottom

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

with open("portal/index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("assemble.py tamamlandi!")
