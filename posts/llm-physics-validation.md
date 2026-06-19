---
title: Teaching an LLM not to float objects in mid-air
date: 2026-03-08
read: ~9 min
summary: A small grammar of 3D world predicates, a physics-validation layer, and the surprisingly hard question of what "on top of" actually means. Notes from building Plumb.
---

> Replace this body with the real post.

## Predicates over prose

Instead of asking the model to "place it nicely," I gave it a grammar of
predicates — `on(a, b)`, `inside(a, b)`, `clear(a)` — and validated them
against the scene.

## What "on top of" actually means

Contact, support, and overlap are three different things, and the model
conflates them constantly.
