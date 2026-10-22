import json

from langchain_core.tools import tool

from analytics.business_insight_tools import (
    get_business_summary
)


@tool
def get_business_insight_summary() -> str:
    """
    Get a compact deterministic summary of the business.

    Includes:
    - Sales performance
    - Revenue and order metrics
    - Latest monthly performance
    - Revenue forecast
    - Detected anomalies
    - Customer RFM segmentation

    This tool provides factual analytics for the
    Insight Agent. It does not generate interpretations
    or recommendations.
    """

    result = get_business_summary()

    return json.dumps(
        result,
        default=str
    )