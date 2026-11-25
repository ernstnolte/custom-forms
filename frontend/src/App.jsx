import { useState } from 'react'

const inputClass =
  'w-full rounded-[3px] border border-line-input bg-input px-3 py-2.5 text-ink placeholder:text-placeholder transition-[border-color,box-shadow] duration-150 ease-standard focus:border-focus focus:shadow-[0_0_0_2px_rgba(255,255,255,0.08)] focus:outline-none'

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  return (
    <div className="flex flex-1 flex-col">
      <main className="flex flex-1 items-center justify-center px-4 py-12">
        <section
          className="w-full max-w-[400px] overflow-hidden rounded border border-line-strong bg-panel shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
          aria-labelledby="signup-title"
        >
          <h1
            id="signup-title"
            className="border-b border-line-strong bg-panel-header px-6 py-[14px] text-body font-semibold tracking-[0.01em] text-ink-strong"
          >
            Create an account
          </h1>

          <form className="p-6" onSubmit={(e) => e.preventDefault()}>
            <div className="mb-[18px]">
              <label htmlFor="username" className="mb-1.5 block text-caption font-semibold text-muted">
                Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                autoComplete="username"
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
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                autoComplete="new-password"
                className={inputClass}
              />
            </div>

            <button
              type="submit"
              className="w-full cursor-pointer rounded-[3px] border border-primary bg-primary px-4 py-2.5 font-semibold text-on-primary transition-[background-color,border-color] duration-150 ease-standard hover:border-white hover:bg-white focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            >
              Sign up
            </button>
          </form>

          <p className="px-6 pb-6 text-center text-note text-subtle">
            Already have an account?{' '}
            <a href="/login" className="text-link underline underline-offset-2 hover:text-white">
              Log in
            </a>
          </p>
        </section>
      </main>

      <footer className="border-t border-line bg-footer p-4 text-center text-caption text-faint">
        &copy; 2026 ReForm. All rights reserved.
      </footer>
    </div>
  )
}

export default App
