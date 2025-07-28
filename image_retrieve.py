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
        if item_path== os.path.join(folder_path, 'urls.txt'):
            with open(item_path, 'w') as f:
                f.write('')
        else:
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                    print(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Deleted folder: {item_path}")
            except Exception as e:
                print(f"Error deleting {item_path}: {e}")


def process_image(result, urls, saved_images, folder):
    url = result["image"]
    if url in urls:
            return saved_images
    
    try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Verifica se è davvero un'immagine (controlla intestazione + contenuto)
            image = Image.open(BytesIO(response.content))
            image_format = image.format.lower()  # jpg, png, webp, ecc.

            # Nome file con estensione corretta
            file_name = f"image_{saved_images+1}.{image_format}"
            path = os.path.join(folder, file_name)

            image.save(path)
            print(f"Saved: {path}")

            with open(os.path.join(folder,'urls.txt'),'a') as f:
                f.write(url+'\n')
            urls.append(url)

            saved_images+=1
            return saved_images

    except Exception as e:
            print(f"Error with {url}: {e}")
            return saved_images
    

    
def image_retrieve(query, max_results:int = 3, folder="downloads"):
    # save_image(image_search(query,max_results=max_results), folder=folder)
    image_results = DDGS().images(query=query, max_results=max_results)
    saved_images=0
    
    clean_folder(folder)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder,'urls.txt'),'r') as f:
        urls= f.readlines()
    
    for result in image_results:
        saved_images= process_image(result, urls, saved_images, folder)
    
    while saved_images < max_results:
        image_results = DDGS().images(query=query, max_results=max_results-saved_images+1)
        for result in image_results:
            saved_images= process_image(result, urls, saved_images, folder)



image_retrieve('example', max_results=20)