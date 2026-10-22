from agents.sql_agent import ask_business_question


questions = [
    "What is the total revenue from delivered orders?",

    "Which customer state generated the highest revenue?",

    "What are the top 5 product categories by revenue?",

    "How many orders were delivered late?",

    "What is the average delivery time for delivered orders?"
]


for question in questions:

    result = ask_business_question(question)

    print("\n" + "=" * 70)
    print("FINAL ANSWER:")
    print(result["answer"])