from ddgs import DDGS
import requests
import os
import shutil
import json
from PIL import Image
from io import BytesIO

def clean_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Not a valid folder.")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")
        except Exception as e:
            print(f"Error deleting {item_path}: {e}")


def image_search(query:str, max_results:int = 3):
    results = DDGS().images(query=query, max_results=max_results)
    return results


def save_image(image_results, folder="downloads"):
    clean_folder(folder)
    os.makedirs(folder, exist_ok=True)

    for i, result in enumerate(image_results):
        url = result["image"]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Verifica se è davvero un'immagine (controlla intestazione + contenuto)
            image = Image.open(BytesIO(response.content))
            image_format = image.format.lower()  # jpg, png, webp, ecc.

            # Nome file con estensione corretta
            file_name = f"image_{i+1}.{image_format}"
            path = os.path.join(folder, file_name)

            image.save(path)
            print(f"Saved: {path}")

        except Exception as e:
            print(f"Error with {url}: {e}")

def image_retrieve(query, max_results:int = 3, folder="downloads"):
    save_image(image_search(query,max_results=max_results), folder=folder)


image_retrieve('example')