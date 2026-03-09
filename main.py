class AVLNode:
    def __init__(self, data: any, parent=None, left=None, right=None) -> None:
        self.data = data
        self.left = left
        self.parent = parent
        self.right = right
        self.height = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def increase_height(self):
        if self.height is None:
            self.height = 1
        else:
            self.height += 1

    def decrease_height(self):
        if self.height is None:
            raise ValueError("Cannot decrease height of a leaf")
        else:
            self.height -= 1

    def no_left(self):
        return self.left is None

    def no_right(self):
        return self.right is None


class AVLTree:
    def __init__(self, initial_data_list: list[any]) -> None:
        self.root = None
        self.size = 0  # Add size counter for O(1) counting
        if initial_data_list:
            for data in initial_data_list:
                self.insert(data)

    def _get_height(self, node: AVLNode | None) -> int:
        if node is None:
            return 0
        if node.height is None:
            return 1
        return node.height

    def _get_balance_factor(self, node: AVLNode) -> int:
        """Calculate balance factor: left_height - right_height"""
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return left_height - right_height

    def _is_balanced(self, node: AVLNode) -> bool:
        """Check if a node is balanced (balance factor between -1 and 1)"""
        balance_factor = self._get_balance_factor(node)
        return -1 <= balance_factor <= 1

    def _insert(self, root: AVLNode | None, data: any):
        if root is None:
            return AVLNode(data=data)

        if root.is_leaf():
            root.increase_height()
            if root.data > data:
                root.left = AVLNode(data=data, parent=root)
                return root.left
            elif root.data < data:
                root.right = AVLNode(data=data, parent=root)
                return root.right
        elif root.no_left():
            if root.data > data:
                root.left = AVLNode(data=data, parent=root)
                return root.left
            else:
                return self._insert(root.right, data)
        elif root.no_right():
            if root.data < data:
                root.right = AVLNode(data=data, parent=root)
                return root.right
            else:
                return self._insert(root.left, data)
        else:
            if root.data > data:
                return self._insert(root.left, data)
            else:
                return self._insert(root.right, data)

    def insert(self, data: any):
        if not self.root:
            # first node in DS
            self.root = AVLNode(data=data)
            self.size = 1  # Update size
            return self.root
        else:
            new_node = self._insert(self.root, data)
            self.size += 1  # Update size
            # After insertion, check balance and rebalance if needed
            self._rebalance_after_insertion(new_node)
            return new_node

    def _rebalance_after_insertion(self, node: AVLNode):
        """Check balance up the tree and rebalance if needed"""
        current = node
        while current is not None:
            # Update height of current node
            self._update_height(current)

            # Check if current node is unbalanced
            if not self._is_balanced(current):
                # Node is unbalanced, need to rebalance
                self._rebalance(current)
                break

            current = current.parent

    def _update_height(self, node: AVLNode):
        """Update the height of a node based on its children"""
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        node.height = max(left_height, right_height) + 1

    def _rebalance(self, node: AVLNode):
        """Rebalance an unbalanced node using rotations"""
        balance_factor = self._get_balance_factor(node)

        # Left heavy
        if balance_factor > 1:
            # Check if it's Left-Left case
            if self._get_balance_factor(node.left) >= 0:
                self._right_rotate(node)
            # Left-Right case
            else:
                self._left_rotate(node.left)
                self._right_rotate(node)

        # Right heavy
        elif balance_factor < -1:
            # Check if it's Right-Right case
            if self._get_balance_factor(node.right) <= 0:
                self._left_rotate(node)
            # Right-Left case
            else:
                self._right_rotate(node.right)
                self._left_rotate(node)


    def min(self) -> AVLNode | None:
        """Find the minimum node in the tree O(log n)"""
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current

    def max(self) -> AVLNode | None:
        """Find the maximum node in the tree O(log n)"""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current

    def _left_rotate(self, node: AVLNode):
        """Perform left rotation"""
        right_child = node.right
        if right_child is None:
            return

        # Update parent references
        if node.parent:
            if node.parent.left == node:
                node.parent.left = right_child
            else:
                node.parent.right = right_child
        else:
            self.root = right_child

        right_child.parent = node.parent
        node.parent = right_child

        # Update children
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.left = node

        # Update heights
        self._update_height(node)
        self._update_height(right_child)

    def _right_rotate(self, node: AVLNode):
        """Perform right rotation"""
        left_child = node.left
        if left_child is None:
            return

        # Update parent references
        if node.parent:
            if node.parent.left == node:
                node.parent.left = left_child
            else:
                node.parent.right = left_child
        else:
            self.root = left_child

        left_child.parent = node.parent
        node.parent = left_child

        # Update children
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.right = node

        # Update heights
        self._update_height(node)
        self._update_height(left_child)

    def search(self, data: any) -> AVLNode | None:
        """Search for a node with the given data"""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node: AVLNode | None, data: any) -> AVLNode | None:
        """Recursively search for a node with the given data"""
        if node is None:
            return None

        if node.data == data:
            return node
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def delete(self, data: any) -> bool:
        """Delete a node with the given data. Returns True if found and deleted, False otherwise."""
        node_to_delete = self.search(data)
        if node_to_delete is None:
            return False

        self._delete_node(node_to_delete)
        self.size -= 1  # Update size
        return True

    def _delete_node(self, node: AVLNode):
        """Delete a specific node and rebalance the tree"""
        # Case 1: Node is a leaf
        if node.is_leaf():
            self._delete_leaf(node)

        # Case 2: Node has only one child
        elif node.no_left():
            self._delete_node_with_one_child(node, node.right)
        elif node.no_right():
            self._delete_node_with_one_child(node, node.left)

        # Case 3: Node has two children
        else:
            self._delete_node_with_two_children(node)

    def _delete_leaf(self, node: AVLNode):
        """Delete a leaf node"""
        if node.parent is None:
            # This is the root node
            self.root = None
        else:
            # Update parent's child reference
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None

            # Rebalance starting from parent
            self._rebalance_after_deletion(node.parent)

    def _delete_node_with_one_child(self, node: AVLNode, child: AVLNode):
        """Delete a node with exactly one child"""
        if node.parent is None:
            # This is the root node
            self.root = child
            child.parent = None
        else:
            # Update parent's child reference
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
            child.parent = node.parent

            # Rebalance starting from parent
            self._rebalance_after_deletion(node.parent)

    def _delete_node_with_two_children(self, node: AVLNode):
        """Delete a node with two children by replacing it with its successor"""
        # Find the successor (leftmost node in right subtree)
        successor = self._find_successor(node)

        # Copy successor's data to the node to be deleted
        node.data = successor.data

        # Delete the successor (which has at most one child)
        if successor.is_leaf():
            self._delete_leaf(successor)
        else:
            # Successor must have a right child (since it's the leftmost in right subtree)
            self._delete_node_with_one_child(successor, successor.right)

    def _find_successor(self, node: AVLNode) -> AVLNode:
        """Find the successor of a node (leftmost node in right subtree)"""
        current = node.right
        while current.left is not None:
            current = current.left
        return current

    def _rebalance_after_deletion(self, node: AVLNode):
        """Check balance up the tree after deletion and rebalance if needed"""
        current = node
        while current is not None:
            # Update height of current node
            self._update_height(current)

            # Check if current node is unbalanced
            if not self._is_balanced(current):
                # Node is unbalanced, need to rebalance
                self._rebalance(current)
                # After rebalancing, continue up the tree as heights may have changed

            current = current.parent

    def check_balance(self) -> bool:
        """Check if the entire tree is balanced"""
        return self._check_balance_recursive(self.root)

    def _check_balance_recursive(self, node: AVLNode | None) -> bool:
        """Recursively check if all nodes are balanced"""
        if node is None:
            return True

        # Check current node
        if not self._is_balanced(node):
            print(
                f"Node {node.data} is unbalanced! Balance factor: {self._get_balance_factor(node)}"
            )
            return False

        # Check left and right subtrees
        left_balanced = self._check_balance_recursive(node.left)
        right_balanced = self._check_balance_recursive(node.right)

        return left_balanced and right_balanced

    def get_size(self) -> int:
        """Get the number of nodes in the tree - O(1) operation"""
        return self.size

    def is_empty(self) -> bool:
        """Check if tree is empty - O(1) operation"""
        return self.size == 0


