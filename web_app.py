"""
Flask web server for HITL Salary Management System
A lightweight alternative to Streamlit
"""
from flask import Flask, render_template, request, jsonify, session
import sys
from pathlib import Path
import pandas as pd
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.workflow import graph
from src.state import WorkflowState

app = Flask(__name__)
app.secret_key = 'hitl-demo-secret-key-change-in-production'

# Global store for workflow states
workflow_states = {}


def load_salary_data():
    """Load salary data from Excel."""
    data_path = Path(__file__).parent / "data" / "salary_data.xlsx"
    return pd.read_excel(data_path)


@app.route('/')
def index():
    """Render main page."""
    df = load_salary_data()
    departments = sorted(df['Department'].unique())
    
    # Get department stats
    dept_stats = []
    for dept in departments:
        dept_df = df[df['Department'] == dept]
        dept_stats.append({
            'name': dept,
            'count': len(dept_df),
            'avg_salary': int(dept_df['Current_Salary'].mean())
        })
    
    return render_template('index.html', departments=dept_stats)


@app.route('/analyze', methods=['POST'])
def analyze_department():
    """Analyze department and generate proposal."""
    data = request.json
    department = data.get('department')
    
    # Create unique thread ID
    thread_id = f"web_{id(department)}"
    session['thread_id'] = thread_id
    
    # Run workflow until HITL interrupt
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "department": department,
        "employees": [],
        "execution_log": []
    }
    
    result = None
    for event in graph.stream(initial_state, config, stream_mode="values"):
        result = event
    
    # Store state for later
    workflow_states[thread_id] = result
    
    # Return proposal data
    if result and result.get('proposal_details'):
        return jsonify({
            'success': True,
            'highest_paid': {
                'name': result['highest_paid']['Name'],
                'position': result['highest_paid']['Position'],
                'salary': result['highest_paid']['Current_Salary'],
                'manager': result['highest_paid']['Manager'],
                'department': result['highest_paid']['Department']
            },
            'proposal': {
                'type': result['proposal_type'],
                'details': result['proposal_details']
            },
            'employees': result.get('employees', [])
        })
    else:
        return jsonify({'success': False, 'error': 'No data found'}), 400


@app.route('/decide', methods=['POST'])
def process_decision():
    """Process human decision."""
    data = request.json
    decision = data.get('decision')
    modification = data.get('modification')
    
    thread_id = session.get('thread_id')
    if not thread_id:
        return jsonify({'success': False, 'error': 'No active workflow'}), 400
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Update state with decision
    update_data = {"human_decision": decision}
    if modification:
        update_data["modification_details"] = modification
    
    graph.update_state(config, update_data)
    
    # Resume workflow
    final_result = None
    for event in graph.stream(None, config, stream_mode="values"):
        final_result = event
    
    # Return result
    if final_result:
        return jsonify({
            'success': True,
            'status': final_result.get('final_status'),
            'message': final_result.get('final_message'),
            'log': final_result.get('execution_log', [])
        })
    else:
        return jsonify({'success': False, 'error': 'Workflow failed'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  HITL Salary Management System - Web UI")
    print("="*60)
    print("\n  🚀 Starting server at http://localhost:5000")
    print("  📝 Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000)
