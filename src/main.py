import streamlit as st
from src import parser, validator, utils
import pandas as pd
import altair as alt


def is_numeric_value(x):
    return isinstance(x, (int, float))


def categorize_metrics(df):
    """Categorize metrics by their data type."""
    numeric_df = df[df["value"].apply(is_numeric_value)]
    list_df = df[df["value"].apply(lambda x: isinstance(x, list))]
    mask = ~df.index.isin(numeric_df.index) & ~df.index.isin(list_df.index)
    other_df = df[mask]
    return numeric_df, list_df, other_df


def create_comparison_df(metric_dfs, metadata_list, selected_runs):
    """Create a DataFrame for comparing metrics across selected runs."""
    all_numeric_dfs = []
    for i, (df, meta) in enumerate(zip(metric_dfs, metadata_list)):
        if i in selected_runs:
            numeric_df = df[df["value"].apply(is_numeric_value)].copy()
            if not numeric_df.empty:
                run_label = f"Run {i+1}: {meta['label']}"
                numeric_df["run"] = run_label
                all_numeric_dfs.append(numeric_df)

    if all_numeric_dfs:
        return pd.concat(all_numeric_dfs, ignore_index=True)
    return None


def show(chart):
    """Display an Altair chart with full width."""
    st.altair_chart(chart, use_container_width=True)


