import sys
sys.path.append('B:\\python\\window-flask')

from sqlalchemy import select
from db_config import engine, users, addresses

select_all = "select * from users;"
users_select = "select * from users where name = 'Jane';"
with engine.connect() as conn:
  users = conn.execute(users_select).fetchall()
  for row in users: print(row)
  user = conn.execute(users_select).fetchone()
  print(user)
