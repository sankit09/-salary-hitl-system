# HITL Salary Management System 💼

A **Human-in-the-Loop (HITL)** workflow demonstration using **LangGraph** and **Streamlit** for salary management decisions. This POC showcases how to build intelligent workflows that pause for human judgment before executing critical business actions.

<div align="center">

![Status](https://img.shields.io/badge/Status-Production%20Ready%20POC-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow%20Orchestration-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20UI-red)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

</div>

---

## 🎯 What This Project Demonstrates

This system demonstrates a **complete Human-in-the-Loop workflow** where:
- AI analyzes data and generates proposals
- **Workflow pauses** automatically for human review
- Humans can **Approve**, **Reject**, or **Modify** AI suggestions
- The system executes decisions and maintains complete audit logs

**Real-world use case:** HR managers reviewing and approving salary changes and team restructuring.

---

## 🏗️ Architecture & Approach

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                        │
│  (Data Viz, Department Analysis, Approval Interface)        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  LangGraph Workflow                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Load    │→ │ Analyze  │→ │  HITL    │→ │ Process  │   │
│  │  Data    │  │  Dept    │  │Interrupt │  │ Decision │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                    ↑ Pause for Human        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Data Layer (Excel)                         │
│         Employee Data, Salaries, Departments                 │
└─────────────────────────────────────────────────────────────┘
```

### HITL Workflow Pattern

1. **Load Data** → Reads employee data from Excel by department
2. **Analyze Department** → Identifies highest-paid employee, generates proposal
3. **HITL Interrupt** ⏸️ → Workflow pauses, waits for human decision
4. **Human Decision** → User chooses: Approve ✅ / Reject ❌ / Modify 📝
5. **Process Decision** → Executes the choice and logs the outcome

### State Management (LangGraph)

```python
WorkflowState = {
    department: str,              # Selected department
    employees: List[Dict],        # Employee data
    highest_paid: Dict,           # Highest-paid employee
    proposal_type: str,           # 'salary_hike' or 'manager_change'
    proposal_details: Dict,       # Proposal specifics
    human_decision: str,          # 'approve', 'reject', or 'modify'
    modification_details: Dict,   # Modified values if applicable
    final_status: str,            # Outcome
    execution_log: List[str]      # Audit trail
}
```

---

## ✨ Features Implemented

### 🔄 Three Decision Paths
- **Approve** ✅ - Accept proposal as-is
- **Reject** ❌ - Decline the proposal
- **Modify** 📝 - Adjust salary amount or manager choice

### 📊 Two Proposal Types
1. **Salary Hike** - Proposes 15% salary increase for top performer
2. **Manager Change** - Suggests reassignment to different manager


### 📈 Interactive UI
- **Data Overview Tab** - Employee list, salary distribution charts, statistics
- **Department Analysis Tab** - Analyze any department, see proposal
- **Approval Interface Tab** - Make decisions with interactive forms
- **Workflow History Tab** - Complete audit trail of all decisions

### 🔍 Complete Observability
- Execution logs at each step
- Workflow state persistence
- Full decision history
- Visual status indicators

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

```bash
# Navigate to project directory
cd d:\POCs\salary-hitl-system

# Install dependencies
pip install -r requirements.txt

# Generate dummy employee data
python generate_data.py
```

### Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: View Data (Data Overview Tab)
- Browse all employee records
- See salary distribution by department
- Review department statistics

### Step 2: Analyze a Department (Department Analysis Tab)
1. Select a department from dropdown
2. Click **"🔍 Analyze Department"**
3. System identifies highest-paid employee
4. AI generates a proposal (salary hike or manager change)

### Step 3: Make a Decision (Approval Interface Tab)

**Option A: Approve** ✅
- Review the proposal
- Click **"✅ Approve"**
- System executes immediately

**Option B: Reject** ❌
- Click **"❌ Reject"**
- Proposal is declined and logged

**Option C: Modify** 📝
- Click **"📝 Modify"**
- Adjust the proposed values:
  - For salary hike: Enter new salary amount
  - For manager change: Select different manager
- Submit the modification

### Step 4: Review History (Workflow History Tab)
- See all completed workflows
- Review execution logs
- Audit decision trail

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Workflow Engine** | LangGraph | State management, conditional routing, HITL interrupts |
| **UI Framework** | Streamlit | Interactive web interface |
| **Data Handling** | Pandas, OpenPyXL | Excel file operations, data manipulation |
| **Visualization** | Plotly | Interactive charts and graphs |
| **State Storage** | MemorySaver | Workflow checkpointing and persistence |

---

## 📁 Project Structure

```
salary-hitl-system/
├── src/
│   ├── state.py           # TypedDict state schema
│   ├── nodes.py           # Workflow node functions
│   │   ├── load_data_node()
│   │   ├── analyze_department_node()
│   │   ├── human_approval_node()      ← HITL interrupt
│   │   ├── process_approval_node()
│   │   ├── process_rejection_node()
│   │   └── process_modification_node()
│   └── workflow.py        # LangGraph workflow definition
│
├── data/
│   └── salary_data.xlsx   # Employee dataset
│
├── app.py                 # Streamlit application
├── generate_data.py       # Data generation script
├── requirements.txt       # Python dependencies
├── README.md             # This file
```

---

## 🎓 Key Concepts Demonstrated

### 1. Human-in-the-Loop Pattern
The workflow uses `interrupt_before=["human_approval"]` to pause execution:
```python
compiled_workflow = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_approval"]  # Stops here for human input
)
```

### 2. Conditional Routing
Different decisions route to different processing nodes:
```python
def route_decision(state):
    if state["human_decision"] == "approve":
        return "process_approval"
    elif state["human_decision"] == "reject":
        return "process_rejection"
    else:
        return "process_modification"
