import argparse
from PIL import Image
import base64
import json
import yaml
import glob
import os.path

SOURCE_DIR = os.path.curdir
TARGET_DIR = os.path.curdir

def decode_character_card(card_path, is_V2 = False):
    im = Image.open(card_path)
    im.load()
    chara_card = None
    if im.info is not None and "chara" in im.info:
        decoded = base64.b64decode(im.info["chara"])
        chara_card = json.loads(decoded)
        if is_V2 and 'data' in chara_card:
            chara_card = chara_card['data']
        keys = {
            'name' : 'char_name',
            'description' : 'char_persona',
            'scenario' : 'world_scenario',
            'mes_example' : 'example_dialogue',
            'first_mes' : 'char_greeting'
        }
        for key in keys:
            chara_card[keys[key]] = chara_card[key]
    else:
        print("Could not find character info in card: " + card_path)
    return chara_card

def save_card_as_json(card_path, json_content, type, target_dir):
    if 'name' in json_content:
        character_name = json_content['name']

        copy_image_filename = os.path.join(target_dir, character_name + ".png")
        image = Image.open(card_path)
        data = list(image.getdata())
        image2 = Image.new(image.mode, image.size)
        image2.putdata(data)
        image2.save(copy_image_filename)

        if type == "JSON" or type == "JSON&YAML": 
            json_filename = os.path.join(target_dir, character_name + ".json")
            with open(json_filename, 'w') as json_file:
                json_file.write(json.dumps(json_content))

        if type == "YAML" or type == "JSON&YAML": 
            yaml_filename = os.path.join(target_dir, character_name + ".yaml")
            yaml_string=yaml.dump(json_content)
            with open(yaml_filename, 'w') as yaml_file:
                yaml_file.write(yaml_string)
    else:
        ("Could not find name filed in: " + card_path)

def main():
    parser = argparse.ArgumentParser(
                    prog='CharacterCardConverter',
                    description='Converts V2 and Tavern type character cards to yaml and json format for use in text-generation-webui',
                    epilog='The default is files from current folder are converted into current folder into both YAML and JSON'
                    )
    parser.add_argument('--type', choices=['JSON', 'YAML', 'JSON&YAML'], default = "JSON&YAML", required=False)
    parser.add_argument('--source', default = SOURCE_DIR, required=False)
    parser.add_argument('--target', default = TARGET_DIR, required=False)
    args = parser.parse_args()
    print(f"Conversion type: {args.type}")
    print(f"Source dir: {args.source}")
    print(f"target dir: {args.target}")

    v2_pattern = os.path.join(args.source, "*spec_v2.png")
    tavern_pattern = os.path.join(args.source, "*tavern.png")

    v2_cards = glob.glob(v2_pattern)
    tavern_cards = glob.glob(tavern_pattern)

    if v2_cards is not None:
        for v2_card in v2_cards:
            print("Unwrapping v2 card: " + v2_card)
            json_content = decode_character_card(v2_card, True)
            save_card_as_json(v2_card, json_content, args.type, args.target)
    if tavern_cards is not None:
        for tavern_card in tavern_cards:
            print("Unwrapping tavern card: " + tavern_card)
            json_content =  decode_character_card(tavern_card)
            save_card_as_json(tavern_card, json_content, args.type, args.target)

if __name__ == "__main__":
    main()