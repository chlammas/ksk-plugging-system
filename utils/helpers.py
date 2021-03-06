import os
import shutil

connectors_list = {
    # connector_id" {"cavity": [dimention, plug]}
    'IC81AB': {
        1: [(170, 110), 'P00000602'],
        2: [(230, 110), 'P00000621'],
        3: [(280, 110), 'P00000621'],
        4: [(335, 110), 'P00000621'],
        5: [(395, 110), 'P00000602'],
        6: [(125, 147), 'P00000621'],
        7: [(175, 147), 'P00000621'],
        8: [(230, 147), 'P00000621'],
        9: [(282, 147), 'P00000621'],
        10: [(335, 147), 'P00000621'],
        11: [(390, 147), 'P00000621'],
        12: [(441, 147), 'P00000621'],
        13: [(123, 180), 'P00000621'],
        14: [(176, 180), 'P00000621'],
        15: [(229, 180), 'P00000621'],
        16: [(282, 180), 'P00000621'],
        17: [(335, 180), 'P00000621'],
        18: [(390, 180), 'P00000621'],
        19: [(441, 180), 'P00000621'],
        20: [(170, 215), 'P00000602'],
        21: [(229, 215), 'P00000621'],
        22: [(282, 215), 'P00000621'],
        23: [(335, 215), 'P00000621'],
        24: [(397, 215), 'P00000602'],

    },
    'ICY0AB': {
        1: [(156, 103), 'P00000602'],
        2: [(225, 104), 'P00000621'],
        3: [(279, 104), 'P00000621'],
        4: [(333, 104), 'P00000621'],
        5: [(385, 103), 'P00000602'],
        6: [(118, 146), 'P00000621'],
        7: [(169, 146), 'P00000621'],
        8: [(225, 146), 'P00000621'],
        9: [(278, 146), 'P00000621'],
        10: [(330, 146), 'P00000621'],
        11: [(388, 146), 'P00000621'],
        12: [(440, 146), 'P00000621'],
        13: [(115, 178), 'P00000621'],
        14: [(169, 178), 'P00000621'],
        15: [(225, 178), 'P00000621'],
        16: [(278, 178), 'P00000621'],
        17: [(330, 178), 'P00000621'],
        18: [(388, 178), 'P00000621'],
        19: [(440, 178), 'P00000621'],
        20: [(157, 216), 'P00000602'],
        21: [(225, 220), 'P00000621'],
        22: [(278, 220), 'P00000621'],
        23: [(330, 220), 'P00000621'],
        24: [(385, 216), 'P00000602'],

    },
    '8426AC': {
        1: [(42, 106), 'P00102450'],
        2: [(96, 106), 'P00102450'],
        3: [(149, 106), 'P00102450'],
        4: [(202, 106), 'P00102450'],
        5: [(256, 106), 'P00102450'],
        6: [(309, 106), 'P00102450']
    },
    '8426AD': {
        1: [(42, 106), 'P00102450'],
        2: [(96, 106), 'P00102450'],
        3: [(149, 106), 'P00102450'],
        4: [(202, 106), 'P00102450'],
        5: [(256, 106), 'P00102450'],
        6: [(309, 106), 'P00102450']
    },
}


def remove_directory_content(dir_name):
    """Remove the whole directory content and keep it empty"""
    
    #dir_name = 'result'
    dir_path = dir_name
    if os.path.exists(dir_path):
        for child in os.listdir(dir_name):
            child_path = os.path.join(dir_path, child)
            if os.path.isfile(child_path):
                os.remove(child_path)
            elif os.path.isdir(child_path):
                remove_directory(child_path)


def remove_directory(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)


def copy_directory(dir_name, destination):
    """Copy the dir_name directory into the destiation directory"""

    if os.path.exists(destination):
        remove_directory(destination)
    shutil.copytree(dir_name, destination)
