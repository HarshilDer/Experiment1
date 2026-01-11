import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def show_tasks(tasks):
    if not tasks:
        print("\n--- No tasks found! ---")
        return
    print("\n--- Your Task List ---")
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{index}. {task['title']} [{status}]")


def main():
    tasks = load_tasks()

    while True:
        print("\n1. View Tasks | 2. Add Task | 3. Complete Task | 4. Delete Task | 5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            title = input("Enter task title: ")
            tasks.append({"title": title, "done": False})
            save_tasks(tasks)
            print("Task added!")

        elif choice == "3":
            show_tasks(tasks)
            idx = int(input("Enter task number to mark complete: ")) - 1
            if 0 <= idx < len(tasks):
                tasks[idx]["done"] = True
                save_tasks(tasks)
                print("Task updated!")

        elif choice == "4":
            show_tasks(tasks)
            idx = int(input("Enter task number to delete: ")) - 1
            if 0 <= idx < len(tasks):
                tasks.pop(idx)
                save_tasks(tasks)
                print("Task deleted!")

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()