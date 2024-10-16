import shapefile
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
import numpy as np

# draw shapes # correctly draws every part of every shape in a shapefile
# may also fill the shape with color
def plot_shapes(shfile:str, ax:plt.Axes, color:str='black', lw:float=1, ls:str='solid',
                zorder:int=6, fill=False, fcolor:str='black', fzorder:int=3):
    """
        Draw all entries of a shapefile.

        Parameters
        ----------

        shfile : str
            Path to shapefile (.shp or .shx)

        ax : plt.Axes 
            Matplotlib axes object where shapes will be drawn

        color : str
            Color of the lines of the shape

        lw : float
            Line thickness
        
        ls : str
            Line style 

        zorder : int
            Stacking order for lines

        fill : bool
            If True, fill the shape with color

        fcolor : str
            Fill color

        fzorder : int
            Stacking order for filling


        Returns
        --------
        Graphic of the shapefile


        Examples
        ---------
        %Crear la figura y los ejes de Matplotlib

        fig, ax = plt.subplots(figsize=(10, 8))

        %Llamar a plot_shapes con los parámetros adecuados
        
        plot_shapes('/home/rodrigo/Documents/repositorios/gtMapTools/gtMapTools/utilities/maps/america/America.shx', ax, color='blue', lw=0.5, fill=True, fcolor='lightblue')

    """

    # read shapefile
    shapes = shapefile.Reader(shfile)
    # get all shapes
    for shape in shapes.shapeRecords():
        # points in the shape
        points = np.array(shape.shape.points)

        # start points of parts + total number of points
        parts = list(shape.shape.parts)+[len(shape.shape.points)]
        # make interval tuples by pairing (part_i, part_i+1)
        intervals = zip(parts[:-1], parts[1:])

        # draw the shape defined by every interval
        for start, end in intervals:
            # *points gives coordinate pairs
            # zip(*points) gives x and y lists
            x, y = zip(*points[start:end])
            ax.plot(x, y, color=color, lw=lw, zorder=zorder, ls=ls)

            # fill the shape with some color
            if fill:
                ax.fill(x, y, facecolor=fcolor, zorder=fzorder)

    # Show the graphic
    plt.show()



# # Crear la figura y los ejes de Matplotlib
# fig, ax = plt.subplots(figsize=(10, 8))

# # Llamar a plot_shapes con los parámetros adecuados
# plot_shapes('/home/rodrigo/Documents/repositorios/gtMapTools/gtMapTools/utilities/maps/america/America.shx',
#            ax, color='blue', lw=0.5, fill=True, fcolor='lightblue')
