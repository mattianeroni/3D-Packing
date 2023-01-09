import collections 
import operator 
import functools


def best_fit (order, pallets_generator, packer, evaluation=None):
    """
    Best Fit Aprroach.
    Every time a new packing is required, the pallets are prioritized
    according to a provided function.
    If none of the pallets is feasible, a new pallet is started.

    :param order: The customer order to process as a set of orderlines.
    :param pallets_generator: A generator of standardized pallets.
    :param packer: The packing algorithm.
    :param evaluation: A function hat takes as arguments (pallet, orderline)
                    and returns a number. The lower is the number the better is
                    the assignment.
                    If None, we prioritize the pallets with the minor 
                    remaining volume. 

    :return: A set of pallets able to contain the required products.
    """
    last_pallet = next(pallets_generator)
    pallets = [last_pallet,]

    if evaluation is None:
        def evaluation (pallet, orderline):
            if pallet.volume + orderline.volume > pallet.maxVolume:
                return float('inf')
            return pallet.maxVolume - pallet.volume
    
    # Sort orderlines according for ascending strength
    # NOTE: This is not that reasonable in this case (to reconsider)
    orderlines = sorted(order, key=lambda i: (i.strength, i.volume), reverse=True)

    for orderline in orderlines:
        sorted_pallets = sorted(pallets, key=functools.partial(evaluation, orderline=orderline))
        packing_result = next( ((i, pallet) for pallet in sorted_pallets if (i := packer(pallet, orderline))[0]), None )
        
        # Start a new pallet...
        if packing_result is None:
            target_pallet = next(pallets_generator)
            pallets.append(target_pallet) 
            done, packedCases, layersMap = packer(target_pallet, orderline)
            if not done:
                raise Exception(f"{orderline} cannot be stored in a single pallet.")
        else:
            # A target pallet has been found among the existing ones
           (done, packedCases, layersMap), target_pallet = packing_result

        # Update loaded pallet
        target_pallet.cases = packedCases
        target_pallet.layersMap = layersMap
        target_pallet.weight += orderline.weight
        target_pallet.volume += orderline.volume
        target_pallet.orderlines.add(orderline)
    
    # Return pallets list
    return pallets
