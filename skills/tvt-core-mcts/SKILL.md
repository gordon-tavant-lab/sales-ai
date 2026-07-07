---
name: tvt-core-mcts
description: 'Core skill — raw Monte Carlo Tree Search (MCTS) engine. Takes any
  decision problem with a defined state space and finds the statistically best action
  sequence by running simulated playouts. Three modes: solve (model a problem and
  run the algorithm end-to-end), run (execute the engine against an existing problem
  file — used by domain skills for composition), scaffold (generate a clean problem
  definition template for a new domain). This is the base primitive — no domain flavor.
  Domain-specific skills (finance, game, planning) compose on top of this. Trigger
  on "run MCTS", "monte carlo tree search", "best decision", "simulate outcomes",
  "find optimal action", "decision tree search", "what''s the best move", "run simulations
  to decide".

  '
layer: kernel
modes:
- solve
- run
- scaffold
inputs:
- name: problem
  type: text
  required: true
  description: 'solve: natural language description of the decision problem. run:
    path to an existing problem.py file. scaffold: domain name and brief context for
    template generation.

    '
- name: mode
  type: enum (solve|run|scaffold)
  required: false
  description: Default is solve.
- name: iterations
  type: int
  required: false
  description: Number of MCTS simulations. Default 1000. Scale up for large/complex
    state spaces.
- name: exploration_weight
  type: float
  required: false
  description: UCB1 exploration constant C. Default 1.414 (√2). Lower = exploit known
    good paths. Higher = explore more alternatives.
- name: max_rollout_depth
  type: int
  required: false
  description: Max steps per simulation before forcing terminal evaluation. Default
    50.
outputs:
- name: best_action
  type: text
  description: The recommended next action.
- name: action_sequence
  type: list
  description: Optimal path from root forward through the best subtree.
- name: win_rate
  type: float
  description: Average reward across all simulations that went through the best action
    (0–1).
- name: confidence
  type: float
  description: Fraction of total iterations that visited the best action node — a
    convergence signal.
- name: tree_summary
  type: structured-data
  description: Top nodes of the search tree with action, visits, win_rate per level.
depends_on: []
consumed_by: []
trigger_phrases:
- run MCTS
- monte carlo
- monte carlo tree search
- best decision
- simulate outcomes
- find optimal action
- decision tree
- what's the best move
- run simulations to decide
- /g-mcts
eval:
  mode: gate
  depth: deep
expected_impact: capital-touching
default_overhead: deep
---
# MCTS — Monte Carlo Tree Search Engine

Raw MCTS primitive. No domain assumptions. Feed it a problem; get back the statistically best action sequence.

| Mode | Purpose | Used by |
|---|---|---|
| `solve` | Model a natural-language problem, run the engine, interpret results | Interactive use |
| `run` | Execute the engine against an existing problem file, return raw results | Domain skills composing this primitive |
| `scaffold` | Generate a problem definition template for a new domain | Domain skill development |

---

## The Problem Contract

Every MCTS problem is defined by five required functions plus one optional override. This is the interface between the engine and any domain skill.

| Function | Signature | Returns |
|---|---|---|
| `initial_state()` | `() → State` | Starting state |
| `get_actions(state)` | `State → List[Action]` | All legal actions from this state. Empty list = terminal. |
| `apply_action(state, action)` | `(State, Action) → State` | New state after taking action. Never mutate — return a new object. |
| `is_terminal(state)` | `State → bool` | True when no further decisions can be made |
| `get_reward(state)` | `State → float [0–1]` | Quality of a terminal state. 1.0 = best possible outcome. |
| `rollout_policy(state, actions)` | `(State, List[Action]) → Action` | *(optional)* Which action to take during simulation. Defaults to uniform random. |

**The engine path:**
```
~/.claude/skills/tvt-core-mcts/scripts/mcts_engine.py
```

---

## Mode: run — Execute Against an Existing Problem File

This is the composition interface. Domain skills call this after they've already modeled the problem.

```bash
python ~/.claude/skills/tvt-core-mcts/scripts/mcts_engine.py \
  <path/to/problem.py> \
  <path/to/config.json>
```

Config JSON (all fields optional, shown with defaults):
```json
{
  "iterations": 1000,
  "exploration_weight": 1.414,
  "max_rollout_depth": 50
}
```

The engine validates that all five required functions are present and exits with a JSON error if any are missing.

Output is JSON on stdout:
```json
{
  "best_action": "...",
  "win_rate": 0.72,
  "confidence": 0.18,
  "iterations": 1000,
  "action_sequence": ["action1", "action2", "..."],
  "tree": [{ "action": "...", "visits": 91, "win_rate": 0.76, "children": [...] }]
}
```

---

## Mode: solve — Full Pipeline from Natural Language

### Step 1 — Model the problem

Translate the user's description into the five-function contract. Ask clarifying questions if any of these are ambiguous:

- **State**: What information fully describes a point in the decision process?
- **Actions**: What choices are available at each state? Are they finite and enumerable?
- **Transition**: How does each action change state? If stochastic, sample inside `apply_action`.
- **Terminal**: When does the decision process end?
- **Reward**: How is an outcome scored? What does 0 and 1 represent in this problem?

Write the problem definition to `/tmp/mcts_problem.py` using the template from **scaffold** mode.

### Step 2 — Run the engine

```bash
python ~/.claude/skills/tvt-core-mcts/scripts/mcts_engine.py \
  /tmp/mcts_problem.py \
  /tmp/mcts_config.json
```

### Step 3 — Interpret and report

