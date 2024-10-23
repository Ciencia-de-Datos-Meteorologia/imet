def plot_points(points,ax,color='black'):
    """
    Plot multiple points and its label

    Parameters
    ----------
    array : list
        List with the coordenate (y,x) and the label. For example [[2,4,'Point A'] , [5,3,'Point B']]
    ax : plt.Axes
        Here's where the points are gonna be drawn.
    color : str, optional
        The color of the points and labels.

    Returns
    -------
    array[2] : str
        The labels introduced
    """

    pad = 0.0085  # Padding for labels

    # Iterate over the list of points
    for point in points:
        # Verify if at least exists a coordenate (y, x) to draw
        if len(point) >= 2:
            # point[0]: Y (coordinate), point[1]: X (coordinate)
            ax.plot(point[1], point[0], 'o', markersize=1, color=color, zorder=8)
            
            # If the list has a third element, it is shown
            if len(point) == 3 and point[2] is not None:
                ax.text(point[1] + pad, point[0] + pad, point[2], color=color, 
                        fontstyle='italic', fontsize=4.5, fontvariant='small-caps', zorder=8)

    # Returns the labels of all points that have them
    return [point[2] for point in points if len(point) == 3 and point[2] is not None]



#This part of the code is executed if 'plot_points.py' is run in the terminal
if __name__=='__main__':
    import matplotlib.pyplot as plt

    #Create a figure and an axis
    fig, ax = plt.subplots()

    #Define a list of points ant their labels
    puntos = [[2, 3, 'Punto A'],[4,2], [2,9,'Punto C']]  # [y, x, etiqueta]

    #Call the function 
    plot_points(puntos, ax, color='blue')

    # Establish the limits of the axis
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)

    # Show the graphic
    plt.show()
