import altair as alt
import streamlit as st

def make_horizontal_bar(df, title, tooltip_cols):
    if df.empty:
        return
        
    source = df.copy()
    source["unit"] = 1
    
    chart = alt.Chart(source).mark_bar().encode(
        y=alt.Y("Status:N", title="Test Status"),
        x=alt.X("unit:Q", stack=True, title="Total Count"),
        color=alt.Color(
            "Issue:N", 
            title="Issue / Exception", 
            scale=alt.Scale(scheme="tableau20"),
            legend=None
        ),
        order=alt.Order("Issue:N"), 
        tooltip=[alt.Tooltip(c) for c in tooltip_cols]
    ).properties(
        height=alt.Step(150) 
    )
    
    st.markdown(f"<h3 style='text-align: center; color: grey;'>{title}</h3>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)