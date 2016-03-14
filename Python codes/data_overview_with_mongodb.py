#Connect to mongod instance
client=MongoClient('mongodb://localhost:27017/')

#Use OSM database
db=client.OSM

#In database use AnkaraOSM collection and find the number of documents, nodes, ways and unique users
docs=db.AnkaraOSM.find().count()
nodes=db.AnkaraOSM.find({"type":"node"}).count()
ways=db.AnkaraOSM.find({"type":"way"}).count()
un_users=len(db.AnkaraOSM.distinct("created.user"))

print "### DOCUMENTS, NODES, WAYS AND UNIQUE USERS ###\n"
print "\tNumber of documents:    ", docs
print "\tNumber of nodes:        ", nodes
print "\tNumber of ways:         ", ways
print "\tNumber of unique users: ", un_users
#Find top 10 contributing users
#This code queries the dataset and displays some basic statistics
from pymongo import MongoClient

def top(items,name,number):
    #This function displays the given data
    i=1
    print "\n\t### TOP ",number," ",name.upper()," ###\n"
    for item in items:
        print "\t",i,". ", item["_id"]," ", item["count"]
        i+=1

contrib= db.AnkaraOSM.aggregate([
        {'$group':{'_id':'$created.user', 
                   'count':{'$sum':1}}}, 
        {'$sort':{'count':-1}},
        {'$limit':10}])
top(contrib,"contributers",10)
#Find top 10 leisures
leisures=db.AnkaraOSM.aggregate([
        {'$match':{'leisure':{'$exists':1}}},
        {'$group':{'_id':'$leisure',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}])
top(leisures,"leisures",10)
#Find top 10 amenities
amenities=db.AnkaraOSM.aggregate([
        {'$match':{'amenity':{'$exists':1}}},
        {'$group':{'_id':'$amenity',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}])
top(amenities,"amenities",10)
#Find top 10 banks
banks=db.AnkaraOSM.aggregate([
        {'$match':{'amenity':{'$regex':'[Bb]ank'}}},
        {'$group':{'_id':'$name',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}])
top(banks,"banks",10)
#Find top 3 cuisines
cuisines=db.AnkaraOSM.aggregate([
        {'$match':{'amenity':{'$regex':'[Rr]estaurant'}}},
        {'$group':{'_id':'$cuisine',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':3}])
top(cuisines,"cuisines",3)

