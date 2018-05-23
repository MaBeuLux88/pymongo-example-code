"""
Program to demon Transactions in MongoDB 4.x.

@Author: Joe.Drumgoole@mongodb.com

"""
from argparse import ArgumentParser
from datetime import datetime
import time
import sys
import random
import pymongo


def txn_sequence(seats, payments, seat_no, delay, session=None):
    price=500
    seat_str = "{}A".format(seat_no)
    print( "Booking seat: '{}'".format(seat_str))
    seats.insert_one({"flight_no": "EI178", "seat": seat_str, "date": datetime.utcnow()}, session=session)
    if delay > 0 :
        delay_period = random.uniform(0, delay)
        print( "Sleeping: {}".format(delay_period))
        time.sleep(delay_period)
    payments.insert_one({"flight_no": "EI178", "seat" : seat_str, "date": datetime.utcnow(), "price": price},session=session)
    print( "Paying {} for seat '{}'".format(price, seat_str))


if __name__ == "__main__" :

    parser=ArgumentParser()
    parser.add_argument("--host", default="mongodb://localhost:27017/?replicaSet=txntest" , help="MongoDB URI [default: %(default)s]")
    parser.add_argument("--usetxns", default=False, action="store_true", help="Use transactions [default: %(default)s]")
    parser.add_argument("--delay", default=1.0, type=float, help="Delay between two insertion events [default: %(default)s]")
    parser.add_argument("--iterations", default=3, type=int, help="Run  %(default)s iterations" )
    args = parser.parse_args()

    client = pymongo.MongoClient( host=args.host)
    database = client["PYTHON_TXNS_EXAMPLE"]
    payments_collection = database[ "payments"]
    seats_collection = database[ "seats"]
    print( "using collection: {}.{}".format(database.name, seats_collection.name))
    print( "using collection: {}.{}".format(database.name, payments_collection.name))

    server_info = client.server_info()
    major_version= int(server_info[ 'version'].partition( ".")[0])
    if major_version < 4 :
        print( "The program requires MongoDB Server version 4.x or greater")
        print( "You are running: mongod '{}'".format(server_info[ 'version']))
        print( "get the latest version at https://www.mongodb.com/download-center#community")
        sys.exit(1)

    #book a flight, assume currency is dollars


    for i in range(1,args.iterations+1):
        if args.usetxns:
            print( "Using transactions")
            with client.start_session() as s:
                with s.start_transaction():
                    txn_sequence(seats_collection, payments_collection, i, args.delay, s)

        else:
            txn_sequence(seats_collection, payments_collection, i, args.delay)


