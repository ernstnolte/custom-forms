import React from "react";
import { createRoot } from "react-dom/client";
import { Navbar } from "./template-engine";
import App from "./App";
import "./style.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <App />
    </div>
  </React.StrictMode>,
);
