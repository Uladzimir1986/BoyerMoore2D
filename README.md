# PatternSearch2D
PatternSearch2D counts number of occurrences of specific two-dimensional text pattern in text.

The algorithm is implementation of the idea from paper: "A Boyer-Moore Approach for Two-Dimensional Matching"
https://pdfs.semanticscholar.org/ec0b/8b247b9a6efdbe8b3ddc2e4e3547cecf5223.pdf by  ‪Jorma Tarhio.

This implementation is modified to work with jagged 2D array shapes of pattern and text.
The expected running time of the algorithm is sub-linear for random texts and patterns.

Example:
----------------



    python pattern_search_2D.py -p pattern.txt -t text.txt


Copyright © 2019 Vladimir Vilchinsky
