import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("="*70)
print("           COLLEGE DATASET GENERATOR")
print("="*70)
print()

# ================== SUBJECT-SEMESTER MAPPING ==================

subjects_data = [
    # Semester 1
    {'Subject': 'MATH101', 'Semester': 1},
    {'Subject': 'PHY101', 'Semester': 1},
    {'Subject': 'CHEM101', 'Semester': 1},
    {'Subject': 'ENG101', 'Semester': 1},
    {'Subject': 'CS101', 'Semester': 1},
    
    # Semester 2
    {'Subject': 'MATH102', 'Semester': 2},
    {'Subject': 'PHY102', 'Semester': 2},
    {'Subject': 'EE101', 'Semester': 2},
    {'Subject': 'ME101', 'Semester': 2},
    {'Subject': 'CS102', 'Semester': 2},
    
    # Semester 3
    {'Subject': 'MATH201', 'Semester': 3},
    {'Subject': 'CS201', 'Semester': 3},
    {'Subject': 'CS202', 'Semester': 3},
    {'Subject': 'CS203', 'Semester': 3},
    {'Subject': 'CS204', 'Semester': 3},
    
    # Semester 4
    {'Subject': 'MATH202', 'Semester': 4},
    {'Subject': 'CS205', 'Semester': 4},
    {'Subject': 'CS206', 'Semester': 4},
    {'Subject': 'CS207', 'Semester': 4},
    {'Subject': 'CS208', 'Semester': 4},
    {'Subject': 'MGT101', 'Semester': 4},
    
    # Semester 5
    {'Subject': 'CS301', 'Semester': 5},
    {'Subject': 'CS302', 'Semester': 5},
    {'Subject': 'CS303', 'Semester': 5},
    {'Subject': 'CS304', 'Semester': 5},
    {'Subject': 'CS305', 'Semester': 5},
    
    # Semester 6
    {'Subject': 'CS306', 'Semester': 6},
    {'Subject': 'CS307', 'Semester': 6},
    {'Subject': 'CS308', 'Semester': 6},
    {'Subject': 'CS309', 'Semester': 6},
    {'Subject': 'CS310', 'Semester': 6},
    
    # Semester 7
    {'Subject': 'CS401', 'Semester': 7},
    {'Subject': 'CS402', 'Semester': 7},
    {'Subject': 'CS403', 'Semester': 7},
    {'Subject': 'CS404', 'Semester': 7},
    {'Subject': 'CS405', 'Semester': 7},
    
    # Semester 8
    {'Subject': 'CS406', 'Semester': 8},
    {'Subject': 'CS407', 'Semester': 8},
    {'Subject': 'CS408', 'Semester': 8},
    {'Subject': 'MGT201', 'Semester': 8},
]

# Save subject-semester mapping
subjects_df = pd.DataFrame(subjects_data)
subjects_df.to_csv('subjects_semester.csv', index=False)
print("✓ Created: subjects_semester.csv")
print(f"  Total subjects: {len(subjects_df)}")
print()

# ================== STUDENT DATA GENERATION ==================

# Student names pool
first_names = ['Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Arnav', 'Ayaan', 'Krishna', 'Ishaan', 'Reyansh',
               'Ananya', 'Diya', 'Aadhya', 'Saanvi', 'Pari', 'Avni', 'Sara', 'Myra', 'Anika', 'Riya',
               'Rohan', 'Karan', 'Rahul', 'Amit', 'Priya', 'Neha', 'Pooja', 'Sneha', 'Vikram', 'Rajesh',
               'Shreya', 'Ishita', 'Kavya', 'Nidhi', 'Tanvi', 'Aryan', 'Dev', 'Harsh', 'Kunal', 'Nikhil',
               'Aditi', 'Divya', 'Gargi', 'Jiya', 'Kiara', 'Lakshmi', 'Meera', 'Naina', 'Ojas', 'Pranav',
               'Manish', 'Suresh', 'Deepak', 'Ramesh', 'Sandeep', 'Anjali', 'Shalini', 'Preeti', 'Sunita', 'Rekha']

