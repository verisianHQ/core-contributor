import pandas as pd
import altair as alt
import streamlit as st


def make_pie(labels, num, title, color_scheme="category10", donut=True, show_full_label=True):
    source = pd.DataFrame({"category": labels, "value": num})

    if show_full_label:
        source["display_text"] = source["category"] + ": " + source["value"].astype(str)
    else:
        source["display_text"] = source["value"].astype(str)

    base = alt.Chart(source).encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color("category:N", scale=alt.Scale(scheme=color_scheme), legend=None),
        tooltip=["category", "value"],
    )

    inner_r = 40 if donut else 0
    pie = base.mark_arc(outerRadius=120, innerRadius=inner_r)

    text = base.mark_text(radius=140).encode(
        text=alt.Text("display_text:N"), order=alt.Order("category:N"), color=alt.value("black")
    )

    st.markdown(f"<h3 style='text-align: center; color: grey;'>{title}</h3>", unsafe_allow_html=True)
    st.altair_chart(pie + text, use_container_width=True)
