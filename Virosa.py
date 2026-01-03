import random
import string
import re
import os
import math

# Dahili yaygın şifreler (fallback)
DAHILI_YAYGIN = {
    "123456", "password", "123456789", "12345",
    "qwerty", "abc123", "111111", "123123",
    "password1", "admin", "letmein"
}

def yaygin_sifreleri_yukle():
    if os.path.exists("rockyou.txt"):
        try:
            with open("rockyou.txt", "r", encoding="latin-1") as f:
                print("✅ rockyou.txt yüklendi")
                return set(s.strip().lower() for s in f)
        except:
            print("⚠️ rockyou.txt okunamadı, dahili liste kullanılıyor")
            return DAHILI_YAYGIN
    else:
        print("⚠️ rockyou.txt yok, dahili liste kullanılıyor")
        return DAHILI_YAYGIN

YAYGIN_SIFRELER = yaygin_sifreleri_yukle()

def guclu_sifre_uret(uzunluk=12):
    karakterler = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        "!@#$%^&*()_+-="
    )
    return "".join(random.choice(karakterler) for _ in range(uzunluk))

def kirilma_suresi_hesapla(sifre):
    charset = 0
    if re.search(r"[a-z]", sifre): charset += 26
    if re.search(r"[A-Z]", sifre): charset += 26
    if re.search(r"[0-9]", sifre): charset += 10
    if re.search(r"[^a-zA-Z0-9]", sifre): charset += 32

    if charset == 0:
        return "Hesaplanamadı"

    kombinasyon = charset ** len(sifre)
    saniye = kombinasyon / 1_000_000_000  # saniyede 1 milyar deneme

    if saniye < 60:
        return "Saniyeler içinde"
    elif saniye < 3600:
        return f"{int(saniye/60)} dakika"
    elif saniye < 86400:
        return f"{int(saniye/3600)} saat"
    elif saniye < 31536000:
        return f"{int(saniye/86400)} gün"
    else:
        return f"{int(saniye/31536000)} yıl+"

def sifre_analiz(sifre):
    puan = 0
    nedenler = []

    if len(sifre) >= 8:
        puan += 1
    else:
        nedenler.append("Çok kısa (en az 8 karakter)")

    if re.search(r"[A-Z]", sifre):
        puan += 1
    else:
        nedenler.append("Büyük harf yok")

    if re.search(r"[a-z]", sifre):
        puan += 1
    else:
        nedenler.append("Küçük harf yok")

    if re.search(r"[0-9]", sifre):
        puan += 1
    else:
        nedenler.append("Rakam yok")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", sifre):
        puan += 1
    else:
        nedenler.append("Özel karakter yok")

    yaygin = sifre.lower() in YAYGIN_SIFRELER
    if yaygin:
        nedenler.append("Yaygın şifre listesinde")

    if yaygin:
        guc = "❌ ÇOK ZAYIF"
    elif puan <= 2:
        guc = "❌ Zayıf"
    elif puan <= 4:
        guc = "⚠️ Orta"
    else:
        guc = "✅ Güçlü"

    return yaygin, guc, nedenler

print("""
==============================
   VIROSA - Password Tool
==============================
!key  -> Güçlü şifre öner
exit  -> Çıkış
""")

while True:
    giris = input("Komut veya şifre gir: ").strip()

    if giris.lower() == "exit":
        print("👋 Çıkış yapıldı.")
        break

    elif giris == "!key":
        print("🔑 Önerilen güçlü şifre:", guclu_sifre_uret())

    elif giris == "":
        print("⚠️ Boş giriş.")
        continue

    else:
        yaygin, guc, nedenler = sifre_analiz(giris)
        sure = kirilma_suresi_hesapla(giris)

        print("\n🔍 Analiz Sonucu")
        print("----------------")
        print("Durum:", guc)

        if yaygin:
            print("⚠️ Yaygın şifre tespit edildi")

        print("⏱️ Tahmini kırılma süresi:", sure)

        if nedenler:
            print("\n📌 Zayıflık nedenleri:")
            for n in nedenler:
                print(" -", n)
        else:
            print("🎉 Belirgin bir zayıflık bulunamadı")

        print()
