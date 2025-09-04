# Cafe Life QR Kod Oluşturucu
# PyCharm'da çalıştırmak için gerekli kütüphaneler: pip install qrcode[pil] pillow

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


def create_cafe_qr_code(url, output_dir="qr_codes"):
    """
    Cafe Life için özelleştirilmiş QR kod oluşturur
    """

    # Çıktı klasörünü oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("CAFE LIFE QR KOD OLUŞTURUCU")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Çıktı klasörü: {output_dir}")

    # QR kod ayarları
    qr = qrcode.QRCode(
        version=1,  # QR kodun boyutu (1-40 arası)
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Hata düzeltme seviyesi
        box_size=10,  # Her kutunun piksel boyutu
        border=4,  # Kenar boşluğu
    )

    # URL'yi QR koda ekle
    qr.add_data(url)
    qr.make(fit=True)

    # QR kod renkli tema - Cafe Life temasına uygun
    cafe_colors = [
        ('#ff6b35', 'white'),  # Ana tema: Turuncu-Beyaz
        ('#ff9a56', 'white'),  # Açık turuncu-Beyaz
        ('black', 'white'),  # Klasik siyah-Beyaz
        ('#8B4513', '#FFE4B3'),  # Kahverengi-Krem
    ]

    qr_codes = []

    for i, (fill_color, back_color) in enumerate(cafe_colors, 1):
        # QR kodu oluştur
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Boyutu ayarla (800x800 piksel)
        qr_img = qr_img.resize((800, 800), Image.Resampling.LANCZOS)

        # Yeni bir canvas oluştur (logo ve yazı için ekstra alan)
        canvas_width, canvas_height = 800, 1000
        canvas = Image.new('RGB', (canvas_width, canvas_height), back_color)

        # QR kodu ortala
        qr_x = (canvas_width - 800) // 2
        qr_y = 100  # Üstte biraz boşluk bırak
        canvas.paste(qr_img, (qr_x, qr_y))

        # Yazı ekle
        draw = ImageDraw.Draw(canvas)

        try:
            # Sistem fontunu bul (Windows/Linux/Mac uyumlu)
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
            url_font = ImageFont.truetype("arial.ttf", 20)
        except:
            # Varsayılan font kullan
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            url_font = ImageFont.load_default()

        # Başlık
        title_text = "CAFE LIFE"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (canvas_width - title_width) // 2
        draw.text((title_x, 20), title_text, fill=fill_color, font=title_font)

        # Alt başlık
        subtitle_text = "DİJİTAL MENÜ"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (canvas_width - subtitle_width) // 2
        draw.text((subtitle_x, 70), subtitle_text, fill=fill_color, font=subtitle_font)

        # QR kod altına açıklama
        instruction_text = "Kameranızı QR koda tutun"
        instruction_bbox = draw.textbbox((0, 0), instruction_text, font=subtitle_font)
        instruction_width = instruction_bbox[2] - instruction_bbox[0]
        instruction_x = (canvas_width - instruction_width) // 2
        draw.text((instruction_x, 920), instruction_text, fill=fill_color, font=subtitle_font)

        # URL bilgisi (küçük yazıyla)
        url_text = f"{url[:50]}{'...' if len(url) > 50 else ''}"
        url_bbox = draw.textbbox((0, 0), url_text, font=url_font)
        url_width = url_bbox[2] - url_bbox[0]
        url_x = (canvas_width - url_width) // 2
        draw.text((url_x, 960), url_text, fill='gray', font=url_font)

        # Dosya adı
        color_name = fill_color.replace('#', '').replace(' ', '_')
        filename = f"cafe_life_qr_{color_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(output_dir, filename)

        # Kaydet
        canvas.save(filepath, 'PNG', quality=95)
        qr_codes.append(filepath)

        print(f"QR Kod {i}: {filename}")
        print(f"   Renk: {fill_color} / {back_color}")
        print(f"   Boyut: {canvas.size}")

    return qr_codes


