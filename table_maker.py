import sqlite3

class Context_DB:

    def __init__(self, main_db_source, db_hp_1, db_hp_2,db_hp_3, db_pb,db_nauk):
        self.con = sqlite3.connect(main_db_source)
        self.c = self.con.cursor()

        self.con_hp_1 = sqlite3.connect(db_hp_1)
        self.c_hp_1 = self.con_hp_1.cursor()

        self.con_hp_2 = sqlite3.connect(db_hp_2)
        self.c_hp_2 = self.con_hp_2.cursor()

        self.con_hp_3 = sqlite3.connect(db_hp_3)
        self.c_hp_3 = self.con_hp_3.cursor()

        self.con_pb = sqlite3.connect(db_pb)
        self.c_pb = self.con_pb.cursor()

        self.con_nauk = sqlite3.connect(db_nauk)
        self.c_nauk= self.con_nauk.cursor()

    def select_row_hp(self):
        self.c_hp_1.execute("select * from bigramhpNunverb")
        data = self.c_hp_1.fetchall()
        self.c_hp_2.execute("select * from bigramhpNunverb")
        data += self.c_hp_2.fetchall()
        self.c_hp_3.execute("select * from bigramhpNunverb")
        data += self.c_hp_3.fetchall()
        print(len(data))
        return data

    def select_row_pb(self):
        self.c_pb.execute("select * from bigrampublNunverb")
        data = self.c_pb.fetchall()
        return data

    def select_row_nauk(self):
        self.c_nauk.execute("select * from bigramnaukNunverb")
        data = self.c_nauk.fetchall()
        return data

    def insert_Row_hp(self,word1, code, word2, frequency):
        print("Loading HP...")
        self.c.execute("INSERT INTO context_hp (word1, code, word2, frequency) VALUES (?,?,?,?)", (word1, code, word2, frequency))
        self.con.commit()

    def insert_Row_pb(self,word1, code, word2, frequency):
        print("Loading PUBL...")
        self.c.execute("INSERT INTO context_pb (word1, code, word2, frequency) VALUES (?,?,?,?)",
                       (word1, code, word2, frequency))
        self.con.commit()

    def insert_Row_nauk(self, word1, code, word2, frequency):
        print("Loading NAUKA....")
        self.c.execute("INSERT INTO context_nauk (word1, code, word2, frequency) VALUES (?,?,?,?)",
                       (word1, code, word2, frequency))
        self.con.commit()

if __name__=='__main__':
    main_db_source = "context.db"
    db_hp_1 = "context_hp_1.db"
    db_hp_2 = "context_hp_2.db"
    db_hp_3 = "context_hp_3.db"
    db_pb = "context_pb.db"
    db_nauk = "context_nauk.db"
    db=Context_DB(main_db_source, db_hp_1, db_hp_2, db_hp_3, db_pb, db_nauk)

    hps = db.select_row_hp()
    for hp in hps:
        db.insert_Row_hp(hp[0], hp[1], hp[2], hp[3])

    pbs = db.select_row_pb()
    for pb in pbs:
        db.insert_Row_pb(pb[1], pb[2], pb[3], pb[4])

    nauks = db.select_row_nauk()
    for nauk in nauks:
        db.insert_Row_nauk(nauk[1],nauk[2],nauk[3],nauk[4])

