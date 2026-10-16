import altair as alt
import streamlit as st

def make_stacked_area(df, x_col, y_col, color_col, title):
    if df.empty:
        return

    chart = (
        alt.Chart(df)
        .mark_area(opacity=0.8)
        .encode(
            x=alt.X(f"{x_col}:N", title="Timeline"),
            y=alt.Y(f"{y_col}:Q", title="Number of Rules", stack="zero"),
            color=alt.Color(
                f"{color_col}:N",
                scale=alt.Scale(
                    domain=["Missing from Repo", "Unvalidated Rules", "Validated Rules"],
                    range=["#d62728", "#ff7f0e", "#2ca02c"]
                ),
                legend=alt.Legend(title="Rule Status")
            ),
            order=alt.Order("Order:Q", sort="ascending"),
            tooltip=[x_col, color_col, y_col]
        )
        .properties(height=350)
    )

    st.markdown(f"<h3 style='text-align: center; color: grey;'>{title}</h3>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)