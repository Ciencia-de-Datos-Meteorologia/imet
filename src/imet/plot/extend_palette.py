import matplotlib as mpl
import numpy as np

def colorFader(c1,c2,mix=0): 
    """
    Fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)

    Parameters
    ----------
    c1 : str
        Color 1, it can be by name (red), hexadecimal (FF0000) or RGB (1,0,0)
    c2 : str
        Color 1, it can be by name (blue), hexadecimal (0000FF) or RGB (0,0,1)
    mix : int, optional
        How close of far is the new color to c1 or c2, by default 0

    Returns
    -------
    str
        Hexadecimal code of the color
    """
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))

    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)




def extend_palette(palette:list,amnt:int,dir:str):
    """
    

    Parameters
    ----------
    palette : list
        The palette of colors you want to extend. It can be RGB, name or hexadecimal
    amnt : int
        Amount of subdivisions to add between each pair of consecutive boundaries.
    dir : str, {'max', 'min', 'both', 'neither'}
        Add extra bound for arrow-shape at ends of colorbar. 
    """

    ret = []
    colorsamnt = len(palette)

    if dir == 'max':
        for i in range(colorsamnt-1):
            c1,c2 = palette[i],palette[i+1]
            for j in range(amnt):
                ret.append(colorFader(c1,c2,j/amnt))

        ret.append(palette[-1])

    elif dir == 'min':
        palette.reverse()
        for i in range(colorsamnt-1):
            c1,c2 = palette[i],palette[i+1]
            for j in range(amnt):
                ret.append(colorFader(c1,c2,j/amnt))
        
        ret.append(palette[-1])

        ret.reverse()
    
    elif dir == 'both' or dir == 'neither':

        below = None
        above = None


        if colorsamnt%2 == 0:
            half = int(colorsamnt/2)
            below = palette[:half]
            above = palette[half:]
        else:
            half = int((colorsamnt+1)/2)
            below = palette[:half]
            above = palette[half-1:]

        # below:
        below.reverse()
        for i in range(len(below)-1):
            c1,c2 = below[i],below[i+1]
            for j in range(amnt):
                ret.append(colorFader(c1,c2,j/amnt))
        
        ret.append(below[-1])

        ret.reverse()

        if colorsamnt%2:
            ret.remove(ret[-1])

        # above:
        for i in range(len(above)-1):
            c1,c2 = above[i],above[i+1]
            for j in range(amnt):
                ret.append(colorFader(c1,c2,j/amnt))

        ret.append(above[-1])

    # if amnt != 1:
    #     ret.append(palette[-1])

    # print(ret)

    return(ret)


if __name__=='__main__':
    print(extend_palette(['red','blue','green'],5,'max'))   