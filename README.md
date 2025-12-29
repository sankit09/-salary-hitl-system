# HITL Salary Management System 💼

A **Human-in-the-Loop (HITL)** workflow system using **LangGraph** and **Flask** for salary management decisions. This project demonstrates how AI-powered workflows can pause for human judgment before executing critical business actions.

![Status](https://img.shields.io/badge/Status-Production%20Ready-green) ![Flask](https://img.shields.io/badge/Flask-Web%20UI-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange)

---

## 🎯 What This System Does

**AI analyzes → Workflow pauses ⏸️ → Human decides → System executes**

This is a complete demonstration of the HITL pattern where:
- AI analyzes employee data and generates salary/manager change proposals
- Workflow **automatically pauses** for human review
- Humans can **Approve** ✅, **Reject** ❌, or **Modify** 📝 the proposals
- System tracks complete history showing what was changed

---

## ✨ Key Features

### 🎨 **Beautiful Web Interface**
- Modern gradient design with purple theme
- Responsive card-based layout
- Smooth animations and hover effects
- Color-coded status indicators

### 📜 **Workflow History**
- Shows ALL previous decisions
- **Displays original vs modified values** for modifications
- Shows proposal details for approved and rejected workflows
- Color-coded badges (Green/Red/Yellow)
- Persistent storage using localStorage

### 🔄 **Three Decision Paths**
1. **Approve** ✅ - Accept the AI proposal as-is
2. **Reject** ❌ - Decline the proposal
3. **Modify** 📝 - Change the proposed values before executing

### 📊 **Two Proposal Types**
- **Salary Hike** - AI proposes percentage increase with justification
- **Manager Change** - AI suggests reassignment to different manager

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

```bash
# Navigate to project directory
cd d:\POCs\salary-hitl-system

# Activate virtual environment (if using one)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Sample Data

```bash
# Creates data/salary_data.xlsx with 31 employees
python generate_data.py
```

### Run the Application

```bash
# Start Flask web server
python web_app.py
```

The application will start at **http://localhost:5000**

---

## 📖 How to Use

### Step 1: Select Department
- View all departments with employee count and average salary
- Click on any department card to select it
- Click **"🔍 Analyze Department"**

### Step 2: Review Proposal
System shows:
- 🏆 **Highest-paid employee** details (name, position, current salary, manager)
- 📊 **AI-generated proposal** with reasoning

**Example Salary Hike Proposal:**
```
Employee: Rohan Malhotra
Current Salary: ₹16,544,831
Proposed Salary: ₹19,026,555
Increase: 15% (₹2,481,724)
Reason: Top performer in Finance department
```

### Step 3: Make Your Decision

**Option A: Approve** ✅
- Click "✅ Approve"
- Proposal executes immediately
- History shows: "Approved Salary Hike: Current: ₹16.5L → Proposed: ₹19L (+15%)"

**Option B: Reject** ❌
- Click "❌ Reject"
- Proposal is declined
- History shows: "Rejected Salary Hike: Proposed ₹19L was not approved"

**Option C: Modify** 📝
- Click "📝 Modify"
- Enter new values:
  - For salary: Enter custom amount
  - For manager: Select from dropdown
- Click "Submit Modification"
- History shows: "Original: ₹19L → Modified: ₹18L"

### Step 4: View History
Scroll down to see **Workflow History** section showing:
- All previous workflows numbered (#1, #2, #3...)
- Department, employee, timestamp
- Status badge (APPROVED/REJECTED/MODIFIED)
- **Original vs modified values** highlighted

---

## 📊 Workflow History Examples

### Modified Salary:
```
Workflow #3 - MODIFIED
Department: Finance
Employee: Rohan Malhotra
Time: 29/12/2025, 3:15 PM

Salary Change:
Original Proposed: ₹19,026,555  (crossed out)
Modified To: ₹18,000,000        (bold)
```

### Approved:
```
Workflow #2 - APPROVED
Department: Engineering
Employee: Arjun Patel
Time: 29/12/2025, 3:10 PM

✅ Approved Salary Hike:
Current: ₹9,500,000
Proposed: ₹10,925,000 (+15%)
```

### Rejected:
```
Workflow #1 - REJECTED
Department: HR
Employee: Priya Singh
Time: 29/12/2025, 3:05 PM

❌ Rejected Manager Change:
From: Amit Kumar
To: Rajesh Sharma
```

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────┐
│         Flask Web Server                 │
│  (web_app.py - API endpoints)           │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         HTML/CSS/JavaScript              │
│  (templates/index.html)                  │
│  - Beautiful UI                          │
│  - Workflow history                      │
│  - localStorage for persistence          │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         LangGraph Workflow               │
│  ┌──────┐  ┌──────┐  ┌─────┐  ┌─────┐ │
│  │Load  │→ │Analyze│→ │HITL │→ │Process│
│  │Data  │  │Dept  │  │Pause│  │Decision│
│  └──────┘  └──────┘  └─────┘  └─────┘ │
│              ↑ AI proposes              │
│              ⏸️ Pauses here for human   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│         Excel Data Layer                 │
│      data/salary_data.xlsx               │
└─────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Flask | Lightweight web server |
| **Workflow Engine** | LangGraph | State management, HITL interrupts |
| **Frontend** | HTML/CSS/JS | Modern responsive UI |
| **Data** | Pandas + Excel | Employee data handling |
| **State Persistence** | MemorySaver | Workflow checkpointing |
| **History Storage** | localStorage | Browser-side history |

---

## 📁 Project Structure

```
salary-hitl-system/
├── web_app.py              # Flask server (API endpoints)
├── templates/
│   └── index.html          # Web UI with workflow history
├── src/
│   ├── state.py            # Workflow state schema
│   ├── nodes.py            # Workflow logic nodes
│   └── workflow.py         # LangGraph graph definition
├── data/
│   └── salary_data.xlsx    # Employee data
├── generate_data.py        # Data generator script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🎓 Key HITL Concepts Demonstrated

### 1. **Workflow Interrupts**
```python
compiled_workflow = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_approval"]  # Pauses here
)
```

### 2. **State Persistence**
```python
config = {"configurable": {"thread_id": "unique_id"}}
# State is saved automatically at interrupt point
```

### 3. **Human Decision Integration**
```python
# Update state with human choice
graph.update_state(config, {"human_decision": "approve"})
# Resume workflow
graph.stream(None, config)
```

### 4. **Conditional Routing**
```python
def route_decision(state):
    if state["human_decision"] == "approve":
        return "process_approval"
    elif state["human_decision"] == "reject":
        return "process_rejection"
    else:
        return "process_modification"
```

---

## 🔮 Use Cases Beyond Salary Management

This HITL pattern applies to:
- 💰 **Loan Approvals** - AI recommends, banker approves
- 📝 **Content Moderation** - AI flags, human reviews
- 🏥 **Medical Diagnosis** - AI suggests, doctor confirms
- ⚖️ **Legal Contracts** - AI drafts, lawyer approves
- 📈 **Trading Decisions** - AI signals, trader executes
- 🛡️ **Security Alerts** - AI detects, analyst investigates

---

## 📊 Sample Data

The system uses Indian employee data:

| Field | Description | Example |
|-------|-------------|---------|
| Employee_ID | Unique identifier | 1001 |
| Name | Indian names | Rajesh Sharma, Priya Singh |
| Department | Department name | Engineering, Finance, HR |
| Position | Job title | Software Engineer, CFO |
| Current_Salary | Annual salary (₹) | ₹9,500,000 |
| Manager | Manager name | Ramesh Iyer |
| Join_Date | Date joined | 2020-03-15 |

**Salary Ranges (in Rupees):**
- Software Engineer: ₹58L - ₹75L
- Senior Software Engineer: ₹79L - ₹1Cr
- Engineering Manager: ₹1.16Cr - ₹1.41Cr
- CFO: ₹1.25Cr - ₹1.66Cr

---

## 🎨 UI Design Features

### Color Scheme
- **Primary:** Purple gradient (#667eea → #764ba2)
- **Success:** Green (#d4edda, #28a745)
- **Danger:** Red (#f8d7da, #dc3545)
- **Warning:** Yellow (#fff3cd, #ffc107)

### Interactive Elements
- Hover effects on department cards
- Smooth transitions and animations
- Responsive grid layout
- Color-coded status badges
- Value comparison highlights

### Accessibility
- Clear typography (Segoe UI)
- High contrast for readability
- Responsive design (mobile-friendly)
- Intuitive button placement

---

## 🧪 Testing Workflow

**Test All Three Decision Paths:**

1. **Approve Test:**
   - Select Finance department
   - Click Analyze
   - Click ✅ Approve
   - Check history shows green "APPROVED" badge with proposal details

2. **Reject Test:**
   - Select HR department
   - Click Analyze  
   - Click ❌ Reject
   - Check history shows red "REJECTED" badge with what was rejected

3. **Modify Test:**
   - Select Engineering department
   - Click Analyze
   - Click 📝 Modify
   - Change salary to custom amount (e.g., 18000000)
   - Submit
   - Check history shows yellow "MODIFIED" with original vs modified values

---

## 🔧 Configuration

### Port Configuration
Default: `5000`

To change port, edit `web_app.py`:
```python
app.run(debug=True, port=YOUR_PORT)
```

### Data Configuration
To regenerate data with different parameters, edit `generate_data.py`:
```python
num_employees = 31  # Change employee count
departments = [...]  # Add/remove departments
salary_ranges = {...}  # Adjust salary ranges
```

---

## 📝 Dependencies

```
flask==3.0.0
langgraph==0.0.1
langchain-core==0.1.0
pandas==2.0.0
openpyxl==3.1.0
```

Install all: `pip install -r requirements.txt`

---

## 🚦 Troubleshooting

**Port 5000 already in use:**
```bash
# Change port in web_app.py or kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Data file not found:**
```bash
# Regenerate data
python generate_data.py
```

**History not showing:**
- Clear browser localStorage: F12 → Application → Local Storage → Clear
- Refresh page
- Make a new decision to populate history

---

## 📚 Additional Resources

- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **HITL Patterns:** Human-in-the-Loop AI systems

---

## 🤝 Alternative Interfaces

This project also includes:

**Streamlit UI:**
```bash
streamlit run app.py
```

**CLI Demo:**
```bash
python cli_demo.py
```

The Flask HTML UI is recommended for production use due to better customization and control.

---

## 📄 License

Educational/Demo project for HITL workflow patterns with LangGraph.

---

<div align="center">

**Built with ❤️ using Flask + LangGraph**

**Status:** ✅ Production-Ready | Fully Functional HITL Workflow

</div>
