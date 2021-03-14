import os
import json

file_name = ''
folder_path = ''

def find_file():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(THIS_FOLDER, 'rmarton_3.6.21.json')
    return file_name

def create_folder():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(THIS_FOLDER, 'rmarton_3.6.21.json')
    folder_name = file_name.replace('.json', '')
    path = os.path.join(THIS_FOLDER, folder_name)
    os.mkdir(path)
    return path

def read_file_json(file_name):
    with open(file_name) as file:
        data = file.read()
        pretty_json = json.loads(data)
        for i in range(len(pretty_json)):
            temp_file_name = 'data_{}.json'.format(i)
            temp_file_name = os.path.join(folder_path, temp_file_name)
            with open(temp_file_name, 'w') as f:
                json.dump(pretty_json[i], f)
        
file_name = find_file()

folder_path = create_folder()
read_file_json(file_name)

