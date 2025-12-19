"""
State schema for the HITL salary management workflow.
"""
from typing import TypedDict, Optional, List, Dict, Any


class WorkflowState(TypedDict):
    """State schema for the salary management workflow."""
    
    # Input
    department: str
    
    # Data
    employees: List[Dict[str, Any]]
    highest_paid: Optional[Dict[str, Any]]
    
    # Proposal
    proposal_type: Optional[str]  # 'salary_hike' or 'manager_change'
    proposal_details: Optional[Dict[str, Any]]
    
    # Human decision
    human_decision: Optional[str]  # 'approve', 'reject', or 'modify'
    modification_details: Optional[Dict[str, Any]]
    
    # Results
    final_status: Optional[str]
    final_message: Optional[str]
    execution_log: List[str]
