import pandas as pd

from src.orderline import OrderLine
from src.case import Case



def read_test (filename, delimiter=","):
    """ 
    Read the csv file with the problem to solve.
    
    :param filename: The csv file where the problem is reported
    :param delimiter: The csv delimiter char
    :return: A set of orders, each of which is made of a set of orderlines, each 
            of which is reuiring a certain product in a certain quantity (i.e., number of cases)
    """
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
