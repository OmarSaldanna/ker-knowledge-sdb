import os
import hashlib

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

# function to generate hashes
def hashx (string):
    hash_obj = hashlib.sha256()
    # convert the string to bytes and hash
    hash_obj.update(string.encode('utf-8'))
    # get the hex
    return str(hash_obj.hexdigest())[:32]