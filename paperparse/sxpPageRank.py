#-------------------------------------------------------------------------------
# Name:        sxpPageRank
# Purpose:
#
# Author:      sunxp
#
# Created:     04/05/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def pagerank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph.

    @type  graph: digraph
    @param graph: Digraph.

    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.

    @type  max_iterations: number
    @param max_iterations: Maximum number of iterations.

    @type  min_delta: number
    @param min_delta: Smallest variation required to have a new iteration.

    @rtype:  Dict
    @return: Dict containing all the nodes PageRank.
    """

    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    min_value = (1.0-damping_factor)/graph_size #value for nodes without inbound links

    # itialize the page rank dict with 1/N for all nodes
    pagerank = dict.fromkeys(nodes, 1.0/graph_size)

    for i in range(max_iterations):
        diff = 0 #total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            for referring_page in graph.incidents(node):
                rank += damping_factor * pagerank[referring_page] / len(graph.neighbors(referring_page))

            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        #stop if PageRank has converged
        if diff < min_delta:
            break

    return pagerank
def main():
    pass

if __name__ == '__main__':
    main()
