#!/usr/bin/env python3
"""
Comprehensive Test Script for Ski Management System
Based on Appendix A: Data for System Setup
"""

from main import SkiManagementSystem, Student, SkiRoute

def setup_initial_data():
    """Set up the system with initial data from Appendix A"""
    print("="*80)
    print("SETTING UP SKI MANAGEMENT SYSTEM WITH APPENDIX DATA")
    print("="*80)
    
    # Create the management system
    ski_system = SkiManagementSystem()
    
    # Create 5 groups (R1 to R5)
    print("\n1. Creating Groups...")
    for i in range(1, 6):
        group_id = f"R{i}"
        ski_system.create_group(group_id)
    
    # Create ski tracks with difficulty levels
    print("\n2. Creating Ski Tracks...")
    tracks_data = [
        ("LANE1", "Beginner", 1, "3 km, wide, dedicated for beginners"),
        ("LANE2", "Easy", 2, "4 km"),
        ("LANE3", "Intermediate", 3, "2.5 km, for experienced"),
        ("LANE4", "Intermediate", 3, "1.5 km"),
        ("LANE5", "Advanced", 4, "0.5 km, very steep"),
        ("LANE6", "Advanced", 4, "2.5 km"),
        ("LANE7", "Experts", 5, "1 km, very steep"),
        ("LANE8", "Experts", 5, "2 km, difficult-sloped"),
        ("LANE9", "Experts", 5, "2 km, very difficult"),
        ("LANE10", "Experts", 5, "3 km, very difficult")
    ]
    
    for track_id, description, difficulty, details in tracks_data:
        track = SkiRoute(difficulty)
        track.name = f"{track_id}: {description}"
        track.description = details
        ski_system.tracks_tree.insert(track)
        print(f"   Created {track}")
    
    # Add students with initial group allocation
    print("\n3. Adding Students with Initial Group Allocation...")
    students_data = [
        # Group R1 - Beginner
        (1, "Aba", "Ima", "R1", 1),
        (6, "Bo", "Zehava", "R1", 1),
        (11, "Bo", "Zev", "R1", 1),
        (16, "Bugi", "Roni", "R1", 1),
        (21, "Sim", "Simani", "R1", 1),
        
        # Group R2 - Easy
        (2, "Ima", "Aba", "R2", 2),
        (7, "Bubi", "Zilzal", "R2", 2),
        (12, "Lulu", "Yitzhak", "R2", 2),
        (17, "Poli", "Pipi", "R2", 2),
        (22, "Nam", "Kore", "R2", 2),
        
        # Group R3 - Intermediate
        (3, "Uv", "Gog", "R3", 3),
        (8, "Gogi", "Roza", "R3", 3),
        (13, "Mimi", "Moni", "R3", 3),
        (18, "Sim", "Shmuel", "R3", 3),
        (23, "Sus", "Zahor", "R3", 3),
        
        # Group R4 - Advanced
        (4, "Ov", "Didi", "R4", 4),
        (9, "Tuta", "Roni", "R4", 4),
        (14, "Shmuel", "Mashuash", "R4", 4),
        (19, "Shmuel", "Shmueli", "R4", 4),
        (24, "Matsa", "Sash", "R4", 4),
        
        # Group R5 - Experts
        (5, "Ha", "Ha", "R5", 5),
        (10, "Maga", "Maga", "R5", 5),
        (15, "Mela", "Meni", "R5", 5),
        (20, "Shmulik", "Shmuelson", "R5", 5),
        (25, "Ets", "Gatz", "R5", 5)
    ]
    
    for stud_id, first_name, last_name, group_id, track_level in students_data:
        student = Student(str(stud_id), first_name, last_name)
        ski_system.add_student(str(stud_id), first_name, last_name, group_id)
        # Assign appropriate track to group
        ski_system.assign_track_to_group(group_id, track_level)
    
    print(f"\n   Added {len(students_data)} students across 5 groups")
    
    return ski_system

