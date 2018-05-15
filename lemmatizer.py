import sqlite3
from Text_fixer import TextFixer
LEMMAS_FILENAME = 'dict_corp_lt.txt'
DB_source = "context_hp.db"

class Lemmatizer():

    def __init__(self, lemmas_filename = LEMMAS_FILENAME):
        self.con = sqlite3.connect(DB_source)
        self.c = self.con.cursor()
        print('Loading dictionary...')
        self.dict_of_words = self.__get_dict_of_words(lemmas_filename)
        print('Dictionary loaded.')
        self.text_fixer=TextFixer()


    def lemmatize(self):
        words = self.__read_data_from_db()
        words = [self.text_fixer.fix(word) for word in words]
        print(words)
        print(len(words))
        lemmas = [self.dict_of_words[x] if x in self.dict_of_words.keys() else self.dict_of_words.get(x.lower(), x)  for x in words]


        print(lemmas)
        print(len(lemmas))
        return words, lemmas

        # return lemmas

    def __get_dict_of_words(self, filename: str):
        dict_of_words = dict()
        with open(filename, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            for row in lines:
                row = row.split(' ')
                if len(row) > 1:
                    dict_of_words[row[0]] = row[1]
        return dict_of_words

    def __read_data_from_db(self) -> list:
        self.c.execute("""select distinct bigramhpNunverb.word1 from
                          bigramhpNunverb union select distinct bigramhpNunverb.word2
                        from bigramhpNunverb""")
        data = self.c.fetchall()
        words=list(i[0]for i in data)
        return words
    def create_table(self):
        self.c.execute("CREATE TABLE `wforms` (`word`TEXT,`lem`TEXT);")
        self.con.commit()

    def insert_Row(self,lem, word):
        self.c.execute("INSERT INTO wforms (word,lem) VALUES(?,?) ", (word, lem))
        self.con.commit()

if __name__=='__main__':
    lemmatizer = Lemmatizer()
    list_of_words,list_of_lemmas = lemmatizer.lemmatize()
    # print(len(list_of_lemmas))
    print('Loading lemmmas...')
    lemmatizer.create_table()
    for i,lem in enumerate(list_of_lemmas):
        print(list_of_words[i],lem)
        lemmatizer.insert_Row(lem,list_of_words[i])
