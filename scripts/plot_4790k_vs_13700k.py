import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("plots/summary_selected.csv")

df["machine"] = df["machine"].apply(lambda s: "_".join(s.split("_")[1:3]))

scale_factor = 4.0 / 3.4
scaled = df[df["machine"] == "i7_4790K"].copy()
scaled["machine"] = "i7_4790K@3.4GHz"
scaled["median"] *= scale_factor
scaled["min"] *= scale_factor
df = pd.concat([df, scaled], ignore_index=True)

machines = ["i7_4790K", "i7_13700K", "i7_4790K@3.4GHz"]
metrics = ["exec_bp_altp2m", "exec_bp_altp2m_fss", "read_bp_altp2m"]

barWidth = 0.25
x = np.arange(len(machines))  # positions for CPUs

fig, ax = plt.subplots(figsize=(14, 8))

colors = {
    "exec_bp_rep":        "red",
    "exec_bp_emul":       "lime",
    "exec_bp_altp2m":     "cornflowerblue",
    "exec_bp_altp2m_fss": "deepskyblue",
    "read_bp_emul":       "greenyellow",
    "read_bp_altp2m":     "lightskyblue",
}

labels = {
    "exec_bp_rep":        "WL1 exec_bp_rep             (SmartVMI)",
    "exec_bp_emul":       "WL1 exec_bp_emul          (SmartVMI)",
    "exec_bp_altp2m":     "WL1 exec_bp_altp2m       (DRAKVUF)",
    "exec_bp_altp2m_fss": "WL1 exec_bp_altp2m_fss (DRAKVUF)",
    "read_bp_emul":       "WL3 read_bp_emul          (SmartVMI)",
    "read_bp_altp2m":     "WL3 read_bp_altp2m       (DRAKVUF)",
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
plt.savefig("plots/i7_4790K_vs_i7_13700K.pdf", format="pdf")
