#!/usr/bin/env python3
"""pushdown_auto - Pushdown automaton for context-free language recognition."""
import sys

class PDA:
    def __init__(self, start, accept_states, start_symbol="Z"):
        self.state = start
        self.accept = accept_states
        self.stack = [start_symbol]
        self.transitions = {}  # (state, input, stack_top) -> [(new_state, stack_push)]
    def add(self, state, inp, stack_top, new_state, stack_push):
        key = (state, inp, stack_top)
        if key not in self.transitions:
            self.transitions[key] = []
        self.transitions[key].append((new_state, stack_push))
    def accepts(self, word):
        configs = [(self.state, list(self.stack), 0)]
        visited = set()
        while configs:
            state, stack, pos = configs.pop()
            key = (state, tuple(stack), pos)
            if key in visited: continue
            visited.add(key)
            if pos == len(word) and state in self.accept:
                return True
            # Epsilon transitions
            if stack:
                for ns, sp in self.transitions.get((state, "", stack[-1]), []):
                    new_stack = stack[:-1] + list(reversed(sp)) if sp else stack[:-1]
                    configs.append((ns, new_stack, pos))
            # Input transitions
            if pos < len(word) and stack:
                for ns, sp in self.transitions.get((state, word[pos], stack[-1]), []):
                    new_stack = stack[:-1] + list(reversed(sp)) if sp else stack[:-1]
                    configs.append((ns, new_stack, pos + 1))
        return False

def test():
    # PDA for a^n b^n
    pda = PDA("q0", {"q2"}, "Z")
    pda.add("q0", "a", "Z", "q0", "AZ")
    pda.add("q0", "a", "A", "q0", "AA")
    pda.add("q0", "b", "A", "q1", "")
    pda.add("q1", "b", "A", "q1", "")
    pda.add("q1", "", "Z", "q2", "Z")
    assert pda.accepts("ab")
    assert pda.accepts("aabb")
    assert pda.accepts("aaabbb")
    pda2 = PDA("q0", {"q2"}, "Z")
    pda2.add("q0", "a", "Z", "q0", "AZ")
    pda2.add("q0", "a", "A", "q0", "AA")
    pda2.add("q0", "b", "A", "q1", "")
    pda2.add("q1", "b", "A", "q1", "")
    pda2.add("q1", "", "Z", "q2", "Z")
    assert not pda2.accepts("aab")
    assert not pda2.accepts("abb")
    print("pushdown_auto: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: pushdown_auto.py --test")
