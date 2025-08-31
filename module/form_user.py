def createUserForm():
  return '''
  <h3>사용자를 추가합니다.</h3>
  <div class="links-list">
      <a href="/users/all">All Users</a>
      <a href="/users/">HOME</a>
      <a href="/users/all" onclick="goBack">Go Back</a>
  </div>
  </div>
  <form class="form_create" action="/users/create" method="post">
    <p><input type="text" name="first_name" placeholder="이름"></p>
    <p><input type="text" name="last_name" placeholder="성"></p>
    <p><input type="text" name="email" placeholder="email"></p>
    <p><button type="submit">Create</button></p>
  </form>
  <script>
  function goBack() {
    event.preventDefault(); 
    if (window.history.length > 1) 
      window.history.back(); 
    else window.location.href='/users/all';
  }
  </script>
  '''
def editUserForm(user):
  return f'''
  <h3>사용자를 수정합니다.</h3>
    <div class="links-list">
      <a href="/users/all">All Users</a>
      <a href="/users/">HOME</a>
      <button onclick="goBack()">Go Back</button>
  </div>
  <form class="form_create" action="/users/{user['id']}/edit" method="post">
    <p><input type="text" name="first_name" placeholder="이름" value="{user['first_name']}"></p>
    <p><input type="text" name="last_name" placeholder="성" value="{user['last_name']}"></p>
    <p><input type="text" name="email" placeholder="email" value="{user['email']}"></p>
    <p><button type="submit">Update</button></p>
  </form>
  <script>
  function goBack() {{
    event.preventDefault(); 
    if (window.history.length > 1) 
      window.history.back(); 
    else window.location.href='/users/all';
  }}
  </script>
  '''

def deleteUserForm(user):
  return f'''
  <h3>사용자를 삭제합니다.</h3>
    <div class="links-list">
      <a href="/users/all">All Users</a>
      <a href="/users/">HOME</a>
      <a href="/users/all" onclick="goBack">Go Back</a>
  </div>
  <form class="form_create" action="/users/{user['id']}/delete" method="post">
    <p>Are you sure you want to delete this User({user['email']}, {user['first_name']})?</p>
    <p><button type="submit">Delete</button></p>
  </form>
  <script>
  function goBack() {{
    event.preventDefault(); 
    if (window.history.length > 1) 
      window.history.back(); 
    else window.location.href='/users/all';
  }}
  </script>
  '''