---
name: lead-capture-form
category: cta
dial_compatibility:
  variance: [2, 7]
  motion: [1, 5]
  density: [2, 5]
when_to_use: "The email capture on a landing page - lead magnet, enquiry, waitlist. Handles the four states a real form has, guards double-submit and replay, and stays accessible while doing it."
not_for: "Multi-step or conditional forms. Checkout. Anything needing file upload or payment. Login - an auth form has different security requirements entirely."
stack: ["react", "next", "tailwind"]
harvested_from: ["arianademers-site/src/components/LeadForm.tsx", "colinrigney-site/components/LeadForm.tsx"]
---

# Lead Capture Form

Name, email, optional message. The interesting part is everything that is not the fields.

Both harvest sources independently define the **same status union** and independently arrived at
the **same replay defence**, each documenting it in a comment. That agreement is why those two
things are in this block and the styling is not.

## 1. Visual sketch

```
  idle                        submitting              success
┌────────────────────┐      ┌────────────────────┐  ┌────────────────────┐
│ Name               │      │ Name      (dim)    │  │  ✓  You're in.     │
│ [________________] │      │ [_______________]  │  │                    │
│ Email              │  ->  │ Email     (dim)    │  │  What happens next │
│ [________________] │      │ [_______________]  │  │  in one sentence.  │
│ Message (optional) │      │                    │  │                    │
│ [________________] │      │ [  Sending…    ]   │  └────────────────────┘
│ [   Send   ]       │      │                    │   the form is REPLACED,
└────────────────────┘      └────────────────────┘   not left sitting there
```

## 2. Props API

```ts
type Status = "idle" | "submitting" | "success" | "error";   // both sources, verbatim

type LeadCaptureFormProps = {
  nonce: string;                 // per-request, from the server. see section 3.
  endpoint?: string;             // default "/api/lead"
  fields?: ("name" | "email" | "message")[];   // default all three
  submitLabel?: string;
  success?: { heading: string; body: string };
  reassurance?: string;          // "No spam, ever."
};
```

Three fields is the ceiling. Every additional field costs conversion, and a lead magnet needs an
address, not a profile.

## 3. Code sketch

Client island (`"use client"`). The parent stays a Server Component and passes the nonce down.

```tsx
"use client";
import { useEffect, useRef, useState } from "react";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function LeadCaptureForm({ nonce: serverNonce, endpoint = "/api/lead" }) {
  // Defence in depth: prefer a fresh client nonce generated on mount, falling back to the
  // per-request server nonce. Stable for this form instance, so a double-submit collides on
  // the unique nonce and dedups server-side even behind an unexpected cache layer.
  const nonceRef = useRef(serverNonce);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const submittingRef = useRef(false);

  useEffect(() => {
    try { nonceRef.current = crypto.randomUUID(); } catch { /* keep server nonce */ }
  }, []);

  async function onSubmit(e) {
    e.preventDefault();
    if (submittingRef.current) return;          // guard against double-fire
    const data = new FormData(e.currentTarget);
    const name = String(data.get("name") ?? "").trim();
    const email = String(data.get("email") ?? "").trim();

    const next = {};
    if (!name) next.name = "Please enter your name.";
    if (!EMAIL_RE.test(email)) next.email = "Please enter a valid email address.";
    if (Object.keys(next).length) { setFieldErrors(next); setStatus("error"); return; }

    submittingRef.current = true;
    setStatus("submitting");
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15_000);
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, nonce: nonceRef.current }),
        signal: controller.signal,
      });
      if (res.status === 429) { setStatus("error"); setError("Too many attempts. Try again shortly."); return; }
      if (!res.ok) { setStatus("error"); setError("Something went wrong. Please try again."); return; }
      setStatus("success");
    } catch {
      setStatus("error");
      setError("Network problem. Please try again.");
    } finally {
      clearTimeout(timeout);
      submittingRef.current = false;
    }
  }

  if (status === "success") {
    return (
      <div role="status" className="rounded-[--radius] border border-line p-6">
        <p className="font-semibold">You&apos;re in.</p>
        <p className="mt-2 text-muted">Check your inbox. The guide is on its way.</p>
      </div>
    );
  }

  const busy = status === "submitting";
  return (
    <form onSubmit={onSubmit} noValidate className="flex flex-col gap-5">
      {/* fields, each disabled={busy}, autoComplete set, aria-invalid + aria-describedby on error */}
      {status === "error" && error && (
        <p role="alert" className="text-[0.9rem] text-danger">{error}</p>
      )}
      <button type="submit" disabled={busy} className="...">
        {busy ? "Sending…" : "Send"}
      </button>
    </form>
  );
}
```

