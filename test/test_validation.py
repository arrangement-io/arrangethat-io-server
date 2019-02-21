from app import *
from validate import Validate

def mock_arrangement():
    return {
        "arrangement": {
            "_id": "EPQPQmmmm",
            "containers": [
                {
                    "_id": "c6440J009",
                    "name": "chia van",
                    "size": 8
                },
                {
                    "_id": "cB3GGD1Y7",
                    "name": "nathan car",
                    "size": 8
                }
            ],
            "is_deleted": False,
            "items": [
                {
                    "_id": "iIGUFNXE3",
                    "name": "gideon",
                    "size": 1
                },
                {
                    "_id": "iOSOI9CIS",
                    "name": "gideon luggage",
                    "size": 1
                },
                {
                    "_id": "iS9VCNY3P",
                    "name": "jeff",
                    "size": 1
                },
                {
                    "_id": "i0SIZA58U",
                    "name": "nathan",
                    "size": 1
                },
                {
                    "_id": "i4JVG98T0",
                    "name": "moses",
                    "size": 1
                },
                {
                    "_id": "i1KVG98T0",
                    "name": "jon",
                    "size": 1
                }
            ],
            "modified_timestamp": "177742014.00000",
            "name": "first arrangement",
            "snapshots": [
                {
                    "_id": "s2OOMJ0HF",
                    "name": "only snapshot",
                    "snapshot": {
                        "c6440J009": [
                            "i0SIZA58U",
                            "iOSOI9CIS",
                            "i4JVG98T0"
                        ],
                        "cB3GGD1Y7": [
                            "iIGUFNXE3",
                            "iS9VCNY3P"
                        ]
                    },
                    "unassigned": [
                        "i1KVG98T0"
                    ]
                }
            ],
            "timestamp": "1538842014.061443"
        }
    }

def mock_bad_arrangement():
    return {
        "arrangement": {
            "_id": "EPQPQmmmm",
            "is_deleted": False,
            "items": [
                {
                    "_id": "iIGUFNXE3",
                    "name": "gideon",
                    "size": 1
                },
                {
                    "_id": "iOSOI9CIS",
                    "name": "gideon luggage",
                    "size": 1
                },
                {
                    "_id": "iS9VCNY3P",
                    "name": "jeff",
                    "size": 1
                },
                {
                    "_id": "i0SIZA58U",
                    "name": "nathan",
                    "size": 1
                },
                {
                    "_id": "i4JVG98T0",
                    "name": "moses",
                    "size": 1
                },
                {
                    "_id": "i1KVG98T0",
                    "name": "jon",
                    "size": 1
                }
            ],
            "modified_timestamp": "177742014.00000",
            "name": "first arrangement",
            "snapshots": [
                {
                    "_id": "s2OOMJ0HF",
                    "name": "only snapshot",
                    "snapshot": {
                        "c6440J009": [
                            "i0SIZA58U",
                            "iOSOI9CIS",
                            "i4JVG98T0"
                        ],
                        "cB3GGD1Y7": [
                            "iIGUFNXE3",
                            "iS9VCNY3P"
                        ]
                    },
                    "unassigned": [
                        "i1KVG98T0"
                    ]
                }
            ],
            "timestamp": "1538842014.061443"
        }
    }

def mock_arrangement_owner():
    return {
        "arrangement": {
            "_id": "aQY6RP4J3",
            "containers": [
                {
                    "_id": "cBQSPDH7W",
                    "name": "Gideon's Van",
                    "size": 8
                }
            ],
            "is_deleted": False,
            "items": [
                {
                    "_id": "i2QIBHIUY",
                    "name": "Gideon",
                    "size": 1
                },
                {
                    "_id": "i3CDAPZQJ",
                    "name": "alan",
                    "size": 1
                },
                {
                    "_id": "iF51F9MBY",
                    "name": "Alan",
                    "size": 1
                }
            ],
            "modified_timestamp": 1550637564.537,
            "name": "Gideon's 2nd arrangement",
            "owner": "116550101409368732312",
            "snapshots": [
                {
                    "_id": "sHQMS220B",
                    "name": "blah",
                    "snapshot": {
                        "cBQSPDH7W": [
                            "i2QIBHIUY",
                            "i3CDAPZQJ"
                        ]
                    },
                    "unassigned": [
                        "iF51F9MBY"
                    ]
                }
            ],
            "timestamp": 1550632395.346,
            "user": "116550101409368732312",
            "users": [
                "116550101409368732312"
            ]
        }
    }

def test_validate_arrangement():
    with app.app_context():
        assert Validate.validate_payload(mock_arrangement())

def test_not_valid_arrangement():
    with app.app_context():
        assert Validate.validate_payload(mock_bad_arrangement()) == False

def test_validate_arrangement_owner():
    with app.app_context():
        assert Validate.validate_payload(mock_arrangement_owner())
