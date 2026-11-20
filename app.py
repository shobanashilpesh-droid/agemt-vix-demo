
import os

import streamlit as st
import pandas as pd
#from dotenv import load_dotenv
from langfuse import get_client

# -----------------------------------------
# 1. Application configuration
# -----------------------------------------

st.set_page_config(
    page_title="Agent VIX | Channel Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Load local environment variables
import os

# Load Streamlit Clouimport osd secrets before importing agents
try:
    for key in [
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "LANGFUSE_HOST"
    ]:
        if key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception:
    pass

# Import project modules after loading credentials
from data.synthetic_data import generate_adobe_data
from smart_orchestrator import run_smart_agent_vix


# -----------------------------------------
# 2. Page styling
# -----------------------------------------

st.title("🤖 Agent VIX")
st.subheader("AI-Powered Channel Intelligence Platform")

st.markdown(
    """
    Agent VIX is the Master Orchestrator that coordinates
    specialist AI agents to identify subscription renewals,
    churn risks, pricing opportunities and revenue expansion.
    """
)

st.divider()


# -----------------------------------------
# 3. Generate synthetic subscription data
# -----------------------------------------

@st.cache_data
def load_subscription_data():
    return generate_adobe_data()


df = load_subscription_data()


# -----------------------------------------
# 4. Overview dashboard
# -----------------------------------------

st.header("Business Intelligence Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Subscriptions",
    len(df)
)

col2.metric(
    "Unique Customers",
    df["customer_id"].nunique()
)

col3.metric(
    "Unique Resellers",
    df["reseller_id"].nunique()
)

st.divider()


# -----------------------------------------
# 5. Subscription data preview
# -----------------------------------------

with st.expander("View Subscription Dataset"):

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# -----------------------------------------
# 6. Execute Agent VIX
# -----------------------------------------

st.header("Agent VIX Orchestration")

st.write(
    "Execute the Master Orchestrator to analyse subscription "
    "data and identify relevant business opportunities."
)

if st.button("🚀 Run Agent VIX", type="primary"):

    with st.spinner(
        "Agent VIX is analysing subscription data and invoking specialist agents..."
    ):

        try:
            results = run_smart_agent_vix(df)

            st.session_state["agent_vix_results"] = results

            # Flush Langfuse observations
            get_client().flush()

            st.success("Agent VIX execution completed successfully!")

        except Exception as error:
            st.error("Agent VIX execution failed.")
            st.exception(error)


# -----------------------------------------
# 7. Display orchestration results
# -----------------------------------------

if "agent_vix_results" in st.session_state:

    results = st.session_state["agent_vix_results"]
    summary = results["summary"]

    st.divider()
    st.header("Consolidated Business Intelligence")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Renewal Opportunities",
        summary["renewal_opportunities"]
    )

    col2.metric(
        "Churn Risk Customers",
        summary["churn_risk_customers"]
    )

    col3.metric(
        "Pricing Opportunities",
        summary["pricing_opportunities"]
    )

    col4.metric(
        "Upsell Opportunities",
        summary["upsell_opportunities"]
    )

    # -------------------------------------
    # Agent execution status
    # -------------------------------------

    st.subheader("Agent Execution Status")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Agents Invoked")

        for agent in summary["agents_invoked"]:
            st.success(f"✓ {agent}")

    with col2:
        st.markdown("#### Agents Skipped")

        if summary["agents_skipped"]:

            for agent in summary["agents_skipped"]:
                st.info(f"Skipped: {agent}")

        else:
            st.write("No agents were skipped.")

    # -------------------------------------
    # Specialist agent results
    # -------------------------------------

    st.divider()
    st.header("Specialist Agent Insights")

    tabs = st.tabs([
        "Renewal Intelligence",
        "Churn Prediction",
        "Pricing Intelligence",
        "Upsell & Cross-sell"
    ])

    agent_results = [
        ("renewal_results", "Renewal opportunities"),
        ("churn_results", "At-risk customers"),
        ("pricing_results", "Pricing opportunities"),
        ("upsell_results", "Upsell opportunities")
    ]

    for tab, (result_key, heading) in zip(
        tabs, agent_results
    ):

        with tab:

            if result_key in results:

                result_df = results[result_key]

                st.subheader(heading)

                st.metric(
                    "Identified opportunities",
                    len(result_df)
                )

                if not result_df.empty:

                    st.dataframe(
                        result_df,
                        width="stretch",
                        hide_index=True
                    )

                else:
                    st.info("No opportunities identified.")

            else:
                st.info(
                    "This agent was not invoked because "
                    "its routing condition was not met."
                )


# -----------------------------------------
# 8. Langfuse monitoring
# -----------------------------------------

st.divider()

st.subheader("Agent Observability")

st.write(
    "Agent execution observations and monitoring are captured "
    "through Langfuse when credentials are configured."
)

if os.getenv("LANGFUSE_PUBLIC_KEY"):

    st.success("Langfuse credentials are configured.")

else:

    st.warning(
        "Langfuse credentials are not configured. "
        "Business analysis can run, but traces will not be recorded."
    )


# -----------------------------------------
# 9. Footer
# -----------------------------------------

st.divider()

st.caption(
    "Agent VIX | AI-Powered Channel Intelligence | "
    "Prototype using synthetic Adobe subscription data"
)
