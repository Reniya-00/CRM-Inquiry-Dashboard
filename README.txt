Aiitech Inquiry Dashboard - Setup

1. Keep app.py and Aiitech_Inquiry_Tracking_Sample_60.xlsx in the same folder.
2. Install Python 3.10+ from https://www.python.org/downloads/ if needed.
3. Open VS Code, then File > Open Folder and select this folder.
4. Open Terminal > New Terminal.
5. Run:
   python -m pip install -r requirements.txt
6. Run:
   python -m streamlit run app.py
7. The dashboard opens in your browser. Use the sidebar filters or upload a different .xlsx file.

Excel format:
- Sheet name: Inquiries
- Required columns include Inquiry ID, Inquiry Date, Institute Name, Vertical,
  Responsible Employee, Quotation Forwarded, Proposal Submitted,
  ERP Meeting Booked, Deal Status.

Important:
- The workbook contains fictional demo data only.
- Do not upload confidential client or employee information to an unapproved system.
- ERP connection needs the company's approved API/export and access permissions.
