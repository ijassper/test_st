import streamlit as st

st.title("가져올 기준정보 sql 만들기")

st.button("라인")
st.button("제품")
st.button("스탭")
st.text_input("가지고있는 명령문 붙여넣기")
st.button("검색")

uploaded_file = st.file_uploader("기준정보 파일 선택", type=['csv','xlsx'])

st.title("가져온 기준정보 리스트")



line_list = [
    "12", "12EF", "13", "15", "U2", "16", "U3", "17", 
    "U4", "P1F", "P1D", "P23F", "P2D", "P3D", "P4F", "P4D"
]
select_list = st.selectbox("SENDFAB 보낼 라인선택",line_list)

#selected_line = line_list[i]

st.write(f"라인 ID : {select_list}")

st.button("검색")
