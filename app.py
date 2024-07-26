import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB

        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                progress_bar.update(size)

        file_size = os.path.getsize(filename) / (1024*1024)
        print(f"\nDownload completed. File saved as: {filename}")
        print(f"File size: {file_size:.2f} MB")

        if file_size < 1:  # If file is smaller than 1 MB, it's likely a torrent file
            print("\nNOTE: This appears to be a torrent file, not the actual movie.")
            print("To download the movie, you need to use this file with a BitTorrent client.")
            print("1. Install a BitTorrent client like qBittorrent or uTorrent.")
            print("2. Open the downloaded .torrent file with your BitTorrent client.")
            print("3. The BitTorrent client will then download the actual movie file.")

        return os.path.abspath(filename)

    except requests.exceptions.RequestException as err:
        print(f"Error during download: {err}")
        return None

def main():
    url = input("Enter URL: ")
    default_name = os.path.basename(url.split('?')[0])
    filename = input(f"Rename (press Enter to keep '{default_name}'): ") or default_name
    
    file_path = download_file(url, filename)
    
    if not file_path:
        print("Download failed. Please check the URL and try again.")

if __name__ == "__main__":
    main()