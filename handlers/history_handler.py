import os



def search_for_ksk(query: str = "") -> list:
    """Return a ksk list that match the search query"""
    ksk_names = []
    for ksk_name in os.listdir('history'):
        if  ksk_name.upper().startswith(query.upper()):
            ksk_names.append(f'{ksk_name}')
    return ksk_names



def get_ksk_from_history(ksk_name) -> list:
    """return a list of images that belong to a ksk"""
    images = []
    ksk_path = f'history/{ksk_name}'
    if os.path.exists(ksk_path):
        for img_name in os.listdir(ksk_path): 
                images.append(f'{ksk_path}/{img_name}')
    return images

