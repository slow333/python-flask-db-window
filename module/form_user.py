def createUserForm():
  return '''
  <h3>사용자를 추가합니다.</h3>
  <form class="form_create" action="/users/create" method="post">
    <p><input type="text" name="fname" placeholder="이름"></p>
    <p><input type="text" name="lname" placeholder="성"></p>
    <p><button type="submit">Create</button></p>
  </form>
  '''
def editUserForm(user):
  return f'''
  <h3>사용자를 수정합니다.</h3>
  <form class="form_create" action="/users/{user['id']}/edit" method="post">
    <p><input type="text" name="fname" placeholder="이름" value="{user['fname']}"></p>
    <p><input type="text" name="lname" placeholder="성" value="{user['lname']}"></p>
    <p><button type="submit">Update</button></p>
  </form>
  '''

def deleteUserForm(user):
  return f'''
  <h3>사용자를 삭제합니다.</h3>
  <form class="form_create" action="/users/{user['id']}/delete" method="post">
    <p>Are you sure you want to delete this User({user['lname']}, {user['fname']})?</p>
    <p><button type="submit">Delete</button></p>
  </form>
  '''