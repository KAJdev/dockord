import pymongo
import os

client = pymongo.MongoClient(os.environ.get('DOCKORD_MONGO'))
db = client['prod']
users = db['users']

def encode_key(key):
    return key.replace("\\", "\\\\").replace("$", "\\u0024").replace(".", "\\u002e")

def decode_key(key):
    return key.replace("\\u002e", ".").replace("\\u0024", "\$").replace("\\\\", "\\")

class Session():

    def __init__(self, id=None):
        super().__init__()
        r = users.find_one({'id': id})
        if r is None:
            r = {
                'id': id,
                'current_path': '/',
                'filesystem': {'Desktop': {}, 'Documents': {}, 'hello\\u002etxt': "Welcome to dockord!"}
            }
            users.insert_one(r)
        for key, value in r.items():
            setattr(self, key, value)

    def get_file_from_path(self, path):
        split_path = (self.current_path + path).split('/')
        current_place = self.filesystem
        for p in split_path:
            p = encode_key(p)
            x = current_place.get(p, None)
            if x is not None:
                if not isinstance(x, dict):
                    return x
                else:
                    current_place = x
            else:
                return None
    
    def get_dir_from_path(self, path):
        if new_path.startswith("/"):
            split_path = path.split('/')
        else:
            split_path = (self.current_path + path).split("/")
        current_place = self.filesystem
        for p in split_path:
            p = encode_key(p)
            next = current_place.get(p, None)
            if next is not None:
                if isinstance(next, dict):
                    current_place = next
                    if split_path.index(p) == len(split_path) - 1:
                        return next
                    continue
                return False

    def refresh(self):
        self.__init__(self.id)

    def update(self, update):
        r = users.update_one({'id': self.id}, update)
        self.__init__(self.id)
        return r

    def delete(self):
        r = user.delete_one({'id': self.id})
        return r
    
    def delete_file(self, path):
        self.refresh()
        x = self.get_file_from_path(path)
        if x is not None:
            del x
            self.update({'$set': {'filesystem': self.filesystem}})
            return True
        else:
            return False

    def save_file(self, path, content):
        self.refresh()
        split_path = (self.current_path + path).split('/')
        current_place = self.filesystem
        for p in split_path:
            p = encode_key(p)
            next = current_place.get(p, None)
            if next is not None:
                if isinstance(next, dict):
                    current_place = next
                    continue
                return False
            if split_path.index(p) == len(split_path) - 1:
                current_place[p] = content
                self.update({'$set': {'filesystem': self.filesystem}})
                return True

    def read_file(self, path):
        self.refresh()
        return self.get_file_from_path(path)

    def change_directory(self, new_path):
        self.refresh()
        if self.get_dir_from_path(new_path):
            self.update({'$set': {'current_path': new_path}})
            return True
        return False