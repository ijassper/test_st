import os
import pymysql
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Retrieve DB connection parameters
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")

# Cache the DB connection as a resource
@st.cache_resource(show_spinner=False)
def get_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        return conn
    except Exception as e:
        st.error(f"❌ DB 연결 오류: {e}")
        return None

# Cache the query result as data
@st.cache_data(show_spinner=False)
def load_data(limit: int) -> pd.DataFrame:
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    query = f"""
        SELECT STEPID, PPID, DCSPEC_ID
        FROM factory_db.flow_head
        LIMIT {limit};
    """
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ 데이터 조회 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="Factory DB Flow Head", layout="wide")
st.title("🏭 Factory DB Flow Head 데이터 현황")
st.caption("MySQL 데이터베이스에서 STEPID, PPID, DCSPEC_ID 를 시각화합니다.")

# Sidebar - filters and settings
with st.sidebar:
    st.header("필터 및 설정")
    limit_val = st.number_input("조회 건수 제한 (Limit)", min_value=10, max_value=500, value=25, step=5)
    search_term = st.text_input("검색 (STEPID 또는 PPID)", "")
    if st.button("데이터 새로고침"):
        st.experimental_rerun()

# Load data
df = load_data(limit_val)

if df.empty:
    st.warning("조회된 데이터가 없습니다.")
else:
    # Apply search filter if provided
    if search_term:
        mask = df["STEPID"].astype(str).str.contains(search_term, case=False, na=False) |
               df["PPID"].astype(str).str.contains(search_term, case=False, na=False)
        df = df[mask]

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 레코드 수", len(df))
    col2.metric("유니크 STEPID 수", df["STEPID"].nunique())
    col3.metric("유니크 PPID 수", df["PPID"].nunique())

    # Dataframe display
    st.dataframe(df, use_container_width=True)

    # CSV download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name="flow_head.csv",
        mime="text/csv",
    )
