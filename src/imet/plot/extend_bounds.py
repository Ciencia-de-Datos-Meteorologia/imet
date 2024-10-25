def bound_Fader(n1 , n2 , mix=0):
    """
    Fade (linear interpolate) from number n1 (at mix=0) to n2 (mix=1)

    Parameters
    ----------
    n1 : float
        Number 1
    n2 : float
        Number 2
    mix : float, optional
        How close the n1 is to n2
    """

    if mix<0 or mix>1:
        raise ValueError('mix out of rage [0,1]')
    
    return (1-mix)*n1 + mix*n2

def extend_bounds(bounds , amnt , dir , palette_len):

    """
    Extends a list of bounds.

    Parameters
    ----------
    bounds : list
        List of original bounds
    amnt : int
        Number of subdivisions to add between each pair of consecutive boundaries.
    dir : str, {'max', 'min', 'both', 'neither'}
        Add extra bound for arrow-shape at ends of colorbar. 
    palette_len : int
        Length of accompanying palette.

    Returns
    --------
    list 
        Extended bounds list
    """
    
    #Return list
    ret = []

    #Create new bounds
    for i in range(len(bounds)-1):
        #New bounds will be created between adjacent original bounds
        n1, n2 = bounds[i], bounds[i+1]
        #Make the desired number of new bounds
        for j in range(amnt):
            ret.append(bound_Fader(n1,n2,j/amnt))

    #Finish it up with last original bound
    ret.append(bounds[-1])

    #Cutoff
    cutoffamnt = amnt-1

    if cutoffamnt != 0:
        #cutting for extensions conditions
        if dir == 'max':
            if palette_len < len(ret):
                ret = ret[:-cutoffamnt]

        elif dir == 'min':
            if palette_len < len(ret):
                ret = ret[cutoffamnt:]

        elif dir == 'both' or dir == 'neither':
            if palette_len <= len(ret):
                ret = ret[cutoffamnt:-cutoffamnt]

    return ret


#This is just a test to check 
if __name__=='__main__':
    bounds = [0,10,20,30]
    amnt = 5
    palette_len = 3

    print('Prueba 1: ', extend_bounds(bounds,amnt,'max',palette_len))