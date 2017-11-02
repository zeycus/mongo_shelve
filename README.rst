========================================
Persistent dictionaries based on mongoDB
========================================

A class :class:`Mongo_shelve` is implemented, that provides a `dict`-like interface for `mongoDB <https://www.mongodb.com>`_ collections.


Motivation
==========

For a long time Python has included the :mod:`shelve` module, an implementation of persistent dictionaries based on :mod:`dbm`, which in turn saves information in local text files. I have used them myself, but for hundreds of thousands of entries performance was far from ideal. Inserting a single new entry would take nearly a second.

A simple test helped me realize that replacing :mod:`shelve` with mongodb speed was about x50 or better for that project [#f1]_.

Another relevant plus is that decent mongoDB servers include safety options, backup systems, etc., so data is safer than in a local file.

Finally, I know pretty much nothing about multi-threading, but it seems mongoDB has a decent support for concurrent access, while I understand :mod:`shelve` has none.


Project Description
===================

A class :class:`Mongo_shelve` is implemented providing a `dict`-like interface for a `mongoDB <https://www.mongodb.com>`_ collection. All usual `dict` operations are supported. On the other hand, powerful interfaces of mongoDB collections like `delete_many` are preserved. See the class documentation for details.

I am currently using Python 3.6 on Windows. I have not tested this code in other versions or platforms.


Warning
=======

To be able to use mongoDB, we must have a connection to a mongoDB server. It could be our own machine, a hosting service, etc. If you are new to mongoDB, several tutorials are available, `this <https://www.hongkiat.com/blog/webdev-with-mongodb-part1/>`_ is one of them. There are also many mongoDB-hosting services that provide free sandboxes with a decent size, no need to spend a dime just to experiment.

If you have mongoDB installed, to serve it locally (in Windows) just run:

.. code:: bash

    mongod.exe --dbpath=<database_path>


Warning regarding tests
=======================

To be able to run tests, we need a mongoDB server to connect to (I know of no better way. If there is, please let me know). The tests are written asumming that a local server is running, building a client that connects to it, creates testing databases/collections, fills them, accesses information stored, and wipe them all in the end.


Usage Example
=============

The example below asummes that a local mongoDB server is running (thus the IP 127.0.0.1) and in the default 27017 port.

.. code:: python

    # Creation of a mongodb client
    import pymongo
    client = pymongo.MongoClient("127.0.0.1:27017")
    db = client['tvs761_hashes']
    col = db['files']  # This is the collection that will be used as dict

    # Creation of the Mongo_shelve instance, choosing 'filename' as look-up field.
    ms = Mongo_shelve(col=col, keyField='filename')

    # Some basic operations
    print("There are %s entries." % len(ms))

    # Insertion of new information
    ms['myBestJoke.txt'] = dict(size=14461)
    print("Info stored: %s" % ms['myBestJoke.txt'])
    print("There are %s entries." % len(ms))

    # Updating information
    ms['myBestJoke.txt'] = dict(size=14732)
    print("Info stored: %s" % ms['myBestJoke.txt'])

    # Deletion
    del ms['myBestJoke.txt']
    print("There are %s entries." % len(ms))

    # Traversing is easy
    for key, data in ms.items():
       print("For key '%s' the information stored is %s" % (key, data))

    # Collection 'delete_many': remove information for files smaller than 1 KB.
    ms.delete_many({'size': {"$lt": 1024}})

    # Delete all entries
    ms.clear()



.. rubric:: Footnotes

.. [#f1] I was using the least refined `dbm.dumb` manager.
   Theoretically, with Berkeley's `dbm.ndbm` or GNU's `dmb.gnu` performance would have been better, but I was unable to install them at the time.

