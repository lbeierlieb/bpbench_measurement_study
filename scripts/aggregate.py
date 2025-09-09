import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import re

def median_and_min(file):
    with open(file, 'r') as f:
        numbers = [float(line.strip()) / 1000 for line in f if line.strip().isdigit()]

    return (np.median(numbers), np.min(numbers))

def find_file(machine, variant, measurement):
    result_folder = list(filter(lambda entry: entry.endswith(variant), os.listdir("results/" + machine)))
    if len(result_folder) == 1:
        return "results/" + machine + "/" + result_folder[0] + "/" + measurement + ".csv"
    elif len(result_folder) == 0:
        print("  WARNING: did not find " + variant)
        return None
    else:
        print("  ERROR: found " + variant + " multiple times for machine " + machine)
        exit(1)

def find_sysbench_score(machine):
    score = None
    pattern = re.compile(r"events per second:\s*([\d.]+)")

    with open("results/" + machine + "/readme.txt") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                score = float(match.group(1))
                break

    return score

print("Aggregating all data")
rows = [ ["machine", "variant", "measurement", "median", "min"] ]
for machine in sorted(os.listdir("results")):
    print(machine)

    sysbench_score = find_sysbench_score(machine)
    if sysbench_score != None:
        rows.append([machine, "-", "sysbench", sysbench_score, sysbench_score])

    data = [
        ("repair",   "timing_overhead"),
        ("repair",   "exec_bp"),
        ("repair",   "exec_page"),
        ("repair",   "read_bp"),
        ("repair",   "read_page"),
        ("emul",     "timing_overhead"),
        ("emul",     "exec_bp"),
        ("emul",     "exec_page"),
        ("emul",     "read_bp"),
        ("emul",     "read_page"),
        ("ept",      "timing_overhead"),
        ("ept",      "exec_bp"),
        ("ept",      "exec_page"),
        ("ept",      "read_bp"),
        ("ept",      "read_page"),
        ("ept-fast", "timing_overhead"),
        ("ept-fast", "exec_bp"),
        ("ept-fast", "exec_page"),
        ("ept-fast", "read_bp"),
        ("ept-fast", "read_page"),
    ]
    for (variant, measurement) in data:
        f = find_file(machine, variant, measurement)
        if f != None:
            (median, mini) = median_and_min(f)
            rows.append([machine, variant, measurement, median, mini])

with open("plots/summary_all.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerows(rows)

print("\nAggregating selected data")
rows = [ ["machine", "metric", "median", "min"] ]
for machine in sorted(os.listdir("results")):
    print(machine)

    data = [
        (0, "emul",     "timing_overhead", "timing_overhead"),
        (1, "repair",   "exec_bp",         "exec_bp_rep"),
        (2, "emul",     "exec_bp",         "exec_bp_emul"),
        (3, "ept",      "exec_bp",         "exec_bp_altp2m"),
        (4, "ept-fast", "exec_bp",         "exec_bp_altp2m_fss"),
        (5, "emul",     "read_bp",         "read_bp_emul"),
        (6, "ept",      "read_bp",         "read_bp_altp2m"),
    ]
    # filter out the machines that do not have a sysbench score
    sysbench_score = find_sysbench_score(machine)
    if sysbench_score == None:
        continue

    rows.append([machine, "sysbench", sysbench_score, sysbench_score])

    # machines that struggled with smartvmi should not include smartvmi measurements
    sysbench_score = find_sysbench_score(machine)
    f = find_file(machine, "emul", "timing_overhead")
    if f == None or median_and_min(f)[1] > 10 or sysbench_score == None:
        no_smartvmi = True
    else:
        no_smartvmi = False

    for (num, variant, measurement, label) in data:
        if no_smartvmi and (variant == "repair" or variant == "emul"):
            continue
        f = find_file(machine, variant, measurement)
        if f != None:
            (median, mini) = median_and_min(f)
            rows.append([machine, label, median, mini])

with open("plots/summary_selected.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerows(rows)
