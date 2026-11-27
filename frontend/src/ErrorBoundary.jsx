import React from "react";

const primaryButtonClass =
  "cursor-pointer rounded-[3px] border border-primary bg-primary px-4 py-2 text-caption font-semibold text-on-primary transition-[background-color,border-color] duration-150 ease-standard hover:border-ink-strong hover:bg-ink-strong focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink-strong";

const secondaryButtonClass =
  "cursor-pointer rounded-[3px] border border-line-strong bg-panel px-4 py-2 text-caption font-semibold text-link transition-colors duration-150 ease-standard hover:border-focus hover:text-ink-strong focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus";

export class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Unhandled UI error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-page p-6">
          <section
            className="w-full max-w-[400px] overflow-hidden rounded border border-line-strong bg-panel shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
            role="alert"
          >
            <h1 className="border-b border-line-strong bg-panel-header px-6 py-[14px] text-body font-semibold text-ink-strong">
              Something went wrong
            </h1>
            <div className="p-6">
              <p className="mb-4 text-caption text-subtle">The page hit an unexpected error.</p>
              <div className="flex gap-2">
                <button type="button" className={primaryButtonClass} onClick={() => window.location.reload()}>
                  Reload
                </button>
                <a href="/home" className={secondaryButtonClass}>
                  Go home
                </a>
              </div>
            </div>
          </section>
        </div>
      );
    }

    return this.props.children;
  }
}
