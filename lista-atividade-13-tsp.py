import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    big_m = 100
    c = [
        [big_m, 1, 1, big_m, big_m, big_m, big_m, big_m],
        [1, big_m, 1, 2, big_m, 5, big_m, big_m],
        [1, 1, big_m, 2, big_m, big_m, 4, big_m],
        [big_m, 2, 2, big_m, big_m, big_m, big_m, 1],
        [big_m, big_m, big_m, big_m, big_m, 1, 1, big_m],
        [big_m, 5, big_m, big_m, 1, big_m, 1, 2],
        [big_m, big_m, 4, big_m, 1, 1, big_m, 2],
        [big_m, big_m, big_m, 1, big_m, 2, 2, big_m],
    ]
    
    n = len(c)

    big_M = n
    
    model = Model(solver_name="GRB", sense=MINIMIZE)


    x = [
        [model.add_var(
                name="x_"+ str(i) + "_" + str(j), 
                lb=0, 
                ub=1, 
                var_type=BINARY
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    u = [model.add_var(
            name="u_" + str(i), 
            var_type=INTEGER,
            lb=1,
            ub=n-1
        )
        for i in range(n)
    ]


    model.objective = (
        sum([
            sum(
                c[i][j] * x[i][j] 
                for j in range(n)
            ) 
            for i in range(n)
        ])
    )

    constr_ii_is_zero = [model.add_constr(
            name="x_ii_is_zero_" + str(i),
            lin_expr=(
                x[i][i]
                ==
                0
            )
        )
        for i in range(n)
    ]

    constrs_outing = [model.add_constr(
            name="eges_outing_" + str(i),
            lin_expr=(
                sum(x[i][j] for j in range(n))
                ==
                1
            )
        )
        for i in range(n)
    ]

    constrs_outing = [model.add_constr(
            name="edges_comming_" + str(j),
            lin_expr=(
                sum(x[i][j] for i in range(n))
                ==
                1
            )
        )
        for j in range(n)
    ]

    constrs_mtz = [model.add_constr(
            name="mtz_" + str(i) + "_" + str(j),
            lin_expr=(
                u[i] - u[j] + (n-1) * x[i][j]
                <=
                n-2
            )
        )
        for i in range(1, n) for j in range(1, n)
    ]


    print_model(model)

    model.optimize()

    for line in x:
        for var in line:
            print(var.name, var.x)

    for line in x:
        for var in line:
            if (var.x > 0.99):
                print(var.name)

