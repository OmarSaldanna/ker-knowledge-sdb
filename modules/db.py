import os
import json
import ollama
import hashlib
import chromadb
from typing import List

from modules.extras import hashx

# collection
#  |--- config.json
#  |--- assets/
#         |---- every file added ...

class SDB:
    def __init__ (self, name: str):
        # check if the db exists
        availables = os.listdir(os.environ["COLLECTIONS_PATH"])
        if name not in availables:
            raise ValueError(f"SDB \"{name}\" doesn't exist")
        # if not
        # instance the db on its path
        self.client = chromadb.PersistentClient(path=os.environ["COLLECTIONS_PATH"] + name)
        self.collection = self.client.get_or_create_collection(name=name)
        # also load the config and the db dir
        self.dir = os.environ["COLLECTIONS_PATH"] + name + "/"
        with open(self.dir + "config.json", 'r') as f:
            self.config = json.load(f)

    def _generate_embedding (self, text: str) -> List[float]:
        # use the preset model with ollama to make the embeddings
        response = ollama.embeddings(model=self.config["embedding"], prompt=text)
        return response['embedding']

    def add_documents (self, docs: List[str]):
        # for every "text" on the docs, generate an embedding
        embeddings = [self._generate_embedding(doc) for doc in docs]
        # now generate ids
        ids = [str(hashx(doc)) for doc in docs]
        # check if any of the documents already exist
        exist_any = self.collection.get(ids=ids[0])['documents']
        if exist_any:
            print('\033[93m' + ">>> coincidence on SDB, skipping..." + '\033[0m\n')
            return 0
        else:
            # and add to collection
            self.collection.add(ids=ids, documents=docs, embeddings=embeddings)
            return len(ids)

    def query(self, query_text: str, n_results: int):
        # make a query to the db
        query_embedding = self._generate_embedding(query_text)
        # fetch results from the db
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        # and return
        return results['documents'][0] if 'documents' in results else []


# function to create db
def new_sdb (name: str):
    # try to create the db dir
    try:
        os.mkdir(os.environ["COLLECTIONS_PATH"] + name)
    # if it already exists
    except FileExistsError:
        print('\033[91m' + f"Error creating SDB: {name} already exists" + '\033[0m')
        return
    # then
    # also make the assets dir
    os.mkdir(os.environ["COLLECTIONS_PATH"] + name + "/assets")
    # load db prototype
    with open(os.environ["PROTOTYPE_PATH"], 'r') as f:
        prototype = json.load(f)
    # config the prototype
    prototype['name'] = name
    prototype['description'] = input(">>> SDB description (or leave blank): ")
    # and write the config.json
    with open(os.environ["COLLECTIONS_PATH"] + name + "/config.json", 'w') as write_file:
        json.dump(prototype, write_file, indent=int(4), ensure_ascii=False)
    # final notes
    print(f"SDB \"{name}\" created on " + '\033[92m' + f"{os.environ["COLLECTIONS_PATH"] + name}" + '\033[0m')
    print("to modify your SDB presets type: " + '\033[92m' + f"ker set {name}" + '\033[0m')

# https://ollama.com/blog/embedding-models
# https://chatgpt.com/share/67a8059a-0bcc-8008-9417-f96ce53298b5