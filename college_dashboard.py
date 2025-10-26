import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

class CollegeDashboard:
    def __init__(self):
        self.students_file = 'college_students.csv'
        self.courses_file = 'course_structure.csv'
        self.students_data = pd.DataFrame()
        self.course_structure = pd.DataFrame()
        self.load_data()
        
    def load_data(self):
        """Load student and course structure data"""
        if os.path.exists(self.students_file):
            self.students_data = pd.read_csv(self.students_file)
            print(f"✓ Loaded {len(self.students_data)} student records.")
        else:
            print("⚠ No student data found. Please add students first.")
            
        if os.path.exists(self.courses_file):
            self.course_structure = pd.read_csv(self.courses_file)
            print(f"✓ Loaded course structure with {len(self.course_structure)} subjects.\n")
        else:
            print("⚠ No course structure found. Using default structure.\n")
    
    def save_data(self):
        """Save all data"""
        self.students_data.to_csv(self.students_file, index=False)
        print("✓ Data saved successfully!\n")
    
    def get_available_batches(self):
        """Get list of unique batches"""
        if self.students_data.empty:
            return []
        return sorted(self.students_data['Batch'].unique())
    
    def get_subjects_for_semester(self, semester):
        """Get subjects for a specific semester"""
        if self.course_structure.empty:
            return []
        subjects = self.course_structure[
            self.course_structure['Semester'] == semester
        ]['Subject_Code'].tolist()
        return subjects
    
    def add_student(self):
        """Add a new student with marks"""
        print("\n--- Add New Student ---")
        name = input("Enter student name: ").strip()
        roll_no = input("Enter roll number: ").strip()
        
        # Check if roll number already exists
        if not self.students_data.empty and roll_no in self.students_data['Roll_No'].values:
            print(f"❌ Error: Roll number {roll_no} already exists!")
            return
        
        batch = input("Enter batch (e.g., 2024-28): ").strip()
        
        try:
            semester = int(input("Enter current semester (1-8): "))
            if semester < 1 or semester > 8:
                print("❌ Error: Semester must be between 1 and 8!")
                return
        except ValueError:
            print("❌ Error: Invalid semester!")
            return
        
        # Get subjects for this semester
        subjects = self.get_subjects_for_semester(semester)
        
        if not subjects:
            print(f"⚠ No subjects defined for Semester {semester}. Using manual entry.")
            num_subjects = int(input("How many subjects? "))
            subjects = [f"SEM{semester}_SUB{i+1}" for i in range(num_subjects)]
        
        # Collect marks
        marks_dict = {
            'Name': name,
            'Roll_No': roll_no,
            'Batch': batch,
            'Semester': semester
        }
        
        print(f"\nEnter marks for Semester {semester} (out of 100):")
        for subject in subjects:
            while True:
                try:
                    mark = float(input(f"{subject}: "))
                    if 0 <= mark <= 100:
                        marks_dict[subject] = mark
                        break
                    else:
                        print("Marks must be between 0 and 100!")
                except ValueError:
                    print("Please enter a valid number!")
        
        # Add to dataframe
        new_student = pd.DataFrame([marks_dict])
        self.students_data = pd.concat([self.students_data, new_student], ignore_index=True)
        
        print(f"\n✓ Student {name} added successfully!")
        self.save_data()
    
    def view_students(self, batch=None, semester=None):
        """View students with optional filtering"""
        if self.students_data.empty:
            print("\n⚠ No student data available!")
            return
        
        df = self.students_data.copy()
        
        # Apply filters
        if batch:
            df = df[df['Batch'] == batch]
        if semester:
            df = df[df['Semester'] == semester]
        
        if df.empty:
            print("\n⚠ No students found with the specified filters!")
            return
        
        # Calculate total and percentage
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No', 'Batch', 'Semester']]
        
        if subject_cols:
            df['Total'] = df[subject_cols].sum(axis=1)
            max_marks = len(subject_cols) * 100
            df['Percentage'] = (df['Total'] / max_marks * 100).round(2)
            df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        print("\n--- Student Records ---")
        if batch:
            print(f"Batch: {batch}")
        if semester:
            print(f"Semester: {semester}")
        print("-" * 100)
        print(df.to_string(index=False))
        print()
    
    def calculate_grade(self, percentage):
        """Calculate letter grade based on percentage"""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def calculate_statistics(self, batch=None, semester=None):
        """Calculate comprehensive statistics with filtering"""
        if self.students_data.empty:
            print("\n⚠ No student data available!")
            return
        
        df = self.students_data.copy()
        
        # Apply filters
        if batch:
            df = df[df['Batch'] == batch]
        if semester:
            df = df[df['Semester'] == semester]
        
        if df.empty:
            print("\n⚠ No students found with the specified filters!")
            return
        
        print("\n" + "="*80)
        print("STUDENT STATISTICS REPORT")
        print("="*80)
        
        if batch:
            print(f"Batch: {batch}")
        if semester:
            print(f"Semester: {semester}")
        
        # Get subject columns
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No', 'Batch', 'Semester']]
        
        if not subject_cols:
            print("\n⚠ No subject data available!")
            return
        
        # 1. Subject-wise Statistics
        print("\n1. SUBJECT-WISE PERFORMANCE")
        print("-" * 80)
        
        stats_data = []
        for subject in subject_cols:
            stats_data.append({
                'Subject': subject,
                'Average': round(df[subject].mean(), 2),
                'Highest': df[subject].max(),
                'Lowest': df[subject].min(),
                'Std Dev': round(df[subject].std(), 2),
                'Pass %': round((df[subject] >= 40).sum() / len(df) * 100, 2)
            })
        
        stats_df = pd.DataFrame(stats_data)
        print(stats_df.to_string(index=False))
        
        # 2. Overall Statistics
        print("\n2. OVERALL CLASS PERFORMANCE")
        print("-" * 80)
        
        df['Total'] = df[subject_cols].sum(axis=1)
        max_marks = len(subject_cols) * 100
        df['Percentage'] = (df['Total'] / max_marks * 100)
        df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        print(f"Total Students: {len(df)}")
        print(f"Class Average: {df['Percentage'].mean():.2f}%")
        print(f"Highest Percentage: {df['Percentage'].max():.2f}%")
        print(f"Lowest Percentage: {df['Percentage'].min():.2f}%")
        print(f"Standard Deviation: {df['Percentage'].std():.2f}")
        
        # 3. Grade Distribution
        print("\n3. GRADE DISTRIBUTION")
        print("-" * 80)
        grade_dist = df['Grade'].value_counts().sort_index()
        for grade, count in grade_dist.items():
            percentage = (count / len(df) * 100)
            print(f"{grade}: {count} students ({percentage:.1f}%)")
        
        # 4. Top 10 Students
        print("\n4. TOP 10 STUDENTS")
        print("-" * 80)
        top_students = df.nlargest(10, 'Total')[['Name', 'Roll_No', 'Total', 'Percentage', 'Grade']]
        print(top_students.to_string(index=False))
        
        # 5. Pass/Fail Analysis
        print("\n5. PASS/FAIL ANALYSIS")
        print("-" * 80)
        
        # Students failing in any subject
        fail_mask = (df[subject_cols] < 40).any(axis=1)
        failed_students = df[fail_mask]
        passed_students = df[~fail_mask]
        
        print(f"Students Passed (all subjects >= 40): {len(passed_students)} ({len(passed_students)/len(df)*100:.1f}%)")
        print(f"Students Failed (any subject < 40): {len(failed_students)} ({len(failed_students)/len(df)*100:.1f}%)")
        
        if len(failed_students) > 0:
            print(f"\nStudents with backlogs:")
            for idx, row in failed_students.iterrows():
                failed_subjects = [col for col in subject_cols if row[col] < 40]
                print(f"  {row['Name']} ({row['Roll_No']}): {', '.join(failed_subjects)}")
        
        print("\n" + "="*80 + "\n")
    
    def visualize_data(self, batch=None, semester=None):
        """Create visualizations with filtering"""
        if self.students_data.empty:
            print("\n⚠ No student data available!")
            return
        
        df = self.students_data.copy()
        
        # Apply filters
        if batch:
            df = df[df['Batch'] == batch]
        if semester:
            df = df[df['Semester'] == semester]
        
        if df.empty:
            print("\n⚠ No students found with the specified filters!")
            return
        
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No', 'Batch', 'Semester']]
        
        if not subject_cols:
            print("\n⚠ No subject data available for visualization!")
            return
        
        # Calculate percentages
        df['Total'] = df[subject_cols].sum(axis=1)
        max_marks = len(subject_cols) * 100
        df['Percentage'] = (df['Total'] / max_marks * 100)
        df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        # Create visualizations
        fig = plt.figure(figsize=(16, 12))
        
        title = "Student Performance Dashboard"
        if batch:
            title += f" - Batch {batch}"
        if semester:
            title += f" - Semester {semester}"
        fig.suptitle(title, fontsize=18, fontweight='bold')
        
        # 1. Subject-wise Average (Bar Chart)
        ax1 = plt.subplot(3, 3, 1)
        avg_marks = [df[subject].mean() for subject in subject_cols]
        colors = plt.cm.viridis(np.linspace(0, 1, len(subject_cols)))
        bars = ax1.bar(range(len(subject_cols)), avg_marks, color=colors)
        ax1.set_xticks(range(len(subject_cols)))
        ax1.set_xticklabels(subject_cols, rotation=45, ha='right')
        ax1.set_title('Average Marks by Subject', fontweight='bold')
        ax1.set_ylabel('Average Marks')
        ax1.set_ylim(0, 100)
        ax1.axhline(y=40, color='r', linestyle='--', alpha=0.5, label='Pass Line')
        ax1.grid(axis='y', alpha=0.3)
        ax1.legend()
        
        # 2. Percentage Distribution (Histogram)
        ax2 = plt.subplot(3, 3, 2)
        ax2.hist(df['Percentage'], bins=15, color='#4ECDC4', edgecolor='black', alpha=0.7)
        ax2.axvline(df['Percentage'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f"Mean: {df['Percentage'].mean():.1f}%")
        ax2.set_title('Percentage Distribution', fontweight='bold')
        ax2.set_xlabel('Percentage')
        ax2.set_ylabel('Number of Students')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Grade Distribution (Pie Chart)
        ax3 = plt.subplot(3, 3, 3)
        grade_counts = df['Grade'].value_counts().sort_index()
        colors_pie = ['#2ecc71', '#27ae60', '#3498db', '#f39c12', '#e74c3c', '#c0392b', '#95a5a6']
        ax3.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
               colors=colors_pie[:len(grade_counts)], startangle=90)
        ax3.set_title('Grade Distribution', fontweight='bold')
        
        # 4. Subject-wise Box Plot
        ax4 = plt.subplot(3, 3, 4)
        subject_data = [df[subject].values for subject in subject_cols]
        bp = ax4.boxplot(subject_data, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax4.set_xticklabels(subject_cols, rotation=45, ha='right')
        ax4.set_title('Subject-wise Performance Distribution', fontweight='bold')
        ax4.set_ylabel('Marks')
        ax4.axhline(y=40, color='r', linestyle='--', alpha=0.5)
        ax4.grid(axis='y', alpha=0.3)
        
        # 5. Top 10 Students (Horizontal Bar)
        ax5 = plt.subplot(3, 3, 5)
        top_10 = df.nlargest(10, 'Percentage')[['Name', 'Percentage']].sort_values('Percentage')
        ax5.barh(top_10['Name'], top_10['Percentage'], color='#FF6B6B')
        ax5.set_title('Top 10 Students', fontweight='bold')
        ax5.set_xlabel('Percentage')
        ax5.grid(axis='x', alpha=0.3)
        
        # 6. Pass/Fail by Subject (Stacked Bar)
        ax6 = plt.subplot(3, 3, 6)
        pass_counts = [(df[subject] >= 40).sum() for subject in subject_cols]
        fail_counts = [(df[subject] < 40).sum() for subject in subject_cols]
        
        x = np.arange(len(subject_cols))
        ax6.bar(x, pass_counts, label='Pass (≥40)', color='#2ecc71')
        ax6.bar(x, fail_counts, bottom=pass_counts, label='Fail (<40)', color='#e74c3c')
        ax6.set_xticks(x)
        ax6.set_xticklabels(subject_cols, rotation=45, ha='right')
        ax6.set_title('Pass/Fail Distribution by Subject', fontweight='bold')
        ax6.set_ylabel('Number of Students')
        ax6.legend()
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. Performance Heatmap (Top 15 students)
        ax7 = plt.subplot(3, 3, 7)
        top_15 = df.nlargest(15, 'Total')
        heatmap_data = top_15[subject_cols].values
        im = ax7.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        ax7.set_xticks(range(len(subject_cols)))
        ax7.set_xticklabels(subject_cols, rotation=45, ha='right')
        ax7.set_yticks(range(len(top_15)))
        ax7.set_yticklabels(top_15['Name'].values, fontsize=8)
        ax7.set_title('Performance Heatmap (Top 15)', fontweight='bold')
        plt.colorbar(im, ax=ax7, label='Marks')
        
        # 8. Cumulative Performance (Line Chart)
        ax8 = plt.subplot(3, 3, 8)
        sorted_perc = df['Percentage'].sort_values().values
        cumulative = np.arange(1, len(sorted_perc) + 1) / len(sorted_perc) * 100
        ax8.plot(sorted_perc, cumulative, linewidth=2, color='#3498db')
        ax8.fill_between(sorted_perc, cumulative, alpha=0.3, color='#3498db')
        ax8.set_title('Cumulative Performance Distribution', fontweight='bold')
        ax8.set_xlabel('Percentage')
        ax8.set_ylabel('Cumulative % of Students')
        ax8.grid(alpha=0.3)
        ax8.axvline(x=40, color='r', linestyle='--', alpha=0.5, label='Pass Line')
        ax8.legend()
        
        # 9. Statistics Summary (Text)
        ax9 = plt.subplot(3, 3, 9)
        ax9.axis('off')
        
        stats_text = f"""
        SUMMARY STATISTICS
        {'='*30}
        
        Total Students: {len(df)}
        
        Average: {df['Percentage'].mean():.2f}%
        Highest: {df['Percentage'].max():.2f}%
        Lowest: {df['Percentage'].min():.2f}%
        Std Dev: {df['Percentage'].std():.2f}
        
        Pass Rate: {(~(df[subject_cols] < 40).any(axis=1)).sum()/len(df)*100:.1f}%
        Fail Rate: {((df[subject_cols] < 40).any(axis=1)).sum()/len(df)*100:.1f}%
        
        Top Grade: {df.nlargest(1, 'Percentage')['Name'].values[0]}
        Score: {df['Percentage'].max():.2f}%
        """
        
        ax9.text(0.1, 0.5, stats_text, fontsize=11, fontfamily='monospace',
                verticalalignment='center')
        
        plt.tight_layout()
        plt.show()
        print("\n✓ Visualization displayed!")
    
    def filter_menu(self):
        """Interactive filter menu"""
        print("\n--- Filter Options ---")
        
        # Batch selection
        batches = self.get_available_batches()
        batch = None
        if batches:
            print("\nAvailable Batches:")
            for i, b in enumerate(batches, 1):
                print(f"{i}. {b}")
            print(f"{len(batches)+1}. All Batches")
            
            choice = input(f"\nSelect batch (1-{len(batches)+1}): ").strip()
            try:
                choice = int(choice)
                if 1 <= choice <= len(batches):
                    batch = batches[choice-1]
            except:
                pass
        
        # Semester selection
        semester = None
        print("\nSemester Filter:")
        for i in range(1, 9):
            print(f"{i}. Semester {i}")
        print("9. All Semesters")
        
        choice = input("\nSelect semester (1-9): ").strip()
        try:
            choice = int(choice)
            if 1 <= choice <= 8:
                semester = choice
        except:
            pass
        
        return batch, semester
    
    def search_student(self):
        """Search for a specific student"""
        if self.students_data.empty:
            print("\n⚠ No student data available!")
            return
        
        search_term = input("\nEnter student name or roll number: ").strip()
        
        result = self.students_data[
            (self.students_data['Name'].str.contains(search_term, case=False, na=False)) |
            (self.students_data['Roll_No'].str.contains(search_term, case=False, na=False))
        ]
        
        if result.empty:
            print(f"\n⚠ No student found matching '{search_term}'")
        else:
            subject_cols = [col for col in result.columns if col not in ['Name', 'Roll_No', 'Batch', 'Semester']]
            display_df = result.copy()
            
            if subject_cols:
                display_df['Total'] = display_df[subject_cols].sum(axis=1)
                max_marks = len(subject_cols) * 100
                display_df['Percentage'] = (display_df['Total'] / max_marks * 100).round(2)
                display_df['Grade'] = display_df['Percentage'].apply(self.calculate_grade)
            
            print("\n--- Search Results ---")
            print(display_df.to_string(index=False))
        print()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("          COLLEGE STUDENT DASHBOARD SYSTEM")
        print("="*60)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. View Students (with filters)")
        print("4. Calculate Statistics")
        print("5. Calculate Statistics (with filters)")
        print("6. Visualize Data")
        print("7. Visualize Data (with filters)")
        print("8. Search Student")
        print("9. Show Available Batches")
        print("10. Exit")
        print("="*60)
    
    def run(self):
        """Main program loop"""
        print("\n🎓 Welcome to College Student Dashboard System!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-10): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_students()
            elif choice == '3':
                batch, semester = self.filter_menu()
                self.view_students(batch, semester)
            elif choice == '4':
                self.calculate_statistics()
            elif choice == '5':
                batch, semester = self.filter_menu()
                self.calculate_statistics(batch, semester)
            elif choice == '6':
                self.visualize_data()
            elif choice == '7':
                batch, semester = self.filter_menu()
                self.visualize_data(batch, semester)
            elif choice == '8':
                self.search_student()
            elif choice == '9':
                batches = self.get_available_batches()
                if batches:
                    print("\nAvailable Batches:")
                    for batch in batches:
                        count = len(self.students_data[self.students_data['Batch'] == batch])
                        print(f"  • {batch}: {count} students")
                else:
                    print("\n⚠ No batches available yet!")
            elif choice == '10':
                print("\nThank you for using College Student Dashboard System!")
                print("Goodbye! 👋\n")
                break
            else:
                print("\n❌ Invalid choice! Please enter a number between 1 and 10.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    dashboard = CollegeDashboard()
    dashboard.run()