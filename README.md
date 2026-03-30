<div align="center">

<!-- Logo/Banner placeholder -->
<!-- <img src="assets/banner.png" alt="HyperClaw Banner" width="800"> -->

<h1>HyperClaw</h1>

<p>
HyperClaw is a self-referential, self-improving AI agent built on OpenClaw and inspired by HyperAgents. It unifies execution and self-modification into a recursive system that continuously optimizes its architecture and strategies, compounding capability over time by improving its own learning process.
</p>

<p>
<a href="LICENSE.md">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge" alt="License: GPL v3">
</a>
<a href="https://arxiv.org/abs/2603.19461">
  <img src="https://img.shields.io/badge/arXiv-2603.19461-b31b1b.svg?style=for-the-badge&logo=arxiv&logoColor=white" alt="arXiv: 2603.19461">
</a>
<a href="https://ai.meta.com/research/publications/hyperagents/">
  <img src="https://img.shields.io/badge/HyperAgents-Blog-8A2BE2.svg?style=for-the-badge&logo=readthedocs&logoColor=white" alt="HyperAgents Blog">
</a>
</p>

---

</div>

## Core Concept

HyperClaw operates as a **population of evolving agents**, where each agent is represented as a **mutable execution graph**.

Each request triggers:

1. Execution
2. Evaluation
3. Evolution (mutation + crossover)
4. Meta-evolution (adjusting the evolution process itself)

This creates a recursive improvement loop:

```
agents → execute → evaluate → evolve → repeat
```

---

## Architecture

```
HyperClaw
 ├── Population (agents as graphs)
 ├── Execution Layer (OpenClaw-style graph runner)
 ├── Evaluator (fitness function)
 ├── Evolution Engine
 │    ├── Mutation (structural + parametric)
 │    ├── Crossover (graph recombination)
 │    └── Selection (elitism)
 ├── Archive (stepping stones)
 └── Meta² Layer (evolves evolution itself)
```

---

## Agent Representation

Each agent is a **graph (program)**:

```
nodes:
  - input (IO)
  - planner (LLM)
  - executor (LLM)
  - tool nodes (optional)

edges:
  - directed connections between nodes
```

Example:

```
input → planner → executor → output
```

This allows evolution over:

* Control flow
* Tool usage
* Prompt structure
* Execution topology

---

## Key Features

### 1. Evolutionary Search

* Population-based optimization
* Elitism selection
* Mutation + crossover
* Continuous improvement across requests

### 2. Structural Mutation

* Add/remove nodes
* Modify prompts
* Change graph topology

### 3. Crossover

* Combine subgraphs from multiple agents
* Enables reuse of useful structures

### 4. Async Evaluation

* Parallel scoring of agents
* Scales with compute

### 5. Persistence

* Population and archive saved to disk
* Evolution continues across restarts

### 6. Stepping-Stone Archive

* Stores high-performing intermediate agents
* Prevents loss of useful structures

### 7. Meta² Evolution

* Adjusts evolution parameters (e.g. selection pressure)
* Moves toward self-improving optimization process

---

## API

OpenAI-compatible endpoint:

```
POST /v1/chat/completions
```

### Request

```json
{
  "model": "hyperclaw",
  "messages": [
    {"role": "user", "content": "Your input here"}
  ]
}
```

### Response

```json
{
  "id": "...",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Generated output"
      }
    }
  ],
  "debug": {
    "best_fitness": 8,
    "archive_size": 12,
    "elite_k": 3,
    "population": 8
  }
}
```

---

## Evolution Loop

Each API call executes:

```
1. Evaluate population
2. Select top-K agents (elitism)
3. Generate offspring:
     - mutation OR
     - crossover
4. Replace population
5. Update meta-parameters
6. Return best agent output
```

---

## Mutation Types

* Prompt mutation
* Node insertion
* Edge removal
* Tool injection (extensible)

---

## Crossover

Combines:

* Nodes from parent A and B
* Partial edge sets

This enables reuse of discovered substructures.

---

## Evaluation

Current implementation:

```
fitness = len(output) % 10
```

This is a placeholder.

### Replace with:

* Unit test success rates
* Task completion metrics
* Profit signals (e.g. trading systems)
* Simulation rewards
* Latency / cost efficiency

**Evaluator quality determines system performance.**

---

## Persistence

State is stored in:

```
hyperclaw_state.json
```

Includes:

* Population
* Archive

This enables long-term evolution.

---

## Limitations

Current system is a minimal prototype:

* Weak evaluator (low signal)
* No constraint enforcement (graphs may degrade)
* No type system for nodes
* No long-horizon credit assignment
* No distributed execution

---

## Recommended Extensions

### High Priority

1. Replace evaluator with real-world signal
2. Integrate actual OpenClaw execution
3. Enforce DAG + validity constraints
4. Introduce typed nodes:

   * planner
   * executor
   * memory
   * verifier
   * tools

### Medium Priority

5. Multi-task training (avoid overfitting)
6. Population diversity preservation
7. Novelty search (not just fitness)

### Advanced

8. Program synthesis mutations
9. Learned mutation operators
10. Cross-run meta-learning
11. Distributed evolutionary system

---

## Conceptual Positioning

HyperClaw sits at the intersection of:

* Agent systems (OpenClaw)
* Evolutionary computation
* Self-improving systems (HyperAgents)
* Program search

It is **not** just:

* prompt engineering
* fine-tuning
* static agent design

It is a **recursive optimizer over agents themselves**.

---

## Minimal Mental Model

```
Traditional AI:
    optimize parameters

HyperClaw:
    optimize programs that optimize themselves
```

---

## Summary

HyperClaw is an experimental framework for:

* Autonomous agent improvement
* Structural evolution of AI systems
* Recursive optimization loops

Its effectiveness depends primarily on:

> The quality of the evaluation function and the richness of the mutation space.
