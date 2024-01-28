import time
import cvxpy
import matplotlib.pyplot as plt
import random


def egalitarian_allocation(valuations: list[list[float]]):
    # Declare the variables and utility
    num_of_players = len(valuations)
    num_of_resources = len(valuations[0])
    variables = []
    utility_for_player = []

    # Calculation of the utility for all player
    for i in range(num_of_players):
        utility = 0
        for j in range(num_of_resources):
            variables.append(cvxpy.Variable(num_of_players))  # fractions of all the resources by number of player
            utility += variables[j][i] * valuations[i][j]  # Calculation of the utility for player i
        utility_for_player.append(utility)  # insert  utility for player i to utility list

    min_utility = cvxpy.Variable()

    # list all the constraints for the maximize function
    fixed_constraints = \
        [variables[i][j] >= 0 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [variables[i][j] <= 1 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [utility_for_player[i] >= min_utility for i in range(num_of_players)] + \
        [sum(variables[i]) == 1 for i in range(num_of_resources)]

    # solve the equation
    prob = cvxpy.Problem(cvxpy.Maximize(min_utility), constraints=fixed_constraints)
    prob.solve(solver=cvxpy.ECOS)


def egalitarian_allocation_indivisible(valuations: list[list[float]]):
    # Declare the variables and utility
    num_of_players = len(valuations)
    num_of_resources = len(valuations[0])
    variables = []
    utility_for_player = []

    # Calculation of the utility for all player
    for i in range(num_of_players):
        utility = 0
        for j in range(num_of_resources):
            variables.append(
                cvxpy.Variable(num_of_players, integer=True))  # fractions of all the resources by number of player
            utility += variables[j][i] * valuations[i][j]  # Calculation of the utility for player i
        utility_for_player.append(utility)  # insert  utility for player i to utility list

    min_utility = cvxpy.Variable()

    # list all the constraints for the maximize function
    fixed_constraints = \
        [variables[i][j] >= 0 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [variables[i][j] <= 1 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [utility_for_player[i] >= min_utility for i in range(num_of_players)] + \
        [sum(variables[i]) == 1 for i in range(num_of_resources)]

    # solve the equation
    prob = cvxpy.Problem(cvxpy.Maximize(min_utility), constraints=fixed_constraints)
    prob.solve()


num_of_resources_list = [100, 200, 300, 400, 500, 600, 700, 800, 900,
                         1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700,
                         1800, 1900, 2000, 2100, 2200, 2300, 2400]
runtimes = []
runtimesIndivisible = []

for num_of_resources in num_of_resources_list:
    player1 = []
    player2 = []
    player3 = []
    # fill all values for resources
    player1.extend(random.randint(1, 100) for i in range(num_of_resources))
    player2.extend(random.randint(1, 100) for i in range(num_of_resources))
    player3.extend(random.randint(1, 100) for i in range(num_of_resources))

    valuations = [player1, player2, player3]
    start_time = time.time()  # start measuring times
    egalitarian_allocation(valuations)
    end_time = time.time()  # stop measuring times
    runtime = end_time - start_time  # calculation runtime
    runtimes.append(runtime)

    start_time = time.time()  # start measuring times
    egalitarian_allocation_indivisible(valuations)
    end_time = time.time()  # stop measuring times
    runtime = end_time - start_time  # calculation runtime
    runtimesIndivisible.append(runtime)

# Plot the graph
plt.plot(num_of_resources_list, runtimes, label="Continuous")  # line for continuous resources
plt.plot(num_of_resources_list, runtimesIndivisible, label="Indivisible")  # line for indivisible resources
plt.title('Runtime vs. Number of Resources')
plt.xlabel('Number of Resources')
plt.ylabel('Runtime (seconds)')
plt.grid(True)
plt.legend()
plt.show()