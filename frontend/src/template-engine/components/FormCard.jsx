import React from "react";

export function FormCard({ form }) {
  return (
    <article className="flex min-h-[110px] flex-col justify-between rounded border border-line-strong bg-panel p-4">
      <h2 className="truncate text-body font-semibold text-ink-strong">{form.name}</h2>
      <p className="line-clamp-2 text-caption text-subtle">{form.description || "No description"}</p>
    </article>
  );
}
