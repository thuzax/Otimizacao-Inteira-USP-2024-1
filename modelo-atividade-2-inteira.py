import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    c = [1, 1]
    model = Model(solver_name="CBC", sense=MINIMIZE)


    x1 = model.add_var(name="x1", lb=1, ub=3, var_type=CONTINUOUS)
    x2 = model.add_var(name="x2", lb=1, var_type=CONTINUOUS)
    y = model.add_var(name="y", var_type=BINARY)

    model.objective = c[0] * x1 + c[1] * x2

    model.add_constr(x1 >= 2*(1-y))
    model.add_constr(x2 <= 2 - 0.5*y)

    model.optimize()
    print_model(model)

    print(x1.x)
    print(x2.x)
    print(y.x)
    


