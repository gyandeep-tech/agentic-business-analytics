import json

from langchain_core.tools import tool

from analytics.rfm_tools import (
    get_rfm_summary,
    get_customer_rfm
)


@tool
def get_customer_segment_summary() -> str:
    """
    Analyze overall customer RFM segmentation.

    Returns:
    - Total customers
    - Total monetary value
    - Average monetary value
    - Average recency
    - Average frequency
    - Largest customer segment
    - Highest average monetary segment
    - Segment-level statistics

    This tool performs deterministic RFM analysis.
    """

    result = get_rfm_summary()

    return json.dumps(
        result,
        default=str
    )


@tool
def lookup_customer_rfm(customer_unique_id: str) -> str:
    """
    Look up RFM information for a specific customer.

    Returns:
    - Customer ID
    - Recency
    - Frequency
    - Monetary value
    - RFM score
    - Customer segment

    Use this tool when the user asks about a
    specific customer.
    """

    result = get_customer_rfm(
        customer_unique_id
    )

    return json.dumps(
        result,
        default=str
    )