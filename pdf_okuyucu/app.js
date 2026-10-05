// PDF & Kitaplık - iPad mini 1 (iOS 9) Uyumlu Vanilla ES5
(function () {
  var fileInput = document.getElementById('pdf-file-input');
  var uploadFilename = document.getElementById('upload-filename');
  var booksContainer = document.getElementById('books-container');
  var statusPill = document.getElementById('status-pill');

  // Varsayılan / mevcut kitapları çek
  loadBooks();

  // Dosya seçildiğinde otomatik yükle
  fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
      var file = fileInput.files[0];
      uploadFilename.textContent = file.name + ' (' + formatBytes(file.size) + ') yükleniyor...';
      uploadFile(file);
    }
  });

  function uploadFile(file) {
    statusPill.textContent = 'Yükleniyor...';
    statusPill.style.backgroundColor = '#f59e0b';

    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/upload-pdf', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        uploadFilename.textContent = file.name + ' başarıyla yüklendi!';
        statusPill.textContent = 'Yüklendi';
        statusPill.style.backgroundColor = '#10b981';
        loadBooks();
      } else {
        uploadFilename.textContent = 'Yükleme başarısız oldu.';
        statusPill.textContent = 'Hata';
        statusPill.style.backgroundColor = '#ef4444';
      }
    };
    xhr.onerror = function () {
      uploadFilename.textContent = 'Ağ hatası.';
      statusPill.textContent = 'Hata';
      statusPill.style.backgroundColor = '#ef4444';
    };
    xhr.send(formData);
  }

  function loadBooks() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/books', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          var books = JSON.parse(xhr.responseText);
          renderBooks(books);
        } catch (e) {
          renderFallback();
        }
      } else {
        renderFallback();
      }
    };
    xhr.onerror = function () {
      renderFallback();
    };
    xhr.send();
  }

  function renderBooks(books) {
    booksContainer.innerHTML = '';
    if (!books || books.length === 0) {
      booksContainer.innerHTML = '<div style="text-align:center; padding:30px; color:#64748b;">Henüz yüklenmiş kitap yok. Yukarıdan Mac\'inizdeki bir PDF dosyasını seçip yükleyebilirsiniz.</div>';
      return;
    }

    for (var i = 0; i < books.length; i++) {
      var b = books[i];
      var item = document.createElement('div');
      item.className = 'book-item';

      var ext = b.name.split('.').pop().toLowerCase();
      var icon = '📄';
      if (ext === 'epub') icon = '📖';
      else if (ext === 'pdf') icon = '📕';

      item.innerHTML = 
        '<div class="book-info">' +
          '<div class="book-icon">' + icon + '</div>' +
          '<div>' +
            '<div class="book-title">' + escapeHtml(b.name) + '</div>' +
            '<div class="book-size">' + formatBytes(b.size) + '</div>' +
          '</div>' +
        '</div>' +
        '<div class="book-actions">' +
          '<a class="open-btn" href="' + b.url + '" target="_blank">Aç / Oku</a>' +
        '</div>';

      booksContainer.appendChild(item);
    }
  }

  function renderFallback() {
    // Sunucu API'si henüz başlamadıysa örnek kılavuz belgesini göster
    renderBooks([
      { name: "iPad Mini 1 Kullanım ve Hızlandırma Kılavuzu.pdf", size: 245000, url: "/docs/kilavuz.pdf" }
    ]);
  }

  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    var k = 1024;
    var sizes = ['B', 'KB', 'MB', 'GB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
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
