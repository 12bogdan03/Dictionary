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
        words = self.__read_data_from_db()
        words = [self.text_fixer.fix(word) for word in words]
        print('WORDS', len(words))
        lemmas = [self.dict_of_words[x] if self.dict_of_words.get(x)
                  else self.dict_of_words.get(x.lower(), x) for x in words]
        print(len(lemmas))
        return words, lemmas

    def __read_data_from_db(self) -> list:
        self.c.execute("""
          select distinct context_hp.word1 from context_hp 
          union 
          select distinct context_hp.word2 from context_hp
          union 
          select distinct context_nauk.word1 from context_nauk
          union
          select distinct context_nauk.word2 from context_nauk
          union 
          select distinct context_pb.word1 from context_pb
          union 
          select distinct context_pb.word2 from context_pb
          """)
        data = self.c.fetchall()
        words = list(set(j[0]for j in data))
        return words

    def create_table(self):
        self.c.execute("""
                CREATE TABLE IF NOT EXISTS "wforms" (
                    "word" TEXT NOT NULL,
                    "lem" TEXT NOT NULL
                 )
            """)
        self.con.commit()

    def insert_row(self, word, lem):
        self.c.execute("""
              INSERT INTO wforms (word, lem) VALUES ("{}", "{}")
        """.format(word, lem))


if __name__ == '__main__':
    lemmatizer = Lemmatizer()
    list_of_words, list_of_lemmas = lemmatizer.lemmatize()
    lemmatizer.create_table()
    for w, lem in zip(list_of_words, list_of_lemmas):
        print(w, '---', lem)
        lemmatizer.insert_row(w, lem)
    lemmatizer.con.commit()
