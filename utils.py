import os.path
import settings

FOLDER_NAME = "\effects"


# GLOBALS TO ENABLE MY ANTIPATTERNS
effects = {}
fft_out = []


# FOR FILE STORAGE
def save(name, body):
    f = folder()
    if not os.path.isdir(f):
        os.mkdir(f)
    save_file(f, name, body)


def save_file(folder, name, body):
    completeName = os.path.join(folder, name+".json")
    file1 = open(completeName, "w")
    file1.write(body)
    file1.close()
    print("saved " + name)


def load(filename):
    f = folder()
    completeName = os.path.join(f, filename)
    file1 = open(completeName, "r")
    data = file1.read()
    file1.close()
    return data


def list_files():
    (_, _, filenames) = next(os.walk(folder()))
    return filenames


def folder():
    return os.getcwd()+FOLDER_NAME


# FOR AUDIO
def hz_to_index(hz):
    return round(hz/settings.HZ_INDEX_CONSTANT)


def index_to_hz(index):
    return index*settings.HZ_INDEX_CONSTANT
