from __future__ import print_function

import csv
from io import StringIO

import six

from flask import jsonify, make_response


class Export:
    """Given an arrangement, render the arrangement in a spreadsheet matrix."""
    @staticmethod
    def render_arrangement(arrangement):
        render = []
        for snapshot in arrangement["snapshots"]:
            snapshot_render = Export.render_snapshot(snapshot, arrangement["containers"], arrangement["items"])
            # Transpose the render
            render.extend(map(list, six.moves.zip_longest(*snapshot_render, fillvalue="")))

        return render

    """Given a snapshot and list of containers and items, render a single snapshot in a spreadsheet matrix."""
    @staticmethod
    def render_snapshot(snapshot, containers, items):
        # will render a nxm array of name and transpose it
        output = []
        sider = [snapshot["name"], "car", "driver", "passenger"]
        output.append(sider)
        for container in snapshot["snapshotContainers"]:
            container_and_items = ["", Export.retrieve_name(container["_id"], containers)]
            for item in container["items"]:
                container_and_items.append(Export.retrieve_name(item, items))
            output.append(container_and_items)
        unassigned_items = ["", "unassigned"]
        for item in snapshot["unassigned"]:
            unassigned_items.append(Export.retrieve_name(item, items))
        output.append(unassigned_items)

        return output

    """Helper method to retrieve the name of an object, given the id."""
    @staticmethod
    def retrieve_name(object_id, list_of_objects):
        for obj in list_of_objects:
            if obj["_id"] == object_id:
                return obj["name"]

    """Outputs the arrangement as a csv in a spreadsheet matrix."""
    @staticmethod
    def to_csv(arrangement):
        matrix = Export.render_arrangement(arrangement)

        si = StringIO.StringIO()
        cw = csv.writer(si)
        for line in matrix:
            cw.writerow(line)
        return si.getvalue()

    """Outputs the arrangement as a tsv in a spreadsheet matrix."""
    @staticmethod
    def to_tsv(arrangement):
        matrix = Export.render_arrangement(arrangement)

        si = StringIO.StringIO()
        cw = csv.writer(si, delimiter='\t')
        for line in matrix:
            cw.writerow(line)
        return si.getvalue()

    @staticmethod
    def export_arrangement(export_type, arrangement):
        if export_type == "csv":
            return Export.to_csv(arrangement)
        elif export_type == "tsv":
            return Export.to_tsv(arrangement)
        elif export_type == "json":
            return jsonify({"arrangement": arrangement})
        else:
            return jsonify({"error": "Please provide a valid export type"})
