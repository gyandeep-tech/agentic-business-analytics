import json

from langchain_core.tools import tool

from analytics.eda_tools import get_monthly_sales_summary


@tool
def get_sales_summary() -> str:
    """
    Analyze monthly e-commerce sales performance.

    Returns:
    - Total number of months
    - Total revenue
    - Average monthly revenue
    - Total orders
    - Average monthly orders
    - Total items
    - Total freight
    - Highest revenue month
    - Lowest revenue month
    - Latest month performance
    - Latest month revenue growth percentage

    This tool performs deterministic calculations using
    the processed monthly sales dataset.
    """

    result = get_monthly_sales_summary()

    return json.dumps(
        result,
        default=str
    )

