from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.sql_tools import execute_query


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# GROQ LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# =========================================================
# DATABASE SCHEMA
# =========================================================

SCHEMA = """
Database: agentic_analytics

TABLE: orders
Columns:
- order_id
- customer_id
- order_status
- order_purchase_timestamp
- order_approved_at
- order_delivered_carrier_date
- order_delivered_customer_date
- order_estimated_delivery_date
- delivery_days
- delivery_delay_days
- is_late
- product_revenue
- freight_cost
- total_items
- total_order_value
- order_year
- order_month
- order_month_name
- order_quarter
- order_day
- order_day_of_week


TABLE: customers
Columns:
- customer_id
- customer_unique_id
- customer_zip_code_prefix
- customer_city
- customer_state


TABLE: order_items
Columns:
- order_id
- order_item_id
- product_id
- seller_id
- shipping_limit_date
- price
- freight_value


TABLE: products
Columns:
- product_id
- product_category_name
- product_name_lenght
- product_description_lenght
- product_photos_qty
- product_weight_g
- product_length_cm
- product_height_cm
- product_width_cm
- product_category_name_english
- product_category


TABLE: sellers
Columns:
- seller_id
- seller_zip_code_prefix
- seller_city
- seller_state


TABLE: payments
Columns:
- order_id
- payment_sequential
- payment_type
- payment_installments
- payment_value


TABLE: reviews
Columns:
- review_id
- order_id
- review_score
- review_comment_title
- review_comment_message
- review_creation_date
- review_answer_timestamp


IMPORTANT BUSINESS RULES:

1. Only generate SELECT or WITH queries.

2. Never modify database data.

3. For completed-order revenue, normally use:
   order_status = 'delivered'

4. For order-level revenue:
   use orders.total_order_value

5. For product-level revenue:
   use order_items.price

6. For freight revenue/cost:
   use order_items.freight_value or orders.freight_cost
   depending on the level of analysis.

7. For delivery time:
   use orders.delivery_days

8. delivery_days is measured in DAYS.

9. For late orders:
   use:
   is_late = 1

10. For customer-state analysis:
    join customers with orders using:
    customers.customer_id = orders.customer_id

11. For product-category analysis:
    join order_items with products using:
    order_items.product_id = products.product_id

12. For seller analysis:
    join order_items with sellers using:
    order_items.seller_id = sellers.seller_id

13. Do not invent tables or columns.

14. Use LIMIT when the question asks for top/bottom N results.

15. Return only SQL when generating a SQL query.
"""


# =========================================================
# SQL GENERATION
# =========================================================

def generate_sql(question: str) -> str:
    """
    Convert a natural-language business question
    into a MySQL SELECT query.
    """

    prompt = f"""
You are a SQL Business Analyst working with a MySQL
e-commerce analytics database.

Your task is to convert the user's business question
into a correct SQL query.

DATABASE SCHEMA:
{SCHEMA}

USER QUESTION:
{question}

Rules:
- Generate ONLY SQL.
- Do not use markdown.
- Do not explain the SQL.
- Only SELECT or WITH queries are allowed.
- Do not modify the database.
- Do not invent columns or tables.
- Use the business rules provided above.

SQL:
"""

    response = llm.invoke(prompt)

    sql = response.content.strip()

    # Remove accidental markdown code fences
    sql = sql.replace("```sql", "")
    sql = sql.replace("```mysql", "")
    sql = sql.replace("```", "")

    return sql.strip()


# =========================================================
# SQL VALIDATION
# =========================================================

def validate_sql(sql: str) -> bool:
    """
    Perform basic safety validation before SQL execution.
    """

    if not sql:
        return False

    sql = sql.strip()

    # -----------------------------------------
    # Remove one trailing semicolon
    # -----------------------------------------

    if sql.endswith(";"):
        sql = sql[:-1].strip()

    # -----------------------------------------
    # Prevent multiple SQL statements
    # -----------------------------------------

    if ";" in sql:
        return False

    # -----------------------------------------
    # Must start with SELECT or WITH
    # -----------------------------------------

    upper_sql = sql.upper()

    if not (
        upper_sql.startswith("SELECT")
        or upper_sql.startswith("WITH")
    ):
        return False

    # -----------------------------------------
    # Block dangerous SQL operations
    # -----------------------------------------

    forbidden_keywords = [
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

    import re

    for keyword in forbidden_keywords:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, upper_sql):
            return False

    return True


