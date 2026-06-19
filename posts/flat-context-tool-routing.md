---
title: Keeping context flat as your tool count grows
date: 2026-02-15
read: ~11 min
summary: A hybrid BM25 + embedding router that loads only 10 of ~80 tool schemas at a time. Why I stopped dumping every tool into the prompt and started treating tools like a search problem.
---

> Replace this body with the real post.

## Tools are a retrieval problem

Eighty tool schemas in the prompt is mostly wasted tokens. Treat the request as
a query and retrieve the ~10 tools that matter.

## BM25 + embeddings

Lexical recall catches exact names; embeddings catch intent. The union beats
either alone.
