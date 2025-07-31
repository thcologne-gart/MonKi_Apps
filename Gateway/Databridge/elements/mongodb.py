import datetime
import random
import time
import pymongo

class MongoDBHandler:
    mongo_dbs = {}

    @staticmethod
    def get_mongo_db(url: str):
        if url not in MongoDBHandler.mongo_dbs.keys():
            MongoDBHandler.mongo_dbs[url] = MongoDB(url)
        return MongoDBHandler.mongo_dbs[url]

class MongoDB:
    def __init__(self, url: str):
        self.url = url
        self._client = pymongo.MongoClient(self.url)

    def get_databases(self) -> list:
        return self._client.list_database_names()

    def get_database(self, name: str) -> pymongo.database.Database:
        return self._client.get_database(name)

    def get_collection(self, database_name: str, collection_name: str) -> pymongo.collection.Collection | None:
        db = self.get_database(database_name)
        if db is None:
            return None
        return db.get_collection(collection_name)

    def contains_database(self, name: str):
        return name in self.get_databases()

    def contains_collection(self, database_name: str, collection_name: str):
        db = self._client.get_database(database_name)
        return collection_name in db.list_collection_names()


    def insert_time_series_value(self, collection: pymongo.collection.Collection, submodel_name: str, id_short_path: str, datetime: datetime.datetime, value):
        data = {
           "idShortSubmodel": submodel_name,
           "shortIdPath": id_short_path,
           "ts": datetime,
           "value": value
        }
        result = collection.insert_one(data)


    def create_time_series_database_collection(self, database_name: str, collection_name: str):
        db = self._client[database_name]
        timeseries_dict = {'timeField': 'ts', 'metaField': "idShortSubmodel", "metaField": "shortIdPath", 'granularity': 'seconds'}
        col = db.create_collection(collection_name, timeseries=timeseries_dict)








