# Cafe Life Web Uploader
# HTML dosyasını çeşitli platformlara otomatik yükler

import os
import requests
import json
import zipfile
import tempfile
import base64
from datetime import datetime
import webbrowser


class WebUploader:
    def __init__(self):
        self.html_file = None
        self.project_name = "cafe-life-menu"

    def find_html_file(self):
        """HTML dosyasını bulur"""
        # Önce root seviyede ara
        if os.path.exists("index.html"):
            self.html_file = "index.html"
            print(f"HTML dosyası bulundu: {self.html_file}")
            return True

        # Sonra assets klasöründe ara
        if os.path.exists("assets/html/index.html"):
            self.html_file = "assets/html/index.html"
            print(f"HTML dosyası bulundu: {self.html_file}")
            return True

        print("HTML dosyası bulunamadı!")
        return False

    def upload_to_netlify_drop(self):
        """Netlify Drop API ile yükleme"""
        print("Netlify'a yükleniyor...")

        try:
            # HTML dosyasını oku
            with open(self.html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Netlify'nin deploy API'sine POST
            files = {
                'index.html': html_content
            }

            # Zip dosyası oluştur
            zip_path = tempfile.mktemp(suffix='.zip')
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                zip_file.writestr('index.html', html_content)

            # Netlify'e yükle
            with open(zip_path, 'rb') as zip_file:
                response = requests.post(
                    'https://api.netlify.com/api/v1/sites',
                    files={'zip': zip_file},
                    headers={'Content-Type': 'application/zip'}
                )

            os.unlink(zip_path)

            if response.status_code == 201:
                site_data = response.json()
                url = f"https://{site_data['subdomain']}.netlify.app"
                print(f"Başarılı! URL: {url}")
                return url
            else:
                print(f"Hata: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Netlify yükleme hatası: {e}")
            return None

    def upload_to_github_pages(self, github_token=None, repo_name=None):
        """GitHub Pages'e yükleme"""
        print("GitHub Pages'e yükleniyor...")

        if not github_token:
            print("GitHub token gerekli!")
            print("Token almak için: https://github.com/settings/tokens")
            print("'repo' ve 'pages' yetkilerini verin")
            github_token = input("GitHub Token girin: ").strip()

        if not repo_name:
            repo_name = f"{self.project_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }

            # Repository oluştur
            repo_data = {
                'name': repo_name,
                'description': 'Cafe Life Digital Menu',
                'homepage': f'https://github.com/{github_token.split("_")[0]}/{repo_name}',
                'private': False,
                'auto_init': True
            }

            response = requests.post(
                'https://api.github.com/user/repos',
                headers=headers,
                json=repo_data
            )

            if response.status_code not in [201, 422]:  # 422 = repo zaten var
                print(f"Repo oluşturma hatası: {response.status_code}")
                return None

            repo_info = response.json()
            owner = repo_info['owner']['login']

            # HTML dosyasını oku ve encode et
            with open(self.html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            content_encoded = base64.b64encode(html_content.encode()).decode()

            # index.html dosyasını repo'ya yükle
            file_data = {
                'message': 'Add cafe menu HTML',
                'content': content_encoded,
                'branch': 'main'
            }

            response = requests.put(
                f'https://api.github.com/repos/{owner}/{repo_name}/contents/index.html',
                headers=headers,
                json=file_data
            )

            if response.status_code not in [201, 200]:
                print(f"Dosya yükleme hatası: {response.status_code}")
                return None

            # Pages'i aktifleştir
            pages_data = {
                'source': {
                    'branch': 'main',
                    'path': '/'
                }
            }

            response = requests.post(
                f'https://api.github.com/repos/{owner}/{repo_name}/pages',
                headers=headers,
                json=pages_data
            )

            url = f'https://{owner}.github.io/{repo_name}'
            print(f"Başarılı! URL: {url}")
            print("Not: GitHub Pages'in aktif olması birkaç dakika sürebilir")

            return url

        except Exception as e:
            print(f"GitHub yükleme hatası: {e}")
            return None

    def upload_to_vercel(self, vercel_token=None):
        """Vercel'e yükleme"""
        print("Vercel'e yükleniyor...")

        if not vercel_token:
            print("Vercel token gerekli!")
            print("Token almak için: https://vercel.com/account/tokens")
            vercel_token = input("Vercel Token girin: ").strip()

        try:
            headers = {
                'Authorization': f'Bearer {vercel_token}',
                'Content-Type': 'application/json'
            }

            # HTML dosyasını oku
            with open(self.html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Deployment verisi hazırla
            deployment_data = {
                'name': self.project_name,
                'files': [
                    {
                        'file': 'index.html',
                        'data': base64.b64encode(html_content.encode()).decode()
                    }
                ],
                'projectSettings': {
                    'framework': None
                }
            }

            response = requests.post(
                'https://api.vercel.com/v13/deployments',
                headers=headers,
                json=deployment_data
            )

            if response.status_code == 201:
                deployment_info = response.json()
                url = f"https://{deployment_info['url']}"
                print(f"Başarılı! URL: {url}")
                return url
            else:
                print(f"Vercel yükleme hatası: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Vercel yükleme hatası: {e}")
            return None

    def create_zip_for_manual_upload(self):
        """Manuel yükleme için ZIP dosyası oluştur"""
        print("Manuel yükleme için ZIP dosyası oluşturuluyor...")

        try:
            zip_filename = f"{self.project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            zip_path = os.path.join('qr_codes', zip_filename)

            # qr_codes klasörünü oluştur
            os.makedirs('qr_codes', exist_ok=True)

            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                # HTML dosyasını index.html olarak ekle
                with open(self.html_file, 'r', encoding='utf-8') as f:
                    zip_file.writestr('index.html', f.read())

                # Eğer assets/images klasörü varsa, görsel dosyalarını da ekle
                images_dir = 'assets/images'
                if os.path.exists(images_dir):
                    for filename in os.listdir(images_dir):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                            file_path = os.path.join(images_dir, filename)
                            zip_file.write(file_path, f'images/{filename}')

            print(f"ZIP dosyası oluşturuldu: {zip_path}")
            print("Manuel yükleme seçenekleri:")
            print("1. Netlify Drop: https://app.netlify.com/drop")
            print("2. Vercel: https://vercel.com/new")
            print("3. Surge.sh: surge {zip_path}")

            return zip_path

        except Exception as e:
            print(f"ZIP oluşturma hatası: {e}")
            return None

    def show_menu(self):
        """Platform seçim menüsü"""
        print("\n" + "=" * 50)
        print("CAFE LIFE WEB UPLOADER")
        print("=" * 50)

        if not self.find_html_file():
            return

        print("\nYükleme Platformu Seçin:")
        print("1. Netlify (Otomatik) - Önerilen")
        print("2. GitHub Pages (Token gerekli)")
        print("3. Vercel (Token gerekli)")
        print("4. Manuel ZIP oluştur")
        print("5. Çıkış")

        while True:
            choice = input("\nSeçim (1-5): ").strip()

            if choice == "1":
                url = self.upload_to_netlify_drop()
                break
            elif choice == "2":
                url = self.upload_to_github_pages()
                break
            elif choice == "3":
                url = self.upload_to_vercel()
                break
            elif choice == "4":
                zip_path = self.create_zip_for_manual_upload()
                return zip_path
            elif choice == "5":
                print("Çıkılıyor...")
                return None
            else:
                print("Geçersiz seçim! Lütfen 1-5 arası bir sayı girin.")

        if 'url' in locals() and url:
            print(f"\n" + "=" * 50)
            print("YÜKLEME BAŞARILI!")
            print("=" * 50)
            print(f"Menü URL'si: {url}")

            # URL'yi clipboard'a kopyala (opsiyonel)
            try:
                import pyperclip
                pyperclip.copy(url)
                print("URL clipboard'a kopyalandı!")
            except ImportError:
                pass

            # Tarayıcıda aç
            open_browser = input("Tarayıcıda açmak ister misiniz? (e/h): ").strip().lower()
            if open_browser in ['e', 'evet', 'y', 'yes']:
                webbrowser.open(url)

            # QR kod oluşturma önerisi
            create_qr = input("QR kodları oluşturmak ister misiniz? (e/h): ").strip().lower()
            if create_qr in ['e', 'evet', 'y', 'yes']:
                try:
                    from . import qr_generator
                    qr_generator.main()
                except ImportError:
                    print("QR generator bulunamadı. Lütfen src/qr_generator.py çalıştırın")
                    print(f"URL: {url}")

            return url

        return None


def main():
    """Ana program"""
    uploader = WebUploader()
    uploader.show_menu()


if __name__ == "__main__":
    main()