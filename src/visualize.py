from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "manufacturing_data.csv"
VIZ_DIR = ROOT / "visualizations"


def generate_visuals() -> None:
    VIZ_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("No data available in manufacturing_data.csv")

    by_machine = (
        df.groupby("machine", as_index=False)
        .agg(total_units=("produced_units", "sum"), total_defects=("defects", "sum"))
    )
    by_machine["defect_rate"] = by_machine["total_defects"] / by_machine["total_units"]

    plt.figure(figsize=(10, 5))
    sns.barplot(data=by_machine, x="machine", y="total_units", color="steelblue")
    plt.title("Production by Machine")
    plt.xlabel("Machine")
    plt.ylabel("Units Produced")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "production_by_machine.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(data=by_machine, x="machine", y="defect_rate", color="tomato")
    plt.title("Defect Rate by Machine")
    plt.xlabel("Machine")
    plt.ylabel("Defect Rate")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "defects_by_machine.png", dpi=150)
    plt.close()

    print("Visualizations generated successfully.")


if __name__ == "__main__":
    generate_visuals()
