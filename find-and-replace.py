import zipfile
import json
from functools import reduce
import operator

H5P_FILE = "mock/interactive-book-15123.h5p"
CONTENT_FILE = "content/content.json"


def main():
    with zipfile.ZipFile(H5P_FILE) as z:
        content = json.loads(z.read(CONTENT_FILE).decode(encoding="utf-8"))
        lookup = filter_lookup_values(dict_key_lookup(content, 'path'), 'https://youtu.be')
        content = setInDict(content, lookup[0][0], '')
        lookup1 = dict_key_lookup(content, 'path')
        print(lookup1)

def filter_lookup_values(lookup, string):
    results = []
    for item in lookup:
        _, v = item
        if string in v:
            results.append(item)

    return results

# https://stackoverflow.com/questions/51413998/how-to-find-all-occurrence-of-a-key-in-nested-dict-but-also-keep-track-of-the-o
def dict_key_lookup(_dict, key, path=[]):
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
    return results


# https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
    return dataDict

if __name__ == "__main__":
    main()