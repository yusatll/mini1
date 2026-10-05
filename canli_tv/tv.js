// iPad mini 1 (iOS 9) Uyumlu Vanilla ES5 JavaScript
(function () {
  var player = document.getElementById('tv-player');
  var channelNameDisplay = document.getElementById('channel-name-display');
  var statusPill = document.getElementById('status-pill');
  var searchInput = document.getElementById('search-input');
  var container = document.getElementById('channels-container');

  var allChannels = [];
  var currentActiveCard = null;

  // Kanalları JSON'dan çek
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'channels.json', true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200 || xhr.status === 0) {
        try {
          allChannels = JSON.parse(xhr.responseText);
          renderChannels(allChannels);
          // Varsayılan olarak ilk kanalı (TRT 1) hazırla
          if (allChannels.length > 0) {
            prepareChannel(allChannels[0], null, false);
          }
        } catch (e) {
          console.error("JSON okunamadı:", e);
          statusPill.textContent = "Hata";
          statusPill.style.backgroundColor = "#ef4444";
        }
      }
    }
  };
  xhr.send();

  function renderChannels(channels) {
    container.innerHTML = '';
    if (!channels || channels.length === 0) {
      container.innerHTML = '<div style="width:100%; text-align:center; padding: 20px; color:#94a3b8;">Kanal bulunamadı.</div>';
      return;
    }

    for (var i = 0; i < channels.length; i++) {
      var ch = channels[i];
      var card = document.createElement('div');
      card.className = 'channel-card';

      var inner = document.createElement('div');
      inner.className = 'channel-card-inner';

      if (ch.logo && ch.logo.indexOf('http') === 0) {
        var img = document.createElement('img');
        img.className = 'channel-logo';
        img.src = ch.logo;
        img.alt = ch.name;
        img.onerror = function () {
          this.style.display = 'none';
        };
        inner.appendChild(img);
      } else {
        var placeholder = document.createElement('div');
        placeholder.className = 'channel-placeholder';
        placeholder.textContent = '📺';
        inner.appendChild(placeholder);
      }

      var title = document.createElement('div');
      title.className = 'channel-title';
      title.textContent = ch.name;
      inner.appendChild(title);

      card.appendChild(inner);

      // Tıklama olayı
      (function (channelData, cardInner) {
        card.addEventListener('click', function () {
          prepareChannel(channelData, cardInner, true);
        });
      })(ch, inner);

      container.appendChild(card);
    }
  }

  function prepareChannel(channel, cardInner, autoPlay) {
    if (currentActiveCard) {
      currentActiveCard.className = 'channel-card-inner';
    }
    if (cardInner) {
      cardInner.className = 'channel-card-inner active';
      currentActiveCard = cardInner;
    }

    channelNameDisplay.textContent = 'Oynatılıyor: ' + channel.name;
    statusPill.textContent = 'Bağlanıyor...';
    statusPill.style.backgroundColor = '#f59e0b';

    player.src = channel.url;
    player.load();

    if (autoPlay) {
      var playPromise = player.play();
      if (playPromise !== undefined) {
        playPromise.then(function () {
          statusPill.textContent = 'Canlı Yayın';
          statusPill.style.backgroundColor = '#10b981';
        }).catch(function (error) {
          console.log("Otomatik oynatma kısıtlandı:", error);
          statusPill.textContent = 'Oynat tuşuna basın';
          statusPill.style.backgroundColor = '#64748b';
        });
      }
    }
  }

  player.addEventListener('playing', function () {
    statusPill.textContent = 'Canlı Yayın';
    statusPill.style.backgroundColor = '#10b981';
  });

  player.addEventListener('error', function () {
    statusPill.textContent = 'Yayın Yok / Hata';
    statusPill.style.backgroundColor = '#ef4444';
  });

  // Arama filtreleme
  searchInput.addEventListener('input', function () {
    var query = searchInput.value.toLowerCase().trim();
    if (!query) {
      renderChannels(allChannels);
      return;
    }

    var filtered = [];
    for (var i = 0; i < allChannels.length; i++) {
      if (allChannels[i].name.toLowerCase().indexOf(query) !== -1) {
        filtered.push(allChannels[i]);
      }
    }
    renderChannels(filtered);
  });
})();
