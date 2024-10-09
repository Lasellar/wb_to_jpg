import requests
import zipfile
import os


def create_archive(article):
    with zipfile.ZipFile(f'{article}.zip', 'w') as archive:
        for foldername, subfolders, filenames in os.walk('images'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                archive.write(file_path, arcname=filename)
                os.remove(path=file_path)
    return f'{article}.zip'


def download_images(images_list, article):
    for image in images_list:
        response = requests.get(image)
        with open(fr'images\{article}_{images_list.index(image) + 1}.jpg', 'wb') as out:
            out.write(response.content)
    return create_archive(article)


def process(link):
    _link = f"{link[:link.find('/images') + 8]}big/"
    images_links_list_ = []
    _article = link[:link.find('/images')]
    try:
        article = _article[_article.find('/', -12) + 1:]
        for item in range(1, 30):
            image_url = f'{_link}{item}.webp'
            if item > 1:
                response = requests.get(image_url)
                if str(response) == '<Response [404]>':
                    return download_images(images_links_list_, article)
            images_links_list_.append(image_url)
        return download_images(images_links_list_, article)
    except Exception as exception:
        print(exception)
