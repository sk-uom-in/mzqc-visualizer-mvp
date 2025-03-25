import os
import pandas as pd
from mzqc.MZQCFile import JsonSerialisable


def load_mzqc_from_file(file_path: str):
    print(f"\n📂 Loading mzQC file: {file_path}")
    with open(file_path, 'r') as f:
        mzqc = JsonSerialisable.FromJson(f.read())
    return mzqc


def print_metadata_and_metrics(mzqc):
    for run in mzqc.runQualities:
        print("\n📋 Metadata Summary:")
        if run.metadata.inputFiles:
            print(f"Input File: {run.metadata.inputFiles[0].location}")
        if run.metadata.analysisSoftware:
            print(
                f"Analysis Software: {run.metadata.analysisSoftware[0].name} "
                f"v{run.metadata.analysisSoftware[0].version}"
            )
        if run.metadata.label:
            print(f"Label: {run.metadata.label}")
        print("-" * 40)

        metrics_data = []
        for metric in run.qualityMetrics:
            metrics_data.append({
                "accession": metric.accession,
                "name": metric.name,
                "value": metric.value,
                "unit_name": getattr(metric.unit, 'name', 'None'),
                "unit_accession": getattr(metric.unit, 'accession', 'None')
            })

        df = pd.DataFrame(metrics_data)

        # Save to CSV
        df.to_csv("parsed_metrics.csv", index=False)
        print("\nSaved metrics to parsed_metrics.csv")

        # Display summary info
        print(f"\nParsed {len(df)} metrics")
        print(f"Unique metric names: {df['name'].nunique()}")
        print(f"Unique units: {df['unit_name'].nunique()}")

        # Display first few unique metric names
        print("\n📌 Sample metric names:")
        print(df['name'].unique()[:5])

        # Display first 10 rows as preview
        print("\n📈 First 10 Quality Metrics:")
        print(df.head(10))


if __name__ == "__main__":
    file_path = os.path.join("sample_files", "intro_run.mzQC")
    mzqc_obj = load_mzqc_from_file(file_path)
    print_metadata_and_metrics(mzqc_obj)