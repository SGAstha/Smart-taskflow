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

## Run locally

### 1. Install Python

Use Python 3.10 or newer.

### 2. Open the project folder

```bash
cd smart-taskflow
```

### 3. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The SQLite database and tables are created automatically the first time the app runs.

## Push to GitHub

Create an empty repository on GitHub named `smart-taskflow`. Then run these commands in the project directory:

```bash
git init
git add .
git commit -m "Build Smart TaskFlow task management app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/smart-taskflow.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not commit passwords, API keys, `.env` files, or the local database.

## Deployment notes

This app includes a `Procfile` for a compatible Python hosting service.

1. Push the project to GitHub.
2. Create a new **Web Service** on your chosen Python hosting provider and connect the repository.
3. Set the build/install command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app` (install `gunicorn` by adding it to `requirements.txt` if your provider requires it; see note below).
5. Set an environment variable named `SECRET_KEY` to a long random value.
6. Deploy and open the public URL.

**Important database note:** SQLite is suitable for a local demo and small portfolio project. On many hosted platforms, local filesystems may be temporary or reset during redeployments. For durable production deployment, use a managed persistent disk or migrate to a hosted database such as PostgreSQL. Also add `gunicorn` to `requirements.txt` for production deployment.

## Security and production improvements

This is a portfolio project, not a production-hardened service. Before real-world use, add CSRF protection, rate limiting, secure cookie settings appropriate to HTTPS, stronger input validation, and a persistent production database. Set a unique `SECRET_KEY` in the deployment environment.

## Ideas for future enhancements

- Drag-and-drop Kanban board
- Email or browser notifications for deadlines
- Export tasks to CSV
- Recurring tasks
- Team workspaces and shared projects
- Dark mode
- Unit and integration tests

## Screenshots

Add screenshots after running the app:

```text
screenshots/
├── landing-page.png
└── dashboard.png
```

Then embed them here with Markdown, for example:

```markdown
![Smart TaskFlow dashboard](screenshots/dashboard.png)
```

## Author

**Your Name**  
GitHub: `https://github.com/YOUR-USERNAME`

---

Built as a web development portfolio project to practice frontend design, Flask routing, authentication, CRUD operations, SQL, and data visualization.
