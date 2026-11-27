import React, { useState, useEffect } from "react";
import { Navbar } from "./template-engine/components/Navbar";
import { RecentForms } from "./template-engine/components/RecentForms";
import { FormsTable } from "./template-engine/components/FormsTable";

function App() {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    fetch("/api/forms")
      .then((response) => {
        if (!response.ok) throw new Error("Could not load forms.");
        return response.json();
      })
      .then(({ data: formsData }) => {
        if (active) setForms(Array.isArray(formsData) ? formsData : []);
      })
      .catch(() => {
        if (active) setError("Could not load forms.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col bg-page">
        <Navbar />
        <main className="flex flex-1 items-center justify-center p-6 text-caption text-subtle">Loading...</main>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-page">
      <Navbar />

      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-6 p-6">
        {error && (
          <p className="text-caption text-error" role="alert">
            {error}
          </p>
        )}

        <RecentForms forms={forms} />
        <FormsTable forms={forms} />
      </main>
    </div>
  );
}

export default App;
