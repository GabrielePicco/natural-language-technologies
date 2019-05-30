# Concept Similarity

Similarity measures are used to calculate the semantic distance between the senses of two terms. In this repository there is an implementation of three metrics: Wu Palmer, Shortest Path and Leacock Chodorow.

## Wu Palmer

Wu Palmer Similarity uses the following formula:
<img src="https://imgur.com/BMj7EK5" width="50%">
LCS is the Lowest Common Subusmer that represent the deepest common ancestor in the taxonomy between two synset.
depth() is the distance from the Wordnet's root to the synset.

In this case the lowest common subsumer is calculate using only the first of the hypernyms of the synset instead of considering the entire list. With this simplification some path might not have been considered.

## Shortest Path

Shortest Path Similarity uses the following formula:
<img src="https://imgur.com/nKtZh8a" width="50%">
depthMax is the longest path from the root of the taxonomy to a leaf and for the given dataset is 12.
len(s1,s2) reresent the shortest path between two senses. The path is calculated together with the LCS keeping track of the path that leads to the lowest common ancestor.

## Leacock Chodorow

Leacock Chodorow Similarity uses the following formula:
<img src="https://imgur.com/wiLah4D" width="50%">
depthMax is the longest path from the root of the taxonomy to a leaf and for the given dataset is 12.
len(s1,s2) reresent the shortest path between two senses. The path is calculated together with the LCS keeping track of the path that leads to the lowest common ancestor.

## Term Similarity
These three metrics show the semantic distance between two senses, to calculate the semantic distance between two terms the maximum similarity between all the senses of the two words was calculated.

## Human annotation and metrics correlations
To calculate the correlation between the results obtained with the three metrics, the Pearson and Spearman indexes were used for each of them. In this case we used the SciPy library obtaining the following results:

Pearson:
    Wu Palmer (correlation=0.18308428587286402, pvalue=0.0005464176617977586)
    Shortest Path (correlation=0.14147208049051546, pvalue=0.007767955350030443)
    Leacock Chodorow (correlation=0.20094674182389424, pvalue=0.00014417361175218793)

Spearman:
    Wu Palmer (correlation=0.31638553337150477, pvalue=1.2006963211619606e-09)
    Shortest Path (correlation=0.2622972821540983, pvalue=5.780063455097429e-07)
    Leacock Chodorow (correlation=0.2622972821540983, pvalue=5.780063455097429e-07)

These results show that the values recorded by hand and the values obtained with the three metrics are not very correlated, in fact if the values obtained with the similarity measurements and the human evaluations are graphically shown, it can be seen that they do not follow the same trend:

Wu Palmer:
<img src="https://imgur.com/uq1njYa" width="50%">

Shortest Path:
<img src="https://imgur.com/Q8qfzUr" width="50%">

Leacock Chodorow:
<img src="https://imgur.com/1GgZL6S" width="50%">
