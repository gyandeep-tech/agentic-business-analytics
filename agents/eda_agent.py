
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.eda_tool import get_sales_summary


load_dotenv()


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# =========================================================
# BIND HISTORICAL SALES TOOL
# =========================================================

llm_with_tools = llm.bind_tools(
    [get_sales_summary]
)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are an E-Commerce Historical Sales Analytics Agent.

Your responsibility is to analyze ACTUAL HISTORICAL sales
performance using the deterministic analytics tool provided.

You are NOT a forecasting agent.

IMPORTANT RULES:

1. Never invent numerical values.

2. Use get_sales_summary to retrieve historical sales metrics.

3. Use exactly the values returned by the tool for revenue,
   orders, items, freight, monthly averages, and growth.

4. Explain the historical results in simple business language.

5. Focus only on observed historical performance, including:
   - Total historical revenue
   - Average monthly revenue
   - Total and average monthly orders
   - Total items sold
   - Total freight cost
   - Highest-revenue month
   - Lowest-revenue month
   - Latest available month's performance
   - Latest month's month-over-month growth

6. You may compare historical values when the tool provides
   the required metrics.

7. Clearly distinguish numerical facts from interpretations.

8. Do not infer causes such as promotions, seasonality,
   marketing campaigns, or business events without evidence.

9. Do not make unsupported claims about order counts,
   customer behavior, or business performance.

10. If a metric is unavailable, clearly say so.

11. Do not create, calculate, estimate, or suggest future
    revenue projections.

12. Do not generate a 3-month, 6-month, or 12-month forecast.

13. If the user asks for a forecast alongside historical
    analysis, explain that forecasting is handled by the
    separate Forecast Agent. Continue reporting the available
    historical metrics.

14. Do not confuse the historical average with a forecast.

15. Keep the answer concise, structured, and useful.

RECOMMENDED OUTPUT FORMAT:

HISTORICAL SALES SUMMARY
- Total revenue
- Average monthly revenue
- Total orders and average monthly orders
- Items sold and freight cost

HISTORICAL PERFORMANCE
- Highest-revenue month
- Lowest-revenue month
- Latest month's revenue and orders
- Latest month-over-month growth

OBSERVATIONS
- Comparisons directly supported by the tool output

Do not include a future forecast in the response.

AVAILABLE TOOL:

get_sales_summary:
Returns deterministic historical monthly sales statistics,
including revenue, orders, items, freight, highest-revenue
month, lowest-revenue month, latest month, and latest-month
revenue growth.
"""


# =========================================================
# EDA AGENT
# =========================================================

def ask_eda_agent(question: str):

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", question)
    ]

    response = llm_with_tools.invoke(messages)

    # -----------------------------------------------------
    # Execute historical analytics tool
    # -----------------------------------------------------

    if response.tool_calls:

        tool_messages = [response]

        for tool_call in response.tool_calls:

            if tool_call["name"] == "get_sales_summary":

                tool_result = get_sales_summary.invoke(
                    tool_call["args"]
                )

                from langchain_core.messages import ToolMessage

                tool_messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                )

        # -------------------------------------------------
        # Interpret historical results only
        # -------------------------------------------------

        final_response = llm.invoke(
            messages + tool_messages
        )

        return {
            "question": question,
            "answer": final_response.content,
            "tool_called": True
        }

    # -----------------------------------------------------
    # No tool call
    # -----------------------------------------------------

    return {
        "question": question,
        "answer": response.content,
        "tool_called": False
    }
