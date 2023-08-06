from PIL import Image
import base64
import json
import yaml
import glob
import os.path

SOURCE_DIR = os.path.curdir
TARGET_DIR = os.path.curdir
V2_PATTERN = os.path.join(SOURCE_DIR, "*spec_v2.png")
TAVERN_PATTERN = os.path.join(SOURCE_DIR, "*tavern.png")

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

def save_card_as_json(card_path, json_content):
    if 'name' in json_content:
        character_name = json_content['name']

        copy_image_filename = os.path.join(TARGET_DIR, character_name + ".png")
        image = Image.open(card_path)
        data = list(image.getdata())
        image2 = Image.new(image.mode, image.size)
        image2.putdata(data)
        image2.save(copy_image_filename)

        json_filename = os.path.join(TARGET_DIR, character_name + ".json")
        with open(json_filename, 'w') as json_file:
            json_file.write(json.dumps(json_content))

        yaml_filename = os.path.join(TARGET_DIR, character_name + ".yaml")
        yaml_string=yaml.dump(json_content)
        with open(yaml_filename, 'w') as yaml_file:
            yaml_file.write(yaml_string)
    else:
        ("Could not find name filed in: " + card_path)

def main():
    v2_cards = glob.glob(V2_PATTERN)
    tavern_cards = glob.glob(TAVERN_PATTERN)
    if v2_cards is not None:
        for v2_card in v2_cards:
            print("Unwrapping v2 card: " + v2_card)
            json_content = decode_character_card(v2_card, True)
            save_card_as_json(v2_card, json_content)
    if tavern_cards is not None:
        for tavern_card in tavern_cards:
            print("Unwrapping tavern card: " + tavern_card)
            json_content =  decode_character_card(tavern_card)
            save_card_as_json(tavern_card, json_content)

if __name__ == "__main__":
    main()