def create_table_tent_qr(url, output_dir="qr_codes"):
    """
    Masa üstü çadır tarzı QR kod kartı oluşturur - Logo ile
    """
    print("\nMASA ÇADİR KARTI OLUŞTURULUYOR...")

    # A4 boyutu (300 DPI): 2480x3508 piksel
    # Yarım A4 yatay: 3508x1240 piksel (katlanacak)
    card_width, card_height = 2480, 1240

    # Canvas oluştur
    canvas = Image.new('RGB', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(canvas)

    # Arka plan gradyanı benzeri efekt
    for y in range(card_height):
        ratio = y / card_height
        r = int(255 * (1 - ratio * 0.1))
        g = int(154 + 101 * ratio * 0.3)
        b = int(86 + 169 * ratio * 0.2)
        color = (r, g, b)
        draw.rectangle([(0, y), (card_width, y + 1)], fill=color)

        # Logo kontrol - debug bilgisi ekleyin
        print("Mevcut dizin:", os.getcwd())
        print("Logo dosyası aranıyor...")

        logo_paths = [
            "assets/images/logo.jpg",
            "assets/images/logo.png",
            "logo.jpg",
            "logo.png"
        ]

        for path in logo_paths:
            print(f"Kontrol ediliyor: {path} - {'✓ VAR' if os.path.exists(path) else '✗ YOK'}")

        # Dosya listesini göster
        if os.path.exists("assets/images"):
            print("assets/images klasöründeki dosyalar:")
            for f in os.listdir("assets/images"):
                print(f"  - {f}")

    # Logo yüklemeyi dene
    logo_img = None
    logo_paths = [
        "assets/images/logo.jpg",
        "assets/images/logo.png",
        "assets\\images\\logo.jpg",
        "assets\\images\\logo.png"
    ]

    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
                print(f"Logo bulundu: {logo_path}")
                break
            except Exception as e:
                print(f"Logo yükleme hatası: {e}")
                continue

    # Sol yarı: QR kod
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=8, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color='#ff6b35', back_color='white')
    qr_img = qr_img.resize((400, 400), Image.Resampling.LANCZOS)

    # QR kodu sol tarafa yerleştir
    canvas.paste(qr_img, (200, (card_height - 400) // 2))

    # Logo varsa, QR kodun üstüne yerleştir
    if logo_img:
        logo_x = 200 + (400 - 150) // 2  # QR kodun ortasına
        logo_y = (card_height - 400) // 2 - 180  # QR kodun üstüne

        # Logo için beyaz arka plan (daire)
        logo_bg = Image.new('RGBA', (170, 170), (255, 255, 255, 0))
        logo_bg_draw = ImageDraw.Draw(logo_bg)
        logo_bg_draw.ellipse([0, 0, 170, 170], fill=(255, 255, 255, 255))

        # Logo arka planını yapıştır
        canvas.paste(logo_bg, (logo_x - 10, logo_y - 10), logo_bg)

        # Logoyu yapıştır
        if logo_img.mode == 'RGBA':
            canvas.paste(logo_img, (logo_x, logo_y), logo_img)
        else:
            canvas.paste(logo_img, (logo_x, logo_y))

    # Sağ yarı: Yazılar
    try:
        big_font = ImageFont.truetype("arial.ttf", 120)
        medium_font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 40)
    except:
        big_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Başlık
    title_x = card_width // 2 + 200
    draw.text((title_x, 150), "CAFE LIFE", fill='white', font=big_font)
    draw.text((title_x, 280), "DİJİTAL MENÜ", fill='white', font=medium_font)

    # Açıklama
    draw.text((title_x, 450), "QR kodu okut", fill='white', font=medium_font)
    draw.text((title_x, 520), "Menüyü görüntüle", fill='white', font=medium_font)
    draw.text((title_x, 590), "Siparişini ver", fill='white', font=medium_font)

    # WiFi bilgisi (isteğe bağlı)
    draw.text((title_x, 700), "WiFi: CafeLife_Guest", fill='lightgray', font=small_font)

    # Kaydet
    tent_filename = f"cafe_life_table_tent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    tent_filepath = os.path.join(output_dir, tent_filename)
    canvas.save(tent_filepath, 'PNG', quality=95, dpi=(300, 300))

    print(f"Masa çadır kartı: {tent_filename}")
    return tent_filepath


def create_small_qr_stickers(url, output_dir="qr_codes"):
    """
    Küçük QR kod etiketleri oluşturur (masalar için)
    """
    print("\nKÜÇÜK QR ETİKETLERİ OLUŞTURULUYOR...")

    # 5x5 cm sticker boyutu (300 DPI): 590x590 piksel
    sticker_size = 590
    stickers_per_sheet = 4  # A4'te 4 adet

    # A4 boyutu
    sheet_width, sheet_height = 2480, 3508
    canvas = Image.new('RGB', (sheet_width, sheet_height), 'white')

    # QR kod oluştur
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)

    positions = [
        (300, 400),  # Sol üst
        (1590, 400),  # Sağ üst
        (300, 2500),  # Sol alt
        (1590, 2500)  # Sağ alt
    ]

    for i, (x, y) in enumerate(positions):
        # QR kod oluştur
        qr_img = qr.make_image(fill_color='#ff6b35', back_color='white')
        qr_img = qr_img.resize((400, 400), Image.Resampling.LANCZOS)

        # Sticker alanı
        sticker_canvas = Image.new('RGB', (sticker_size, sticker_size), 'white')
        draw = ImageDraw.Draw(sticker_canvas)

        # Kenarlık
        draw.rectangle([0, 0, sticker_size - 1, sticker_size - 1], outline='#ff6b35', width=5)

        # QR kodu ortala
        qr_x = (sticker_size - 400) // 2
        qr_y = 50
        sticker_canvas.paste(qr_img, (qr_x, qr_y))

        # Yazı
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        text = "CAFE LIFE MENÜ"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (sticker_size - text_width) // 2
        draw.text((text_x, 480), text, fill='#ff6b35', font=font)

        # Masa numarası
        table_text = f"MASA {i + 1}"
        table_bbox = draw.textbbox((0, 0), table_text, font=font)
        table_width = table_bbox[2] - table_bbox[0]
        table_x = (sticker_size - table_width) // 2
        draw.text((table_x, 520), table_text, fill='gray', font=font)

        # Ana canvas'a yapıştır
        canvas.paste(sticker_canvas, (x, y))

    # Kaydet
    sticker_filename = f"cafe_life_stickers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    sticker_filepath = os.path.join(output_dir, sticker_filename)
    canvas.save(sticker_filepath, 'PNG', quality=95, dpi=(300, 300))

    print(f"Sticker sayfası: {sticker_filename}")
    return sticker_filepath


