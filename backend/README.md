# Backend

The Django project, SQLite database, and Python environment live here. From
this directory, create the environment and install dependencies with:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use the environment's Python directly to run the backend:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
.\venv\Scripts\python.exe manage.py test
```

The API is available under `/api/`; the React frontend is served separately by
Vite from `frontend/`.

Configure backend deployments to use `backend/` as their project root so they
can find `manage.py`, `requirements.txt`, and `runtime.txt`.
