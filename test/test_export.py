from app import *
from export import Export
import json

def mock_arrangement():
    with open("arrangement.json") as f:
        return json.loads(f.read())

def test_export_csv():
    with app.app_context():
        csv_export = """only snapshot,,\r\ncar,nathan car,gideon car\r\ndriver,gideon,nathan\r\npassenger,jeff,gideon luggage\r\n,,moses\r\n"""
        assert csv_export == Export.to_csv(mock_arrangement())

def test_export_tsv():
    with app.app_context():
        tsv_export = """only snapshot\t\t\r
car	nathan car	gideon car\r
driver	gideon	nathan\r
passenger	jeff	gideon luggage\r
		moses\r\n"""
        print Export.to_tsv(mock_arrangement())
        assert tsv_export == Export.to_tsv(mock_arrangement())

