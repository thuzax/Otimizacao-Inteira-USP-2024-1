import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    c = [
        [12, 13, 6, 0, 1],
        [8, 4, 9, 1, 2],
        [2, 6, 6, 0, 1],
        [3, 5, 2, 1, 8],
        [8, 0, 5, 10, 8],
        [2, 0, 3, 4, 1]
    ]
    
    n = len(c)

    f = [4, 3, 4, 4, 7]
    
    m = len(f)

    big_M = n
    
    model = Model(solver_name="GRB", sense=MINIMIZE)


    x = [
        [model.add_var(
                name="x_"+ str(i) + "_" + str(j), 
                lb=0, 
                ub=1, 
                var_type=CONTINUOUS
            )
            for j in range(m)
        ]
        for i in range(n)
    ]
    y = [model.add_var(
            name="y_" + str(j), var_type=BINARY
        )
        for j in range(5)
    ]

    print(c[0][0])
    print(x[0][0])

    model.objective = (
        sum([sum(c[i][j] * x[i][j] for j in range(5)) for i in range(n)])
        +
        sum([f[j] * y[j] for j in range(m)])
    )

    constrs_demand = [model.add_constr(
            name="demand_" + str(i),
            lin_expr=(
                sum(x[i][j] for j in range(m))
                ==
                1
            )
        )
        for i in range(6)
    ]

    constrs_depot_activation =  [
        model.add_constr(
            name="depot_activation_" + str(j),
            lin_expr=(
                sum(x[i][j] for i in range(n))
                <=
                big_M * y[j]
            )
        )
        for j in range(m)
    ]


    print_model(model)

    model.optimize()

    for line in x:
        for var in line:
            print(var.name, var.x)
    for var in y:
        print(var.name, var.x)


