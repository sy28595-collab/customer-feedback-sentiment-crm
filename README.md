# Customer Feedback Sentiment CRM

I built this project to collect customer feedback and understand whether customers are happy or unhappy with their experience.

The application uses Python and VADER to analyze written feedback. It also saves customer details and feedback in an SQLite database.

## Project Links

- Live App: https://customer-feedback-sentiment-crm-sandeep.streamlit.app/
- GitHub Repository: https://github.com/sy28595-collab/customer-feedback-sentiment-crm

## Features

- Customer feedback form
- Emoji ratings
- Positive, negative, and neutral sentiment analysis
- Customer feedback history
- Admin dashboard
- Sentiment summary and recent feedback
- SQLite database to store customer information

## Technologies Used

- Python
- Streamlit
- SQLite
- NLTK
- VADER Sentiment Analyzer

## How It Works

Customers enter their details, select an emoji rating, and can write a review.

If a customer writes a review, VADER analyzes the text and predicts its sentiment. If the customer submits only an emoji, the selected emoji determines the sentiment.

The feedback is saved in the database. The admin dashboard displays customer history and an overall summary of the feedback.

## Run Locally

First, clone the repository:

```bash
git clone https://github.com/sy28595-collab/customer-feedback-sentiment-crm.git