# This is the layout of the data
# Arrangement:
# {_id: a,
#  name: _,
#  # owner: owner_id #[google_id],  <--- change this from user_id to google_id, 
#  # users: user_id  #[google_id],   <--- change this from user_id to google_id
#  items: [_item_objects_],
#  containers: [_container_objects_],
#  is_deleted: _,
#  timestamp: _,
#  snapshots: [_snapshot_objects_]
# }
#
# Snapshot:
# {_id: s,
#  name: _,
#  snapshot: {container1_id: [item1_id, item2_id], container2_id: [item3_id]},
#  unassigned: [item4_id, item5_id, ...]  # <- this is the change
# }
#
# Item:
# {_id: i,
#  name: _,
#  size: 1,
# }
#
# Container:
# {_id: c,
#  name: _,
#  size: 8
# }

import json
import random
import string
import time


def create_container(container_id, name, size):
    return {"_id": container_id, "name": name, "size": size}


def create_item(item_id, name, size):
    return {"_id": item_id, "name": name, "size": size}


def create_snapshot(snapshot_id, name, snapshot_unassigned):
    return {"_id": snapshot_id, "name": name, "snapshot": {}, "unassigned": snapshot_unassigned}


class Arrangement:
    data = {}

    def pass_json(self, arrangement):
        self.data["name"] = arrangement['name']
        self.data["_id"] = arrangement['_id']
        self.data["owner_id"] = arrangement['owner_id']
        self.data["user_id"] = arrangement['user_id']
        self.data["items"] = []
        self.data["containers"] = []
        self.data["is_deleted"] = arrangement['is_deleted']
        self.data["timestamp"] = arrangement['timestamp']
        self.data["modified_timestamp"] = arrangement['modified_timestamp']
        containers = arrangement['containers']
        for container in containers:
            container_id = container['_id']
            container_name = container['name']
            container_size = container['size']
            self.add_container(container_id, container_name, container_size)
        items = arrangement['items']
        for item in items:
            item_id = item['_id']
            item_name = item['name']
            item_size = item['size']
            self.add_item(item_id, item_name, item_size)
        snapshots_data = arrangement['snapshots']
        for snapshot in snapshots_data:
            snapshot_id = snapshot['_id']
            snapshot_name = snapshot['name']
            snapshot_snapshots = snapshot['snapshot']
            snapshot_unassigned = snapshot['unassigned']
            self.data["snapshots"] = [create_snapshot(snapshot_id, snapshot_name, snapshot_unassigned)]
            data1 = {}
            for key, value in snapshot_snapshots.items():
                data1[key] = value
                self.data['snapshots'][0]['snapshot'][key] = value

    def add_item(self, item_id, name, size):
        item = create_item(item_id, name, size)
        self.data['items'].append(item)

    def add_container(self, container_id, name, size):
        container = create_container(container_id, name, size)
        self.data['containers'].append(container)

    def build(self):
        return self.data

