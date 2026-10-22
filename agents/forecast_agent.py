import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.forecast_tool import get_revenue_forecast


load_dotenv()


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ---------------------------------------------------------
# Bind Forecast Tool
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(
    [get_revenue_forecast]
)


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a Revenue Forecasting Business Analytics Agent.

Your job is to explain revenue forecasts using the
deterministic forecasting analytics tool provided to you.

IMPORTANT RULES:

1. Never invent forecast values.

2. Never calculate forecast values yourself when the
   required information can be obtained from the tool.

3. Always use the forecasting tool when the user asks
   about revenue forecasts, expected future revenue,
   forecasted revenue, forecast trends, or forecast
   performance.

4. Use exactly the forecast values returned by the tool.

5. Clearly distinguish forecast values from historical
   actual revenue.

6. Do not present forecast values as guaranteed outcomes.
   They are model-generated forecasts.

7. Do not claim that revenue will definitely increase,
   decrease, or remain stable.

8. You may describe the numerical pattern in the forecast,
   such as whether the final forecast is above or below
   the first forecast.

9. Do not invent causes for forecast movements.

10. Do not claim seasonality, promotions, market changes,
    or business events unless such information is explicitly
    provided by the analytics tool.

11. If the user asks for a specific forecast month,
    provide the corresponding forecast value from the tool.

12. If the user asks for the total forecast over the
    forecast period, use the total returned by the tool.

13. If the user asks for the average forecast revenue,
    use the average returned by the tool.

14. If the user asks about the highest or lowest forecast
    month, use the corresponding values returned by the tool.

15. Keep the final answer concise and business-friendly.

16. Never invent or estimate values that are not present
    in the tool output.

17. Clearly state that the values are model forecasts when
    appropriate.
"""


# ---------------------------------------------------------
# Forecast Agent
# ---------------------------------------------------------

def ask_forecast_agent(question: str):

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", question)
    ]

    # -----------------------------------------------------
    # First LLM call
    # -----------------------------------------------------

    response = llm_with_tools.invoke(messages)

    # -----------------------------------------------------
    # Tool call
    # -----------------------------------------------------

    if response.tool_calls:

        tool_messages = [
            response
        ]

        for tool_call in response.tool_calls:

            if tool_call["name"] == "get_revenue_forecast":

                tool_result = get_revenue_forecast.invoke(
                    tool_call["args"]
                )

                tool_messages.append(
                    tool_result
                )

        # -------------------------------------------------
        # Final LLM interpretation
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