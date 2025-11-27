import os
import shutil

def organize_downloads(path):
    if not os.path.exists(path):
        return "Folder Downloads tidak ditemukan."

    files = os.listdir(path)
    if not files:
        return "Folder Downloads kosong."

    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            ext = file.split(".")[-1]
            folder = os.path.join(path, ext.upper())

            if not os.path.exists(folder):
                os.makedirs(folder)

            shutil.move(full_path, os.path.join(folder, file))

    return "Folder Downloads berhasil dirapikan!"
