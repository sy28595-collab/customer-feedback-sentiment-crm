import streamlit as st

from src.database import (
    create_tables,
    save_customer,
    save_feedback
)

from src.sentiment import analyze_sentiment


# ---------------------------------
# Database initialization
# ---------------------------------

create_tables()


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="Customer Feedback",
    page_icon="💬",
    layout="centered"
)


# ---------------------------------
# Custom CSS
# ---------------------------------

st.markdown("""
<style>

.stApp {
    background: #F5F0E8;
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #2B2723;
    margin: 0 0 4px 0;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #756B61;
    margin-bottom: 18px;
}

.question {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    color: #3A332C;
    margin-bottom: 8px;
}

div[data-testid="stTextInput"] label p,
div[data-testid="stTextArea"] label p {
    color: #5A5047 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    color: #F5F0E8 !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #B9B1A7 !important;
    opacity: 1 !important;
}

div.stButton > button {
    height: 78px;
    border-radius: 18px;
    border: 1px solid #DDD5C8;
    background: #FFFDF8;
    color: #2C2925;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #E9DFD0;
    border-color: #8B7A65;
    transform: translateY(-2px);
}

div.stButton > button[kind="primary"] {
    height: 44px;
    border-radius: 23px;
    background: #2C2925;
    color: white;
    border: none;
    font-size: 15px;
}

div.stButton > button[kind="primary"]:hover {
    background: #45403A;
}

.success-card {
    background: #FFFDF8;
    border: 1px solid #DDD5C8;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin-top: 15px;
}

.success-icon {
    font-size: 28px;
    color: #5E7655;
}

.success-title {
    font-size: 20px;
    font-weight: 600;
    color: #2C2925;
}

.success-text {
    color: #746F68;
    font-size: 14px;
    margin-top: 4px;
}

.footer {
    text-align: center;
    color: #746F68;
    font-size: 12px;
    margin-top: 10px;
}

@media (max-width: 700px) {

    .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 27px;
    }

    .subtitle {
        font-size: 13px;
        margin-bottom: 15px;
    }

    .question {
        font-size: 17px;
    }

    div.stButton > button {
        height: 70px;
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# Page Header
# ---------------------------------

st.markdown(
    '<div class="main-title">We’d love to hear from you.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your feedback helps us create a better experience.</div>',
    unsafe_allow_html=True
)


# ---------------------------------
# Main Layout
# ---------------------------------

left_col, right_col = st.columns(
    [1, 1.15],
    gap="large"
)


# ---------------------------------
# Customer Details
# ---------------------------------

with left_col:

    st.markdown(
        '<div class="question">Customer Details</div>',
        unsafe_allow_html=True
    )

    customer_id = st.text_input(
        "Customer ID",
        placeholder="Customer ID"
    )

    name = st.text_input(
        "Name",
        placeholder="Customer name"
    )

    email = st.text_input(
        "Email (Optional)",
        placeholder="Email (optional)"
    )

    phone = st.text_input(
        "Phone (Optional)",
        placeholder="Phone (optional)"
    )


# ---------------------------------
# Feedback Section
# ---------------------------------

with right_col:

    st.markdown(
        '<div class="question">How was your experience?</div>',
        unsafe_allow_html=True
    )

    emoji_options = {
        "😞": "Not great",
        "😐": "Okay",
        "😊": "Great"
    }

    # Default emoji
    if "selected_emoji" not in st.session_state:
        st.session_state.selected_emoji = "😊"

    cols = st.columns(3)

    for col, (emoji, label) in zip(
        cols,
        emoji_options.items()
    ):

        with col:

            if st.button(
                f"{emoji}\n\n{label}",
                key=f"emoji_{emoji}",
                use_container_width=True
            ):

                st.session_state.selected_emoji = emoji
                st.rerun()

    st.markdown(
        f"""
        <div style="
            text-align:center;
            color:#746F68;
            font-size:13px;
            margin-top:5px;
        ">
            Selected: {emoji_options[st.session_state.selected_emoji]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            font-size:16px;
            font-weight:700;
            color:#3A332C;
            margin-top:10px;
            margin-bottom:5px;
        ">
            Tell us more about your experience
        </div>
        """,
        unsafe_allow_html=True
    )

    review = st.text_area(
        "Review",
        placeholder="Share your thoughts...",
        height=90,
        max_chars=500,
        label_visibility="collapsed"
    )

    submit = st.button(
        "Submit Feedback →",
        type="primary",
        use_container_width=True
    )


# ---------------------------------
# Submit Feedback
# ---------------------------------

if submit:

    customer_id = customer_id.strip()
    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    review = review.strip()

    selected_emoji = st.session_state.selected_emoji


    # ---------------------------------
    # Validation
    # ---------------------------------

    if not customer_id:

        st.warning("Please enter Customer ID.")

    elif not name:

        st.warning("Please enter customer name.")

    else:

        # ---------------------------------
        # Emoji Sentiment Mapping
        # ---------------------------------

        emoji_sentiment = {
            "😊": ("Positive", 1.0),
            "😐": ("Neutral", 0.0),
            "😞": ("Negative", -1.0)
        }


        # ---------------------------------
        # Sentiment Analysis
        # ---------------------------------

        if review:

            # Written feedback
            # → VADER
            sentiment, score = analyze_sentiment(review)

        else:

            # Emoji-only feedback
            # → Emoji sentiment
            sentiment, score = emoji_sentiment[
                selected_emoji
            ]


        # ---------------------------------
        # Save Customer
        # ---------------------------------

        save_customer(
            customer_id,
            name,
            email or None,
            phone or None
        )


        # ---------------------------------
        # Save Feedback
        # ---------------------------------

        save_feedback(
            customer_id,
            review if review else selected_emoji,
            sentiment,
            score,
            selected_emoji
        )


        # ---------------------------------
        # Success Message
        # ---------------------------------

        st.markdown(
            """
            <div class="success-card">
                <div class="success-icon">✓</div>
                <div class="success-title">Thank you.</div>
                <div class="success-text">
                    Your feedback has been received.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------
# Footer
# ---------------------------------

st.markdown(
    '<div class="footer">Every piece of feedback helps us improve.</div>',
    unsafe_allow_html=True
)