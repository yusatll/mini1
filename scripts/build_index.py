import json

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

channels_json_str = json.dumps(channels, ensure_ascii=False)

html_template = r'''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="iPad Hub">
  <title>iPad Hub - Canlı TV, YouTube & Kitaplık</title>
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="apple-touch-icon" sizes="76x76" href="apple-touch-icon-76x76.png">
  <link rel="apple-touch-icon" sizes="152x152" href="apple-touch-icon-152x152.png">
  <style>
/* Reset & Temel Ayarlar - iOS 9 WebKit Uyumlu */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-tap-highlight-color: rgba(56, 189, 248, 0.2);
}

body {
  background-color: #0b0f19;
  color: #f1f5f9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px;
  line-height: 1.4;
  overflow-x: hidden;
  padding-bottom: 75px;
  -webkit-text-size-adjust: 100%;
}

/* Üst Hata & Teşhis Çubuğu (Varsayılan Gizli) */
#debug-error-bar {
  display: none;
  background-color: #b91c1c;
  color: #ffffff;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: bold;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 99999;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.app-layout {
  max-width: 900px;
  margin: 0 auto;
}

/* Üst Başlık */
.top-nav {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #111827;
  border-bottom: 1px solid #1f2937;
  padding: 10px 16px;
  display: -webkit-flex;
  display: flex;
  -webkit-justify-content: space-between;
  justify-content: space-between;
  -webkit-align-items: center;
  align-items: center;
}

.nav-brand {
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: center;
  align-items: center;
}

.nav-logo {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  margin-right: 10px;
  background-color: #0284c7;
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  justify-content: center;
  font-size: 18px;
}

.nav-title-group h1 {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.3px;
}

.nav-subtitle {
  font-size: 12px;
  color: #38bdf8;
  font-weight: 500;
}

.nav-status-badge {
  font-size: 11px;
  background-color: #10b981;
  color: #ffffff;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 600;
}

/* Ana İçerik */
.content-area {
  padding: 12px;
}

.tab-pane {
  display: none;
}

.tab-pane.active {
  display: block;
}

/* 1. CANLI TV STİLLERİ */
.player-container {
  background-color: #000000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
  margin-bottom: 14px;
}

.player-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
  background-color: #050811;
}

.player-wrapper video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
  background-color: #000;
}

.player-overlay {
  position: absolute;
  top: 8px;
  left: 8px;
  background-color: rgba(15, 23, 42, 0.85);
  color: #f8fafc;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  pointer-events: none;
  border: 1px solid rgba(255,255,255,0.1);
  max-width: 90%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-wrap {
  margin-bottom: 12px;
}

.search-input {
  width: 100%;
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 10px 14px;
  color: #ffffff;
  font-size: 15px;
  outline: none;
  -webkit-appearance: none;
}

.search-input:focus {
  border-color: #38bdf8;
}

.channels-grid {
  display: -webkit-flex;
  display: flex;
  -webkit-flex-wrap: wrap;
  flex-wrap: wrap;
  margin: -4px;
}

.ch-card {
  width: 25%;
  padding: 4px;
  box-sizing: border-box;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  outline: none;
  -webkit-user-select: none;
  user-select: none;
}

@media (max-width: 600px) {
  .ch-card {
    width: 33.33%;
  }
}

@media (max-width: 400px) {
  .ch-card {
    width: 50%;
  }
}

.ch-inner {
  background-color: #161f30;
  border: 1px solid #23324d;
  border-radius: 10px;
  padding: 10px 6px;
  text-align: center;
  transition: background-color 0.15s;
  pointer-events: none;
}

.ch-card:active .ch-inner {
  background-color: #243553;
  transform: scale(0.97);
}

.ch-inner.active {
  border-color: #38bdf8;
  background-color: #1e3a5f;
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
}

.ch-logo {
  height: 34px;
  max-width: 80%;
  object-fit: contain;
  margin: 0 auto 6px;
  display: block;
}

.ch-placeholder {
  font-size: 24px;
  line-height: 34px;
  margin-bottom: 6px;
}

.ch-name {
  font-size: 12px;
  font-weight: 600;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 2. YOUTUBE STİLLERİ */
.yt-player-box {
  background-color: #000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
  margin-bottom: 12px;
}

.yt-frame-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background-color: #0f172a;
}

.yt-frame-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.yt-placeholder-screen {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  flex-direction: column;
  -webkit-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  justify-content: center;
  color: #94a3b8;
  text-align: center;
  padding: 20px;
}

.yt-play-icon {
  font-size: 42px;
  color: #ef4444;
  margin-bottom: 8px;
}

.yt-now-playing {
  padding: 8px 12px;
  background-color: #1e293b;
  border-radius: 8px;
  margin-bottom: 12px;
  display: none;
}

.yt-title {
  font-size: 14px;
  font-weight: 700;
  color: #f8fafc;
}

.yt-author {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

.search-bar-row {
  display: -webkit-flex;
  display: flex;
  margin-bottom: 12px;
}

.search-bar-row input {
  -webkit-flex: 1;
  flex: 1;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.search-bar-row button {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0 16px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.search-bar-row button:active {
  background-color: #dc2626;
}

.chips-scroll {
  display: -webkit-flex;
  display: flex;
  overflow-x: auto;
  padding-bottom: 8px;
  margin-bottom: 12px;
  gap: 8px;
  -webkit-overflow-scrolling: touch;
}

.chip-btn {
  background-color: #1e293b;
  color: #cbd5e1;
  border: 1px solid #334155;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
  outline: none;
  -webkit-flex-shrink: 0;
  flex-shrink: 0;
}

.chip-btn.active {
  background-color: #ef4444;
  border-color: #ef4444;
  color: #ffffff;
  font-weight: 600;
}

.videos-grid {
  display: -webkit-flex;
  display: flex;
  -webkit-flex-wrap: wrap;
  flex-wrap: wrap;
  margin: -5px;
}

.v-card {
  width: 50%;
  padding: 5px;
  box-sizing: border-box;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  outline: none;
  -webkit-user-select: none;
  user-select: none;
}

@media (max-width: 500px) {
  .v-card {
    width: 100%;
  }
}

.v-inner {
  background-color: #161f30;
  border: 1px solid #23324d;
  border-radius: 10px;
  overflow: hidden;
  pointer-events: none;
}

.v-card:active .v-inner {
  background-color: #243553;
  transform: scale(0.98);
}

.v-thumb {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  background-color: #0f172a;
}

.v-thumb img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.v-info {
  padding: 8px 10px;
}

.v-title {
  font-size: 13px;
  font-weight: 600;
  color: #f1f5f9;
  line-height: 1.3;
  height: 34px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.v-author {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
}

/* 3. PDF & AYARLAR STİLLERİ */
.pane-subtitle {
  font-size: 16px;
  font-weight: 700;
  margin: 12px 0 10px;
  color: #f8fafc;
}

.guide-box {
  background-color: #1e293b;
  border-left: 4px solid #38bdf8;
  border-radius: 8px;
  padding: 12px 14px;
  margin-bottom: 14px;
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: flex-start;
  align-items: flex-start;
}

.guide-icon {
  font-size: 22px;
  margin-right: 10px;
  line-height: 1.2;
}

.guide-desc {
  font-size: 13px;
  line-height: 1.5;
  color: #cbd5e1;
}

.books-container {
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  flex-direction: column;
  gap: 10px;
}

.book-row {
  background-color: #161f30;
  border: 1px solid #23324d;
  border-radius: 10px;
  padding: 12px 14px;
  display: -webkit-flex;
  display: flex;
  -webkit-justify-content: space-between;
  justify-content: space-between;
  -webkit-align-items: center;
  align-items: center;
}

.book-meta {
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: center;
  align-items: center;
}

.book-meta-icon {
  font-size: 32px;
  margin-right: 12px;
}

.book-meta-name {
  font-weight: 600;
  font-size: 14px;
  color: #f8fafc;
}

.book-meta-size {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

.btn-open {
  background-color: #10b981;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  cursor: pointer;
}

.btn-open:active {
  background-color: #059669;
}

.settings-list {
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  flex-direction: column;
  gap: 10px;
}

.setting-item {
  background-color: #161f30;
  border: 1px solid #23324d;
  border-radius: 10px;
  padding: 14px;
  text-decoration: none;
  color: inherit;
  display: -webkit-flex;
  display: flex;
  -webkit-align-items: center;
  align-items: center;
  cursor: pointer;
}

.setting-item:active {
  background-color: #243553;
}

.item-icon {
  font-size: 28px;
  margin-right: 14px;
}

.item-details strong {
  display: block;
  font-size: 14px;
  color: #f8fafc;
  margin-bottom: 2px;
}

.item-details span {
  font-size: 12px;
  color: #94a3b8;
  line-height: 1.4;
}

.tip-card {
  background-color: #161f30;
  border: 1px solid #23324d;
  border-radius: 10px;
  padding: 14px;
  margin-top: 12px;
}

.tip-card h4 {
  font-size: 14px;
  color: #38bdf8;
  margin-bottom: 8px;
}

.tip-card ul {
  padding-left: 20px;
  font-size: 13px;
  color: #cbd5e1;
  line-height: 1.6;
}

/* Sabit Alt Sekme Barı (iOS Tarzı) */
.bottom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 62px;
  background-color: #111827;
  border-top: 1px solid #1f2937;
  display: -webkit-flex;
  display: flex;
  z-index: 999;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
}

.tab-btn {
  -webkit-flex: 1;
  flex: 1;
  background: none;
  border: none;
  color: #94a3b8;
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
  flex-direction: column;
  -webkit-align-items: center;
  align-items: center;
  -webkit-justify-content: center;
  justify-content: center;
  cursor: pointer;
  padding: 4px 0;
  outline: none;
  -webkit-user-select: none;
  user-select: none;
}

.tab-btn * {
  pointer-events: none;
}

.tab-btn:active {
  background-color: #1e293b;
}

.tab-btn.active {
  color: #38bdf8;
}

.tab-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.tab-icon.tab-yt {
  color: #ef4444;
}

.tab-label {
  font-size: 11px;
  font-weight: 600;
}
  </style>
</head>
<body>

  <!-- Teşhis ve Hata Çubuğu -->
  <div id="debug-error-bar"></div>

  <div class="app-layout">
    <!-- Üst Başlık Çubuğu -->
    <header class="top-nav">
      <div class="nav-brand">
        <div class="nav-logo">⚡</div>
        <div class="nav-title-group">
          <h1>iPad Hub</h1>
          <div class="nav-subtitle" id="current-view-title">Canlı TV</div>
        </div>
      </div>
      <div class="nav-status-badge" id="global-status">Hazır</div>
    </header>

    <main class="content-area">
      <!-- 1. CANLI TV SEKME İÇERİĞİ -->
      <section class="tab-pane active" id="tab-tv">
        <div class="player-container">
          <div class="player-wrapper">
            <video id="tv-player" controls playsinline webkit-playsinline></video>
            <div class="player-overlay" id="tv-overlay">
              <span id="tv-playing-title">Bir kanal seçin</span>
            </div>
          </div>
        </div>

        <div class="search-wrap">
          <input type="text" id="tv-search" class="search-input" placeholder="Kanal ara... (TRT, ATV, Haber, Spor...)" oninput="filterChannels()" onkeyup="filterChannels()">
        </div>

        <div class="channels-grid" id="tv-channels-grid"></div>
      </section>

      <!-- 2. LITE YOUTUBE SEKME İÇERİĞİ -->
      <section class="tab-pane" id="tab-youtube">
        <div class="yt-player-box">
          <div class="yt-frame-wrapper" id="yt-player-container">
            <div class="yt-placeholder-screen">
              <div class="yt-play-icon">▶</div>
              <div>İzlemek istediğiniz bir videoya dokunun veya arayın</div>
            </div>
          </div>
        </div>

        <div class="yt-now-playing" id="yt-info-bar">
          <div class="yt-title" id="yt-current-title"></div>
          <div class="yt-author" id="yt-current-author"></div>
        </div>

        <form class="search-bar-row" id="yt-search-form" onsubmit="handleYTSearch(event)">
          <input type="text" id="yt-search-input" class="search-input" placeholder="Video adı yazın veya YouTube linki yapıştırın...">
          <button type="submit" id="yt-search-btn">Oynat</button>
        </form>

        <div class="chips-scroll">
          <button class="chip-btn active" onclick="selectYTChip(this, 'all')">Öne Çıkanlar</button>
          <button class="chip-btn" onclick="selectYTChip(this, 'muzik')">Müzik</button>
          <button class="chip-btn" onclick="selectYTChip(this, 'nostalji')">Nostalji & Klasik</button>
          <button class="chip-btn" onclick="selectYTChip(this, 'cizgifilm')">Çizgi Film</button>
          <button class="chip-btn" onclick="selectYTChip(this, 'belgesel')">Belgesel & Tarih</button>
        </div>

        <div class="videos-grid" id="yt-videos-grid"></div>
      </section>

      <!-- 3. PDF KİTAPLIK SEKME İÇERİĞİ -->
      <section class="tab-pane" id="tab-pdf">
        <div class="guide-box">
          <span class="guide-icon">💡</span>
          <div class="guide-desc">
            Aşağıdaki kitaba dokunduğunuzda Safari'de açılır; ekranın sağ üstündeki <strong>"iBooks'ta Aç"</strong> butonuna basarsanız kitap kalıcı olarak iPad hafızasına kaydedilir ve internetsiz/Mac'siz okunur.
          </div>
        </div>

        <h3 class="pane-subtitle">Kayıtlı Kitaplar ve Belgeler</h3>
        <div class="books-container" id="books-list">
          <div class="book-row">
            <div class="book-meta">
              <span class="book-meta-icon">📕</span>
              <div>
                <div class="book-meta-name">iPad Mini 1 Hızlandırma ve Kullanım Rehberi.pdf</div>
                <div class="book-meta-size">Dahili Belge (İnternetsiz Okunabilir)</div>
              </div>
            </div>
            <a class="btn-open" href="books/iPad_Mini_1_Rehberi.pdf" target="_blank">Aç / Oku</a>
          </div>
        </div>
      </section>

      <!-- 4. AYARLAR SEKME İÇERİĞİ -->
      <section class="tab-pane" id="tab-settings">
        <h3 class="pane-subtitle">Sistem ve Güvenlik Araçları</h3>
        <div class="settings-list">
          <a href="certs/isrgrootx1.der" class="setting-item" download>
            <span class="item-icon">🔒</span>
            <div class="item-details">
              <strong>ISRG Root X1 SSL Sertifikasını Kur</strong>
              <span>iOS 9'da güncel sitelerin ve yayınların SSL sertifika hatasını çözer.</span>
            </div>
          </a>

          <a href="playlists/kanallar.m3u" class="setting-item" download>
            <span class="item-icon">📋</span>
            <div class="item-details">
              <strong>VLC / IPTV M3U Çalma Listesini İndir</strong>
              <span>Tüm 167 kanalı harici VLC veya IPTV uygulamasında izlemek için.</span>
            </div>
          </a>
        </div>

        <div class="tip-card">
          <h4>⚡ iPad Mini 1 Hızlandırma İpuçları (Cihaz Ayarlarından)</h4>
          <ul>
            <li><strong>Ayarlar &gt; Genel &gt; Erişilebilirlik &gt; Hareketi Azalt:</strong> AÇIK yapın (pencereler anında açılır, kasma biter).</li>
            <li><strong>Ayarlar &gt; Genel &gt; Erişilebilirlik &gt; Saydamlığı Azalt:</strong> AÇIK yapın (A5 çipinin grafik yükünü %50 hafifletir).</li>
            <li><strong>Ayarlar &gt; Genel &gt; Arka Planda Uygulama Yenile:</strong> KAPALI yapın (512 MB RAM'i sadece aktif uygulamaya ayırır).</li>
            <li><strong>Ayarlar &gt; Safari &gt; Geçmişi ve Web Sitesi Verilerini Sil:</strong> Safari belleğini boşaltır.</li>
          </ul>
        </div>
      </section>
    </main>

    <!-- Sabit Alt Sekme Barı -->
    <nav class="bottom-tab-bar">
      <button class="tab-btn active" id="btn-tab-tv" onclick="switchTab('tab-tv', 'Canlı TV')">
        <span class="tab-icon">📺</span>
        <span class="tab-label">Canlı TV</span>
      </button>

      <button class="tab-btn" id="btn-tab-youtube" onclick="switchTab('tab-youtube', 'Lite YouTube')">
        <span class="tab-icon tab-yt">▶</span>
        <span class="tab-label">YouTube</span>
      </button>

      <button class="tab-btn" id="btn-tab-pdf" onclick="switchTab('tab-pdf', 'PDF Kitaplık')">
        <span class="tab-icon">📚</span>
        <span class="tab-label">Kitaplık</span>
      </button>

      <button class="tab-btn" id="btn-tab-settings" onclick="switchTab('tab-settings', 'Ayarlar')">
        <span class="tab-icon">⚙️</span>
        <span class="tab-label">Ayarlar</span>
      </button>
    </nav>
  </div>

  <script>
  // Global Error Handler - Herhangi bir JS hatasını iPad ekranında gösterir
  window.onerror = function (msg, url, line) {
    var b = document.getElementById('debug-error-bar');
    if (b) {
      b.style.display = 'block';
      b.innerHTML = '⚠️ Hata: ' + msg + ' (Satır: ' + line + ') <button onclick="this.parentNode.style.display=\'none\'" style="margin-left:10px;padding:2px 6px;background:#fff;color:#000;border:none;border-radius:4px;">Kapat</button>';
    }
    return false;
  };

  // Resim hata yakalayıcıları (Inline onerror için)
  window.hideImgError = function (img) {
    if (img) img.style.display = 'none';
  };
  window.thumbImgError = function (img) {
    if (img) img.src = 'apple-touch-icon-76x76.png';
  };

  // TV Kanalları Verisi
  var allChannels = ''' + channels_json_str + ''';
  var currentFilteredChannels = allChannels;

  // Curated YouTube Videoları
  var allVideos = [
    { id: "GUKIEjmQ1Bc", category: "muzik", title: "Barış Manço - Müsaadenizle Çocuklar (Klasik)", author: "Barış Manço" },
    { id: "V-_O7nl0Ii0", category: "muzik", title: "Tarkan - Kış Güneşi (Canlı Performans)", author: "Tarkan" },
    { id: "jfKfPfyJRdk", category: "muzik", title: "Lofi Hip Hop Radio - Chill Beats to Relax/Study", author: "Lofi Girl" },
    { id: "hT_nvWreIhg", category: "muzik", title: "OneRepublic - Counting Stars (Official Music Video)", author: "OneRepublic" },
    { id: "q36b7q9g2e8", category: "muzik", title: "Barış Manço - Gülpembe (Orijinal Klip)", author: "Barış Manço" },
    { id: "L_LUpnjgPso", category: "nostalji", title: "Hababam Sınıfı Efsane Sahneler", author: "Arzu Film" },
    { id: "tP80n7P_30w", category: "nostalji", title: "Tosun Paşa - Yeşil Vadi Bizimdir Sahneleri", author: "Arzu Film" },
    { id: "cOqQ-i5K-9U", category: "nostalji", title: "Şaban Oğlu Şaban - En Komik Anlar", author: "Arzu Film" },
    { id: "5T6XbC8Vz3k", category: "nostalji", title: "Zeki Alasya & Metin Akpınar Klasikleri", author: "Yeşilçam" },
    { id: "0wUaEwK43rI", category: "cizgifilm", title: "Rafadan Tayfa - Görevimiz Macera", author: "TRT Çocuk" },
    { id: "J9mY4iG3z8A", category: "cizgifilm", title: "Keloğlan Masalları - Devler Diyarı", author: "TRT Çocuk" },
    { id: "1L9h_4xJ6sE", category: "cizgifilm", title: "Niloya - Şarkılar ve Oyunlar", author: "Niloya" },
    { id: "D8g-B8cO7iE", category: "belgesel", title: "Doğanın Harikaları - Vahşi Yaşam Belgeseli", author: "BBC Earth Türkçe" },
    { id: "bQ-3k5L1_q8", category: "belgesel", title: "Anadolu Medeniyetleri ve Tarih", author: "TRT Belgesel" }
  ];
  var currentFilteredVideos = allVideos;

  // 1. SEKME DEĞİŞTİRME FONKSİYONU
  window.switchTab = function (tabId, title) {
    try {
      var tabs = ['tab-tv', 'tab-youtube', 'tab-pdf', 'tab-settings'];
      for (var i = 0; i < tabs.length; i++) {
        var pane = document.getElementById(tabs[i]);
        var btn = document.getElementById('btn-' + tabs[i]);
        if (pane) {
          if (tabs[i] === tabId) {
            pane.className = 'tab-pane active';
          } else {
            pane.className = 'tab-pane';
          }
        }
        if (btn) {
          if (tabs[i] === tabId) {
            btn.className = 'tab-btn active';
          } else {
            btn.className = 'tab-btn';
          }
        }
      }
      var titleElem = document.getElementById('current-view-title');
      if (titleElem) titleElem.textContent = title;
      window.scrollTo(0, 0);
    } catch (e) {
      console.error(e);
    }
  };

  // 2. CANLI TV İŞLEMLERİ
  var tvPlayer = document.getElementById('tv-player');
  var tvPlayingTitle = document.getElementById('tv-playing-title');
  var globalStatus = document.getElementById('global-status');
  var tvGrid = document.getElementById('tv-channels-grid');
  var activeChIndex = -1;

  window.renderChannels = function (channels) {
    if (!tvGrid) return;
    currentFilteredChannels = channels;
    var html = '';
    for (var i = 0; i < channels.length; i++) {
      var ch = channels[i];
      var isActive = (i === activeChIndex) ? ' active' : '';
      var logoHtml = '';
      if (ch.logo && ch.logo.indexOf('http') === 0) {
        logoHtml = '<img class="ch-logo" src="' + ch.logo + '" alt="' + escapeHtml(ch.name) + '" onerror="hideImgError(this)">';
      } else {
        logoHtml = '<div class="ch-placeholder">📺</div>';
      }
      html += '<button type="button" class="ch-card" onclick="playChannelIndex(' + i + ')">' +
                '<div class="ch-inner' + isActive + '" id="ch-inner-' + i + '">' +
                  logoHtml +
                  '<div class="ch-name">' + escapeHtml(ch.name) + '</div>' +
                '</div>' +
              '</button>';
    }
    tvGrid.innerHTML = html;
  };

  window.playChannelIndex = function (index) {
    try {
      var ch = currentFilteredChannels[index];
      if (!ch) return;
      activeChIndex = index;

      var inners = document.querySelectorAll('.ch-inner');
      for (var i = 0; i < inners.length; i++) inners[i].className = 'ch-inner';
      var currentInner = document.getElementById('ch-inner-' + index);
      if (currentInner) currentInner.className = 'ch-inner active';

      if (tvPlayingTitle) tvPlayingTitle.textContent = 'Oynatılıyor: ' + ch.name;
      if (globalStatus) {
        globalStatus.textContent = 'Yayın Açılıyor...';
        globalStatus.style.backgroundColor = '#f59e0b';
      }

      if (tvPlayer) {
        tvPlayer.src = ch.url;
        tvPlayer.load();
        try {
          var p = tvPlayer.play();
          if (p && typeof p.catch === 'function') {
            p.catch(function () {
              if (globalStatus) {
                globalStatus.textContent = 'Oynat tuşuna basın';
                globalStatus.style.backgroundColor = '#64748b';
              }
            });
          }
        } catch (e) {
          if (globalStatus) {
            globalStatus.textContent = 'Oynat tuşuna basın';
            globalStatus.style.backgroundColor = '#64748b';
          }
        }
      }
      window.scrollTo(0, 0);
    } catch (err) {
      console.error(err);
    }
  };

  window.filterChannels = function () {
    try {
      var input = document.getElementById('tv-search');
      var q = (input ? input.value : '').toLowerCase().trim();
      if (!q) {
        window.renderChannels(allChannels);
        return;
      }
      var filtered = [];
      for (var i = 0; i < allChannels.length; i++) {
        var name = (allChannels[i].name || '').toLowerCase();
        var full = (allChannels[i].fullName || '').toLowerCase();
        if (name.indexOf(q) !== -1 || full.indexOf(q) !== -1) {
          filtered.push(allChannels[i]);
        }
      }
      window.renderChannels(filtered);
    } catch (e) {
      console.error(e);
    }
  };

  if (tvPlayer) {
    tvPlayer.addEventListener('playing', function () {
      if (globalStatus) {
        globalStatus.textContent = 'Canlı Yayın';
        globalStatus.style.backgroundColor = '#10b981';
      }
    });
    tvPlayer.addEventListener('error', function () {
      if (globalStatus) {
        globalStatus.textContent = 'Yayın Hatası';
        globalStatus.style.backgroundColor = '#ef4444';
      }
    });
  }

  // 3. YOUTUBE İŞLEMLERİ
  var ytPlayerContainer = document.getElementById('yt-player-container');
  var ytInfoBar = document.getElementById('yt-info-bar');
  var ytCurrentTitle = document.getElementById('yt-current-title');
  var ytCurrentAuthor = document.getElementById('yt-current-author');
  var ytGrid = document.getElementById('yt-videos-grid');
  var currentYTCategory = 'all';

  window.renderYTVideos = function (videos) {
    if (!ytGrid) return;
    currentFilteredVideos = videos;
    var html = '';
    for (var i = 0; i < videos.length; i++) {
      var v = videos[i];
      var thumb = 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';
      var escTitle = escapeHtml(v.title);
      var escAuthor = escapeHtml(v.author || 'YouTube');
      html += '<button type="button" class="v-card" onclick="playVideoIndex(' + i + ')">' +
                '<div class="v-inner">' +
                  '<div class="v-thumb">' +
                    '<img src="' + thumb + '" alt="' + escTitle + '" onerror="thumbImgError(this)">' +
                  '</div>' +
                  '<div class="v-info">' +
                    '<div class="v-title">' + escTitle + '</div>' +
                    '<div class="v-author">' + escAuthor + '</div>' +
                  '</div>' +
                '</div>' +
              '</button>';
    }
    ytGrid.innerHTML = html;
  };

  window.playVideoIndex = function (index) {
    try {
      var v = currentFilteredVideos[index];
      if (!v) return;
      window.playYT(v.id, v.title, v.author);
    } catch (e) {
      console.error(e);
    }
  };

  window.playYT = function (id, title, author) {
    try {
      if (ytCurrentTitle) ytCurrentTitle.textContent = title;
      if (ytCurrentAuthor) ytCurrentAuthor.textContent = author || 'YouTube';
      if (ytInfoBar) ytInfoBar.style.display = 'block';

      if (ytPlayerContainer) {
        ytPlayerContainer.innerHTML = 
          '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1&rel=0&modestbranding=1" ' +
          'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' +
          'allowfullscreen webkitallowfullscreen></iframe>';
      }

      if (globalStatus) {
        globalStatus.textContent = 'Oynatılıyor';
        globalStatus.style.backgroundColor = '#10b981';
      }
      window.scrollTo(0, 0);
    } catch (e) {
      console.error(e);
    }
  };

  window.selectYTChip = function (btn, category) {
    try {
      var chips = document.querySelectorAll('.chip-btn');
      for (var i = 0; i < chips.length; i++) chips[i].className = 'chip-btn';
      if (btn) btn.className = 'chip-btn active';
      currentYTCategory = category;

      if (category === 'all') {
        window.renderYTVideos(allVideos);
      } else {
        var filtered = [];
        for (var j = 0; j < allVideos.length; j++) {
          if (allVideos[j].category === category) filtered.push(allVideos[j]);
        }
        window.renderYTVideos(filtered);
      }
    } catch (e) {
      console.error(e);
    }
  };

  window.handleYTSearch = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    try {
      var input = document.getElementById('yt-search-input');
      var q = (input ? input.value : '').trim();
      if (!q) return;

      // YouTube Link veya ID kontrolü
      var match = q.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i);
      if (match && match[1]) {
        window.playYT(match[1], "Seçilen Video", "YouTube");
        return;
      }

      // 11 haneli direkt video ID kontrolü
      if (/^[a-zA-Z0-9_-]{11}$/.test(q)) {
        window.playYT(q, "Video: " + q, "YouTube");
        return;
      }

      // Başlık araması
      var lowerQ = q.toLowerCase();
      var found = [];
      for (var i = 0; i < allVideos.length; i++) {
        if (allVideos[i].title.toLowerCase().indexOf(lowerQ) !== -1 ||
            (allVideos[i].author && allVideos[i].author.toLowerCase().indexOf(lowerQ) !== -1)) {
          found.push(allVideos[i]);
        }
      }

      if (found.length > 0) {
        window.renderYTVideos(found);
      } else {
        if (ytGrid) {
          ytGrid.innerHTML = 
            '<div style="width:100%; text-align:center; padding:30px 10px; color:#94a3b8;">' +
              '<div style="font-size:16px; font-weight:bold; color:#f8fafc; margin-bottom:10px;">"' + escapeHtml(q) + '" için kayıtlı video bulunamadı</div>' +
              '<p style="margin-bottom:14px; font-size:13px;">Dilediğiniz videonun YouTube linkini yukarıdaki kutuya yapıştırıp "Oynat"a basabilirsiniz.</p>' +
              '<a href="https://m.youtube.com/results?search_query=' + encodeURIComponent(q) + '" target="_blank" style="display:inline-block; background:#ef4444; color:#fff; padding:8px 16px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:13px;">YouTube Mobil\'de Ara ↗</a>' +
            '</div>';
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // İlk Yükleme Başlatma
  try {
    window.renderChannels(allChannels);
    if (allChannels.length > 0) {
      var first = allChannels[0];
      if (tvPlayingTitle) tvPlayingTitle.textContent = first.name;
      if (tvPlayer) tvPlayer.src = first.url;
    }
    window.renderYTVideos(allVideos);
  } catch (initErr) {
    console.error('Init error:', initErr);
  }
  </script>
</body>
</html>'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated clean index.html successfully!")
