"""
Workflow node functions for the HITL salary management system.
"""
import pandas as pd
import random
from pathlib import Path
from typing import Dict, Any
from .state import WorkflowState


def load_data_node(state: WorkflowState) -> Dict[str, Any]:
    """Load employee data and filter by department."""
    print(f"[Node] Loading data for department: {state['department']}")
    
    # Load Excel data
    data_path = Path(__file__).parent.parent / "data" / "salary_data.xlsx"
    df = pd.read_excel(data_path)
    
    # Filter by department
    dept_df = df[df['Department'] == state['department']]
    employees = dept_df.to_dict('records')
    
    log_entry = f"Loaded {len(employees)} employees from {state['department']} department"
    
    return {
        "employees": employees,
        "execution_log": state.get("execution_log", []) + [log_entry]
    }


def analyze_department_node(state: WorkflowState) -> Dict[str, Any]:
    """Identify highest-paid employee and generate a proposal."""
    print("[Node] Analyzing department data")
    
    employees = state['employees']
    
    if not employees:
        return {
            "final_status": "no_data",
            "final_message": "No employees found in this department",
            "execution_log": state.get("execution_log", []) + ["No employees found"]
        }
    
    # Find highest-paid employee
    highest_paid = max(employees, key=lambda x: x['Current_Salary'])
    
    # Generate proposal (alternating between salary hike and manager change)
    proposal_type = random.choice(['salary_hike', 'manager_change'])
    
    if proposal_type == 'salary_hike':
        current_salary = highest_paid['Current_Salary']
        proposed_salary = int(current_salary * 1.15)  # 15% hike
        proposal_details = {
            'employee_id': highest_paid['Employee_ID'],
            'employee_name': highest_paid['Name'],
            'current_salary': current_salary,
            'proposed_salary': proposed_salary,
            'increase_percentage': 15,
            'reason': f"Top performer in {state['department']} department"
        }
    else:  # manager_change
        # Suggest a new manager from the same department (excluding the employee)
        potential_managers = [e for e in employees if e['Employee_ID'] != highest_paid['Employee_ID']]
        if potential_managers:
            new_manager = random.choice(potential_managers)
            proposal_details = {
                'employee_id': highest_paid['Employee_ID'],
                'employee_name': highest_paid['Name'],
                'current_manager': highest_paid['Manager'],
                'proposed_manager': new_manager['Name'],
                'reason': f"Reassignment for better team dynamics in {state['department']}"
            }
        else:
            # Fall back to salary hike if no other employees
            proposal_type = 'salary_hike'
            current_salary = highest_paid['Current_Salary']
            proposed_salary = int(current_salary * 1.15)
            proposal_details = {
                'employee_id': highest_paid['Employee_ID'],
                'employee_name': highest_paid['Name'],
                'current_salary': current_salary,
                'proposed_salary': proposed_salary,
                'increase_percentage': 15,
                'reason': f"Top performer in {state['department']} department"
            }
    
    log_entry = f"Identified highest-paid: {highest_paid['Name']} (₹{highest_paid['Current_Salary']:,}). Proposal: {proposal_type}"
    
    return {
        "highest_paid": highest_paid,
        "proposal_type": proposal_type,
        "proposal_details": proposal_details,
        "execution_log": state.get("execution_log", []) + [log_entry]
    }


def human_approval_node(state: WorkflowState) -> Dict[str, Any]:
    """HITL interrupt point - waits for human decision."""
    print("[Node] Waiting for human approval...")
    
    # This node doesn't modify state, it just serves as the interrupt point
    # The human decision will be set externally through the workflow update
    
    log_entry = "Workflow paused for human review"
    
    return {
        "execution_log": state.get("execution_log", []) + [log_entry]
    }


def process_approval_node(state: WorkflowState) -> Dict[str, Any]:
    """Process an approved proposal."""
    print("[Node] Processing approval")
    
    proposal_type = state['proposal_type']
    proposal_details = state['proposal_details']
    
    if proposal_type == 'salary_hike':
        message = (
            f"✅ APPROVED: Salary hike for {proposal_details['employee_name']} "
            f"from ₹{proposal_details['current_salary']:,} to ₹{proposal_details['proposed_salary']:,}"
        )
    else:  # manager_change
        message = (
            f"✅ APPROVED: Manager change for {proposal_details['employee_name']} "
            f"from {proposal_details['current_manager']} to {proposal_details['proposed_manager']}"
        )
    
    log_entry = f"Proposal approved: {proposal_type} for {proposal_details['employee_name']}"
    
    return {
        "final_status": "approved",
        "final_message": message,
        "execution_log": state.get("execution_log", []) + [log_entry]
    }


def process_rejection_node(state: WorkflowState) -> Dict[str, Any]:
    """Process a rejected proposal."""
    print("[Node] Processing rejection")
    
    proposal_details = state['proposal_details']
    message = f"❌ REJECTED: Proposal for {proposal_details['employee_name']} was rejected"
    
    log_entry = f"Proposal rejected for {proposal_details['employee_name']}"
    
    return {
        "final_status": "rejected",
        "final_message": message,
        "execution_log": state.get("execution_log", []) + [log_entry]
    }


def process_modification_node(state: WorkflowState) -> Dict[str, Any]:
    """Process a modified proposal."""
    print("[Node] Processing modification")
    
    proposal_type = state['proposal_type']
    proposal_details = state['proposal_details']
    modification_details = state['modification_details']
    
    if proposal_type == 'salary_hike':
        modified_salary = modification_details.get('modified_salary', proposal_details['proposed_salary'])
        message = (
            f"📝 MODIFIED: Salary hike for {proposal_details['employee_name']} "
            f"from ₹{proposal_details['current_salary']:,} to ₹{modified_salary:,} "
            f"(originally proposed: ₹{proposal_details['proposed_salary']:,})"
        )
        log_entry = f"Proposal modified: salary changed to ₹{modified_salary:,}"
    else:  # manager_change
        modified_manager = modification_details.get('modified_manager', proposal_details['proposed_manager'])
        message = (
            f"📝 MODIFIED: Manager change for {proposal_details['employee_name']} "
            f"to {modified_manager} "
            f"(originally proposed: {proposal_details['proposed_manager']})"
        )
        log_entry = f"Proposal modified: manager changed to {modified_manager}"
    
    return {
        "final_status": "modified",
        "final_message": message,
        "execution_log": state.get("execution_log", []) + [log_entry]
    }
