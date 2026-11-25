# AGENTS.md

Rules for agents working in this repository. Follow them unless the user explicitly overrides them.

## Project

- Django backend in `backend/` (SQLite DB with existing data, API under `/api/`).
- React + Vite frontend in `frontend/`. Branding is ReForm, greyscale palette.
- Styling uses Tailwind CSS v4 through the Vite plugin.
- Do not add backend logic, dependencies, or infrastructure unless asked.

## Styling

- Tailwind is the only styling system. Do not add component CSS files or inline `style` unless Tailwind cannot express the style.
- Define shared design values (colors, font sizes, easing) as tokens in `@theme` in `frontend/src/style.css`, and use the generated utilities in JSX.
- Use the existing ReForm greyscale tokens. Do not introduce new colors or hard-code hex values in components.
- Keep `style.css` limited to the Tailwind import, theme tokens, and base element styles.
- Remove CSS that duplicates or overrides Tailwind utilities; keep one source of truth.

## Keep changes simple

- Make the smallest change that fully satisfies the request.
- Change only what the request touches. Do not reformat, rename, or "clean up" unrelated code.
- Match the existing structure, file layout, naming, and formatting.
- Do not add abstractions for one-off use, config layers, or options nobody asked for.
- Do not add libraries when the platform or existing code already covers it.
- Never commit secrets or modify `backend/db.sqlite3`.

## Remove redundant code

- Delete dead code, unused imports/state/props, duplicate components, and unreachable branches.
- Collapse needless wrappers and pass-through functions.
- Prefer a single line for short `if`s, early returns, and simple evaluations when it stays clear:
  - `if (!user) return null;`
  - `const fullName = first + " " + last;`
- Remove duplicate CSS and `!important` overrides that fight each other; keep one source of truth.
- Do not keep a comment that restates code, and do not keep commented-out code.
- Keep long lines only when splitting them hurts readability.

## Readability is essential

- Names must say what a thing is or does: `handleLogout`, `auth-card`, `isSubmitting`. Avoid `data`, `temp`, `obj`, `handleClick2`, and vague abbreviations.
- Structure code so it reads top to bottom without explanation.
- Comments are a crutch. Fix the code or the name instead of explaining it.
- Only comment non-obvious intent or constraints the code cannot express, and keep it one short line.
- Leave no stale comments; update or delete them with the code.

## Workflow

- Read the relevant files before editing; check for existing user changes and build on them.
- Verify before reporting: `npm run build` in `frontend/`, `.\venv\Scripts\python.exe manage.py test` in `backend/` when the backend changed.
- Do not create markdown files, plans, or notes unless asked.

## Report back

End every task with a short bullet summary, in this order:

- **Steps taken** — what changed, with file paths.
- **Pending decisions/steps** — anything blocked or left for the user; omit if none.
- **Problems** — errors, limitations, or surprises; omit if none.
- **Improvements** — optional, only when a concrete follow-up is worth suggesting.

Keep it to a few bullets. No essays.
