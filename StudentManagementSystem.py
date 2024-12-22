
import sys

class StudentRecord:

    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}"

    def __eq__(self, other):
        if isinstance(other, StudentRecord):
            return self.student_id == other.student_id
        return False

    def __lt__(self, other):
        if isinstance(other, StudentRecord):
            return self.student_id < other.student_id
        return False

    def __gt__(self, other):
        if isinstance(other, StudentRecord):
            return self.student_id > other.student_id
        return False


class TreeNode:
    """Class representing a node in the Binary Search Tree."""

    def __init__(self, record: StudentRecord):
        self.record = record
        self.left = None
        self.right = None


class StudentBST:
    """Binary Search Tree class to manage student records efficiently."""

    def __init__(self):
        self.root = None

    def add_student(self, record: StudentRecord):
        if not isinstance(record, StudentRecord):
            raise ValueError("Expected a StudentRecord instance.")
        if self.root is None:
            self.root = TreeNode(record)
        else:
            self._insert(self.root, record)
        print(f"Student record with ID {record.student_id} added successfully.")

    def _insert(self, node: TreeNode, record: StudentRecord):
        if record == node.record:
            print("Student ID already exists. Not added.")
            return
        if record < node.record:
            if node.left is None:
                node.left = TreeNode(record)
            else:
                self._insert(node.left, record)
        else:
            if node.right is None:
                node.right = TreeNode(record)
            else:
                self._insert(node.right, record)

    def search_student(self, student_id=None, name=None):
        if student_id is not None:
            return self._search_by_id(self.root, student_id)
        elif name is not None:
            return self._search_by_name(self.root, name)
        return None

    def _search_by_id(self, node: TreeNode, student_id: int):
        if node is None:
            return None
        if node.record.student_id == student_id:
            return node.record
        elif student_id < node.record.student_id:
            return self._search_by_id(node.left, student_id)
        else:
            return self._search_by_id(node.right, student_id)

    def _search_by_name(self, node: TreeNode, name: str):
        if node is None:
            return None
        if node.record.name.lower() == name.lower():
            return node.record
        left_result = self._search_by_name(node.left, name)
        if left_result:
            return left_result
        return self._search_by_name(node.right, name)

    def update_student(self, student_id: int):
        record = self.search_student(student_id=student_id)
        if record:
            new_age = input("Enter new Age (or press Enter to skip): ")
            new_grade = input("Enter new Grade (or press Enter to skip): ")

            if new_age:
                try:
                    record.age = int(new_age)
                except ValueError:
                    print("Invalid age input. Age not updated.")
                    return

            if new_grade:
                record.grade = new_grade

            print("Student record updated successfully.")
        else:
            print(f"Student Record with ID {student_id} not found.")

    def display_all_records(self):
        if self.root is None:
            print("No student records to display.")
            return
        print("Displaying all student records:")
        self._in_order_traversal(self.root)

    def _in_order_traversal(self, node: TreeNode):
        if node:
            self._in_order_traversal(node.left)
            print(node.record)
            self._in_order_traversal(node.right)

    def delete_student(self, student_id: int):
        self.root = self._delete(self.root, student_id)

    def _delete(self, node: TreeNode, student_id: int):
        if node is None:
            print(f"Student with ID {student_id} not found.")
            return node
        if student_id < node.record.student_id:
            node.left = self._delete(node.left, student_id)
        elif student_id > node.record.student_id:
            node.right = self._delete(node.right, student_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                min_larger_node = self._min_value_node(node.right)
                node.record = min_larger_node.record
                node.right = self._delete(node.right, min_larger_node.record.student_id)
        return node

    def _min_value_node(self, node: TreeNode):
        current = node
        while current.left is not None:
            current = current.left
        return current

def login():
    username = "admin"
    password = "password"

    for _ in range(3):  # Allow up to 3 attempts
        user_input = input("Enter username: ")
        pass_input = input("Enter password: ")

        if user_input == username and pass_input == password:
            print("Login successful.")
            return True
        else:
            print("Invalid username or password. Try again.")

    print("Too many failed attempts. Exiting.")
    return False

def main():
    if not login():
        sys.exit(1)

    bst = StudentBST()
    menu_options = {
        "1": "Add Student Record",
        "2": "Search Student Record",
        "3": "Display All Records",
        "4": "Exit"
    }

    while True:
        print("\nStudent Records Management System")
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                student_id = int(input("Enter Student ID: "))
                name = input("Enter Student Name: ")
                age = int(input("Enter Age: "))
                grade = input("Enter Grade: ")
                record = StudentRecord(student_id, name, age, grade)
                bst.add_student(record)

                while True:
                    next_action = input("Continue with main menu or exit? (main menu/exit): ").lower()
                    if next_action == "main menu":
                        break
                    elif next_action == "exit":
                        print("Exiting the system.")
                        sys.exit(0) 
                    else:
                        print("Invalid input. Please enter 'main menu' or 'exit'.")

            elif choice == '2':
                while True:
                    search_type = input("Search by ID or Name? (id/name): ").strip().lower()
                    if search_type == 'id':
                        student_id = int(input("Enter Student ID to search: "))
                        record = bst.search_student(student_id=student_id)
                    elif search_type == 'name':
                        name = input("Enter Student Name to search: ")
                        record = bst.search_student(name=name)
                    else:
                        print("Invalid search type. Try again.")
                        continue

                    if record:
                        print("Student Record Found:", record)
                        action = input("Would you like to Update or Delete the record? (update/delete): ").strip().lower()
                        if action == "update":
                            bst.update_student(record.student_id)
                            break
                        elif action == "delete":
                            bst.delete_student(record.student_id)
                            print("Student Record Delete Successfully")
                            break
                        else:
                            print("Invalid choice. Try again.")
                    else:
                        print("Student record not found.")
                        cont = input("Would you like to continue searching? (y/n): ").strip().lower()
                        if cont == 'n':
                            break

            elif choice == '3':
                bst.display_all_records()
                while True:
                    next_action = input("Continue with main menu or exit? (main menu/exit): ").lower()
                    if next_action == "main menu":
                        break
                    elif next_action == "exit":
                        print("Exiting the system.")
                        sys.exit(0)
                    else:
                        print("Invalid input. Please enter 'main menu' or 'exit'.")

            elif choice == '4':
                print("Exiting the system.")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Input error: {e}. Please enter valid data.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occured: {e}")