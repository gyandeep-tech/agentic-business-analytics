from analytics.sql_tools import execute_query


query = """
SELECT
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered';
"""

result = execute_query(query)

print(result)






# run : python -m tests.test_sql_tool