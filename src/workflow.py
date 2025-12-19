"""
LangGraph workflow definition for HITL salary management.
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import WorkflowState
from . import nodes


def create_workflow():
    """Create and compile the LangGraph workflow."""
    
    # Create the graph
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("load_data", nodes.load_data_node)
    workflow.add_node("analyze_department", nodes.analyze_department_node)
    workflow.add_node("human_approval", nodes.human_approval_node)
    workflow.add_node("process_approval", nodes.process_approval_node)
    workflow.add_node("process_rejection", nodes.process_rejection_node)
    workflow.add_node("process_modification", nodes.process_modification_node)
    
    # Define edges
    workflow.set_entry_point("load_data")
    workflow.add_edge("load_data", "analyze_department")
    workflow.add_edge("analyze_department", "human_approval")
    
    # Conditional routing after human approval
    def route_decision(state: WorkflowState) -> str:
        """Route based on human decision."""
        decision = state.get("human_decision")
        
        if decision == "approve":
            return "process_approval"
        elif decision == "reject":
            return "process_rejection"
        elif decision == "modify":
            return "process_modification"
        else:
            # If no decision yet, stay at human_approval (shouldn't happen in practice)
            return "human_approval"
    
    workflow.add_conditional_edges(
        "human_approval",
        route_decision,
        {
            "process_approval": "process_approval",
            "process_rejection": "process_rejection",
            "process_modification": "process_modification",
            "human_approval": "human_approval"
        }
    )
    
    # All processing nodes lead to END
    workflow.add_edge("process_approval", END)
    workflow.add_edge("process_rejection", END)
    workflow.add_edge("process_modification", END)
    
    # Compile with memory saver for checkpointing
    memory = MemorySaver()
    compiled_workflow = workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_approval"]  # HITL interrupt
    )
    
    return compiled_workflow


# Create a singleton instance
graph = create_workflow()
