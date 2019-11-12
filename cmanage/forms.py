from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cmanage.models import Users, Deliveries

##############################################################################3


#All Stations with IDs

ALLSTATIONS = [
("",""),
('JK01','JK01'),
('PB01','PB01'),
('HP02','HP02'),
('HR01','HR01'),
('UK02','UK02'),
('DL01','DL01'),
('RJ01','RJ01'),
('MP01','MP01'),
('UP01','UP01'),
('MH12','MH12'),
('GO37','GO37'),
('KR01','KR01'),
('JH13','JH13'),
('CH01','CH01'),
('TE05','TE05'),
('TN15','TN15'),
('KL37','KL37'),
('AD01','AD01'),
('OR01','OR01'),
('WB14','WB14'),
('BR14','BR14'),
('SK14','SK14'),
('AS14','AS14'),
('NG14','NG14'),
('AN14','AN14'),
('ME14','ME14'),
('MN14','MN14'),
('TR14','TR14'),
('MZ14','MZ14'),
('GJ14','GJ14'),
]

###############################################################################
#   User Form
class UserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    lane = StringField('Lane',
                            validators = [DataRequired()])
    station = SelectField('Station',
                            choices = ALLSTATIONS,
                            validators = [DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')



#   Delivery Form
class DeliveryForm(FlaskForm):
    sender_id = IntegerField('Sender Id',
                        validators=[DataRequired()])
    receiver_id = IntegerField('Receiver Id',
                        validators=[DataRequired()])
    weight = IntegerField('Weight of Package',
                        validators=[DataRequired()])

    submit = SubmitField('Create')

    def validate_sender_id(self, sender_id):
        station_extracted = Users.query.get(sender_id.data)
        if not station_extracted:
            raise ValidationError("No such User Exists")


    def validate_receiver_id(self, receiver_id):
        station_extracted = Users.query.get(receiver_id.data)
        if not station_extracted:
            raise ValidationError("No such User Exists")


# deletion forms

class UserDeletionForm(FlaskForm):
    object_id = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')

    def validate_object_id(self, object_id):
        if not Users.query.get(object_id.data):
            raise ValidationError("No Delivery of This ID. Please check again.")

class DeliveryDeletionForm(FlaskForm):
    Del_id = IntegerField('Delivery ID', validators=[DataRequired()])
    submit = SubmitField('Confirm Delete')

    def validate_Del_id(self, Del_id):
        if not Deliveries.query.get(Del_id.data):
            raise ValidationError("No Delivery of This ID. Please check again.")

##############################################################################3

#   gets all deliveries to be shown
def GetDelivers():
    allDelis = Deliveries.query.all()
    return allDelis


def GetStation(_id):
    user_for_station = Users.query.get(_id)
    return user_for_station.address_station

#   gets all users to be shown
def GetUsers():
    allUsers = Users.query.all()
    return allUsers
