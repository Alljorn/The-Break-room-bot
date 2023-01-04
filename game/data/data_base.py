import sqlite3
import os

import game.data.data_base_utils as utils_db


DATA_BASE = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/data_base.db')

utils_db.init_data_base(DATA_BASE)