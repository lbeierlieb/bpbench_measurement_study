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

for machine in os.listdir("results"):
    print(machine)
    for (variant, vmi_app) in [ ("ept", "drakvuf"), ("ept-fast", "drakvuf"), ("repair", "smartvmi"), ("emul", "smartvmi") ]:
        result_folder = list(filter(lambda entry: entry.endswith(variant), os.listdir("results/" + machine)))
        if len(result_folder) == 1:
            files = list(map(lambda measure: ("results/" + machine + "/" + result_folder[0] + "/" + measure + ".csv", measure), [ "timing_overhead", "exec_bp_only", "exec_page", "read_byte" ]))
            read_files_and_plot_box(files, "plots/individual/" + machine + "_" + vmi_app + "_" + variant + ".pdf", (0, 225), 0.25, (10, 6), 13, 1000, "\u03bcs")
        elif len(result_folder) == 0:
            print("  WARNING: did not find " + variant)
        else:
            print("  ERROR: found " + variant + " multiple times for machine " + machine)
            exit(1)
