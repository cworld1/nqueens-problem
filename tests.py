"""
Run test_all() to test NQueensProblem, hill_climbing_instrumented, hill_climbing_sideways and hill_climbing_random_restart.

Or run their individual tests. Methods to be tested are imported from hill_climbing.py in the same directory as this file.
"""

import random
from functools import wraps

from hill_climbing import (
    NQueensProblem,
    hill_climbing_instrumented,
    hill_climbing_sideways,
    hill_climbing_random_restart,
)


SEED = 1
VERBOSE = True


# {state: problem.result(state, problem.actions(state))}
action_and_result_examples = {
    (0, 0): [(1, 0), (0, 1)],
    (0, 1): [(1, 1), (0, 0)],
    (0, 0, 0, 0): [  # 4 queens, all in row 0
        (1, 0, 0, 0),
        (2, 0, 0, 0),
        (3, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 2, 0, 0),
        (0, 3, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 2, 0),
        (0, 0, 3, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 2),
        (0, 0, 0, 3),
    ],
    (0, 1, 2, 3): [  # 4 queens, arranged diagonally
        (1, 1, 2, 3),
        (2, 1, 2, 3),
        (3, 1, 2, 3),
        (0, 0, 2, 3),
        (0, 2, 2, 3),
        (0, 3, 2, 3),
        (0, 1, 0, 3),
        (0, 1, 1, 3),
        (0, 1, 3, 3),
        (0, 1, 2, 0),
        (0, 1, 2, 1),
        (0, 1, 2, 2),
    ],
}


# {args: f(*args)}
# {(state,): hill_climbing_instrumented(state)}
hill_climbing_instrumented_examples = {
    ((0, 0, 0, 0),): {
        "expanded": 3,
        "solved": True,
        "best_state": (2, 0, 3, 1),
    },
    ((0, 1, 2, 3),): {
        "expanded": 3,
        "solved": False,
        "best_state": (1, 0, 2, 3),
    },
}


# {args: f(*args)}
# {(state, max_sideways_moves): hill_climbing_sideways(state, max_sideways_moves)}
hill_climbing_sideways_examples = {
    ((0, 0, 0, 0), 1): {
        "expanded": 3,
        "solved": True,
        "best_state": (2, 0, 3, 1),
        "sideways_moves": 0,
    },
    ((0, 1, 2, 3), 1): {
        "expanded": 5,
        "solved": False,
        "best_state": (1, 2, 0, 3),
        "sideways_moves": 1,
    },
    ((0, 0, 0, 0), 10): {
        "expanded": 3,
        "solved": True,
        "best_state": (2, 0, 3, 1),
        "sideways_moves": 0,
    },
    ((0, 1, 2, 3), 10): {
        "expanded": 6,
        "solved": True,
        "best_state": (1, 3, 0, 2),
        "sideways_moves": 2,
    },
    ((0, 0, 0, 0, 0, 0, 0, 0), 10): {
        "expanded": 17,
        "solved": False,
        "best_state": (4, 0, 0, 3, 6, 2, 7, 1),
        "sideways_moves": 10,
    },
    ((0, 1, 2, 3, 4, 5, 6, 7), 10): {
        "expanded": 18,
        "solved": False,
        "best_state": (3, 0, 7, 4, 1, 5, 2, 6),
        "sideways_moves": 10,
    },
    ((0, 0, 0, 0, 0, 0, 0, 0), 100): {
        "expanded": 107,
        "solved": False,
        "best_state": (4, 0, 0, 3, 6, 2, 7, 1),
        "sideways_moves": 100,
    },
    ((0, 1, 2, 3, 4, 5, 6, 7), 100): {
        "expanded": 108,
        "solved": False,
        "best_state": (3, 0, 7, 4, 1, 5, 2, 6),
        "sideways_moves": 100,
    },
}


