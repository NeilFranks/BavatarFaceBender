import os.path

FOLDER_NAME = "\effects"


def save(name, body):
    folder = os.getcwd()+FOLDER_NAME
    if not os.path.isdir(folder):
        os.mkdir(folder)
    save_file(folder, name, body)


def save_file(folder, name, body):
    completeName = os.path.join(folder, name+".json")         
    file1 = open(completeName, "w")
    file1.write(body)
    file1.close()
