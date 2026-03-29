#!/usr/bin/env python3
"""Pushdown automaton simulator. Zero dependencies."""

class PDA:
    def __init__(self, transitions, start, start_stack, accept):
        self.transitions = transitions; self.start = start
        self.start_stack = start_stack; self.accept = set(accept)

    def accepts(self, input_str):
        configs = [(self.start, list(input_str), [self.start_stack])]
        visited = set()
        while configs:
            state, remaining, stack = configs.pop()
            key = (state, tuple(remaining), tuple(stack))
            if key in visited: continue
            visited.add(key)
            if not remaining and state in self.accept: return True
            top = stack[-1] if stack else None
            ch = remaining[0] if remaining else None
            for (s, inp, stk_top), actions in self.transitions.items():
                if s != state: continue
                if stk_top is not None and stk_top != top: continue
                if inp is not None and inp != ch: continue
                for next_state, push in actions:
                    new_stack = stack[:-1] if stk_top is not None else stack[:]
                    if push: new_stack.extend(reversed(push))
                    new_remaining = remaining[1:] if inp is not None else remaining[:]
                    configs.append((next_state, new_remaining, new_stack))
        return False

def balanced_parens_pda():
    """PDA that accepts balanced parentheses."""
    transitions = {
        ("q0", "(", "Z"): [("q0", ["(", "Z"])],
        ("q0", "(", "("): [("q0", ["(", "("])],
        ("q0", ")", "("): [("q0", [])],
        ("q0", None, "Z"): [("q1", [])],
    }
    return PDA(transitions, "q0", "Z", {"q1"})

def anbn_pda():
    """PDA that accepts a^n b^n."""
    transitions = {
        ("q0", "a", "Z"): [("q0", ["A", "Z"])],
        ("q0", "a", "A"): [("q0", ["A", "A"])],
        ("q0", "b", "A"): [("q1", [])],
        ("q1", "b", "A"): [("q1", [])],
        ("q1", None, "Z"): [("q2", [])],
    }
    return PDA(transitions, "q0", "Z", {"q2"})

if __name__ == "__main__":
    pda = balanced_parens_pda()
    for s in ["()", "(())", "(()", ")(", ""]:
        print(f"'{s}': {pda.accepts(s)}")
