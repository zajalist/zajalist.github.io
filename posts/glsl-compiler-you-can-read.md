---
title: Round-tripping GLSL through a compiler you can read
date: 2026-04-12
read: ~14 min
summary: How I built Shaddy's bidirectional Recipe↔GLSL compiler, and why magic comments turned out to be the right abstraction for keeping a visual editor and raw shader code honest with each other.
---

> Replace this body with the real post. Everything below the frontmatter is
> standard Markdown — headings, **bold**, `code`, lists, links, images, and
> fenced code blocks all work.

## The problem

A visual shader editor and hand-written GLSL want to disagree the moment you
edit one of them. The goal was a single source of truth that survives both.

## Magic comments

```glsl
// @recipe noise(scale=4.0)
float n = noise(uv * 4.0);
```

These markers let the compiler walk GLSL back into editor "recipes" without a
full parser.

## What I learned

- Keep the round-trip lossless or don't bother.
- A small, readable IR beats a clever one.
