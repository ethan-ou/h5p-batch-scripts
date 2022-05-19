import zipfile
import json
from functools import reduce
import operator
from pathlib import Path

PATH = "mock"
CONTENT_FILE = "content/content.json"
KEY = "autoplay"
FILTER = ''
# Set to "single" for setting a single value
# Set to "batch" to dynamically set values
TYPE = "single"
SINGLE_VALUE = True
BATCH_LOOKUP = ''


# Autoplay Videos Settings
# PATH = "mock"
# CONTENT_FILE = "content/content.json"
# KEY = "autoplay"
# FILTER = ''
# # Set to "single" for setting a single value
# # Set to "batch" to dynamically set values
# TYPE = "single"
# SINGLE_VALUE = True
# BATCH_LOOKUP = ''

def main():
    for file in Path(PATH).glob('*.h5p'):
        print(file)
        with zipfile.ZipFile(file) as z:
            content = json.loads(z.read(CONTENT_FILE).decode(encoding="utf-8"))
            lookup = dict_key_lookup(content, KEY, FILTER)
            new_content = content
            if TYPE == "single":
                for key, value in lookup:
                    new_content = setInDict(new_content, key, SINGLE_VALUE)

            if TYPE == "batch":
                pass
            
            print_changes(new_content, lookup)

            # z.writestr(CONTENT_FILE, new_content)


# https://stackoverflow.com/questions/51413998/how-to-find-all-occurrence-of-a-key-in-nested-dict-but-also-keep-track-of-the-o
def dict_key_lookup(_dict, key, filter_str=None, path=[]):
    results = []
    if isinstance(_dict, dict):
        if key in _dict:
            results.append((path+[key], _dict[key]))
        else:
            for k, v in _dict.items():
                results.extend(dict_key_lookup(v, key, path= path+[k]))
    elif isinstance(_dict, list):
        for index, item in enumerate(_dict):
            results.extend(dict_key_lookup(item, key, path= path+[index]))

    if filter_str is not None:
        filtered_results = []
        for item in results:
            _, v = item
            if isinstance(v, str):
                if filter_str in v:
                    filtered_results.append(item)
            else:
                filtered_results.append(item)
        return filtered_results

    return results


# https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
    return dataDict

def print_changes(new_content, lookup):
    for key, value in lookup:
        print(f"{key[-1]}: {value} -> {getFromDict(new_content, key)}")

if __name__ == "__main__":
    main()