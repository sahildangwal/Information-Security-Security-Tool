import requests
import argparse
import os
import shutil
from datetime import datetime

def scan_website(url):
    try:
        print(f"Scanning website: {url}")
        response = requests.get(url, verify=True)
        if response.status_code == 200:
            print("Website is vulnerable!")
            backup_dir = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{url.replace('https://', '').replace('http://', '')}"
            os.mkdir(backup_dir)
            for root, dirs, files in os.walk("."):
                for file in files:
                    if os.path.splitext(file)[1] in ['.php', '.html', '.js']:
                        file_path = os.path.join(root, file)
                        shutil.copy2(file_path, backup_dir)
                        print(f"Backed up file: {file_path}")
            return True
        else:
            print("Website is not vulnerable.")
            return False
    except Exception as e:
        print(f"Error scanning website: {e}")
        return False
    finally:
        try:
            os.rmdir(backup_dir)
            print(f"Deleted backup: {backup_dir}")
        except Exception as e:
            print(f"Error deleting backup: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL of the website to scan.")
    args = parser.parse_args()

    vulnerable = scan_website(args.url)

if __name__ == "__main__":
    main()
