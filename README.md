# Agentic AI Business Analytics Platform (AIBA)

An AI-powered business analytics platform that helps users understand business performance, analyze sales data, identify unusual trends, forecast revenue, and generate actionable insights using natural language.

## 📌 Project Overview

Businesses generate large amounts of data, but extracting useful insights often requires technical skills in SQL, Python, data analysis, and visualization.

The **Agentic AI Business Analytics Platform (AIBA)** aims to simplify this process by combining traditional data analytics with AI agents.

Instead of manually writing SQL queries or running separate analysis scripts, users can ask business questions in simple English through an interactive Streamlit dashboard. The system identifies the appropriate analytical task, executes the relevant tools, and uses an AI model to present the results in an understandable format.

For example, users can ask:
- What is the total revenue?
- Which customer segments are most valuable?
- How are monthly sales changing?
- Which months contain unusual sales patterns?
- What business actions could improve performance?

The platform combines SQL-based analysis, Python analytics, forecasting, anomaly detection, customer segmentation, and AI-generated recommendations in a single application.

## 🎯 Project Objectives

- Simplify business data analysis using natural language.
- Automate common business analytics tasks using AI agents.
- Analyze sales, orders, customers, products, and delivery performance.
- Identify customer segments using RFM analysis.
- Forecast future sales based on historical data.
- Detect unusual revenue patterns and potential business anomalies.
- Generate actionable insights to support business decisions.
- Reduce the need for users to write SQL queries manually.

## ✨ Key Features

### 1. Natural Language Business Analytics

Users can ask business-related questions in everyday English through the Streamlit dashboard.

The AI workflow interprets the question, identifies the required analysis, invokes the relevant agent or analytical tool, and returns a readable response.

### 2. SQL-Based Business Analysis

The platform connects business questions with SQL queries and database operations.

It supports analysis of business metrics such as:
- Revenue and order performance
- Customer and product information
- Sales trends
- Payment information
- Delivery performance

MySQL stores the structured business data, while SQL queries retrieve the information required for analysis.

### 3. Exploratory Data Analysis (EDA)

The EDA component helps users understand the dataset and its business patterns.

It supports analysis of:
- Data distributions and summary statistics
- Sales and order trends
- Customer and product performance
- Business KPIs
- Relationships between relevant business variables

### 4. Customer Segmentation Using RFM Analysis

The platform uses **RFM analysis**, which evaluates customers based on three dimensions:

- **Recency:** How recently a customer made a purchase.
- **Frequency:** How often a customer purchases.
- **Monetary:** How much a customer spends.

These measures help group customers into meaningful business segments, such as:

- Champions
- Loyal Customers
- Potential Loyalists
- New Customers
- At-Risk Customers
- Lost Customers

The resulting segments can help businesses understand customer behavior and plan retention or engagement strategies.

### 5. Sales Forecasting

The forecasting component analyzes historical sales data to identify trends and estimate future sales.

It helps users explore:
- Historical monthly revenue
- Sales trends over time
- Forecasted revenue
- Potential changes in business performance

Forecasts are estimates based on historical data and the selected forecasting method. They should not be treated as guaranteed future revenue.

### 6. Revenue Anomaly Detection

The anomaly detection component identifies unusual patterns in monthly revenue.

It helps highlight periods that differ from expected business behavior and may require further investigation.

Potential reasons for unusual results include:
- Sudden changes in order volume
- Unusually low or high revenue
- Data quality issues
- Seasonal business patterns
- Operational changes

An anomaly is a signal for investigation, not automatic proof of fraud or a business problem.

### 7. Business Insights and Recommendations

The platform combines analytical results with AI-generated explanations and recommendations.

Depending on the user's question, it can help explain:
- What happened in the business data
- Which trends require attention
- What might be causing an unusual result
- Which customer groups may need attention
- What actions could be considered next

Recommendations should be reviewed against the underlying data and business context before implementation.

### 8. Interactive Streamlit Dashboard

The dashboard provides a user-friendly interface for interacting with the analytics system.

It includes natural language questions, suggested queries, conversational responses, and options to clear the conversation.

The objective is to make business analytics accessible without requiring users to interact directly with multiple scripts or database queries.

## 🏗️ System Architecture

The platform follows an agent-based analytics workflow.

```text
                   User
                    |
                    v
          Streamlit Dashboard
                    |
                    v
          Natural Language Query
                    |
                    v
           AI Planning / Routing
                    |
                    v
          Business Analytics Graph
                    |
       +------------+-------------+
       |            |             |
       v            v             v
   SQL Agent     EDA Agent    RFM Agent
       |            |             |
       v            v             |
    MySQL       Python Tools      |
       |            |             |
       +------------+-------------+
                    |
          +---------+---------+
          |                   |
          v                   v
   Forecast Agent      Anomaly Agent
          |                   |
          +---------+---------+
                    |
                    v
        Insights / Recommendations
                    |
                    v
           AI Response Synthesis
                    |
                    v
          Results in Dashboard
```

