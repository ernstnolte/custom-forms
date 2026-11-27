import React from "react";

const dateFormatter = new Intl.DateTimeFormat(undefined, {
  year: "numeric",
  month: "short",
  day: "numeric",
});

const iconButtonClass =
  "cursor-pointer rounded border border-line p-1.5 text-link transition-colors duration-150 ease-standard hover:border-line-strong hover:text-ink-strong focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus";

const primaryButtonClass =
  "cursor-pointer rounded-[3px] border border-primary bg-primary px-4 py-2 text-caption font-semibold text-on-primary transition-[background-color,border-color] duration-150 ease-standard hover:border-ink-strong hover:bg-ink-strong focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink-strong";

const secondaryButtonClass =
  "cursor-pointer rounded-[3px] border border-line-strong bg-panel px-4 py-2 text-caption font-semibold text-link transition-colors duration-150 ease-standard hover:border-focus hover:text-ink-strong focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus";

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : dateFormatter.format(date);
}

function ExportIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v12m0 0 4-4m-4 4-4-4M4 17v3h16v-3" />
    </svg>
  );
}

function DeleteIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 7h16M9 7V4h6v3m-8 0 1 13h8l1-13M10 11v5m4-5v5" />
    </svg>
  );
}

function ShareIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
      <circle cx="18" cy="5" r="2.5" />
      <circle cx="6" cy="12" r="2.5" />
      <circle cx="18" cy="19" r="2.5" />
      <path strokeLinecap="round" d="m8.2 10.8 7.6-4.6M8.2 13.2l7.6 4.6" />
    </svg>
  );
}

export function FormsTable({ forms }) {
  const [dialog, setDialog] = React.useState(null);

  return (
    <section className="flex flex-col gap-4" aria-labelledby="forms-title">
      <div className="overflow-x-auto rounded border border-line-strong bg-panel">
        <table className="w-full min-w-[640px] border-collapse text-left text-nav">
          <thead className="bg-panel-header text-caption uppercase tracking-[0.04em] text-muted">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Name
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Date created
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Responses
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {forms.map((form) => (
              <tr key={form.id} className="transition-colors duration-150 ease-standard hover:bg-panel-header/50">
                <td className="px-4 py-3 font-semibold text-ink-strong">{form.name}</td>
                <td className="px-4 py-3 text-subtle">{formatDate(form.creation_date)}</td>
                <td className="px-4 py-3 text-subtle">{form.response_count ?? "—"}</td>
                <td className="px-4 py-3">
                  <div className="flex justify-end gap-1">
                    <button
                      type="button"
                      aria-label={`Export ${form.name}`}
                      title="Export"
                      className={iconButtonClass}
                      onClick={() => setDialog({ type: "export", form })}
                    >
                      <ExportIcon />
                    </button>
                    <button
                      type="button"
                      aria-label={`Delete ${form.name}`}
                      title="Delete"
                      className={iconButtonClass}
                      onClick={() => setDialog({ type: "delete", form })}
                    >
                      <DeleteIcon />
                    </button>
                    <button
                      type="button"
                      aria-label={`Share ${form.name}`}
                      title="Share"
                      className={iconButtonClass}
                      onClick={() => setDialog({ type: "share", form })}
                    >
                      <ShareIcon />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {forms.length === 0 && (
          <p className="px-4 py-8 text-center text-caption text-subtle">No forms created yet.</p>
        )}
      </div>

      {dialog && <FormActionDialog dialog={dialog} onClose={() => setDialog(null)} />}
    </section>
  );
}

function FormActionDialog({ dialog, onClose }) {
  const { type, form } = dialog;

  React.useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === "Escape") onClose();
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  const title =
    type === "export" ? `Export ${form.name}` : type === "delete" ? `Delete ${form.name}` : `Share ${form.name}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-page/80 p-4" onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="form-action-title"
        className="w-full max-w-sm overflow-hidden rounded border border-line-strong bg-panel shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-center justify-between gap-4 border-b border-line-strong bg-panel-header px-5 py-3">
          <h3 id="form-action-title" className="min-w-0 truncate text-body font-semibold text-ink-strong">
            {title}
          </h3>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close dialog"
            className="cursor-pointer border-0 bg-transparent p-0 text-title leading-none text-subtle hover:text-ink-strong"
          >
            &times;
          </button>
        </div>

        <div className="p-5">
          {type === "export" && (
            <>
              <p className="mb-4 text-caption text-subtle">Choose a format. Export is not implemented yet.</p>
              <div className="flex gap-2">
                <button type="button" className={primaryButtonClass} onClick={onClose}>
                  Excel
                </button>
                <button type="button" className={secondaryButtonClass} onClick={onClose}>
                  CSV
                </button>
              </div>
            </>
          )}

          {type === "delete" && (
            <>
              <p className="mb-5 text-caption text-subtle">
                Are you sure you want to delete <strong className="text-ink-strong">{form.name}</strong>? This is a
                preview; the form will not be deleted yet.
              </p>
              <div className="flex justify-end gap-2">
                <button type="button" className={secondaryButtonClass} onClick={onClose}>
                  Cancel
                </button>
                <button type="button" className={primaryButtonClass} onClick={onClose}>
                  Delete
                </button>
              </div>
            </>
          )}

          {type === "share" && (
            <>
              <p className="mb-3 text-caption text-subtle">Anyone with this link can respond to the form.</p>
              <input
                readOnly
                value={`https://reform.example/forms/${form.id}/respond`}
                aria-label="Form response link"
                onFocus={(event) => event.target.select()}
                className="w-full rounded-[3px] border border-line-input bg-input px-3 py-2.5 text-caption text-ink focus:border-focus focus:outline-none"
              />
              <div className="mt-4 flex justify-end">
                <button type="button" className={secondaryButtonClass} onClick={onClose}>
                  Close
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