**Three things here are not styling decisions and must be copied:**

1. **The nonce.** A per-request server nonce, replaced on mount by a fresh client one, held in a
   ref so it is stable for the form's life. A double-submit then collides on the same unique value
   and the server dedups. Both sources do this and both explain it in a comment.
2. **`noValidate` + explicit client validation.** The browser's native bubbles cannot be styled,
   are inconsistent across engines, and are not announced reliably. Turning them off means you owe
   the user real messages — which is the point.
3. **`role="status"` on success and `role="alert"` on error.** Without these a screen-reader user
   submits the form and hears nothing at all.

The 15-second `AbortController` timeout matters more than it looks: without it a hung request
leaves the form disabled forever with no way back.

## 4. Mobile fallback (`< 768px`)

- Fields go full width, stacked, `gap-5`. Never side-by-side name/email at 375px.
- Inputs need `text-[16px]` minimum — **iOS Safari zooms the viewport on focus for anything
  smaller**, which yanks the layout sideways and is one of the commonest mobile form bugs.
- Tap targets: `py-3` minimum on inputs, and a full-width submit button.
- Keep `autoComplete` set (`name`, `email`) — on mobile this is the difference between one tap and
  thirty keystrokes.
- `inputMode="email"` on the email field so the keyboard shows `@`.
- The success panel must occupy roughly the form's height, or the page jumps on submit.

## 5. Motion variants

| MOTION_INTENSITY | Behaviour |
|---|---|
| 1-3 | No motion. State changes are instant. |
| 4-7 | Cross-fade between form and success panel (~200ms). Button label swaps to "Sending…" with a subtle opacity change. |
| 8-10 | As 4-7. **Do not** animate field borders on focus beyond a colour change, and never animate field height — a shifting form is a form people abandon. |

Reduced motion: instant swaps. A success message that fades in over 400ms is a success message a
reduced-motion user may not register at all.

## 6. Dark-mode notes

Forms are where dark mode most often breaks, and the pre-flight checklist has a box for exactly
this. Every one of these needs a value in **both** modes:

- input background against the card surface (they must be distinguishable — an input that matches
  its container does not read as a field)
- input border, and the **focus** border, which must be visible against both
- placeholder text — the single most common WCAG AA failure in a form
- disabled state (`disabled:opacity-60` reads fine on light and can vanish on dark)
- the error colour, which must clear AA on both surfaces — a red tuned for white is often
  unreadable on dark

One source floats the form on `bg-white/60`, which only works because it sits on a pinned dark
band. If you lift that pattern onto a themed surface, replace the translucency with a real token.

## 7. Anti-patterns

- **No double-submit guard.** A ref checked synchronously, not a state check — state updates are
  async and a fast double-click races them.
- **No replay/dedup key.** Without the nonce, a retry or a double-fire creates two leads.
- **Leaving the form on screen after success.** Replace it. A still-filled form invites a resubmit.
- **Native validation bubbles** (`required` without `noValidate`). Unstyleable, inconsistent,
  poorly announced.
- **No `role="alert"` / `role="status"`.** Silent failure for screen-reader users.
- **Inputs below 16px on mobile.** iOS zooms. See section 4.
- **A generic "Something went wrong"** for every failure. Distinguish at minimum: validation
  (fix the field), 429 (wait), network (retry). One source handles 429 explicitly.
- **No timeout.** A hung fetch disables the form permanently.
- **Placeholder text instead of a label.** The label disappears the moment typing starts, and
  placeholder-only fields fail accessibility outright.
- **More than three fields** on a lead magnet.
- **No reassurance line.** "No spam, ever." next to the button removes the main objection.
- **Clearing what the user typed on a failed submit.** Punishing a typo by wiping the form is how
  you lose the lead you already earned.

## 8. References

- `arianademers-site/src/components/LeadForm.tsx` — controlled inputs, single error message,
  `AbortController` with a 15s timeout, JSON error-body parsing with a non-JSON fallback.
- `colinrigney-site/components/LeadForm.tsx` — uncontrolled via `FormData`, per-field errors, a
  shared `Field` subcomponent, explicit `EMAIL_RE`, explicit 429 handling, `submittingRef` guard.

Independently agreed: the `Status` union verbatim, the server-nonce → client-nonce defence with
the same reasoning in a comment, `noValidate` with hand-rolled validation, `disabled` on every
field while submitting, `autoComplete` on name and email, `role="status"` / `role="alert"`,
`POST /api/lead`, and replacing the form entirely on success.
