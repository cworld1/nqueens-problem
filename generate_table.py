import timeit, statistics

from hill_climbing import (
    NQueensProblem,
    hill_climbing_instrumented,
    hill_climbing_sideways,
    hill_climbing_random_restart,
)


# Function to measure the performance of an algorithm
def measure_performance(algorithm, n, runs):
    nqueens8 = NQueensProblem(8)
    nqueens9 = NQueensProblem(9)
    nqueens10 = NQueensProblem(10)
    success = 0
    nodes_expanded = []
    times_taken = []
    if n == 8:
        nqueens = nqueens8
    if n == 9:
        nqueens = nqueens9
    if n == 10:
        nqueens = nqueens10
    for _ in range(runs):
        start_time = timeit.default_timer()
        # Run the algorithm and store the number of expanded nodes
        if algorithm == "hillclimbing":
            temp = hill_climbing_instrumented(nqueens)
            if temp.get("solved"):
                success += 1
        if algorithm == "sideways":
            temp = hill_climbing_sideways(nqueens, 10)
            if temp.get("solved"):
                success += 1
        if algorithm == "randomrestart":
            temp = hill_climbing_random_restart(nqueens, 10)
            if temp.get("solved"):
                success += 1
        num_nodes = temp.get(
            "expanded"
        )  # Run the algorithm and get the number of expanded nodes
        elapsed_time = timeit.default_timer() - start_time
        nodes_expanded.append(num_nodes)
        times_taken.append(elapsed_time)
    avg_nodes = statistics.mean(nodes_expanded)
    std_dev_nodes = statistics.stdev(nodes_expanded)
    avg_time = statistics.mean(times_taken)
    std_dev_time = statistics.stdev(times_taken)
    success_rate = success / runs
    return avg_nodes, std_dev_nodes, avg_time, std_dev_time, success_rate


# Main function to generate the table
def generate_table():
    queens = [8, 9, 10]
    methods = ["hillclimbing", "sideways", "randomrestart"]
    runs = 10  # Number of runs for each algorithm
    print(
        "# queens\tmethod\t\tAverage # of nodes +/- std dev\tAverage time to solve +/- std dev\tProbability of solving"
    )
    for n in queens:
        print(f"{n} queens")
        for method in methods:
            avg_nodes, std_dev_nodes, avg_time, std_dev_time, success_rate = (
                measure_performance(method, n, runs)
            )
            print(
                f"\t\t{method}\t{avg_nodes:.2f} +/- {std_dev_nodes:.2f}\t\t\t\t{avg_time:.4f} +/- {std_dev_time:.4f}\t\t{success_rate:.2f}"
            )


if __name__ == "__main__":
    generate_table()
