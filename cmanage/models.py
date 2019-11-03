from cmanage import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    address_lane= db.Column(db.String(100), nullable=False)
    address_station = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.user_id}', '{self.address_lane}', '{self.address_station}')"


class Deliveries(db.Model):
    deli_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    start_station = db.Column(db.String(4), nullable=False)
    end_station = db.Column(db.String(4), nullable=False)


    def __repr__(self):
        return f"Deliveries('{self.sender_station}' , '{self.receiver_station}', '{self.weight}' )"

# db.create_all()
