def print_name(place, ax , color='black'):

    plt.text(place[1], place[2], place[3], fontsize=4.5, transform = ax.transAxes, color=color, va='top', ha='left', fontstyle='italic', fontvariant='small-caps', zorder=8)

    return place[0]