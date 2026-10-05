#!/bin/bash
# Mac'in tüm ağ arayüzlerindeki IP adreslerini ve iPad'in bağlanabileceği URL'leri gösterir.

PORT=8000

echo "=========================================================="
echo "📡 Mac Ağ Bağlantıları ve iPad Bağlantı Adresleri:"
echo "=========================================================="

# Wi-Fi (en0)
WIFI_IP=$(ipconfig getifaddr en0 2>/dev/null)
if [ -n "$WIFI_IP" ]; then
    echo "📶 Ev/Ofis Wi-Fi Bağlantısı:"
    echo "   👉 http://$WIFI_IP:$PORT/portal/index.html"
    echo "   📺 Canlı TV:     http://$WIFI_IP:$PORT/canli_tv/index.html"
    echo "   ▶️  Lite YouTube: http://$WIFI_IP:$PORT/lite_youtube/index.html"
    echo "   📚 PDF Okuyucu:  http://$WIFI_IP:$PORT/pdf_okuyucu/index.html"
    echo ""
fi

# Telefon Hotspot / Mobil Paylaşım (en1 veya en2)
for IFACE in en1 en2 en3 bridge100; do
    IF_IP=$(ipconfig getifaddr $IFACE 2>/dev/null)
    if [ -n "$IF_IP" ]; then
        echo "📱 Kişisel Erişim Noktası / USB Ağ Bağlantısı ($IFACE):"
        echo "   👉 http://$IF_IP:$PORT/portal/index.html"
        echo "   📺 Canlı TV:     http://$IF_IP:$PORT/canli_tv/index.html"
        echo "   ▶️  Lite YouTube: http://$IF_IP:$PORT/lite_youtube/index.html"
        echo "   📚 PDF Okuyucu:  http://$IF_IP:$PORT/pdf_okuyucu/index.html"
        echo ""
    fi
done

echo "💡 İpucu: iPad'iniz mobil veriye/hotspot'a bağlıysa, Mac'inizi de aynı"
echo "   hotspot ağına bağladığınızda yukarıdaki adres anında çalışacaktır!"
echo "=========================================================="
