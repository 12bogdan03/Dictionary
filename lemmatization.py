import json

lemmas_dict = json.load(open('lemmas.json'))

# print('LEMM ', len(set(lemmas_dict.values())))
# print('WORDS ', len(set(lemmas_dict.keys())))


def get_lemma(word):
    return lemmas_dict.get(word, word)


# class Lemmatizer:
#     lemmas_dict = json.load(open('lemmas.json'))
#
#     def lemma(self, word):
#         return self.lemmas_dict.get(word)
