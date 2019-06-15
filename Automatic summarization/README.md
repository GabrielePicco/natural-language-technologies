# Automatic Summarization

Automatic summarization is the process of shortening a text document with software, in order to create a summary with the major points of the original document.

In this repository there is an implementation of an extraction-based summarization algorithm. n particular, the approach used is based on the cohesion method.

## Cohesion calculation

Cohesion is calculated by adding the internal cohesion between each paragraph (or sentence depending on the selected granularity) to each other.

Internal cohesion is calculated by preprocessing the paragraphs or sentences in a dictionary composed of the words and the frequencies in which they appear. The pre-processing phase removes the punctuation and invalid characters, carries out the part of speech and lemmatizes the words.  Then the similarity between each combination of words in the two segments is calculated and multiplied by the frequencies.

The similarity between two words is calculated using the following formula:

<img src="https://i.imgur.com/wdlEj3u.png" width="50%">

Where WO corresponds to the square-rooted weighted overlap vector comparison

<img src="https://i.imgur.com/BATU32r.png" width="50%">


For the calculation of the similarity between two words, the list of [nasari](http://lcl.uniroma1.it/nasari/) vectors (with lexical representation) related to the lemmas is identified and the maximum value of WO given by the combinations of the comparisons of the vectors is used.

## Content Selection


Each paragraph or sentence is sorted according to the calculated cohesion value. Furthermore an increase of the cohesion value is applied in the case in which the comparison was made with the title (to highlight the fact that the content that is cohesive with the title is probably relevant)

A percentage (method input) of the section according to the sort is then selected.

## Information Ordering & Sentence Realisation

The sorting of the output sections respects the original order within the text. The hypothesis is that the order of a text is in some way relevant to the presentation of the content. The summarizer therefore eliminates the less relevant information, while maintaining the original order of the text.


## Run the summarizer

The core algorithms are contained in the Summarizer class, inside the automatic_summarizer.py script. 

In particular it is possible to summarize a document in the following way:

    summarizer = Summarizer(nasari_file_path=NASARI_PATH)
    summarizer.summarize_document(document_path, percentage=0.3, granularity=Granularity.PARAGRAPH)
    
Furthermore it is possible to summarize a document using the sentences as granularity of the calculation of the cohesion value

    summarizer = Summarizer(nasari_file_path=NASARI_PATH)
    summarizer.summarize_document(document_path, percentage=0.3, granularity=Granularity.SENTENCE)
    
Below is an example of a summary with 30% selection percentage and granularity at the sentence level

Original Text:

    Donald Trump vs Barack Obama on Nuclear Weapons in East Asia

    Donald Trump broke a lot of foreign-policy crockery last week.
    President Barack Obama dressed him down for encouraging South Korea and Japan to acquire nuclear weapons.
    NATO’s secretary-general, Jens Stoltenberg, has criticized him too.
    Academics trying to parse Mr. Trump’s statements can’t figure out which “school” of foreign-policy thinking he belongs to. 
    (So far, my favorite scholarly comment has been: “There is no indication that Trump understands the workings of balance of power theory…” Of course, there is no indication that Mr. Trump cares about the workings of any theories—and no real danger that he subscribes to them.)
    The candidate’s set-to with the president, however, was far from frivolous.
    Mr. Trump suggested that, if South Korea and Japan had nuclear weapons, we could spend less protecting those allies.
    This approach, Mr. Obama rejoined, would reverse decades of U.S. policy on nuclear proliferation. 
    (One of the president’s aides said it would be “catastrophic.”) The president was particularly indignant after the success of last week’s Nuclear Security Summit—at which he got Poland and Kazakhstan to agree to reduce their stockpiles of enriched uranium, Japan to ship out some separated plutonium, and other participants to tighten up a treaty on securing nuclear materials.
    These were worthy achievements. 
    Yet Mr. Trump has—okay, maybe unwittingly—highlighted a question about the entire non-proliferation enterprise that is at least as important as anything that happened at Mr. Obama’s summit.
    In the half-century since the nuclear Non-Proliferation Treaty was negotiated, no state has gotten nuclear weapons because materials for doing so were inadequately secured. 
    For all new nuclear powers (and those countries that decided not to go nuclear, such as Germany, Ukraine, and South Africa), the decisive factor was how they saw the main threats to their own security.
    Mr. Trump is right about one thing: The big question raised by North Korea’s success in building a nuclear arsenal is whether South Korea and Japan feel obliged to follow suit.
    There is a terrible irony in thinking through how to avoid this result.
    Only one country—China—may be able to get the North Koreans to change course. Beijing’s record on this issue, while improving, remains inadequate.
    China has usually failed to deliver the pressure it promises. 
    Yet there is one thing that might get Beijing to do better: the Trumpian prospect that Seoul and Tokyo will decide to become nuclear powers. No U.S. president should want them to do so—or take for granted that he or she could stop them.
    China needs to reckon with, and be reminded of, the enormous danger it is courting.
    Whatever he understands about the workings of balance-of-power theory, Donald Trump has provided one such reminder. He may do more good than he knows.
    
Summarized Text:

    Donald Trump vs Barack Obama on Nuclear Weapons in East Asia

    Donald Trump broke a lot of foreign-policy crockery last week.
    (So far, my favorite scholarly comment has been: “There is no indication that Trump understands the workings of balance of power theory…” Of course, there is no indication that Mr. Trump cares about the workings of any theories—and no real danger that he subscribes to them.)
    Mr. Trump suggested that, if South Korea and Japan had nuclear weapons, we could spend less protecting those allies.
    Yet Mr. Trump has—okay, maybe unwittingly—highlighted a question about the entire non-proliferation enterprise that is at least as important as anything that happened at Mr. Obama’s summit.
    Mr. Trump is right about one thing: The big question raised by North Korea’s success in building a nuclear arsenal is whether South Korea and Japan feel obliged to follow suit.
    Whatever he understands about the workings of balance-of-power theory, Donald Trump has provided one such reminder.

