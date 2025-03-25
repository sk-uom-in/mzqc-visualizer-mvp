import streamlit as st
import pandas as pd
import altair as alt
from mzqc.MZQCFile import JsonSerialisable

st.set_page_config(page_title="mzQC Visualizer", layout="wide")
st.title("🧪 mzQC Quality Metrics Visualizer")

uploaded_file = st.file_uploader("Upload an .mzQC file", type="mzQC")

if uploaded_file is not None:
    try:
        with st.spinner("🔄 Parsing .mzQC file..."):
            raw_json = uploaded_file.read().decode("utf-8")
            mzqc = JsonSerialisable.FromJson(raw_json)
            st.success("✅ File loaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to parse file: {e}")
        st.stop()

    run_count = len(mzqc.runQualities)
    selected_index = st.selectbox(
        "Select a run to view",
        options=range(run_count),
        format_func=lambda x: f"Run {x}"
    )
    run = mzqc.runQualities[selected_index]

    st.subheader(f"📋 Metadata – Run {selected_index}")

    if run.metadata.inputFiles:
        st.markdown(f"- **Input File**: `{run.metadata.inputFiles[0].location}`")

    if run.metadata.analysisSoftware:
        sw = run.metadata.analysisSoftware[0]
        st.markdown(f"- **Software**: {sw.name} v{sw.version}")

    if hasattr(run.metadata, 'label') and run.metadata.label:
        st.markdown(f"- **Label**: {run.metadata.label}")

    if hasattr(run.metadata, 'sample') and run.metadata.sample:
        sample = run.metadata.sample[0]
        st.markdown(f"- **Sample Name**: {getattr(sample, 'name', 'N/A')}")
        st.markdown(f"- **Sample Description**: {getattr(sample, 'description', 'N/A')}")

    if hasattr(run.metadata, 'instrument') and run.metadata.instrument:
        st.markdown(f"- **Instrument**: {run.metadata.instrument[0].name}")

    # Extract and normalize metrics
    metrics_data = []
    for metric in run.qualityMetrics:
        value = metric.value
        if isinstance(value, (int, float, str)):
            display_value = value
        else:
            display_value = f"{str(value)[:80]}..."

        metrics_data.append({
            "accession": metric.accession,
            "name": getattr(metric, 'name', metric.accession),
            "value": str(display_value),
            "unit_name": getattr(metric.unit, 'name', 'None'),
            "unit_accession": getattr(metric.unit, 'accession', 'None'),
            "is_scalar": isinstance(metric.value, (int, float))
        })

    df = pd.DataFrame(metrics_data)
    df["value"] = df["value"].astype(str)

    scalar_df = df[df['is_scalar']].copy()
    scalar_df['value'] = pd.to_numeric(scalar_df['value'], errors='coerce')
    scalar_df = scalar_df.dropna(subset=['value'])

    # ✂️ Truncate long metric names
    scalar_df['short_name'] = scalar_df['name'].apply(lambda x: x if len(x) <= 25 else x[:25] + "…")

    st.markdown("### 📊 Metric Summary")
    st.write(f"- Total Metrics: {len(df)}")
    st.write(f"- Unique Metric Names: {df['name'].nunique()}")
    st.write(f"- Unique Units: {df['unit_name'].nunique()}")

    st.markdown("#### 🏷️ Sample Metric Names")
    st.write(df['name'].dropna().unique()[:10])

    # Filter option
    st.markdown("### 📈 Preview of Quality Metrics")
    show_scalar_only = st.checkbox("🔢 Show only simple numeric metrics (plottable)", value=False)
    preview_df = df[df['is_scalar']] if show_scalar_only else df
    st.dataframe(preview_df.drop(columns=["is_scalar"]).head(20), use_container_width=True)

    # 📥 CSV download
    csv = preview_df.drop(columns=["is_scalar"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Metrics as CSV",
        data=csv,
        file_name=f"parsed_metrics_run_{selected_index}.csv",
        mime="text/csv",
        key=f"download_csv_{selected_index}"
    )

    st.markdown("### 📊 All Numeric Metrics (Bar Chart)")

    if not scalar_df.empty:
        bar_chart = alt.Chart(scalar_df).mark_bar().encode(
            y=alt.Y('short_name:N', sort=alt.SortField('value', order='descending'), title='Metric Name'),
            x=alt.X('value:Q', title='Value', scale=alt.Scale(zero=True)),
            tooltip=[alt.Tooltip('name:N', title="Full Name"), 'value', 'unit_name']
        ).properties(
            width=700,
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("No numeric metrics available to plot.")


    # 🔍 Inspect individual metric
    st.markdown("### 🔎 Inspect a Metric")
    if not scalar_df.empty:
        selected_metric = st.selectbox(
            "Choose a metric to inspect",
            scalar_df['name'].unique()
        )
        metric_row = scalar_df[scalar_df['name'] == selected_metric]

        st.metric(
            label=f"{selected_metric} ({metric_row['unit_name'].values[0]})",
            value=f"{metric_row['value'].values[0]:,.2f}"
        )
