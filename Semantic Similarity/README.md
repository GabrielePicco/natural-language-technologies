# Semantic Similarity

In this task we have hand annotated 100 couples of words following these guidelines:
- 4: Very similar -- The two words are synonyms (e.g., midday-noon).
- 3: Similar -- The two words share many of the important ideas of their
meaning but include slightly different details. They refer to similar but not
identical concepts (e.g., lion-zebra).
- 2: Slightly similar -- The two words do not have a very similar meaning,
but share a common topic/domain/function and ideas or concepts that
are related (e.g., house-window).
- 1: Dissimilar -- The two items describe clearly dissimilar concepts, but
may share some small details, a far relationship or a domain in common
and might be likely to be found together in a longer document on the
same topic (e.g., software-keyboard).
- 0: Totally dissimilar and unrelated -- The two items do not mean the
same thing and are not on the same topic (e.g., pencil-frog)

Then, after calculating the senses that maximize the cosine similarity for each pair of terms, we evaluated the obtained results by calculating the accuracy between intended meanings during hand annotation and meanings that maximizes the similarity between pairs of words. Accuracy has been calculated both for individual terms and for term pairs.


## Cosine similarity

In order to compute the similarity between embedded NASARI vectors we used the cosine similarity represented by the following formula:

<img src="https://i.imgur.com/GYUqbNb.png" width="50%">

For this task the cosine similarity has been calculated for each pair of nasari vectors matching the senses of the two term and then we've identified the senses that have maximum similarity.

## Babelnet

Once we got the senses that maximize similarity, we used Babelnet to get their gloss that we used to compute the final accuracy.


## Results

For obtain the final result we hand annotated each term ad pair with "1" if the sense that maximize the similarity is the same we intended during the hand annotation, "0" otherwise. Accuracy has been calculated counting the occurences of "1" annotated term(pair) and dividing them for the total number of annotated term(pair). The final result we obtained calculating is the following:

    Individual term accuracy for user S = 0.7551020408163265
    Pair accuracy for user S = 0.6122448979591837
    Individual term accuracy for user G = 0.7346938775510204
    Pair accuracy for user G = 0.5714285714285714
