import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def read_files_and_plot_box(files, plotFilename, xLimit, yLimit, textOffset, figsize, fontsize, scaling, unit):
    data = []
    labels = []
    groups = []
    machine = ""

    for system, filename, group, label in files:
        machine = system
        labels.append(label)
        groups.append(group)
        if filename != None: 
            with open(filename, 'r') as f:
                numbers = [float(line.strip()) / scaling for line in f if line.strip().isdigit()]
                if numbers:
                    data.append(numbers)
                else:
                    print(f"No valid numbers found in {filename}")
        else:
            data.append([0])

    figure, plot = plt.subplots(figsize=figsize)

    # create box plot
    plot.boxplot(data, patch_artist=False)

    # insert median values
    for i, dataset in enumerate(data):
        median = np.median(dataset)
        min    = np.min(dataset)
        if median > 0:
            plot.text(x                   = i + 1  + textOffset[0], 
                      y                   = median + textOffset[1], 
                      s                   = f'{median:.2f} {unit}\n({min:.2f} {unit})', 
                      horizontalalignment = 'left', 
                      verticalalignment   = 'center', 
                      color               = 'black',
                      bbox                = dict(facecolor='white', alpha=1))

    plot.set_title(f'Aggregated Results for Machine {machine}', fontsize=fontsize)
    
    plot.set_xlabel(None)
    plot.set_ylabel(f'Latency [{unit}]', fontsize=fontsize)

    plot.set_xlim(xLimit)
    plot.set_ylim(yLimit)

    xAxisMain = plot.get_xaxis()
    xAxisMain.set_ticks([1,2,3,4,5,6,7,8])
    xAxisMain.set_ticklabels(labels=labels, fontsize=fontsize, rotation=45, ha='center')
    xAxisMain.set_tick_params(length=10, pad=-8)
    
    xAxisGroup = plot.secondary_xaxis(location=0).get_xaxis()
    xAxisGroup.set_ticks([1.5, 4.5, 7.5])
    xAxisGroup.set_ticklabels(labels=['timer latency', 'WL1: execute breakpoint', 'WL3: read at breakpoint location'], fontsize=fontsize)
    xAxisGroup.set_tick_params(length=0, pad=80)

    xAxisGroupSplitter = plot.secondary_xaxis(location=0)
    xAxisGroupSplitter.set_xticks([0.5, 2.5, 6.5, 8.5], labels=[])
    xAxisGroupSplitter.tick_params(length=100, width=1.5)

    yAxisMain = plot.get_yaxis()
    yAxisMain.set_tick_params(labelsize=fontsize)

    figure.subplots_adjust(top=0.95, bottom=0.25, left=0.05, right=0.95)

    figure.savefig(plotFilename, format="pdf")

    plt.close("all")

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
        ("emul",     "timing_overhead", "smartvmi timer"),
        ("ept",      "timing_overhead", "drakvuf timer"),

        ("repair",   "exec_bp",         "exec_bp_rep"),
        ("emul",     "exec_bp",         "exec_bp_emul"),
        ("ept",      "exec_bp",         "exec_bp_altp2m"),
        ("ept-fast", "exec_bp",         "exec_bp_altp2m_fss"),
        
        ("emul",     "read_bp",         "read_bp_emul"),
        ("ept-fast", "read_bp",         "read_bp_altp2m"),
    ]
    files = []
    for (variant, measurement, label) in data:
        filename = find_file(machine, variant, measurement)
        #if f != None:
        files.append((machine, filename, measurement, label))

    read_files_and_plot_box(files        = files, 
                            plotFilename = "plots/machines/" + machine + ".pdf", 
                            xLimit       = (0.5, 8.5),
                            yLimit       = (0, 225), 
                            textOffset   = (0.3, 0),
                            figsize      = (12, 6), 
                            fontsize     = 10, 
                            scaling      = 1000, 
                            unit         = "\u03bcs")
