import sqlite3
from sqlite3 import Error
import random


################################################################

# User Address Class
class Address:
    def __init__(self, A_lane, A_station, A_pin):
        self.lane = A_lane
        self.station = A_station
        self.PIN = A_pin

#User Class
class User:
    def __init__(self, U_name, U_lane, U_station, U_PIN):
        self.loc = Address(U_lane, U_station, U_PIN)
        self.name = U_name


# Delivery class
class Delivery:

    def __init__(self, s_id, r_id, s_st, r_st, wt):
        self.weight = wt
        self.price = 0
        self.s_id =s_id
        self.r_id = r_id
        self.s_st = s_st
        self.r_st = r_st

        # result of this will be sent as sender
    # def _senderInfo(self,_askForPrompts):
    #     print("Sender's Info: ")
    #     # self._sender = (_askForPrompts())

    #     self._sender = User(*(_askForPrompts()))
    #     self._calcWeight()
        # print("SENDER'S INFORMATION: ", U_SENDER.name, U_SENDER.loc.lane, U_SENDER.loc.station, U_SENDER.loc.PIN)
        # result of this will be sent as receiver
    # def _receiverInfo(self, _askForPrompts):
    #     print("Receiver's Info: ")
    #     # self._receiver = (_askForPrompts())

    #     self._receiver = User(*(_askForPrompts()))

        # print("RECEIVER'S INFORMATION: ", U_RECEIVER.name, U_RECEIVER.loc.lane, U_RECEIVER.loc.station, U_RECEIVER.loc.PIN)


    def _calcWeight(self):
        # claculating price of the delivery
        self.price = 50*int(self.weight) + 100
        # print("The price will be : ", self.price)




################################################################

# connecting to database
# conn = sqlite3.connect('courier.db')
#
# cur = conn.cursor()
# cur.execute()
def sql_connection():
    try:
        con = sqlite3.connect('courier.db')
        return con
    except Error:
        print(Error)   

def sql_table(con):
    cursorobj = con.cursor()
    cursorobj.execute("create table if not exists users(u_id integer primary key autoincrement, name text, lane text, station text, PIN integer)")
    cursorobj.execute("create table if not exists delivery(d_id integer primary key autoincrement, weight integer, price integer, sender_id integer, receiver_id integer, sender_station text, receiver_station text)")
    con.commit()

def sql_insert_user(con, entities):
    cursorobj = con.cursor()
    cursorobj.execute('Insert into  users(name, station) values(?,?)', entities)
    con.commit()

def sql_insert_delivery(con, entities):
    cursorobj = con.cursor()

    cursorobj.execute('Insert into  delivery(weight, price, sender_id, receiver_id, sender_station, receiver_station) values(?,?,?,?,?,?)', entities)
    con.commit()

def sql_update(con):
    cursorobj = con.cursor()
    # cursorobj.execute('Update employees set name = "Ranp" where id = 2')
    con.commit() 

def sql_fetch_deliveries(con):
    cursorobj = con.cursor()
    cursorobj.execute('Select * from delivery')
    rows = cursorobj.fetchall()
    for row in rows:
        print(row)

def fetch_station_from_id(con, id):
    cursorobj = con.cursor()
    cursorobj.execute('Select u_id, station from users where u_id = {}'.format(id))
    rows = cursorobj.fetchall()
    return rows[0][1]

################################################################
# getting user inputs
# print("Enter user details: ")

def askPrompts():
    prompt_name = input("Name: ")
    prompt_address_lane = input("Address Lane:")
    prompt_address_station = input("Address Station:")
    prompt_address_PIN = input("Address PIN:")

    return [prompt_name, prompt_address_lane, prompt_address_station, prompt_address_PIN]

def askDeliveryPrompts():
    prompt_sender_id = input("Sender Id:")
    prompt_receiver_id = input("Receiver Id:")
    prompt_weight = input("Weight:")
    return [prompt_sender_id, prompt_receiver_id, prompt_weight]

con = sql_connection()
sql_table(con)
print("Welcome Human! Get to Work!");
print("Choose:")
choice = -1
while choice != 0:
    choice = int(input("1. Enter new user\t2. Enter a new delivery\t3.Show deliveries\t0. Done for the day\n"))
    if choice == 1:
        newUser = User(*(askPrompts()))
        userDetails = [newUser.name, newUser.loc.station]
        sql_insert_user(con, userDetails)
    elif choice ==2:
        deliveryDetails = askDeliveryPrompts()
        s_id, r_id = deliveryDetails[0], deliveryDetails[1]
        s_st, r_st = fetch_station_from_id(con, s_id), fetch_station_from_id(con, r_id)
        Order = Delivery(s_id, r_id, s_st, r_st, deliveryDetails[2])
        Order._calcWeight()
        values = [Order.weight, Order.price, Order.s_id, Order.r_id, Order.s_st, Order.r_st]
        # print(values)
        # c = con.cursor()
        # c.execute('PRAGMA table_info({})'.format('delivery'))
        # rows = c.fetchall()
        # for r in rows:
            # print(r)
        sql_insert_delivery(con, values)

    elif choice == 3:
        sql_fetch_deliveries(con)
    elif choice == 0:
        print("Goodbye  ~\-_-/~")
        break
    else:
        print("Invalid choice, try agian :/")          

# Order = Delivery()

# sql_insert_user(Order._senderInfo(askPrompts))
# Order._receiverInfo(askPrompts)


# printing user inputs
# print(f"Delivery INFO -----  of delivery_id - ", Order.d_id)
# print("SENDER: ", Order._sender.name)
# print("RECEIVER: ", Order._receiver.name)



################################################################
