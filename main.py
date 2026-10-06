from src.database import (
    create_tables,
    save_customer,
    save_feedback,
    get_customer_history,
    get_feedback_summary
)

from src.sentiment import analyze_sentiment


def add_customer_feedback():
    print("\n--- Customer Feedback ---")

    customer_id = input("Customer ID: ").strip()
    name = input("Customer Name: ").strip()
    email = input("Email (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    review = input("Feedback: ").strip()

    if not customer_id:
        print("Customer ID is required.")
        return

    if not name:
        print("Customer name is required.")
        return

    if not review:
        print("Feedback is required.")
        return

    # Save or update customer
    save_customer(
        customer_id,
        name,
        email or None,
        phone or None
    )

    # Analyze sentiment
    sentiment, score = analyze_sentiment(review)

    # Save feedback
    save_feedback(
        customer_id,
        review,
        sentiment,
        score
    )

    print("\nFeedback saved successfully!")
    print("Sentiment:", sentiment)
    print("Score:", score)


def show_customer_history():
    print("\n--- Customer History ---")

    customer_id = input("Customer ID: ").strip()

    if not customer_id:
        print("Customer ID is required.")
        return

    history = get_customer_history(customer_id)

    if not history:
        print("No feedback found for this customer.")
        return

    print("\nFeedback History")
    print("-" * 40)

    for feedback in history:

        feedback_id = feedback[0]
        review = feedback[1]
        sentiment = feedback[2]
        score = feedback[3]
        rating = feedback[4]
        date = feedback[5]

        print(f"\nFeedback {feedback_id}")
        print("Review:", review)
        print("Sentiment:", sentiment)
        print("Score:", score)
        print("Date:", date)

        if rating:
            print("Rating:", rating)


def show_summary():
    print("\n--- Feedback Summary ---")

    summary = get_feedback_summary()

    total_feedback = summary[0]
    positive = summary[1] or 0
    negative = summary[2] or 0
    neutral = summary[3] or 0

    print("\nTotal Feedback:", total_feedback)
    print("Positive:", positive)
    print("Negative:", negative)
    print("Neutral:", neutral)


def main():

    # Create database tables if they don't exist
    create_tables()

    while True:

        print("\n==============================")
        print("Customer Feedback Sentiment CRM")
        print("==============================")

        print("1. Add Customer Feedback")
        print("2. Customer History")
        print("3. Feedback Summary")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            add_customer_feedback()

        elif choice == "2":

            show_customer_history()

        elif choice == "3":

            show_summary()

        elif choice == "4":

            print("Goodbye!")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()