import streamlit as st
import sqlite3
import os

st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="centered"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "tasks.db")


def get_connection():
    conn = sqlite3.connect(DATABASE)
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return tasks


def add_task(title, description):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, 'Pending')
        """,
        (title, description)
    )

    conn.commit()
    conn.close()


def complete_task(task_id):
    conn = get_connection()

    conn.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


initialize_database()

st.title("✅ Task Manager")
st.write("Manage your tasks easily.")

st.divider()

# Add Task
st.subheader("Add New Task")

title = st.text_input("Task Title")
description = st.text_area("Description")

if st.button("➕ Add Task", use_container_width=True):

    if title.strip():
        add_task(title.strip(), description.strip())
        st.success("Task added successfully!")
        st.rerun()

    else:
        st.warning("Please enter a task title.")

st.divider()

# Filter
st.subheader("Your Tasks")

filter_option = st.selectbox(
    "Filter tasks",
    ["All", "Pending", "Completed"]
)

tasks = get_tasks()

for task in tasks:

    task_id = task[0]
    task_title = task[1]
    task_description = task[2]
    task_status = task[3]

    if filter_option == "Pending" and task_status != "Pending":
        continue

    if filter_option == "Completed" and task_status != "Completed":
        continue

    with st.container(border=True):

        st.write(f"### {task_title}")

        if task_description:
            st.write(task_description)

        st.write(f"**Status:** {task_status}")

        col1, col2 = st.columns(2)

        with col1:
            if task_status == "Pending":
                if st.button(
                    "✅ Complete",
                    key=f"complete_{task_id}",
                    use_container_width=True
                ):
                    complete_task(task_id)
                    st.rerun()

        with col2:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{task_id}",
                use_container_width=True
            ):
                delete_task(task_id)
                st.rerun()