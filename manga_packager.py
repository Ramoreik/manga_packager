from zipfile import ZipFile
import os
import glob
import argparse
from PIL import Image

KNOWN_MANGA_IMAGES_EXTENSIONS = ('*.jpg', '*.png', '*.webp')
PACKAGE_DIRECTORY_NAME = "packaged"



def handle_arguments():
    print("handling arguments")
    parser = argparse.ArgumentParser(description='Program that takes in a folder and packages manga volumes in zips under it')
    parser.add_argument('--folder','-f', required=True, help="Parent folders of all the volumes you want to package")
    parser.add_argument('--title','-t', required=True, help="Give the manga name to the packager")
    args = parser.parse_args()
    return args


def find_volume_folders(folder):
    volume_folders = []
    for element in os.listdir(folder):
        full_path = os.path.join(folder, element)
        if os.path.isdir(full_path) and element != "packaged":
            volume_folders.append(element)
    return volume_folders


def find_images(volume_folder):
    images = []
    for wanted_type in KNOWN_MANGA_IMAGES_EXTENSIONS:
        image_path = os.path.join(volume_folder, wanted_type)
        images_found = glob.glob(os.path.join(volume_folder, wanted_type))
        if wanted_type == "*.webp":
            print("Found webp images, converting to jpg ...")
            images_found = convert_webp_to_jpg(images_found)
        images.extend(images_found)
    return images


def make_package_directory(folder):
    packaged_directory = os.path.join(folder, PACKAGE_DIRECTORY_NAME)
    if not os.path.exists(packaged_directory):
       os.mkdir(packaged_directory) 


def package_volume_images(images, manga, volume, root_folder):
    filename = "{}-{}".format(manga, volume)
    full_path = os.path.join(root_folder, PACKAGE_DIRECTORY_NAME, filename)
    print("packaging {} ...".format(full_path))
    with ZipFile('{}.zip'.format(full_path), 'w') as zip:
        for image in images:
            zip.write(image)


def convert_webp_to_jpg(images):
    converted_images = []
    for image in images:
        im = Image.open(image).convert("RGB")
        converted_image_path = "{}.jpg".format(image[:image.find(".webp")])
        im.save(converted_image_path)
        if os.path.exists(converted_image_path):
            os.remove(image)
        converted_images.append(converted_image_path)
    return converted_images


if __name__ == "__main__": 
    print("Initiating packaging ...")
    args = handle_arguments()
    root_folder = args.folder
    print(root_folder)
    make_package_directory(root_folder)
    volumes = find_volume_folders(root_folder)
    for volume in volumes:
        full_path = os.path.join(root_folder, volume)
        images = find_images(full_path)
        package_volume_images(images, args.title, volume, root_folder)
    print("Packaging done, output packages will be here : {}".format(os.path.join(root_folder, PACKAGE_DIRECTORY_NAME)))
