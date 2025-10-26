import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob

class CollegeDashboard:
    def __init__(self):
        self.subjects_semester_file = 'subjects_semester.csv'
        self.batch_files = {}
        self.subjects_semester = pd.DataFrame()
        self.load_data()
        
    def load_data(self):
        """Load subject-semester mapping and all batch files"""
        # Load subject-semester mapping
        if os.path.exists(self.subjects_semester_file):
            self.subjects_semester = pd.read_csv(self.subjects_semester_file)
            print(f"✓ Loaded subject-semester mapping ({len(self.subjects_semester)} subjects)")
        else:
            print("⚠ subjects_semester.csv not found!")
            return
        
        # Load all batch CSV files
        batch_pattern = "batch_*.csv"
        batch_files_list = glob(batch_pattern)
        
        if not batch_files_list:
            print("⚠ No batch files found!")
            return
        
        for file in batch_files_list:
            # Extract batch name from filename (e.g., batch_2021_25.csv -> 2021-25)
            batch_name = file.replace('batch_', '').replace('.csv', '').replace('_', '-')
            self.batch_files[batch_name] = pd.read_csv(file)
            print(f"✓ Loaded {batch_name}: {len(self.batch_files[batch_name])} students")
        
        print()
    
    def get_available_batches(self):
        """Get list of available batches"""
        return sorted(self.batch_files.keys())
    
    def get_subjects_for_semester(self, semester):
        """Get subjects for a specific semester"""
        if self.subjects_semester.empty:
            return []
        return self.subjects_semester[
            self.subjects_semester['Semester'] == semester
        ]['Subject'].tolist()
    
    def get_batch_data(self, batch):
        """Get data for a specific batch"""
        if batch in self.batch_files:
            return self.batch_files[batch].copy()
        return pd.DataFrame()
    
    def get_available_semesters_for_batch(self, batch):
        """Get list of semesters that a batch has completed"""
        if batch not in self.batch_files:
            return []
        
        df = self.batch_files[batch]
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No']]
        
        # Find which semesters these subjects belong to
        available_semesters = set()
        for subject in subject_cols:
            sem_data = self.subjects_semester[self.subjects_semester['Subject'] == subject]
            if not sem_data.empty:
                available_semesters.add(int(sem_data['Semester'].values[0]))
        
        return sorted(list(available_semesters))
    
    def validate_semester_for_batch(self, batch, semester):
        """Check if batch has data for the specified semester"""
        if not semester:  # If no semester filter, it's valid
            return True
        
        available_sems = self.get_available_semesters_for_batch(batch)
        
        if semester not in available_sems:
            print(f"\n❌ Batch {batch} does not have information for Semester {semester}!")
            print(f"   Available semesters for this batch: {available_sems}")
            print(f"   This batch has only completed up to Semester {max(available_sems) if available_sems else 0}")
            return False
        
        return True
    
    def add_student_to_batch(self):
        """Add a new student to an existing batch"""
        print("\n--- Add New Student ---")
        
        batches = self.get_available_batches()
        if not batches:
            print("⚠ No batches available!")
            return
        
        print("\nAvailable Batches:")
        for i, batch in enumerate(batches, 1):
            print(f"{i}. {batch}")
        
        try:
            choice = int(input(f"\nSelect batch (1-{len(batches)}): "))
            if choice < 1 or choice > len(batches):
                print("❌ Invalid choice!")
                return
            batch = batches[choice - 1]
        except ValueError:
            print("❌ Invalid input!")
            return
        
        name = input("Enter student name: ").strip()
        roll_no = input("Enter roll number: ").strip()
        
        # Check if roll number exists
        batch_df = self.batch_files[batch]
        if roll_no in batch_df['Roll_No'].values:
            print(f"❌ Roll number {roll_no} already exists!")
            return
        
        # Determine max semester from existing data
        subject_cols = [col for col in batch_df.columns if col not in ['Name', 'Roll_No']]
        max_semester = self.subjects_semester[
            self.subjects_semester['Subject'].isin(subject_cols)
        ]['Semester'].max()
        
        print(f"\nThis batch has completed up to Semester {max_semester}")
        
        # Collect marks
        new_student = {
            'Name': name,
            'Roll_No': roll_no
        }
        
        print(f"\nEnter marks for all subjects (out of 100):")
        for subject in subject_cols:
            sem = self.subjects_semester[
                self.subjects_semester['Subject'] == subject
            ]['Semester'].values[0]
            
            while True:
                try:
                    mark = float(input(f"{subject} (Sem {sem}): "))
                    if 0 <= mark <= 100:
                        new_student[subject] = mark
                        break
                    else:
                        print("Marks must be between 0 and 100!")
                except ValueError:
                    print("Please enter a valid number!")
        
        # Add to dataframe
        new_row = pd.DataFrame([new_student])
        self.batch_files[batch] = pd.concat([self.batch_files[batch], new_row], ignore_index=True)
        
        # Save to file
        filename = f"batch_{batch.replace('-', '_')}.csv"
        self.batch_files[batch].to_csv(filename, index=False)
        
        print(f"\n✓ Student {name} added to batch {batch}!")
    
    def view_batch_students(self, batch=None, semester_filter=None):
        """View students from a specific batch"""
        if not batch:
            print("\n⚠ Please select a batch!")
            return
        
        # Validate semester for batch
        if not self.validate_semester_for_batch(batch, semester_filter):
            return
        
        df = self.get_batch_data(batch)
        if df.empty:
            print(f"\n⚠ No data found for batch {batch}!")
            return
        
        # Get subject columns
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No']]
        
        # Filter by semester if specified
        if semester_filter:
            semester_subjects = self.get_subjects_for_semester(semester_filter)
            display_cols = ['Name', 'Roll_No'] + [s for s in semester_subjects if s in subject_cols]
            df_display = df[display_cols].copy()
            subject_cols = [s for s in semester_subjects if s in subject_cols]
        else:
            df_display = df.copy()
        
        # Calculate statistics
        if subject_cols:
            df_display['Total'] = df_display[subject_cols].sum(axis=1)
            max_marks = len(subject_cols) * 100
            df_display['Percentage'] = (df_display['Total'] / max_marks * 100).round(2)
            df_display['Grade'] = df_display['Percentage'].apply(self.calculate_grade)
        
        print("\n" + "="*100)
        print(f"STUDENT RECORDS - BATCH {batch}")
        if semester_filter:
            print(f"Semester: {semester_filter}")
        print("="*100)
        print(df_display.to_string(index=False))
        print("="*100 + "\n")
    
    def calculate_grade(self, percentage):
        """Calculate letter grade"""
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
    
    def calculate_statistics(self, batch=None, semester_filter=None):
        """Calculate comprehensive statistics"""
        if not batch:
            print("\n⚠ Please select a batch!")
            return
        
        # Validate semester for batch
        if not self.validate_semester_for_batch(batch, semester_filter):
            return
        
        df = self.get_batch_data(batch)
        if df.empty:
            print(f"\n⚠ No data found for batch {batch}!")
            return
        
        # Get subject columns
        all_subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No']]
        
        # Filter by semester if specified
        if semester_filter:
            semester_subjects = self.get_subjects_for_semester(semester_filter)
            subject_cols = [s for s in semester_subjects if s in all_subject_cols]
        else:
            subject_cols = all_subject_cols
        
        if not subject_cols:
            print("\n⚠ No subjects found!")
            return
        
        print("\n" + "="*90)
        print(f"STATISTICS REPORT - BATCH {batch}")
        if semester_filter:
            print(f"Semester: {semester_filter}")
        print("="*90)
        
        # 1. Subject-wise Statistics
        print("\n1. SUBJECT-WISE PERFORMANCE")
        print("-" * 90)
        
        stats_data = []
        for subject in subject_cols:
            sem = self.subjects_semester[
                self.subjects_semester['Subject'] == subject
            ]['Semester'].values[0] if not self.subjects_semester.empty else 'N/A'
            
            stats_data.append({
                'Subject': subject,
                'Sem': sem,
                'Average': round(df[subject].mean(), 2),
                'Highest': df[subject].max(),
                'Lowest': df[subject].min(),
                'Std Dev': round(df[subject].std(), 2),
                'Pass %': round((df[subject] >= 40).sum() / len(df) * 100, 2)
            })
        
        stats_df = pd.DataFrame(stats_data)
        print(stats_df.to_string(index=False))
        
        # 2. Overall Statistics
        print("\n2. OVERALL PERFORMANCE")
        print("-" * 90)
        
        df['Total'] = df[subject_cols].sum(axis=1)
        max_marks = len(subject_cols) * 100
        df['Percentage'] = (df['Total'] / max_marks * 100)
        df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        print(f"Total Students: {len(df)}")
        print(f"Class Average: {df['Percentage'].mean():.2f}%")
        print(f"Highest: {df['Percentage'].max():.2f}%")
        print(f"Lowest: {df['Percentage'].min():.2f}%")
        print(f"Standard Deviation: {df['Percentage'].std():.2f}")
        
        # 3. Grade Distribution
        print("\n3. GRADE DISTRIBUTION")
        print("-" * 90)
        grade_dist = df['Grade'].value_counts().sort_index()
        for grade, count in grade_dist.items():
            bar = '█' * int(count / len(df) * 50)
            print(f"{grade}: {count:3d} students ({count/len(df)*100:5.1f}%) {bar}")
        
        # 4. Top 10 Students
        print("\n4. TOP 10 PERFORMERS")
        print("-" * 90)
        top_10 = df.nlargest(10, 'Percentage')[['Name', 'Roll_No', 'Total', 'Percentage', 'Grade']]
        print(top_10.to_string(index=False))
        
        # 5. Backlog Analysis
        print("\n5. BACKLOG ANALYSIS")
        print("-" * 90)
        
        fail_mask = (df[subject_cols] < 40).any(axis=1)
        failed_students = df[fail_mask]
        
        print(f"Students with No Backlogs: {len(df) - len(failed_students)} ({(len(df)-len(failed_students))/len(df)*100:.1f}%)")
        print(f"Students with Backlogs: {len(failed_students)} ({len(failed_students)/len(df)*100:.1f}%)")
        
        if len(failed_students) > 0:
            print(f"\nStudents with Backlogs (Marks < 40):")
            for idx, row in failed_students.iterrows():
                failed_subs = [col for col in subject_cols if row[col] < 40]
                backlog_details = ', '.join([f"{s} ({row[s]:.1f})" for s in failed_subs])
                print(f"  • {row['Name']} ({row['Roll_No']}): {backlog_details}")
        
        print("\n" + "="*90 + "\n")
    
    def visualize_data(self, batch=None, semester_filter=None):
        """Create visualizations"""
        if not batch:
            print("\n⚠ Please select a batch!")
            return
        
        # Validate semester for batch
        if not self.validate_semester_for_batch(batch, semester_filter):
            return
        
        df = self.get_batch_data(batch)
        if df.empty:
            print(f"\n⚠ No data found for batch {batch}!")
            return
        
        # Get subject columns
        all_subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No']]
        
        # Filter by semester if specified
        if semester_filter:
            semester_subjects = self.get_subjects_for_semester(semester_filter)
            subject_cols = [s for s in semester_subjects if s in all_subject_cols]
        else:
            subject_cols = all_subject_cols
        
        if not subject_cols:
            print("\n⚠ No subjects to visualize!")
            return
        
        # Calculate metrics
        df['Total'] = df[subject_cols].sum(axis=1)
        max_marks = len(subject_cols) * 100
        df['Percentage'] = (df['Total'] / max_marks * 100)
        df['Grade'] = df['Percentage'].apply(self.calculate_grade)
        
        # Create figure
        fig = plt.figure(figsize=(18, 12))
        title = f"Performance Dashboard - Batch {batch}"
        if semester_filter:
            title += f" (Semester {semester_filter})"
        fig.suptitle(title, fontsize=20, fontweight='bold')
        
        # 1. Average Marks by Subject
        ax1 = plt.subplot(3, 3, 1)
        avg_marks = [df[s].mean() for s in subject_cols]
        colors = plt.cm.viridis(np.linspace(0, 1, len(subject_cols)))
        ax1.bar(range(len(subject_cols)), avg_marks, color=colors)
        ax1.set_xticks(range(len(subject_cols)))
        ax1.set_xticklabels(subject_cols, rotation=45, ha='right', fontsize=8)
        ax1.set_title('Average Marks by Subject', fontweight='bold')
        ax1.set_ylabel('Average Marks')
        ax1.set_ylim(0, 100)
        ax1.axhline(40, color='r', linestyle='--', alpha=0.5)
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Percentage Distribution
        ax2 = plt.subplot(3, 3, 2)
        ax2.hist(df['Percentage'], bins=20, color='#4ECDC4', edgecolor='black', alpha=0.7)
        ax2.axvline(df['Percentage'].mean(), color='red', linestyle='--', 
                    linewidth=2, label=f"Mean: {df['Percentage'].mean():.1f}%")
        ax2.set_title('Percentage Distribution', fontweight='bold')
        ax2.set_xlabel('Percentage')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Grade Distribution
        ax3 = plt.subplot(3, 3, 3)
        grade_counts = df['Grade'].value_counts().sort_index()
        colors_pie = ['#2ecc71', '#27ae60', '#3498db', '#f39c12', '#e74c3c', '#c0392b', '#95a5a6']
        ax3.pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
                colors=colors_pie[:len(grade_counts)], startangle=90)
        ax3.set_title('Grade Distribution', fontweight='bold')
        
        # 4. Box Plot
        ax4 = plt.subplot(3, 3, 4)
        subject_data = [df[s].values for s in subject_cols]
        bp = ax4.boxplot(subject_data, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax4.set_xticklabels(subject_cols, rotation=45, ha='right', fontsize=8)
        ax4.set_title('Subject Performance Distribution', fontweight='bold')
        ax4.set_ylabel('Marks')
        ax4.axhline(40, color='r', linestyle='--', alpha=0.5)
        ax4.grid(axis='y', alpha=0.3)
        
        # 5. Top 10 Students
        ax5 = plt.subplot(3, 3, 5)
        top_10 = df.nlargest(10, 'Percentage')[['Name', 'Percentage']].sort_values('Percentage')
        ax5.barh(range(len(top_10)), top_10['Percentage'], color='#FF6B6B')
        ax5.set_yticks(range(len(top_10)))
        ax5.set_yticklabels(top_10['Name'], fontsize=8)
        ax5.set_title('Top 10 Students', fontweight='bold')
        ax5.set_xlabel('Percentage')
        ax5.grid(axis='x', alpha=0.3)
        
        # 6. Pass/Fail by Subject
        ax6 = plt.subplot(3, 3, 6)
        pass_counts = [(df[s] >= 40).sum() for s in subject_cols]
        fail_counts = [(df[s] < 40).sum() for s in subject_cols]
        x = np.arange(len(subject_cols))
        ax6.bar(x, pass_counts, label='Pass', color='#2ecc71')
        ax6.bar(x, fail_counts, bottom=pass_counts, label='Fail', color='#e74c3c')
        ax6.set_xticks(x)
        ax6.set_xticklabels(subject_cols, rotation=45, ha='right', fontsize=8)
        ax6.set_title('Pass/Fail Distribution', fontweight='bold')
        ax6.set_ylabel('Students')
        ax6.legend()
        ax6.grid(axis='y', alpha=0.3)
        
        # 7. Heatmap (Top 20)
        ax7 = plt.subplot(3, 3, 7)
        top_20 = df.nlargest(20, 'Total')
        heatmap_data = top_20[subject_cols].values
        im = ax7.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        ax7.set_xticks(range(len(subject_cols)))
        ax7.set_xticklabels(subject_cols, rotation=45, ha='right', fontsize=8)
        ax7.set_yticks(range(len(top_20)))
        ax7.set_yticklabels(top_20['Name'].values, fontsize=7)
        ax7.set_title('Heatmap (Top 20)', fontweight='bold')
        plt.colorbar(im, ax=ax7)
        
        # 8. Cumulative Distribution
        ax8 = plt.subplot(3, 3, 8)
        sorted_perc = np.sort(df['Percentage'].values)
        cumulative = np.arange(1, len(sorted_perc) + 1) / len(sorted_perc) * 100
        ax8.plot(sorted_perc, cumulative, linewidth=2, color='#3498db')
        ax8.fill_between(sorted_perc, cumulative, alpha=0.3, color='#3498db')
        ax8.set_title('Cumulative Distribution', fontweight='bold')
        ax8.set_xlabel('Percentage')
        ax8.set_ylabel('Cumulative %')
        ax8.grid(alpha=0.3)
        ax8.axvline(40, color='r', linestyle='--', alpha=0.5)
        
        # 9. Summary Statistics
        ax9 = plt.subplot(3, 3, 9)
        ax9.axis('off')
        
        pass_rate = (~(df[subject_cols] < 40).any(axis=1)).sum() / len(df) * 100
        
        summary = f"""
        SUMMARY STATISTICS
        {'='*35}
        
        Total Students: {len(df)}
        Total Subjects: {len(subject_cols)}
        
        Class Average: {df['Percentage'].mean():.2f}%
        Highest Score: {df['Percentage'].max():.2f}%
        Lowest Score: {df['Percentage'].min():.2f}%
        Std Deviation: {df['Percentage'].std():.2f}
        
        Pass Rate: {pass_rate:.1f}%
        Fail Rate: {100-pass_rate:.1f}%
        
        Top Scorer: {df.loc[df['Percentage'].idxmax(), 'Name']}
        Top Score: {df['Percentage'].max():.2f}%
        """
        
        ax9.text(0.1, 0.5, summary, fontsize=10, fontfamily='monospace',
                verticalalignment='center')
        
        plt.tight_layout()
        plt.show()
        print("\n✓ Visualization displayed!")
    
    def search_student(self):
        """Search for a student across all batches"""
        if not self.batch_files:
            print("\n⚠ No batch data available!")
            return
        
        search_term = input("\nEnter student name or roll number: ").strip().lower()
        
        found = False
        for batch_name, batch_df in self.batch_files.items():
            result = batch_df[
                (batch_df['Name'].str.lower().str.contains(search_term, na=False)) |
                (batch_df['Roll_No'].str.lower().str.contains(search_term, na=False))
            ]
            
            if not result.empty:
                found = True
                subject_cols = [col for col in result.columns if col not in ['Name', 'Roll_No']]
                display_df = result.copy()
                
                if subject_cols:
                    display_df['Total'] = display_df[subject_cols].sum(axis=1)
                    max_marks = len(subject_cols) * 100
                    display_df['Percentage'] = (display_df['Total'] / max_marks * 100).round(2)
                    display_df['Grade'] = display_df['Percentage'].apply(self.calculate_grade)
                
                print(f"\n--- Found in Batch {batch_name} ---")
                print(display_df.to_string(index=False))
        
        if not found:
            print(f"\n⚠ No student found matching '{search_term}'")
        print()
    
    def semester_wise_comparison(self, batch):
        """Compare performance across semesters for a batch"""
        if not batch:
            print("\n⚠ Please select a batch!")
            return
        
        df = self.get_batch_data(batch)
        if df.empty:
            print(f"\n⚠ No data found for batch {batch}!")
            return
        
        subject_cols = [col for col in df.columns if col not in ['Name', 'Roll_No']]
        
        # Group subjects by semester
        semester_data = {}
        for sem in range(1, 9):
            sem_subjects = self.get_subjects_for_semester(sem)
            available_subjects = [s for s in sem_subjects if s in subject_cols]
            if available_subjects:
                semester_data[sem] = {
                    'subjects': available_subjects,
                    'avg': df[available_subjects].mean().mean(),
                    'count': len(available_subjects)
                }
        
        if not semester_data:
            print("\n⚠ No semester data available!")
            return
        
        print("\n" + "="*70)
        print(f"SEMESTER-WISE COMPARISON - BATCH {batch}")
        print("="*70)
        print()
        
        for sem, data in sorted(semester_data.items()):
            print(f"Semester {sem}:")
            print(f"  Subjects: {data['count']}")
            print(f"  Average: {data['avg']:.2f}")
            print(f"  Subjects: {', '.join(data['subjects'])}")
            print()
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(f'Semester-wise Performance - Batch {batch}', fontsize=14, fontweight='bold')
        
        semesters = sorted(semester_data.keys())
        averages = [semester_data[s]['avg'] for s in semesters]
        
        # Line plot
        ax1.plot(semesters, averages, marker='o', linewidth=2, markersize=10, color='#3498db')
        ax1.set_xlabel('Semester')
        ax1.set_ylabel('Average Marks')
        ax1.set_title('Average Performance Trend')
        ax1.grid(alpha=0.3)
        ax1.set_ylim(0, 100)
        ax1.axhline(40, color='r', linestyle='--', alpha=0.5, label='Pass Line')
        ax1.legend()
        
        # Bar plot
        colors = plt.cm.viridis(np.linspace(0, 1, len(semesters)))
        ax2.bar(semesters, averages, color=colors)
        ax2.set_xlabel('Semester')
        ax2.set_ylabel('Average Marks')
        ax2.set_title('Semester-wise Average')
        ax2.set_ylim(0, 100)
        ax2.axhline(40, color='r', linestyle='--', alpha=0.5)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        print("✓ Visualization displayed!")
    
    def batch_selection_menu(self):
        """Menu for selecting batch"""
        batches = self.get_available_batches()
        if not batches:
            print("\n⚠ No batches available!")
            return None
        
        print("\nAvailable Batches:")
        for i, batch in enumerate(batches, 1):
            count = len(self.batch_files[batch])
            print(f"{i}. {batch} ({count} students)")
        
        try:
            choice = int(input(f"\nSelect batch (1-{len(batches)}): "))
            if 1 <= choice <= len(batches):
                return batches[choice - 1]
        except ValueError:
            pass
        
        print("❌ Invalid choice!")
        return None
    
    def semester_selection_menu(self, batch=None):
        """Menu for selecting semester with validation"""
        available_sems = []
        
        if batch:
            available_sems = self.get_available_semesters_for_batch(batch)
            print(available_sems)
            print(f"\nAvailable Semesters for Batch {batch}: {available_sems}")
        
        print("\nSemester Filter:")
        for i in range(1, 9):
            status = "✓" if i in available_sems else "✗" if batch else " "
            print(f"{i}. Semester {i} {status}")
        print("9. All Semesters")
        
        try:
            choice = int(input("\nSelect semester (1-9): "))
            if 1 <= choice <= 8:
                return choice
            elif choice == 9:
                return None
        except ValueError:
            pass
        
        print("❌ Invalid choice!")
        return None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("          COLLEGE STUDENT DASHBOARD SYSTEM")
        print("="*70)
        print("1.  Add Student to Batch")
        print("2.  View Batch Students")
        print("3.  View Batch Students (with Semester Filter)")
        print("4.  Calculate Statistics for Batch")
        print("5.  Calculate Statistics (with Semester Filter)")
        print("6.  Visualize Batch Data")
        print("7.  Visualize Data (with Semester Filter)")
        print("8.  Semester-wise Comparison")
        print("9.  Search Student (across all batches)")
        print("10. Show All Batches Info")
        print("11. Exit")
        print("="*70)
    
    def run(self):
        """Main program loop"""
        print("\n🎓 Welcome to College Student Dashboard System!")
        print()
        
        if not self.batch_files:
            print("⚠ No batch data found! Please run the dataset generator first.")
            return
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-11): ").strip()
            
            if choice == '1':
                self.add_student_to_batch()
                
            elif choice == '2':
                batch = self.batch_selection_menu()
                if batch:
                    self.view_batch_students(batch)
                    
            elif choice == '3':
                batch = self.batch_selection_menu()
                if batch:
                    semester = self.semester_selection_menu()
                    self.view_batch_students(batch, semester)
                    
            elif choice == '4':
                batch = self.batch_selection_menu()
                if batch:
                    self.calculate_statistics(batch)
                    
            elif choice == '5':
                batch = self.batch_selection_menu()
                if batch:
                    semester = self.semester_selection_menu()
                    self.calculate_statistics(batch, semester)
                    
            elif choice == '6':
                batch = self.batch_selection_menu()
                if batch:
                    self.visualize_data(batch)
                    
            elif choice == '7':
                batch = self.batch_selection_menu()
                if batch:
                    semester = self.semester_selection_menu()
                    self.visualize_data(batch, semester)
                    
            elif choice == '8':
                batch = self.batch_selection_menu()
                if batch:
                    self.semester_wise_comparison(batch)
                    
            elif choice == '9':
                self.search_student()
                
            elif choice == '10':
                print("\n" + "="*70)
                print("AVAILABLE BATCHES")
                print("="*70)
                for batch in self.get_available_batches():
                    batch_df = self.batch_files[batch]
                    subject_cols = [col for col in batch_df.columns if col not in ['Name', 'Roll_No']]
                    max_sem = max([self.subjects_semester[self.subjects_semester['Subject'] == s]['Semester'].values[0] 
                                    for s in subject_cols if s in self.subjects_semester['Subject'].values])
                    
                    print(f"\nBatch: {batch}")
                    print(f"  Students: {len(batch_df)}")
                    print(f"  Semesters Completed: {max_sem}")
                    print(f"  Total Subjects: {len(subject_cols)}")
                print()
                
            elif choice == '11':
                print("\nThank you for using College Student Dashboard System!")
                print("Goodbye! 👋\n")
                break
                
            else:
                print("\n❌ Invalid choice! Please enter a number between 1 and 11.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    dashboard = CollegeDashboard()
    dashboard.run()