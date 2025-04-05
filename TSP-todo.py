import mysql.connector as mysql

def connect_db():
    return mysql.connect(host="localhost",  port=3307, user="root", passwd="root", database="TODO")

def initialize_db():
    con = mysql.connect(host="localhost", port=3307, user="root", passwd="root")
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS TODO")
    cursor.execute("USE TODO")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_todo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(50) NOT NULL,
            status ENUM('pending', 'completed') DEFAULT 'pending'
        )
    """)
    con.commit()
    con.close()

def add_task():
    task = input("Enter task: ")
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO tb_todo (task) VALUES (%s)", (task,))
    con.commit()
    con.close()
    print("✅ Task added successfully!")

def view_tasks():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tb_todo")
    tasks = cursor.fetchall()
    con.close()
    if tasks:
        print("\nYour Tasks:")
        for task in tasks:
            print(f"{task[0]}. {task[1]} - {task[2]}")
    else:
        print("No tasks available.")

def update_task():
    view_tasks()
    task_id = input("Enter task ID to update: ")
    new_status = input("Enter new status (pending/completed): ")
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("UPDATE tb_todo SET status = %s WHERE id = %s", (new_status, task_id))
    con.commit()
    con.close()
    print("✅ Task updated successfully!")

def delete_task():
    view_tasks()
    task_id = input("Enter task ID to delete: ")
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM tb_todo WHERE id = %s", (task_id,))
    con.commit()
    con.close()
    print("✅ Task deleted successfully!")

def main():
    initialize_db()
    while True:
        print("\nTask Management")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Exiting Task Management... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

