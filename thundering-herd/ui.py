# ui.py

import asyncio
import streamlit as st

from run_naive import run_naive
from run_coalesced import run_coalesced
from run_distributed import run_distributed

st.set_page_config(
    page_title="Thundering Herd Demo",
    layout="wide"
)

st.title("Thundering Herd Demo")

st.write(
    "See how different approaches reduce duplicate database calls."
)


# Inputs
col1, col2 = st.columns(2)

with col1:
    requests = st.number_input(
        "Concurrent Requests",
        min_value=1,
        value=100
    )

with col2:
    instances = st.number_input(
        "API Instances",
        min_value=1,
        value=20
    )


st.divider()


# Buttons
col1, col2, col3 = st.columns(3)

result = None
approach = None


with col1:
    if st.button("Naive", use_container_width=True):

        approach = "Naive"

        result = asyncio.run(
            run_naive(
                int(requests),
                int(instances)
            )
        )


with col2:
    if st.button(
        "Local Coalescing",
        use_container_width=True
    ):

        approach = "Local Coalescing"

        result = asyncio.run(
            run_coalesced(
                int(requests),
                int(instances)
            )
        )


with col3:
    if st.button(
        "Distributed Lock",
        use_container_width=True
    ):

        approach = "Distributed Lock"

        result = asyncio.run(
            run_distributed(
                int(requests),
                int(instances)
            )
        )


# Results
if result:

    st.divider()

    st.subheader(approach)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Requests",
        result["requests"]
    )

    col2.metric(
        "Database Calls",
        result["db_calls"]
    )

    col3.metric(
        "Elapsed Time",
        f'{result["elapsed_ms"]:.0f} ms'
    )


    st.subheader("Database Calls")

    st.bar_chart(
        {
            "DB Calls": [
                result["db_calls"]
            ]
        }
    )