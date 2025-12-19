"""
Streamlit UI for the HITL Salary Management System.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.workflow import graph
from src.state import WorkflowState

# Page configuration
st.set_page_config(
    page_title="HITL Salary Management System",
    page_icon="💼",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .proposal-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = None
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = "thread_1"
if 'workflow_history' not in st.session_state:
    st.session_state.workflow_history = []

# Load data
@st.cache_data
def load_salary_data():
    """Load the salary data from Excel."""
    data_path = Path(__file__).parent / "data" / "salary_data.xlsx"
    if not data_path.exists():
        return None
    return pd.read_excel(data_path)

# Main app
st.markdown('<div class="main-header">💼 HITL Salary Management System</div>', unsafe_allow_html=True)
st.markdown("**Human-in-the-Loop Workflow powered by LangGraph**")

# Load data
df = load_salary_data()

if df is None:
    st.error("❌ Salary data not found. Please run `python generate_data.py` first.")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🔍 Department Analysis", "✅ Approval Interface", "📋 Workflow History"])

# =========================
# TAB 1: Data Overview
# =========================
with tab1:
    st.markdown('<div class="sub-header">Employee Data Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", len(df))
    with col2:
        st.metric("Departments", df['Department'].nunique())
    with col3:
        st.metric("Avg Salary", f"₹{df['Current_Salary'].mean():,.0f}")
    
    st.markdown("### 📋 All Employees")
    st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("### 📊 Salary Distribution by Department")
    fig = px.box(df, x='Department', y='Current_Salary', color='Department',
                 title='Salary Distribution',
                 labels={'Current_Salary': 'Salary (₹)'})
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📈 Department Statistics")
    dept_stats = df.groupby('Department').agg({
        'Current_Salary': ['count', 'mean', 'min', 'max']
    }).round(0)
    dept_stats.columns = ['Employees', 'Avg Salary', 'Min Salary', 'Max Salary']
    dept_stats = dept_stats.reset_index()
    st.dataframe(dept_stats, use_container_width=True)

# =========================
# TAB 2: Department Analysis
# =========================
with tab2:
    st.markdown('<div class="sub-header">Analyze Department</div>', unsafe_allow_html=True)
    
    # Department selection
    departments = sorted(df['Department'].unique())
    selected_dept = st.selectbox("Select Department to Analyze", departments)
    
    if st.button("🔍 Analyze Department", type="primary", use_container_width=True):
        # Initialize workflow
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        initial_state = {
            "department": selected_dept,
            "employees": [],
            "execution_log": []
        }
        
        # Run workflow until interrupt
        try:
            with st.spinner("Analyzing department..."):
                result = None
                for event in graph.stream(initial_state, config, stream_mode="values"):
                    result = event
                
                st.session_state.workflow_state = result
                st.success("✅ Analysis complete! See proposal below.")
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
    
    # Display analysis results
    if st.session_state.workflow_state:
        state = st.session_state.workflow_state
        
        if state.get('highest_paid'):
            highest = state['highest_paid']
            
            st.markdown("### 👤 Highest-Paid Employee")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {highest['Name']}")
                st.info(f"**Position:** {highest['Position']}")
                st.info(f"**Current Salary:** ₹{highest['Current_Salary']:,}")
            with col2:
                st.info(f"**Department:** {highest['Department']}")
                st.info(f"**Manager:** {highest['Manager']}")
                st.info(f"**Join Date:** {highest['Join_Date']}")
            
            # Show proposal
            if state.get('proposal_details'):
                proposal = state['proposal_details']
                proposal_type = state['proposal_type']
                
                st.markdown('<div class="proposal-box">', unsafe_allow_html=True)
                st.markdown("### 📝 AI-Generated Proposal")
                
                if proposal_type == 'salary_hike':
                    st.markdown(f"**Proposal Type:** Salary Hike")
                    st.markdown(f"**Employee:** {proposal['employee_name']}")
                    st.markdown(f"**Current Salary:** ₹{proposal['current_salary']:,}")
                    st.markdown(f"**Proposed Salary:** ₹{proposal['proposed_salary']:,}")
                    st.markdown(f"**Increase:** {proposal['increase_percentage']}% (₹{proposal['proposed_salary'] - proposal['current_salary']:,})")
                    st.markdown(f"**Reason:** {proposal['reason']}")
                else:  # manager_change
                    st.markdown(f"**Proposal Type:** Manager Change")
                    st.markdown(f"**Employee:** {proposal['employee_name']}")
                    st.markdown(f"**Current Manager:** {proposal['current_manager']}")
                    st.markdown(f"**Proposed Manager:** {proposal['proposed_manager']}")
                    st.markdown(f"**Reason:** {proposal['reason']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.info("👉 Go to the **Approval Interface** tab to make your decision.")

# =========================
# TAB 3: Approval Interface
# =========================
with tab3:
    st.markdown('<div class="sub-header">Human-in-the-Loop Approval</div>', unsafe_allow_html=True)
    
    if not st.session_state.workflow_state:
        st.warning("⚠️ No active proposal. Please analyze a department first in the **Department Analysis** tab.")
    elif st.session_state.workflow_state.get('final_status'):
        st.info("ℹ️ Current workflow is complete. Analyze a new department to create a new proposal.")
        
        # Show final result
        final_msg = st.session_state.workflow_state.get('final_message', '')
        status = st.session_state.workflow_state.get('final_status', '')
        
        if status == 'approved':
            st.markdown(f'<div class="success-box">{final_msg}</div>', unsafe_allow_html=True)
        elif status == 'rejected':
            st.markdown(f'<div class="error-box">{final_msg}</div>', unsafe_allow_html=True)
        elif status == 'modified':
            st.markdown(f'<div class="warning-box">{final_msg}</div>', unsafe_allow_html=True)
    else:
        state = st.session_state.workflow_state
        proposal = state.get('proposal_details', {})
        proposal_type = state.get('proposal_type', '')
        
        # Display current proposal
        st.markdown('<div class="proposal-box">', unsafe_allow_html=True)
        st.markdown("### 📝 Current Proposal")
        
        if proposal_type == 'salary_hike':
            st.markdown(f"**Type:** Salary Hike")
            st.markdown(f"**Employee:** {proposal['employee_name']}")
            st.markdown(f"**Current Salary:** ₹{proposal['current_salary']:,}")
            st.markdown(f"**Proposed Salary:** ₹{proposal['proposed_salary']:,}")
            st.markdown(f"**Increase:** {proposal['increase_percentage']}%")
        else:
            st.markdown(f"**Type:** Manager Change")
            st.markdown(f"**Employee:** {proposal['employee_name']}")
            st.markdown(f"**Current Manager:** {proposal['current_manager']}")
            st.markdown(f"**Proposed Manager:** {proposal['proposed_manager']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Your Decision")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Approve", type="primary", use_container_width=True):
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                # Update state with approval
                graph.update_state(
                    config,
                    {"human_decision": "approve"}
                )
                
                # Continue workflow
                result = None
                for event in graph.stream(None, config, stream_mode="values"):
                    result = event
                
                st.session_state.workflow_state = result
                st.session_state.workflow_history.append(result)
                st.rerun()
        
        with col2:
            if st.button("❌ Reject", type="secondary", use_container_width=True):
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                # Update state with rejection
                graph.update_state(
                    config,
                    {"human_decision": "reject"}
                )
                
                # Continue workflow
                result = None
                for event in graph.stream(None, config, stream_mode="values"):
                    result = event
                
                st.session_state.workflow_state = result
                st.session_state.workflow_history.append(result)
                st.rerun()
        
        with col3:
            modify_clicked = st.button("📝 Modify", use_container_width=True)
        
        # Modification interface
        if modify_clicked or st.session_state.get('show_modify_form', False):
            st.session_state.show_modify_form = True
            
            st.markdown("### ✏️ Modify Proposal")
            
            with st.form("modify_form"):
                if proposal_type == 'salary_hike':
                    modified_salary = st.number_input(
                        "Enter New Salary",
                        min_value=proposal['current_salary'],
                        value=proposal['proposed_salary'],
                        step=1000
                    )
                    modification_details = {'modified_salary': int(modified_salary)}
                else:
                    # Get list of potential managers
                    dept_employees = [e['Name'] for e in state['employees'] 
                                    if e['Employee_ID'] != proposal['employee_id']]
                    modified_manager = st.selectbox(
                        "Select New Manager",
                        options=dept_employees,
                        index=dept_employees.index(proposal['proposed_manager']) 
                            if proposal['proposed_manager'] in dept_employees else 0
                    )
                    modification_details = {'modified_manager': modified_manager}
                
                submit_modify = st.form_submit_button("Submit Modification", type="primary")
                
                if submit_modify:
                    config = {"configurable": {"thread_id": st.session_state.thread_id}}
                    
                    # Update state with modification
                    graph.update_state(
                        config,
                        {
                            "human_decision": "modify",
                            "modification_details": modification_details
                        }
                    )
                    
                    # Continue workflow
                    result = None
                    for event in graph.stream(None, config, stream_mode="values"):
                        result = event
                    
                    st.session_state.workflow_state = result
                    st.session_state.workflow_history.append(result)
                    st.session_state.show_modify_form = False
                    st.rerun()

# =========================
# TAB 4: Workflow History
# =========================
with tab4:
    st.markdown('<div class="sub-header">Workflow Execution History</div>', unsafe_allow_html=True)
    
    if not st.session_state.workflow_history:
        st.info("No workflow history yet. Process some proposals to see history here.")
    else:
        for idx, workflow in enumerate(reversed(st.session_state.workflow_history), 1):
            with st.expander(f"Workflow #{len(st.session_state.workflow_history) - idx + 1} - {workflow.get('final_status', 'unknown').upper()}"):
                st.markdown(f"**Department:** {workflow.get('department', 'N/A')}")
                st.markdown(f"**Status:** {workflow.get('final_status', 'N/A')}")
                st.markdown(f"**Result:** {workflow.get('final_message', 'N/A')}")
                
                if workflow.get('execution_log'):
                    st.markdown("**Execution Log:**")
                    for log_entry in workflow['execution_log']:
                        st.text(f"  • {log_entry}")
    
    # Current workflow log
    if st.session_state.workflow_state and st.session_state.workflow_state.get('execution_log'):
        st.markdown("### 📝 Current Workflow Log")
        for log_entry in st.session_state.workflow_state['execution_log']:
            st.text(f"  • {log_entry}")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 About")
    st.markdown("""
    This system demonstrates **Human-in-the-Loop (HITL)** workflows using:
    
    - **LangGraph** for workflow orchestration
    - **Streamlit** for interactive UI
    - **HITL interrupts** for human decisions
    
    The workflow:
    1. Analyzes department data
    2. Identifies highest-paid employee
    3. Generates a proposal (salary hike or manager change)
    4. **Pauses for human approval**
    5. Processes the decision (approve/reject/modify)
    """)
    
    st.markdown("### 🔄 System Status")
    if st.session_state.workflow_state:
        if st.session_state.workflow_state.get('final_status'):
            st.success("Workflow Complete")
        else:
            st.warning("Awaiting Human Decision")
    else:
        st.info("No Active Workflow")
    
    if st.button("🔄 Reset Workflow", use_container_width=True):
        st.session_state.workflow_state = None
        st.session_state.thread_id = f"thread_{pd.Timestamp.now().timestamp()}"
        st.session_state.show_modify_form = False
        st.rerun()
