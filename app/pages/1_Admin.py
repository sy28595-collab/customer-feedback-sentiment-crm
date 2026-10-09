import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from src.database import (
    create_tables,
    get_feedback_summary,
    get_total_customers,
    get_all_feedback,
    get_customer_details,
    get_customer_history
)

# Database
create_tables()

# Page Configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    background: #F5F0E8;
}
.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #2B2723;
    margin-bottom: 4px;
}
.subtitle {
    font-size: 14px;
    color: #756B61;
    margin-bottom: 25px;
}
.metric-card {
    background: #FFFDF8;
    border: 1px solid #DDD5C8;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}
.metric-title {
    color: #756B61;
    font-size: 13px;
    font-weight: 600;
}
.metric-value {
    color: #2C2925;
    font-size: 28px;
    font-weight: 700;
    margin-top: 5px;
}
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #3A332C;
    margin-top: 25px;
    margin-bottom: 12px;
}
.customer-card {
    background: #FFFDF8;
    border: 1px solid #DDD5C8;
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
}
.customer-name {
    font-size: 20px;
    font-weight: 700;
    color: #2C2925;
}
.customer-info {
    color: #756B61;
    font-size: 14px;
    margin-top: 5px;
}
.history-card {
    background: #FFFDF8;
    border: 1px solid #DDD5C8;
    border-radius: 14px;
    padding: 16px;
    margin-top: 10px;
}
.history-review {
    color: #3A332C;
    font-size: 15px;
    margin-bottom: 8px;
    line-height: 1.5;
}
.history-meta {
    color: #756B61;
    font-size: 13px;
    line-height: 1.6;
}
.sentiment-container {
    background: #FFFDF8;
    border: 1px solid #DDD5C8;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 20px;
}
.sentiment-row {
    margin-bottom: 16px;
}
.sentiment-row:last-child {
    margin-bottom: 0;
}
.sentiment-label {
    display: flex;
    justify-content: space-between;
    color: #3A332C;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 6px;
}
.progress-background {
    width: 100%;
    height: 9px;
    background: #E8E1D7;
    border-radius: 10px;
    overflow: hidden;
}
.progress-positive {
    height: 100%;
    background: #6F8F68;
    border-radius: 10px;
}
.progress-neutral {
    height: 100%;
    background: #B49A68;
    border-radius: 10px;
}
.progress-negative {
    height: 100%;
    background: #A56B62;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">Admin Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Customer feedback and sentiment overview.</div>',
    unsafe_allow_html=True
)

# Summary
summary = get_feedback_summary()
total_feedback = summary[0] or 0
positive = summary[1] or 0
negative = summary[2] or 0
neutral = summary[3] or 0
total_customers = get_total_customers()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Customers</div><div class="metric-value">{total_customers}</div></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Feedback</div><div class="metric-value">{total_feedback}</div></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Positive</div><div class="metric-value">{positive}</div></div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Neutral</div><div class="metric-value">{neutral}</div></div>',
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Negative</div><div class="metric-value">{negative}</div></div>',
        unsafe_allow_html=True
    )

# Customer Search
st.markdown(
    '<div class="section-title">Customer Search</div>',
    unsafe_allow_html=True
)

with st.form("customer_search_form"):
    search_col, button_col = st.columns([4, 1])
    with search_col:
        customer_id = st.text_input(
            "Customer ID",
            placeholder="Enter Customer ID",
            label_visibility="collapsed"
        )
    with button_col:
        search_button = st.form_submit_button(
            "Search",
            use_container_width=True
        )

# Customer Search Result
if search_button:
    customer_id = customer_id.strip()
    if not customer_id:
        st.warning("Please enter Customer ID.")
    else:
        customer = get_customer_details(customer_id)
        if not customer:
            st.warning("Customer not found.")
        else:
            customer_id_value = customer[0]
            customer_name = customer[1]
            email = customer[2]
            phone = customer[3]
            created_date = customer[4]
            st.markdown(
                f'<div class="customer-card"><div class="customer-name">{customer_name}</div><div class="customer-info">Customer ID: {customer_id_value}</div><div class="customer-info">Email: {email or "Not provided"}</div><div class="customer-info">Phone: {phone or "Not provided"}</div><div class="customer-info">Customer Since: {created_date}</div></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="section-title">Customer History</div>',
                unsafe_allow_html=True
            )
            history = get_customer_history(customer_id_value)
            if not history:
                st.info("No feedback history found.")
            else:
                for feedback in history:
                    feedback_id = feedback[0]
                    review = feedback[1]
                    sentiment = feedback[2]
                    score = feedback[3]
                    rating = feedback[4]
                    date = feedback[5]
                    st.markdown(
                        f'<div class="history-card"><div class="history-review">{review}</div><div class="history-meta">Feedback #{feedback_id} | Sentiment: {sentiment} | Score: {score} | Rating: {rating or "N/A"} | Date: {date}</div></div>',
                        unsafe_allow_html=True
                    )

# Sentiment Distribution
st.markdown(
    '<div class="section-title">Sentiment Distribution</div>',
    unsafe_allow_html=True
)

if total_feedback > 0:
    positive_percent = round((positive / total_feedback) * 100)
    neutral_percent = round((neutral / total_feedback) * 100)
    negative_percent = round((negative / total_feedback) * 100)
    st.markdown(
        f"""
        <div class="sentiment-container">
            <div class="sentiment-row">
                <div class="sentiment-label">
                    <span>😊 Positive</span>
                    <span>{positive} ({positive_percent}%)</span>
                </div>
                <div class="progress-background">
                    <div class="progress-positive" style="width:{positive_percent}%;"></div>
                </div>
            </div>
            <div class="sentiment-row">
                <div class="sentiment-label">
                    <span>😐 Neutral</span>
                    <span>{neutral} ({neutral_percent}%)</span>
                </div>
                <div class="progress-background">
                    <div class="progress-neutral" style="width:{neutral_percent}%;"></div>
                </div>
            </div>
            <div class="sentiment-row">
                <div class="sentiment-label">
                    <span>😞 Negative</span>
                    <span>{negative} ({negative_percent}%)</span>
                </div>
                <div class="progress-background">
                    <div class="progress-negative" style="width:{negative_percent}%;"></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("No sentiment data available yet.")

# Recent Feedback
st.markdown(
    '<div class="section-title">Recent Feedback</div>',
    unsafe_allow_html=True
)

all_feedback = get_all_feedback()

if all_feedback:
    for feedback in all_feedback[:50]:
        feedback_id = feedback[0]
        customer_id_value = feedback[1]
        customer_name = feedback[2] or "Unknown"
        review = feedback[3]
        sentiment = feedback[4]
        score = feedback[5]
        rating = feedback[6]
        date = feedback[7]
        st.markdown(
            f'<div class="history-card"><div class="history-review">{review}</div><div class="history-meta">ID: {customer_id_value} | Customer: {customer_name} | Sentiment: {sentiment} | Score: {score} | Rating: {rating or "N/A"} | Date: {date}</div></div>',
            unsafe_allow_html=True
        )
else:
    st.info("No feedback available yet.")