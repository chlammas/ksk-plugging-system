import os
import pickle
from PIL import Image
from utils.helpers import connectors_list, remove_directory, remove_directory_content


def generate_KSK_images(KSK_name: str, KSK_data: list):

    create_KSK_directory('output', KSK_name)

    used_connectors = [connector for connector, _ in KSK_data]
    directory = f'output/{KSK_name}'
    for connector in used_connectors:
        empty_cavities = [cavity for conn,
                          cavity in KSK_data if connector == conn]
        connector_image = Image.open(
            f'input/images/connectors/{connector}.png')
        for cavity in connectors_list[connector]:
            if cavity not in empty_cavities:
                plug = Image.open(
                    f'input/images/plugs/{connectors_list[connector][cavity][1]}.png')
                connector_image.paste(
                    plug, connectors_list[connector][cavity][0])

        connector_image.save(f'{directory}/new{connector}.png', quality=95)


def search_for_KSK(query: str = "") -> list:
    """Return a KSK list that match the search query"""
    KSK_names = []
    KSK_list = load_KSK_object()
    for KSK_name in KSK_list.keys():
        if KSK_name.upper().startswith(query.upper()):
            KSK_names.append(f'{KSK_name}')
    return KSK_names


def get_KSK(KSK_name):
    """return a list of images that belong to a KSK"""
    KSK_list = load_KSK_object()
    if KSK_name in KSK_list:
        generate_KSK_images(KSK_name, KSK_list[KSK_name])


def create_KSK_directory(parent_dir: str, KSK_name: str):
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    else:
        remove_directory_content(parent_dir)
    KSK_path = os.path.join(parent_dir, KSK_name)
    if os.path.exists(KSK_path):
        remove_directory(KSK_path)
    os.mkdir(KSK_path)



def dump_KSK_object(KSK_list: dict):
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/KSK.back', 'wb') as KSK_file:
        pickle.dump(KSK_list, KSK_file)


def load_KSK_object() -> dict:
    if not os.path.exists('data/KSK.back'):
        return {}
    with open('data/KSK.back', 'rb') as KSK_file:
        KSK_list = pickle.load(KSK_file)
    return KSK_list

