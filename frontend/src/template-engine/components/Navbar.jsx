import React from "react";

export function Navbar() {
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
    <header className="flex flex-none items-center justify-between gap-4 border-b border-line bg-footer px-6 py-2.5">
      <a className="text-title font-bold tracking-[0.02em] text-ink-strong hover:text-white" href="/">
        ReForm
      </a>
      <nav className="flex items-center gap-5 text-nav" aria-label="Main navigation">
        {user === undefined ? null : user ? (
          <>
            <span className="text-subtle">Hi, {user.username}</span>
            <button
              className="cursor-pointer border-0 bg-transparent p-0 text-link hover:text-white hover:underline"
              onClick={handleLogout}
              type="button"
            >
              Log out
            </button>
          </>
        ) : (
          <>
            <a className="text-link hover:text-white hover:underline" href="/login">
              Log in
            </a>
            <a className="text-link hover:text-white hover:underline" href="/signup">
              Sign up
            </a>
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