class Student:

    def __init__(
        self,
        stud_id: str,
        first_name: str = None,
        last_name: str = None,
        group_id: int | None = None,
        group_ord: int | None = None,
    ) -> None:
        self.stud_id = stud_id
        self.first_name = first_name
        self.last_name = last_name
        self.group_id = group_id
        self.group_ord = group_ord

    def __lt__(self, other):
        """For AVL tree comparison - compare by student ID"""
        if not isinstance(other, Student):
            return False
        return self.stud_id < other.stud_id

    def __eq__(self, other):
        """For AVL tree comparison - equal if same student ID"""
        if not isinstance(other, Student):
            return False
        return self.stud_id == other.stud_id

    def __str__(self):
        return f"{self.stud_id}: {self.first_name} {self.last_name}"

    def get_full_name(self):
        """Get student's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.stud_id


class SkiRoute:

    def __init__(self, level: int) -> None:
        self.level = level
        self.name = f"Level {level} Route"
        self.max_students = 10  # Maximum students that can safely use this route

    def __lt__(self, other):
        """For AVL tree comparison - compare by level"""
        if not isinstance(other, SkiRoute):
            return False
        return self.level < other.level

    def __eq__(self, other):
        """For AVL tree comparison - equal if same level"""
        if not isinstance(other, SkiRoute):
            return False
        return self.level == other.level

    def __str__(self):
        return f"{self.name} (Difficulty: {self.level})"

    def can_accommodate_group(self, group_size: int) -> bool:
        """Check if this route can safely accommodate a group of given size"""
        return group_size <= self.max_students


class Round:
    def __init__(self, round_number: int, student: Student, score: float = None):
        self.round_number = round_number
        self.student = student
        self.score = score
        self.completed = False
        self.priority = student.group_ord  # Priority based on student order

    def __lt__(self, other):
        """For priority queue comparison - lower order number = higher priority"""
        if not isinstance(other, Round):
            return False
        return self.priority < other.priority

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        score_str = f" (Score: {self.score})" if self.score is not None else ""
        return f"Round {self.round_number}: {self.student} - {status}{score_str}"

    def complete_round(self, score: float):
        """Mark round as completed with a score"""
        self.score = score
        self.completed = True


class PriorityQueue:
    """Min-heap based priority queue for efficient round management"""
    
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def is_empty(self) -> bool:
        """Check if queue is empty - O(1)"""
        return self.size == 0
    
    def get_size(self) -> int:
        """Get queue size - O(1)"""
        return self.size
    
    def enqueue(self, item):
        """Add item to priority queue - O(log n)"""
        self.heap.append(item)
        self.size += 1
        self._bubble_up(self.size - 1)
    
    def dequeue(self):
        """Remove and return highest priority item - O(log n)"""
        if self.is_empty():
            return None
        
        if self.size == 1:
            self.size -= 1
            return self.heap.pop()
        
        # Swap root with last element
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.size -= 1
        
        # Bubble down the new root
        self._bubble_down(0)
        return root
    
    def peek(self):
        """View highest priority item without removing - O(1)"""
        return self.heap[0] if not self.is_empty() else None
    
    def _bubble_up(self, index):
        """Bubble up element to maintain heap property - O(log n)"""
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._bubble_up(parent)
    
    def _bubble_down(self, index):
        """Bubble down element to maintain heap property - O(log n)"""
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < self.size and self.heap[left] < self.heap[smallest]:
            smallest = left
        
        if right < self.size and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)
    
    def contains(self, item) -> bool:
        """Check if item exists in queue - O(n) but optimized for small queues"""
        return item in self.heap
    
    def remove(self, item) -> bool:
        """Remove specific item from queue - O(n) but optimized for small queues"""
        try:
            self.heap.remove(item)
            self.size -= 1
            # Rebuild heap to maintain property
            self._rebuild_heap()
            return True
        except ValueError:
            return False
    
    def _rebuild_heap(self):
        """Rebuild heap after removal - O(n)"""
        for i in range(self.size // 2 - 1, -1, -1):
            self._bubble_down(i)


class SkiGroup:
    def __init__(self, id: str) -> None:
        self.id = id
        self.tree = AVLTree([])
        self.students_ordered = []  # Maintain round order efficiently
        self.next_order = 1
        self.current_round = 0
        self.assigned_track = None
        self.round_queue = PriorityQueue()  # Priority queue for active rounds

    def __lt__(self, other):
        """For AVL tree comparison - compare by group ID"""
        if not isinstance(other, SkiGroup):
            return False
        return self.id < other.id

    def __eq__(self, other):
        """For AVL tree comparison - equal if same group ID"""
        if not isinstance(other, SkiGroup):
            return False
        return self.id == other.id

    def add_student(self, student: Student) -> bool:
        """Add a new student to the group"""
        if self.search_student(student.stud_id):
            print(f"Student {student.stud_id} already exists in group {self.id}")
            return False
        
        # Set group ID and order (order based on when they were added)
        student.group_id = self.id
        student.group_ord = self.next_order
        self.next_order += 1
        
        # Add to tree and ordered list
        self.tree.insert(student)
        self.students_ordered.append(student)
        
        print(f"Student {student.stud_id} added to group {self.id} with order {student.group_ord}")
        return True


    def min_student(self) -> Student | None:
        """Get the minimum student in the group O(log n)"""
        node = self.tree.min()
        if node is None:
            return None
        return node.data

    def remove_student(self, student_id: str) -> bool:
        """Remove a student from the group"""
        student = self.search_student(student_id)
        if not student:
            print(f"Student {student_id} not found in group {self.id}")
            return False
        
        # Remove from tree and ordered list
        self.tree.delete(student)
        self.students_ordered.remove(student)
        
        # Remove from round queue if present
        if hasattr(self, 'rounds'):
            for round_obj in self.rounds:
                if round_obj.student.stud_id == student_id:
                    self.round_queue.remove(round_obj)
                    break
        
        # Reorder remaining students to maintain sequential order
        self._reorder_students()
        
        print(f"Student {student_id} removed from group {self.id}")
        return True

    def _reorder_students(self):
        """Reorder students to maintain sequential order after removal"""
        # Reset order numbers
        self.next_order = 1
        for student in self.students_ordered:
            student.group_ord = self.next_order
            self.next_order += 1

    def search_student(self, id: str) -> Student | None:
        """Search for a student by ID"""
        node = self.tree.search(Student(stud_id=id))
        if not node:
            return None
        return node.data

    def get_student_count(self) -> int:
        """Get the number of students in the group - O(1) operation"""
        return self.tree.get_size()

    def display_students(self):
        """Display all students in the group in their round order - O(n) but optimized"""
        if not self.students_ordered:
            print(f"Group {self.id} has no students")
            return
        
        print(f"\nStudents in Group {self.id} (in round order):")
        print("-" * 50)
        for student in self.students_ordered:
            print(f"{student.group_ord}. {student}")

    def assign_track(self, track: SkiRoute) -> bool:
        """Assign a ski track to the group"""
        group_size = self.get_student_count()  # O(1) operation
        if not track.can_accommodate_group(group_size):
            print(f"Track {track} cannot accommodate group size {group_size}")
            return False
        
        self.assigned_track = track
        print(f"Track {track} assigned to Group {self.id}")
        return True

    def get_round_count(self) -> int:
        """Get the number of rounds in the group"""
        return self.round_queue.get_size() if hasattr(self, 'rounds') else 0

    def start_new_round(self) -> bool:
        """Start a new round for the group"""
        if not self.students_ordered:
            print(f"No students in group {self.id} to start a round")
            return False
        
        self.current_round += 1
        # Create rounds for all students in their original order
        self.rounds = []
        self.round_queue = PriorityQueue()  # Reset priority queue
        
        for student in self.students_ordered:
            round_obj = Round(self.current_round, student)
            self.rounds.append(round_obj)
            self.round_queue.enqueue(round_obj)  # Add to priority queue
        
        print(f"Round {self.current_round} started for Group {self.id}")
        return True

    def get_next_student(self) -> Student | None:
        """Get the next student for the current round - O(1) operation"""
        if not hasattr(self, 'rounds') or self.round_queue.is_empty():
            print(f"No active rounds in group {self.id}")
            return None
        
        # Get next student from priority queue
        next_round = self.round_queue.peek()
        if next_round and not next_round.completed:
            return next_round.student
        
        print(f"All rounds completed in group {self.id}")
        return None

    def complete_student_round(self, student_id: str, score: float) -> bool:
        """Complete a student's round with a score"""
        student = self.search_student(student_id)
        if not student:
            print(f"Student {student_id} not found in group {self.id}")
            return False
        
        if not hasattr(self, 'rounds'):
            print(f"No active rounds in group {self.id}")
            return False
        
        # Find the round for this student
        for round_obj in self.rounds:
            if round_obj.student.stud_id == student_id and not round_obj.completed:
                round_obj.complete_round(score)
                # Remove from priority queue since it's completed
                self.round_queue.remove(round_obj)
                print(f"Round completed for {student_id} with score {score}")
                return True
        
        print(f"No active round found for student {student_id}")
        return False

    def remove_student_from_round(self, student_id: str) -> bool:
        """Remove a student from the current round (terminate their turn)"""
        student = self.search_student(student_id)
        if not student:
            print(f"Student {student_id} not found in group {self.id}")
            return False
        
        if not hasattr(self, 'rounds'):
            print(f"No active rounds in group {self.id}")
            return False
        
        # Find and mark the round as completed (terminated)
        for round_obj in self.rounds:
            if round_obj.student.stud_id == student_id and not round_obj.completed:
                round_obj.completed = True
                round_obj.score = 0  # Terminated rounds get 0 score
                # Remove from priority queue since it's completed
                self.round_queue.remove(round_obj)
                print(f"Student {student_id} removed from round {self.current_round}")
                return True
        
        print(f"No active round found for student {student_id}")
        return False

    def display_rounds(self):
        """Display all rounds in the group"""
        if not hasattr(self, 'rounds') or not self.rounds:
            print(f"No rounds in group {self.id}")
            return
        
        print(f"\nRounds in Group {self.id}:")
        print("-" * 40)
        for round_obj in self.rounds:
            print(round_obj)

    def get_round_summary(self) -> dict:
        """Get a summary of all rounds and scores"""
        student_scores = {}
        
        if hasattr(self, 'rounds'):
            for round_obj in self.rounds:
                if round_obj.completed and round_obj.score is not None:
                    student_scores[round_obj.student.stud_id] = round_obj.score
        
        summary = {
            'group_id': self.id,
            'total_students': self.get_student_count(),  # O(1) operation
            'completed_rounds': len([r for r in self.rounds if r.completed]) if hasattr(self, 'rounds') else 0,
            'student_scores': student_scores,
            'assigned_track': str(self.assigned_track) if self.assigned_track else "None"
        }
        return summary


