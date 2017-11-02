#!/usr/bin/python 3.5

from unittest import TestCase
import pymongo

import mongo_shelve


# *********** Constants ***********

CLIENT_ADDRESS = "127.0.0.1:27017"
TESTING_DB = "testing_mongoshelve"
TESTING_COL = "collec"
KEYFIELD = "key_field"


# *********** Functions ***********

def getTestingClient():
    try:
        client = pymongo.MongoClient(CLIENT_ADDRESS)
        client[TESTING_DB].collection_names(include_system_collections=False)  # Just testing if it works
        return client
    except:
        raise ConnectionRefusedError("The connection to mongo_shelve testing client '%s' failed. See the project's documentation.")


class TestMongo_shelve(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a Mongo_shelve cls.ms to be tested.
        cls.cli = getTestingClient()
        cls.cli.drop_database(TESTING_DB)  # Delete the database in case it exists
        cls.db = cls.cli[TESTING_DB]
        cls.col = cls.db[TESTING_COL]
        cls.ms = mongo_shelve.Mongo_shelve(cls.col, KEYFIELD)


    @classmethod
    def tearDownClass(cls):
        cls.cli.drop_database(TESTING_DB)


    def testBasicOperations(self):
        """Basic operations work"""
        self.col.delete_many({})
        self.assertEqual(len(self.ms), 0)  # Make sure there are no entries

        data = (
            ('Ann', dict(age=23, height=158)),
            ('John', dict(age=21, height=172)),
            ('Helen', dict(age=44, height=168)),
        )

        # Inserting and accessing
        for key, value in data:
            self.ms[key] = value
            self.assertDictEqual(self.ms[key], value)  # Check values are properly inserted
        self.assertEqual(len(self.ms), len(data))

        # Modification
        for key, value in data:
            value['age'] += 1
            self.ms[key] = value
            self.assertDictEqual(self.ms[key], value)  # Check values are properly inserted

        # Deletion
        for key, _ in data:
            del self.ms[key]
            with self.assertRaises(KeyError) as context:
                self.ms[key]
            self.assertIn("Key '%s' not found" % key, str(context.exception))

        self.assertEqual(len(self.ms), 0)  # Make sure there are no entries left


    def testDelete_many(self):
        """Mongo wrapper 'remove' works"""
        # Insert a few values
        self.col.delete_many({})
        data = (
            ('Ann', dict(age=23, height=158)),
            ('John', dict(age=21, height=172)),
            ('Helen', dict(age=44, height=168)),
        )
        for key, value in data:
            self.ms[key] = value

        # Perform a removal
        self.ms.delete_many({'age': {'$gt': 22}})  # Remove records with age > 22

        # Check that only the proper entries remain
        self.assertEqual(
            set(name for (name, info) in data if info['age'] <= 22),
            set(self.ms),
        )
