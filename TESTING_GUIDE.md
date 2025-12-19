# 🧪 Testing Guide for HITL Salary Management System

This guide will help you verify that all features of the HITL workflow are working correctly.

## ✅ Quick Verification Checklist

### 1. Data Overview Tab (📊)
**What to check:**
- [ ] Employee data table displays correctly
- [ ] You see metrics showing: Total Employees, Departments, Average Salary
- [ ] Salary distribution chart shows box plots for each department
- [ ] Department statistics table shows correct counts and averages

**Expected Results:**
- Should see ~30-35 employees across 5 departments (Engineering, Sales, Marketing, HR, Finance)
- Average salary should be around $90,000-$100,000
- Charts should be interactive (hover to see details)

---

### 2. Department Analysis Tab (🔍)
**What to check:**
- [ ] Dropdown shows all 5 departments
- [ ] "Analyze Department" button is visible
- [ ] After clicking analyze, you see "Highest-Paid Employee" section
- [ ] AI-generated proposal appears with either:
  - **Salary Hike** proposal (showing current salary, proposed salary, increase %)
  - **Manager Change** proposal (showing current manager, proposed manager)

**How to test:**
1. Select "Engineering" from dropdown
2. Click "🔍 Analyze Department" button
3. Wait for analysis to complete (should take 1-2 seconds)
4. Verify you see employee details and a proposal

**Expected Results:**
- Highest-paid employee info displays correctly
- Proposal box appears with blue background
- Proposal contains all relevant details
- Message says to go to "Approval Interface" tab

---

### 3. Approval Interface Tab (✅) - Main HITL Test

This is where you test the Human-in-the-Loop functionality!

#### Test A: Approve Flow
**Steps:**
1. Go to Approval Interface tab
2. Review the current proposal
3. Click **✅ Approve** button
4. Verify success message appears (green box with checkmark)
5. Check that the message shows the approved action

**Expected Results:**
- Green success box appears
- Message starts with "✅ APPROVED:"
- Shows the details of what was approved
- System status in sidebar shows "Workflow Complete"

#### Test B: Reject Flow
**Steps:**
1. Reset workflow (click "🔄 Reset Workflow" in sidebar)
2. Analyze a department again (choose different one)
3. Go to Approval Interface tab
4. Click **❌ Reject** button
5. Verify rejection message appears (red box)

**Expected Results:**
- Red error box appears
- Message starts with "❌ REJECTED:"
- Shows which proposal was rejected
- Workflow ends cleanly

#### Test C: Modify Flow - MOST IMPORTANT TEST!
**Steps:**
1. Reset workflow
2. Analyze a department again
3. Go to Approval Interface tab
4. Click **📝 Modify** button

**For Salary Hike Proposals:**
5. Modification form appears
6. Change the salary amount (e.g., increase or decrease)
7. Click "Submit Modification"
8. Verify yellow/warning box appears with modified values

**For Manager Change Proposals:**
5. Modification form appears with dropdown of managers
6. Select a different manager from the dropdown
7. Click "Submit Modification"
8. Verify yellow box shows the modified manager name

**Expected Results:**
- Yellow/orange box appears
- Message starts with "📝 MODIFIED:"
- Shows both original proposed value AND modified value
- Modified values should match what you entered

---

### 4. Workflow History Tab (📋)
**What to check:**
- [ ] History shows all completed workflows
- [ ] Each workflow entry shows: Department, Status, Result
- [ ] Execution log displays step-by-step actions
- [ ] Current workflow log updates in real-time

**How to test:**
1. Complete 2-3 workflows (approve one, reject one, modify one)
2. Go to Workflow History tab
3. Click on each workflow expander
4. Verify details are correct for each

**Expected Results:**
- Each workflow is numbered
- Status matches action taken (APPROVED, REJECTED, MODIFIED)
- Execution log shows logical progression
- Most recent workflow appears at the top

---

## 🔍 Key HITL Workflow Features to Verify

### ✨ Interrupt Behavior
**What to verify:**
- Workflow pauses after analysis and before decision
- You can switch between tabs while workflow is paused
- No automatic actions happen until you click a button
- State is preserved when switching tabs

