"""EC marker analysis for Day08

Creates `day08/` (if missing), loads a CSV of marker results, filters
significant genes (p_val_adj < 0.05), finds top 10 genes per cluster by
avg_log2FC, saves summary CSV and plots (bar, volcano, cluster counts)
into the `day08/` folder.

Usage:
    python day08/ec_marker_analysis.py "gonads_ecs_sig_markers.xlsx - Sheet 1.csv"
"""
from pathlib import Path
import argparse
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def ensure_outdir(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Normalize expected numeric columns
    for col in ("avg_log2FC", "p_val_adj"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def safe_neg_log10(pvals):
    arr = np.array(pvals, dtype=float)
    tiny = np.finfo(float).tiny
    arr = np.where((arr <= 0) | np.isnan(arr), tiny, arr)
    return -np.log10(arr)


def top10_per_cluster(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if "cluster" not in df.columns:
        # If no cluster column, return top N overall
        sel = df.sort_values("avg_log2FC", ascending=False).head(top_n)
        sel = sel.assign(cluster="NA")
        return sel

    grouped = []
    for cluster, g in df.groupby("cluster"):
        # Only consider significant where possible
        if "p_val_adj" in g.columns:
            g_sig = g[g["p_val_adj"] < 0.05].copy()
        else:
            g_sig = g.copy()

        if "avg_log2FC" in g_sig.columns:
            top = g_sig.sort_values("avg_log2FC", ascending=False).head(top_n)
        else:
            top = g_sig.head(top_n)

        if not top.empty:
            top = top.assign(cluster=cluster)
            grouped.append(top)

    if grouped:
        return pd.concat(grouped, ignore_index=True)
    else:
        # No significant genes per cluster, return empty DataFrame
        return pd.DataFrame()


def plot_top10_bar(top_df: pd.DataFrame, outpath: Path):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))

    if top_df.empty:
        print("No top markers to plot for bar chart.")
        return

    # Determine gene column
    gene_col = "gene" if "gene" in top_df.columns else top_df.columns[0]

    # For bar plot show overall top 10 by avg_log2FC
    if "avg_log2FC" in top_df.columns:
        top_overall = top_df.sort_values("avg_log2FC", ascending=False).head(10)
        ax = sns.barplot(data=top_overall, x="avg_log2FC", y=gene_col, palette="mako")
        ax.set_title("Top 10 genes by avg_log2FC")
        ax.set_xlabel("avg_log2FC")
        ax.set_ylabel("Gene")
        plt.tight_layout()
        plt.savefig(outpath, dpi=150)
        plt.close()
    else:
        print("avg_log2FC column not present; skipping bar plot.")


def plot_volcano(df: pd.DataFrame, outpath: Path):
    sns.set(style="whitegrid")
    if not {"avg_log2FC", "p_val_adj"}.issubset(df.columns):
        print("Missing columns for volcano plot; need 'avg_log2FC' and 'p_val_adj'.")
        return

    plot_df = df.copy()
    plot_df["neg_log10_p"] = safe_neg_log10(plot_df["p_val_adj"])
    plot_df["significant"] = plot_df["p_val_adj"] < 0.05

    plt.figure(figsize=(8, 6))
    ax = sns.scatterplot(data=plot_df, x="avg_log2FC", y="neg_log10_p",
                         hue="significant", palette={True: "red", False: "grey"},
                         alpha=0.7, edgecolor=None)

    # reference lines
    ax.axhline(-np.log10(0.05), ls="--", color="black", lw=0.8)
    ax.axvline(0, ls="--", color="black", lw=0.6)
    ax.set_xlabel("avg_log2FC")
    ax.set_ylabel("-log10(p_val_adj)")
    ax.set_title("Volcano plot")
    plt.legend(title="p_val_adj < 0.05")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_cluster_counts(df: pd.DataFrame, outpath: Path):
    sns.set(style="whitegrid")
    if "cluster" not in df.columns:
        print("No 'cluster' column present; skipping cluster count plot.")
        return

    # Consider only significant if available
    if "p_val_adj" in df.columns:
        dfc = df[df["p_val_adj"] < 0.05].copy()
    else:
        dfc = df.copy()

    if dfc.empty:
        print("No significant markers to plot for clusters.")
        return

    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=dfc, x="cluster", palette="viridis")
    ax.set_title("Count of significant markers per cluster")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def save_summary(top_df: pd.DataFrame, outpath: Path):
    if top_df.empty:
        print("No top markers to save in summary.")
        return

    # Keep useful columns if present
    cols = [c for c in ("cluster", "gene", "avg_log2FC", "p_val_adj") if c in top_df.columns]
    summary = top_df[cols].copy()
    summary.to_csv(outpath, index=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Day08 EC marker analysis and plots")
    parser.add_argument("csv", help="Path to CSV file (e.g. 'gonads_ecs_sig_markers.xlsx - Sheet 1.csv')")
    parser.add_argument("--outdir", default="day08", help="Output directory (default: day08)")
    args = parser.parse_args(argv)

    outdir = Path(args.outdir)
    ensure_outdir(outdir)

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        sys.exit(2)

    df = load_csv(csv_path)

    # Filter significant
    if "p_val_adj" in df.columns:
        df_sig = df[df["p_val_adj"] < 0.05].copy()
    else:
        df_sig = df.copy()

    # Identify top 10 per cluster
    top_per_cluster = top10_per_cluster(df, top_n=10)

    # Save summary CSV
    summary_path = outdir / "top_markers_summary.csv"
    save_summary(top_per_cluster, summary_path)

    # Plots
    plot_top10_bar(top_per_cluster, outdir / "top10_bar.png")
    plot_volcano(df, outdir / "volcano.png")
    plot_cluster_counts(df, outdir / "cluster_counts.png")

    print("Outputs written to:", outdir.resolve())


if __name__ == "__main__":
    main()
