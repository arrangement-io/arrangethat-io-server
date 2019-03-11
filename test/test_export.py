from __future__ import print_function

from app import *
from export import Export
import json

def mock_arrangement():
    with open("test/arrangement.json") as f:
        return json.loads(f.read())

def test_export_csv():
    with app.app_context():
        csv_export = """Version 1,,,\r
car,Chia Van,Jeff Van,unassigned\r
driver,Gideon,Jeff,\r
passenger,Crystal,Gabe,\r
Version 2,,,\r
car,Chia Van,Jeff Van,unassigned\r
driver,Gideon,,Jeff\r
passenger,Crystal,,Gabe\r\n"""
        print(Export.to_csv(mock_arrangement()))
        assert csv_export == Export.to_csv(mock_arrangement())

def test_export_tsv():
    with app.app_context():
        tsv_export = """Version 1\t\t\t\r
car	Chia Van	Jeff Van	unassigned\r
driver	Gideon	Jeff\t\r
passenger	Crystal	Gabe\t\r
Version 2\t\t\t\r
car	Chia Van	Jeff Van	unassigned\r
driver	Gideon		Jeff\r
passenger	Crystal		Gabe\r\n"""
        print(Export.to_tsv(mock_arrangement()))
        assert tsv_export == Export.to_tsv(mock_arrangement())

