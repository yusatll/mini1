# iPad mini 1 Projesi — Güvenlik ve Cihaz Bütünlüğü Değerlendirmesi

> **Belge türü:** Teknik risk değerlendirme raporu (AI asistanlarına sunum için yapılandırılmış)
> **Tarih:** 05.10.2026
> **Kapsam:** `readme.md`, `PLAN.md`, `scripts/serve.py`, `scripts/debloat_daemons.sh`, `scripts/restore_daemons.sh`, `portal/**`, `certs/isrgrootx1.pem`, `playlists/kanallar.m3u`, `portal/tv/channels.json`
> **Cihaz:** iPad mini 1 — Apple A5, 512 MB RAM, iOS 9.3.6 (32-bit)

---

## 0. Yönetici Özeti (tek paragrafta anlatım)

Proje genel olarak **makul düşünülmüş ve geri alınabilirlik prensibiyle kurulmuştur**:
hiçbir sistem dosyası silinmiyor, sadece yedek klasörüne taşınıyor ve geri alma scripti mevcut.
Ancak **4 kritik risk noktası** vardır: (1) jailbreak sonrası OpenSSH'nin varsayılan
`alpine` şifresiyle açık kalması, (2) AppSync Unified kurulumunun cihazı imzasız
yazılımlara açması, (3) iOS 9'da kök sertifika kurulumunun ekstra bir güven onayı
katmanı olmaması, (4) yerel sunucunun (`serve.py`) kimlik doğrulaması olmadan tüm
ağa açık olması. Ayrıca belgelerdeki "cihaz kesinlikle bozulamaz" ve "tüm HTTPS
siteleri açılır" iddiaları **aşırı iddialıdır** ve aşağıda düzeltilmiştir.

---

## 1. Özet Risk Matrisi

| # | Bileşen | Güvenlik Riski | Cihaz Riski | Ana Not |
|---|---------|----------------|-------------|----------|
| 1 | Portal + "Ana Ekrana Ekle" | 🟢 Düşük | 🟢 Yok | Standart Safari özelliği, güvenli |
| 2 | Ayarlar (Saydamlık/Hareket/Arka Plan yenileme) | 🟢 Yok | 🟢 Yok | Tamamen geri alınabilir, önerilir |
| 3 | Root CA (ISRG Root X1) kurulumu | 🟡 Orta | 🟢 Yok | iOS 9'da ek onay katmanı yok; doğrulama şart |
| 4 | serve.py (yerel HTTP sunucu) | 🟡 Orta | 🟢 Yok | Kimliksiz, ağa açık, upload sınırsız |
| 5 | Jailbreak (Phoenix) | 🟠 Yüksek | 🟡 Düşük | İmza doğrulama kalkar; IPA kaynağı kritik |
| 6 | **OpenSSH** | 🔴 **Kritik** | 🟢 Yok | Varsayılan şifre = LAN'daki herkese root erişimi |
| 7 | **AppSync Unified** | 🔴 **Kritik** | 🟡 Düşük | İmzasız IPA = kötü amaçlı yazılım vektörü |
| 8 | Debloat scripti | 🟢 Düşük | 🟡 Orta | Liste makul; 2 nüans var (Bölüm 4) |
| 9 | IPTV akış listeleri | 🟢 Düşük teknik / 🟠 yasal gri | 🟢 Yok | Yetkisiz yeniden yayın içerikleri mevcut |
| 10 | "DFU Garantisi" iddiası | — | 🟡 Nüanslı | Doğru çekirdek + 2 önemli istisna (Bölüm 5) |

---

## 2. Kritik Riskler (önce bunlar anlatılmalı)

### 2.1 OpenSSH — projedeki en büyük pratik güvenlik açığı

- **Durum:** PLAN.md, 3. adımda OpenSSH kurulmasını öneriyor ancak **şifre değiştirme
  adımı hiçbir yerde yok.**
- **Sorun:** Jailbreak'li cihazda OpenSSH, `root` ve `mobile` kullanıcıları için
  dünyaca bilinen varsayılan şifre `alpine` ile açılır. Aynı Wi-Fi ağındaki herhangi
  bir cihaz `ssh root@<ip-adresi>` komutuyla iPad'e **tam root erişimi** sağlayabilir.
- **Sonuç:** Jailbreak'li bir cihazda bu; dosya sisteminin (Safari verisi, kayıtlı
  şifreler, mailler) tamamen ele geçirilmesi demektir.
- **Çözüm (uygulanmadan jailbreak adımına geçilmemeli):**
  1. OpenSSH kurulduktan sonra **ilk iş** terminalde: `passwd` (root şifresi) ve
     `passwd mobile` (mobile şifresi) — ikisi de güçlü/uzun şifre olmalı.
  2. SSH kullanılmadığı zamanlarda kapatılmalı:
     `launchctl unload -w /Library/LaunchDaemons/com.openssh.sshd.plist`

