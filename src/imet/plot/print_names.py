import matplotlib.pyplot as plt

def print_names(places, ax , color='black'):
    """
    Print label at particular location in map

    Parameters
    ----------
    place : list
        The lsit estructure is [name , coord_x , coord_y , text]
    ax : plt.Axes
        Here's where the text is gonna be written
    color : str, optional
        _description_, by default 'black'

    Returns
    -------
    list
        list with the name of the places
    """

    # Iterate over the list 'places'
    for place in places:
        # place is a list [name, coord_x, coord_y, text]
        plt.text(place[1], place[2], place[3], fontsize=4.5, transform=ax.transAxes,
                 color=color, va='top', ha='left', ma='left', fontstyle='italic',
                 fontvariant='small-caps', zorder=8)
    
    # Retorn a list with the name of places
    return [place[0] for place in places]




#This part of the code is executed if 'print_names.py' is run in the terminal
if __name__ == '__main__':

    #Create a figure and an axis
    places = [
    ["lugar_1", 0.2, 0.8, "Etiqueta 1"],
    ["lugar_2", 0.5, 0.5, "Etiqueta 2"],
    ["lugar_3", 0.7, 0.3, "Etiqueta 3"]
    ]

    fig, ax = plt.subplots()  
    print_names(places, ax, color='blue')  # Colocar las etiquetas en el gráfico
    plt.show()  # Mostrar el gráfico