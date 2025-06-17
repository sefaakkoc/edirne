import os
import requests
import git
import subprocess  # Yeni bir işlem çalıştırmak için

# GitHub repository URL ve kullanıcı bilgisi
REPO_OWNER = 'sefaakkoc'  # GitHub kullanıcı adı
REPO_NAME = 'edirne'        # GitHub repo adı
REPO_DIR = 'C:\\Users\\sefaa\\Desktop\\edirne'    # Depo yerel yolu

# GitHub API URL'si
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest'

def check_for_update():
    # GitHub API'sinden en son sürümü al
    response = requests.get(API_URL)
    if response.status_code == 200:
        latest_release = response.json()
        return latest_release['tag_name']
    else:
        print(f"GitHub API hatası: {response.status_code}")
        return None

def update_repository():
    try:
        # Git deposunu aç
        repo = git.Repo(REPO_DIR)
        
        # GitHub'dan yeni sürüm olup olmadığını kontrol et
        latest_version = check_for_update()
        if latest_version:
            # Eğer repo güncel değilse, güncelleme işlemi başlat
            print(f"Güncelleme mevcut. Sürüm: {latest_version}.")
            origin = repo.remotes.origin
            origin.fetch()
            # Ana dalda güncelleme yap
            repo.git.merge('origin/main')  # veya origin/master
            print("Güncelleme başarılı!")
            
            # Güncelleme tamamlandıktan sonra çalıştırılacak fonksiyonu çağır
            run_after_update()
        else:
            print("En son sürümde güncelleme yok.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")

def run_after_update():
    # Güncelleme sonrası çalışacak kod burada yer alır
    # Örneğin, bir script çalıştırmak:
    print("Güncelleme tamamlandı, yeni kod çalıştırılıyor...")
    
    try:
        # Örneğin, güncel dosya ile bir Python scripti çalıştırmak
        subprocess.run(['python', 'script.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Script çalıştırma hatası: {e}")

if __name__ == "__main__":
    update_repository()
