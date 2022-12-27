import time
from tqdm import tqdm
import json

from VK_Class import VkUser
from YANDEX_Class import YaUploader

with open("token.txt", "r") as file_object:
    vk_token = file_object.read().strip()


def get_photo_json():
    all_photos = user_vk.search_photo_profile()
    photos_list = []
    for items in all_photos:
        photos_dict = {"file_name": (str(items['likes']['count']) + "-" + str(items['date']) + ".jpg"),
                       "size": items['sizes'][-1]['type'], "url": items['sizes'][-1]['url']}
        photos_list.append(photos_dict)
    photo_json = json.dumps(photos_list, indent=4)
    with open("photos.json", "w") as file:
        file.write(photo_json)
    print("Информация о фото записана в json-файл")


def main():
    uploader.get_folder(path_to_folder)
    max_p = user_vk.parse_size_photo()
    prog_bar = tqdm(total=len(max_p))
    for keys, values in max_p.items():
        photo_url = values
        disk_file_path = f"/{path_to_folder}/{keys}"
        uploader.get_link_to_disk(disk_file_path)
        uploader.upload_files_to_disk(disk_file_path, photo_url)
        time.sleep(0.3)
        prog_bar.update(1)
    prog_bar.close()
    get_photo_json()


if __name__ == "__main__":
    path_to_folder = input("Введите имя папки на Yandex диске: ")
    token = input("Введите Yandex TOKEN: ")
    owner_id = input("Введите id или short-name нужного пользователя Vk: ")
    photo_count = int(input("Введите количество фотографий: "))
    vk_version = 5.131
    user_vk = VkUser(vk_token, vk_version, owner_id, photo_count)
    uploader = YaUploader(token)
    main()
