# 🚀 iPad mini 1 (iOS 9.3.6) Canlandırma ve Medya Merkezi

Bu kılavuz, Mac'inize USB ile bağlı olan **iPad mini 1 (A5 işlemci, 512 MB RAM, iOS 9.3.6)** cihazınızı güvenli, cihaz bütünlüğünü bozmadan bir **Canlı TV**, **Lite YouTube Oynatıcı** ve **PDF/E-Kitap Okuyucu** haline getirmek için hazırlanmıştır.

---

## 🌐 ÖNCELİKLİ ADIM: iPad İnternet Bağlantısını Çözme

iPad mini 1 şu anda internete bağlanamıyorsa aşağıdaki 3 pratik çözümü deneyin:

### 1. Tarih ve Saat Ayarını Kontrol Edin (En Çok Karşılaşılan Sorun!)
* Uzun süre kapalı kalmış veya şarjı bitmiş iPad'lerde tarih sıfırlanır (örneğin 1970).
* Tarih yanlış olduğunda tüm güvenlik sertifikaları geçersiz sayılır ve iPad hiçbir internet sitesine veya Wi-Fi ağına bağlanamaz.
* **Çözüm:** iPad'de `Ayarlar > Genel > Tarih ve Saat` bölümüne gidip tarihi ve saati bugüne ayarlayın.

### 2. Mac'in İnternetini USB Kablo ile iPad'e Verin
iPad şu an Mac'e kablo ile bağlı olduğundan, Mac'in internetini doğrudan kablo üzerinden paylaşabilirsiniz:
1. Mac'inizde **Sistem Ayarları (System Settings)** uygulamasını açın.
2. **Genel > Paylaşım (Sharing)** bölümüne gidin.
3. **İnternet Paylaşımı (Internet Sharing)** yanındaki bilgi (i) simgesine dokunun.
4. *"Paylaşılacak bağlantı:"* **Wi-Fi** seçin.
5. *"Şununla paylaşılacak:"* **iPhone / iPad USB** seçeneğini işaretleyin ve aktif edin.
6. iPad'iniz Mac üzerinden kablolu olarak anında internete erişecektir!

### 3. Wi-Fi Modemi 2.4GHz / WPA2 Moduna Alın
* iPad mini 1 (2012 model donanım) modern **WPA3** şifrelemeyi ve sadece 5GHz olan bazı yeni ağları desteklemez.
* Modemde WPA2-PSK (AES) şifreleme ve 2.4GHz bandı aktif olmalıdır. Alternatif olarak telefonunuzun Kişisel Erişim Noktası'nı (Hotspot) *"Maksimum Uyumluluk"* seçeneğiyle açıp bağlanabilirsiniz.

---

## ⚡ Hızlı Başlangıç (Jailbreak Gerektirmez)

### 1. Adım: Mac'te Yerel Medya Sunucusunu Başlatın
Terminal'de `mini1` klasöründeyken şu komutu çalıştırın:
```bash
python3 scripts/serve.py
```
Ekranda yerel IP adresiniz belirecektir (örneğin: `http://172.26.72.115:8000/portal/index.html`).

### 2. Adım: iPad'den Safari ile Açın ve Ana Ekrana Ekleyin
1. iPad'de Safari'yi açıp terminaldeki adrese gidin.
2. Safari'nin altındaki **Paylaş (kare ve yukarı ok)** simgesine dokunup **"Ana Ekrana Ekle" (Add to Home Screen)** deyin.
3. Artık ana ekranınızda bağımsız çalışan bir medya ve okuma merkezi ikonu yer alacaktır!

### 3. Adım: Kök SSL Sertifikasını Kurun
Sayfanın altındaki **"ISRG Root X1 SSL Sertifikasını Kur"** butonuna basarak Let's Encrypt kök sertifikasını yükleyin (`Ayarlar > Genel > Profil > Yükle`). Bu sertifika, yayın akışları ve web sitelerinin SSL hatası vermesini önler.

---

## 🏎️ iPad Hızlandırma Ayarları (Ayarlar Menüsünden)

512 MB RAM'i rahatlatmak ve A5 işlemciye binen gereksiz grafik yükünü kaldırmak için:
1. `Ayarlar > Genel > Erişilebilirlik > Kontrastı Artır > Saydamlığı Azalt` -> **AÇIK**
2. `Ayarlar > Genel > Erişilebilirlik > Hareketi Azalt` -> **AÇIK**
3. `Ayarlar > Genel > Arka Planda Uygulama Yenile` -> **KAPALI**

---

## 🛡️ Güvenlik Notları (Önemli)
* **AppSync Kullanılmıyor:** Güvenlik değerlendirmesi gereği sisteme imzasız zararlı kod yükleme riski taşıyan AppSync Unified sürece dahil edilmemiştir.
* **OpenSSH Kuralı:** İleride sistem debloating için SSH kurulursa, terminalden `passwd` ve `passwd mobile` ile varsayılan `alpine` şifresi mutlaka değiştirilmeli ve işlem bitince SSH kapatılmalıdır.
* **Sunucu Koruması:** `serve.py` sunucusu ThreadingHTTPServer ile güçlendirilmiş olup yalnızca `.pdf, .epub, .txt, .cbr, .cbz` uzantılarını ve maksimum 50 MB dosyaları kabul eder.
