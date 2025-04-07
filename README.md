# 🧪 mzQC Visualizer MVP

A modern web application for visualizing and analyzing mzQC (Mass Spectrometry Quality Control) files. Built with Streamlit and Python, this tool provides an intuitive interface for exploring quality metrics from mass spectrometry experiments.

> **Note**: This is an MVP (Minimum Viable Product) developed as part of the Google Summer of Code 2025 project for [OpenMS](https://www.openms.de/). The project aims to provide a user-friendly interface for visualizing mzQC files, with future enhancements planned based on community feedback.

## 📌 Features

- 📊 **Interactive Visualization**: Dynamic charts and graphs for numeric metrics using Altair
- 🔄 **Run Comparison**: Compare metrics across multiple runs in a single view
- 📋 **Detailed Metrics View**: Categorized display of numeric, list, and other metrics
- 📑 **Report Generation**: Export detailed HTML reports for both single runs and comparisons
- ✅ **Schema Validation**: Automatic validation against the official mzQC JSON schema
- 📈 **Responsive Design**: Modern, user-friendly interface that adapts to your data

## 🛠 Tech Stack

- `Streamlit` – Web app UI
- `Altair` – Visualizations
- `pandas` – Data handling
- `mzqc` – File parsing
- `jsonschema` – Schema validation
- `Python 3.8+`

## 📁 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mzqc-visualizer-mvp.git
   cd mzqc-visualizer-mvp
   ```

2. **Set up the virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. Open your browser to the local URL (typically http://localhost:8501) and upload a `.mzQC` file to begin!

## 📂 Project Structure

```
mzqc-visualizer-mvp/
├── app.py             # Application entry point
├── src/
│   ├── main.py       # Main application and UI logic
│   ├── parser.py     # mzQC file parsing functionality
│   ├── validator.py  # Schema validation
│   └── utils.py      # Utility functions and visualization helpers
├── .gitignore       # Git ignore rules
├── setup.cfg        # Development tool configurations
├── requirements.txt  # Python dependencies
└── README.md        # Project documentation
```

## 🧠 Planned Features

- **Enhanced Batch Processing**: Support for multiple file uploads and batch analysis
- **Advanced Visualization**: More chart types and interactive filtering options
- **Customizable Dashboards**: User-defined metric views and layouts
- **Integration with OpenMS**: Seamless workflow integration with OpenMS tools
- **Offline CV Support**: Local controlled vocabulary for better performance
- **Statistical Analysis**: Basic statistical tests and outlier detection
- **Export Options**: Additional export formats (PDF, Excel) and customizable reports

## 📊 Example Files

To try out the application, you can use these example mzQC files from the HUPO-PSI repository:

1. **Single Run Example** ([intro_run.mzQC](https://github.com/HUPO-PSI/mzQC/blob/main/specification_documents/examples/intro_run.mzQC))
   - Basic example with a single mass spectrometry run
   - Contains MS1/MS2 spectra counts and acquisition ranges
   - Good for testing basic visualization features

2. **QC2 Sample Example** ([intro_qc2.mzQC](https://github.com/HUPO-PSI/mzQC/blob/main/specification_documents/examples/intro_qc2.mzQC))
   - Contains detailed QC2 sample measurements
   - Includes mass accuracies and intensities for specific peptides
   - Demonstrates complex metric visualization

3. **Batch Comparison Example** ([metabo-batches.mzQC](https://github.com/HUPO-PSI/mzQC/blob/main/specification_documents/examples/metabo-batches.mzQC))
   - Multiple batch runs for comparison
   - Ideal for testing the comparison mode
   - Shows batch-to-batch variations

To use these examples:
1. Download the raw content of any example file
2. Save it with a `.mzQC` extension
3. Upload it to the application

## 👨‍💻 Development

To contribute to the project:

1. Ensure you have development dependencies installed:
```bash
pip install flake8 black
```

2. Format code using Black:
```bash
black src/ app.py
```

3. Run linting checks:
```bash
flake8 src/ app.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenMS](https://www.openms.de/) for the Google Summer of Code 2025 opportunity
- [HUPO-PSI](https://www.psidev.info/) for the mzQC standard and schema
- The mass spectrometry community for feedback and support