def main():
    st.set_page_config(page_title="mzQC Visualizer", layout="wide")
    st.title("🧪 mzQC Visualizer")

    uploaded_file = st.file_uploader("📂 Upload a `.mzQC` file", type="mzQC")

    if uploaded_file is not None:
        json_str = uploaded_file.read().decode("utf-8")
        is_valid, validation_msg = validator.validate_mzqc(json_str)

        if is_valid:
            st.success(validation_msg)
            result = parser.parse_mzqc(json_str)
            metadata_list, metric_dfs, file_metadata = result

            st.subheader("📄 File Metadata")
            st.write(f"**Version**: {file_metadata['version']}")
            st.write(f"**Contact Name**: {file_metadata['contactName']}")
            st.write(f"**Contact Address**: {file_metadata['contactAddress']}")
            st.write(f"**Creation Date**: {file_metadata['creationDate']}")
            st.write(f"**Description**: {file_metadata['description']}")

            if not metadata_list:
                st.warning("No runs found in the file.")
            else:
                # Mode selection
                if len(metadata_list) > 1:
                    comparison_mode = st.toggle(
                        "Enable Comparison Mode",
                        value=False,
                        help=("Switch between single run view " "and comparison view"),
                    )
                else:
                    comparison_mode = False

                if comparison_mode:
                    st.subheader("🔄 Run Comparison")

                    # Run selection
                    run_options = [
                        f"Run {i+1}: {md['label']}"
                        for i, md in enumerate(metadata_list)
                    ]
                    selected_runs = st.multiselect(
                        "Select runs to compare",
                        options=range(len(run_options)),
                        default=[0, 1] if len(metadata_list) > 1 else [0],
                        format_func=lambda i: run_options[i],
                        max_selections=5,  # Limit to 5 runs for readability
                    )

                    if selected_runs:
                        comparison_df = create_comparison_df(
                            metric_dfs,
                            metadata_list,
                            selected_runs,
                        )

                        if comparison_df is not None:
                            # Get unique metric names
                            metric_names = comparison_df["name"].unique()
                            selected_metric = st.selectbox(
                                "Select metric to compare",
                                metric_names,
                            )

                            # Add export button for comparison report
                            st.download_button(
                                "📥 Export Comparison Report",
                                utils.generate_comparison_report_html(
                                    metadata_list,
                                    comparison_df,
                                    selected_metric,
                                ),
                                file_name="mzqc_comparison_report.html",
                                mime="text/html",
                            )

                            # Filter data for selected metric
                            metric_data = comparison_df[
                                comparison_df["name"] == selected_metric
                            ]

                            # Create comparison chart
                            st.write(f"**Comparing {selected_metric}**")

                            # Calculate height for chart
                            min_height = 100  # Minimum height in pixels
                            height_per_run = 60  # Height per run
                            chart_height = max(
                                min_height,
                                len(metric_data) * height_per_run,
                            )

                            chart = (
                                alt.Chart(metric_data)
                                .encode(
                                    y=alt.Y(
                                        "run:N",
                                        title=None,
                                        axis=alt.Axis(
                                            labelColor="white",
                                            labelFontSize=12,
                                            labelLimit=200,
                                            labelPadding=10,
                                        ),
                                    ),
                                    x=alt.X(
                                        "value:Q",
                                        title="Value",
                                        axis=alt.Axis(
                                            labelColor="white",
                                            gridColor="#333",
                                            tickColor="white",
                                        ),
                                    ),
                                    tooltip=["run", "value"],
                                )
                                .properties(height=chart_height, width=600)
                            )

                            bars = chart.mark_bar(color="#7FB3D5", height=20)

                            text = chart.mark_text(
                                align="left",
                                baseline="middle",
                                dx=5,
                                color="white",
                                fontSize=12,
                            ).encode(text=alt.Text("value:Q", format=".2f"))

                            # Configure chart padding
                            padding_config = {
                                "left": 10,
                                "right": 30,
                                "top": 10,
                                "bottom": 10,
                            }

                            final_chart = (
                                alt.layer(bars, text)
                                .properties(padding=padding_config)
                                .configure_view(strokeWidth=0)
                                .configure(background="#1E1E1E")
                            )

                            # Display chart
                            show(final_chart)

                            # Show comparison table
                            st.write("**Detailed Comparison**")
                            st.dataframe(
                                metric_data[["run", "value"]],
                                column_config={
                                    "value": st.column_config.NumberColumn(
                                        "value",
                                        help="Metric value",
                                    )
                                },
                            )
                    else:
                        msg = "Please select at least one run to compare."
                        st.warning(msg)

                else:  # Individual run view
                    run_options = [
                        f"Run {i+1}: {md['label']}"
                        for i, md in enumerate(metadata_list)
                    ]
                    selected_run = st.selectbox(
                        "Select a run to view details",
                        range(len(run_options)),
                        format_func=lambda i: run_options[i],
                    )

                    # Process and categorize metrics
                    metrics = metric_dfs[selected_run]
                    df_metrics = utils.clean_metrics_df(metrics)
                    result = categorize_metrics(df_metrics)
                    numeric_df, list_df, other_df = result

                    # Display run metadata
                    st.subheader("📋 Run Metadata")

                    # Add export button for single run report
                    st.download_button(
                        "📥 Export Run Report",
                        utils.generate_run_report_html(
                            metadata_list[selected_run],
                            numeric_df,
                            list_df,
                            other_df,
                        ),
                        file_name=f"mzqc_run_{selected_run+1}_report.html",
                        mime="text/html",
                    )

                    # Display metadata fields
                    run_data = metadata_list[selected_run]
                    st.write(f"**Label**: {run_data['label']}")
                    st.write(f"**Input File**: {run_data['input_file']}")
                    st.write(f"**Software**: {run_data['software']}")

                    # Display numeric metrics
                    if not numeric_df.empty:
                        st.subheader("📊 Numeric Metrics")
                        st.dataframe(
                            numeric_df,
                            column_config={
                                "value": st.column_config.NumberColumn(
                                    "value",
                                    help="Metric value",
                                )
                            },
                        )

                        # Visualize numeric metrics
                        st.subheader("📈 Metrics Visualization")
                        for _, row in numeric_df.iterrows():
                            metric_name = row["name"]
                            value = row["value"]

                            st.write(f"**{metric_name}**")

                            metric_df = pd.DataFrame(
                                {
                                    "Metric": [metric_name],
                                    "Value": [value],
                                }
                            )

                            x_domain = [0, value * 1.1]

                            base = (
                                alt.Chart(metric_df)
                                .encode(
                                    y=alt.Y(
                                        "Metric:N",
                                        title=None,
                                        axis=alt.Axis(
                                            labelColor="white",
                                            labelFontSize=12,
                                            labelLimit=200,
                                        ),
                                    ),
                                    x=alt.X(
                                        "Value:Q",
                                        title="Value",
                                        scale=alt.Scale(domain=x_domain),
                                        axis=alt.Axis(
                                            labelColor="white",
                                            gridColor="#333",
                                            tickColor="white",
                                        ),
                                    ),
                                    tooltip=["Metric", "Value"],
                                )
                                .properties(height=30, width=600)
                            )

                            bar = base.mark_bar(color="#7FB3D5", height=8)

                            text = base.mark_text(
                                align="left",
                                baseline="middle",
                                dx=5,
                                color="white",
                                fontSize=12,
                            ).encode(text=alt.Text("Value:Q", format=".2f"))

                            final_chart = (
                                alt.layer(bar, text)
                                .configure_view(strokeWidth=0)
                                .configure(background="#1E1E1E")
                            )

                            show(final_chart)

                    # Display list metrics
                    if not list_df.empty:
                        col1, col2 = st.columns([0.85, 0.15])
                        with col1:
                            st.subheader("📋 List Metrics")
                        with col2:
                            st.download_button(
                                "⬇ Download CSV",
                                data=list_df.to_csv(index=False),
                                file_name="list_metrics.csv",
                                mime="text/csv",
                                key="list_download",
                            )

                        for _, row in list_df.iterrows():
                            with st.expander(f"{row['name']}"):
                                st.write("Values:")
                                st.json(row["value"])

                    # Display other metrics
                    if not other_df.empty:
                        col1, col2 = st.columns([0.85, 0.15])
                        with col1:
                            st.subheader("📑 Other Metrics")
                        with col2:
                            st.download_button(
                                "⬇ Download CSV",
                                data=other_df.to_csv(index=False),
                                file_name="other_metrics.csv",
                                mime="text/csv",
                                key="other_download",
                            )

                        for _, row in other_df.iterrows():
                            with st.expander(f"{row['name']}"):
                                st.write("Value:")
                                st.code(str(row["value"]))

        else:
            st.error(validation_msg)


if __name__ == "__main__":
    main()
