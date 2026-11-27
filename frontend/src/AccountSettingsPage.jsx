import React from "react";
import { Navbar } from "./template-engine/components/Navbar";

export default function AccountSettingsPage() {
  return (
    <div className="flex min-h-screen flex-col bg-page">
      <Navbar />

      <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-6 p-6">
        <h1 className="text-title font-bold tracking-[0.02em] text-ink-strong">Account settings</h1>

        <section className="overflow-hidden rounded border border-line-strong bg-panel">
          <div className="border-b border-line-strong bg-panel-header px-5 py-3 text-body font-semibold text-ink-strong">
            Profile
          </div>
          <div className="space-y-4 p-5">
            <div>
              <p className="text-caption font-semibold text-muted">Username</p>
              <p className="text-body text-ink">Not set</p>
            </div>
            <div>
              <p className="text-caption font-semibold text-muted">Email</p>
              <p className="text-body text-ink">Not set</p>
            </div>
            <p className="text-caption text-subtle">Account settings are not implemented yet.</p>
          </div>
        </section>
      </main>
    </div>
  );
}
