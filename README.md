# zeus

> AI app builder that generates a *runnable* Next.js app from a prompt — not a toy demo but a real scaffolded codebase with auth, database, deploy configs. Claim the name, watch this space.

![status](https://img.shields.io/badge/status-active_planning-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![backlog](https://img.shields.io/badge/backlog-see_DESIGN.md-orange)

## What this is

v0.dev, Bolt, Lovable generate beautiful UIs but often miss production concerns — auth, migrations, environment configs, deploy pipelines. They optimize for demo wow, not for 'I can run this in staging tomorrow.'

**Read the full [DESIGN.md](./DESIGN.md)** for problem statement, user personas, architecture, and roadmap.

## Status

**Active planning / pre-alpha.** The design is scoped (see DESIGN.md). Code is minimal — this repo is the home for the first real implementation, not a placeholder.

## MVP (v0.1) — what ships first

- CLI: `zeus new <prompt>` generates a runnable Next.js app in a new directory
- Includes: Tailwind, Supabase auth, one example protected route, seed data, deploy.yml
- Playwright smoke test that verifies auth flow works
- Generates README with local-dev instructions

## Stack

- Python generator core (Claude-powered)
- Templates: Next.js, FastAPI, Supabase, Clerk, Stripe, Resend
- Playwright for smoke-test generation
- Vercel/Railway/Fly deploy configs
- CLI in Python, optional web UI for non-CLI users

See [DESIGN.md](./DESIGN.md#planned-stack) for complete stack rationale.

## Quick start

```bash
git clone https://github.com/MukundaKatta/zeus.git
cd zeus
# See DESIGN.md for full architecture
```


## Roadmap

| Version | Focus |
|---------|-------|
| v0.1 | MVP — see checklist in [DESIGN.md](./DESIGN.md) |
| v0.2 | Patch mode — add features to existing repos |
| v0.3 | Multi-framework (Remix, Astro, SvelteKit) |

Full roadmap in [DESIGN.md](./DESIGN.md#roadmap).

## Contributing

Open an issue if:
- You'd use this tool and have a specific use case not covered
- You spot a design flaw in DESIGN.md
- You want to claim one of the v0.1 checklist items

## See also

- [My other projects](https://github.com/MukundaKatta)
- [mukunda.dev](https://mukunda-ai.vercel.app)