*Note: This diagram represents the main conceptual workflow. The exact execution path depends on the user's question and the routing logic implemented in the project.*

## 🤖 AI Agents

The project organizes analytical tasks into specialized agents.

| Agent | Responsibility |
|---|---|
| Planner Agent | Helps determine which analytical task is required. |
| Router Agent | Routes the request to the appropriate workflow or agent. |
| SQL Agent | Handles database-oriented business questions. |
| SQL Tool Agent | Supports SQL tool execution within the agent workflow. |
| EDA Agent | Handles exploratory data analysis tasks. |
| RFM Agent | Supports customer segmentation analysis. |
| Forecast Agent | Handles sales forecasting tasks. |
| Anomaly Agent | Detects unusual revenue patterns. |
| Insight Agent | Helps explain analytical results. |
| Recommendation Agent | Generates potential business actions. |

The agents and tools work together to transform a natural language question into a business-focused analytical response.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| MySQL 8 | Relational database and business data storage |
| SQL | Querying and analyzing structured data |
| Streamlit | Interactive web dashboard |
| LangChain | LLM integration and tool-oriented workflows |
| LangGraph | Agent workflow orchestration and routing |
| Groq API | Access to the language model used for planning and response generation |
| ARIMA / Time-Series Tools | Historical sales forecasting, where configured |
| Scikit-learn | Supporting analytical and machine learning operations |
| Jupyter Notebook | Data exploration, cleaning, and experimentation |
| Git and GitHub | Version control and source code hosting |

*The exact libraries used by each analytical feature depend on the implementation in the repository.*

## 📂 Project Structure

```text
aiba/
│
├── agents/
│   ├── planner_agent.py
│   ├── router_agent.py
│   ├── business_graph.py
│   ├── sql_agent.py
│   ├── sql_tool_agent.py
│   ├── eda_agent.py
│   ├── rfm_agent.py
│   ├── forecast_agent.py
│   ├── anomaly_agent.py
│   ├── insight_agent.py
│   ├── recommendation_agent.py
│   └── graph_state.py
│
├── analytics/
│   ├── sql_tools.py
│   ├── eda_tools.py
│   ├── rfm_tools.py
│   ├── forecast_tools.py
│   ├── anomaly_tools.py
│   ├── business_insight_tools.py
│   └── recommendation_tools.py
│
├── dashboard/
│   └── app.py
│
├── database/
│   ├── schema.sql
│   ├── views.sql
│   └── business_queries.sql
│
├── data/
│   ├── raw/          # Original datasets; excluded from Git
│   └── processed/    # Generated datasets; excluded from Git
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_mysql_etl.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_rfm_analysis.ipynb
│   ├── 06_sales_forecasting.ipynb
│   └── 7_anomaly_detection.ipynb
│
├── tests/
│   ├── test_groq.py
│   ├── test_sql_agent.py
│   ├── test_sql_tool.py
│   └── test_sql_tool_agent.py
│
├── chat.py
├── .gitignore
├── .env.example       # Optional template containing placeholders only
└── requirements.txt   # Add or maintain this file for installation
```

## 🔄 Project Workflow

### Step 1: Data Collection

The project uses the Olist e-commerce dataset, which contains information related to customers, orders, order items, payments, products, sellers, reviews, and geolocation.

These datasets provide the foundation for business analysis.

### Step 2: Data Cleaning and Preparation

The raw data is explored and prepared using Python and Pandas.

This stage can include:
- Checking missing values and data quality
- Converting dates into suitable formats
- Preparing order-level analytical data
- Combining relevant tables
- Creating business metrics and derived features

The processed data is then prepared for database loading and analytical tasks.

### Step 3: Database Integration

Structured business data is stored in MySQL.

The database schema, views, and SQL queries provide a structured way to retrieve business information and calculate relevant metrics.

### Step 4: User Asks a Business Question

A user submits a question through the Streamlit dashboard.

For example:

"What are the main reasons I should investigate this month's revenue decline?"

### Step 5: Agent Planning and Routing

The AI workflow determines which analytical capabilities are relevant to the question.

Depending on the request, it can route work to SQL, EDA, forecasting, anomaly detection, RFM, or other supported tools.

### Step 6: Analytical Execution

The selected agent or tool performs the relevant task.

This may involve querying MySQL, analyzing historical data, calculating customer segments, forecasting revenue, or identifying unusual patterns.

### Step 7: Insight Generation

The system collects the analytical results and uses the configured language model to help explain them in natural language.

### Step 8: Results and Recommendations

The final response is displayed in the dashboard, helping the user understand the result and decide what to investigate or do next.

## 📊 Dataset

