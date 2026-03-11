from database import *

init_db()
#add_user("Ahmed")
delete_user(1)
users = get_all_users()
print(users)