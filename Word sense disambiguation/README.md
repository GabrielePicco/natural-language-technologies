# Word Sense Disambiguation

In computational linguistics, word-sense disambiguation (WSD) is an open problem concerned with identifying which sense of a word is used in a sentence. The solution to this problem impacts other computer-related writing, such as discourse, improving relevance of search engines, anaphora resolution, coherence, inference.

This repository contains the implementation of the Lesk algorithm proposed for disambiguation. Using Wordnet as a semantic-lexical resource, synonyms, definitions and examples are extracted, using them to select the synset with maximum intersection value given a context.

The project consists of two main experiments:

- [Disambiguation of a set of example sentences and generation of equivalent sentences](##Disambiguation-of-a-set-of-example-sentences-and-generation-of-equivalent-sentences)
- [Accuracy on the first 50 sentences of SemCor](##Accuracy-on-the-first-50-sentences-of-SemCor)

## Disambiguation of a set of example sentences and generation of equivalent sentences

The example sentences for disambiguation are contained in the file data/sentences.txt
Each sentence contains within it a polysemic word, identified by the \*\*word\*\* pattern.

Executing the script:

    word_disambiguation.py

The ambiguous words are extracted from the sentences and the Lesk algorithm is executed to find the most appropriate synset.

The disambiguation context is created by normalizing the input sentence, ie by removing uppercase and punctuation and generating a list of words.

Then the method contained in *word_disambiguation_utils.py* is used to generate alternative sentences given the synset and the ambiguous word: 

    generate_alternative_sentence(sentence, ambiguous_word, syn)
    
The method retrieves the lexemes of the synset and replaces them with the ambiguous word, correctly setting the plural and the capital letters (if present in the original word).

Some examples are provided below:

    Sentence: **Arms** bend at the elbow.

    Syn: Synset('sleeve.n.01')
    
    Syn Definition: the part of a garment that is attached at the armhole and that provides a cloth covering for the arm
    
    Alternatives sentences:
    Sleeves bend at the elbow.
    
'

    Sentence: The **key** problem was not one of quality but of quantity.
    
    Syn: Synset('cardinal.s.01')
    
    Syn Definition: serving as an essential component
    
    Alternatives sentences:
    
    The central problem was not one of quality but of quantity.
    The cardinal problem was not one of quality but of quantity.
    The primal problem was not one of quality but of quantity.
    The fundamental problem was not one of quality but of quantity.

## Accuracy on the first 50 sentences of SemCor
    
To verify the performance of the model the accuracy metrics is calculated using the semantically annotated corpus SemCor (using the first 50 sentences).

To compute the accuracy, the first noun is selected in the 50 sentences and the identifier of the correct Wordnet synset memorized. Then the know true synset is compared with the result of the Lesk algorithm executed on the same sentence and ambiguous word.

Below are the accuracies on the same set of data, but using different contexts to disambiguate. The following options for creating a synset context will be evaluated:

- Gloss of the synset
- Definition of the synset
- Examples of the synset

The following are the relative accuracy values:


    Only Gloss: 0.36
    Only Definition: 0.54
    Only Examples: 0.42
    
The decomposition allows to identify the relative contribution to the disambiguation, but the best accuracy is achieved by creating the context using all the properties of the sysnset:    

    Gloss + definition + examples: 0.62