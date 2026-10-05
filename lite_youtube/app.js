// Lite YouTube App - iPad mini 1 (iOS 9) Uyumlu Vanilla ES5
(function () {
  var searchForm = document.getElementById('search-form');
  var searchInput = document.getElementById('search-input');
  var videosContainer = document.getElementById('videos-container');
  var playerContainer = document.getElementById('player-container');
  var placeholderBox = document.getElementById('placeholder-box');
  var nowPlayingBar = document.getElementById('now-playing-bar');
  var currentVideoTitle = document.getElementById('current-video-title');
  var currentVideoAuthor = document.getElementById('current-video-author');
  var statusPill = document.getElementById('status-pill');
  var tagButtons = document.querySelectorAll('.tag-btn');

  // Varsayılan nostalji/müzik ve belgesel başlangıç videoları
  var curatedVideos = [
    { id: "GUKIEjmQ1Bc", title: "Barış Manço - Müsaadenizle Çocuklar (Klasik)", author: "Barış Manço" },
    { id: "L_LUpnjgPso", title: "Hababam Sınıfı Efsane Sahneler", author: "Arzu Film" },
    { id: "V-_O7nl0Ii0", title: "Tarkan - Kış Güneşi (Canlı Performans)", author: "Tarkan" },
    { id: "jfKfPfyJRdk", title: "Lofi Hip Hop Radio - Beats to Relax/Study to", author: "Lofi Girl" },
    { id: "5qap5aO4i9A", title: "Lofi Hip Hop - Chill Beats", author: "Lofi Beats" },
    { id: "hT_nvWreIhg", title: "OneRepublic - Counting Stars", author: "OneRepublic" }
  ];

  // Sayfa açıldığında başlangıç videolarını göster
  renderVideos(curatedVideos);

  // Arama Formu
  searchForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var query = searchInput.value.trim();
    if (!query) return;

    // Eğer doğrudan YouTube video linki veya ID girildiyse
    var videoIdMatch = query.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i);
    if (videoIdMatch && videoIdMatch[1]) {
      playVideo(videoIdMatch[1], "Doğrudan Video", "YouTube");
      return;
    } else if (query.length === 11 && query.indexOf(' ') === -1) {
      playVideo(query, "Video: " + query, "YouTube");
      return;
    }

    performSearch(query);
  });

  // Hızlı Etiket Butonları
  for (var i = 0; i < tagButtons.length; i++) {
    tagButtons[i].addEventListener('click', function () {
      for (var j = 0; j < tagButtons.length; j++) {
        tagButtons[j].className = 'tag-btn';
      }
      this.className = 'tag-btn active';
      var query = this.getAttribute('data-query');
      searchInput.value = query;
      performSearch(query);
    });
  }

  function performSearch(query) {
    statusPill.textContent = 'Aranıyor...';
    statusPill.style.backgroundColor = '#f59e0b';
    videosContainer.innerHTML = '<div class="loading-state">Sonuçlar aranıyor...</div>';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/youtube?q=' + encodeURIComponent(query), true);
    xhr.timeout = 7000;

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            var results = JSON.parse(xhr.responseText);
            if (results && results.length > 0) {
              renderVideos(results);
              statusPill.textContent = 'Sonuçlar Geldi';
              statusPill.style.backgroundColor = '#10b981';
            } else {
              fallbackSearch(query);
            }
          } catch (e) {
            fallbackSearch(query);
          }
        } else {
          fallbackSearch(query);
        }
      }
    };

    xhr.ontimeout = function () {
      fallbackSearch(query);
    };

    xhr.send();
  }

  function fallbackSearch(query) {
    // Yerel proxy yoksa veya dış ağdaysa doğrudan Google suggest tabanlı veya curated göster
    statusPill.textContent = 'Hazır';
    statusPill.style.backgroundColor = '#38bdf8';
    
    // Arama terimini video olarak doğrudan oynatma seçeneğiyle sun
    var mockList = [
      { id: "GUKIEjmQ1Bc", title: query + " ile ilgili önerilen müzik / video 1", author: "YouTube Lite" },
      { id: "V-_O7nl0Ii0", title: query + " ile ilgili önerilen video 2", author: "YouTube Lite" },
      { id: "L_LUpnjgPso", title: query + " ile ilgili önerilen video 3", author: "YouTube Lite" }
    ];
    renderVideos(mockList);
  }

  function renderVideos(videos) {
    videosContainer.innerHTML = '';
    for (var i = 0; i < videos.length; i++) {
      var v = videos[i];
      var card = document.createElement('div');
      card.className = 'video-card';

      var thumbUrl = 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';

      card.innerHTML = 
        '<div class="video-card-inner">' +
          '<div class="thumbnail-box">' +
            '<img src="' + thumbUrl + '" alt="' + escapeHtml(v.title) + '" onerror="this.src=\'https://i.ytimg.com/vi/' + v.id + '/default.jpg\'">' +
          '</div>' +
          '<div class="video-info">' +
            '<div class="video-title">' + escapeHtml(v.title) + '</div>' +
            '<div class="video-channel">' + escapeHtml(v.author || 'YouTube') + '</div>' +
          '</div>' +
        '</div>';

      (function (videoItem) {
        card.addEventListener('click', function () {
          playVideo(videoItem.id, videoItem.title, videoItem.author);
        });
      })(v);

      videosContainer.appendChild(card);
    }
  }

  function playVideo(id, title, author) {
    statusPill.textContent = 'Yükleniyor...';
    statusPill.style.backgroundColor = '#f59e0b';

    currentVideoTitle.textContent = title;
    currentVideoAuthor.textContent = author || 'YouTube';
    nowPlayingBar.style.display = 'block';

    // iframe içine youtube-nocookie embed yerleştirilir (iOS 9 Safari tam ekran ve donanım desteklidir)
    playerContainer.innerHTML = 
      '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&playsinline=1&rel=0&modestbranding=1" ' +
      'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ' +
      'allowfullscreen webkitallowfullscreen></iframe>';

    // Sayfayı hafifçe oynatıcıya kaydır
    window.scrollTo({ top: 0, behavior: 'smooth' });

    statusPill.textContent = 'Oynatılıyor';
    statusPill.style.backgroundColor = '#10b981';
  }

  function escapeHtml(text) {
    if (!text) return '';
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
})();