### 2.2 AppSync Unified — gereksiz ve tehlikeli

- **Durum:** PLAN.md, 3. adımda AppSync Unified kurulmasını öneriyor.
- **Sorun:** AppSync, Apple'ın kod imza doğrulamasını tamamen devre dışı bırakır.
  İnternetteki **herhangi bir imzasız IPA** (dolayısıyla gizlice zararlı yazılım
  barındıran IPA) cihaza kurulabilir hale gelir. Birincil kullanım alanı korsanlık
  olduğu için güvenilir kaynak varsayımı da taşımaz.
- **Çözüm:** Bu projedeki hiçbir gerçek ihtiyaç AppSync gerektirmiyor — **atlanmalı**.
  VLC/GoodReader gibi 32-bit uygulamalar için güvenli alternatifler:
  - App Store'un "daha önce indirilen son uyumlu sürüm" mekanizması
    (aynı Apple ID ile önceden indirilmişse),
  - veya kendi ücretsiz geliştirici sertifikası ile Sideloadly üzerinden imzalama
    (7 günde bir yeniden imzalama gerekir).

### 2.3 Kök sertifika (ISRG Root X1) kurulumu — iOS 9'ın kritik farkı

- **Teknik arka plan:** iOS 10.3'ten itibaren manuel kurulan kök sertifikalar
  `Ayarlar → Genel → Hakkında → Sertifika Güven Ayarları`'ndan **ayrıca**
  etkinleştirilmelidir. **iOS 9'da bu katman yoktur** — profil kurulduğu an kök
  sertifika sistem genelinde güvenilir olur.
- **Risk:** Yanlış veya değiştirilmiş bir kök sertifika kurulursa cihazda tam
  **MITM (ortadaki adam) kapısı** açılmış olur: tüm HTTPS trafiği okunabilir/degistirilebilir.
- **Mevcut dosya incelemesi:** `certs/isrgrootx1.pem` incelendi:
  - Seri no: `8210:CFB0:D240:E359:4463:E0BB:6382:8B00`
  - Konu: `CN=ISRG Root X1, O=Internet Security Research Group, C=US`
  - Geçerlilik: 04.06.2015 – 04.06.2035
  - **Sonuç: görünüşe göre özgün ISRG Root X1.** Ancak kurulumdan önce parmak izi
    mutlaka **letsencrypt.org/certificates** sayfasındaki resmî SHA-256 değeriyle
    karşılaştırılmalıdır (dosyanın geçmişi bilinemez).
- **Belge düzeltmesi:** readme'deki *"iPad'iniz tüm modern HTTPS sitelerini hatasız
  açacaktır"* iddiası **yanlıştır**. Bu sertifika yalnızca **Let's Encrypt ile
  sertifikalanan siteleri** kurtarır. GlobalSign/DigiCert/Sectigo köklü siteler zaten
  çalışıyordur; diğer bozuk zincirler bu sertifikayla da açılmayabilir.

### 2.4 serve.py — ağa açık, kimliksiz sunucu

Kod incelemesinden bulgular:

1. **Bağlama:** Sunucu `0.0.0.0:8000`'e bağlanır ve **hiçbir kimlik doğrulama yoktur**.
   Aynı ağdaki her cihaz portala **ve tüm `mini1/` klasörüne** erişebilir
   (`SimpleHTTPRequestHandler` kök dizini olarak `BASE_DIR` servis eder — PLAN.md,
   kanal listeleri, sertifika dahil her şey indirilebilir).
2. **`/api/upload-pdf` uç noktası:** Dosya adı `os.path.basename` ile ayıklanıyor
   (path traversal yok ✅) ancak **uzantı ve boyut kontrolü yoktur**:
   - Ağdaki herhangi biri diski doldurabilir,
   - `.html` yükleyip portalın origin'inde (`http://<mac-ip>:8000`) script çalıştırabilir.
   - **İyileştirme:** uzantı beyaz listesi (`.pdf .epub .txt .cbr .cbz`) + boyut limiti.
3. **YouTube scraping:** `ytInitialData` regex'i Hizmet Şartları'na aykırı otomasyondur
   (yasal gri alan) ve kırılgandır — YouTube bot koruması aramayı her an bozabilir.
4. **HTTP cleartext:** LAN trafiği dinlenebilir; medya için kabul edilebilir ama bilinçli olunmalı.
5. **Fonksiyonel not:** `TCPServer` tek iş parçacıklıdır; video `Range` isteklerinde
   arayüz takılabilir. `ThreadingHTTPServer` daha uygundur.