last_names = ['Sharma', 'Verma', 'Kumar', 'Singh', 'Patel', 'Reddy', 'Nair', 'Iyer', 'Joshi', 'Desai',
              'Gupta', 'Agarwal', 'Mehta', 'Shah', 'Kulkarni', 'Rao', 'Pillai', 'Menon', 'Das', 'Roy',
              'Banerjee', 'Mukherjee', 'Chatterjee', 'Jain', 'Sinha', 'Mishra', 'Tiwari', 'Pandey', 'Yadav', 'Chauhan']

def generate_batch_data(batch_name, num_students, max_semester):
    """
    Generate student data for a specific batch
    
    Args:
        batch_name: e.g., '2021-25'
        num_students: number of students in the batch
        max_semester: highest semester completed (1-8)
    """
    # Get batch year for roll number
    batch_year = batch_name.split('-')[0]
    
    # Generate unique student names
    used_names = set()
    students = []
    
    for i in range(num_students):
        # Generate unique name
        while True:
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            if name not in used_names:
                used_names.add(name)
                break
        
        roll_no = f"{batch_year}{str(i+1).zfill(3)}"
        
        # Base performance for this student (consistent across semesters)
        base_performance = np.random.normal(70, 12)
        
        student_data = {
            'Name': name,
            'Roll_No': roll_no
        }
        
        # Add marks for all subjects up to max_semester
        for sem in range(1, max_semester + 1):
            # Get subjects for this semester
            sem_subjects = subjects_df[subjects_df['Semester'] == sem]['Subject'].tolist()
            
            for subject in sem_subjects:
                # Generate marks with some variation
                mark = base_performance + np.random.normal(0, 10)
                # Add semester-specific difficulty (later semesters slightly harder)
                mark = mark - (sem * 0.5)
                # Clamp between 0 and 100
                mark = max(0, min(100, mark))
                student_data[subject] = round(mark, 2)
        
        students.append(student_data)
    
    return pd.DataFrame(students)

# ================== GENERATE BATCH FILES ==================

batches_info = [
    {'name': '2021-25', 'students': 60, 'semesters': 8, 'year': 'Final Year'},
    {'name': '2022-26', 'students': 65, 'semesters': 6, 'year': 'Third Year'},
    {'name': '2023-27', 'students': 70, 'semesters': 4, 'year': 'Second Year'},
    {'name': '2024-28', 'students': 75, 'semesters': 2, 'year': 'First Year'},
]

print("Generating batch data files...")
print("-" * 70)

for batch in batches_info:
    batch_name = batch['name']
    num_students = batch['students']
    max_semester = batch['semesters']
    year = batch['year']
    
    print(f"\nGenerating: Batch {batch_name} ({year})")
    print(f"  Students: {num_students}")
    print(f"  Semesters completed: {max_semester}")
    
    # Generate data
    batch_df = generate_batch_data(batch_name, num_students, max_semester)
    
    # Save to CSV
    filename = f"batch_{batch_name.replace('-', '_')}.csv"
    batch_df.to_csv(filename, index=False)
    
    print(f"  ✓ Created: {filename}")
    print(f"    Columns: {len(batch_df.columns)} (Name, Roll_No + {len(batch_df.columns)-2} subjects)")

print()
print("="*70)
print("DATASET GENERATION COMPLETE!")
print("="*70)

# Display summary
print("\nFiles Created:")
print("-" * 70)
print("1. subjects_semester.csv")
print("   - Maps subjects to their respective semesters")
print(f"   - Total subjects: {len(subjects_df)}")
print()

for i, batch in enumerate(batches_info, 2):
    filename = f"batch_{batch['name'].replace('-', '_')}.csv"
    print(f"{i}. {filename}")
    print(f"   - Batch: {batch['name']} ({batch['year']})")
    print(f"   - Students: {batch['students']}")
    print(f"   - Semesters: {batch['semesters']}")
    
    # Count subjects
    total_subjects = sum(len(subjects_df[subjects_df['Semester'] == sem]) 
                        for sem in range(1, batch['semesters'] + 1))
    print(f"   - Subject columns: {total_subjects}")
    print()

print("="*70)
print("\nSemester-wise Subject Breakdown:")
print("-" * 70)
for sem in range(1, 9):
    subjects = subjects_df[subjects_df['Semester'] == sem]['Subject'].tolist()
    print(f"Semester {sem}: {len(subjects)} subjects")
    print(f"  {', '.join(subjects)}")
    print()

print("="*70)
print("✓ All files generated successfully!")
print("="*70)