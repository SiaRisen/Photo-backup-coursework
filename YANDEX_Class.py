import requests


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {"Content-Type": "application/json",
                "Authorization": f"OAuth {self.token}"}

    def get_folder(self, path_folder):
        url_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        response = requests.put(f"{url_folder}?path={path_folder}", headers=headers)
        if response.status_code == 201:
            print(f"Папка {path_folder} создана.")
        else:
            response.raise_for_status()

    def get_link_to_disk(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_files_to_disk(self, disk_file_path, photo_url):
        href = self.get_link_to_disk(disk_file_path).get("href", "")

        headers = self.get_headers()
        params = {"url": photo_url}
        response = requests.put(href, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print("Загрузка файла(-ов) завершена")
