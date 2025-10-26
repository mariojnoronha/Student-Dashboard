import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ================== COURSE STRUCTURE ==================
# Define course structure for all 8 semesters

course_structure = [
    # Semester 1
    {'Semester': 1, 'Subject_Code': 'MATH101', 'Subject_Name': 'Engineering Mathematics I', 'Credits': 4},
    {'Semester': 1, 'Subject_Code': 'PHY101', 'Subject_Name': 'Engineering Physics', 'Credits': 4},
    {'Semester': 1, 'Subject_Code': 'CHEM101', 'Subject_Name': 'Engineering Chemistry', 'Credits': 3},
    {'Semester': 1, 'Subject_Code': 'ENG101', 'Subject_Name': 'English Communication', 'Credits': 3},
    {'Semester': 1, 'Subject_Code': 'CS101', 'Subject_Name': 'Introduction to Programming', 'Credits': 4},
    
    # Semester 2
    {'Semester': 2, 'Subject_Code': 'MATH102', 'Subject_Name': 'Engineering Mathematics II', 'Credits': 4},
    {'Semester': 2, 'Subject_Code': 'PHY102', 'Subject_Name': 'Applied Physics', 'Credits': 3},
    {'Semester': 2, 'Subject_Code': 'EE101', 'Subject_Name': 'Basic Electrical Engineering', 'Credits': 4},
    {'Semester': 2, 'Subject_Code': 'ME101', 'Subject_Name': 'Engineering Mechanics', 'Credits': 4},
    {'Semester': 2, 'Subject_Code': 'CS102', 'Subject_Name': 'Data Structures', 'Credits': 4},
    
    # Semester 3
    {'Semester': 3, 'Subject_Code': 'MATH201', 'Subject_Name': 'Discrete Mathematics', 'Credits': 4},
    {'Semester': 3, 'Subject_Code': 'CS201', 'Subject_Name': 'Object Oriented Programming', 'Credits': 4},
    {'Semester': 3, 'Subject_Code': 'CS202', 'Subject_Name': 'Computer Organization', 'Credits': 4},
    {'Semester': 3, 'Subject_Code': 'CS203', 'Subject_Name': 'Database Management Systems', 'Credits': 4},
    {'Semester': 3, 'Subject_Code': 'CS204', 'Subject_Name': 'Digital Electronics', 'Credits': 3},
    
    # Semester 4
    {'Semester': 4, 'Subject_Code': 'MATH202', 'Subject_Name': 'Probability and Statistics', 'Credits': 4},
    {'Semester': 4, 'Subject_Code': 'CS205', 'Subject_Name': 'Operating Systems', 'Credits': 4},
    {'Semester': 4, 'Subject_Code': 'CS206', 'Subject_Name': 'Algorithm Design', 'Credits': 4},
    {'Semester': 4, 'Subject_Code': 'CS207', 'Subject_Name': 'Computer Networks', 'Credits': 4},
    {'Semester': 4, 'Subject_Code': 'CS208', 'Subject_Name': 'Theory of Computation', 'Credits': 3},
    {'Semester': 4, 'Subject_Code': 'MGT101', 'Subject_Name': 'Engineering Economics', 'Credits': 2},
    
    # Semester 5
    {'Semester': 5, 'Subject_Code': 'CS301', 'Subject_Name': 'Software Engineering', 'Credits': 4},
    {'Semester': 5, 'Subject_Code': 'CS302', 'Subject_Name': 'Compiler Design', 'Credits': 4},
    {'Semester': 5, 'Subject_Code': 'CS303', 'Subject_Name': 'Artificial Intelligence', 'Credits': 4},
    {'Semester': 5, 'Subject_Code': 'CS304', 'Subject_Name': 'Web Technologies', 'Credits': 3},
    {'Semester': 5, 'Subject_Code': 'CS305', 'Subject_Name': 'Elective I', 'Credits': 3},
    
    # Semester 6
    {'Semester': 6, 'Subject_Code': 'CS306', 'Subject_Name': 'Machine Learning', 'Credits': 4},
    {'Semester': 6, 'Subject_Code': 'CS307', 'Subject_Name': 'Computer Graphics', 'Credits': 4},
    {'Semester': 6, 'Subject_Code': 'CS308', 'Subject_Name': 'Information Security', 'Credits': 4},
    {'Semester': 6, 'Subject_Code': 'CS309', 'Subject_Name': 'Cloud Computing', 'Credits': 3},
    {'Semester': 6, 'Subject_Code': 'CS310', 'Subject_Name': 'Elective II', 'Credits': 3},
    
    # Semester 7
    {'Semester': 7, 'Subject_Code': 'CS401', 'Subject_Name': 'Big Data Analytics', 'Credits': 4},
    {'Semester': 7, 'Subject_Code': 'CS402', 'Subject_Name': 'Deep Learning', 'Credits': 4},
    {'Semester': 7, 'Subject_Code': 'CS403', 'Subject_Name': 'Mobile Application Development', 'Credits': 3},
    {'Semester': 7, 'Subject_Code': 'CS404', 'Subject_Name': 'Blockchain Technology', 'Credits': 3},
    {'Semester': 7, 'Subject_Code': 'CS405', 'Subject_Name': 'Elective III', 'Credits': 3},
    
    # Semester 8
    {'Semester': 8, 'Subject_Code': 'CS406', 'Subject_Name': 'Project Work', 'Credits': 8},
    {'Semester': 8, 'Subject_Code': 'CS407', 'Subject_Name': 'IoT and Applications', 'Credits': 3},
    {'Semester': 8, 'Subject_Code': 'CS408', 'Subject_Name': 'Cyber Security', 'Credits': 3},
    {'Semester': 8, 'Subject_Code': 'MGT201', 'Subject_Name': 'Entrepreneurship', 'Credits': 2},
]

