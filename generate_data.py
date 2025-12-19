"""
Script to generate dummy salary data for the HITL system.
"""
import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Department definitions
departments = {
    'Engineering': ['Software Engineer', 'Senior Software Engineer', 'Tech Lead', 'Engineering Manager'],
    'Sales': ['Sales Representative', 'Senior Sales Rep', 'Sales Manager', 'VP Sales'],
    'Marketing': ['Marketing Specialist', 'Marketing Manager', 'Content Creator', 'Marketing Director'],
    'HR': ['HR Specialist', 'HR Manager', 'Recruiter', 'HR Director'],
    'Finance': ['Financial Analyst', 'Senior Analyst', 'Finance Manager', 'CFO']
}

# Manager names by department
managers = {
    'Engineering': ['Ramesh Iyer', 'Lakshmi Reddy'],
    'Sales': ['Suresh Kapoor', 'Swati Malhotra'],
    'Marketing': ['Rajiv Sharma', 'Swati Desai'],
    'HR': ['Sunita Kulkarni', 'Ashok Mehta'],
    'Finance': ['Sanjana Gupta', 'Prakash Nair']
}

# Indian first names and last names for generating employee names
first_names = [
    'Rajesh', 'Priya', 'Amit', 'Anjali', 'Vikram', 'Kavya', 'Arjun', 'Sneha',
    'Rohan', 'Pooja', 'Karan', 'Neha', 'Aditya', 'Riya', 'Rahul',
    'Meera', 'Sanjay', 'Divya', 'Nikhil', 'Shalini', 'Varun', 'Ananya',
    'Manish', 'Shreya', 'Akash', 'Ishita', 'Abhishek', 'Nisha', 'Vishal', 'Deepika'
]

last_names = [
    'Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Gupta', 'Verma', 'Mehta',
    'Nair', 'Iyer', 'Rao', 'Desai', 'Joshi', 'Agarwal', 'Kulkarni',
    'Chopra', 'Malhotra', 'Kapoor', 'Khanna', 'Bhatia', 'Shah', 'Pillai', 'Menon',
    'Sethi', 'Shetty', 'Bansal', 'Jain', 'Yadav', 'Chawla', 'Naidu'
]

# Salary ranges by position in Indian Rupees (₹)
salary_ranges = {
    'Software Engineer': (5800000, 7500000),
    'Senior Software Engineer': (7900000, 10000000),
    'Tech Lead': (10400000, 12500000),
    'Engineering Manager': (11600000, 14100000),
    'Sales Representative': (4200000, 5800000),
    'Senior Sales Rep': (6200000, 7900000),
    'Sales Manager': (7500000, 10000000),
    'VP Sales': (10800000, 13300000),
    'Marketing Specialist': (4600000, 6200000),
    'Marketing Manager': (6600000, 8700000),
    'Content Creator': (5000000, 6600000),
    'Marketing Director': (9100000, 11600000),
    'HR Specialist': (4600000, 5800000),
    'HR Manager': (6200000, 7900000),
    'Recruiter': (4800000, 6200000),
    'HR Director': (8300000, 10800000),
    'Financial Analyst': (5400000, 7100000),
    'Senior Analyst': (7500000, 9500000),
    'Finance Manager': (8700000, 11200000),
    'CFO': (12500000, 16600000)
}

def generate_random_date(start_year=2018, end_year=2023):
    """Generate a random join date."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def generate_employees():
    """Generate employee data."""
    employees = []
    employee_id = 1001
    used_names = set()
    
    for dept, positions in departments.items():
        # Generate 5-7 employees per department
        num_employees = random.randint(5, 7)
        
        for i in range(num_employees):
            # Generate unique name
            while True:
                first = random.choice(first_names)
                last = random.choice(last_names)
                name = f"{first} {last}"
                if name not in used_names:
                    used_names.add(name)
                    break
            
            # Assign position
            position = random.choice(positions)
            
            # Generate salary within range
            min_sal, max_sal = salary_ranges[position]
            salary = random.randint(min_sal, max_sal)
            
            # Assign manager
            manager = random.choice(managers[dept])
            
            # Generate join date
            join_date = generate_random_date()
            
            employees.append({
                'Employee_ID': employee_id,
                'Name': name,
                'Department': dept,
                'Position': position,
                'Current_Salary': salary,
                'Manager': manager,
                'Join_Date': join_date.strftime('%Y-%m-%d')
            })
            
            employee_id += 1
    
    return employees

# Generate data
print("Generating employee data...")
employees = generate_employees()

# Create DataFrame
df = pd.DataFrame(employees)

# Sort by department and salary
df = df.sort_values(['Department', 'Current_Salary'], ascending=[True, False])

# Save to Excel
output_path = Path(__file__).parent / "data" / "salary_data.xlsx"
output_path.parent.mkdir(exist_ok=True)

df.to_excel(output_path, index=False, sheet_name='Employees')

print(f"✅ Generated {len(employees)} employees across {len(departments)} departments")
print(f"✅ Data saved to: {output_path}")
print(f"\nDepartment breakdown:")
for dept in departments.keys():
    count = len(df[df['Department'] == dept])
    avg_salary = df[df['Department'] == dept]['Current_Salary'].mean()
    print(f"  {dept}: {count} employees (avg salary: ₹{avg_salary:,.0f})")
