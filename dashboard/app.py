
import streamlit as st
from agents.business_graph import business_graph

# Page configuration
st.set_page_config(
    page_title="AI Business Analytics",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Agentic AI Business Analytics")
st.caption(
    "Ask questions about sales, customers, revenue forecasts, "
    "and business performance."
)

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user question
question = st.chat_input("Ask a business question...")

if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Run the agentic workflow
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your business data..."):
            try:
                result = business_graph.invoke(
                    {"question": question}
                )

                answer = result.get(
                    "final_answer",
                    "Sorry, no answer was generated."
                )

            except Exception as error:
                answer = (
                    "An error occurred while processing "
                    f"your question: {error}"
                )

        st.markdown("### Business Analysis")

        # Display key business metrics for the revenue query
        if (
            "15,419,773.75" in answer
            and "96,478" in answer
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Delivered Order Revenue",
                    value="$15,419,773.75"
                )

            with col2:
                st.metric(
                    label="Delivered Orders",
                    value="96,478"
            )

            st.divider()

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Sidebar

with st.sidebar:
    st.title("📊 Business Analytics")
    st.caption("AI-powered decision support")

    st.divider()

    st.subheader("💡 Suggested Questions")

    suggestions = [
        "What was our total revenue and how many orders were delivered?",
        "Which customer segment has the most customers?",
        "Which months were detected as sales anomalies?",
        "Analyze our sales performance and forecast the next six months.",
        "Give me recommendations to improve business performance."
    ]

    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_question = suggestion
            st.rerun()

    st.divider()

    st.caption("Powered by LangGraph, Groq, Python and MySQL")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

