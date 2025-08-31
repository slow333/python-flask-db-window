def getUsersList(users):
  users_list = ''
  for user in users:
    users_list += f"""
    <div class="user-list">
      <div>이름 : {user.first_name}, 성 : {user.last_name}, email : {user.email}</div>
      <div class="links-list">
        <a class="user-link" href="/users/{user.id}/edit">Edit</a>
        <a class="user-link" href="/users/{user.id}/delete">Delete</a>
        <a class="user-link" href="/users/{user.id}">Detail</a>
      </div>
    </div>
    """
  return users_list


def getUsersDetail(user):
    users_detail = f'''
  <h1>사용자 세부 정보</h1>
  <div class="user-name">이름 : {user['first_name']}</div>
  <div class="user-name">성 : {user['last_name']}</div>
  <div class="user-name">email : {user['email']}</div>
  
  <div class="links-list">
    <a href="/users/all">All Users</a>
    <a href="/users/create">Create User</a>
    <a href="/users/{user['id']}/edit">Edit User</a>
    <a href="/users/{user['id']}/delete">Delete User</a>
    <button onclick="goBack()">Go Back</button>
  </div>
  <script>
  function goBack() {{
  event.preventDefault(); 
      if (window.history.length > 1) 
          window.history.back(); 
          else window.location.href='/users/all';
  }}
  </script>
    '''
    return users_detail