class SkiManagementSystem:
    def __init__(self):
        """Initialize the ski management system"""
        self.groups_tree = AVLTree([])  # AVL tree of groups ordered by ID
        self.students_tree = AVLTree([])  # AVL tree of students ordered by ID
        self.tracks_tree = AVLTree([])  # AVL tree of tracks ordered by level
        self.next_group_id = 1
        self.next_track_id = 1

    def create_group(self, group_id: str = None) -> str:
        """Create a new ski group"""
        if group_id is None:
            group_id = f"Group{self.next_group_id}"
            self.next_group_id += 1
        
        # Check if group already exists using tree search
        existing_group = self.groups_tree.search(SkiGroup(group_id))
        if existing_group:
            print(f"Group {group_id} already exists")
            return None
        
        new_group = SkiGroup(group_id)
        self.groups_tree.insert(new_group)
        print(f"Group {group_id} created successfully")
        return group_id

    def add_student(self, stud_id: str, first_name: str = None, last_name: str = None, group_id: str = None) -> bool:
        """Add a new student to the system"""
        # Check if student already exists using tree search
        existing_student = self.students_tree.search(Student(stud_id=stud_id))
        if existing_student:
            print(f"Student {stud_id} already exists in the system")
            return False
        
        # Create new student
        student = Student(stud_id, first_name, last_name)
        self.students_tree.insert(student)
        
        # Add to group if specified
        if group_id:
            group = self._find_group(group_id)
            if not group:
                print(f"Group {group_id} does not exist")
                return False
            return group.add_student(student)
        else:
            print(f"Student {stud_id} added to system (not assigned to any group)")
            return True

    def remove_student(self, stud_id: str) -> bool:
        """Remove a student from the system"""
        student = self._find_student(stud_id)
        if not student:
            print(f"Student {stud_id} not found in the system")
            return False
        
        # Remove from group if assigned
        if student.group_id:
            group = self._find_group(student.group_id)
            if group:
                group.remove_student(stud_id)
        
        # Remove from system tree
        self.students_tree.delete(student)
        print(f"Student {stud_id} removed from the system")
        return True

    def assign_student_to_group(self, stud_id: str, group_id: str) -> bool:
        """Assign a student to a specific group"""
        student = self._find_student(stud_id)
        if not student:
            print(f"Student {stud_id} not found in the system")
            return False
        
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found in the system")
            return False
        
        # Remove from current group if any
        if student.group_id:
            current_group = self._find_group(student.group_id)
            if current_group:
                current_group.remove_student(stud_id)
        
        # Add to new group
        return group.add_student(student)

    def display_group_student_count(self, group_id: str):
        """Display the number of students in a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return
        
        count = group.get_student_count()
        print(f"Group {group_id} has {count} students")

    def display_student_in_group(self, stud_id: str, group_id: str):
        """Display student information if they exist in the group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return
        
        student = group.search_student(stud_id)
        if student:
            print(f"Student {stud_id} found in Group {group_id}: {student}")
        else:
            print(f"Student {stud_id} not found in Group {group_id}")

    def display_round_count(self, group_id: str):
        """Display the number of rounds in a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return
        
        count = group.get_round_count()
        print(f"Group {group_id} has {count} rounds")

    def display_student_assignment(self, group_id: str):
        """Display student assignment in a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return
        
        group.display_students()

    def remove_student_from_round(self, stud_id: str, group_id: str) -> bool:
        """Remove a student from their current round (terminate turn)"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return False
        
        return group.remove_student_from_round(stud_id)

    def display_all_rounds(self):
        """Display rounds in all groups (Mountain View)"""
        if not self.groups_tree.root:
            print("No groups exist in the system")
            return
        
        print("\n" + "="*60)
        print("MOUNTAIN VIEW - ROUNDS IN ALL GROUPS")
        print("="*60)
        
        # Traverse groups tree efficiently
        self._display_groups_rounds(self.groups_tree.root)

    def _display_groups_rounds(self, node):
        """Efficiently display rounds for all groups using tree traversal"""
        if node:
            self._display_groups_rounds(node.left)
            
            group = node.data
            if hasattr(group, 'rounds') and group.rounds:
                print(f"\n{group.id}:")
                group.display_rounds()
            else:
                print(f"\n{group.id}: No active rounds")
            
            self._display_groups_rounds(node.right)

    def get_next_round_student(self, group_id: str) -> Student | None:
        """Get the next student for the current round in a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return None
        
        return group.get_next_student()

    def display_students_in_group(self, group_id: str):
        """Display all students in a specific group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return
        
        group.display_students()

    def assign_track_to_group(self, group_id: str, track_level: int) -> bool:
        """Assign a ski track to a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return False
        
        # Create track if it doesn't exist
        track_id = f"Track{track_level}"
        track = self._find_track(track_level)
        if not track:
            track = SkiRoute(track_level)
            self.tracks_tree.insert(track)
        
        return group.assign_track(track)

    def min_student_in_group(self, group_id: str) -> Student | None:
        """Get the minimum student in a group O(log n)"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return None
        return group.min_student()

    def provide_round_score(self, group_id: str, stud_id: str, score: float) -> bool:
        """Provide a round score for a student in a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return False
        
        return group.complete_student_round(stud_id, score)

    def start_group_round(self, group_id: str) -> bool:
        """Start a new round for a group"""
        group = self._find_group(group_id)
        if not group:
            print(f"Group {group_id} not found")
            return False
        
        return group.start_new_round()

    def get_system_summary(self):
        """Get a complete summary of the system"""
        print("\n" + "="*60)
        print("SKI MANAGEMENT SYSTEM SUMMARY")
        print("="*60)
        
        # Count efficiently using O(1) size operations
        group_count = self.groups_tree.get_size()
        student_count = self.students_tree.get_size()
        track_count = self.tracks_tree.get_size()
        
        print(f"\nTotal Groups: {group_count}")
        print(f"Total Students: {student_count}")
        print(f"Total Tracks: {track_count}")
        
        # Display group summaries efficiently
        self._display_group_summaries(self.groups_tree.root)

    def _count_nodes(self, node) -> int:
        """Count nodes in a tree efficiently"""
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _display_group_summaries(self, node):
        """Efficiently display group summaries using tree traversal"""
        if node:
            self._display_group_summaries(node.left)
            
            group = node.data
            summary = group.get_round_summary()
            print(f"\n{group.id}:")
            print(f"  Students: {summary['total_students']}")
            print(f"  Completed Rounds: {summary['completed_rounds']}")
            print(f"  Track: {summary['assigned_track']}")
            if summary['student_scores']:
                print(f"  Scores: {summary['student_scores']}")
            
            self._display_group_summaries(node.right)

    def _find_group(self, group_id: str) -> SkiGroup | None:
        """Find a group by ID - O(log n) using AVL tree"""
        node = self.groups_tree.search(SkiGroup(group_id))
        return node.data if node else None

    def _find_student(self, stud_id: str) -> Student | None:
        """Find a student by ID - O(log n) using AVL tree"""
        node = self.students_tree.search(Student(stud_id=stud_id))
        return node.data if node else None

    def _find_track(self, track_level: int) -> SkiRoute | None:
        """Find a track by level - O(log n) using AVL tree"""
        node = self.tracks_tree.search(SkiRoute(track_level))
        return node.data if node else None

    def run_demo(self):
        """Run a demonstration of the system"""
        print("SKI MANAGEMENT SYSTEM DEMO")
        print("="*40)
        
        # Create groups
        self.create_group("Beginner")
        self.create_group("Intermediate")
        
        # Add students
        self.add_student("S001", "Alice", "Johnson", "Beginner")
        self.add_student("S002", "Bob", "Smith", "Beginner")
        self.add_student("S003", "Charlie", "Brown", "Intermediate")
        self.add_student("S004", "Diana", "Wilson", "Intermediate")
        
        # Assign tracks
        self.assign_track_to_group("Beginner", 1)
        self.assign_track_to_group("Intermediate", 3)
        
        # Start rounds
        self.start_group_round("Beginner")
        self.start_group_round("Intermediate")
        
        # Display information
        self.display_student_assignment("Beginner")
        self.display_student_assignment("Intermediate")
        
        # Complete some rounds
        self.provide_round_score("Beginner", "S001", 85.5)
        self.provide_round_score("Intermediate", "S003", 92.0)
        
        # Display rounds
        self.display_all_rounds()
        
        # Get next students
        next_beginner = self.get_next_round_student("Beginner")
        next_intermediate = self.get_next_round_student("Intermediate")
        
        if next_beginner:
            print(f"\nNext student in Beginner group: {next_beginner}")
        if next_intermediate:
            print(f"Next student in Intermediate group: {next_intermediate}")
        
        # Final summary
        self.get_system_summary()


# Main execution
if __name__ == "__main__":
    # Create and run the system
    ski_system = SkiManagementSystem()
    ski_system.run_demo()
