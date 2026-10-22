import os
import re

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


connection_url = (
    f"mysql+mysqlconnector://"
    f"{MYSQL_USER}:{MYSQL_PASSWORD}@"
    f"{MYSQL_HOST}:{MYSQL_PORT}/"
    f"{MYSQL_DATABASE}"
)

engine = create_engine(connection_url)


def execute_query(sql: str):
    """
    Execute a read-only SQL query.

    Only SELECT and WITH queries are allowed.
    """

    # -----------------------------------------
    # Clean SQL
    # -----------------------------------------

    sql = sql.strip()

    if not sql:
        raise ValueError("SQL query cannot be empty.")


    # -----------------------------------------
    # Remove trailing semicolon
    # -----------------------------------------

    sql = sql.rstrip(";").strip()


    # -----------------------------------------
    # Prevent multiple statements
    # -----------------------------------------

    if ";" in sql:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )


    # -----------------------------------------
    # Only SELECT / WITH allowed
    # -----------------------------------------

    if not re.match(
        r"^(SELECT|WITH)\b",
        sql,
        re.IGNORECASE
    ):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )


    # -----------------------------------------
    # Block dangerous SQL keywords
    # -----------------------------------------

    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "GRANT",
        "REVOKE"
    ]

    sql_upper = sql.upper()

    for keyword in forbidden:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, sql_upper):

            raise ValueError(
                f"Unsafe SQL operation detected: {keyword}"
            )


    # -----------------------------------------
    # Execute query
    # -----------------------------------------

    with engine.connect() as connection:

        result = connection.execute(
            text(sql)
        )

        rows = result.fetchall()
        columns = result.keys()


    # -----------------------------------------
    # Return structured result
    # -----------------------------------------

    return {
        "columns": list(columns),
        "rows": [list(row) for row in rows]
    }


