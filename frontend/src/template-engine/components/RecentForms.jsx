import React from "react";
import { FormCard } from "./FormCard";

export function RecentForms({ forms }) {
  const recentForms = [...forms]
    .sort((first, second) => {
      const firstDate = new Date(first.creation_date).getTime();
      const secondDate = new Date(second.creation_date).getTime();
      if (Number.isNaN(firstDate) || Number.isNaN(secondDate)) return second.id - first.id;
      return secondDate - firstDate;
    })
    .slice(0, 3);

  return (
    <section aria-label="Recent forms" className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <button
        type="button"
        aria-label="Create new form"
        onClick={() => window.alert("Creating forms is not implemented yet.")}
        className="flex min-h-[110px] cursor-pointer items-center justify-center rounded border border-dashed border-line-strong bg-panel text-ink-strong transition-colors duration-150 ease-standard hover:border-focus hover:bg-panel-header focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus"
      >
        <svg className="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" d="M12 5v14M5 12h14" />
        </svg>
      </button>

      {recentForms.map((form) => (
        <FormCard key={form.id} form={form} />
      ))}
    </section>
  );
}
