def getUsersList(users):
  users_list = ''
  for user in users:
    users_list += f"""
    <div class="user-list">
    <div>이름 : {user.fname}, 성 : {user.lname}</div>
    <div class="links-list">
      <a class="user-link" href="/users/{user.id}/edit">Edit</a>
      <a class="user-link" href="/users/{user.id}/delete">Delete</a>
      <a class="user-link" href="/users/{user.id}">Detail</a>
    </div>
    </div>
    """
  return users_list