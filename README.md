They are three types of methods to create the Networks.

M1: All nodes are already connected and the edges are picked randomly

M2: All nodes are already connected and the edges are picked according to a distribution ('Poisson', 'Normal', 'Uniform' ...) in this case we need a mean for all interactions and the standard deviation for 'Normal' and 'Uniform' interaction

M3: The edges are created with already made networks: 'Erdos-Renyi' need for an extra m parameter m beeing the number of edges
'Small-world' need an extra para k nearest neighbors in ring topology (should not be close to the network siez) and p is float The probability of rewiring each edge
'Regular-lattice' need an extra para k nearest neighbors in ring topology

You can fix memory and agression (so every individual has the same and/or it doesn't evolve through generations)

We can look at evolution through generations. (Plot before refresh if needed)

self.centrality makes sense only in method M3.