```
MCTS RESULT — <problem title>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Best Action:     <action>
Win Rate:        <win_rate>   (avg reward across simulations)
Confidence:      <confidence> (<visits>/<iterations> iterations visited this node)
Iterations:      <iterations>

Top Alternatives Explored:
  1. <action>   visits=<N>  win_rate=<X>  ← recommended
  2. <action>   visits=<N>  win_rate=<X>
  3. <action>   visits=<N>  win_rate=<X>

Optimal Path:
  → <action> → <action> → ... → terminal

Why this action won:
  <explain what the simulations revealed about downstream outcomes vs. alternatives>
```

---

## Mode: scaffold — Generate Problem Definition Template

Generate a clean, runnable Python file for a new domain. Output is drop-in compatible with `mcts_engine.py`.

```python
"""
MCTS Problem Definition: <domain>
"""
import random
from dataclasses import dataclass, replace
from typing import List, Any

@dataclass(frozen=True)
class State:
    # All fields needed to fully describe one decision point.
    # Use frozen=True to enforce immutability — apply_action must return new State.
    ...

def initial_state() -> State:
    return State(...)

def get_actions(state: State) -> List[Any]:
    # Return [] when the decision process is over.
    ...

def apply_action(state: State, action: Any) -> State:
    # Return a new State. For stochastic transitions, sample here.
    # Example: return replace(state, field=new_value)
    ...

def is_terminal(state: State) -> bool:
    ...

def get_reward(state: State) -> float:
    # Must return a value in [0, 1]. 1.0 = best possible outcome.
    ...

# Optional — replace random rollout with domain knowledge.
# A good rollout policy is the #1 performance lever for domain skills.
# def rollout_policy(state: State, actions: List[Any]) -> Any:
#     return random.choice(actions)

if __name__ == "__main__":
    import subprocess, json, os, tempfile
    engine = os.path.expanduser("~/.claude/skills/tvt-core-mcts/scripts/mcts_engine.py")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"iterations": 1000}, f)
        cfg = f.name
    result = subprocess.run(["python", engine, __file__, cfg], capture_output=True, text=True)
    print(result.stdout)
```

---

## Algorithm Reference

Four phases per iteration, repeated N times:

```
SELECT    Walk the tree from root using UCB1 until reaching a node with untried actions.
           UCB1(node) = (value / visits) + C × √(ln(parent.visits) / visits)
           C = exploration_weight. Unvisited nodes score ∞ and are always selected first.

EXPAND    Add one new child for a randomly chosen untried action at the selected node.

SIMULATE  Run a rollout from the new node to a terminal state using rollout_policy.
           Default: uniform random action selection at each step.
           Domain override: use domain knowledge to bias toward realistic/good moves.

BACKPROP  Walk from the expanded node back to root, incrementing visits and value at each node.
```

**Best action selection:** After all iterations, pick the child of root with the **most visits** — not the highest win rate. Visit count is more statistically stable because high-win-rate nodes with few visits are often just lucky.

---

## Tuning Guide

### Iterations
| State space size | Recommended iterations |
|---|---|
| Tiny (< 20 actions, depth < 5) | 200–500 |
| Small (tic-tac-toe scale) | 1,000 |
| Medium (portfolio with 5–10 assets, 10 periods) | 5,000–10,000 |
| Large (complex sequential decisions) | 50,000+ |

**Convergence check:** If `confidence` (visit fraction of best action) is below 0.10, run more iterations — the tree hasn't seen enough of the space to be reliable.

### Exploration weight (C)
- Default √2 ≈ 1.414 is optimal for zero-sum games with rewards in {0, 1}.
- For continuous rewards (e.g., financial returns), try C = 0.5–1.0 — the range is different.
- Lower C → exploits known-good paths faster. Higher C → explores more alternatives.

### Rollout policy
Random rollout works for small state spaces and games. For finance and planning domains, a domain-informed rollout (e.g., "prefer lower-risk actions during simulation") can cut the required iterations by 10×. This is the highest-leverage tuning point for domain skills.

---

## Extension Pattern

`tvt-core-mcts` owns the algorithm. Domain skills own everything else.

**Division of responsibility:**

| Layer | Owns |
|---|---|
| `tvt-core-mcts` (this skill) | MCTS algorithm, UCB1 selection, tree traversal, convergence |
| Domain skill (e.g., a portfolio-optimization skill you build) | State design, action space, reward function, rollout policy, result interpretation |

**How to build a domain skill on top of this:**

1. Create `g-<domain>-mcts/` with its own `SKILL.md`
2. Add `depends_on: [tvt-core-mcts]` to the frontmatter
3. Define the five-function contract for your domain (scaffold mode generates the template)
4. In your skill's execution step, call `run` mode: invoke `mcts_engine.py` with your problem file
5. Post-process the raw JSON output through your domain lens before presenting to the user
6. Add `g-<domain>-mcts` to the `consumed_by` list in this file's frontmatter

**Stochastic transitions (e.g., market prices, uncertain outcomes):**
The contract assumes `apply_action` is deterministic, but stochasticity can be encoded directly:
```python
def apply_action(state, action):
    # Sample from a distribution inside apply_action
    price_change = random.gauss(mu=0.0, sigma=state.volatility)
    return replace(state, price=state.price * (1 + price_change), ...)
```
Each simulation will follow a different sampled path — this is exactly how MCTS handles stochastic domains.

**Finance extension skeleton:**
```python
# State: portfolio weights + market regime + time remaining + risk budget
# Actions: discrete rebalancing decisions (buy/sell/hold per asset, hedging)
# Reward: risk-adjusted return normalized to [0, 1]
#   e.g., reward = sigmoid(sharpe_ratio) or min(1.0, max(0.0, (return - floor) / range))
# Rollout policy: use momentum signals or mean-reversion heuristics during simulation
#   — this replaces random rollout and is the primary alpha-generation lever
```