**How to test:**
1. Analyze a department
2. Switch to Data Overview tab (workflow should stay paused)
3. Return to Approval Interface tab
4. Proposal should still be there, waiting for your decision

### ✨ State Persistence
**What to verify:**
- Workflow maintains state between interactions
- Refreshing the page doesn't lose current workflow
- Thread ID persists across decisions

**How to test:**
1. Start a workflow
2. Note the proposal details
3. Go to another tab and back
4. Verify proposal details are unchanged

### ✨ Decision Routing
**What to verify:**
- Each decision (approve/reject/modify) leads to different outcomes
- Conditional routing works correctly
- Workflow ends properly after each decision

**How to test:**
This is automatically tested by doing Test A, B, and C above!

---

## 🐛 Common Issues & Solutions

### Issue: "Salary data not found" error
**Solution:** Run `python generate_data.py` from the project directory

### Issue: Import errors or module not found
**Solution:** Ensure all packages are installed: `pip install -r requirements.txt`

### Issue: Workflow doesn't pause for approval
**Solution:** Check that `interrupt_before=["human_approval"]` is set in `src/workflow.py`

### Issue: Buttons don't respond
**Solution:** Click "Reset Workflow" in sidebar and try again

### Issue: Modified values don't show correctly
**Solution:** Check console for errors; ensure modification form submitted properly

---

## 🎯 Success Criteria

Your HITL system is working correctly if:

✅ All three decision options (Approve/Reject/Modify) work  
✅ Workflow pauses at approval step (HITL interrupt)  
✅ Highest-paid employee is correctly identified  
✅ Proposals are generated with reasonable data  
✅ UI updates correctly after each decision  
✅ Workflow history tracks all executions  
✅ State persists across tab switches  
✅ Modified values are applied correctly  

---

## 📸 What to Look For in Each State

### ⏸️ Waiting for Approval State
- Sidebar shows: "Awaiting Human Decision"
- Approval Interface shows three buttons
- Proposal box has blue background
- No final status message yet

### ✅ Approved State
- Green success box with checkmark
- Final message shows approved details
- Sidebar shows: "Workflow Complete"
- Can reset and start new workflow

### ❌ Rejected State
- Red error box with X mark
- Clear rejection message
- Sidebar shows: "Workflow Complete"

### 📝 Modified State
- Yellow/orange warning box with pencil icon
- Shows both original and modified values
- Sidebar shows: "Workflow Complete"

---

## 🚀 Advanced Testing

### Test Multiple Departments
Run the workflow for each department to see variety:
- Engineering (usually highest salaries)
- Sales (commission-based salaries)
- Marketing (mid-range salaries)
- HR (lower-mid range salaries)
- Finance (CFO will be highest paid)

### Test Edge Cases
1. **Modify to same value:** Change salary to the same as proposed
2. **Large modifications:** Change salary by a huge amount
3. **Rapid decisions:** Make multiple approve/reject cycles quickly

### Verify Data Integrity
1. Check that employee IDs are unique
2. Verify salary ranges are realistic for positions
3. Confirm all departments have multiple employees
4. Check that managers exist in the system

---

## 📊 Expected Behavior Summary

| Action | Expected Result | Visual Indicator |
|--------|-----------------|------------------|
| Analyze Department | Proposal generated | Blue proposal box |
| Approve | Changes accepted | Green success box |
| Reject | Changes declined | Red error box |
| Modify | New values applied | Yellow warning box |
| Reset | Clean state | "No Active Workflow" |

---

## 💡 Pro Tips

1. **Test Modify First:** The modify flow is the most complex - test it thoroughly!
2. **Watch the Logs:** Execution logs show each step of the workflow
3. **Use Different Departments:** Each department has different salary ranges
4. **Check State Changes:** Notice how sidebar status updates with each action
5. **History Tracking:** Build up history to see how it displays multiple workflows

---

Happy Testing! 🎉

If all tests pass, your HITL workflow system is fully functional! 🚀
