from flask import Blueprint, request, redirect # type: ignore
from module.body import body
from module.form_user import createUserForm, editUserForm, deleteUserForm
from db.users.select_users import users


users_db_bp = Blueprint("crud_db", __name__, url_prefix="/users")

@users_db_bp.route("/")
def users_all():
  users_list = ''
  for user in users:
    users_list += f"<div>{user.fname}</div>"
  return body("users DB", users_list)


""" 
def manage_by_id(id, new_topic=None, delete=False):
  for topic in topics:
    if topic["id"] == id:
      if delete:
        del topics[topics.index(topic)]
        return None
      elif new_topic is not None:
        topic.update(new_topic)
        return topic
      return topic
  return None

@db_bp.route("/create", methods=["GET", "POST"])
def create_data():
  if request.method == "POST":
    global nextId
    title = request.form["title"]
    content = request.form["content"]
    if not title or not content:
      return redirect("/topic/create")
    new_topic = {"id": nextId, "title": title, "content": content}
    topics.append(new_topic)
    url = "/topic/" + str(new_topic["id"])
    nextId += 1
    return redirect(url)
  elif request.method == "GET":
    return body(nav(topics), getCreateForm())

@db_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_data(id):
  if request.method == "POST":
    title = request.form["title"]
    content = request.form["content"]
    new_topic = {"id": id, "title": title, "content": content}
    manage_topic_by_id(id, new_topic)
    url = "/topic/" + str(new_topic["id"])
    return redirect(url)
  elif request.method == "GET":
    topic = manage_topic_by_id(id)
    return body(nav(topics), getEditForm(topic))

@db_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_data(id):
  if request.method == "POST":
    manage_topic_by_id(id, delete=True)
    return redirect("/topic/")
  elif request.method == "GET":
    topic = manage_topic_by_id(id)
    return body(nav(topics), getDeleteForm(topic))

@db_bp.route("/<int:id>")
def detail(id):
  topic = manage_topic_by_id(id)
  content = f'''
  <h1>{topic["title"]}</h1>
  <p>{topic["content"]}</p>
  '''
  return body(nav(topics), content, id)

 """