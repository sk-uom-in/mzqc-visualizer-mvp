import pandas as pd
from typing import Tuple, Optional
from mzqc.MZQCFile import JsonSerialisable


def load_mzqc_from_json_string(json_str: str):
    try:
        return JsonSerialisable.FromJson(json_str)
    except Exception as e:
        print("Parsing error:", e)
        raise


def extract_run_metadata(run) -> dict:
    metadata = run.metadata
    return {
        "label": getattr(metadata, "label", "N/A"),
        "input_file": (
            getattr(metadata.inputFiles[0], "location", "N/A")
            if metadata.inputFiles
            else "N/A"
        ),
        "software": (
            f"{metadata.analysisSoftware[0].name} "
            f"v{metadata.analysisSoftware[0].version}"
            if metadata.analysisSoftware
            else "N/A"
        ),
    }


def extract_quality_metrics(run) -> pd.DataFrame:
    metrics_data = []
    for metric in run.qualityMetrics:
        metrics_data.append(
            {
                "accession": metric.accession,
                "name": metric.name,
                "value": metric.value,
                "unit_name": (
                    getattr(metric.unit, "name", None)
                    if hasattr(metric, "unit") and metric.unit
                    else None
                ),
                "unit_accession": (
                    getattr(metric.unit, "accession", None)
                    if hasattr(metric, "unit") and metric.unit
                    else None
                ),
            }
        )
    return pd.DataFrame(metrics_data)


def extract_global_metadata(mzqc_obj) -> dict:
    return {
        "version": getattr(mzqc_obj, "version", "N/A"),
        "contactName": getattr(mzqc_obj, "contactName", "N/A"),
        "contactAddress": getattr(mzqc_obj, "contactAddress", "N/A"),
        "creationDate": getattr(mzqc_obj, "creationDate", "N/A"),
        "description": getattr(mzqc_obj, "description", "N/A"),
    }


def parse_mzqc(
    json_str: str,
) -> Tuple[Optional[list], Optional[list], Optional[dict]]:
    try:
        mzqc_obj = load_mzqc_from_json_string(json_str)
        run_qualities = mzqc_obj.runQualities or []
        set_qualities = mzqc_obj.setQualities or []

        all_runs = run_qualities + set_qualities
        run_metadata = [extract_run_metadata(run) for run in all_runs]
        metric_dfs = [extract_quality_metrics(run) for run in all_runs]
        file_metadata = extract_global_metadata(mzqc_obj)

        return run_metadata, metric_dfs, file_metadata
    except Exception as e:
        print(f"Error during parsing: {e}")
        return None, None, None
