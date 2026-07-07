# tvt-core-mcts — Monte Carlo Tree Search Engine

**MCTS = Monte Carlo Tree Search**

A decision-making algorithm that finds the best action in a complex situation by running thousands of fast simulations — playing out random futures, learning which paths lead to good outcomes, and concentrating its search there.

It was invented for game AI (Go, Chess) but it's domain-agnostic. Any problem you can express as "here are my options, here's what happens when I pick one, here's how to score the result" can be solved with MCTS. Finance, planning, resource allocation, strategy — same engine, different problem definition.

---

## The mental model

Imagine you're at a crossroads with 5 paths ahead. You don't know where they lead. You have time to scout 1,000 futures before you have to commit.

MCTS sends scouts out repeatedly. Each scout:
1. **Walks** the tree from the start, choosing which path to explore based on what's been learned so far (promising paths get more attention, unexplored paths get visited at least once)
2. **Opens** a new branch that hasn't been tried yet
3. **Runs** forward randomly from there until reaching an outcome
4. **Reports** back — was it good or bad?

After 1,000 scouts, you look at which first step was taken in the most successful futures. That's your answer.

The key insight: you don't need to search every possible future exhaustively. You just need enough samples to know which direction is statistically better — and MCTS gets there faster than brute force by steering scouts toward interesting areas.

---

## The four phases (technical)

```
SELECT    From the root, walk down the tree picking nodes with the best
          balance of "known good" and "unexplored." Formula: UCB1.
          UCB1 = (value / visits) + C × √(ln(parent_visits) / visits)
          C controls explore vs. exploit — default is √2 ≈ 1.414.

EXPAND    At the frontier, add one new untried action as a child node.

SIMULATE  From the new node, play out randomly until reaching a terminal state.
          This is the "rollout" — fast and approximate on purpose.
          Domain skills can replace random rollout with smarter heuristics.

BACKPROP  Walk back to root, crediting every node on the path with the outcome.
          This is how learning happens — good futures make their ancestors look better.
```

After N iterations: **pick the child of root with the most visits** (not the highest win rate — most visited is more statistically stable).

---

## Files

```
tvt-core-mcts/
├── SKILL.md              Claude skill definition — modes, inputs, outputs, tuning guide
├── README.md             This file
└── scripts/
    └── mcts_engine.py    The algorithm — pure Python, no dependencies
```

---

## How to use it

### As a Claude skill (three modes)

**`solve`** — Describe a decision problem in plain language. Claude models it and runs the algorithm.
```
/g-mcts "I'm choosing between three marketing strategies for Q3 — 
         paid ads, content, or partnerships. Budget is $50k."
```

**`run`** — You already have a Python problem file. Just execute it.
```
/g-mcts mode=run problem=/path/to/my_problem.py iterations=5000
```

**`scaffold`** — Generate a Python template for a new domain.
```
/g-mcts mode=scaffold problem="portfolio rebalancing"
```

### Directly via Python

```bash
python ~/.claude/skills/tvt-core-mcts/scripts/mcts_engine.py \
  my_problem.py \
  config.json
```

Output is JSON:
```json
{
  "best_action": "buy_tech_etf",
  "win_rate": 0.72,
  "confidence": 0.18,
  "iterations": 1000,
  "action_sequence": ["buy_tech_etf", "hold", "rebalance_bonds"],
  "tree": [...]
}
```

---

## The problem contract

Every problem needs five Python functions. The engine calls nothing else.

```python
def initial_state():
    """Where do we start?"""
    return State(...)

def get_actions(state):
    """What choices are available from here? Return [] when the decision is over."""
    return [action1, action2, ...]

def apply_action(state, action):
    """What happens if I choose this? Return a NEW state — don't mutate."""
    return State(...)

def is_terminal(state):
    """Are we done deciding?"""
    return bool(...)

def get_reward(state):
    """How good is this outcome? Must be between 0.0 (worst) and 1.0 (best)."""
    return float(...)
```

Optional sixth function — replaces random simulation with something smarter:
```python
def rollout_policy(state, actions):
    """Which action to take during simulation. Default: random."""
    return best_heuristic_action(state, actions)
```

**The rollout policy is the most powerful tuning lever.** Random rollout works for small problems. For finance and planning, a domain-informed rollout (e.g., bias toward lower-risk moves) can cut required iterations by 10×.

### Important rule: states must be immutable

`apply_action` must return a *new* state object, never modify the current one. The engine reuses states across many branches — mutation corrupts the tree.

```python
# Good
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class State:
    cash: float
    position: float

def apply_action(state, action):
    return replace(state, cash=state.cash - action.cost, position=state.position + action.units)

# Bad — mutates in place
def apply_action(state, action):
    state.cash -= action.cost  # corrupts the tree
    return state
```

---

## Tuning

| Parameter | Default | When to change |
|---|---|---|
| `iterations` | 1,000 | Increase for large/complex state spaces. If `confidence < 0.10`, double it. |
| `exploration_weight` (C) | 1.414 (√2) | Lower (0.5–1.0) for finance/continuous rewards. Higher to explore more alternatives. |
| `max_rollout_depth` | 50 | Increase if your decisions span many time steps. |

**Convergence check:** The `confidence` field in the output is the fraction of iterations that visited the best action. Below 0.10 means the search hasn't settled — run more iterations.

**State space sizing:**
| Problem scale | Recommended iterations |
|---|---|
| Tiny — few choices, shallow | 200–500 |
| Small — game-sized | 1,000 |
| Medium — portfolio, 5–10 assets, 10 periods | 5,000–10,000 |
| Large — complex sequential decisions | 50,000+ |

---

## Building a domain skill on top of this

`tvt-core-mcts` owns the algorithm. A domain skill owns the problem definition and result interpretation.

**Step-by-step:**

1. Create `~/.claude/skills/g-<domain>-mcts/SKILL.md`
2. Add `depends_on: [tvt-core-mcts]` to the frontmatter
3. Use `scaffold` mode to generate your `problem.py` starting point
4. Implement the five functions for your domain
5. In your skill, call `run` mode to execute the engine
6. Interpret and format the raw JSON results through your domain lens

**The split:**

| `tvt-core-mcts` handles | Domain skill handles |
|---|---|
| UCB1 selection | State design (what fields matter) |
| Tree expansion | Action space (what choices exist) |
| Backpropagation | Reward function (what makes an outcome good) |
| Convergence detection | Rollout policy (smarter-than-random simulation) |
| Result JSON | Domain-appropriate output format |

### Stochastic transitions

The contract assumes `apply_action` is deterministic, but you can encode randomness directly inside it — the engine will naturally sample different paths across simulations:

```python
import random

def apply_action(state, action):
    # Market moves are stochastic — sample from a distribution
    price_shock = random.gauss(mu=0.0, sigma=state.volatility)
    new_price = state.price * (1 + price_shock)
    return replace(state, price=new_price, cash=state.cash - action.cost)
```

Each of the N simulations follows a different sampled path. MCTS averages across them — this is the Monte Carlo part.

---

## Roadmap

```
tvt-core-mcts (this)        Raw algorithm. Done.
    └── (example) a portfolio-optimization domain skill you build on this engine:
                          State: holdings + market regime + time horizon + risk budget
                          Actions: rebalance, hold, hedge, exit positions
                          Reward: Sharpe ratio normalized to [0, 1]
                          Rollout: momentum/mean-reversion heuristics
                          Self-improving: rollout policy tuned iteratively, e.g. via an eval loop
```

The finance skill uses this engine unchanged. The alpha comes entirely from how you define the state, model the reward, and bias the rollout toward realistic market behavior.