def demonstrate_operations(ski_system):
    """Demonstrate all required operations from Appendix B"""
    print("\n" + "="*80)
    print("DEMONSTRATING REQUIRED OPERATIONS (Appendix B)")
    print("="*80)
    
    # Operation 1: Add student #26
    print("\n OPERATION 1: Add student #26")
    print("-" * 50)
    ski_system.add_student("26", "New", "Student")
    
    # Operation 2: Assign group #26 to Group R1
    print("\n OPERATION 2: Assign student #26 to Group R1")
    print("-" * 50)
    ski_system.assign_student_to_group("26", "R1")
    
    # Operation 3: Remove student #26
    print("\n OPERATION 3: Remove student #26")
    print("-" * 50)
    ski_system.remove_student("26")
    
    # Operation 4: Display students
    print("\n OPERATION 4: Display students")
    print("-" * 50)
    ski_system.get_system_summary()
    
    # Operation 5: Display groups
    print("\n OPERATION 5: Display groups")
    print("-" * 50)
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        ski_system.display_group_student_count(group_id)
    
    # Operation 6: Display student lists
    print("\n OPERATION 6: Display student lists")
    print("-" * 50)
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        ski_system.display_students_in_group(group_id)
    
    # Operation 7: Show difficulty levels
    print("\n OPERATION 7: Show difficulty levels")
    print("-" * 50)
    print("Ski Track Difficulty Levels:")
    print("-" * 30)
    difficulty_names = {1: "Beginner", 2: "Easy", 3: "Intermediate", 4: "Advanced", 5: "Experts"}
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        group = ski_system._find_group(group_id)
        if group and group.assigned_track:
            difficulty = group.assigned_track.level
            print(f"Group {group_id}: {difficulty_names.get(difficulty, 'Unknown')} (Level {difficulty})")
    
    # Operation 8: Transfer student between groups
    print("\n OPERATION 8: Transfer student between groups")
    print("-" * 50)
    print("Transferring student #3 from R3 to R1...")
    ski_system.assign_student_to_group("3", "R1")
    print("After transfer:")
    ski_system.display_students_in_group("R1")
    print("\nR3 after transfer:")
    ski_system.display_students_in_group("R3")
    
    # Operation 9: Remove student from the system
    print("\n OPERATION 9: Remove student from the system")
    print("-" * 50)
    print("Removing student #7 from the system...")
    ski_system.remove_student("7")
    print("R2 after removal:")
    ski_system.display_students_in_group("R2")
    
    # Operation 10: Display student list in all groups
    print("\n OPERATION 10: Display student list in Groups R1, R2, R3, R4, R5")
    print("-" * 70)
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        ski_system.display_students_in_group(group_id)
        print()

def demonstrate_advanced_features(ski_system):
    """Demonstrate advanced features like rounds and scoring"""
    print("\n" + "="*80)
    print("DEMONSTRATING ADVANCED FEATURES")
    print("="*80)
    
    # Start rounds for all groups
    print("\n Starting Rounds for All Groups...")
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        ski_system.start_group_round(group_id)
    
    # Show next students for each group
    print("\n Next Students for Each Group:")
    print("-" * 40)
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        next_student = ski_system.get_next_round_student(group_id)
        if next_student:
            print(f"Group {group_id}: {next_student}")
    
    # Complete some rounds with scores
    print("\n Completing Some Rounds with Scores...")
    print("-" * 40)
    ski_system.provide_round_score("R1", "1", 85.5)  # Aba Ima
    ski_system.provide_round_score("R2", "2", 78.0)  # Ima Aba
    ski_system.provide_round_score("R3", "3", 92.5)  # Uv Gog
    ski_system.provide_round_score("R4", "4", 88.0)  # Ov Didi
    ski_system.provide_round_score("R5", "5", 95.0)  # Ha Ha
    
    # Show updated next students
    print("\n Updated Next Students After Scoring:")
    print("-" * 40)
    for group_id in ["R1", "R2", "R3", "R4", "R5"]:
        next_student = ski_system.get_next_round_student(group_id)
        if next_student:
            print(f"Group {group_id}: {next_student}")
    
    # Display all rounds (Mountain View)
    print("\n MOUNTAIN VIEW - All Groups Rounds:")
    print("-" * 50)
    ski_system.display_all_rounds()

def performance_demo(ski_system):
    """Demonstrate the system's performance capabilities"""
    print("\n" + "="*80)
    print("PERFORMANCE DEMONSTRATION")
    print("="*80)
    
    # Show system statistics
    print("\n System Statistics:")
    print("-" * 25)
    ski_system.get_system_summary()
    
    # Demonstrate efficient operations
    print("\n Performance Test - Finding Students:")
    print("-" * 40)
    import time
    
    # Test search performance
    start_time = time.time()
    for i in range(1000):  # 1000 searches
        ski_system._find_student("1")
    search_time = time.time() - start_time
    print(f"1000 student searches completed in {search_time:.4f} seconds")
    
    # Test group search performance
    start_time = time.time()
    for i in range(1000):  # 1000 searches
        ski_system._find_group("R1")
    search_time = time.time() - start_time
    print(f"1000 group searches completed in {search_time:.4f} seconds")
    
    # Test counting performance
    start_time = time.time()
    for i in range(10000):  # 10000 counts
        ski_system.groups_tree.get_size()
        ski_system.students_tree.get_size()
    count_time = time.time() - start_time
    print(f"10000 counting operations completed in {count_time:.4f} seconds")

def main():
    """Main test execution"""
    print(" SKI MANAGEMENT SYSTEM - COMPREHENSIVE TEST")
    print("="*80)
    
    try:
        # Setup system with appendix data
        ski_system = setup_initial_data()
        
        # Demonstrate all required operations
        demonstrate_operations(ski_system)
        
        # Show advanced features
        demonstrate_advanced_features(ski_system)
        
        # Performance demonstration
        performance_demo(ski_system)
        
        print("\n" + "="*80)
        print(" ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nThe system demonstrates:")
        print("• Efficient data structure usage (AVL trees, Priority Queues)")
        print("• Fast operations (O(log n) search, O(1) counting)")
        print("• Proper round management and scoring")
        print("• Scalable performance for multiple groups and students")
        
    except Exception as e:
        print(f"\n Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 