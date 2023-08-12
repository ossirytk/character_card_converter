# character_card_converter
The character card converted is a batch converter for V2 and Tavern character cards.

The converter converts the character card into a JSON ot YAML formats and creates a character picture without exif data.

The default settings will convert the character cards in the currect folder into both JSON and YAML format into the currect folder.

The Tavern cards need to be in the format *tavern.png and V2 cards in the format *spec_v2.png.

Install the package using python pipenv
>pip install pipenv

>pipenv install

>pipenv run python .\character_card_converter.py

or
>pipenv run python .\character_card_converter.py --type <type> --source <source dir> --target <target dir>

>_--type_
Conversion type

Possible values: JSON,YAML,JSON&YAML

Default: JSON&YAML

>_--source_
Source of the character cards

Default: current dir('.')

>_--target_
Where to save the character cards

Default: current dir('.')