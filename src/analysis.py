from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VIZ_DIR = ROOT / "visualizations"


def generate_sample_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    machines = ["M-101", "M-102", "M-103", "M-104", "M-105"]
    shifts = ["Day", "Night"]
    rows = []

    for day in range(1, 31):
        for machine in machines:
            for shift in shifts:
                produced = int(rng.integers(100, 320))
                defects = int(rng.integers(2, 35))
                downtime = int(rng.integers(0, 18))
                yield_rate = round(np.clip((produced - defects) / produced, 0.65, 0.99), 4)
                rows.append(
                    {
                        "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=day - 1),
                        "machine": machine,
                        "shift": shift,
                        "produced_units": produced,
                        "defects": defects,
                        "downtime_minutes": downtime,
                        "yield_rate": yield_rate,
                    }
                )

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("machine", as_index=False)
        .agg(
            total_units=("produced_units", "sum"),
            total_defects=("defects", "sum"),
            avg_yield=("yield_rate", "mean"),
            total_downtime=("downtime_minutes", "sum"),
        )
        .sort_values("total_units", ascending=False)
    )
    summary["defect_rate"] = summary["total_defects"] / summary["total_units"]
    return summary


def save_outputs(df: pd.DataFrame, summary: pd.DataFrame) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    VIZ_DIR.mkdir(exist_ok=True)

    csv_path = DATA_DIR / "manufacturing_data.csv"
    df.to_csv(csv_path, index=False)

    production_chart = (
        summary.sort_values("total_units")
        .plot(
            kind="bar",
            x="machine",
            y="total_units",
            color="steelblue",
            title="Production by Machine",
            legend=False,
            figsize=(10, 5),
        )
    )
    production_chart.set_xlabel("Machine")
    production_chart.set_ylabel("Units Produced")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "production_by_machine.png", dpi=150)
    plt.close()

    defect_chart = (
        summary.sort_values("defect_rate")
        .plot(
            kind="bar",
            x="machine",
            y="defect_rate",
            color="tomato",
            title="Defect Rate by Machine",
            legend=False,
            figsize=(10, 5),
        )
    )
    defect_chart.set_xlabel("Machine")
    defect_chart.set_ylabel("Defect Rate")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "defects_by_machine.png", dpi=150)
    plt.close()

    trend = (
        df.groupby("date", as_index=False)["produced_units"]
        .sum()
        .rename(columns={"produced_units": "total_units"})
    )
    trend_plot = trend.plot(
        x="date",
        y="total_units",
        kind="line",
        marker="o",
        color="darkgreen",
        figsize=(10, 5),
        title="Production Trend Over Time",
    )
    trend_plot.set_xlabel("Date")
    trend_plot.set_ylabel("Total Units Produced")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "output_trend.png", dpi=150)
    plt.close()

    # Defect-rate analysis by machine
    df["Machine"] = df["machine"]
    df["Production"] = df["produced_units"]
    df["Defects"] = df["defects"]
    df["Downtime"] = df["downtime_minutes"]
    df["Defect_Rate"] = (df["Defects"] / df["Production"]) * 100

    machine_defect_rate = df.groupby("Machine", as_index=False)[["Defect_Rate"]].mean()
    machine_defect_rate["Defect_Rate"] = machine_defect_rate["Defect_Rate"].round(2)

    print("\n===== DEFECT RATE ANALYSIS =====")
    print(df[["Machine", "Production", "Defects", "Defect_Rate"]].head(10).to_string(index=False))

    highest_defect_rate = machine_defect_rate.loc[machine_defect_rate["Defect_Rate"].idxmax()]
    print("\nMachine with Highest Defect Rate:")
    print(highest_defect_rate.to_string(index=False))

    defect_rate_chart = machine_defect_rate.plot(
        kind="bar",
        x="Machine",
        y="Defect_Rate",
        color="darkorange",
        title="Defect Rate by Machine",
        legend=False,
        figsize=(10, 5),
    )
    defect_rate_chart.set_xlabel("Machine")
    defect_rate_chart.set_ylabel("Defect Rate (%)")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "defect_rate_by_machine.png", dpi=150)
    plt.close()

    machine_performance = (
        df.groupby("Machine", as_index=False)
        .agg(
            Production=("Production", "sum"),
            Defects=("Defects", "sum"),
            Downtime=("Downtime", "sum"),
        )
    )

    machine_performance["Production_Score"] = (
        machine_performance["Production"] / machine_performance["Production"].max()
    ) * 100
    machine_performance["Defect_Score"] = (
        1 - (machine_performance["Defects"] / machine_performance["Defects"].max())
    ) * 100
    machine_performance["Downtime_Score"] = (
        1 - (machine_performance["Downtime"] / machine_performance["Downtime"].max())
    ) * 100
    machine_performance["Performance_Score"] = (
        machine_performance["Production_Score"] * 0.5
        + machine_performance["Defect_Score"] * 0.3
        + machine_performance["Downtime_Score"] * 0.2
    )

    print("\n===== MACHINE PERFORMANCE ANALYSIS =====")
    print(
        machine_performance[
            ["Machine", "Production", "Defects", "Downtime", "Performance_Score"]
        ].to_string(index=False)
    )

    best_machine = machine_performance.loc[machine_performance["Performance_Score"].idxmax()]
    print("\nBest Performing Machine:")
    print(best_machine.to_string(index=False))

    machine_ranking = df[
        ["Machine", "Production", "Defects", "Downtime", "Defect_Rate", "Performance_Score"]
    ].sort_values(by="Performance_Score", ascending=False)

    print("\n===== MACHINE RANKING =====")
    print(machine_ranking.to_string(index=False))

    plt.figure(figsize=(10, 6))
    plt.bar(machine_performance["Machine"], machine_performance["Performance_Score"])
    plt.title("Machine Performance Score")
    plt.xlabel("Machine")
    plt.ylabel("Performance Score")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "machine_performance_score.png", dpi=150)
    plt.close()

    # Use machine_performance for the ranking table and insights
    machine_ranking = machine_performance.sort_values(
        by="Performance_Score", ascending=False
    )

    best_machine = machine_ranking.iloc[0]
    worst_machine = machine_ranking.iloc[-1]
    highest_downtime = df.loc[df["Downtime"].idxmax()]
    highest_defect_machine = df.loc[df["Defect_Rate"].idxmax()]

    print("\n===== ACTIONABLE INSIGHTS =====")
    print(
        f"\nBest Performing Machine: {best_machine['Machine']}"
        f"\nPerformance Score: {best_machine['Performance_Score']:.2f}"
    )
    print(
        f"\nMachine Requiring Attention: {worst_machine['Machine']}"
        f"\nPerformance Score: {worst_machine['Performance_Score']:.2f}"
    )
    print(
        f"\nHighest Downtime Machine: {highest_downtime['Machine']}"
        f"\nDowntime: {highest_downtime['Downtime']}"
    )
    print(
        f"\nHighest Defect Rate Machine: {highest_defect_machine['Machine']}"
        f"\nDefect Rate: {highest_defect_machine['Defect_Rate']:.2f}%"
    )
    print(
        "\nRecommendation:"
        "\nInvestigate machines with high downtime and defect rates."
        "\nPrioritize preventive maintenance for low-performing machines."
    )

    print(f"Saved dataset to: {csv_path}")
    print(f"Saved visualizations to: {VIZ_DIR}")


if __name__ == "__main__":
    df = generate_sample_data()
    summary = summarize_data(df)
    save_outputs(df, summary)
    print("\nManufacturing analytics summary:")
    print(summary.head(10).to_string(index=False))
