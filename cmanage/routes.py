from cmanage import app, db
from cmanage.forms import UserForm, DeliveryForm, GetDelivers, GetUsers, GetStation, UserDeletionForm, DeliveryDeletionForm
from flask import render_template, url_for, flash, redirect
from cmanage.models import Users, Deliveries

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
        calculated_price = 50*form.weight.data + 100
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
