import psycopg2
import pymongo
import pandas as pd
from datetime import datetime

class PostgreSQLDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='scrapydb',
            user='scrapyuser',
            password='scrapypassword',
            host='postgres'
        )
        self.cur = self.conn.cursor()

    def fetch_all(self):
        self.cur.execute('SELECT * FROM raw_table')
        rows = self.cur.fetchall()
        columns = [desc[0] for desc in self.cur.description]
        return pd.DataFrame(rows, columns=columns)

    def to_csv(self, file_path):
        df = self.fetch_all()
        df.to_csv(file_path, index=False)

    def close_connections(self):
        self.cur.close()
        self.conn.close()

class MongoDBDatabase:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:example@mongodb:27017/')
        self.db = self.client['scrapydb']
        self.collection = self.db['raw_collection']

    def fetch_all(self):
        data = []
        for doc in self.collection.find():
            data.append(doc)

        df = pd.DataFrame(data)
        
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])

        for col in df.columns:
            if df[col].apply(lambda x: x[0]=='[' and x[-1]==']').any():
                df[col] = df[col].apply(lambda x: x[1:-1] if (x[0]=='[' and x[-1]==']') else x)

        for col in df.columns:
            if df[col].apply(lambda x: x[0]=="'" and x[-1]=="'").any():
                df[col] = df[col].apply(lambda x: x[1:-1] if (x[0]=="'" and x[-1]=="'") else x)

        return df

    def to_csv(self, file_path):
        df = self.fetch_all()
        df.to_csv(file_path, index=False)

    def close_connections(self):
        self.client.close()

if __name__ == '__main__':
    postgres_db = PostgreSQLDatabase()
    postgres_db.to_csv('/app/data/postgres_data.csv')
    postgres_db.close_connections()

    mongo_db = MongoDBDatabase()
    mongo_db.to_csv('/app/data/mongodb_data.csv')
    mongo_db.close_connections()