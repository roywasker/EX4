import cvxpy


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

    # print the result
    for i in range(num_of_players):
        print(f"player {i} get items ", end=" ")
        count = 0
        for j in range(num_of_resources):
            if round(variables[j][i].value) == 1:
                if count == 0:
                    print(f"{j}", end="")
                else:
                    print(f", {j}", end="")
                count += 1
        print(f" with value {round(utility_for_player[i].value)}", end="")
        print()


egalitarian_allocation(valuations=[[11, 11, 22, 33, 44], [11, 22, 44, 55, 66], [11, 33, 22, 11, 66]])