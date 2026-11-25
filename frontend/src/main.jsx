import React from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function Navbar() {
  const [user, setUser] = React.useState(undefined);
  const [error, setError] = React.useState("");

  React.useEffect(() => {
    let active = true;

    fetch("/api/auth/user")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not load your account.");
        }
        return response.json();
      })
      .then(({ user: currentUser }) => {
        if (active) setUser(currentUser);
      })
      .catch(() => {
        if (active) {
          setError("Account status is unavailable.");
          setUser(null);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  async function handleLogout() {
    setError("");

    try {
      const csrfResponse = await fetch("/api/auth/csrf");
      if (!csrfResponse.ok) throw new Error("Could not prepare logout.");
      const { csrfToken } = await csrfResponse.json();

      const response = await fetch("/api/auth/logout", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      });
      if (!response.ok) throw new Error("Could not log out.");

      setUser(null);
    } catch {
      setError("Could not log out. Please try again.");
    }
  }

  return (
    <header className="site-header">
      <a className="site-brand" href="/">
        ReForm
      </a>
      <nav className="site-nav" aria-label="Main navigation">
        {user === undefined ? null : user ? (
          <>
            <span className="nav-greeting">Hi, {user.username}</span>
            <button className="nav-link" onClick={handleLogout} type="button">
              Log out
            </button>
          </>
        ) : (
          <>
            <a className="nav-link" href="/login">
              Log in
            </a>
            <a className="nav-link" href="/signup">
              Sign up
            </a>
          </>
        )}
      </nav>
      {error && <p className="nav-error" role="status">{error}</p>}
    </header>
  );
}

function App() {
  return (
    <>
      <Navbar />
      <main className="top-section">
        <article className="card">
          <h2>Managers Breakdown Checklist</h2>
          <p>John Doe</p>
        </article>
        <article className="card">
          <h2>Shop Safety Checklist</h2>
          <p>Jane Smith</p>
        </article>
      </main>
    </>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