# {args: f(*args)}
# {(state, max_restarts): hill_climbing_random_restart(state, max_restarts)}
hill_climbing_random_restart_examples = {
    ((0, 0, 0, 0), 1): {
        "expanded": 3,
        "solved": True,
        "best_state": (2, 0, 3, 1),
        "restarts": 0,
    },
    ((0, 1, 2, 3), 1): {
        "expanded": 5,
        "solved": False,
        "best_state": (1, 3, 2, 0),
        "restarts": 1,
    },
    ((0, 0, 0, 0), 10): {
        "expanded": 3,
        "solved": True,
        "best_state": (2, 0, 3, 1),
        "restarts": 0,
    },
    ((0, 1, 2, 3), 10): {
        "expanded": 8,
        "solved": True,
        "best_state": (2, 0, 3, 1),
        "restarts": 2,
    },
    ((0, 0, 0, 0, 0, 0, 0, 0), 10): {
        "expanded": 24,
        "solved": True,
        "best_state": (5, 1, 6, 0, 2, 4, 7, 3),
        "restarts": 4,
    },
    ((0, 1, 2, 3, 4, 5, 6, 7), 10): {
        "expanded": 24,
        "solved": True,
        "best_state": (5, 1, 6, 0, 2, 4, 7, 3),
        "restarts": 4,
    },
}


def verbose_test(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        errors = test(*args, **kwargs)
        if not VERBOSE:
            return errors
        if not errors:
            print("PASSED:", test.__name__)
            return errors
        print()
        print("FAILED:", test.__name__)
        for problem, error in errors.items():
            print("\t", problem, sep="")
            print("\tyour result:", error["result"])
            print("\ttrue result:", error["example_result"])
            if "keys" in error:
                print("\tthese keys were in error:", error["keys"])
            print()
        return errors
    return wrapper


def prefix_errors(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        errors = test(*args, **kwargs)
        return {
            (test.__name__, problem): error
            for problem, error in errors.items()
        }
    return wrapper


def test_all():
    """Run all tests.

    Call get_all_prefixed_errors to get all errors as a dict.
    """
    get_all_prefixed_errors()


def get_all_prefixed_errors():
    return {
        **prefix_errors(test_action_and_result)(),
        **prefix_errors(test_hill_climbing_instrumented)(),
        **prefix_errors(test_hill_climbing_sideways)(),
        **prefix_errors(test_hill_climbing_random_restart)(),
    }


@verbose_test
def test_action_and_result():
    errors = {}
    for state, example_result in action_and_result_examples.items():
        problem = NQueensProblem(state=state)
        result = [
            problem.result(problem.initial, action)
            for action in problem.actions(problem.initial)
        ]
        if set(result) != set(example_result):
            errors[state] = {
                "example_result": example_result,
                "result": result,
            }
    return errors


@verbose_test
def test_hill_climbing_instrumented():
    return hill_climbing_test(hill_climbing_instrumented)


@verbose_test
def test_hill_climbing_sideways():
    return {
        **vanilla_check(hill_climbing_sideways),
        **hill_climbing_test(hill_climbing_sideways),
    }


@verbose_test
def test_hill_climbing_random_restart():
    return {
        **vanilla_check(hill_climbing_random_restart),
        **hill_climbing_test(hill_climbing_random_restart),
    }


@prefix_errors
def vanilla_check(hill_climbing_method, examples=hill_climbing_instrumented_examples):
    """Check if hill_climbing_method with a restart / sideways move limit of 0 returns results identical to hill_climbing_instrumented."""
    def hill_climbing_proxy(problem):
        return hill_climbing_method(problem, 0)
    return hill_climbing_test(hill_climbing_proxy, examples=examples)


@prefix_errors
def hill_climbing_test(hill_climbing_method, examples=None):
    """Check if provided hill_climbing_method has the correct output."""
    if examples is None:
        examples = globals()[hill_climbing_method.__name__ + "_examples"]
    answers = generate_answers(hill_climbing_method, problems=examples)
    errors = {}
    for problem, example_result in examples.items():
        result = answers[problem]
        keys = []
        for key, value in example_result.items():
            if result[key] != value:
                keys.append(key)
        if keys:
            errors[problem] = {
                "example_result": example_result,
                "result": result,
                "keys": keys,
            }
    return errors


def generate_answers(hill_climbing_method, problems=None):
    """Return dictionary of results of running hill_climbing_method on problems."""
    if problems is None:
        examples = globals()[hill_climbing_method.__name__ + "_examples"]
    answers = {}
    for key in problems:
        state, *args = key
        problem = NQueensProblem(state=state)
        random.seed(SEED)
        result = hill_climbing_method(problem, *args)
        answers[key] = result
    return answers
