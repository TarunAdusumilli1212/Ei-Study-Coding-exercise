from datetime import datetime

# Task class encapsulating task data and methods
class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.creation_date = datetime.now()
        self.due_date = due_date if due_date is None or isinstance(due_date, datetime) else datetime.strptime(due_date, '%Y-%m-%d')

    def mark_as_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f", Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else ""
        return f"{self.description} - {status}{due_date_str}"


# Task Builder class using the Builder Pattern
class TaskBuilder:
    def __init__(self):
        self.description = None
        self.due_date = None

    def with_description(self, description):
        self.description = description
        return self

    def with_due_date(self, due_date):
        self.due_date = due_date
        return self

    def build(self):
        return Task(self.description, self.due_date)


# Main class handling user interactions through a menu-driven approach
class ToDoListManager:
    def __init__(self):
        self.tasks = []

    def display_menu(self):
        print("======= To-Do List Manager Menu =======")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Exit")

    def add_task(self):
        # Function to add a new task to the list and verify the correctness of the due date
        description = input("Enter task description: ")
        while True:
            due_date_input = input("Enter due date (YYYY-MM-DD), press Enter if none: ")
            if due_date_input == '':
                due_date = None
                break
            try:
                due_date = datetime.strptime(due_date_input, '%Y-%m-%d')
                if due_date < datetime.now():
                    print("Due date cannot be in the past. Please enter a future date or today's date.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        task = TaskBuilder().with_description(description).with_due_date(due_date).build()
        self.tasks.append(task)
        print("Task added successfully.")

    def mark_completed(self):
        # Function to mark a task as completed
        pending_tasks = [task for task in self.tasks if not task.completed]
        if pending_tasks:
            print("Pending Tasks List:")
            for task in pending_tasks:
                print(task)
    
            while True:
                task_description = input("Enter task description to mark as completed (or type 'exit' to return): ")
                if task_description.lower() == 'exit':
                    print("Exiting mark as completed.")
                    break
    
                for task in self.tasks:
                    if task.description == task_description:
                        task.mark_as_completed()
                        print("Task marked as completed.")
                        return
    
                print("Task not found. Please enter a valid task description or type 'exit' to return.")
        else:
            print("No pending tasks.")


    def delete_task(self):
        # Function to delete a task from the list
        task_description = input("Enter task description to delete: ")
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.description != task_description]
        if len(self.tasks) < initial_length:
            print("Task deleted successfully.")
        else:
            print("Task not found.")

    def view_tasks(self):
        # Function to view tasks based on filter options
        filter_option = input("Choose filter (all/completed/pending): ")
        if filter_option == 'all':
            tasks_to_display = self.tasks
        elif filter_option == 'completed':
            tasks_to_display = [task for task in self.tasks if task.completed]
        elif filter_option == 'pending':
            tasks_to_display = [task for task in self.tasks if not task.completed]
        else:
            print("Invalid filter option.")
            return

        if not tasks_to_display:
            print("No tasks found based on the selected filter.")
        else:
            print(f"======= {filter_option.capitalize()} Tasks =======")
            for task in tasks_to_display:
                print(task)


# Main program execution
if __name__ == "__main__":
    todo_manager = ToDoListManager()

    while True:
        todo_manager.display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            todo_manager.add_task()
        elif choice == '2':
            todo_manager.mark_completed()
        elif choice == '3':
            todo_manager.delete_task()
        elif choice == '4':
            todo_manager.view_tasks()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
