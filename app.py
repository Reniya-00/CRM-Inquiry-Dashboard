import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Aiitech Inquiry Dashboard", page_icon="📊", layout="wide")

st.title("Aiitech | Inquiry & Deal Tracking Dashboard")
st.caption("Demo dashboard using sample inquiry data. Replace the sample workbook with approved company data when ready.")

DEFAULT_FILE = Path(__file__).with_name("Aiitech_Inquiry_Tracking_Sample_60.xlsx")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file, sheet_name="Inquiries")
    elif DEFAULT_FILE.exists():
        data = pd.read_excel(DEFAULT_FILE, sheet_name="Inquiries")
    else:
        return pd.DataFrame()
    data["Inquiry Date"] = pd.to_datetime(data["Inquiry Date"], errors="coerce")
    if "Meeting Date" in data:
        data["Meeting Date"] = pd.to_datetime(data["Meeting Date"], errors="coerce")
    return data

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload inquiry Excel (.xlsx)", type=["xlsx"])
    st.caption("The workbook must contain a sheet named 'Inquiries'.")
    st.divider()
    st.header("Filters")

df = load_data(uploaded)

if df.empty:
    st.warning("Upload an Excel workbook with an 'Inquiries' sheet to begin.")
    st.stop()

# Clean and normalize the expected fields
required = ["Inquiry ID", "Inquiry Date", "Institute Name", "Vertical",
            "Responsible Employee", "Quotation Forwarded", "Proposal Submitted",
            "ERP Meeting Booked", "Deal Status"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

with st.sidebar:
    verticals = sorted(df["Vertical"].dropna().astype(str).unique())
    employees = sorted(df["Responsible Employee"].dropna().astype(str).unique())
    outcomes = sorted(df["Deal Status"].dropna().astype(str).unique())
    selected_verticals = st.multiselect("Vertical", verticals, default=verticals)
    selected_employees = st.multiselect("Responsible employee", employees, default=employees)
    selected_outcomes = st.multiselect("Deal status", outcomes, default=outcomes)
    min_date = df["Inquiry Date"].min().date()
    max_date = df["Inquiry Date"].max().date()
    date_range = st.date_input("Inquiry date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)

filtered = df[
    df["Vertical"].astype(str).isin(selected_verticals)
    & df["Responsible Employee"].astype(str).isin(selected_employees)
    & df["Deal Status"].astype(str).isin(selected_outcomes)
].copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["Inquiry Date"].dt.date.between(start_date, end_date)
    ]

def count_yes(series):
    return series.astype(str).str.strip().str.lower().eq("yes").sum()

total = len(filtered)
won = filtered["Deal Status"].astype(str).str.strip().str.lower().eq("won").sum()
lost = filtered["Deal Status"].astype(str).str.strip().str.lower().eq("lost").sum()
pending = filtered["Deal Status"].astype(str).str.strip().str.lower().eq("pending").sum()
quotation_count = count_yes(filtered["Quotation Forwarded"])
proposal_count = count_yes(filtered["Proposal Submitted"])
meeting_count = count_yes(filtered["ERP Meeting Booked"])

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total inquiries", total)
c2.metric("Quotations sent", int(quotation_count))
c3.metric("Proposals submitted", int(proposal_count))
c4.metric("ERP meetings booked", int(meeting_count))
c5.metric("Won", int(won))
c6.metric("Pending", int(pending))

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Inquiries over time")
    if not filtered.empty:
        weekly = filtered.set_index("Inquiry Date").resample("W").size().rename("Inquiries").reset_index()
        weekly["Week"] = weekly["Inquiry Date"].dt.strftime("%d %b %Y")
        fig = px.line(weekly, x="Week", y="Inquiries", markers=True, title="Weekly inquiry volume")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Inquiry distribution by vertical")
    by_vertical = filtered.groupby("Vertical", dropna=False).size().reset_index(name="Inquiries")
    fig = px.bar(by_vertical, x="Vertical", y="Inquiries", text="Inquiries")
    fig.update_layout(xaxis_title="", yaxis_title="Inquiries")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Deal outcomes")
    outcomes_df = filtered.groupby("Deal Status", dropna=False).size().reset_index(name="Count")
    fig = px.pie(outcomes_df, names="Deal Status", values="Count", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Employee activity")
    employee_df = filtered.groupby("Responsible Employee").agg(
        Inquiries=("Inquiry ID", "count"),
        Quotations=("Quotation Forwarded", count_yes),
        Proposals=("Proposal Submitted", count_yes),
        Meetings=("ERP Meeting Booked", count_yes),
    ).reset_index()
    fig = px.bar(employee_df, x="Responsible Employee",
                 y=["Inquiries", "Quotations", "Proposals", "Meetings"],
                 barmode="group")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Follow-up list")
followups = filtered[
    filtered["Deal Status"].astype(str).str.strip().str.lower().eq("pending")
    | filtered["Quotation Forwarded"].astype(str).str.strip().str.lower().ne("yes")
    | filtered["Proposal Submitted"].astype(str).str.strip().str.lower().ne("yes")
].copy()
show_cols = [c for c in [
    "Inquiry ID", "Inquiry Date", "Institute Name", "Vertical",
    "Responsible Employee", "Quotation Forwarded", "Proposal Submitted",
    "ERP Meeting Booked", "Deal Status"
] if c in followups.columns]
st.dataframe(followups[show_cols].sort_values("Inquiry Date", ascending=False),
             use_container_width=True, hide_index=True)

st.subheader("All filtered inquiries")
st.dataframe(filtered.sort_values("Inquiry Date", ascending=False),
             use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", csv,
                   file_name="aiitech_filtered_inquiries.csv", mime="text/csv")

st.info("This is a reporting demo, not an ERP integration. The dashboard only reflects the Excel file currently loaded.")
