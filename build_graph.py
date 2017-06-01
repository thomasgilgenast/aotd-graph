from graph_tool.all import *
from bs4 import BeautifulSoup
import pandas as pd
import requests


DATA_URL = 'https://docs.google.com/spreadsheets/d/1vA8z1uV6LLDmcSYty8toxYGF1ZcYGdnbQoBzuAqb92U/pub?gid=0&single=true&output=csv'
MAX_DEPTH = 1


def explore(g, queue, visited):
    # return if the queue is empty
    if not queue:
        return

    # pick a vertex to explore
    v = queue.pop()

    # short circuit if this vertex is already at MAX_DEPTH
    if g.vp['depth'][v] == MAX_DEPTH:
        return

    # scrape the web
    base_url = 'https://www.youtube.com'
    soup = BeautifulSoup(requests.get(base_url + g.vp['url'][v]).text, 'lxml')

    # iterate over related videos
    for el in soup.findAll('a', {'class': 'content-link'}):
        # if we've been here before, add a new edge
        if el['href'] in visited:
            print('adding edge')
            g.add_edge(v, visited[el['href']])
        elif 'album' in el['title'].lower():
            print('adding node to %s' % el['title'])
            child = g.add_vertex()
            g.vp['url'][child] = el['href']
            g.vp['title'][child] = el['title']
            g.vp['depth'][child] = g.vp['depth'][v] + 1
            g.add_edge(v, child)
            queue.append(child)
            visited[g.vp['url'][child]] = child


def main():
    # parse data
    df = pd.read_csv(DATA_URL, parse_dates=[0])
    df['Date'] = (pd.to_numeric(df['Date']) // int(1e11)).astype(int)

    # set up graph and props
    g = Graph()
    g.vp['url'] = g.new_vertex_property('string')
    g.vp['title'] = g.new_vertex_property('string')
    g.vp['submitter'] = g.new_vertex_property('string')
    g.vp['date'] = g.new_vertex_property('int')
    g.vp['depth'] = g.new_vertex_property('int')

    # set up queue and visited set
    queue = []
    visited = {}

    # populate queue with initial vertices
    for index, row in df.iterrows():
        if row['Link'].startswith('https://www.youtube.com/watch?v='):
            v = g.add_vertex()
            g.vp['url'][v] = row['Link'].split('https://www.youtube.com')[1]
            g.vp['title'][v] = row['Album']
            g.vp['submitter'][v] = row['Selected by']
            g.vp['date'][v] = row['Date']
            g.vp['depth'][v] = 0
            queue.append(v)
            visited[g.vp['url'][v]] = v

    # explore the graph
    while queue:
        explore(g, queue, visited)

    # save to disk
    g.save("aotd.gt")


if __name__ == '__main__':
    main()
