import json
import os
import pickle

class Repository:    
    def get_index(self):
        if os.path.exists('database/index.dbx'):
            with open("database/index.dbx", "rb") as f:
                return pickle.load(f)
        else:
            return {}

    def set_data(self, data):
        self.user_id = data['user_id']
        self.data = data
        self.file_id = int(self.user_id[-1])
        self.filename = f"database/data_{self.file_id}.db"
        
    def save_data(self, partitions):
        if self.user_id in partitions:
            return 0
        try:
            file_position = os.path.getsize(self.filename)
        except FileNotFoundError:
            file_position = 0
        with open(self.filename, "ab") as f:
            pickle.dump(self.data, f)
            data_position = f.tell()
        partitions[self.user_id] = {"filename": self.filename, "position": file_position, "size": data_position - file_position}
        return 1

    def save_index(self, partitions):
        with open('database/index.dbx', 'wb') as f:
            pickle.dump(partitions, f)

    def read_data(self, user_id, partitions):
        if user_id not in partitions:
            return None
        else:
            print(partitions[user_id])
        filename = partitions[user_id]['filename']
        position = partitions[user_id]["position"]
        with open(filename, "rb") as f:
            f.seek(position)
            data = pickle.load(f)
        return data
    
    def regenerate_index(self, partitions):
        partitions.clear()
        for filename in os.listdir('database'):
            print(filename)
            if filename.startswith("data_") and filename.endswith(".db"):
                partition_id = int(filename.split("_")[1].split(".")[0])
                with open('database/'+filename, "rb") as f:
                    while True:
                        try:
                            data = pickle.load(f)
                            user_id = data["user_id"]
                            file_position = f.tell() - len(pickle.dumps(data))
                            partitions[user_id] = {"filename": filename, "position": file_position, "size": len(pickle.dumps(data))}
                        except EOFError:
                            break
        with open('database/index.dbx', 'wb') as f:
            pickle.dump(partitions, f)




partitions = {}

repos = Repository()
#repos.regenerate_index(partitions)
#partitions = repos.get_index()
#print(partitions)


for i in range(0,1000):
    user_id = 'clave' + str(i)
    data = {'user_id': user_id, 'name': 'Juan perez cando', 'age': 30}
    
    repos.set_data(data)
    r = repos.save_data(partitions)
    print('Procesado {0} insertado {1}'.format(i,r))


Repository().save_index(partitions)    
#clave9878
#clave9193

print(repos.read_data('clave8738', partitions))
print(repos.read_data('clave190', partitions))
print(repos.read_data('clave115', partitions))
#print(partitions)