from PIL import Image
from utils.helpers import remove_directory_content, connectors_list, BASE_DIR,copy_directory_content
import os 
import shutil

def create_ksk_directory(parent_dir: str, ksk_name: str):
    if os.path.exists(parent_dir):
        remove_directory_content(parent_dir)
    else:
        os.mkdir(parent_dir)

    ksk_path = os.path.join(BASE_DIR, f'{parent_dir}/{ksk_name}')
    os.mkdir(ksk_path)

# {ksk_name: result}
def generate_ksk_images(ksk_name: str, ksk_data: list):
    create_ksk_directory('output', ksk_name)

    used_connectors = [connector for connector, _ in ksk_data]
    directory=f'output/{ksk_name}'
    for connector in used_connectors:
        empty_cavities = [cavity for conn, cavity in ksk_data if connector == conn]
        connector_image = Image.open(f'input/images/connectors/{connector}.png')
        for cavity in connectors_list[connector]:
            if cavity not in empty_cavities:
                plug = Image.open(
                    f'input/images/plugs/{connectors_list[connector][cavity][1]}.png')
                connector_image.paste(plug, connectors_list[connector][cavity][0])

        connector_image.save(f'{directory}/new{connector}.png', quality=95)
    if not os.path.exists("history"):
        os.mkdir("history")
    copy_directory_content(directory,f"history/{ksk_name}")
    
        

