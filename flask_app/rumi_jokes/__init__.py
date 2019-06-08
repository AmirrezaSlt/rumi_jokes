from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from flask_cqlalchemy import CQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost:3306/dbms'
app.config['MONGOALCHEMY_DATABASE'] = 'rumi'
app.config['MONGOALCHEMY_SERVER'] = 'db-mongo'
app.config['MONGOALCHEMY_PORT'] = '27017'
app.config['MONGOALCHEMY_SAFE_SESSION'] = 'true'
app.config['CASSANDRA_HOSTS'] = ['db-cassandra']
app.config['CASSANDRA_KEYSPACE'] = "dbms"

db = SQLAlchemy(app)
db2 = MongoAlchemy(app)
db3 = CQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from rumi_jokes import routes