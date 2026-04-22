import random
import string
import re
import os
import math

# Renk kodları (Terminal için)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

DAHILI_YAYGIN = {"123456", "password", "123456789", "qwerty", "admin", "letmein"}

def yaygin_sifreleri_yukle():
    if os.path.exists("rockyou.txt"):
        try:
            with open("rockyou.txt", "r", encoding="latin-1") as f:
                return set(s.strip().lower() for s in f)
        except Exception:
            return DAHILI_YAYGIN
    return DAHILI_YAYGIN

YAYGIN_SIFRELER = yaygin_sifreleri_yukle()

def entropi_hesapla(sifre):
    """Şifrenin bilgi teorisine göre rastgeleliğini (bit cinsinden) hesaplar."""
    if not sifre: return 0
    karakter_seti = 0
    if re.search(r"[a-z]", sifre): karakter_seti += 26
    if re.search(r"[A-Z]", sifre): karakter_seti += 26
    if re.search(r"[0-9]", sifre): karakter_seti += 10
    if re.search(r"[^a-zA-Z0-9]", sifre): karakter_seti += 32
    
    # Entropi Formülü: E = log2(KarakterSeti^Uzunluk)
    return math.log2(karakter_seti) * len(sifre) if karakter_seti > 0 else 0

def guclu_sifre_uret(uzunluk=16):
    karakterler = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    # Güvenli seçim için SystemRandom kullanılması önerilir
    return "".join(random.SystemRandom().choice(karakterler) for _ in range(uzunluk))

def sure_formatla(saniye):
    if saniye < 1: return "Anlık"
    birimler = [
        (31536000, "yıl"),
        (86400, "gün"),
        (3600, "saat"),
        (60, "dakika"),
        (1, "saniye")
    ]
    for sn, ad in birimler:
        if saniye >= sn:
            deger = int(saniye / sn)
            return f"{deger}+ {ad}"
    return "Saniyeler içinde"

def analiz_et(sifre):
    nedenler = []
    puan = 0
    
    # Kriterler
    kriterler = [
        (r"[a-z]", "Küçük harf eksik"),
        (r"[A-Z]", "Büyük harf eksik"),
        (r"[0-9]", "Rakam eksik"),
        (r"[^a-zA-Z0-9]", "Özel karakter eksik")
    ]
    
    if len(sifre) < 10: nedenler.append("Boyut çok kısa (Önerilen: 12+)")
    else: puan += 1

    for regex, hata in kriterler:
        if re.search(regex, sifre): puan += 1
        else: nedenler.append(hata)

    is_yaygin = sifre.lower() in YAYGIN_SIFRELER
    entropi = entropi_hesapla(sifre)
    
    # Kırılma Süresi (Saniyede 10 Milyar deneme varsayımı - GPU Cluster)
    deneme_hizi = 10_000_000_000
    tahmini_saniye = (2**entropi) / deneme_hizi if entropi > 0 else 0
    
    # Güç Belirleme
    if is_yaygin: durum = f"{RED}KRİTİK: Yaygın Şifre{RESET}"
    elif entropi < 45: durum = f"{RED}Zayıf{RESET}"
    elif entropi < 60: durum = f"{YELLOW}Orta{RESET}"
    elif entropi < 80: durum = f"{GREEN}İyi{RESET}"
    else: durum = f"{BLUE}Çok Güçlü (Askeri Seviye){RESET}"
    
    return durum, entropi, sure_formatla(tahmini_saniye), nedenler

# --- Arayüz ---
print(f"""
{BLUE}==========================================
   VIROSA v2.0 - Siber Güvenlik Analiz
=========================================={RESET}
{YELLOW}Komutlar:{RESET}
!gen [uzunluk] -> Şifre üret (Örn: !gen 16)
exit           -> Çıkış
""")

while True:
    try:
        user_input = input(f"{BLUE}Virosa > {RESET}").strip()
        
        if not user_input: continue
        if user_input.lower() == "exit": break
        
        if user_input.startswith("!gen"):
            parts = user_input.split()
            uzunluk = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 14
            print(f"🔑 Önerilen: {GREEN}{guclu_sifre_uret(uzunluk)}{RESET}\n")
            continue

        # Analiz Başlat
        durum, ent, sure, hatalar = analiz_et(user_input)
        
        print(f"\n{BLUE}--- Analiz Sonucu ---{RESET}")
        print(f"Güç Durumu: {durum}")
        print(f"Entropi   : {ent:.2f} bit")
        print(f"Kırılma   : ~{sure} (Modern bir PC ile)")
        
        if hatalar:
            print(f"{YELLOW}Zayıf Noktalar:{RESET}")
            for h in hatalar: print(f" • {h}")
        else:
            print(f"{GREEN}✔ Harika bir şifre!{RESET}")
        print("-" * 25 + "\n")

    except KeyboardInterrupt:
        break