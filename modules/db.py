import os
import json
import ollama
import chromadb
import pyperclip
from typing import List

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
        ids = [abs(hash(doc)) for doc in docs]
        # and add to collection
        self.collection.add(ids=ids, documents=docs, embeddings=embeddings)
        print("Added successfully!")

    def add_document_from_clipboard (self):
        # get the clipboard content and make the embedding
        embedding = self._generate_embedding(pyperclip.paste())
        # generate the id
        doc_id = abs(hash(pyperclip.paste()))
        # and add it to collection
        self.collection.add(ids=[doc_id], documents=[pyperclip.paste()], embeddings=[embedding])
        print("Added successfully!")

    def query(self, query_text: str, n_results: int = 5):
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