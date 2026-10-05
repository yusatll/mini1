// iPad mini 1 (iOS 9) Tek Birleşik Uygulama - Vanilla ES5
(function () {
  // Global Elements
  var globalStatus = document.getElementById('global-status');
  var currentViewTitle = document.getElementById('current-view-title');
  var tabButtons = document.querySelectorAll('.tab-btn');
  var tabPanes = document.querySelectorAll('.tab-pane');

  // TV Elements
  var tvPlayer = document.getElementById('tv-player');
  var tvOverlay = document.getElementById('tv-overlay');
  var tvPlayingTitle = document.getElementById('tv-playing-title');
  var tvSearch = document.getElementById('tv-search');
  var tvGrid = document.getElementById('tv-channels-grid');
  var allChannels = (typeof window.allChannels !== 'undefined' && window.allChannels && window.allChannels.length > 0) ? window.allChannels : [];
  var activeChCard = null;

  // YouTube Elements
  var ytSearchForm = document.getElementById('yt-search-form');
  var ytSearchInput = document.getElementById('yt-search-input');
  var ytPlayerContainer = document.getElementById('yt-player-container');
  var ytInfoBar = document.getElementById('yt-info-bar');
  var ytCurrentTitle = document.getElementById('yt-current-title');
  var ytCurrentAuthor = document.getElementById('yt-current-author');
  var ytGrid = document.getElementById('yt-videos-grid');
  var chipButtons = document.querySelectorAll('.chip-btn');

  // PDF Elements
  var pdfUploadFile = document.getElementById('pdf-upload-file');
  var pdfUploadStatus = document.getElementById('pdf-upload-status');
  var booksList = document.getElementById('books-list');

  // ==========================================
  // 1. SEKME YÖNETİMİ (TAB SWITCHING)
  // ==========================================
  for (var i = 0; i < tabButtons.length; i++) {
    tabButtons[i].addEventListener('click', function () {
      var targetTab = this.getAttribute('data-tab');
      var title = this.getAttribute('data-title');

      // Buton aktifliği
      for (var j = 0; j < tabButtons.length; j++) {
        tabButtons[j].className = 'tab-btn';
      }
      this.className = 'tab-btn active';

      // Sekme içeriği
      for (var k = 0; k < tabPanes.length; k++) {
        tabPanes[k].className = 'tab-pane';
      }
      var activePane = document.getElementById(targetTab);
      if (activePane) activePane.className = 'tab-pane active';

      currentViewTitle.textContent = title;
      window.scrollTo(0, 0);
    });
  }

  // ==========================================
  // 2. CANLI TV İŞLEMLERİ
  // ==========================================
  function initTV() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'channels.json', true);
    xhr.onload = function () {
      if (xhr.status === 200 || xhr.status === 0) {
        try {
          allChannels = JSON.parse(xhr.responseText);
          renderChannels(allChannels);
          if (allChannels.length > 0) {
            prepareTV(allChannels[0], null, false);
          }
        } catch (e) {
          console.error(e);
        }
      }
    };
    xhr.send();

    tvSearch.addEventListener('input', function () {
      var q = tvSearch.value.toLowerCase().trim();
      if (!q) { renderChannels(allChannels); return; }
      var filtered = [];
      for (var i = 0; i < allChannels.length; i++) {
        if (allChannels[i].name.toLowerCase().indexOf(q) !== -1) {
          filtered.push(allChannels[i]);
        }
      }
      renderChannels(filtered);
    });

    tvPlayer.addEventListener('playing', function () {
      globalStatus.textContent = 'Canlı Yayın';
      globalStatus.style.backgroundColor = '#10b981';
    });

    tvPlayer.addEventListener('error', function () {
      globalStatus.textContent = 'Yayın Hatası';
      globalStatus.style.backgroundColor = '#ef4444';
    });
  }

  function renderChannels(channels) {
    tvGrid.innerHTML = '';
    for (var i = 0; i < channels.length; i++) {
      var ch = channels[i];
      var card = document.createElement('div');
      card.className = 'ch-card';

      var inner = document.createElement('div');
      inner.className = 'ch-inner';

      if (ch.logo && ch.logo.indexOf('http') === 0) {
        var img = document.createElement('img');
        img.className = 'ch-logo';
        img.src = ch.logo;
        img.alt = ch.name;
        img.onerror = function () { this.style.display = 'none'; };
        inner.appendChild(img);
      } else {
        var ph = document.createElement('div');
        ph.className = 'ch-placeholder';
        ph.textContent = '📺';
        inner.appendChild(ph);
      }

      var nameDiv = document.createElement('div');
      nameDiv.className = 'ch-name';
      nameDiv.textContent = ch.name;
      inner.appendChild(nameDiv);

      card.appendChild(inner);

      (function (channelData, cardInner) {
        card.addEventListener('click', function () {
          prepareTV(channelData, cardInner, true);
        });
      })(ch, inner);

      tvGrid.appendChild(card);
    }
  }

  function prepareTV(ch, cardInner, autoPlay) {
    if (activeChCard) activeChCard.className = 'ch-inner';
    if (cardInner) {
      cardInner.className = 'ch-inner active';
      activeChCard = cardInner;
    }

    tvPlayingTitle.textContent = 'Oynatılıyor: ' + ch.name;
    globalStatus.textContent = 'Bağlanıyor...';
    globalStatus.style.backgroundColor = '#f59e0b';

    tvPlayer.src = ch.url;
    tvPlayer.load();

    if (autoPlay) {
      var p = tvPlayer.play();
      if (p !== undefined) {
        p.catch(function () {
          globalStatus.textContent = 'Oynat tuşuna basın';
          globalStatus.style.backgroundColor = '#64748b';
        });
      }
    }
  }

  // ==========================================
  // 3. LITE YOUTUBE İŞLEMLERİ
  // ==========================================
  var curatedYT = [
    { id: "GUKIEjmQ1Bc", title: "Barış Manço - Müsaadenizle Çocuklar (Klasik)", author: "Barış Manço" },
    { id: "L_LUpnjgPso", title: "Hababam Sınıfı Efsane Sahneler", author: "Arzu Film" },
    { id: "V-_O7nl0Ii0", title: "Tarkan - Kış Güneşi (Canlı)", author: "Tarkan" },
    { id: "jfKfPfyJRdk", title: "Lofi Hip Hop Radio - Chill Beats", author: "Lofi Girl" },
    { id: "hT_nvWreIhg", title: "OneRepublic - Counting Stars", author: "OneRepublic" }
  ];

  function initYT() {
    renderYTVideos(curatedYT);

    ytSearchForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = ytSearchInput.value.trim();
      if (!q) return;

      var match = q.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i);
      if (match && match[1]) {
        playYT(match[1], "Video", "YouTube");
        return;
      }
      searchYT(q);
    });

    for (var i = 0; i < chipButtons.length; i++) {
      chipButtons[i].addEventListener('click', function () {
        for (var j = 0; j < chipButtons.length; j++) chipButtons[j].className = 'chip-btn';
        this.className = 'chip-btn active';
        var q = this.getAttribute('data-q');
        ytSearchInput.value = q;
        searchYT(q);
      });
    }
  }

  function searchYT(query) {
    globalStatus.textContent = 'Aranıyor...';
    globalStatus.style.backgroundColor = '#f59e0b';
    ytGrid.innerHTML = '<div style="width:100%; text-align:center; padding:20px; color:#64748b;">Videolar aranıyor...</div>';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/youtube?q=' + encodeURIComponent(query), true);
    xhr.timeout = 7000;
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          var res = JSON.parse(xhr.responseText);
          if (res && res.length > 0) {
            renderYTVideos(res);
            globalStatus.textContent = 'Hazır';
            globalStatus.style.backgroundColor = '#10b981';
            return;
          }
        } catch (e) {}
      }
      renderYTVideos(curatedYT);
    };
    xhr.onerror = function () { renderYTVideos(curatedYT); };
    xhr.send();
  }

  function renderYTVideos(videos) {
    ytGrid.innerHTML = '';
    for (var i = 0; i < videos.length; i++) {
      var v = videos[i];
      var card = document.createElement('div');
      card.className = 'v-card';
      var thumb = 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';

      card.innerHTML = 
        '<div class="v-inner">' +
          '<div class="v-thumb">' +
            '<img src="' + thumb + '" alt="' + escapeHtml(v.title) + '" onerror="this.src=\'https://i.ytimg.com/vi/' + v.id + '/default.jpg\'">' +
          '</div>' +
          '<div class="v-info">' +
            '<div class="v-title">' + escapeHtml(v.title) + '</div>' +
            '<div class="v-author">' + escapeHtml(v.author || 'YouTube') + '</div>' +
          '</div>' +
        '</div>';

      (function (vid) {
        card.addEventListener('click', function () {
          playYT(vid.id, vid.title, vid.author);
        });
      })(v);

      ytGrid.appendChild(card);
    }
  }

  function playYT(id, title, author) {
    ytCurrentTitle.textContent = title;
    ytCurrentAuthor.textContent = author || 'YouTube';
    ytInfoBar.style.display = 'block';

    ytPlayerContainer.innerHTML = 
      '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1&rel=0&modestbranding=1" ' +
      'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' +
      'allowfullscreen webkitallowfullscreen></iframe>';

    globalStatus.textContent = 'Oynatılıyor';
    globalStatus.style.backgroundColor = '#10b981';
  }

  // ==========================================
  // 4. PDF İŞLEMLERİ
  // ==========================================
  function initPDF() {
    loadBooks();

    pdfUploadFile.addEventListener('change', function () {
      if (pdfUploadFile.files.length > 0) {
        var file = pdfUploadFile.files[0];
        pdfUploadStatus.textContent = file.name + ' yükleniyor...';
        
        var fd = new FormData();
        fd.append('file', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/upload-pdf', true);
        xhr.onload = function () {
          if (xhr.status === 200) {
            pdfUploadStatus.textContent = file.name + ' başarıyla yüklendi!';
            loadBooks();
          } else {
            pdfUploadStatus.textContent = 'Yükleme başarısız.';
          }
        };
        xhr.send(fd);
      }
    });
  }

  function loadBooks() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/books', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          var b = JSON.parse(xhr.responseText);
          renderBooksList(b);
          return;
        } catch (e) {}
      }
      renderBooksFallback();
    };
    xhr.onerror = function () { renderBooksFallback(); };
    xhr.send();
  }

  function renderBooksList(books) {
    booksList.innerHTML = '';
    if (!books || books.length === 0) {
      booksList.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b;">Henüz kayıtlı kitap yok. Yukarıdan bir PDF seçip aktarabilirsiniz.</div>';
      return;
    }

    for (var i = 0; i < books.length; i++) {
      var b = books[i];
      var row = document.createElement('div');
      row.className = 'book-row';

      var ext = b.name.split('.').pop().toLowerCase();
      var icon = '📄';
      if (ext === 'epub') icon = '📖';
      else if (ext === 'pdf') icon = '📕';

      row.innerHTML = 
        '<div class="book-meta">' +
          '<span class="book-meta-icon">' + icon + '</span>' +
          '<div>' +
            '<div class="book-meta-name">' + escapeHtml(b.name) + '</div>' +
            '<div class="book-meta-size">' + formatBytes(b.size) + '</div>' +
          '</div>' +
        '</div>' +
        '<a class="btn-open" href="' + b.url + '" target="_blank">Aç / Oku</a>';

      booksList.appendChild(row);
    }
  }

  function renderBooksFallback() {
    renderBooksList([
      { name: "iPad_Mini_1_Rehberi.pdf", size: 772, url: "/books/iPad_Mini_1_Rehberi.pdf" }
    ]);
  }

  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    var k = 1024, s = ['B', 'KB', 'MB', 'GB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + s[i];
  }

  function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // Başlat
  initTV();
  initYT();
  initPDF();
})();
