# CRM Inquiry Dashboard

A data-driven CRM dashboard built with Python and Streamlit to monitor inquiry pipelines, quotation progress, proposals, meetings, and deal outcomes.

## Project Overview

Managing client inquiries across multiple business verticals can make it difficult to track follow-ups, employee activity, and deal progress.

This project provides an interactive dashboard to organize inquiry data and visualize the sales pipeline using an Excel dataset.

## Dashboard Features

- Total inquiry tracking
- Weekly inquiry trend analysis
- Inquiry distribution by business vertical
- Employee-wise inquiry and activity analysis
- Quotation and proposal tracking
- ERP meeting status monitoring
- Won, Lost, and Pending deal analysis
- Pending follow-up list
- Interactive filters and CSV export

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- Excel

## Dashboard Preview

_Add a screenshot of the running dashboard here._

## Project Structure

```text
CRM-Inquiry-Dashboard/
├── app.py
├── requirements.txt
├── README.md
└── Aiitech_Inquiry_Tracking_Sample_60.xlsx
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Reniya-00/CRM-Inquiry-Dashboard.git
cd CRM-Inquiry-Dashboard
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Data

The repository currently uses fictional sample inquiry data for demonstration.

The dashboard supports uploading an Excel workbook containing inquiry information. ERP integration is a potential future enhancement and is not implemented in this demo.

## Future Enhancements

- Connect to an approved ERP data source
- Automate inquiry updates
- Add AI-assisted inquiry classification
- Generate follow-up recommendations
- Add automated weekly CRM summaries

## Author

Developed as a CRM analytics and dashboard project using Python and Streamlit.
