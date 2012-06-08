from pymongo import Connection
from bson.code import Code

def add():
    global card

    print "Adding a new card - add blank name to exit"
    newCard = {}
    while 1:
        tag = raw_input("type name: ")
        if tag == "":
            break
        value = raw_input("value: ")
        newCard[tag] = value

    if len(newCard) == 0:
        print "Nothing added"
        return

    print card.insert(newCard)
    print "card added"

def find():
    global card
    tag = raw_input("filter on type: ")
    if len(tag) == 0:
        print "nothing to find"
        return

    value = raw_input("value: ")
    sample = {tag: value}

    print "Results:"
    for match in card.find(sample):
        print match

def nameCounts():
    global zips

    city = raw_input("City name: ")
    mapper = Code("""
        function(){
            if (this["city"] == "%s") {
                emit("c", 1);
            }
        }
        """ %city)
    reducer = Code("""
        function(key, values){
            var sum=0;
            for(var i in values) {
                sum += values[i];
            }
            return sum;
        }
        """)

    count = zips.map_reduce(mapper, reducer, "zip"+city)
    print count.find_one()["value"]

def delete():
    global card
    name = raw_input("name: ")
    card.remove({"name":name}, safe=True)

def update():
    global card
    name = raw_input("name to update: ")
    card.update({"name":name}, {"name":name, "updated":"true"})

connection = Connection()
database = connection['test']

card = database['card']
zips = database['zips']

while 1:
    print "what to do?"
    print "1: add a card"
    print "2: find a card"
    print "3: name count"
    print "4: update"
    print "5: delete"
    print "0: exit"
    do = raw_input("pick: ")
    if do == "1":
        add()
    elif do == "2":
        find()
    elif do == "3":
        nameCounts()
    elif do == "4":
        update()
    elif do == "5":
        delete()
    elif do == "0":
        break
    else:
        print "wrong input"
