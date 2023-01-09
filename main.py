from src.utils.db_reader import read_database
from src.utils.plotting import plot 
from src.utils.io import read_test

from src.pallet import pallets_generator

from src.algorithm import next_fit, first_fit, best_fit
from src.packing import dubePacker, cacheDubePacker


import time 



if __name__ == "__main__":

    # Standard pallets' characteristics
    PALLET_SIZE = (120, 200, 150)
    PALLET_MAX_WEIGHT = 450

    # Read the customers request
    #orders = read_test("./bocchiotti_tests/test_20220519.csv")
    orders = read_test("./nestle_tests/test1.csv")

    # Initialise the standard pallets generator
    generator = pallets_generator(PALLET_SIZE, PALLET_MAX_WEIGHT)


    for order_id, order in orders.items():
        start_time = time.time()
        pallets = first_fit(order, generator, dubePacker)
        end_time = time.time()

        print(f"Computational time: {end_time - start_time}s")

        for p in pallets:
            plot(p)

        break