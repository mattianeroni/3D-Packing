import pandas as pd

from src.orderline import OrderLine
from src.case import Case



def read_test (filename, delimiter=","):
    """ Read the csv file with the problem to solve """
    file = pd.read_csv(filename, delimiter=",").groupby("OrderID")
    orders = {}

    for order_id, order in file:

        orders[order_id] = []

        for _, line in order.iterrows():
        
            orderline = OrderLine()
            cases = tuple(Case(orderline, str(line['Code']), line['SizeX'], line['SizeY'], line['SizeZ'], line['Weight'], line['Strength'])
                     for i in range(int(line["#Cases"])))
            orderline.cases = cases
            orderline.weight = sum(c.weight for c in cases)
            orderline.volume = sum(c.volume for c in cases)
            orders[order_id].append(orderline)

    return orders
