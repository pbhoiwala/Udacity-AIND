import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # DONE implement the recognizer
    x_length_values = test_set.get_all_Xlengths().values()
    for x, lengths in x_length_values:
        scores = {}                             # Dictionary with KEY: word and VALUE: word's score
        max_score = float("-inf")
        best_guess = None
        for word, model in models.items():
            try:
                word_score = model.score(x, lengths)
                scores[word] = word_score
                if word_score > max_score:
                    max_score = word_score
                    best_guess = word
            except Exception as e:
                # print(e)
                scores[word] = float("-inf")
        if best_guess:
            guesses.append(best_guess)
        probabilities.append(scores)

    return probabilities, guesses

