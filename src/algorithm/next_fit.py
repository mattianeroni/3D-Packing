import collections 
import operator 


def next_fit (order, pallets_generator, packer):
    """
    Next Fit Aprroach.
    Every time packing is not possible, a new pallet is started.

    :param order: The customer order to process as a set of orderlines.
    :param pallets_generator: A generator of standardized pallets.
    :param packer: The packing algorithm.

    :return: A set of pallets able to contain the required products.
    """
    last_pallet = next(pallets_generator)
    pallets = collections.deque((last_pallet,))
    
    # Sort orderlines according for ascending strength
    # NOTE: This is not that reasonable in this case (to reconsider)
    orderlines = sorted(order, key=operator.attrgetter("strength"), reverse=True)

    for orderline in orderlines:
        done, packedCases, layersMap = packer(last_pallet, orderline)

        # We need a new pallet
        if not done:
            last_pallet = next(pallets_generator)
            pallets.append(last_pallet)
            done, packedCases, layersMap = packer(last_pallet, orderline)
            if not done:
                raise Exception(f"{orderline} cannot be stored in a single pallet.")

        # Update loaded pallet
        last_pallet.cases = packedCases
        last_pallet.layersMap = layersMap
        last_pallet.weight += orderline.weight
        last_pallet.volume += orderline.volume
        last_pallet.orderlines.add(orderline)
    
    # Return pallets list
    return pallets

        



