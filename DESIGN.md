# zeus — Design

> AI app builder that generates a *runnable* Next.js app from a prompt — not a toy demo but a real scaffolded codebase with auth, database, deploy configs. Claim the name, watch this space.

## Problem

v0.dev, Bolt, Lovable generate beautiful UIs but often miss production concerns — auth, migrations, environment configs, deploy pipelines. They optimize for demo wow, not for 'I can run this in staging tomorrow.'

Zeus takes a different bet: generate fewer, less flashy apps, but make each one genuinely production-ready. Full repo with proper project structure, Supabase/NextAuth config, a deploy workflow, seed data, Playwright smoke tests. Open-source the generator; you own the code it produces.

## Primary users

- Solo founders who want an MVP they can continue maintaining
- Dev shops who use AI for scaffolding but hate the cleanup work
- Learners who want to see what 'good' looks like for common patterns

## Use cases

- 'Build a SaaS for X with magic-link auth, Stripe billing, a dashboard, and Postgres' → complete repo
- 'Add Clerk auth to my existing Next.js app' — patch mode
- Download the generator templates to run locally without API dependency
- Regenerate a single route after iterating on the data model

## Planned stack

- Python generator core (Claude-powered)
- Templates: Next.js, FastAPI, Supabase, Clerk, Stripe, Resend
- Playwright for smoke-test generation
- Vercel/Railway/Fly deploy configs
- CLI in Python, optional web UI for non-CLI users

## MVP scope (v0.1)

- [ ] CLI: `zeus new <prompt>` generates a runnable Next.js app in a new directory
- [ ] Includes: Tailwind, Supabase auth, one example protected route, seed data, deploy.yml
- [ ] Playwright smoke test that verifies auth flow works
- [ ] Generates README with local-dev instructions

## Roadmap

- v0.2: Patch mode — add features to existing repos
- v0.3: Multi-framework (Remix, Astro, SvelteKit)
- v0.4: Monorepo generators (web + api + mobile)
- v1.0: Managed hosting + generator-as-a-service

---

_This is a living design document. Status: **concept / active planning**. Follow progress at [github.com/MukundaKatta](https://github.com/MukundaKatta)._
