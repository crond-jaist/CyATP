
# Training Content Guide

This file contains information about the training content included
with CyATP, as well as details about the procedure of generating
training content. The generated training concept is stored partially
in the Neo4j database (keywords and concept map) and partially in a
JSON file named `data/DATA_6_KLTQCP.json` (concept definitions and
quiz questions).


## Included Training Content

CyATP includes training content that was generated using the
methodology outlined in the figure below, as follows:
* 2640 cybersecurity concepts extracted from DBpedia by using
  "computer security" as keyword
* 2315 concept definitions extracted from Wikipedia for the above
  concepts (when available)
* 278 quiz questions and 28 crossword puzzle clues (for the 126 concepts on the 0-2 level) created using Natural
  Language Generation (NLG) techniques

<div align=center><img src='https://github.com/blab-private/CyATP/blob/master/static/images/training_content_overview.png'></div>


## Training Content Generation

The generation of new/updated training content requires generating the
following three types of data, as it will be described below in
detail:
* Concept data
* Quiz data
* Crossword puzzle

### Concept Data

Concept data is created by extracting keywords from the Linked Open
Data (LOD) database DBpedia (see [this
paper](http://hdl.handle.net/10119/15928) for details), then
extracting definitions of those concepts from Wikipedia. To change the
search keyword from "computer security" to something else, modify the
value of the variable `keyword` located at the end of the file
`training_content/generate_content/generate_learning_content_data.py`,
then run that file to generate the new concept data file.

### Quiz Data

To generate quiz question data, we trained the Naive Bayes Model using
the [SQuAD v1.1](https://rajpurkar.github.io/SQuAD-explorer/) dataset,
then used the trained model to predict questions based on the concept
definitions text. Finally, used the
[GENSIM](https://radimrehurek.com/gensim/) library is used to generate
the proposed choices for each quiz question.

To regenerate quiz question data if concept data was changed/updated,
follow the following steps:

1. Extract the model file archive `CyATP_LargeFiles` provided as asset with the
CyATP release into the directory
`training_content/generate_content/generate_quiz/` inside the CyATP
folder.

2. Install the additional third-party Python libraries that are
required to run the models; these dependencies are specified in the
file
`training_content/generate_content/generate_quiz/requirements.txt`.

3. Run the following command to generate the quiz data:
   ```
   $ python main-GQ.py
   ```

**NOTES**
* If you want to save the quiz data in a file with a name different
than the default, modify the parameter `text_data` in the file
`main-GQ.py` to be the desired name of the data file.
* If you also want to retrain the Naive Bayes Model, make sure to
place it in the file named
`training_content/generate_content/generate_quiz/Trained_Models/M_BernoulliNB+isotonic_smote.pkl`.

### Crossword Puzzle

To generate the crossword puzzle, keywords that have clues are
extracted from the JSON data and the script
`training_content/generate_content/generate_cross.py` is used to
generate the puzzle. To alter the input for the crossword puzzle
generation, you can modify the parameter `All_data` in the mentioned
file to include your own.


## Database Update

Part of the generated training content needs to be put in the Neo4j
database for performance reasons, so that the concept keywords and the
relationship between them (concept map) can be queried fast. The
necessary data is saved in the file `data/create_map.txt` when concept
data is generated, and can be loaded into the CyATP Neo4j database
file using the script `neo_db/create_graph.py`. The actual Ne4j
database must then be updated as described at step "3. Set up the
Neo4j database" of the `README.md` file.

If you want to change the update the content yourself, pay attention
to the structure of the concept map data stored in the file
`create_map.txt`. Thus, the 1st and 2nd fields contain the start and
end concepts, respectively; the 3rd field contains the concept
relationship; finally, the 4th and 5th fields contain the levels on
which the start and end concepts are located, respectively.


## File Overview

The CyATP release contains a large number of files, and we provide an
overview below to facilitate development and further extensions of
CyATP.
```
├── data                            # Directory for training data
│   ├── DATA_6_KLTQCP.json          # Pre-generated training dataset
│   ├── concept_map.json            # Concept map data
│   ├── concept_text.json           # Concept text data
│   ├── create_map.txt              # Keywords and relationships
│   ├── crossword_puzzle_data.json  # Crossword puzzle data
├── neo_db                          # Directory for Neo4j related data
│   ├── config.py                   # Script to configure the database
│   ├── create_graph.py             # Script to create the database
│   ├── cyatp.db                    # Pre-generated database file
│   └── query_graph.py              # Script to query the database
├── scripts                         # Directory for other scripts
│   ├── get_cross.py                # Script to get crossword puzzle
│   ├── get_5_data.py               # Script to get information from dataset
│   ├── save_feedback.py            # Script to save trainee feedback
│   └── show_profile.py             # Script to show concept text
├── static                          # Directory for static web files
├── templates                       # Directory for HTML web files
├── training_content                # Directory for content generation
│   ├── feedback                    # Directory for storing trainee feedback
│   ├── generate_content            # Directory for generation scripts
└── └── training_content_guide.md   # Training content generation guide
```

### Question Feedback

When you are taking a quiz, you will see a button name "Question
Evaluation" in the bottom-right corner. Using this button, trainees
can provide feedback about the quality of a quiz question at any
time. This feedback data is saved in the file named
`training_content/feedback/feedback_question.json`.

### Survey Data

The CyATP website includes a **Survey** page on which we use the
[System Usability Scale
(SUS)](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html)
method to evaluate the CyATP platform. The survey data is saved in the
file `training_content/feedback/feedback_survey_data.json`.
