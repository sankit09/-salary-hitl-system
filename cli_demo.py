"""
Command-line demo of the HITL Salary Management System.
Run this to see the workflow in action without Streamlit UI.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.workflow import graph
from src.state import WorkflowState
import pandas as pd


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text):
    """Print a formatted section."""
    print(f"\n--- {text} ---")


def load_salary_data():
    """Load salary data from Excel."""
    data_path = Path(__file__).parent / "data" / "salary_data.xlsx"
    if not data_path.exists():
        print(f"❌ Error: Data file not found at {data_path}")
        print("Please run: python generate_data.py")
        sys.exit(1)
    return pd.read_excel(data_path)


def display_employee(employee, label="Employee"):
    """Display employee details."""
    print(f"\n{label}:")
    print(f"  Name: {employee['Name']}")
    print(f"  Position: {employee['Position']}")
    print(f"  Department: {employee['Department']}")
    print(f"  Current Salary: ₹{employee['Current_Salary']:,}")
    print(f"  Manager: {employee['Manager']}")
    print(f"  Join Date: {employee['Join_Date']}")


def display_proposal(proposal_type, proposal_details):
    """Display proposal details."""
    print_section("AI-Generated Proposal")
    
    if proposal_type == 'salary_hike':
        print(f"📊 Proposal Type: SALARY HIKE")
        print(f"  Employee: {proposal_details['employee_name']}")
        print(f"  Current Salary: ₹{proposal_details['current_salary']:,}")
        print(f"  Proposed Salary: ₹{proposal_details['proposed_salary']:,}")
        increase = proposal_details['proposed_salary'] - proposal_details['current_salary']
        print(f"  Increase: {proposal_details['increase_percentage']}% (₹{increase:,})")
        print(f"  Reason: {proposal_details['reason']}")
    else:  # manager_change
        print(f"👔 Proposal Type: MANAGER CHANGE")
        print(f"  Employee: {proposal_details['employee_name']}")
        print(f"  Current Manager: {proposal_details['current_manager']}")
        print(f"  Proposed Manager: {proposal_details['proposed_manager']}")
        print(f"  Reason: {proposal_details['reason']}")


def get_user_decision():
    """Prompt user for decision."""
    print_section("Your Decision")
    print("What would you like to do?")
    print("  1. ✅ Approve")
    print("  2. ❌ Reject")
    print("  3. 📝 Modify")
    print()
    
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == '1':
            return 'approve', None
        elif choice == '2':
            return 'reject', None
        elif choice == '3':
            return 'modify', None
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def get_modification(proposal_type, proposal_details, employees):
    """Get modification details from user."""
    print_section("Modify Proposal")
    
    if proposal_type == 'salary_hike':
        current = proposal_details['current_salary']
        proposed = proposal_details['proposed_salary']
        print(f"Current Salary: ₹{current:,}")
        print(f"Proposed Salary: ₹{proposed:,}")
        print()
        
        while True:
            try:
                new_salary = input(f"Enter new salary amount (min ₹{current:,}): ").strip()
                new_salary = int(new_salary.replace(',', ''))
                if new_salary >= current:
                    return {'modified_salary': new_salary}
                else:
                    print(f"❌ Salary must be at least ₹{current:,}")
            except ValueError:
                print("❌ Please enter a valid number")
    else:  # manager_change
        current_manager = proposal_details['current_manager']
        proposed_manager = proposal_details['proposed_manager']
        
        # Get list of potential managers from employees
        potential_managers = [e['Name'] for e in employees 
                            if e['Employee_ID'] != proposal_details['employee_id']]
        
        print(f"Current Manager: {current_manager}")
        print(f"Proposed Manager: {proposed_manager}")
        print(f"\nAvailable managers:")
        for i, manager in enumerate(potential_managers, 1):
            print(f"  {i}. {manager}")
        print()
        
        while True:
            try:
                choice = input(f"Enter manager number (1-{len(potential_managers)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(potential_managers):
                    return {'modified_manager': potential_managers[idx]}
                else:
                    print(f"❌ Please enter a number between 1 and {len(potential_managers)}")
            except ValueError:
                print("❌ Please enter a valid number")


def display_result(final_status, final_message):
    """Display final result."""
    print_section("Workflow Result")
    
    if final_status == 'approved':
        print("✅ " + final_message)
    elif final_status == 'rejected':
        print("❌ " + final_message)
    elif final_status == 'modified':
        print("📝 " + final_message)
    else:
        print(final_message)


def display_execution_log(log_entries):
    """Display execution log."""
    print_section("Execution Log")
    for i, entry in enumerate(log_entries, 1):
        print(f"  {i}. {entry}")


def main():
    """Main CLI workflow."""
    print_header("HITL Salary Management System - CLI Demo")
    print("Human-in-the-Loop Workflow powered by LangGraph")
    
    # Load data
    print_section("Loading Data")
    df = load_salary_data()
    departments = sorted(df['Department'].unique())
    
    print(f"✅ Loaded {len(df)} employees across {len(departments)} departments")
    print(f"Departments: {', '.join(departments)}")
    
    # Select department
    print_section("Select Department")
    for i, dept in enumerate(departments, 1):
        count = len(df[df['Department'] == dept])
        avg_salary = df[df['Department'] == dept]['Current_Salary'].mean()
        print(f"  {i}. {dept} ({count} employees, avg: ₹{avg_salary:,.0f})")
    
    print()
    while True:
        try:
            choice = input(f"Enter department number (1-{len(departments)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(departments):
                selected_dept = departments[idx]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(departments)}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Initialize workflow
    print_section(f"Analyzing {selected_dept} Department")
    print("🔄 Running workflow...")
    
    config = {"configurable": {"thread_id": "cli_demo_thread"}}
    initial_state = {
        "department": selected_dept,
        "employees": [],
        "execution_log": []
    }
    
    # Run workflow until HITL interrupt
    result = None
    for event in graph.stream(initial_state, config, stream_mode="values"):
        result = event
    
    # Display analysis results
    if result and result.get('highest_paid'):
        display_employee(result['highest_paid'], "🏆 Highest-Paid Employee")
    
    if result and result.get('proposal_details'):
        display_proposal(result['proposal_type'], result['proposal_details'])
    
    # Get human decision
    print("\n⏸️  WORKFLOW PAUSED - Waiting for Human Decision")
    decision, mod_details = get_user_decision()
    
    # Get modification details if needed
    if decision == 'modify':
        mod_details = get_modification(
            result['proposal_type'],
            result['proposal_details'],
            result['employees']
        )
    
    # Update state with decision
    print_section("Processing Decision")
    print("🔄 Updating workflow state...")
    
    update_data = {"human_decision": decision}
    if mod_details:
        update_data["modification_details"] = mod_details
    
    graph.update_state(config, update_data)
    
    # Continue workflow
    print("▶️  Resuming workflow...")
    final_result = None
    for event in graph.stream(None, config, stream_mode="values"):
        final_result = event
    
    # Display results
    if final_result:
        display_result(final_result.get('final_status'), final_result.get('final_message'))
        display_execution_log(final_result.get('execution_log', []))
    
    print_header("Workflow Complete")
    print("\n✅ Thank you for using the HITL Salary Management System!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Workflow cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
