import os

from mip import *


def print_model(model):
    model.write("temp.lp")
    with open("temp.lp", "r") as f_model:
        text = f_model.read()
        print(text)
        os.remove("temp.lp")

if __name__=="__main__":
    big_m_1 = 10000
    big_m_2 = 1000
    big_m_3 = 10
    
    stations = 10

    frequencies_set = (1, 2, 3, 4, 5, 6)
    number_of_frequencies = len(frequencies_set)

    minimum_freq_differences = (
        (0, 0, 0, 0, 0, 0, 0, 2, 0, 0),
        (0, 0, 2, 0, 2, 0, 0, 0, 0, 1),
        (0, 2, 0, 4, 0, 0, 0, 0, 0, 1),
        (0, 0, 4, 0, 2, 0, 0, 0, 0, 0),
        (0, 2, 0, 2, 0, 3, 3, 0, 2, 4),
        (0, 0, 0, 0, 3, 0, 1, 0, 0, 0),
        (0, 0, 0, 0, 3, 1, 0, 1, 0, 2),
        (2, 0, 0, 0, 0, 0, 1, 0, 2, 0),
        (0, 0, 0, 0, 2, 0, 0, 2, 0, 3),
        (0, 1, 1, 0, 4, 0, 2, 0, 3, 0)
    )
    
    model = Model(solver_name="GRB", sense=MINIMIZE)


    station_frequency = [
        model.add_var(
            name="station_frequency_"+ str(i) , 
            var_type=INTEGER,
            lb=min(frequencies_set),
            ub=max(frequencies_set)
        )
        for i in range(stations)
    ]
    
    frequence_i_bigger_j = [
        [
            model.add_var(
                name="frequence_i_bigger_j_" + str(i) + "_" + str(j),
                var_type=BINARY,
            )
            for j in range(stations)
        ]
        for i in range(stations)
    ]

    min_freq = model.add_var(
        name="min_freq",
        var_type=INTEGER,
        lb=min(frequencies_set),
        ub=max(frequencies_set)
    )

    max_freq = model.add_var(
        name="max_freq",
        var_type=INTEGER,
        lb=min(frequencies_set),
        ub=max(frequencies_set)
    )

    model.objective = max_freq - min_freq + sum(
        sum(
            frequence_i_bigger_j[i][j]/big_m_1
            for j in range(stations)
        )
        for i in range(stations)
    )

    constrs_differnce_i_j = [
        model.add_constr(
            name="differnce_i_j_" + str(i) + "_" + str(j),
            lin_expr=(
                station_frequency[i] - station_frequency[j]
                >=
                (
                    minimum_freq_differences[i][j] 
                    -
                    frequence_i_bigger_j[i][j] * big_m_3
                )
            )
        )
        for i in range(stations) for j in range(i+1, stations)
        if minimum_freq_differences[i][j] > 0
    ]

    constrs_differnce_j_i = [
        model.add_constr(
            name="differnce_j_i_" + str(i) + "_" + str(j),
            lin_expr=(
                station_frequency[j] - station_frequency[i]
                >=
                (
                    minimum_freq_differences[i][j] 
                    - (1 - frequence_i_bigger_j[i][j]) * big_m_3
                )
            )
        )
        for i in range(stations) for j in range(i+1, stations)
        if minimum_freq_differences[i][j] > 0
    ]

    verify_i_bigger_j = [
        model.add_constr(
            name="i_bigger_j_" + str(j) + "_" + str(i),
            lin_expr=(
                frequence_i_bigger_j[i][j]
                >= 
                1/big_m_2 * (station_frequency[i] - station_frequency[j])
            )
        )
        for i in range(stations) for j in range(i+1, stations)
        if (minimum_freq_differences[i][j] > 0)
    ]
    
    # constrs_max_freq =  [
    #     model.add_constr(
    #         name="max_freq_" + str(i),
    #         lin_expr=(
    #             max_freq
    #             >=
    #             station_frequency[i]
    #         )
    #     )
    #     for i in range(stations)
    # ]

    # constrs_min_freq =  [
    #     model.add_constr(
    #         name="min_freq_" + str(i),
    #         lin_expr=(
    #             min_freq
    #             <=
    #             station_frequency[i]
    #         )
    #     )
    #     for i in range(stations)
    # ]


    print_model(model)

    model.optimize()

    for line in frequence_i_bigger_j:
        for var in line:
            print(var.name, var.x)
    for var in station_frequency:
        print(var.name, var.x)

    print(min_freq.name, min_freq.x)
    print(max_freq.name, max_freq.x)


