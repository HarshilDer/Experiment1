from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime
import calendar

app = Flask(__name__)
FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


@app.route('/')
def index():
    tasks = load_tasks()

    # --- Calendar Logic ---
    # Get current year and month
    now = datetime.now()
    year = now.year
    month = now.month
    month_name = now.strftime("%B %Y")

    # Get a matrix of the month (list of weeks, where each week is a list of days)
    # 0 represents a day belonging to another month
    cal_matrix = calendar.monthcalendar(year, month)

    # Group tasks by date string "YYYY-MM-DD" for easy lookup in the template
    tasks_by_date = {}
    for task in tasks:
        d = task.get('date')  # e.g. "2023-10-25"
        if d:
            if d not in tasks_by_date:
                tasks_by_date[d] = []
            tasks_by_date[d].append(task)

    return render_template('index.html',
                           tasks=tasks,
                           calendar_matrix=cal_matrix,
                           current_year=year,
                           current_month=month,
                           month_name=month_name,
                           tasks_by_date=tasks_by_date)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    priority = request.form.get('priority')  # High, Medium, Low
    due_date = request.form.get('date')  # YYYY-MM-DD

    if title:
        tasks = load_tasks()
        tasks.append({
            "title": title,
            "done": False,
            "priority": priority,
            "date": due_date
        })
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']  # Toggle status
        save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)