6. **Öneri:** Sunucu kullanılmadığında kapatılmalı; mümkünse yalnız Mac'in IP'sine
   bind edilmeli; misafir ağından izole edilmelidir.

---

## 3. Orta Düzey Riskler

### 3.1 Jailbreak (Phoenix)

- **Risk artışı:** Jailbreak, kod imzalama ve sandbox korumalarını zayıflatır; cihaz
  iOS 9'a ait bilinen kernel açıklarına karşı savunmasızdır. Yalnızca tanınmış
  Cydia repoları kullanılmalıdır.
- **Kaynak kritik:** Phoenix'in sahte/bozuk imzalı kopyaları dolaşımdadır; IPA
  yalnızca doğrulanabilir kaynaktan alınmalıdır.
- **Pratik bilgi:** Cydia Impactor 2019'dan beri çalışmıyor; doğru araç
  **Sideloadly**'dir ve ücretsiz Apple ID ile **7 günde bir yeniden imzalama**
  gerektirir (readme/PLAN.md'ye eklenmeli). Phoenix **semi-untethered**'dir: her
  yeniden başlatma sonrası yeniden çalıştırılmalıdır.

### 3.2 IPTV akışları — teknik risk düşük, yasal durum gri

- `channels.json` ve `kanallar.m3u` büyük ölçüde topluluk listelerinden (iptv-org
  tarzı) derlenmiştir.
- **Meşru içerik:** TRT kanalları resmî TRT CDN'lerinden (`tv-trt1.medya.trt.com.tr`
  vb.) geliyor.
- **Riskli içerik:** Listede BabyTV, BBC Earth gibi uluslararası kanalların üçüncü
  taraf CDN'lerden akan **muhtemelen yetkisiz yeniden yayınları** vardır (BBC Earth
  satırında `http-user-agent` sahteciliği gerektiren kayıtlar bile var). Kişisel
  kullanımda kovuşturma riski pratikte düşüktür ancak bu içerikler telif ihlali
  kapsamındadır.
- **Teknik güvenlik:** HLS video içeriği Safari'de zararlı script çalıştırmaz — düşük risk.
- **Uyumluluk uyarısı:** iOS 9 Safari HLS'de yalnızca **TS tabanlı** akışları
  destekler; **fMP4/CMAF** iOS 10+ ile geldi ve A5'te **HEVC donanım çözücü yoktur**.
  1080p kanalların bir kısmı Safari'de **oynamayabilir** (VLC'de oynar). "160+ kanal
  tek tıkla açılır" ifadesi bu yüzden garanti değildir.

### 3.3 YouTube portalı

- Oynatma `youtube-nocookie.com` embed ile yapılıyor — güvenli yaklaşım ✅.
- Ancak **"sıfır reklam" iddiası doğru değildir**: embed'lerde reklam çıkabilir.
- YouTube, eski iOS Safari player desteğini her an kırabilir (fonksiyonel dayanıklılık riski).
- Portal kodu Vanilla ES5, üçüncü taraf JS kütüphanesi yok (tedarik zinciri riski yok ✅),
  `escapeHtml` ile XSS önlemi var ✅.

---

## 4. Cihaz Bütünlüğü: Debloat Scripti Değerlendirmesi

**İncelenen dosya:** `scripts/debloat_daemons.sh` (15 daemon)

**Olumlu bulgular:**
- Hiçbir dosya silinmiyor, yalnızca `/System/Library/LaunchDaemons_Backup`'a taşınıyor ✅
- Geri alma scripti (`restore_daemons.sh`) mevcut ve doğru çalışıyor ✅
- OpenSSH'ın kendi daemon'u listede **yok** (geri alma yolu her zaman açık) ✅
- Liste, iOS 9 topluluğundaki bilinen güvenli listeye uygun; açılış için kritik daemon yok ✅

**Nüanslar (bilinmeli):**
1. `com.apple.mobile.obliteration.plist` uzaktan/yerel silme servisidir. Taşındığında
   Ayarlar'dan **"Tüm İçeriği ve Ayarları Sil" çalışmayabilir** — cihazı elden
   çıkarırken bilinmeli (DFU restore ile çözülür).
2. `ReportCrash.Jetsam` taşınınca RAM olay kayıtları düşmez; sorun giderme zorlaşır.
3. **Önemli avantaj:** OpenSSH plist'i `/Library/LaunchDaemons` içinde olduğu için
   reboot sonrası jailbreak yeniden etkinleştirilmese bile SSH çalışmaya devam eder —
   debloat geri alma yolu her zaman açıktır.
4. **Beklenti yönetimi:** "RAM rezervi %25–30 artar" ve "performans 2 katına çıkar"
   iddiaları gerçekçi değildir. Bu daemonlar çoğunlukle boşta bekler; toplam kazanç
   birkaç on MB'dır. His edilir iyileşme olur, 2 kat hız olmaz.

