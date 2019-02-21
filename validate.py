class Validate(object):
    """Given an arrangement, validate that it is a valid arrangement"""

    @staticmethod
    def validate_payload(payload):
        try:
            assert "arrangement" in payload
            assert Validate.validate_arrangment(payload["arrangement"])
        except AssertionError:
            return False
        return True

    @staticmethod
    def validate_arrangment(arrangement):
        try:
            assert "_id" in arrangement
            assert "containers" in arrangement
            assert Validate.validate_containers(arrangement['containers'])
            assert "is_deleted" in arrangement
            assert "items" in arrangement
            assert Validate.validate_items(arrangement['items'])
            assert "modified_timestamp" in arrangement
            assert "name" in arrangement
            assert "snapshots" in arrangement
            assert Validate.validate_snapshots(arrangement['snapshots'])
            assert "timestamp" in arrangement
            assert "owner" in arrangement
            assert "users" in arrangement
        except AssertionError:
            return False
        return True

    @staticmethod
    def validate_containers(containers):
        try:
            for container in containers:
                assert "_id" in container
                assert container["_id"][0] == "c"
                assert "name" in container
                assert "size" in container
        except AssertionError:
            return False
        return True

    @staticmethod
    def validate_items(items):
        try:
            for item in items:
                assert "_id" in item
                assert item["_id"][0] == "i"
                assert "name" in item
                assert "size" in item
        except AssertionError:
            return False
        return True

    @staticmethod
    def validate_snapshots(snapshots):
        try:
            for snapshot in snapshots:
                assert "_id" in snapshot
                assert snapshot["_id"][0] == "s"
                assert "name" in snapshot
                assert "snapshot" in snapshot
                assert "unassigned" in snapshot
        except AssertionError:
            return False
        return True