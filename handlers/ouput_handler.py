import os
import pickle
from PIL import Image
from utils.helpers import connectors_list, BASE_DIR, remove_directory_content


def generate_ksk_images(ksk_name: str, ksk_data: list):

    create_ksk_directory('output', ksk_name)

    used_connectors = [connector for connector, _ in ksk_data]
    directory = f'output/{ksk_name}'
    for connector in used_connectors:
        empty_cavities = [cavity for conn,
                          cavity in ksk_data if connector == conn]
        connector_image = Image.open(
            f'input/images/connectors/{connector}.png')
        for cavity in connectors_list[connector]:
            if cavity not in empty_cavities:
                plug = Image.open(
                    f'input/images/plugs/{connectors_list[connector][cavity][1]}.png')
                connector_image.paste(
                    plug, connectors_list[connector][cavity][0])

        connector_image.save(f'{directory}/new{connector}.png', quality=95)


def search_for_ksk(query: str = "") -> list:
    """Return a ksk list that match the search query"""
    ksk_names = []
    for ksk_name in os.listdir('output'):
        if ksk_name.upper().startswith(query.upper()):
            ksk_names.append(f'{ksk_name}')
    return ksk_names


def get_ksk_from_history(ksk_name) -> list:
    """return a list of images that belong to a ksk"""
    images = []
    ksk_path = f'output/{ksk_name}'
    if os.path.exists(ksk_path):
        for img_name in os.listdir(ksk_path):
            images.append(f'{ksk_path}/{img_name}')
    return images


def create_ksk_directory(parent_dir: str, ksk_name: str):
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    ksk_path = os.path.join(BASE_DIR, f'{parent_dir}/{ksk_name}')
    if os.path.exists(ksk_path):
        remove_directory_content(ksk_path)
    os.mkdir(ksk_path)


def dump_ksk_object(ksk_list: dict):
    with open('output/ksk.back', 'wb') as ksk_file:
        pickle.dump(ksk_list, ksk_file)


def load_ksk_object():
    with open('output/ksk.back', 'rb') as ksk_file:
        ksk_list = pickle.load(ksk_file)
    return ksk_list
