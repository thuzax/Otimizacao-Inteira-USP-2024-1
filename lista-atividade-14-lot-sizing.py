import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    number_of_periods = 6
    
    # For all tuples, the first value is fake

    demands = (0, 6, 7, 4, 6, 3, 8)
    capacities =(0, 10, 10, 10, 10, 10, 10)
    
    setup_costs = (0, 12, 15, 30, 23, 19, 45)
    production_costs = (0, 3, 4, 3, 4, 4, 5)
    storage_costs = (0, 1, 1, 1, 1, 1, 1)

    model = Model(solver_name="GRB", sense=MINIMIZE)

    production = [
        model.add_var(
            name="production_" + str(t),
            var_type=CONTINUOUS,
            lb=0
        )
        for t in range(number_of_periods+1)
    ]
    inventory = [
        model.add_var(
            name="inventory_" + str(t),
            var_type=CONTINUOUS,
            lb=0
        )
        for t in range(number_of_periods+1)
    ]

    setup_active = [
        model.add_var(
            name="setup_active_" + str(t),
            var_type=BINARY
        )
        for t in range(number_of_periods+1)
    ]


    model.objective = (
        sum(
            production_costs[t] * production[t] 
            for t in range(1, number_of_periods+1)
        )
        +
        sum(
            storage_costs[t] * inventory[t]
            for t in range(1, number_of_periods+1)
        )
        +
        sum(
            setup_costs[t] * setup_active[t]
            for t in range(1, number_of_periods+1)
        )
    )

    constr_initial_inventory = model.add_constr(
        name="initial_inventory",
        lin_expr=(inventory[0] == 0)
    )
    constr_fake_setup = model.add_constr(
        name="fake_setup",
        lin_expr=(setup_active[0] == 0)
    )
    constr_fake_production = model.add_constr(
        name="fake_production",
        lin_expr=(production[0] == 0)
    )

    constrs_production_limit = [
         model.add_constr(
            name="constrs_production_limit_" + str(t),
            lin_expr=(
                production[t]
                <= 
                capacities[t]

            )
        )
        for t in range(1, number_of_periods+1)
    ]

    constrs_demands = [
        model.add_constr(
            name="demand_attenadance_" + str(t),
            lin_expr=(
                inventory[t-1] + production[t]
                == 
                demands[t] + inventory[t]

            )
        )
        for t in range(1, number_of_periods+1)
    ]

    period_big_M = tuple([
        min(capacities[t], sum(demands[k] for k in range(t, number_of_periods+1)))
        for t in range(number_of_periods+1)
    ])

    print(period_big_M)

    constrs_active_setup = [
        model.add_constr(
            name="active_setup_" + str(t),
            lin_expr=(
                production[t]
                <= 
                period_big_M[t] * setup_active[t]

            )
        )
        for t in range(1, number_of_periods+1)
    ]

    print_model(model)

    model.optimize()

    for t in range(1, number_of_periods+1):
        print(production[t].name, production[t].x)
    for t in range(1, number_of_periods+1):
        print(inventory[t].name, inventory[t].x)
    for t in range(1, number_of_periods+1):
        print(setup_active[t].name, setup_active[t].x)
