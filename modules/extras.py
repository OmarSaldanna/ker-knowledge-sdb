import os

def which_sdb ():
    try:
        with open(os.environ["FLAG_SDB_NAME"], 'r') as f:
            content = f.read()
        return content.strip()
    except:
        return ""

def move_to_sdb (name):
    with open(os.environ["FLAG_SDB_NAME"], 'w') as f:
        f.write(name)