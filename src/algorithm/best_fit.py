import collections 
import operator 


def first_fit (order, pallets_generator, packer):
    """
    Best Fit Aprroach.
    Every time a new packing is required, all pallets from the first to the
    last one are considered. If none of them can host the new cases, a new 
    pallet is started.

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
        packing_result = next( ((i, pallet) for pallet in pallets if (i := packer(pallet, orderline))[0]), None )
        
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
