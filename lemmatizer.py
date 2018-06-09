import sqlite3
import json

from Text_fixer import TextFixer
LEMMAS_FILENAME = 'lemmas.json'
DB_source = "context.db"


class Lemmatizer:

    def __init__(self, lemmas_filename=LEMMAS_FILENAME):
        self.con = sqlite3.connect(DB_source)
        self.c = self.con.cursor()
        print('Loading dictionary...')
        self.dict_of_words = json.load(open(lemmas_filename))
        print('Dictionary loaded.')
        self.text_fixer = TextFixer()

    def lemmatize(self):
        words_hp, words_nauk, words_pb = self.__read_data_from_db()
        words_hp = [(self.text_fixer.fix(i[0]), self.text_fixer.fix(i[1]))
                    for i in words_hp]
        words_nauk = [(self.text_fixer.fix(i[0]), self.text_fixer.fix(i[1]))
                      for i in words_nauk]
        words_pb = [(self.text_fixer.fix(i[0]), self.text_fixer.fix(i[1]))
                    for i in words_pb]
        print('words loaded')
        lemmas_hp = list()
        for i, words in enumerate(words_hp):
            lemmas_hp.append(list())
            if self.dict_of_words.get(words[0]):
                lemmas_hp[i].append(self.dict_of_words.get(words[0]))
            else:
                lemmas_hp[i].append(self.dict_of_words.get(words[0].lower(), words[0]))
            if self.dict_of_words.get(words[1]):
                lemmas_hp[i].append(self.dict_of_words.get(words[1]))
            else:
                lemmas_hp[i].append(self.dict_of_words.get(words[1].lower(), words[1]))
        print('lemmas hp generated')
        lemmas_nauk = list()
        for i, words in enumerate(words_nauk):
            lemmas_nauk.append(list())
            if self.dict_of_words.get(words[0]):
                lemmas_nauk[i].append(self.dict_of_words.get(words[0]))
            else:
                lemmas_nauk[i].append(self.dict_of_words.get(words[0].lower(), words[0]))
            if self.dict_of_words.get(words[1]):
                lemmas_nauk[i].append(self.dict_of_words.get(words[1]))
            else:
                lemmas_nauk[i].append(self.dict_of_words.get(words[1].lower(), words[1]))
        print('lemmas nauk generated')
        lemmas_pb = list()
        for i, words in enumerate(words_pb):
            lemmas_pb.append(list())
            if self.dict_of_words.get(words[0]):
                lemmas_pb[i].append(self.dict_of_words.get(words[0]))
            else:
                lemmas_pb[i].append(self.dict_of_words.get(words[0].lower(), words[0]))
            if self.dict_of_words.get(words[1]):
                lemmas_pb[i].append(self.dict_of_words.get(words[1]))
            else:
                lemmas_pb[i].append(self.dict_of_words.get(words[1].lower(), words[1]))
        print('lemmas pb generated')
        return (words_hp, words_nauk, words_pb,
                lemmas_hp, lemmas_nauk, lemmas_pb)

    def __read_data_from_db(self) -> list:
        self.c.execute("""
          select word1, word2 from context_hp 
        """)
        words_hp = self.c.fetchall()
        self.c.execute("""
          select word1, word2 from context_nauk 
        """)
        words_nauk = self.c.fetchall()
        self.c.execute("""
          select word1, word2 from context_pb 
        """)
        words_pb = self.c.fetchall()

        return [words_hp, words_nauk, words_pb]

    def insert_lemmas(self, table, words_list, lemmas_list):
        print('{} updating...'.format(table))
        for words, lemmas in zip(words_list, lemmas_list):
            self.c.execute("""
                  UPDATE {} SET lem1="{}", lem2="{}" WHERE word1="{}" AND word2="{}"
            """.format(table, lemmas[0], lemmas[1], words[0], words[1]))


if __name__ == '__main__':
    lemmatizer = Lemmatizer()
    words_hp, words_nauk, words_pb, \
        lemmas_hp, lemmas_nauk, lemmas_pb = lemmatizer.lemmatize()

    lemmatizer.insert_lemmas('context_hp', words_hp, lemmas_hp)
    print('context_hp updated')
    lemmatizer.con.commit()

    lemmatizer.insert_lemmas('context_nauk', words_nauk, lemmas_nauk)
    print('context_nauk updated')
    lemmatizer.con.commit()

    lemmatizer.insert_lemmas('context_pb', words_pb, lemmas_pb)
    print('context_pb updated')
    lemmatizer.con.commit()
