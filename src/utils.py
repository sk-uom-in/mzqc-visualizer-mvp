import streamlit as st
import pandas as pd
import altair as alt
import json
from datetime import datetime
from typing import Dict, List, Union, Optional, Any


def clean_metrics_df(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and cast metric values to appropriate types."""
    df = df.copy()
    if "value" in df.columns:
        df["value"] = df["value"].apply(_smart_cast)
    return df


def generate_run_report_html(
    run_metadata: Dict[str, str],
    numeric_df: pd.DataFrame,
    list_df: pd.DataFrame,
    other_df: pd.DataFrame,
) -> str:
    """Generate HTML report for a single run."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>mzQC Run Report - {run_metadata['label']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #fafafa;
            }}
            .header {{
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f5f5f5;
                font-weight: bold;
            }}
            .section {{
                margin: 30px 0;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .timestamp {{
                color: #666;
                font-size: 0.9em;
            }}
            pre {{
                background: #f8f8f8;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }}
            h1, h2 {{
                color: #333;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>mzQC Run Report</h1>
            <p class="timestamp">Generated on: {timestamp}</p>
        </div>

        <div class="section">
            <h2>Run Metadata</h2>
            <table>
                <tr>
                    <th>Label</th>
                    <td>{run_metadata['label']}</td>
                </tr>
                <tr>
                    <th>Input File</th>
                    <td>{run_metadata['input_file']}</td>
                </tr>
                <tr>
                    <th>Software</th>
                    <td>{run_metadata['software']}</td>
                </tr>
            </table>
        </div>
    """

    if not numeric_df.empty:
        html += """
        <div class="section">
            <h2>Numeric Metrics</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Value</th>
                    <th>Unit Name</th>
                    <th>Unit Accession</th>
                </tr>
        """
        for _, row in numeric_df.iterrows():
            unit_name = row["unit_name"] if pd.notna(row["unit_name"]) else "-"
            unit_acc = row["unit_accession"] if pd.notna(row["unit_accession"]) else "-"
            html += f"""
                <tr>
                    <td>{row['name']}</td>
                    <td>{row['value']:.2f}</td>
                    <td>{unit_name}</td>
                    <td>{unit_acc}</td>
                </tr>
            """
        html += "</table></div>"

    if not list_df.empty:
        html += """
        <div class="section">
            <h2>List Metrics</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Values</th>
                </tr>
        """
        for _, row in list_df.iterrows():
            values = json.dumps(row["value"], indent=2)
            html += f"""
                <tr>
                    <td>{row['name']}</td>
                    <td><pre>{values}</pre></td>
                </tr>
            """
        html += "</table></div>"

    if not other_df.empty:
        html += """
        <div class="section">
            <h2>Other Metrics</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Value</th>
                </tr>
        """
        for _, row in other_df.iterrows():
            html += f"""
                <tr>
                    <td>{row['name']}</td>
                    <td><pre>{str(row['value'])}</pre></td>
                </tr>
            """
        html += "</table></div>"

    html += """
    </body>
    </html>
    """
    return html


def generate_comparison_report_html(
    metadata_list: List[Dict[str, str]],
    comparison_df: pd.DataFrame,
    selected_metric: Optional[str] = None,
) -> str:
    """Generate HTML report for run comparison."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
    <html>
    <head>
        <title>mzQC Comparison Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #fafafa;
            }}
            .header {{
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #f5f5f5;
                font-weight: bold;
            }}
            .section {{
                margin: 30px 0;
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .timestamp {{
                color: #666;
                font-size: 0.9em;
            }}
            h1, h2 {{
                color: #333;
                margin-bottom: 20px;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>mzQC Comparison Report</h1>
            <p class="timestamp">Generated on: {timestamp}</p>
        </div>

        <div class="section">
            <h2>Runs Overview</h2>
            <table>
                <tr>
                    <th>Run</th>
                    <th>Label</th>
                    <th>Input File</th>
                    <th>Software</th>
                </tr>
    """

    for i, meta in enumerate(metadata_list):
        html += f"""
            <tr>
                <td>Run {i+1}</td>
                <td>{meta['label']}</td>
                <td>{meta['input_file']}</td>
                <td>{meta['software']}</td>
            </tr>
        """

    html += "</table></div>"

    if comparison_df is not None:
        html += """
        <div class="section">
            <h2>Metrics Comparison</h2>
            <table>
                <tr>
                    <th>Run</th>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
        """

        if selected_metric:
            df_view = comparison_df[comparison_df["name"] == selected_metric]
        else:
            df_view = comparison_df

        for _, row in df_view.iterrows():
            html += f"""
                <tr>
                    <td>{row['run']}</td>
                    <td>{row['name']}</td>
                    <td>{row['value']:.2f}</td>
                </tr>
            """
        html += "</table></div>"

    html += """
    </body>
    </html>
    """
    return html


def _smart_cast(val: Union[str, int, float]) -> Union[str, int, float]:
    """Cast string values to appropriate numeric types if possible."""
    try:
        if isinstance(val, str):
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except ValueError:
                return val
        return val
    except Exception:
        return val


def render_single_value(value: Union[int, float, str], metric_name: str) -> None:
    """Render a single scalar value metric."""
    st.markdown(f"### 📊 {metric_name}")

    if isinstance(value, pd.DataFrame):
        value = value.iloc[0, 0]

    if isinstance(value, (int, float, str)):
        st.metric(label=metric_name, value=value)
        chart_data = pd.DataFrame({metric_name: [value]})
        st.bar_chart(chart_data)
    else:
        msg = f"⚠ Invalid metric type for `{metric_name}`: {type(value)}"
        st.warning(msg)


def visualize_metric(value: Any, name: str) -> None:
    """Visualize a metric with appropriate chart type."""
    st.markdown(f"### 🧪 {name}")
    if isinstance(value, (int, float)):
        _render_scalar(value, name)
    elif isinstance(value, list):
        _render_list(value, name)
    elif isinstance(value, dict):
        _render_dict(value, name)
    elif isinstance(value, str):
        _render_string(value, name)
    else:
        _render_unknown(value, name)


def _render_scalar(val: Union[int, float], name: str) -> None:
    st.metric(label=name, value=val)
    st.bar_chart(pd.DataFrame({name: [val]}))


def _render_list(lst: List[Any], name: str) -> None:
    is_numeric = all(isinstance(x, (int, float)) for x in lst)
    if is_numeric:
        indices = list(range(1, len(lst) + 1))
        df = pd.DataFrame({"index": indices, "value": lst})
        base = alt.Chart(df).mark_line(point=True)
        chart = base.encode(
            x="index:O", y="value:Q", tooltip=["index", "value"]
        ).properties(title=name)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.json(lst)


def _render_dict(dct: Dict[Any, Any], name: str) -> None:
    try:
        df = pd.DataFrame.from_dict(dct, orient="index").T
        st.dataframe(df)
    except Exception:
        st.json(dct)


def _render_string(text: str, name: str) -> None:
    if len(text) > 100:
        try:
            st.json(json.loads(text))
        except Exception:
            st.code(text)
    else:
        st.code(text)


def _render_unknown(val: Any, name: str) -> None:
    st.warning(f"⚠ Unknown format for `{name}`")
    st.write(val)


def render_table_metric(value: pd.DataFrame, name: str) -> None:
    """Render a metric when it has a tabular (dataframe) structure."""
    if isinstance(value, pd.DataFrame):
        st.subheader(f"📊 {name} as Table")
        st.dataframe(value)
    else:
        st.warning(f"⚠ Metric `{name}` has unsupported format.")