```

### 3. State Persistence
LangGraph's checkpointing maintains state across interactions:
```python
memory = MemorySaver()
config = {"configurable": {"thread_id": "thread_1"}}
```

### 4. Update State Mid-Flow
Human decisions update state while workflow is paused:
```python
graph.update_state(config, {"human_decision": "approve"})
graph.stream(None, config)  # Resume workflow
```

---

## 🔮 Future Enhancements

### 🤖 LLM Integration (When Data Is Available)
**Current:** Rule-based proposals  
**Future:** Intelligent proposals using LLM with:
- Performance review history
- Market salary benchmarks
- Team dynamics analysis
- Personalized justifications

**When to add:** Once you have real employee data including performance reviews, tenure, achievements, and historical salary data.

### ⚖️ Rules Engine
**Current:** Manual review for all proposals  
**Future:** Automated validation and auto-approval:

**Validation Rules:**
- Block raises exceeding 25%
- Prevent manager changes within 6 months
- Ensure salary caps by position

**Auto-Approve Rules:**
- Small raises under ₹50,000
- Routine transfers with same grade
- Budget-approved promotions

**Warning Rules:**
- Alert if salary exceeds ₹1.5 crore
- Flag if employee has performance warnings
- Check against department budget

### 📊 Enhanced Analytics
- Department budget tracking
- Salary trend analysis
- Approval rate metrics
- Time-to-decision analytics
- Comparative salary reports

### 🔐 Multi-Level Approval
- Manager approval → HR approval → CFO approval
- Different authority levels for different amounts
- Escalation workflows for exceptions

### 📧 Notifications
- Email alerts for pending approvals
- Slack integration for team updates
- SMS for urgent decisions

### 🗄️ Database Integration
- Replace Excel with PostgreSQL/MongoDB
- Real-time data sync
- Historical tracking and versioning

---

## 💡 Why This Approach?

### ✅ Advantages

**1. Demonstrates HITL Pattern Clearly**
- Clean separation of AI and human decision points
- Easy to understand workflow structure
- Shows value of human oversight

**2. Production-Ready Architecture**
- Scalable state management
- Proper error handling
- Complete audit trails

**3. Technology Stack Relevance**
- LangGraph is purpose-built for agent workflows
- Streamlit enables rapid UI development
- Pattern applies to many use cases

**4. Easy to Extend**
- Add new proposal types easily
- Integrate with real HR systems
- Scale to multiple approval levels

### 🎯 Use Cases Beyond Salary Management

This same HITL pattern can be applied to:
- **Loan Approvals** - Review AI-recommended loan decisions
- **Content Moderation** - Human review of flagged content
- **Medical Diagnosis** - Doctor reviews AI diagnosis suggestions
- **Legal Document Review** - Lawyer approves AI-drafted contracts
- **Financial Trading** - Trader approves AI-suggested trades
- **Customer Support** - Agent reviews AI-generated responses

---

## 🧪 Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing instructions.

**Quick Test:**
1. Analyze Finance department
2. Approve the proposal → See green success message
3. Analyze HR department  
4. Reject the proposal → See red rejection message
5. Analyze Marketing department
6. Modify the proposal → See yellow modification message

All three paths should work correctly with proper state management.

---

## 📊 Data Format

The Excel file contains:

| Column | Description | Example |
|--------|-------------|---------|
| Employee_ID | Unique identifier | 1001 |
| Name | Full name | Rajesh Sharma |
| Department | Department name | Engineering |
| Position | Job title | Senior Software Engineer |
| Current_Salary | Annual salary in ₹ | 9500000 |
| Manager | Manager name | Ramesh Iyer |
| Join_Date | Date joined | 2020-03-15 |

---

## 🤝 Contributing

To extend this POC:

**Add New Proposal Types:**
1. Define logic in `analyze_department_node()`
2. Add processing in new node function
3. Update conditional routing
4. Add UI elements in Streamlit

**Integrate Real Data:**
1. Replace `generate_data.py` with real data loader
2. Update Excel file path in `nodes.py`
3. Adjust proposal logic based on available fields

**Add Rules:**
1. Create `config/rules.json` with validation rules
2. Add `evaluate_rules_node()` in workflow
3. Update UI to display rule violations

---

