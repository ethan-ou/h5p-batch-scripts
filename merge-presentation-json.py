import zipfile
import json
from pathlib import Path

H5P_FILES = ["course-presentation-14853.h5p", "course-presentation-14863.h5p"]
FOLDER = "mock"
CONTENT_FILE = "content/content.json"
H5P_SETTINGS = "h5p.json"

def main():
    output = None

    for file in H5P_FILES:
        file_path = Path(FOLDER, file)
        with zipfile.ZipFile(file_path) as z:
            content = json.loads(z.read(CONTENT_FILE).decode(encoding="utf-8"))
            settings = json.loads(z.read(H5P_SETTINGS).decode(encoding="utf-8"))
            print(settings['title'])
            if output is None:
                output = content
            else:
                if output.get('presentation') is not None:
                    output['presentation']['slides'].extend(content['presentation']['slides'])
                else:
                    print(f"{file} is not a presentation!")

    with open(Path(FOLDER, 'content.json'), 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    main()