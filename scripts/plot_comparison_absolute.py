import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("plots/summary_selected.csv")

df["machine"] = df["machine"].apply(lambda s: "_".join(s.split("_")[1:3]))

machines = df["machine"].unique()
metrics = df["metric"].unique()
metrics = list(metrics)
metrics.remove("sysbench")
metrics.remove("timing-overhead")

barWidth = 0.15
x = np.arange(len(machines))  # positions for CPUs

fig, ax = plt.subplots(figsize=(14, 8))

colors = {
    "ept_exec": "green",
    "ept-fast_exec": "blue",
    "ept_read": "orange",
    "repair_exec": "purple",
    "emul_exec": "cyan",
    "emul_read": "red",
}

labels = {
    "ept_exec": "DRAKVUF EPT exec",
    "ept-fast_exec": "DRAKVUF EPT FSS exec",
    "ept_read": "DRAKVUF read",
    "repair_exec": "SmartVMI repair exec",
    "emul_exec": "SmartVMI emul exec",
    "emul_read": "SmartVMI read",
}

# plot each metric as a bar group
for i, metric in enumerate(metrics):
    offsets = x + i * barWidth
    subset = df[df["metric"] == metric]

    # align the subset with machine order
    heights = [subset[subset["machine"] == m]["median"].values[0] if m in subset["machine"].values else 0 for m in machines]
    mins = [subset[subset["machine"] == m]["min"].values[0] if m in subset["machine"].values else 0 for m in machines]

    bars = ax.bar(offsets, heights, barWidth, label=labels.get(metric), color=colors.get(metric, "grey"), edgecolor="black")

    # draw the min line inside each bar
    for xi, min_val in zip(offsets, mins):
        ax.hlines(min_val, xi - barWidth/2, xi + barWidth/2, colors="black", linewidth=2)

# axis labels
ax.set_xlabel("CPU", fontsize=14, fontweight="bold")
ax.set_ylabel("Time (µs)", fontsize=14, fontweight="bold")
ax.set_title("Absolute Measurements", fontsize=16, fontweight="bold")

# x ticks
ax.set_xticks(x + (len(metrics)-1) * barWidth / 2)
ax.set_xticklabels(machines, rotation=30, ha="right")

ax.legend()
plt.tight_layout()
plt.savefig("plots/comparison_absolute.pdf", format="pdf")
