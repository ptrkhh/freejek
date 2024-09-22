import streamlit as st
from dotenv import load_dotenv
from st_supabase_connection import SupabaseConnection, execute_query

load_dotenv()

# Initialize connection.
conn = st.connection("supabase", type=SupabaseConnection)
# Perform query.
res = execute_query(conn.table("vehicle_model").select("*"))
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Print results.
for row in res:
    print("THE ROW", row)
    st.write(row)
    # st.write(f"{row['make']} has a :{row['model']}:")
