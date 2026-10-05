#!/bin/bash
# iPad mini 1 (iOS 9.3.6) Güvenli Sistem Servisleri Hafifletme (Debloat) Scripti
# Bu script hiçbir dosyayı silmez; güvenli bir yedek klasörüne taşır.

BACKUP_DIR="/System/Library/LaunchDaemons_Backup"
DAEMONS_DIR="/System/Library/LaunchDaemons"

echo "=========================================================="
echo "⚡ iPad mini 1 Güvenli Sistem Hafifletme Başlatılıyor..."
echo "=========================================================="

# 1. Yedek klasörünü oluştur
mkdir -p "$BACKUP_DIR"

# 2. Uyutulacak / Devre dışı bırakılacak gereksiz servisler listesi
DAEMONS=(
    "com.apple.softwareupdateservicesd.plist"
    "com.apple.OTATaskingAgent.plist"
    "com.apple.ReportCrash.plist"
    "com.apple.ReportCrash.DirectoryService.plist"
    "com.apple.ReportCrash.Jetsam.plist"
    "com.apple.ReportCrash.SafetyNet.plist"
    "com.apple.ReportCrash.Simulate.plist"
    "com.apple.CrashHouseKeeping.plist"
    "com.apple.DumpHound.plist"
    "com.apple.awdd.plist"
    "com.apple.passd.plist"
    "com.apple.gamed.plist"
    "com.apple.iadd.plist"
    "com.apple.familycircled.plist"
    "com.apple.mobile.obliteration.plist"
)

MOVED_COUNT=0

for DAEMON in "${DAEMONS[@]}"; do
    if [ -f "$DAEMONS_DIR/$DAEMON" ]; then
        mv "$DAEMONS_DIR/$DAEMON" "$BACKUP_DIR/$DAEMON"
        echo "✅ Yedeklendi ve pasife alındı: $DAEMON"
        MOVED_COUNT=$((MOVED_COUNT+1))
    fi
done

echo "----------------------------------------------------------"
echo "🎉 Tamamlandı! Toplam $MOVED_COUNT gereksiz servis pasife alındı."
echo "📁 Orijinal dosyalar güvenle şurada saklanıyor: $BACKUP_DIR"
echo "💡 Değişikliklerin etkili olması için cihazı yeniden başlatın (respring/reboot)."
echo "=========================================================="
