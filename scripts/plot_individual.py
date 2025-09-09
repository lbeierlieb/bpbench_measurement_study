import matplotlib.pyplot as plt
import numpy as np
import os

def read_files_and_plot_box(files, plotFilename, limits, textOffset, figureSize, fontSize, scaling, unit):
    data = []
    labels = []
    variant = ""
    machine = ""

    for filename, label, bpVariant, system in files:
        with open(filename, 'r') as f:
            numbers = [float(line.strip()) / scaling for line in f if line.strip().isdigit()]
            if numbers:
                data.append(numbers)
                labels.append(label)
                variant = bpVariant
                machine = system
            else:
                print(f"No valid numbers found in {filename}")

    figure, plot = plt.subplots(figsize=figureSize)

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

    plot.set_title(f'Results for method {variant} on machine {machine}', fontsize=fontSize)

    plot.set_xlim(limits[0])
    plot.set_ylim(limits[1])
    
    plot.set_xlabel(None)
    plot.set_ylabel(f'Latency [{unit}]', fontsize=fontSize)

    xAxisMain = plot.get_xaxis()
    xAxisMain.set_ticks([1,2,3,4])
    xAxisMain.set_ticklabels(labels=labels, fontsize=fontSize, rotation=0, ha='center')
    xAxisMain.set_tick_params(length=5, pad=5)

    xAxisGroup = plot.secondary_xaxis(location=0).get_xaxis()
    xAxisGroup.set_ticks([1, 2.5, 4])
    xAxisGroup.set_ticklabels(labels=['', 'execute breakpoint', 'read at\nbreakpoint location'], fontsize=fontSize)
    xAxisGroup.set_tick_params(length=0, pad=27)

    xAxisGroupSplitter = plot.secondary_xaxis(location=0)
    xAxisGroupSplitter.set_xticks([0.5, 1.5, 3.5, 4.5], labels=[])
    xAxisGroupSplitter.tick_params(length=50, width=1.5)

    yAxisMain = plot.get_yaxis()
    yAxisMain.set_tick_params(labelsize=fontSize)

    figure.subplots_adjust(top=0.95, bottom=0.12, left=0.06, right=0.97)

    figure.savefig(plotFilename, format="pdf")
    
    plt.close("all")

data = [
    ("ept",      "drakvuf",  "altp2m"), 
    ("ept-fast", "drakvuf",  "altp2m_fss"), 
    ("repair",   "smartvmi", "instr_repair"), 
    ("emul",     "smartvmi", "instr_emulation")
]

filenameMarker = [ "timing_overhead", "exec_bp", "exec_page", "read_bp" ]
labels = [ "timer latency", "WL1: exec_bp", "WL2: exec_page", "WL3: read_bp" ]

for machine in os.listdir("results"):
    print(machine)
    for (variant, vmi_app, label) in data:
        result_folder = list(filter(lambda entry: entry.endswith(variant), os.listdir("results/" + machine)))
        if len(result_folder) == 1:
            files = list(map(lambda measure, labels: ("results/" + machine + "/" + result_folder[0] + "/" + measure + ".csv", labels, label, machine), filenameMarker, labels))
            read_files_and_plot_box(files        = files, 
                                    plotFilename = "plots/individual/" + machine + "_" + vmi_app + "_" + variant + ".pdf", 
                                    limits       = [(0.5, 4.5), (0, 225)], 
                                    textOffset   = (0.24, 0), 
                                    figureSize   = (10, 6), 
                                    fontSize     = 10, 
                                    scaling      = 1000, 
                                    unit         = "\u03bcs")
        elif len(result_folder) == 0:
            print("  WARNING: did not find " + variant)
        else:
            print("  ERROR: found " + variant + " multiple times for machine " + machine)
            exit(1)
