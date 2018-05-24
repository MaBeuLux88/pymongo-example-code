import pymongo
import pymongo.write_concern
import pprint
from argparse import ArgumentParser
import time

if __name__ =="__main__" :

    parser=ArgumentParser()

    parser.add_argument("--host", default="mongodb://localhost:27100/?replicaSet=txntest" , help="MongoDB URI [default: %(default)s]")
    parser.add_argument("--feature_version",help="Server the server featureCompatibilityVersion (also try '4.0' for transactions [default: %(default)s]")

    args=parser.parse_args()

    c=pymongo.MongoClient(args.host)

    doc = c.admin.command( { "getParameter": 1, "featureCompatibilityVersion": 1 })
    print("Old featureCompatibilityVersion: '{}'".format(  doc["featureCompatibilityVersion"]["version"]))

    if args.feature_version:
        c.admin.command( { "setFeatureCompatibilityVersion": args.feature_version} )
        doc = c.admin.command({"getParameter": 1, "featureCompatibilityVersion": 1})
        print("New featureCompatibilityVersion: '{}'".format(  doc["featureCompatibilityVersion"]["version"]))
