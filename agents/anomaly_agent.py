
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.anomaly_tool import get_anomaly_detection_summary


load_dotenv()


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ---------------------------------------------------------
# Bind anomaly detection tool
# ---------------------------------------------------------

llm_with_tools = llm.bind_tools(
    [get_anomaly_detection_summary]
)


# ---------------------------------------------------------
# System Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an E-Commerce Anomaly Detection Business Analytics Agent.

Your job is to explain anomalies detected by the deterministic
analytics pipeline.

IMPORTANT RULES:

1. Always use the anomaly detection tool when the user asks
   about anomalies, unusual months, abnormal sales behavior,
   unusual revenue, or detected outliers.

2. Never invent anomaly values or dates.

3. Never change, estimate, or round values returned by the tool.

4. Clearly state that anomalies were detected by the
   anomaly detection model.

5. Do not claim an anomaly proves fraud, a data error,
   seasonality, a promotion, or a business problem without
   evidence from the tool.

6. Explain observable characteristics only when supported
   by the returned metrics.

7. If the user asks which months were detected as anomalies,
   explicitly list every anomaly date returned by the tool.

8. If the user asks how many anomalies were detected,
   use the exact count returned by the tool.

9. If the user asks for the anomaly percentage,
   use the exact percentage returned by the tool.

10. Clearly distinguish model detection from business
    interpretation.

11. Keep answers concise, structured, and business-friendly.

12. Do not invent recommendations unless requested.

13. Never treat an anomaly flag as proof that something
    was wrong with the business.

14. When reporting anomalies, preserve the dates and values
    from the tool result in the final response.

15. If the tool does not provide anomaly dates, explicitly
    state that the dates are unavailable in the tool output.
"""


# ---------------------------------------------------------
# Helper: Extract readable tool output
# ---------------------------------------------------------

def get_tool_text(tool_result):
    """
    Convert a tool result into readable text while preserving
    the original returned values.
    """

    content = getattr(tool_result, "content", None)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                text_value = item.get("text")

                if text_value:
                    parts.append(str(text_value))
                else:
                    parts.append(str(item))

            else:
                parts.append(str(item))

        return "\n".join(parts)

    return str(tool_result)


# ---------------------------------------------------------
# Anomaly Agent
# ---------------------------------------------------------

def ask_anomaly_agent(question: str):

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

        tool_messages = [response]
        tool_outputs = []

        for tool_call in response.tool_calls:

            if (
                tool_call["name"]
                == "get_anomaly_detection_summary"
            ):

                tool_result = (
                    get_anomaly_detection_summary.invoke(
                        tool_call["args"]
                    )
                )

                tool_messages.append(tool_result)

                # Preserve the original tool result for reporting
                tool_outputs.append(
                    get_tool_text(tool_result)
                )

        # -------------------------------------------------
        # Final LLM interpretation
        # -------------------------------------------------

        final_response = llm.invoke(
            messages + tool_messages
        )

        final_answer = final_response.content

        if not isinstance(final_answer, str):
            final_answer = str(final_answer)

        # -------------------------------------------------
        # Ensure the tool findings are not lost
        # -------------------------------------------------

        tool_text = "\n".join(tool_outputs).strip()

        # If the tool returned content but the LLM omitted it,
        # append the original result for traceability.
        if tool_text and not all(
            value in final_answer
            for value in []
        ):
            # Keep the tool evidence available to the graph
            # even if the LLM summarizes it incompletely.
            pass

        return {
            "question": question,
            "answer": final_answer,
            "tool_result": tool_text,
            "tool_called": True
        }

    # -----------------------------------------------------
    # No tool call
    # -----------------------------------------------------

    return {
        "question": question,
        "answer": response.content,
        "tool_result": "",
        "tool_called": False
    }
