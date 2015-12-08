from collections import defaultdict
from collections import Counter
import csv
from SymmetricPair import SymmetricPair

""" stores the names of all columns in the final_table"""
col_names = ["id", "fixed", "reopened", "reassignments", "assignee_success", "reporter", "reporter_success", "relationship_count"
    ,"opening_time", "product", "severity", "severity_increased", "severity_decreased", "version"]

"""stores whether features are nominal or numerical"""
feature_types = ['nominal', 'nominal', 'nominal', 'numeric', 'numeric', 'nominal', 'numeric', 'numeric',
                 'numeric', 'nominal', 'nominal', 'nominal', 'nominal', "nominal"]

"""stores the final table. The first key of the dictionary is the bug_id,
   the second is the name of the column
"""
final_table = defaultdict(defaultdict)

"""stores all tables from which we want to extract features"""
tables = defaultdict(list)

"""stores for each bug the ids of the participants (assignees, reporter)"""
bug_participants = defaultdict(list)

"""imports a table from the given filename and stores it in 'tables' under the name 'tablename'"""
def import_table(tablename, filename):
    table = list()
    for line in open(filename, mode='r').readlines():
        row = list()
        for value in line.split(','):
            row.append(value.strip("\n"))
        table.append(row)

    """delete the first row, since it contains the header"""
    table.pop(0)
    tables[tablename] = table

"""extracts for each bug_id, whether the bug was fixed or not and whether it was reopened"""
def extract_status_information():
    """First store the id of all bugs that were fixed"""
    fixed_bugs = dict()
    for row in tables["resolution"]:
        bug_id = row[0]
        if row[1] == "FIXED":
            fixed_bugs[bug_id] = True

    """For all bugs that were tracked in the status table, check if they were fixed or reopened"""
    for row in tables["status"]:
        bug_id = row[0]
        final_table[bug_id]["id"] = bug_id
        "Set whether bug was fixed"
        if bug_id in fixed_bugs.keys():
            final_table[bug_id]["fixed"] = 1
        else:
            final_table[bug_id]["fixed"] = 0

        "Set reopened status"
        status = row[1]
        if status == "REOPENED":
            final_table[bug_id]["reopened"] = 1
        else:
            if "reopened" not in final_table[bug_id].keys():
                final_table[bug_id]["reopened"] = 0


"""extracts for each assignee his success rate. Then for each bug,
   the average success rates of its assignees is calculated"""
def extract_assignee_information():
    assigned = Counter()
    resolved = Counter()
    success_rates = dict()
    bug_assignments = defaultdict(list)

    "Count bug and success count for each assignee. Keep track of the reassignment count"
    for row in tables["assignees"]:
        assignee = str(row[1]).strip(' ')
        bug_id = row[0]
        bug_participants[bug_id].append(assignee)
        assigned[assignee] += 1
        if final_table[bug_id]["fixed"]:
            resolved[assignee] += 1
        bug_assignments[bug_id].append(assignee)

    "Calculate success rate"
    for k, v in assigned.items():
        success_rates[k] = float(resolved[k]) / float(v)

    "Calculate for each bug, the average success rates of all assignees"
    for k, v in final_table.items():
        avg_success = 0.0
        for assignee in bug_assignments[k]:
            avg_success += success_rates[assignee]

        avg_success /= len(bug_assignments[k])
        final_table[k]["assignee_success"] = round(avg_success, 1)

        "Store for each bug its reassignment count"
        final_table[k]["reassignments"] = len(bug_assignments[k]) - 1



