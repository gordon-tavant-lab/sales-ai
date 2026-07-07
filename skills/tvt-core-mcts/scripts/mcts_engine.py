"""
tvt-core-mcts engine — generic Monte Carlo Tree Search
Interface: python mcts_engine.py <problem.py> [config.json]
"""
import math
import random
import json
import sys
import importlib.util
from typing import Any, Callable, List, Optional


class MCTSNode:
    def __init__(self, state: Any, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children: List["MCTSNode"] = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions: Optional[list] = None

    def ucb1(self, exploration: float) -> float:
        if self.visits == 0:
            return float("inf")
        return (self.value / self.visits) + exploration * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

    def best_child(self, exploration: float) -> "MCTSNode":
        return max(self.children, key=lambda c: c.ucb1(exploration))

    def is_fully_expanded(self) -> bool:
        return self.untried_actions is not None and len(self.untried_actions) == 0


class MCTS:
    def __init__(
        self,
        get_actions: Callable,
        apply_action: Callable,
        is_terminal: Callable,
        get_reward: Callable,
        rollout_policy: Optional[Callable] = None,
        exploration_weight: float = 1.414,
        iterations: int = 1000,
        max_rollout_depth: int = 50,
    ):
        self.get_actions = get_actions
        self.apply_action = apply_action
        self.is_terminal = is_terminal
        self.get_reward = get_reward
        self.rollout_policy = rollout_policy or (
            lambda state, actions: random.choice(actions)
        )
        self.exploration_weight = exploration_weight
        self.iterations = iterations
        self.max_rollout_depth = max_rollout_depth

    def search(self, initial_state: Any) -> dict:
        root = MCTSNode(initial_state)
        root.untried_actions = list(self.get_actions(initial_state))

        for _ in range(self.iterations):
            node = self._select(root)
            if not self.is_terminal(node.state):
                node = self._expand(node)
            reward = self._simulate(node.state)
            self._backpropagate(node, reward)

        if not root.children:
            return {
                "error": "No actions available from initial state",
                "best_action": None,
                "win_rate": 0,
                "confidence": 0,
                "iterations": self.iterations,
                "tree": [],
            }

        # Best action = most visited child (statistically stable)
        best = max(root.children, key=lambda c: c.visits)

        return {
            "best_action": str(best.action),
            "win_rate": round(best.value / best.visits, 4) if best.visits > 0 else 0,
            "confidence": round(best.visits / self.iterations, 4),
            "iterations": self.iterations,
            "action_sequence": self._best_path(best),
            "tree": self._summarize_tree(root),
        }

    def _select(self, node: MCTSNode) -> MCTSNode:
        while not self.is_terminal(node.state):
            if not node.is_fully_expanded():
                return node
            if not node.children:
                return node
            node = node.best_child(self.exploration_weight)
        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        if node.untried_actions is None:
            node.untried_actions = list(self.get_actions(node.state))
        if not node.untried_actions:
            return node
        action = node.untried_actions.pop(random.randrange(len(node.untried_actions)))
        new_state = self.apply_action(node.state, action)
        child = MCTSNode(new_state, parent=node, action=action)
        child.untried_actions = list(self.get_actions(new_state))
        node.children.append(child)
        return child

    def _simulate(self, state: Any) -> float:
        depth = 0
        while not self.is_terminal(state) and depth < self.max_rollout_depth:
            actions = self.get_actions(state)
            if not actions:
                break
            action = self.rollout_policy(state, actions)
            state = self.apply_action(state, action)
            depth += 1
        return self.get_reward(state)

    def _backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def _best_path(self, node: MCTSNode) -> list:
        path = []
        while node is not None and node.action is not None:
            path.append(str(node.action))
            if node.children:
                node = max(node.children, key=lambda c: c.visits)
            else:
                break
        return path

    def _summarize_tree(self, root: MCTSNode, depth: int = 0, max_depth: int = 3) -> list:
        if depth > max_depth or not root.children:
            return []
        result = []
        for child in sorted(root.children, key=lambda c: c.visits, reverse=True)[:5]:
            result.append(
                {
                    "action": str(child.action),
                    "visits": child.visits,
                    "win_rate": round(child.value / child.visits, 3) if child.visits > 0 else 0,
                    "children": self._summarize_tree(child, depth + 1, max_depth),
                }
            )
        return result


ENGINE_PATH = __file__


def load_problem(path: str):
    spec = importlib.util.spec_from_file_location("mcts_problem", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: mcts_engine.py <problem.py> [config.json]"}))
        sys.exit(1)

    problem_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else None

    config = {"iterations": 1000, "exploration_weight": 1.414, "max_rollout_depth": 50}
    if config_path:
        with open(config_path) as f:
            config.update(json.load(f))

    try:
        problem = load_problem(problem_path)
    except Exception as e:
        print(json.dumps({"error": f"Failed to load problem: {e}"}))
        sys.exit(1)

    for fn in ("initial_state", "get_actions", "apply_action", "is_terminal", "get_reward"):
        if not hasattr(problem, fn):
            print(json.dumps({"error": f"Problem missing required function: {fn}"}))
            sys.exit(1)

    mcts = MCTS(
        get_actions=problem.get_actions,
        apply_action=problem.apply_action,
        is_terminal=problem.is_terminal,
        get_reward=problem.get_reward,
        rollout_policy=getattr(problem, "rollout_policy", None),
        exploration_weight=float(config["exploration_weight"]),
        iterations=int(config["iterations"]),
        max_rollout_depth=int(config["max_rollout_depth"]),
    )

    initial = problem.initial_state()
    results = mcts.search(initial)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
