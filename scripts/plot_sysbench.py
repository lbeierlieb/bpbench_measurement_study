import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("plots/summary_selected.csv")

df["machine"] = df["machine"].apply(lambda s: "_".join(s.split("_")[1:3]))

# Keep only sysbench results
df = df[df["metric"] == "sysbench"]

machines = df["machine"].unique()
x = np.arange(len(machines))

fig, ax = plt.subplots(figsize=(8, 6))

# Plot sysbench median as a single bar per CPU
heights = [df[df["machine"] == m]["median"].values[0] for m in machines]
ax.bar(x, heights, color="grey", edgecolor="black", label="sysbench median")

# Labels & formatting
ax.set_xlabel("CPU", fontsize=14, fontweight="bold")
ax.set_ylabel("Sysbench score", fontsize=14, fontweight="bold")
ax.set_title("Sysbench Scores", fontsize=16, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(machines, rotation=30, ha="right")

plt.tight_layout()
plt.savefig("plots/sysbench_scores.pdf", format="pdf")
