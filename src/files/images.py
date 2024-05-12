import shutil


def download_image(path: str, file):
    with open(path, 'wb+') as file_obj:
        shutil.copyfileobj(file, file_obj)
