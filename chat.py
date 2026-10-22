
from agents.business_graph import business_graph


def main():
    print("\n" + "=" * 60)
    print("  AGENTIC AI BUSINESS ANALYTICS CHATBOT")
    print("=" * 60)
    print("Ask questions about sales, customers, forecasts, and anomalies.")
    print("Type /exit to quit.\n")

    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in {"/exit", "exit", "quit"}:
                print("Chatbot: Goodbye!")
                break

            print("\nChatbot: Analyzing your question...\n")

            result = business_graph.invoke({
                "question": question
            })

            print("-" * 60)
            print(result.get(
                "final_answer",
                "Sorry, no answer was generated."
            ))
            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\nChatbot: Goodbye!")
            break

        except Exception as error:
            print(f"\nError: {error}")
            print("Please try asking your question again.\n")


if __name__ == "__main__":
    main()