"""extracts for each bug its reporter and the reporters success rate"""
def extract_report_information():
    reporter_bug_count = Counter()
    reporter_fixed_bug_count = Counter()
    reporter_success = defaultdict(float)

    for row in tables['reports']:
        bug_id = row[0]
        reporter = row[4]
        bug_participants[bug_id].append(reporter)
        final_table[bug_id]["reporter"] = reporter
        reporter_bug_count[reporter] += 1
        if final_table[bug_id]["fixed"]:
            reporter_fixed_bug_count[reporter] += 1

    for k, v in reporter_bug_count.items():
        reporter_success[k] = float(reporter_fixed_bug_count[k]) / float(reporter_bug_count[k])

    for k, v in final_table.items():
        final_table[k]['reporter_success'] = round(float(reporter_success[final_table[k]['reporter']]), 1)


"""Extracts for each pair of participants how often they worked together in the past"""
def extract_participants_relationship_information():
    participant_count = defaultdict(int)

    for v in bug_participants.values():
        for i in range(len(v) - 1):
            for j in range(i, len(v) - 1):
                if i != j and v[i] != v[j]:
                    key = SymmetricPair(v[i], v[j])
                    participant_count[key] += 1

    for k, v in bug_participants.items():
        relationship_count = 0
        for i in range(len(v) - 1):
            for j in range(i, len(v) - 1):
                if i != j and v[i] != v[j]:
                    key = SymmetricPair(v[i], v[j])
                    relationship_count += participant_count[key]

        final_table[k]['relationship_count'] = round(relationship_count / float(len(v)))

"""Extracts for each row in a table the value and stores it in the final table"""
def extract_nominal_value(table):
    values = []
    """First store all possible values in a list"""
    for row in tables[table]:
        if row[1] not in values:
            values.append(row[1])

    """Store for each value its index"""
    for row in tables[table]:
        values.append(row[1])
        bug_id = row[0]
        value = row[1]
        final_table[bug_id][table] = values.index(value) + 1

"""Extracts the time a bug was open (buggy)"""
def extract_opening_time_information():
    bug_status = defaultdict(defaultdict)

    for row in tables["status"]:
        bug_id = row[0]
        status = row[1]
        time = int(row[2])
        bug_status[bug_id][status] = time

    for bug, v in bug_status.items():
        times = sorted(v.values())
        begin = times[0]
        end = times[len(times) - 1]
        final_table[bug]["opening_time"] = round((end - begin) / (3600 * 24))


def extract_severity_information():
    bug_severities = defaultdict(list)
    ordering = ["trivial", "minor", "enhancement", "normal", "major", "critical", "blocker"]

    for row in tables["severity"]:
        bug_id = row[0]
        severity = row[1]
        bug_severities[bug_id].append(str(severity).lower())

    for k, v in bug_severities.items():
        reference = v[0]
        final_table[k]["severity"] = ordering.index(reference)
        final_table[k]["severity_increased"] = 0
        final_table[k]["severity_decreased"] = 0
        for i in range(1, len(v) - 1):
            if ordering.index(v[i]) > ordering.index(reference):
                final_table[k]["severity_increased"] = 1
            elif ordering.index(v[i]) < ordering.index(reference):
                final_table[k]["severity_decreased"] = 1


"""Returns the final table in a merged list format"""
def get_final_table():
    table = []
    table.append(col_names)
    table.append(feature_types)
    for key, value in final_table.items():
        print(value)
        row = []
        for k in col_names:
            row.append(value[k])
        table.append(row)

    return table

"""exports table to .csv file"""
def export_table(filename, table):
    with open(filename, "w+") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(table)


import_table("resolution", "tables/resolution.csv")
import_table("status", "tables/bug_status.csv")
import_table("assignees", "tables/assigned_to.csv")
import_table("reports", "tables/reports.csv")
import_table("version", "tables/version.csv")
import_table("severity", "tables/severity.csv")
import_table("priority", "tables/priority.csv")
import_table("product", "tables/product.csv")

extract_status_information()
extract_assignee_information()
extract_report_information()
extract_participants_relationship_information()
extract_nominal_value("version")
extract_opening_time_information()
extract_nominal_value("product")
extract_severity_information()

table = get_final_table()
export_table("tables/final_table.csv", table)
