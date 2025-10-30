import streamlit as st

# --- Configuration ---
# Your pre-created Cortex Agent's fully qualified name
# IMPORTANT: Use the full uppercase name to avoid compilation errors
AGENT_NAME = "SALES_INTELLIGENCE.DATA.SALES_INTELLIGENCE_AGENT"

# --- Streamlit UI Setup ---
st.set_page_config(layout="wide")
st.title("🤖 Cortex Sales Intelligence Chatbot")
st.caption("Powered by Snowflake Cortex Agents and Streamlit Community Cloud.")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming message from the agent
    st.session_state.messages.append(
        {"role": "assistant", "content": f"Hello! I am your {AGENT_NAME}."}
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Main Chat Input and Agent Invocation ---

if prompt := st.chat_input("Ask a question about sales data or sentiment..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Call the Cortex Agent using st.connection
    with st.spinner(f"Agent is analyzing data using {AGENT_NAME}..."):
        try:
            # st.connection('snowflake') automatically uses the credentials
            # loaded from the secrets manager (your .toml settings).
            conn = st.connection("snowflake")
            
            # The Cortex Agent is called directly via SQL
            sql_query = f"""
                SELECT {AGENT_NAME}('{prompt}') AS AGENT_RESPONSE
            """
            
            # Execute the query
            response_df = conn.query(sql_query, ttl=0)
            
            # Extract the response string from the first row of the DataFrame
            agent_response = response_df['AGENT_RESPONSE'][0]
            
        except Exception as e:
            # Display a user-friendly error message if the connection or query fails
            agent_response = f"Sorry, an error occurred while reaching Snowflake: {e}"

    # 3. Display agent response and update history
    with st.chat_message("assistant"):
        st.write(agent_response)
        
    st.session_state.messages.append({"role": "assistant", "content": agent_response})