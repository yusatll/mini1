import json

with open("portal/channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

channels_js_str = json.dumps(channels, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="tr" manifest="offline.appcache">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="iPad Hub">
  <title>iPad Hub - Canlı TV, YouTube & Kitaplık</title>
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <style>
    /* Reset & Temel Ayarlar - Tamamen Dahili (Inline) CSS */
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      background-color: #0b0f19;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 15px;
      line-height: 1.4;
      overflow-x: hidden;
      padding-bottom: 75px;
    }}

    .app-layout {{
      max-width: 900px;
      margin: 0 auto;
    }}

    /* Üst Başlık Barı */
    .top-nav {{
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
    }}

    .app-brand {{
      display: -webkit-flex;
      display: flex;
      -webkit-align-items: center;
      align-items: center;
      gap: 8px;
    }}

    .brand-logo {{ font-size: 20px; }}
    .brand-name {{
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
    }}

    .status-indicator {{
      font-size: 11px;
      background-color: #10b981;
      color: #ffffff;
      padding: 3px 9px;
      border-radius: 12px;
      font-weight: 600;
    }}

    /* Sekmeler */
    .content-viewport {{
      padding: 12px 14px;
    }}

    .tab-pane {{
      display: none;
    }}

    .tab-pane.active {{
      display: block;
    }}

    /* Video Player */
    .player-box {{
      background-color: #000000;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid #1e293b;
      margin-bottom: 14px;
    }}

    .video-aspect {{
      position: relative;
      width: 100%;
      height: 0;
      padding-bottom: 56.25%; /* 16:9 */
      background-color: #000000;
    }}

    .video-aspect video, .video-aspect iframe {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
    }}

    .player-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 8px 12px;
      background: -webkit-linear-gradient(bottom, rgba(0,0,0,0.85), rgba(0,0,0,0));
      background: linear-gradient(to top, rgba(0,0,0,0.85), rgba(0,0,0,0));
      pointer-events: none;
    }}

    #tv-playing-title {{
      font-size: 14px;
      font-weight: 600;
      color: #38bdf8;
    }}

    .yt-placeholder {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      display: -webkit-flex; display: flex;
      -webkit-align-items: center; align-items: center;
      -webkit-justify-content: center; justify-content: center;
      color: #64748b; font-size: 14px; text-align: center; padding: 20px;
    }}

    .yt-info-bar {{
      padding: 8px 12px;
      background-color: #161b26;
      border-top: 1px solid #1e293b;
    }}

    #yt-current-title {{ font-size: 14px; color: #f8fafc; margin-bottom: 2px; }}
    #yt-current-author {{ font-size: 12px; color: #94a3b8; }}

    /* Arama Çubukları */
    .search-wrap {{
      margin-bottom: 12px;
    }}

    .search-wrap input {{
      width: 100%;
      padding: 12px 14px;
      background-color: #1e293b;
      border: 1px solid #334155;
      border-radius: 10px;
      color: #ffffff;
      font-size: 15px;
      outline: none;
    }}

    .yt-search-form {{
      display: -webkit-flex;
      display: flex;
      gap: 8px;
    }}

    .yt-search-form input {{
      -webkit-flex: 1;
      flex: 1;
    }}

    #yt-search-btn {{
      background-color: #ef4444;
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 0 16px;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
    }}

    .quick-chips {{
      display: -webkit-flex;
      display: flex;
      overflow-x: auto;
      gap: 8px;
      padding-bottom: 10px;
      margin-bottom: 10px;
    }}

    .chip-btn {{
      background-color: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 6px 14px;
      border-radius: 16px;
      font-size: 12px;
      white-space: nowrap;
      cursor: pointer;
    }}

    .chip-btn.active {{
      background-color: #38bdf8;
      color: #0f172a;
      border-color: #38bdf8;
      font-weight: 700;
    }}

    /* TV Kanal Grid */
    .channels-list-grid {{
      display: -webkit-flex;
      display: flex;
      -webkit-flex-wrap: wrap;
      flex-wrap: wrap;
      margin: -5px;
    }}

    .ch-card {{
      width: 25%;
      padding: 5px;
      box-sizing: border-box;
      cursor: pointer;
    }}

    @media (max-width: 600px) {{
      .ch-card {{ width: 33.33%; }}
    }}

    .ch-inner {{
      background-color: #161f30;
      border: 1px solid #233047;
      border-radius: 10px;
      padding: 12px 6px;
      text-align: center;
      height: 100%;
      display: -webkit-flex;
      display: flex;
      -webkit-flex-direction: column;
      flex-direction: column;
      -webkit-align-items: center;
      align-items: center;
      -webkit-justify-content: center;
      justify-content: center;
      transition: background-color 0.15s;
    }}

    .ch-inner.active, .ch-inner:active {{
      background-color: #1e3a5f;
      border-color: #38bdf8;
    }}

    .ch-logo {{
      max-width: 44px;
      max-height: 28px;
      margin-bottom: 6px;
      object-fit: contain;
    }}

    .ch-placeholder {{
      font-size: 20px;
      margin-bottom: 6px;
    }}

    .ch-name {{
      font-size: 12px;
      font-weight: 600;
      color: #f1f5f9;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      width: 100%;
    }}

    /* YouTube Video Grid */
    .videos-list-grid {{
      display: -webkit-flex;
      display: flex;
      -webkit-flex-wrap: wrap;
      flex-wrap: wrap;
      margin: -5px;
    }}

    .v-card {{
      width: 50%;
      padding: 5px;
      box-sizing: border-box;
      cursor: pointer;
    }}

    @media (max-width: 500px) {{
      .v-card {{ width: 100%; }}
    }}

    .v-inner {{
      background-color: #161b26;
      border: 1px solid #233047;
      border-radius: 10px;
      overflow: hidden;
    }}

    .v-thumb {{
      position: relative;
      width: 100%;
      height: 0;
      padding-bottom: 56.25%;
      background-color: #000;
    }}

    .v-thumb img {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
    }}

    .v-info {{ padding: 8px; }}
    .v-title {{
      font-size: 12px;
      font-weight: 600;
      color: #f1f5f9;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin-bottom: 3px;
    }}
    .v-author {{ font-size: 11px; color: #94a3b8; }}

    /* PDF / Kitaplık */
    .guide-box {{
      background-color: #162032;
      border: 1px solid #1e3a5f;
      border-radius: 10px;
      padding: 12px;
      display: -webkit-flex;
      display: flex;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .guide-icon {{ font-size: 24px; }}
    .guide-desc {{ font-size: 13px; color: #cbd5e1; line-height: 1.4; }}

    .pane-subtitle {{
      font-size: 16px;
      font-weight: 600;
      color: #e2e8f0;
      margin-bottom: 10px;
    }}

    .books-container {{
      display: -webkit-flex;
      display: flex;
      -webkit-flex-direction: column;
      flex-direction: column;
      gap: 8px;
    }}

    .book-row {{
      background-color: #161f30;
      border: 1px solid #233047;
      border-radius: 8px;
      padding: 12px 14px;
      display: -webkit-flex;
      display: flex;
      -webkit-align-items: center;
      align-items: center;
      -webkit-justify-content: space-between;
      justify-content: space-between;
    }}

    .book-meta {{
      display: -webkit-flex;
      display: flex;
      -webkit-align-items: center;
      align-items: center;
      gap: 10px;
    }}

    .book-meta-icon {{ font-size: 24px; }}
    .book-meta-name {{ font-size: 14px; font-weight: 600; color: #fff; }}
    .book-meta-size {{ font-size: 11px; color: #94a3b8; }}

    .btn-open {{
      background-color: #2563eb;
      color: #fff;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 6px;
      display: inline-block;
    }}

    /* Ayarlar */
    .settings-list {{
      display: -webkit-flex;
      display: flex;
      -webkit-flex-direction: column;
      flex-direction: column;
      gap: 10px;
    }}

    .setting-item {{
      display: -webkit-flex;
      display: flex;
      -webkit-align-items: center;
      align-items: center;
      background-color: #161f30;
      border: 1px solid #233047;
      border-radius: 10px;
      padding: 12px 14px;
      text-decoration: none;
      color: #f1f5f9;
    }}

    .item-icon {{ font-size: 24px; margin-right: 12px; }}
    .item-details strong {{ display: block; font-size: 14px; color: #fff; margin-bottom: 2px; }}
    .item-details span {{ font-size: 12px; color: #94a3b8; }}

    .tip-card {{
      background-color: #162032;
      border: 1px solid #1e3a5f;
      border-radius: 10px;
      padding: 14px;
      font-size: 13px;
      line-height: 1.6;
    }}

    /* Sabit Alt Sekme Barı */
    .bottom-tab-bar {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 60px;
      background-color: #111827;
      border-top: 1px solid #1f2937;
      display: -webkit-flex;
      display: flex;
      z-index: 200;
      box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
    }}

    .tab-btn {{
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
    }}

    .tab-btn.active {{
      color: #38bdf8;
    }}

    .tab-icon {{
      font-size: 20px;
      margin-bottom: 2px;
    }}

    .tab-yt {{ color: #ef4444; font-size: 16px; }}

    .tab-label {{
      font-size: 11px;
      font-weight: 600;
    }}
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
            <a class="btn-open" href="/books/iPad_Mini_1_Rehberi.pdf" target="_blank">Aç / Oku</a>
          </div>
        </div>
      </section>

      <!-- 4. AYARLAR -->
      <section class="tab-pane" id="tab-settings">
        <h3 class="pane-subtitle">Sistem ve Güvenlik Araçları</h3>
        <div class="settings-list">
          <a href="/certs/isrgrootx1.der" class="setting-item" download>
            <span class="item-icon">🔒</span>
            <div class="item-details">
              <strong>ISRG Root X1 SSL Sertifikasını Kur</strong>
              <span>iOS 9'da güncel sitelerin ve yayınların SSL hatasını çözer.</span>
            </div>
          </a>

          <a href="/playlists/kanallar.m3u" class="setting-item" download>
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
  // DAHİLİ KANAL VERİSİ (Ağ gerektirmez, Mac kapalıyken de hafızadadır)
  var allChannels = {channels_js_str};

  // DAHİLİ YOUTUBE ÖNERİ LİSTESİ
  var curatedYT = [
    {{ id: "GUKIEjmQ1Bc", title: "Barış Manço - Müsaadenizle Çocuklar (Klasik)", author: "Barış Manço" }},
    {{ id: "L_LUpnjgPso", title: "Hababam Sınıfı Efsane Sahneler", author: "Arzu Film" }},
    {{ id: "V-_O7nl0Ii0", title: "Tarkan - Kış Güneşi (Canlı)", author: "Tarkan" }},
    {{ id: "jfKfPfyJRdk", title: "Lofi Hip Hop Radio - Chill Beats", author: "Lofi Girl" }},
    {{ id: "hT_nvWreIhg", title: "OneRepublic - Counting Stars", author: "OneRepublic" }}
  ];

  (function () {{
    var globalStatus = document.getElementById("global-status");
    var currentViewTitle = document.getElementById("current-view-title");
    var tabButtons = document.querySelectorAll(".tab-btn");
    var tabPanes = document.querySelectorAll(".tab-pane");

    // 1. SEKME GEÇİŞLERİ (Sıfır Ağ, Anında Geçiş)
    for (var i = 0; i < tabButtons.length; i++) {{
      tabButtons[i].addEventListener("click", function () {{
        var targetTab = this.getAttribute("data-tab");
        var title = this.getAttribute("data-title");

        for (var j = 0; j < tabButtons.length; j++) {{
          tabButtons[j].className = "tab-btn";
        }}
        this.className = "tab-btn active";

        for (var k = 0; k < tabPanes.length; k++) {{
          tabPanes[k].className = "tab-pane";
        }}
        var activePane = document.getElementById(targetTab);
        if (activePane) activePane.className = "tab-pane active";

        currentViewTitle.textContent = title;
        window.scrollTo(0, 0);
      }});
    }}

    // 2. CANLI TV İŞLEMLERİ
    var tvPlayer = document.getElementById("tv-player");
    var tvPlayingTitle = document.getElementById("tv-playing-title");
    var tvSearch = document.getElementById("tv-search");
    var tvGrid = document.getElementById("tv-channels-grid");
    var activeChCard = null;

    function renderChannels(channels) {{
      tvGrid.innerHTML = "";
      for (var i = 0; i < channels.length; i++) {{
        var ch = channels[i];
        var card = document.createElement("div");
        card.className = "ch-card";

        var inner = document.createElement("div");
        inner.className = "ch-inner";

        if (ch.logo && ch.logo.indexOf("http") === 0) {{
          var img = document.createElement("img");
          img.className = "ch-logo";
          img.src = ch.logo;
          img.alt = ch.name;
          img.onerror = function () {{ this.style.display = "none"; }};
          inner.appendChild(img);
        }} else {{
          var ph = document.createElement("div");
          ph.className = "ch-placeholder";
          ph.textContent = "📺";
          inner.appendChild(ph);
        }}

        var nameDiv = document.createElement("div");
        nameDiv.className = "ch-name";
        nameDiv.textContent = ch.name;
        inner.appendChild(nameDiv);

        card.appendChild(inner);

        (function (channelData, cardInner) {{
          card.addEventListener("click", function () {{
            prepareTV(channelData, cardInner, true);
          }});
        }})(ch, inner);

        tvGrid.appendChild(card);
      }}
    }}

    function prepareTV(ch, cardInner, autoPlay) {{
      if (activeChCard) activeChCard.className = "ch-inner";
      if (cardInner) {{
        cardInner.className = "ch-inner active";
        activeChCard = cardInner;
      }}

      tvPlayingTitle.textContent = "Oynatılıyor: " + ch.name;
      globalStatus.textContent = "Bağlanıyor...";
      globalStatus.style.backgroundColor = "#f59e0b";

      tvPlayer.src = ch.url;
      tvPlayer.load();

      if (autoPlay) {{
        var p = tvPlayer.play();
        if (p !== undefined) {{
          p.catch(function () {{
            globalStatus.textContent = "Oynat tuşuna basın";
            globalStatus.style.backgroundColor = "#64748b";
          }});
        }}
      }}
    }}

    tvSearch.addEventListener("input", function () {{
      var q = tvSearch.value.toLowerCase().trim();
      if (!q) {{ renderChannels(allChannels); return; }}
      var filtered = [];
      for (var i = 0; i < allChannels.length; i++) {{
        if (allChannels[i].name.toLowerCase().indexOf(q) !== -1) {{
          filtered.push(allChannels[i]);
        }}
      }}
      renderChannels(filtered);
    }});

    tvPlayer.addEventListener("playing", function () {{
      globalStatus.textContent = "Canlı Yayın";
      globalStatus.style.backgroundColor = "#10b981";
    }});

    tvPlayer.addEventListener("error", function () {{
      globalStatus.textContent = "Yayın Hatası";
      globalStatus.style.backgroundColor = "#ef4444";
    }});

    // İlk kanalları yükle
    renderChannels(allChannels);
    if (allChannels.length > 0) {{
      prepareTV(allChannels[0], null, false);
    }}

    // 3. YOUTUBE İŞLEMLERİ
    var ytSearchForm = document.getElementById("yt-search-form");
    var ytSearchInput = document.getElementById("yt-search-input");
    var ytPlayerContainer = document.getElementById("yt-player-container");
    var ytInfoBar = document.getElementById("yt-info-bar");
    var ytCurrentTitle = document.getElementById("yt-current-title");
    var ytCurrentAuthor = document.getElementById("yt-current-author");
    var ytGrid = document.getElementById("yt-videos-grid");
    var chipButtons = document.querySelectorAll(".chip-btn");

    function renderYTVideos(videos) {{
      ytGrid.innerHTML = "";
      for (var i = 0; i < videos.length; i++) {{
        var v = videos[i];
        var card = document.createElement("div");
        card.className = "v-card";
        var thumb = "https://i.ytimg.com/vi/" + v.id + "/hqdefault.jpg";

        card.innerHTML = 
          "<div class=\"v-inner\">" +
            "<div class=\"v-thumb\">" +
              "<img src=\"" + thumb + "\" alt=\"" + escapeHtml(v.title) + "\" onerror=\"this.src=\\'https://i.ytimg.com/vi/" + v.id + "/default.jpg\\'\">" +
            "</div>" +
            "<div class=\"v-info\">" +
              "<div class=\"v-title\">" + escapeHtml(v.title) + "</div>" +
              "<div class=\"v-author\">" + escapeHtml(v.author || "YouTube") + "</div>" +
            "</div>" +
          "</div>";

        (function (vid) {{
          card.addEventListener("click", function () {{
            playYT(vid.id, vid.title, vid.author);
          }});
        }})(v);

        ytGrid.appendChild(card);
      }}
    }}

    function playYT(id, title, author) {{
      ytCurrentTitle.textContent = title;
      ytCurrentAuthor.textContent = author || "YouTube";
      ytInfoBar.style.display = "block";

      ytPlayerContainer.innerHTML = 
        "<iframe src=\"https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&playsinline=1&rel=0&modestbranding=1\" " +
        "allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" " +
        "allowfullscreen webkitallowfullscreen></iframe>";

      globalStatus.textContent = "Oynatılıyor";
      globalStatus.style.backgroundColor = "#10b981";
    }}

    ytSearchForm.addEventListener("submit", function (e) {{
      e.preventDefault();
      var q = ytSearchInput.value.trim();
      if (!q) return;

      var match = q.match(/(?:youtube\\.com\\/(?:[^\\/]+\\/.+\\/|(?:v|e(?:mbed)?)\\/|.*[?&]v=)|youtu\\.be\\/)([^"&?\\/\\s]{{11}})/i);
      if (match && match[1]) {{
        playYT(match[1], "Video", "YouTube");
        return;
      }}
      searchYT(q);
    }});

    for (var i = 0; i < chipButtons.length; i++) {{
      chipButtons[i].addEventListener("click", function () {{
        for (var j = 0; j < chipButtons.length; j++) chipButtons[j].className = "chip-btn";
        this.className = "chip-btn active";
        var q = this.getAttribute("data-q");
        ytSearchInput.value = q;
        searchYT(q);
      }});
    }}

    function searchYT(query) {{
      globalStatus.textContent = "Aranıyor...";
      globalStatus.style.backgroundColor = "#f59e0b";
      ytGrid.innerHTML = "<div style=\"width:100%; text-align:center; padding:20px; color:#64748b;\">Videolar aranıyor...</div>";

      var xhr = new XMLHttpRequest();
      xhr.open("GET", "/api/youtube?q=" + encodeURIComponent(query), true);
      xhr.timeout = 5000;
      xhr.onload = function () {{
        if (xhr.status === 200) {{
          try {{
            var res = JSON.parse(xhr.responseText);
            if (res && res.length > 0) {{
              renderYTVideos(res);
              globalStatus.textContent = "Hazır";
              globalStatus.style.backgroundColor = "#10b981";
              return;
            }}
          }} catch (e) {{}}
        }}
        renderYTVideos(curatedYT);
      }};
      xhr.onerror = function () {{ renderYTVideos(curatedYT); }};
      xhr.ontimeout = function () {{ renderYTVideos(curatedYT); }};
      xhr.send();
    }}

    renderYTVideos(curatedYT);

    function escapeHtml(text) {{
      if (!text) return "";
      return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }}
  }})();
  </script>
</body>
</html>
"""

with open("portal/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Tamamen dahili portal/index.html basariyla olusturuldu!")
