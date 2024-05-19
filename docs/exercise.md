# Exercise

Download the code that comes with the assignment. The hill_climbing.py code has 5 places where you need to write code. The test.py file has tests you can run against your code to make sure they work correctly. For full marks in 1.1 your code will need to pass the provided tests, as well as continue to perform correctly with some additional states. Make sure that you name your python code `<your upi>.py` when submitting it!

## Local Search Implementation

### Task 1 [1 mark]

Complete the n-queens implementation provided by implementing the 2 missing methods in the NQueensHillClimbing code; actions and result. Refer to action_and_result_examples and the test_action_and_result function in tests.py to ensure your method output is correct.

### Task 2 [0.5 marks]

Write a function called hill_climbing_instrumented, which performs hill climbing exactly as the provided hill_climbing function does, but outputs additional information. It must return a dictionary containing entries for the number of expanded nodes and whether the problem is solved or not, and lastly the board state found with the highest hill climbing value. Refer to the function signature and dummy return value in the provided function skeleton, and check the corresponding examples and tests in the test.py file to make sure you return the correct information.

### Task 3 [0.5 marks]

Write a new hill climbing function called hill_climbing_sideways, that implements the sideways moves discussed in the lectures. It should return the same information as task 2, and additionally the number of sideways moves taken. This must allow the user to specify the maximum number of sideways moves used. Again, refer to the function skeleton and test.py for the exact format required. Make sure you continue to use the provided method for selecting the best neighbouring state (Node.best_of, as used in the hill_climbing function) to ensure your output matches the test examples.

### Task 4 [0.5 marks]

Write a new hill climbing function called hill_climbing_random_restart, that implements the random restarts discussed in the lectures. It should return the same information as task 2, and additionally the number of restarts taken. This must allow the user to specify the maximum number of random restarts used. Again, refer to the function skeleton and test.py for the exact format required. Use the provided NQueensProblem.random_state method to ensure your output matches the test examples. When debugging your code, don’t forget to use random.seed for reproducible results.
