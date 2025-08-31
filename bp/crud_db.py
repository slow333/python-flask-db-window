import sys
sys.path.append('B:\\python\\window-flask')

from flask import Blueprint, request, redirect # type: ignore
from sqlalchemy import insert, delete, update, select

from module.body import body
from module.form_user import createUserForm, editUserForm, deleteUserForm
from db.users.create_users_table import users
from db.users.connect_db import engine
from module.user_list import getUsersList

users_db_bp = Blueprint("crud_db", __name__, url_prefix="/users")

def all_users():
  with engine.connect() as conn:
    result = conn.execute(select([users]))
    return result.fetchall()

@users_db_bp.route("/")
def users_home():
  content = f'''
  <ul>
    <li><a href="/users/all">All Users</a></li>
    <li><a href="/users/create">Create User</a></li>
  </ul>
  '''
  return body("users DB", content)

@users_db_bp.route("/all")
def users_all(id=None):
  users_list = getUsersList(all_users())
  users_list += f'''
  <div class="links-list">
    <a href="/users/all">All Users</a>
    <a href="/users/create">Create User</a>
  </div>
  '''
  return body("users DB", users_list)
@users_db_bp.route("/<int:id>")
def users_detail(id):
  sel_user = select([users]).where(users.c.id == id)
  user = ''
  with engine.connect() as conn:
    user = conn.execute(sel_user).fetchone()
  user_detail = f'''
  <div class="user-name">이름 : {user['fname']}</div>
  <div class="user-name">성 : {user['lname']}</div>
  <div class="links-list">
    <a href="/users/all">All Users</a>
    <a href="/users/create">Create User</a>
    <a href="/users/{user['id']}/edit">Edit User</a>
    <a href="/users/{user['id']}/delete">Delete User</a>
  </div>
  '''
  return body("users DB", user_detail)

@users_db_bp.route("/create", methods=["GET", "POST"])
def create_user():
  if request.method == "POST":
    fname = request.form["fname"]
    lname = request.form["lname"]
    if not fname or not lname:
      return redirect("/users/create")
    stmt = insert(users).values(fname=fname, lname=lname)
    with engine.connect() as conn: conn.execute(stmt)
    return redirect("/users/all")
  elif request.method == "GET":
    return body("Create User", createUserForm())

@users_db_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_user(id):
  if request.method == "POST":
    fname = request.form["fname"]
    lname = request.form["lname"]
    stmt = update(users).where(users.c.id == id).values(fname=fname, lname=lname)
    with engine.connect() as conn: conn.execute(stmt)
    return redirect("/users/all")
  elif request.method == "GET":
    user = select([users]).where(users.c.id == id)
    with engine.connect() as conn:
      user = conn.execute(user).fetchone()
    return body("Edit User", editUserForm(user))

@users_db_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_user(id):
  if request.method == "POST":
    stmt = delete(users).where(users.c.id == id)
    with engine.connect() as conn: conn.execute(stmt)
    return redirect("/users/all")
  elif request.method == "GET":
    sel_user = select([users]).where(users.c.id == id)
    with engine.connect() as conn:
      user = conn.execute(sel_user).fetchone()
    return body("Delete User", deleteUserForm(user))