#!/bin/bash
# iPad mini 1 (iOS 9.3.6) Sistem Servislerini Geri Yükleme (Rollback) Scripti
# Pasife alınan servisleri anında orijinal yerine taşır.

BACKUP_DIR="/System/Library/LaunchDaemons_Backup"
DAEMONS_DIR="/System/Library/LaunchDaemons"

echo "=========================================================="
echo "🔄 Sistem Servisleri Orijinal Haline Geri Yükleniyor..."
echo "=========================================================="

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Hata: Yedek klasörü ($BACKUP_DIR) bulunamadı!"
    exit 1
fi

RESTORED_COUNT=0

for FILE in "$BACKUP_DIR"/*.plist; do
    if [ -f "$FILE" ]; then
        FILENAME=$(basename "$FILE")
        mv "$FILE" "$DAEMONS_DIR/$FILENAME"
        echo "✅ Orijinal yerine taşındı: $FILENAME"
        RESTORED_COUNT=$((RESTORED_COUNT+1))
    fi
done

echo "----------------------------------------------------------"
echo "🎉 Tamamlandı! Toplam $RESTORED_COUNT servis eski haline getirildi."
echo "💡 Cihazınızı yeniden başlatın."
echo "=========================================================="