This project uses the Olist Brazilian e-commerce dataset.

The data includes information such as:

- Customers
- Orders
- Order items
- Payments
- Products
- Sellers
- Customer reviews
- Geolocation
- Product category translations

The data is useful for analyzing e-commerce sales, customer behavior, order performance, and delivery patterns.

**Dataset note:** The raw and processed CSV files are excluded from this GitHub repository to keep it lightweight. You must obtain the dataset separately and follow the expected file paths used by the notebooks and data-processing code.

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Install or prepare:

- Python 3.10 or a compatible version supported by your dependencies
- MySQL 8
- Git
- A Groq API key
- The required project dataset

### 1. Clone the repository

```bash
git clone https://github.com/gyandeep-tech/agentic-business-analytics.git
cd agentic-business-analytics
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Ensure that `requirements.txt` lists the project's required packages, then run:

```bash
python -m pip install -r requirements.txt
```

If the dependency file is missing or incomplete, create or update it from the packages actually imported by the project.

### 4. Configure environment variables

Create a local `.env` file in the project root.

Add the variables expected by your application's configuration, for example:

```dotenv
GROQ_API_KEY=your_groq_api_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=agentic_analytics
```

**Important:** These names are examples. Confirm the exact environment variable names in your code and use those names in your actual `.env` file.

Never commit `.env` to GitHub. Do not put real API keys or passwords in this README.

### 5. Configure MySQL

Start your MySQL server and create the required database.

For example, if the configured database name is `agentic_analytics`:

```sql
CREATE DATABASE agentic_analytics;
```

Review and execute the SQL scripts in the `database/` directory as required by your implementation.

Ensure the database is populated with the expected data before running database-dependent features.

### 6. Prepare the dataset

Download or obtain the required Olist dataset separately.

Place the CSV files in the expected local `data/raw/` directory and run the applicable data preparation and ETL steps.

Check the notebooks and Python modules for exact file names and processing instructions.

### 7. Run the Streamlit application

The primary dashboard is located at `dashboard/app.py`.

From the project root, run:

```bash
python -m streamlit run dashboard/app.py
```

If you use a different entry point, such as `chat.py`, follow the entry point documented in that file.

Once Streamlit starts, open the local URL printed in the terminal, usually `http://localhost:8501`.

## 🔐 Security and Configuration

The project uses API credentials and database connection settings, so secret management is important.

- Keep `.env` out of version control.
- Never publish Groq API keys, database passwords, or access tokens.
- Keep `.streamlit/secrets.toml` out of Git.
- Avoid committing private customer information or sensitive database exports.
- Use least-privilege database credentials.
- Store deployment secrets in the deployment platform's secret manager.

The repository's `.gitignore` excludes raw and processed datasets by default.

## 🚀 Deployment

The project can be prepared for deployment using Streamlit Community Cloud or another compatible hosting environment.

Before deployment:

1. Ensure the application starts successfully in your local environment.
2. Confirm `requirements.txt` includes the necessary dependencies.
3. Configure API keys and database credentials through the hosting platform's secrets settings.
4. Configure a database that the deployed application can securely reach.
5. Test all required agents and analytical workflows.
6. Verify that no local-only file paths or dependencies prevent cloud execution.

**Database consideration:** A MySQL server running on your personal computer is not automatically accessible to a cloud application. Use a suitable hosted database or another secure deployment architecture.

Deployment is not complete until the application has been configured and tested in its target environment.

## 🧪 Testing

The `tests/` directory contains tests related to Groq integration and SQL agents/tools.

Run the tests with:

```bash
python -m pytest tests/
```

Some tests may require configured API credentials, a running database, or valid test data. Configure those prerequisites before interpreting test failures.

## 💼 Business Use Cases

Potential uses of this platform include:

- Monitoring revenue and order performance
- Understanding customer purchasing behavior
- Identifying customers who may need retention campaigns
- Exploring historical sales patterns
- Investigating unusual revenue changes
- Supporting data-driven business decisions
- Making analytical results easier for non-technical users to understand

These are intended applications of the analytics capabilities, not guarantees of business outcomes.

## 🔮 Future Improvements

Possible future enhancements include:

- Deploying a stable public dashboard
- Adding role-based access control
- Improving error handling and observability
- Adding more business KPIs and visualizations
- Supporting additional datasets and databases
- Adding automated scheduled reports
- Improving agent evaluation and answer validation
- Adding data freshness and data-quality monitoring
- Improving scalability and query safety

## 👨‍💻 Author

**Gyandeep Talukder**

B.Tech Computer Science and Engineering

GitHub: [@gyandeep-tech](https://github.com/gyandeep-tech)

## 📄 License

Choose and add a license before distributing or reusing this project. Until a license is added, don't assume that others have permission to reuse the source code.

---

**If you find this project useful, consider starring the repository on GitHub.**
