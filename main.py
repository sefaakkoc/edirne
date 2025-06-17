import os
import requests
import git

# GitHub repository URL ve kullanıcı bilgisi
REPO_OWNER = 'sefaakkoc'  # GitHub kullanıcı adı
REPO_NAME = 'edirne'        # GitHub repo adı
REPO_DIR = 'C:\\Users\\sefaa\\Desktop\\edirne'    # Depo yerel yolu (programınızın bulunduğu dizin)

# GitHub API URL'si (en son sürümü almak için)
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest'

def check_for_update():
    """GitHub API'sinden en son sürümü alır."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        latest_release = response.json()
        return latest_release['tag_name']  # Son sürüm numarasını döndürür
    else:
        print(f"GitHub API hatası: {response.status_code}")
        return None

def update_repository():
    """GitHub'dan yeni sürüm varsa, yerel repo'yu günceller."""
    try:
        # Git depo objesi oluştur
        repo = git.Repo(REPO_DIR)
        
        # GitHub'dan yeni sürüm olup olmadığını kontrol et
        latest_version = check_for_update()
        if latest_version:
            print(f"Güncelleme mevcut: {latest_version}.")
            
            # Repo'yu güncellemek için origin'den fetch ve merge işlemi yap
            origin = repo.remotes.origin
            origin.fetch()  # Değişiklikleri uzak depodan al
            repo.git.merge('origin/main')  # veya 'origin/master' kullanabilirsiniz
            print("Güncelleme başarılı!")
        else:
            print("En son sürümde güncelleme yok.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")

def run_after_update():
    """Güncelleme sonrası çalışacak kod."""
    print("Güncelleme tamamlandı, yeni kod çalıştırılıyor...")
    try:
        # Güncellenen dosyaları çalıştırmak için örnek olarak:
        os.system("python script.py")  # script.py yerine çalıştırmak istediğiniz dosya adı
    except Exception as e:
        print(f"Script çalıştırma hatası: {e}")

if __name__ == "__main__":
    update_repository()  # Depoyu güncelle
    run_after_update()   # Güncelleme sonrası çalışacak kod
