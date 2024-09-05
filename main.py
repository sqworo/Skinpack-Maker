import os
import json
import uuid
import zipfile

def crear_uuid():
    return str(uuid.uuid4())

def crear_skins_json(folder_path):
    skin_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    name = input("Introduce el nombre de tu skinpack: ")

    skins_data = {
        "serialize_name": name,
        "localization_name": name,
        "skins": []
    }

    for i, skin_file in enumerate(skin_files):
        skin_entry = {
            "localization_name": f"Skin-{i+1}",
            "geometry": "geometry.humanoid.customSlim",
            "texture": skin_file,
            "type": "free"
        }
        skins_data["skins"].append(skin_entry)

    skins_json_path = os.path.join(folder_path, "skins.json")
    
    with open(skins_json_path, 'w') as json_file:
        json.dump(skins_data, json_file, indent=4)
    
    print(f"skins.json creado exitosamente en {folder_path}")

    manifest_data = {
        "header": {
            "name": name,
            "version": [1, 0, 0],
            "uuid": crear_uuid()
        },
        "modules": [
            {
                "version": [1, 0, 0],
                "type": "skin_pack",
                "uuid": crear_uuid()
            }
        ],
        "format_version": 1
    }

    manifest_json_path = os.path.join(folder_path, "manifest.json")
    
    with open(manifest_json_path, 'w') as json_file:
        json.dump(manifest_data, json_file, indent=4)
    
    print(f"manifest.json creado exitosamente en {folder_path}")

    crear_mcpack(folder_path, name)

def crear_mcpack(folder_path, pack_name):
    mcpack_name = f"{pack_name}.mcpack"
    mcpack_path = os.path.join(folder_path, mcpack_name)

    with zipfile.ZipFile(mcpack_path, 'w') as mcpack_zip:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.json') or file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    mcpack_zip.write(file_path, os.path.relpath(file_path, folder_path))

    print(f"Archivo {mcpack_name} creado exitosamente en {folder_path}")

folder_path = input("Introduce el directorio de tus skins: ")
crear_skins_json(folder_path)
