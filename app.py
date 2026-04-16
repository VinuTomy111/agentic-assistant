import streamlit as st
import os

from config import GROQ_API_KEY, MEMORY_DIR
from agents import PlannerAgent, ExecutorAgent
from memory import ShortTermMemory, LongTermMemory

st.set_page_config(page_title="Personal AI Assistant", page_icon="🤖")

st.title("🤖 AI Personal Task & Decision Assistant")
st.markdown("Plan tasks, search the web, calculate math, and take notes!")

# Initialize objects
if 'short_term_memory' not in st.session_state:
    st.session_state.short_term_memory = ShortTermMemory()
if 'long_term_memory' not in st.session_state:
    long_term_path = os.path.join(MEMORY_DIR, "long_term.json")
    st.session_state.long_term_memory = LongTermMemory(filepath=long_term_path)
if 'planner' not in st.session_state:
    st.session_state.planner = PlannerAgent(api_key=GROQ_API_KEY)
if 'executor' not in st.session_state:
    st.session_state.executor = ExecutorAgent(api_key=GROQ_API_KEY)

# Display Chat History
for message in st.session_state.short_term_memory.get_history():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("What do you want to accomplish today?")

if user_query:
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY is not configured in .env")
    else:
        # Display user message
        st.chat_message("user").markdown(user_query)
        st.session_state.short_term_memory.add_message("user", user_query)
        
        # Prepare context
        st_context = st.session_state.short_term_memory.get_context_string()
        relevant_ltm = st.session_state.long_term_memory.retrieve_relevant(user_query, top_k=3)
        ltm_context = "\n".join(relevant_ltm) if relevant_ltm else "No relevant long-term memories found."
        
        # Display planning step
        with st.status("Analyzing and Planning...", expanded=True) as status:
            st.write("Generating structured plan...")
            plan = st.session_state.planner.plan(user_query, st_context, ltm_context)
            if plan:
                for step in plan:
                    st.write(f"- **Step {step.get('step_number')}**: `{step.get('tool')}` ({step.get('reasoning')})")
            else:
                 st.write("Direct answering (no tools needed)")
                 
            st.write("Executing plan...")
            final_answer = st.session_state.executor.execute_plan(plan, user_query)
            status.update(label="Task Complete!", state="complete", expanded=False)
            
        # Display assistant message
        st.chat_message("assistant").markdown(final_answer)
        st.session_state.short_term_memory.add_message("assistant", final_answer)