# Save course structure
course_df = pd.DataFrame(course_structure)
course_df.to_csv('course_structure.csv', index=False)
print("✓ Course structure created: course_structure.csv")
print(f"  Total subjects: {len(course_df)}")
print()

# ================== STUDENT DATA GENERATION ==================

# Student names pool
first_names = ['Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 'Arnav', 'Ayaan', 'Krishna', 'Ishaan', 'Reyansh',
               'Ananya', 'Diya', 'Aadhya', 'Saanvi', 'Pari', 'Avni', 'Sara', 'Myra', 'Anika', 'Riya',
               'Rohan', 'Karan', 'Rahul', 'Amit', 'Priya', 'Neha', 'Pooja', 'Sneha', 'Vikram', 'Rajesh',
               'Shreya', 'Ishita', 'Kavya', 'Nidhi', 'Tanvi', 'Aryan', 'Dev', 'Harsh', 'Kunal', 'Nikhil',
               'Aditi', 'Divya', 'Gargi', 'Jiya', 'Kiara', 'Lakshmi', 'Meera', 'Naina', 'Ojas', 'Pranav']

last_names = ['Sharma', 'Verma', 'Kumar', 'Singh', 'Patel', 'Reddy', 'Nair', 'Iyer', 'Joshi', 'Desai',
              'Gupta', 'Agarwal', 'Mehta', 'Shah', 'Kulkarni', 'Rao', 'Pillai', 'Menon', 'Das', 'Roy',
              'Banerjee', 'Mukherjee', 'Chatterjee', 'Jain', 'Sinha', 'Mishra', 'Tiwari', 'Pandey', 'Yadav', 'Chauhan']

def generate_student_data(batch, num_students, semesters_to_generate):
    """Generate student data for a specific batch"""
    students = []
    
    for i in range(num_students):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate roll number based on batch
        batch_year = batch.split('-')[0]
        roll_no = f"{batch_year}{str(i+1).zfill(3)}"
        
        # For each semester the student has completed
        for sem in semesters_to_generate:
            student_record = {
                'Name': name,
                'Roll_No': roll_no,
                'Batch': batch,
                'Semester': sem
            }
            
            # Get subjects for this semester
            sem_subjects = course_df[course_df['Semester'] == sem]['Subject_Code'].tolist()
            
            # Generate marks (with some variation for realism)
            base_performance = np.random.normal(70, 15)  # Student's base ability
            
            for subject in sem_subjects:
                # Add some subject-specific variation
                mark = base_performance + np.random.normal(0, 10)
                # Clamp between 0 and 100
                mark = max(0, min(100, mark))
                student_record[subject] = round(mark, 2)
            
            students.append(student_record)
    
    return students

# Generate data for multiple batches
all_students = []

# Batch 2021-25 (Final year - all 8 semesters completed)
print("Generating data for Batch 2021-25...")
all_students.extend(generate_student_data('2021-25', 60, range(1, 9)))

# Batch 2022-26 (Third year - 6 semesters completed)
print("Generating data for Batch 2022-26...")
all_students.extend(generate_student_data('2022-26', 65, range(1, 7)))

# Batch 2023-27 (Second year - 4 semesters completed)
print("Generating data for Batch 2023-27...")
all_students.extend(generate_student_data('2023-27', 70, range(1, 5)))

# Batch 2024-28 (First year - 2 semesters completed)
print("Generating data for Batch 2024-28...")
all_students.extend(generate_student_data('2024-28', 75, range(1, 3)))

# Create DataFrame and save
students_df = pd.DataFrame(all_students)
students_df.to_csv('college_students.csv', index=False)

print(f"\n✓ Student data created: college_students.csv")
print(f"  Total records: {len(students_df)}")
print(f"  Unique students: {students_df['Roll_No'].nunique()}")
print(f"  Batches: {', '.join(students_df['Batch'].unique())}")
print()

# Display summary
print("="*60)
print("DATASET SUMMARY")
print("="*60)
print("\nBatch-wise Distribution:")
for batch in sorted(students_df['Batch'].unique()):
    batch_data = students_df[students_df['Batch'] == batch]
    unique_students = batch_data['Roll_No'].nunique()
    semesters = sorted(batch_data['Semester'].unique())
    print(f"  {batch}: {unique_students} students, Semesters: {semesters}")

print("\nSemester-wise Subject Count:")
for sem in range(1, 9):
    subjects = course_df[course_df['Semester'] == sem]
    print(f"  Semester {sem}: {len(subjects)} subjects")

print("\n" + "="*60)
print("Files created successfully!")
print("  1. course_structure.csv - Course and subject information")
print("  2. college_students.csv - Student marks data")
print("\nYou can now run the dashboard system!")
print("="*60)