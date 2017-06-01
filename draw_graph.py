from graph_tool.all import *
import numpy as np
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def map_categorical_to_int(g, source):
    categories = g.vp[source].get_2d_array([0])
    unique_categories = np.unique(categories)
    reverse_map = {unique_categories[i]: i / len(unique_categories)
                   for i in range(len(unique_categories))}
    vp = g.new_vertex_property('float')
    map_property_values(g.vp[source], vp, lambda x: reverse_map[x])
    return vp, reverse_map


def add_legend(color_dict, cmap=None):
    legend_labels = color_dict.keys()
    legend_handles = [mpatches.Patch(color=color_dict[l] if cmap is None
                                     else cmap(color_dict[l]))
                      for l in legend_labels]
    plt.legend(legend_handles, legend_labels, scatterpoints=1, loc='upper left',
               bbox_to_anchor=(1, 1.05))


def main():
    g = load_graph('aotd.gt')
    pos = sfdp_layout(g)
    vcmap = matplotlib.cm.jet
    submitter_colors, reverse_map = map_categorical_to_int(g, 'submitter')
    graph_draw(g, pos, vertex_fill_color=submitter_colors, vcmap=vcmap,
               mplfig=plt.gcf())
    add_legend(reverse_map, cmap=vcmap)
    plt.axis('off')
    plt.savefig('aotd.svg', bbox_inches='tight')


if __name__ == '__main__':
    main()
