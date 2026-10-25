# Smart TaskFlow

A responsive full-stack task management and productivity dashboard built with **HTML, CSS, JavaScript, Python Flask, and SQLite**.

Smart TaskFlow helps users organize their work, prioritize tasks, manage deadlines, and view a snapshot of their productivity.

## Features

- User registration and login with hashed passwords
- Private tasks for each user
- Create, edit, update, search, filter, and delete tasks
- Priority levels: Low, Medium, High
- Status tracking: Pending, In Progress, Completed
- Due dates and overdue task indicators
- Dashboard summary cards and charts
- Responsive layout for desktop, tablet, and mobile
- SQLite database initialized automatically
- Flash messages for clear user feedback

## Tech stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Charts:** Chart.js (loaded from CDN)
- **Authentication:** Werkzeug password hashing and Flask sessions

## Project structure

```text
smart-taskflow/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── 404.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Ideas for future enhancements

- Drag-and-drop Kanban board
- Email or browser notifications for deadlines
- Export tasks to CSV
- Recurring tasks
- Team workspaces and shared projects
- Dark mode
- Unit and integration tests

