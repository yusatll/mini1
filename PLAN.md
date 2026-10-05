# iPad mini 1 (iOS 9.3.6) Canlandırma ve Güvenli Optimizasyon Planı

Bu belge, Mac'e USB ile bağlı olan iPad mini 1 (A5 işlemci, 512 MB RAM, 32-bit ARMv7, iOS 9.3.6) cihazının güvenli, riskleri en aza indirilmiş ve cihaz bütünlüğünü koruyan bir yaklaşımla canlandırılması için hazırlanmıştır.

---

## 🛡️ Güvenlik ve Cihaz Bütünlüğü İlkeleri (Güvenlik İncelemesi Doğrultusunda)

1. **Jailbreak'siz Başlangıç (Öncelikli Aşama):**
   * Canlı TV, Lite YouTube ve PDF okuma işlevleri Safari Web Portalı üzerinden **Jailbreak yapılmadan da** tamamen çalışabilmektedir.
   * Cihazın sandbox korumasını bozmamak adına ilk aşama Jailbreak'siz olarak uygulanır.
   * **AppSync Unified** kaldırılmıştır (imzasız rastgele kod çalıştırma riskini önlemek için).

2. **OpenSSH Güvenlik Kuralı:**
   * İleride sistem debloating için Jailbreak ve OpenSSH kullanılırsa, kurulduğu **ilk saniye** terminalden `passwd` ve `passwd mobile` ile varsayılan `alpine` şifresi değiştirilecek; işlem bitince SSH servisi pasife alınacaktır.

3. **Gerçekçi Beklentiler:**
   * **DFU Durumu:** DFU donanımsal kurtarma sağlar; ancak cihazdaki verileri sıfırlar ve Apple'ın iOS 9.3.6'yı imzalamaya devam etmesine bağlıdır.
   * **Performans:** 512 MB RAM'de sistem servislerini uyutmak onlarca megabayt boş bellek sağlar ve arayüzü rahatlatır; ancak donanımın fiziksel hızını 2 katına çıkarmaz.
   * **SSL/HTTPS:** ISRG Root X1 sertifikası Let's Encrypt kullanan siteleri ve TV yayınlarını çözer; ancak TLS 1.3 veya ağır modern JavaScript (ES2020+) gerektiren siteleri çalıştırmaz.

---

## 🌐 0. ADIM: iPad İnternet Bağlantısını Çözme (Öncelikli Adım)

iPad mini 1 şu anda internete bağlanamıyorsa sırasıyla şu yöntemler uygulanır:

1. **Yöntem A: Tarih ve Saat Kontrolü (En Sık Görülen Sorun):**
   * Şarjı bitip beklemiş eski iPad'lerde tarih 1970'e sıfırlanır. Tarih yanlışsa tüm SSL/ağ bağlantıları bloke olur ve internete bağlanamaz.
   * `Ayarlar > Genel > Tarih ve Saat` -> Saatin ve tarihin güncel olduğundan emin olun.

2. **Yöntem B: Mac Üzerinden USB Kablolu İnternet Paylaşımı:**
   * iPad zaten Mac'e USB ile bağlı olduğu için Mac'in interneti doğrudan kabloyla iPad'e aktarılabilir.
   * Mac'te: `Sistem Ayarları > Genel > Paylaşım > İnternet Paylaşımı (Internet Sharing)`
   * "Paylaşılacak bağlantı: Wi-Fi", "Şununla paylaşılacak: iPhone/iPad USB" seçeneğini aktif edin.

3. **Yöntem C: Wi-Fi Uyumluluk Sorunu (WPA3 / 5GHz):**
   * iPad mini 1 (2012) sadece WPA/WPA2 ve 2.4GHz / 802.11n destekler.
   * Modeminiz WPA3 veya sadece 5GHz yayını yapıyorsa iPad ağı göremez veya bağlanamaz. Telefonunuzdan "Kişisel Erişim Noktası" açıp "Maksimum Uyumluluk" seçeneğini açarak bağlanmayı deneyin.

---

## 📋 Uygulama Yol Haritası

```
+------------------------------------------------------------------------+
| 0. ADIM: iPad İnternet Bağlantısını Sağlama (Tarih/Saat, USB Paylaşım) |
+------------------------------------------------------------------------+
                                   |
+------------------------------------------------------------------------+
| 1. ADIM: Ağ & Kök Sertifika (ISRG Root X1)                            |
|    - Let's Encrypt sertifikalı TV akışları ve siteler aktif edilir.   |
+------------------------------------------------------------------------+
                                   |
+------------------------------------------------------------------------+
| 2. ADIM: Yerel Arayüz Hızlandırma Ayarları (Risksiz, Ayarlar Menüsü)  |
|    - Saydamlığı Azalt -> AÇIK                                         |
|    - Hareketi Azalt -> AÇIK                                           |
|    - Arka Planda Uygulama Yenile -> KAPALI                            |
+------------------------------------------------------------------------+
                                   |
+------------------------------------------------------------------------+
| 3. ADIM: Web Portallarının Kullanımı (Jailbreak Gerekmez)              |
|    - Canlı TV: HLS .m3u8 doğrudan A5 donanım hızlandırmalı.           |
|    - Lite YouTube: Reklamsız, arama özellikli, 720p.                  |
|    - PDF Kitaplık: Mac'ten kablosuz/USB aktarım, Apple Books ile oku. |
+------------------------------------------------------------------------+
                                   |
+------------------------------------------------------------------------+
| 4. ADIM (İsteğe Bağlı): İleri Düzey Debloating                        |
|    - İhtiyaç duyulursa Phoenix semi-untethered JB ile OpenSSH açılır, |
|      şifresi değiştirilip gereksiz servisler yedeklenerek uyutulur.   |
+------------------------------------------------------------------------+
```
