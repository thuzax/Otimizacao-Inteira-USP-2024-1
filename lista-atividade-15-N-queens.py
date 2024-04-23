import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    n = 10

    model = Model(solver_name="GRB", sense=MAXIMIZE)

    x = [[
        model.add_var(
            name="x_" + str(i) + "_" + str(j),
            var_type=BINARY
        )
        for j in range(n)
    ] for i in range(n)]


    # model.objective = (sum(sum(x[i][j] for j in range(n)) for i in range(n)))

    constrs_rows = [
        model.add_constr(
            name="row_" + str(i),
            lin_expr=(
                sum(x[i][j] for j in range(n))
                ==
                1
            )
        )
        for i in range(n)
    ]

    constrs_columns = [
        model.add_constr(
            name="columns_" + str(j),
            lin_expr=(
                sum(x[i][j] for i in range(n))
                ==
                1
            )
        )
        for j in range(n)
    ]

    constrs_diagonal_top_left_right = [
        model.add_constr(
            name="diagonal_top_left_right_" + str(j),
            lin_expr=(
                x[0][j]
                +
                sum(x[k][j+k] for k in range(n-j))
                <=
                1
            )
        )
        for j in range(n-1)
    ]
    
    constrs_diagonal_top_left_down = [
        model.add_constr(
            name="diagonal_top_left_down_" + str(i),
            lin_expr=(
                x[i][0]
                +
                sum(x[i+k][k] for k in range(1, n-i))
                <=
                1
            )
        )
        for i in range(1, n-1)
    ]

    constrs_diagonal_top_right_left = [
        model.add_constr(
            name="diagonal_top_right_left_" + str(j),
            lin_expr=(
                x[0][j]
                +
                sum(x[k+1][j-k-1] for k in range(0, j))
                <=
                1
            )
        )
        for j in range(1, n)
    ]

    constrs_diagonal_top_right_down = [
        model.add_constr(
            name="diagonal_top_right_down_" + str(i),
            lin_expr=(
                x[i][n-1]
                +
                sum(x[i+k][n-k-1] for k in range(0, n-i))
                <=
                1
            )
        )
        for i in range(1, n-1)
    ]

    print_model(model)

    model.optimize()

    text = ""
    for i in range(n):
        line = ""
        for j in range(n):
            if (x[i][j].x > 0.99):
                line += "| " + str(1) + " "
            else:
                line += "| " + str(" ") + " "
        
        text += "-" * len(line) + "\n"
        text += line + "|"
        text += "\n"
    
    text += "-" * len(text.splitlines()[0]) + "\n"
    print(text)