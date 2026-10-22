import json

from langchain_core.tools import tool

from analytics.sql_tools import execute_query


@tool
def execute_sql(sql: str) -> str:
    """
    Execute a read-only SQL query against the
    agentic_analytics MySQL database.

    Returns the query result as JSON so the LLM
    receives a clean and structured response.
    """

    result = execute_query(sql)

    return json.dumps(
        result,
        default=str
    )