import os
import pickle
from datetime import datetime
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
    dates = {}
    KSK_list = load_KSK_object()
    for KSK_name in KSK_list.keys():
        KSK_date = str(KSK_list[KSK_name][0].date())
        if KSK_name.upper().startswith(query.upper()):
                KSK_names.append(f'{KSK_name}')
        if KSK_date not in dates:
            dates[KSK_date] = []
        dates[KSK_date].append(KSK_name)
    return KSK_names, dates


def get_KSK(KSK_name):
    """return a list of images that belong to a KSK"""
    all_KSK = load_KSK_object()
    if KSK_name in all_KSK:
        generate_KSK_images(KSK_name, all_KSK[KSK_name][1])


def create_KSK_directory(parent_dir: str, KSK_name: str):
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    else:
        remove_directory_content(parent_dir)
    KSK_path = os.path.join(parent_dir, KSK_name)
    if os.path.exists(KSK_path):
        remove_directory(KSK_path)
    os.mkdir(KSK_path)


def dump_KSK_object(all_KSK: dict):
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/KSK.back', 'wb') as KSK_file:
        pickle.dump(all_KSK, KSK_file)


def load_KSK_object() -> dict:
    if not os.path.exists('data/KSK.back'):
        return {}
    with open('data/KSK.back', 'rb') as KSK_file:
        all_KSK = pickle.load(KSK_file)
    return all_KSK
