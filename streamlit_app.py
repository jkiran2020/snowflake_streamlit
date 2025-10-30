import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Row

# Get the current Snowpark session
session = get_active_session()

# session.sql("USE ROLE ACCOUNTADMIN").collect()
# --- Configuration ---
# Your pre-created Cortex Agent's fully qualified name
AGENT_NAME = "SNOWFLAKE_INTELLIGENCE.AGENTS.SALES_INTELLIGENCE_AGENT"

# --- Streamlit UI Setup ---
st.set_page_config(layout="wide")
st.title("🤖 Snowflake Cortex Agent Chat: Sales Intelligence")
st.caption(f"Agent: **{AGENT_NAME}**")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming message from the agent
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm your Sales Intelligence Agent. How can I help you today?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Main Chat Input and Agent Invocation ---
if prompt := st.chat_input("Ask a question about sales data..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Get the last 5 messages for conversation context
    # Snowflake's Agent API usually handles history internally, but this is good practice
    # for a Streamlit chat UI. We'll pass the full history to keep the UI simple.
    chat_history_for_agent = []
    for msg in st.session_state.messages:
        chat_history_for_agent.append({"role": msg["role"], "content": msg["content"]})

    # 3. Call the Cortex Agent using Snowpark session.call
    with st.spinner(f"Agent {AGENT_NAME} is thinking..."):
        try:
            # The Cortex Agent is invoked via its stored procedure, which typically
            # takes an array of messages (the conversation history) and an agent name.
            # The specific signature might vary, but this is a common approach for agent SPs.

            # We assume the agent was created with a signature that takes a prompt string.
            # If your agent accepts conversation history (an array of messages), you'll need
            # to adjust the call to pass the 'chat_history_for_agent' array as a JSON string.

            # Common Agent Invocation (simplest form: just the prompt)
            agent_response_df = session.sql(f"""
                SELECT {AGENT_NAME}('{prompt}') AS AGENT_RESPONSE
            """).collect()
            
            # Extract the response from the Snowpark DataFrame result
            agent_response = agent_response_df[0]['AGENT_RESPONSE']
            
        except Exception as e:
            agent_response = f"An error occurred while calling the agent: {e}"

    # 4. Display agent response and update history
    with st.chat_message("assistant"):
        st.write(agent_response)
        
    st.session_state.messages.append({"role": "assistant", "content": agent_response})

    # # Import python packages
# import streamlit as st
# from snowflake.snowpark.context import get_active_session
# from snowflake.ml.cortex import CortexAgent


# # Write directly to the app
# st.title(f"Example Streamlit App :balloon: {st.__version__}")
# st.write(
#   """Replace this example with your own code!
#   **And if you're new to Streamlit,** check
#   out our easy-to-follow guides at
#   [docs.streamlit.io](https://docs.streamlit.io).
#   """
# )

# # Get the current credentials
# session = get_active_session()

# # # Use an interactive slider to get user input
# # import streamlit as st
# # from snowflake.snowpark import Session

# session = st.connection("snowflake").session()
# agent = CortexAgent(session, "SALES_SENTIMENT_ANALYSIS_AGENT")

# st.title("Sales Intelligence Assistant")

# user_query = st.text_input("Ask a question:")
# if st.button("Submit"):
#     response = agent.invoke(user_query)
#     st.write(response["answer"])
