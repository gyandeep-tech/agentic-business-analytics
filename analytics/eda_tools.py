
import os
import pandas as pd


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MONTHLY_SALES_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "monthly_sales.csv"
)


# =========================================================
# LOAD MONTHLY SALES
# =========================================================

def load_monthly_sales():
    """
    Load the processed monthly sales dataset.
    """

    if not os.path.exists(MONTHLY_SALES_PATH):
        raise FileNotFoundError(
            f"Monthly sales file not found: {MONTHLY_SALES_PATH}"
        )

    df = pd.read_csv(MONTHLY_SALES_PATH)

    if df.empty:
        raise ValueError(
            "monthly_sales.csv is empty."
        )

    # Convert date column
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    return df


# =========================================================
# MONTHLY SALES SUMMARY
# =========================================================

def get_monthly_sales_summary():
    """
    Generate deterministic summary statistics
    from monthly_sales.csv.
    """

    df = load_monthly_sales()

    # -----------------------------------------------------
    # Basic validation
    # -----------------------------------------------------

    required_columns = [
        "order_year",
        "order_month",
        "revenue",
        "freight",
        "orders",
        "items",
        "date"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # -----------------------------------------------------
    # Numeric conversion
    # -----------------------------------------------------

    numeric_columns = [
        "revenue",
        "freight",
        "orders",
        "items"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=["revenue"]
    )

    # -----------------------------------------------------
    # Basic metrics
    # -----------------------------------------------------

    total_months = len(df)

    total_revenue = df["revenue"].sum()

    average_monthly_revenue = df["revenue"].mean()

    total_orders = df["orders"].sum()

    average_monthly_orders = df["orders"].mean()

    total_items = df["items"].sum()

    total_freight = df["freight"].sum()

    # -----------------------------------------------------
    # Highest revenue month
    # -----------------------------------------------------

    highest_revenue_row = df.loc[
        df["revenue"].idxmax()
    ]

    # -----------------------------------------------------
    # Lowest revenue month
    # -----------------------------------------------------

    lowest_revenue_row = df.loc[
        df["revenue"].idxmin()
    ]

    # -----------------------------------------------------
    # Revenue growth
    # -----------------------------------------------------

    df = df.sort_values("date").copy()

    df["revenue_growth_pct"] = (
        df["revenue"]
        .pct_change()
        .mul(100)
    )

    # -----------------------------------------------------
    # Latest month
    # -----------------------------------------------------

    latest_month = df.iloc[-1]

    # -----------------------------------------------------
    # Build result
    # -----------------------------------------------------

    summary = {

        "total_months": int(
            total_months
        ),

        "total_revenue": float(
            total_revenue
        ),

        "average_monthly_revenue": float(
            average_monthly_revenue
        ),

        "total_orders": int(
            total_orders
        ),

        "average_monthly_orders": float(
            average_monthly_orders
        ),

        "total_items": float(
            total_items
        ),

        "total_freight": float(
            total_freight
        ),

        "highest_revenue_month": {
            "date": highest_revenue_row["date"],
            "revenue": float(
                highest_revenue_row["revenue"]
            ),
            "orders": int(
                highest_revenue_row["orders"]
            )
        },

        "lowest_revenue_month": {
            "date": lowest_revenue_row["date"],
            "revenue": float(
                lowest_revenue_row["revenue"]
            ),
            "orders": int(
                lowest_revenue_row["orders"]
            )
        },

        "latest_month": {
            "date": latest_month["date"],
            "revenue": float(
                latest_month["revenue"]
            ),
            "orders": int(
                latest_month["orders"]
            )
        },

        "latest_month_growth_pct": (
            None
            if pd.isna(
                latest_month["revenue_growth_pct"]
            )
            else float(
                latest_month["revenue_growth_pct"]
            )
        )
    }

    return summary