---

## 5. "DFU Garantisi" İddiasının Doğru Değerlendirilmesi

**Doğru olan:**
- A5 çipinin DFU modu Secure ROM (boot çipi) seviyesinde kazılıdır; yazılım bunu bozamaz.
- Yazılımsal bir boot-loop neredeyse her zaman DFU + restore ile kurtarılır.

**İstisnalar (readme'deki "kesinlikle bozulamaz" ifadesini aşırı yapan):**
1. **İmza bağımlılığı:** DFU restore, Apple'ın SHSH imza sunucularının iOS 9.3.5/9.3.6'yı
   hâlâ imzalamasına bağlıdır. iPad mini 1'in son iOS'u olduğu için Apple şu ana kadar
   imzalamaya devam etmiştir; ancak bu **garanti edilmez**. İmzalama kapanırsa restore
   imza hatası verir ve cihaz gerçekten kurtarılamaz hale gelebilir. Riskli işlemlerden
   önce imza durumu kontrol edilmelidir.
2. **Veri kaybı:** Restore **her şeyi siler** (fotoğraflar, uygulama verileri). "Cihaz
   bozulmaz" doğru olabilir ama "veriniz kaybolmaz" garanti edilmez.
3. **Aktivasyon Kilidi:** Restore sonrası Apple ID bilgileri sorulur; hesap bilgileri
   unutulmamalıdır.

**Önerilen ifade değişikliği (readme için):**
> "DFU donanımda olduğu için yazılımsal brick neredeyse her zaman restore ile
> kurtarılabilir; ancak restore, Apple'ın 9.3.6 imzalamaya devam etmesine bağlıdır
> ve tüm veriyi siler."

---

## 6. Risksiz / Önerilen Bileşenler

| Bileşen | Değerlendirme |
|---------|---------------|
| Portal arayüzü (index.html, tv.js, app.js, pdf/app.js) | Üçüncü taraf JS yok, ES5 uyumlu, `escapeHtml` ile XSS önlemi var — güvenli |
| "Ana Ekrana Ekle" web app | Standart Safari özelliği, risksiz |
| Saydamlığı Azalt / Hareketi Azalt / Arka Plan Yenileme kapalı | Tamamen güvenli, geri alınabilir, 512 MB RAM cihazda net fayda |
| PDF'i iBooks'ta açma akışı | Güvenli, çevrimdışı kalıcı kayıt sağlar |
| TRT resmî HLS akışları | Meşru kaynak, donanım çözücüyle verimli |

---

## 7. Öncelikli Eylem Listesi

| Öncelik | Eylem | Nerede |
|---------|-------|--------|
| 🔴 1 | OpenSSH sonrası **ilk iş** `passwd` + `passwd mobile`; kullanım dışında sshd unload | PLAN.md 3. adıma eklenmeli |
| 🔴 2 | **AppSync Unified listeden çıkarılmalı** | PLAN.md 3. adım |
| 🟠 3 | Sertifika parmak izi letsencrypt.org ile doğrulanmalı; readme'deki "tüm HTTPS siteleri" ifadesi düzeltilmeli | readme.md Adım 3 |
| 🟠 4 | Jailbreak öncesi Finder/iTunes tam yedek + Apple ID doğrulaması | PLAN.md 3. öncesi |
| 🟡 5 | serve.py'ye upload uzantı/boyut sınırı; kullanılmadığında kapatma alışkanlığı | scripts/serve.py |
| 🟡 6 | "DFU garantisi" ifadesinin yumuşatılması; "RAM %25-30" ve "2x performans" iddialarının gerçeğe bağlanması | readme.md + PLAN.md |
| 🟡 7 | Sideloadly 7 günlük imzalama periyodu ve Phoenix semi-untethered doğası belgelere eklenmeli | readme.md / PLAN.md |

---

## 8. Genel Sonuç

Proje, jailbreak'li eski cihaz projelerine göre **özenli hazırlanmıştır**: yedekleme
prensibi, rollback scriptleri, üçüncü taraf kütüphane kullanmayan sade portal kodu
tasarım açısından olumlu durumdadir. Ancak:

- **Bölüm 2.1 ve 2.2'deki iki kritik madde (SSH şifresi + AppSync)** uygulanmadan
  jailbreak adımına geçilmemelidir.
- Belgelerdeki abartılı iddialar (DFU, HTTPS, performans, reklam) yukarıdaki gibi
  düzeltilmelidir; bu düzeltmeler kullanıcı beklentisini gerçekçi kılar ve güvenlik
  kararlarını doğru verilebilir hale getirir.
