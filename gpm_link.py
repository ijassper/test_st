import streamlit as st

line_list = [
    "12", "12EF", "13", "15", "U2", "16", "U3", "17", 
    "U4", "P1F", "P1D", "P23F", "P2D", "P3D", "P4F", "P4D"
]
select_list = st.selectbox("SENDFAB 보낼 라인선택",line_list)

#selected_line = line_list[i]

st.write(f"선택된 보낼 라인 : {selected_list}")
