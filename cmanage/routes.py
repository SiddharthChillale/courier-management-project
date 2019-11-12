from cmanage import app, db
from cmanage.forms import UserForm, DeliveryForm, GetDelivers, GetUsers, GetStation, UserDeletionForm, DeliveryDeletionForm
from flask import render_template, url_for, flash, redirect
from cmanage.models import Users, Deliveries

#---------DIjkstra and Other things----------------------------------------
def findMin(graph, visited, d):
    minNode = -1
    min = float('inf')
    for i in range(len(graph)):
        if visited[i] == 0 and d[i] < min:
            min = d[i]
            minNode = i
    return minNode

def checkConnection(graph, u, v):
    # print('u is',u,'and v is',v)
    for i,j in enumerate(graph[u]):
        # print('i is', i, 'and j is', j)
        if j[0] == v:
            # print('yes connection is there and cost is', j[1])
            return True, j[1] # returns whether there is an edge in graph and the weight of it

    # print('No connection')
    return False, float('inf')

def dijkstra(graph, root):
    d = [float('inf')]*len(graph)
    visited = [0]*len(graph)
    d[root] = 0
    queue = []
    for k in range(len(graph)):
        u = findMin(graph, visited, d)
        visited[u] = 1
        # print('Min node is ', u)
        for i in range(len(graph)):
            x = checkConnection(graph, u, i)
            # print("x is ", x)
            if visited[i] == 0 and  x[0] and d[u] != float('inf') and d[u] + x[1] < d[i]:
                d[i] = d[u] + x[1]
    return d

graph = dict({
    0: [(1,17),(2,20)],
    1: [(0,17),(3,12)],
    2: [(0, 20),(3,7),(4,11)],
    3: [(1,12),(2,7), (5,2), (6,3)],
    4: [(2,11),(8,5)],
    5: [(3,2), (8,2), (6,2)],
    6: [(3, 3), (5, 2), (7, 3), (29,3), (9,5)],
    7: [(6,3),(8,7), (9,3), (12,4)],
    8: [(4,5),(5,2),(7,3), (20, 10)],
    9: [(6, 10),(7,3),(10,3), (11, 4), (29, 4)],
    10: [(9,3)],
    11: [(9,4),(13,5),(14,5), (15,7)],
    12: [(7,4), (13,2), (18, 3)],
    13: [(11,5), (12,2), (14,3), (17,3), (18, 3)],
    14: [(11,5),(13,3), (17,1)],
    15: [(11,7),(16,3),(17,2)],
    16: [(15, 3)],
    17: [(13,3),(14,1), (15, 2)],
    18: [(12,3),(13,3),(19,2)],
    19: [(18,5), (20,7), (21, 3)],
    20: [(8,10), (19,6), (21, 1)],
    21: [(19,3),(20,1), (22,2)],
    22: [(21,2),(23,1),(28,1)],
    23: [(22, 1),(24,1)],
    24: [(23,1),(25,2)],
    25: [(24,2),(26,1),(28,1)],
    26: [(25,1), (27,1)],
    27: [(26,1)],
    28: [(22,1),(25,1)],
    29: [(6,3),(9,4)] 
})

statemap = {
    'JK01':0,
    'PB01':1,
    'HP02':2,
    'HR01':3,
    'UK02':4,
    'DL01':5,
    'RJ01':6,
    'MP01':7,
    'UP01':8,
    'MH12':9,
    'GO37':10,
    'KR01':11,
    'JH13':12,
    'CH01':13,
    'TE05':14,
    'TN15':15,
    'KL37':16,
    'AD01':17,
    'OR01':18,
    'WB14':19,
    'BR14':20,
    'SK14':21,
    'AS14':22,
    'NG14':23,
    'AN14':24,
    'ME14':25,
    'MN14':26,
    'TR14':27,
    'MZ14':28,
    'GJ14':29,
}
def calc_dist(sender_station, receiver_station):
    sender_id = statemap[sender_station]
    receiver_id = statemap[receiver_station]
    d = dijkstra(graph, sender_id)
    return d[receiver_id]


###########################################################################

# routes for all pages

#   home route
@app.route('/')
@app.route('/home')
def home():
    add= [url_for('newuser'), url_for('delivery'), url_for('viewdelivery'), url_for('viewusers'), url_for('deleteuser'), url_for('deletedelivery')]
    return render_template('home.html', address=add)

#   route fo creating a new user
@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    form = UserForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     address_lane=form.lane.data,
                     address_station=form.station.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('viewusers'))
    return render_template('newuser.html', title='New User', form=form, homeadd=url_for('home') )



#   route to creating a new delivery
@app.route("/delivery", methods=['GET', 'POST'])
def delivery():
    form = DeliveryForm()
    if form.validate_on_submit():
        ## causing some InterFaceError
        sender_station = GetStation(form.sender_id.data)

        receiver_station = GetStation(form.receiver_id.data)
        shortest_distance = calc_dist(sender_station, receiver_station)
        calculated_price = 50*form.weight.data*shortest_distance + 100
        delivery = Deliveries(sender_id=form.sender_id.data,
                              receiver_id=form.receiver_id.data,
                              start_station=sender_station,
                              end_station=receiver_station,
                              weight=form.weight.data,
                              price = calculated_price)
        db.session.add(delivery)
        db.session.commit()
        flash(f'Delivery created for {form.sender_id.data}!', 'success')
        return redirect(url_for('viewdelivery'))
    return render_template('delivery.html', title='New Delivery', form=form, homeadd=url_for('home') )


@app.route("/deleteuser", methods=['GET', 'POST'])
def deleteuser():
    form = UserDeletionForm()
    if form.validate_on_submit():
        Users.query.filter_by(user_id=form.object_id.data).delete()
        db.session.commit()
        flash(f'User deleted for {form.object_id.data}!', 'success')
        return redirect(url_for('viewusers'))
    return render_template('deleteuser.html', title='Delete User', form=form )
        # delete user from user table


@app.route("/deletedelivery", methods=['GET', 'POST'])
def deletedelivery():
    form = DeliveryDeletionForm()
    if form.validate_on_submit():
        Deliveries.query.filter_by(deli_id=form.Del_id.data).delete()
        db.session.commit()
        flash(f'Delivery deleted for {form.Del_id.data}!', 'success')
        return redirect(url_for('viewdelivery'))
    return render_template('deletedelivery.html', title='Delete Delivery', form=form )
        # delete delivery from delivery table



#   route to view all deliveries
@app.route("/viewdelivery")
def viewdelivery():
    allDeliveries = GetDelivers()
    return render_template('viewdelivery.html', table=allDeliveries)


#   route to view all users
@app.route("/viewusers")
def viewusers():
    allDeliveries = GetUsers()
    return render_template('viewusers.html', table=allDeliveries)
