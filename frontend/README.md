# Frontend

The frontend uses React and Vite. Install Node.js 20.19+ or 22.12+, then from
this directory run `npm install`.

For development, start Django from `backend/` with
`.\venv\Scripts\python.exe manage.py runserver`. In another terminal, run
`npm run dev` here and open `http://localhost:5173/`. Vite proxies `/api`
requests to Django at `http://127.0.0.1:8000/`.

Run `npm run build` here to produce a standalone static frontend in `dist/`.
