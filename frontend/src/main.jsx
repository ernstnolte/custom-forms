import React from "react";
import { createRoot } from "react-dom/client";
import { Navbar } from "./template-engine";
import "./style.css";

function App() {
  return (
    <>
      <Navbar />
      <main className="top-section">
        <div className="card">
          <h2>Managers Breakdown Checklist</h2>
          <p>John Doe</p>
        </div>
        <div className="card">
          <h2>Shop Safety Checklist</h2>
          <p>Jane Smith</p>
        </div>
      </main>
    </>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
