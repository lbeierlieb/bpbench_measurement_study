import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def read_files_and_plot_box(files, plot_filename, ylimit, textoffset, figsize, fontsize, scaling, unit):
    data = []
    labels = []

    for filename, label in files:
        with open(filename, 'r') as f:
            numbers = [float(line.strip()) / scaling for line in f if line.strip().isdigit()]
            if numbers:
                data.append(numbers)
                labels.append(label)
            else:
                print(f"No valid numbers found in {filename}")

    plt.rcParams.update({'font.size': fontsize})
    plt.figure(figsize=figsize)
    plt.boxplot(data, tick_labels=labels)
    for i, dataset in enumerate(data, 1):
        median = np.median(dataset)
        plt.text(i+textoffset, median, f'{median:.2f} {unit}', horizontalalignment='left', verticalalignment='center', color='black')
    plt.ylim(ylimit)
    plt.xticks(rotation=45)
    plt.xlabel('Workload')
    plt.ylabel(f'Latency [{unit}]')
    plt.savefig(plot_filename, format="pdf")
    plt.close()

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

for machine in os.listdir("results"):
    print(machine)
    data = [
        ("ept", "timing_overhead", "drakvuf timer"),
        ("emul", "timing_overhead", "smartvmi timer"),
        ("ept", "exec_bp_only", "ept exec"),
        ("ept", "read_byte", "ept read"),
        ("ept-fast", "exec_bp_only", "ept-fast exec"),
        ("ept-fast", "read_byte", "ept-fast read"),
        ("repair", "exec_bp_only", "repair exec"),
        ("repair", "read_byte", "repair read"),
        ("emul", "exec_bp_only", "emul exec"),
        ("emul", "read_byte", "emul read"),
    ]
    files = []
    for (variant, measurement, label) in data:
        f = find_file(machine, variant, measurement)
        if f != None:
            files.append((f, label))

    read_files_and_plot_box(files, "plots/machines/" + machine + ".pdf", (0, 225), 0.1, (12, 6), 13, 1000, "\u03bcs")
