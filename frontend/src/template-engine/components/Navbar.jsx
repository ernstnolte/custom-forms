import React from "react";
import { Link } from "react-router-dom";

export function Navbar() {
  const [user, setUser] = React.useState(undefined);
  const [error, setError] = React.useState("");
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);
  const menuRef = React.useRef(null);

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

  React.useEffect(() => {
    if (!isMenuOpen) return;

    function handlePointerDown(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) setIsMenuOpen(false);
    }

    function handleKeyDown(event) {
      if (event.key === "Escape") setIsMenuOpen(false);
    }

    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isMenuOpen]);

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
      setIsMenuOpen(false);
    } catch {
      setError("Could not log out. Please try again.");
    }
  }

  return (
    <header className="flex flex-none items-center justify-between gap-4 border-b border-line bg-footer px-6 py-2.5">
      <Link className="text-title font-bold tracking-[0.02em] text-ink-strong hover:text-ink-strong" to="/home">
        ReForm
      </Link>
      <nav className="flex items-center gap-5 text-nav" aria-label="Main navigation">
        {user === undefined ? null : user ? (
          <div className="relative" ref={menuRef}>
            <button
              type="button"
              aria-label="Account menu"
              aria-haspopup="menu"
              aria-expanded={isMenuOpen}
              onClick={() => setIsMenuOpen((open) => !open)}
              className="flex h-9 w-9 cursor-pointer items-center justify-center rounded-full border border-line-strong bg-panel text-ink-strong transition-colors duration-150 ease-standard hover:border-focus hover:bg-panel-header focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus"
            >
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <circle cx="12" cy="8" r="4" />
                <path strokeLinecap="round" d="M4 21c0-4 3.6-7 8-7s8 3 8 7" />
              </svg>
            </button>

            {isMenuOpen && (
              <div
                role="menu"
                className="absolute right-0 top-full z-20 mt-2 w-48 overflow-hidden rounded border border-line-strong bg-panel shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
              >
                <Link
                  role="menuitem"
                  to="/account"
                  className="block px-4 py-2 text-nav text-link hover:bg-panel-header hover:text-ink-strong"
                >
                  Account settings
                </Link>
                <Link
                  role="menuitem"
                  to="/home"
                  className="block px-4 py-2 text-nav text-link hover:bg-panel-header hover:text-ink-strong"
                >
                  Forms
                </Link>
                <button
                  type="button"
                  role="menuitem"
                  onClick={handleLogout}
                  className="block w-full cursor-pointer border-0 bg-transparent px-4 py-2 text-left text-nav text-link hover:bg-panel-header hover:text-ink-strong"
                >
                  Log out
                </button>
              </div>
            )}
          </div>
        ) : (
          <>
            <Link className="text-link hover:text-ink-strong hover:underline" to="/login">
              Log in
            </Link>
            <Link className="text-link hover:text-ink-strong hover:underline" to="/">
              Sign up
            </Link>
          </>
        )}
      </nav>
      {error && (
        <p className="text-caption text-error" role="status">
          {error}
        </p>
      )}
    </header>
  );
}
