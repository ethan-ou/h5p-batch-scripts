import zipfile
import json
from pathlib import Path
# from pathvalidate import sanitize_filename

PATH = 'mock'
SETTINGS_FILE = 'h5p.json'
PRE_FILENAME = ''
POST_FILENAME = '' # Add subtitle name here

def main():
    for file in Path(PATH).glob('*.h5p'):
        with zipfile.ZipFile(file) as z:
            settings = json.loads(z.read(SETTINGS_FILE).decode(encoding="utf-8"))
            name = settings['title']

            # Optional Sanitize
            # name = sanitize_filename(name)
        file.rename(f'{PATH}/{name}.h5p')

if __name__ == "__main__":
    main()