# =========================================================
# SQL RETRY / CORRECTION
# =========================================================

def regenerate_sql(
    question: str,
    previous_sql: str,
    error_message: str
) -> str:
    """
    Ask the LLM to correct SQL after a validation
    or database execution error.
    """

    prompt = f"""
You are an expert MySQL Business Analyst.

The following SQL query was generated for a business question,
but it could not be executed successfully.

DATABASE SCHEMA:
{SCHEMA}

USER QUESTION:
{question}

PREVIOUS SQL:
{previous_sql}

ERROR:
{error_message}

Generate a corrected SQL query.

Rules:
- Return ONLY SQL.
- Use only SELECT or WITH.
- Do not modify the database.
- Do not invent tables or columns.
- Follow the database schema.
- Follow the business rules.
- Do not include markdown.

CORRECTED SQL:
"""

    response = llm.invoke(prompt)

    sql = response.content.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```mysql", "")
    sql = sql.replace("```", "")

    return sql.strip()


# =========================================================
# BUSINESS ANSWER GENERATION
# =========================================================

def generate_business_answer(
    question: str,
    result: dict
) -> str:
    """
    Convert database results into a concise
    business-friendly answer.
    """

    prompt = f"""
You are a Business Analyst.

Answer the user's question using ONLY the database result.

USER QUESTION:
{question}

DATABASE RESULT:
{result}

Rules:
- Do not invent numbers.
- Use the exact values from the database result.
- Be concise and business-friendly.
- Use appropriate units.
- delivery_days means DAYS.
- Revenue should be presented as a monetary value.
- If there are multiple rows, summarize them clearly.
- If appropriate, use a small Markdown table.
"""

    response = llm.invoke(prompt)

    return response.content.strip()


# =========================================================
# MAIN SQL BUSINESS ANALYST AGENT
# =========================================================

def ask_business_question(question: str):
    """
    Main entry point for the SQL Business Analyst Agent.

    Flow:

    User Question
          ↓
    Generate SQL
          ↓
    Validate SQL
          ↓
    Execute SQL
          ↓
    Retry if necessary
          ↓
    Generate Business Answer
    """

    if not question or not question.strip():
        raise ValueError(
            "Business question cannot be empty."
        )

    print("\nUser Question:")
    print(question)

    max_attempts = 3

    sql = None
    result = None

    # =====================================================
    # SQL GENERATION + EXECUTION LOOP
    # =====================================================

    for attempt in range(1, max_attempts + 1):

        print(
            f"\nSQL Generation Attempt: {attempt}"
        )

        # ---------------------------------------------
        # First attempt
        # ---------------------------------------------

        if attempt == 1:

            sql = generate_sql(question)

        # ---------------------------------------------
        # Retry attempt
        # ---------------------------------------------

        else:

            sql = regenerate_sql(
                question=question,
                previous_sql=sql,
                error_message=error_message
            )

        print("\nGenerated SQL:")
        print(sql)

        # ---------------------------------------------
        # Validate SQL
        # ---------------------------------------------

        if not validate_sql(sql):

            error_message = (
                "Generated SQL failed the safety validation."
            )

            print(
                "\nSQL Validation Error:"
            )

            print(error_message)

            if attempt == max_attempts:
                raise ValueError(
                    "Unable to generate a safe SQL query "
                    "after multiple attempts."
                )

            continue

        # ---------------------------------------------
        # Execute SQL
        # ---------------------------------------------

        try:

            result = execute_query(sql)

            print("\nQuery Result:")
            print(result)

            break

        except Exception as error:

            error_message = str(error)

            print("\nSQL Execution Error:")
            print(error_message)

            if attempt == max_attempts:
                raise RuntimeError(
                    "SQL execution failed after "
                    "multiple attempts."
                ) from error

    # =====================================================
    # GENERATE FINAL BUSINESS ANSWER
    # =====================================================

    answer = generate_business_answer(
        question=question,
        result=result
    )

    print("\nFinal Answer:")
    print(answer)

    # =====================================================
    # RETURN STRUCTURED RESPONSE
    # =====================================================

    return {
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer
    }