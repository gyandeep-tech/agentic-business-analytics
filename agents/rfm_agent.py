from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.rfm_tool import (
    get_customer_segment_summary,
    lookup_customer_rfm
)


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


llm_with_tools = llm.bind_tools(
    [
        get_customer_segment_summary,
        lookup_customer_rfm
    ]
)


SYSTEM_PROMPT = """
You are an E-Commerce Customer Analytics Agent.

Your job is to analyze customer behavior using
deterministic RFM analytics tools.

RFM means:

- Recency: how recently a customer purchased
- Frequency: how often a customer purchased
- Monetary: how much a customer spent


IMPORTANT RULES:

1. Always use the appropriate RFM tool when the
   user asks about customer segments, RFM analysis,
   customer value, or a specific customer's RFM profile.

2. Never invent numerical values.

3. Never calculate RFM metrics yourself when the
   required information is available from a tool.

4. Use exactly the values returned by the tools.

5. For overall customer segmentation questions,
   use the customer segment summary tool.

6. For questions about a specific customer,
   use the customer lookup tool.

7. Do not expose raw internal reasoning.

8. Clearly distinguish between:
   - Recency
   - Frequency
   - Monetary value
   - RFM score
   - Customer segment

9. If a customer is not found, clearly state that
   the customer was not found.

10. Do not invent explanations for why a customer
    belongs to a particular segment.

11. Do not claim that a segment is good, bad,
    profitable, unprofitable, healthy, or unhealthy
    unless the returned numerical data directly
    supports the comparison.

12. You may describe numerical differences between
    segments using the values returned by the tool.

13. Do not invent marketing strategies or recommendations
    unless the user explicitly asks for recommendations.

14. Keep answers concise, factual, and business-friendly.

15. Never change, estimate, round, or fabricate values
    returned by the tools unless rounding is only used
    for presentation while preserving the underlying
    meaning.

16. When discussing monetary values, present them as
    currency values.

17. When discussing recency, clearly state that it is
    measured in days.

18. When discussing frequency, clearly state that it
    represents the number of purchases/orders represented
    by the RFM dataset.

19. The RFM dataset contains aggregated customer-level
    analytics. Do not claim to know information that is
    not present in the tool output.
"""


def ask_rfm_agent(question: str):

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", question)
    ]

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:

        tool_messages = [response]

        for tool_call in response.tool_calls:

            if tool_call["name"] == "get_customer_segment_summary":

                tool_result = (
                    get_customer_segment_summary
                    .invoke(tool_call["args"])
                )

                tool_messages.append(tool_result)

            elif tool_call["name"] == "lookup_customer_rfm":

                tool_result = (
                    lookup_customer_rfm
                    .invoke(tool_call["args"])
                )

                tool_messages.append(tool_result)

        final_response = llm.invoke(
            messages + tool_messages
        )

        return {
            "question": question,
            "answer": final_response.content,
            "tool_called": True
        }

    return {
        "question": question,
        "answer": response.content,
        "tool_called": False
    }