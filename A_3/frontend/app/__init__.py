from flask import Flask

global num_n

webapp = Flask(__name__)

num_n = {'old_num': 1}

from app import main
from app import get
from app import put
from app import key
from app import deleteAll
from app import sizeChange
from app import library
from app import place
from app import dbconnection


# dbconnection.initializeDB()



