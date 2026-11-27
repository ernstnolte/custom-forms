import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { Navbar } from "./template-engine/components/Navbar";

const inputClass =
  "w-full rounded-[3px] border border-line-input bg-input px-3 py-2.5 text-ink placeholder:text-placeholder transition-[border-color,box-shadow] duration-150 ease-standard focus:border-focus focus:shadow-[0_0_0_2px_rgba(255,255,255,0.08)] focus:outline-none";

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState("");
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const csrfResponse = await fetch("/api/auth/csrf");
      if (!csrfResponse.ok) throw new Error("Could not prepare login.");
      const { csrfToken } = await csrfResponse.json();

      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ username, password }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Could not log in.");

      navigate("/home");
    } catch (submitError) {
      setError(submitError.message || "Could not log in. Please try again.");
      setIsSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-page">
      <Navbar />

      <main className="flex flex-1 items-center justify-center px-4 py-12">
        <section
          className="w-full max-w-[400px] overflow-hidden rounded border border-line-strong bg-panel shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
          aria-labelledby="login-title"
        >
          <h1
            id="login-title"
            className="border-b border-line-strong bg-panel-header px-6 py-[14px] text-body font-semibold tracking-[0.01em] text-ink-strong"
          >
            Log in
          </h1>

          <form className="p-6" onSubmit={handleSubmit}>
            <div className="mb-[18px]">
              <label htmlFor="username" className="mb-1.5 block text-caption font-semibold text-muted">
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="Enter your username"
                autoComplete="username"
                required
                disabled={isSubmitting}
                className={inputClass}
              />
            </div>

            <div className="mb-[18px]">
              <label htmlFor="password" className="mb-1.5 block text-caption font-semibold text-muted">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter your password"
                autoComplete="current-password"
                required
                disabled={isSubmitting}
                className={inputClass}
              />
            </div>

            {error && (
              <p className="mb-4 text-caption text-error" role="alert">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full cursor-pointer rounded-[3px] border border-primary bg-primary px-4 py-2.5 font-semibold text-on-primary transition-[background-color,border-color] duration-150 ease-standard hover:border-ink-strong hover:bg-ink-strong disabled:cursor-wait disabled:opacity-60 focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink-strong"
            >
              {isSubmitting ? "Logging in..." : "Log in"}
            </button>
          </form>

          <p className="px-6 pb-6 text-center text-note text-subtle">
            Need an account?{" "}
            <Link to="/" className="text-link underline underline-offset-2 hover:text-ink-strong">
              Sign up
            </Link>
          </p>
        </section>
      </main>

      <footer className="border-t border-line bg-footer p-4 text-center text-caption text-faint">
        &copy; 2026 ReForm. All rights reserved.
      </footer>
    </div>
  );
}