def main():
    """Ana program"""
    print("=" * 60)
    print("CAFE LIFE QR KOD OLUŞTURUCU v1.0")
    print("=" * 60)

    # URL'yi buraya gir (Netlify'dan aldıktan sonra)
    menu_url = input("Menü URL'sini girin: ").strip()

    if not menu_url:
        print("URL boş olamaz!")
        return

    if not menu_url.startswith(('http://', 'https://')):
        menu_url = 'https://' + menu_url

    print(f"Hedef URL: {menu_url}")

    try:
        # QR kodları oluştur
        qr_files = create_cafe_qr_code(menu_url)

        # Masa çadır kartı oluştur
        tent_file = create_table_tent_qr(menu_url)

        # Küçük sticker'lar oluştur
        sticker_file = create_small_qr_stickers(menu_url)

        print("\n" + "=" * 60)
        print("BAŞARIYLA TAMAMLANDI!")
        print("=" * 60)
        print(f"Toplam {len(qr_files) + 2} dosya oluşturuldu:")

        for qr_file in qr_files:
            print(f"   {os.path.basename(qr_file)}")
        print(f"   {os.path.basename(tent_file)}")
        print(f"   {os.path.basename(sticker_file)}")

        print(f"\nKULLANIM ÖNERİLERİ:")
        print(f"   • Renkli QR kodları farklı yerlerde kullan")
        print(f"   • Masa çadır kartını A4'te yazdır ve katla")
        print(f"   • Sticker'ları kes ve masalara yapıştır")
        print(f"   • QR kodları 5cm x 5cm'den küçük yazdırma")
        print(f"   • Test et: Telefon kamerasıyla okutabildiğini kontrol et")

        # Klasörü aç (Windows)
        try:
            import subprocess
            import platform
            if platform.system() == "Windows":
                subprocess.run(['explorer', os.path.abspath('qr_codes')])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', os.path.abspath('qr_codes')])
            else:  # Linux
                subprocess.run(['xdg-open', os.path.abspath('qr_codes')])
        except:
            print(f"QR kodlar '{os.path.abspath('qr_codes')}' klasöründe")

    except Exception as e:
        print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    main()