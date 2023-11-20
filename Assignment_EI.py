# Importing datetime and logging modules
import datetime
import logging

# Configuring the logging level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Defining a class for Task objects
class Task:
    # Using the Builder Pattern for constructing tasks with optional attributes
    def __init__(self, description, due_date=None, tags=None):
        self.description = description
        self.due_date = due_date
        self.tags = tags
        self.completed = False

    # Defining a method for marking tasks as completed
    def mark_completed(self):
        self.completed = True

    # Defining a method for displaying tasks
    def display(self):
        # Formatting the task description and status
        output = f"{self.description} - {'Completed' if self.completed else 'Pending'}"
        # Adding the due date if present
        if self.due_date:
            output += f", Due: {self.due_date.strftime('%Y-%m-%d')}"
        # Adding the tags if present
        if self.tags:
            output += f", Tags: {', '.join(self.tags)}"
        # Returning the output
        return output

# Defining a class for To-Do List Manager
class ToDoListManager:
    # Using the Memento Pattern for allowing undo and redo actions
    # Defining a nested class for Memento objects
    class Memento:
        # Initializing the Memento with a copy of the task list
        def __init__(self, task_list):
            self.task_list = task_list.copy()

    # Initializing the To-Do List Manager with an empty task list and empty undo and redo stacks
    def __init__(self):
        self.task_list = []
        self.undo_stack = []
        self.redo_stack = []

    # Defining a method for adding a new task
    def add_task(self, description, due_date=None, tags=None):
        # Using a try block to execute the code that may raise an exception
        try:
            # Creating a new Task object with the given attributes
            task = Task(description, due_date, tags)
            # Appending the task to the task list
            self.task_list.append(task)
            # Saving the current state to the undo stack
            self.undo_stack.append(self.Memento(self.task_list))
            # Clearing the redo stack
            self.redo_stack.clear()
            # Printing a confirmation message
            print(f"Added task: {task.display()}")
            # Logging the action
            logging.info(f"Added task: {task.display()}")
        # Using an except block to catch the specific exception and handle it 
        except ValueError as e:
            # Print an error message and ask the user to enter a valid date
            print(f"Invalid date: {e}")
            print("Please enter a valid date in the format YYYY-MM-DD")
            # Logging the error
            logging.error(f"Invalid date: {e}")
        # Using a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

    # Define a method for deleting a task
    def delete_task(self, description):
        # Use a try block to execute the code that may raise an exception
        try:
            # Find the task with the matching description in the task list
            task = next((t for t in self.task_list if t.description == description), None)
            # If the task is found, remove it from the task list
            if task:
                self.task_list.remove(task)
                # Save the current state to the undo stack
                self.undo_stack.append(self.Memento(self.task_list))
                # Clear the redo stack
                self.redo_stack.clear()
                # Print a confirmation message
                print(f"Deleted task: {task.display()}")
                # Log the action
                logging.info(f"Deleted task: {task.display()}")
            # If the task is not found, print an error message
            else:
                print(f"No task found with description: {description}")
                # Log the error
                logging.error(f"No task found with description: {description}")
        # Use an except block to catch the specific exception and handle it gracefully
        except Exception as e:
            # Print a generic error message and the exception details
            print(f"An error occurred while deleting the task: {e}")
            # Log the error
            logging.error(f"An error occurred while deleting the task: {e}")
        # Use a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

    # Define a method for marking a task as completed
    def mark_completed(self, description):
        # Using a try block to execute the code that may raise an exception
        try:
            # Finding the task with the matching description in the task list
            task = next((t for t in self.task_list if t.description == description), None)
            # If the task is found and not already completed, mark it as completed
            if task and not task.completed:
                task.mark_completed()
                # Save the current state to the undo stack
                self.undo_stack.append(self.Memento(self.task_list))
                # Clear the redo stack
                self.redo_stack.clear()
                # Printing a confirmation message
                print(f"Marked task as completed: {task.display()}")
                # Logging the action
                logging.info(f"Marked task as completed: {task.display()}")
            # If the task is not found or already completed, print an error message
            else:
                print(f"No pending task found with description: {description}")
                # Log the error
                logging.error(f"No pending task found with description: {description}")
        # Use an except block to catch the specific exception and handle it 
        except Exception as e:
            # Print a generic error message and the exception details
            print(f"An error occurred while marking the task as completed: {e}")
            # Log the error
            logging.error(f"An error occurred while marking the task as completed: {e}")
        # Use a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

    # Define a method for viewing tasks
    def view_tasks(self, filter=None):
        # Use a try block to execute the code that may raise an exception
        try:
            # If no filter is specified, display all tasks
            if filter is None:
                print("All tasks:")
                for task in self.task_list:
                    print(task.display())
            # If filter is 'completed', display only completed tasks
            elif filter == 'completed':
                print("Completed tasks:")
                for task in self.task_list:
                    if task.completed:
                        print(task.display())
            # If filter is 'pending', display only pending tasks
            elif filter == 'pending':
                print("Pending tasks:")
                for task in self.task_list:
                    if not task.completed:
                        print(task.display())
            # If filter is invalid, print an error message
            else:
                print(f"Invalid filter: {filter}")
                # Log the error
                logging.error(f"Invalid filter: {filter}")
        # Use an except block to catch the specific exception and handle it 
        except Exception as e:
            # Print a generic error message and the exception details
            print(f"An error occurred while viewing the tasks: {e}")
            # Log the error
            logging.error(f"An error occurred while viewing the tasks: {e}")
        # Use a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

    # Define a method for undoing the last action
    def undo(self):
        # Use a try block to execute the code that may raise an exception
        try:
            # If the undo stack is not empty, pop the last state and restore it to the task list
            if self.undo_stack:
                memento = self.undo_stack.pop()
                self.task_list = memento.task_list
                # Save the current state to the redo stack
                self.redo_stack.append(self.Memento(self.task_list))
                # Print a confirmation message
                print("Undid the last action. Tasks at present:")
                ToDoListManager.view_tasks(self)
                # Log the action
                logging.info("Undid the last action")
            # If the undo stack is empty, print an error message
            else:
                print("No actions to undo")
                # Log the error
                logging.error("No actions to undo")
        # Use an except block to catch the specific exception and handle it gracefully
        except Exception as e:
            # Print a generic error message and the exception details
            print(f"An error occurred while undoing the last action: {e}")
            # Log the error
            logging.error(f"An error occurred while undoing the last action: {e}")
        # Use a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

    # Define a method for redoing the last undone action
    def redo(self):
        # Use a try block to execute the code that may raise an exception
        try:
            # If the redo stack is not empty, pop the last state and restore it to the task list
            if self.redo_stack:
                memento = self.redo_stack.pop()
                self.task_list = memento.task_list
                # Save the current state to the undo stack
                self.undo_stack.append(self.Memento(self.task_list))
                # Print a confirmation message
                print("Redid the last action. Tasks at present:")
                ToDoListManager.view_tasks(self)
                # Log the action
                logging.info("Redid the last action")

            # If the undo stack is empty, print an error message
            else:
                print("No actions to redo")
                # Log the error
                logging.error("No actions to redo")

        # Use an except block to catch the specific exception and handle it gracefully
        except Exception as e:
            # Print a generic error message and the exception details
            print(f"An error occurred while redoing the last action: {e}")
            # Log the error
            logging.error(f"An error occurred while redoing the last action: {e}")
        # Use a finally block to perform any cleanup actions
        finally:
            # No cleanup actions required for this method
            pass

# Create an instance of To-Do List Manager
todo = ToDoListManager()

# Add some tasks
todo.add_task("Buy groceries", datetime.date(2023, 9, 20))
todo.add_task("Pay bills", datetime.date(2023, 9, 25), ["finance", "urgent"])
todo.add_task("Complete Assignment",datetime.date(2023,9,22),["urgent"])
todo.add_task("Attend Vishal's party",datetime.date(2023,10,21),["Leisure"])
todo.add_task("Read a book",datetime.date(2023,10,21))

# View all tasks
todo.view_tasks()

# Mark a task as completed
todo.mark_completed("Buy groceries")

# View completed tasks
#todo.view_tasks("completed")
todo.view_tasks("completed")

# Delete a task
todo.delete_task("Read a book")
todo.undo()
todo.delete_task("Attend Vishal's party")
todo.delete_task("Attend Vishal's party")

# Undoing the last action
todo.undo() # "Attend Vishal's party" task would come back into the tasks list.
todo.undo() # "Read a book" task would come back into the tasks list.

# Redoing the last undone action
todo.redo() # returns the same as no new actions have been performed

