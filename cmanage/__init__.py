from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_images import Images


#######################################################################


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
images = Images(app)
db = SQLAlchemy(app)


from cmanage import routes
from cmanage.models import Users, Deliveries
db.create_all()