from graph_tool.all import *


def main():
    g = Graph()
    v1 = g.add_vertex()
    v2 = g.add_vertex()
    e = g.add_edge(v1, v2)

    graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18,
               output_size=(200, 200), output="test.png")


if __name__ == '__main__':
    main()
