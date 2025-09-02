from flask import Blueprint, request, redirect # type: ignore
from sqlalchemy import insert, delete, update, select

from module.body import body
from module.form_user import createUserForm, editUserForm, deleteUserForm
from db.users.create_users_table import users
from db.users.connect_db import engine
from module.user_list import getUsersList, getUsersDetail

users_db_bp = Blueprint("crud_db", __name__, url_prefix="/users")

def all_users():
  with engine.connect() as conn:
    result = conn.execute(select([users]).order_by(users.c.id.desc()))
    return result.fetchall()

@users_db_bp.route("/")
def users_home():
  content = f'''
  <h1>users DB를 조회합니다.</h1>
  <div class="links-list">
    <div>전체 사용자 리스트 : <a href="/users/all">All Users</a></div>
    <hr style="margin: 10px 0px;">
    <div>사용자 새로 생성 : <a href="/users/create">Create User</a></div>
  </div>
  '''
  return body("users DB", content)

@users_db_bp.route("/all")
def users_all():
    page = int(request.args.get("page", 1))
    per_page = 5  # 한 페이지에 5명씩
    offset = (page - 1) * per_page

    with engine.connect() as conn:
      result = conn.execute(
          select([users]).order_by(users.c.id.desc()).offset(offset).limit(per_page)
      )
      users_page = result.fetchall()

      # 전체 사용자 수 구하기
      total = conn.execute(select([users])).rowcount

    users_list = getUsersList(users_page)

    # 페이지네이션: 현재 페이지 기준으로 최대 5개 페이지만 표시
    total_pages = (total // per_page) + (1 if total % per_page else 0)
    start_page = max(1, page - 2)
    end_page = min(total_pages, start_page + 4)
    if end_page - start_page < 4:
      start_page = max(1, end_page - 4)
    page_links = ''
    for i in range(start_page, end_page + 1):
      if i == page:
        page_links += f'<strong style="color: red;font-size:1.4rem;">{i}</strong> '
      else:
        page_links += f'<a href="/users/all?page={i}" style="color: blue;font-size:1.4rem;">{i}</a> '
    next_page = getPage(page + 1, "Next") if len(users_page) == per_page else ''
    prev_page = getPage(page - 1, "Prev") if page > 1 else ''
    first_page = getPage(1, "First") if page > 1 else ''
    last_page = getPage(total_pages, "Last") if page < total_pages else ''
    pagination = f'''<div>
      {first_page} {prev_page}
      {page_links}
      {next_page} {last_page}
      </div>'''

    new_users_list = f'''
    <h1>전체 사용자 목록</h1>
    <div class="links-list">
      <a href="/users/create">Create User</a>
      <a href="/users/">HOME</a>
    </div>
    {users_list}
    {pagination}
    '''
    return body("users DB", new_users_list)

def getPage(goto=1, label=""):
  return f'''<button class="nav-button">
        <a href="/users/all?page={goto}">
        {label}</a></button>
  '''

@users_db_bp.route("/<int:id>")
def users_detail(id):
  sel_user = select([users]).where(users.c.id == id)
  user = ''
  with engine.connect() as conn:
    user = conn.execute(sel_user).fetchone()
  user_detail = getUsersDetail(user)
  return body("users DB", user_detail)

@users_db_bp.route("/create", methods=["GET", "POST"])
def create_user():
  if request.method == "POST":
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    email = request.form["email"]
    if not fname or not lname:
      return redirect("/users/create")
    stmt = insert(users).values(first_name=fname, last_name=lname, email=email)
    with engine.connect() as conn: conn.execute(stmt)
    return redirect("/users/all")
  elif request.method == "GET":
    return body("Create User", createUserForm())
  return None


@users_db_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_user(id):
  if request.method == "POST":
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    email = request.form["email"]
    stmt = update(users).where(users.c.id == id).values(first_name=fname, last_name=lname, email=email)
    with engine.connect() as conn: conn.execute(stmt)
    return redirect("/users/all")
  elif request.method == "GET":
    user = select([users]).where(users.c.id == id)
    with engine.connect() as conn:
      user = conn.execute(user).fetchone()
    return body("Edit User", editUserForm(user))
  return None

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
  return None