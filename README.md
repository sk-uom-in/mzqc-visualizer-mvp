# 🧪 mzQC Visualizer MVP

This is a lightweight, Streamlit-based web application to **upload, explore, and visualize `.mzQC` quality control files** from mass spectrometry workflows.

🧠 Built as part of **Google Summer of Code 2025** with [OpenMS](https://www.openms.de/)

---

## 📌 Features

- Upload `.mzQC` files and extract run-level QC metadata
- Interactive tables for exploring scalar and structured metrics
- Altair-powered visualizations with dynamic filters and unit-based views
- Supports large files and complex metric structures
- Export metrics to CSV or interactive HTML report
- Designed for future `.obo` CV integration and batch mode

---

## 🛠 Tech Stack

- `Streamlit` – Web app UI
- `Altair` – Visualizations
- `pandas` – Data handling
- `pymzqc` *(planned)* / `mzqc.MZQCFile.JsonSerialisable` – File parsing
- `Python 3.12+`

---

## 📁 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/sk-uom-in/mzqc-visualizer-mvp.git
   cd mzqc-visualizer-mvp
   ```

2. **Set up the virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run src/streamlit_app.py
   ```

4. Open your browser to the local URL and upload a `.mzQC` file to begin!

---

## 📂 Folder Structure

```
mzqc-visualizer-mvp/
├── sample_files/           # Sample mzQC files
├── src/
│   ├── streamlit_app.py    # Main Streamlit interface
│   └── parse_mzqc.py       # File parsing logic
├── requirements.txt
└── README.md
```

---

## 🧠 Planned Features

- Batch upload and cross-run comparison
- Outlier detection and threshold alerts
- Offline PSI-MS CV support with `.obo` uploads
- PDF report generation
- Customizable metric templates for user-defined dashboards

---

## 👨‍💻 Author

**Sambbhav Khare**  
📧 sambbhavkhare@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sambbhavkhare/)  
🔗 [Portfolio](https://sambbhav-khare.dev)

---
