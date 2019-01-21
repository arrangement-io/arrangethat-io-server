import StringIO
import csv
from flask import make_response, jsonify


def to_csv(arrangements):
    si = StringIO.StringIO()
    cw = csv.writer(si)

    cw.writerow(arrangements.keys())
    cw.writerow(arrangements.values())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=arrangements.csv"
    output.headers["Content-type"] = "text/csv"
    return output


def to_tsv(arrangements):
    si = StringIO.StringIO()
    cw = csv.writer(si, delimiter='\t')

    cw.writerow(arrangements.keys())
    cw.writerow(arrangements.values())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=arrangements.tsv"
    output.headers["Content-type"] = "text/csv"
    return output


class Export:

    def get_arrangements(self, export_type, arrangements):

        if len(arrangements) == 1:
            if export_type == "csv":
                return to_csv(arrangements[0])
            elif export_type == "tsv":
                return to_tsv(arrangements[0])
            elif export_type == "json":
                return jsonify({"arrangement": arrangements[0]})
            else:
                return jsonify({"error": "Please provide a valid export type"})
        else:
            return jsonify({"arrangement": "no arrangement found"})
