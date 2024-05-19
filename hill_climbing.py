# based on code from: https://github.com/aimacode/aima-python

import random


class NQueensProblem:
    """
    The problem of placing N queens on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r.

    This class operates on complete state descriptions where all queens are
    on the board in each state (one in each column c). This is in contrast to
    the NQueensProblem implementation in aima-python, whose initial state has
    no queens on the board, and whose actions method generates all the valid
    positions to place a queen in the first free column.
    """

    def __init__(self, N=None, state=None):
        if N is None:
            N = len(state)
        if state is None:
            state = tuple(0 for _ in range(N))
        assert N == len(state)
        self.N = N
        self.initial = state

    def actions(self, state: tuple) -> list:
        """Return a list containing all the valid actions for `state`.

        For each column c, one action is generated for each free row r in c,
        describing moving the queen in c from her current row to row r.

        This method does not take conflicts into account. It returns all
        actions which transform the current state into a neighbouring state.
        The neighbours of the current state are all states in which the
        position of exactly one queen is different. For example:
        (0, 0, 0, 0) and (0, 0, 0, 2) are neighbours, but
        (0, 0, 0, 0) and (0, 0, 1, 1) are not.

        Node.expand calls `result` with each action returned by `actions`.
        """
        result = [
            (c, r)
            for c in range(len(state))
            for r in range(len(state))
            if r != state[c]
        ]
        # print(result)
        return result

    def result(self, state: tuple, action) -> tuple:
        """Return the result of applying `action` to `state`.

        Move the queen in the column specified by `action` to the row specified by `action`.
        Node.expand calls `result` on each action returned by `actions`.
        """
        col, row = action
        result = tuple(row if i == col else r for i, r in enumerate(state))
        return result

    def goal_test(self, state):
        """Check if all columns filled, no conflicts."""
        return self.value(state) == 0

    def value(self, state):
        """Return 0 minus the number of conflicts in `state`."""
        return -self.num_conflicts(state)

    def num_conflicts(self, state):
        """Return the number of conflicts in `state`."""
        num_conflicts = 0
        for col1, row1 in enumerate(state):
            for col2, row2 in enumerate(state):
                if (col1, row1) != (col2, row2):
                    num_conflicts += self.conflict(row1, col1, row2, col2)
        return num_conflicts

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (
            row1 == row2  # same row
            or col1 == col2  # same column
            or row1 - col1 == row2 - col2  # same \ diagonal
            or row1 + col1 == row2 + col2
        )  # same / diagonal

    def random_state(self):
        """Return a new random n-queens state.

        Use this to implement hill_climbing_random_restart.
        """
        return tuple(random.choice(range(self.N)) for _ in range(self.N))


class Node:
    """
    A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node.
    Delegates problem specific functionality to self.problem.
    """

    def __init__(self, problem, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.problem = problem
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):  # print
        return "<Node {}>".format(self.state)

    def __lt__(self, node):  # smaller than
        return self.state < node.state

    def __eq__(self, node):  # equal
        return self.state == node.state

    def value(self):  # its value
        return self.problem.value(self.state)

    def goal_test(self):  # check if it is the goal (no conflics)
        return self.problem.goal_test(self.state)

    def expand(self):
        """List the nodes reachable from this node."""
        state = self.state
        problem = self.problem
        return [
            Node(
                state=problem.result(state, action),
                problem=problem,
                parent=self,
                action=action,
            )
            for action in problem.actions(state)
        ]

    def best_of(self, nodes):
        """Return the best Node from a list of Nodes, based on problem.value.

        Sorting the nodes is not the best for runtime or search performance,
        but it ensures that the result is deterministic for the purpose of
        this assignment.
        """
        return max(
            sorted(nodes),
            key=lambda node: node.value(),
        )


def hill_climbing(problem):
    """
    [Figure 4.2] in the textbook.
    From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better.
    """
    current = Node(problem=problem, state=problem.initial)
    while True:
        if current.goal_test():
            break
        neighbours = current.expand()
        if not neighbours:
            break
        neighbour = current.best_of(neighbours)
        if neighbour.value() <= current.value():
            break
        current = neighbour
    return current.state


def hill_climbing_instrumented(problem):
    """
    Find the same solution as `hill_climbing`, and return a dictionary
    recording the number of nodes expanded, and whether the problem was
    solved.
    """
    expanded = 0
    solved = False

    current = Node(problem=problem, state=problem.initial)
    while True:
        if current.goal_test():
            solved = True
            break

        # Compute other actions
        neighbours = current.expand()
        expanded += 1
        if not neighbours:
            break

        # Get the best action
        neighbour = current.best_of(neighbours)
        if neighbour.value() <= current.value():
            break
        current = neighbour

    return {
        "expanded": expanded,
        "solved": solved,
        "best_state": current.state,
    }


def hill_climbing_sideways(problem, max_sideways_moves):
    """
    When the search would terminate because the best neighbour doesn't
    have a higher value than the current state, continue the search if
    the the best neighbour's value is equal to that of the current state.

    But don't do this more than `max_sideways_moves` times. Watch out for
    off by one errors, and don't forget to return early if the search finds
    a goal state.
    """
    ######################
    ### Your code here ###
    ######################
    return {
        "expanded": int,
        "solved": bool,
        "best_state": tuple,
        "sideways_moves": int,
    }


def hill_climbing_random_restart(problem, max_restarts):
    """
    When the search would terminate because the best neighbour doesn't
    have a higher value than the current state, generate a new state to
    continue the search from (using problem.random_state).

    But don't do this more than `max_restarts` times. Watch out for
    off by one errors, and don't forget to return early if the search finds
    a goal state.

    To get consistent results each time, call random.seed(YOUR_FAVOURITE_SEED)
    before calling this function.
    """
    ######################
    ### Your code here ###
    ######################
    return {
        "expanded": int,
        "solved": bool,
        "best_state": tuple,
        "restarts": int,
    }
