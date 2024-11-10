# np-no-problem

### run this command in your terminal after cloning the repo
`pip install -r requirements.txt`

1) Keep working on your applications. You probably have the first ideas for tackling the problem, and now it is time to test them out.

2) Smart pre-processing: You saw in today's and last week's lectures that applying a layout algorithm beforehand drastically reduces the overall crossings and will help your algorithms find a good solution for an instance. Apply a layout algorithm as a pre-processing step. For Python, you could try s_gd2, or NetworkX' Kamada-Kawai or SpringEmbedder.
3) 
4) Smart snapping: If you pre-process an instance with a layout algorithm, you will get real coordinates for each vertex. However, the output (and most likely subsequent steps) requires that each vertex is on a position in the grid. Try implementing an algorithm that can take vertices with assigned real coordinates and map them onto the grid position. Furthermore, the grid positions should be valid positions such that no two vertices are assigned to the same position, edges don't pass through vertices, and vertices are placed inside the grid boundary.

5) Try computing a solution for all instances in the small benchmark (benchmark_small.zip) dataset. Prepare your numbers (and maybe a visual proof) for the next lecture. You can find the benchmark dataset on Moodle.



Bonus points:

5) As a second pre-processing strategy, we can check if the graph is planar. Try detecting if a graph is planar and use a planar layout algorithm instead of the strategy used in 2).

6) We added a second benchmark dataset with the instances from the last GD challenge (benchmark_2024.zip). Instances graph1-graph7 are small instances from the manual category. The more interesting instances are graph8-graph15, which are only given for the automatic category. See if your approach can handle the much larger instances and try computing a solution for each. Attention: the json files contain an additional attribute called 'points'. You can ignore this as it was only relevant for the last challenge.
