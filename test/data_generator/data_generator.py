# This is the layout of the data
# Arrangement: 
# {id: a_,
#  name: _,
#  # owner: _,
#  # users: [_ids_],
#  items: [_item_objects_],
#  containers: [_container_objects_],
#  is_deleted: _,
#  timestamp: _,
#  snapshots: [_snapshot_objects_]
# }
#
# Snapshot:
# {id: s_,
#  name: _,
#  snapshot: {container1_id: [item1_id, item2_id], container2_id: [item3_id]}
# }
# 
# Item:
# {id: i_,
#  name: _,
#  size: 1,
# }
#
# Container:
# {id: c_,
#  name: _,
#  size: 8
# }
# 

import json
import random
import string
import time

def create_random_id(prepended_letter=""):
  return prepended_letter + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def create_container(name, size):
  return {"id": create_random_id('c'), "name": name, "size": size}

def create_item(name, size=1):
  return {"id": create_random_id('i'), "name": name, "size": size}

def create_snapshot(name):
  return {"id": create_random_id('s'), "name": name, "snapshot": {}}


class Arrangement(object):
  def __init__(self, name):
    self.data = {}
    self.data["name"] = name
    self.data["id"] = create_random_id("a")
    self.data["items"] = []
    self.data["containers"] = []
    self.data["is_deleted"] = False
    self.data["snapshots"] = [create_snapshot("only snapshot")]
    self.data["timestamp"] = time.time()
  
  def add_item(self, name):
    item = create_item(name)
    self.data['items'].append(create_item(name))
    return item

  def add_container(self, name, size):
    container = create_container(name, size)
    self.data['containers'].append(container)
    self.data['snapshots'][0]['snapshot'][container['id']] = [] 

  def get_container(self, name):
    for container in self.data['containers']:
      if container['name'] == name:
        return container

  def add_item_to_container(self, name, container_name):
    item = self.add_item(name)
    container_id = self.get_container(container_name)['id']
    self.data['snapshots'][0]['snapshot'][container_id].append(item['id'])

  def build(self):
    return json.dumps(self.data, sort_keys=True, indent=4)

def main():
  arrangement = Arrangement("first arrangement")
  arrangement.add_container("chia van", 8)
  arrangement.add_container("nathan car", 8)
  arrangement.add_item_to_container('gideon', 'chia van')
  arrangement.add_item_to_container('gideon luggage', 'chia van')
  arrangement.add_item_to_container('jeff', 'chia van')
  arrangement.add_item_to_container('nathan', 'nathan car')
  arrangement.add_item_to_container('moses', 'nathan car')

  print arrangement.build()

if __name__ == "__main__":
  main()

