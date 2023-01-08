from src.utils.db_reader import read_database
from src.utils.plotting import plot 
from src.utils.io import read_test


# Standard pallets' characteristics
PALLET_SIZE = (120, 80, 150)
PALLET_MAX_WEIGHT = 450



if __name__ == "__main__":

    print(read_test("./bocchiotti_tests/test_20220413.csv"))
