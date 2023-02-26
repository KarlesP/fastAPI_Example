
from model.database import verify_password, get_user_by_email


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email, whole=True)
    if not user:
        return "Check your credentials!\nEmail or password is not correct."
    if not verify_password(password, user['password']):
        return "Check your credentials!\nEmail or password is not correct."
    return "Loggedin email: "+user['email']

print(authenticate_user("johndoe@example.com", "mysecretpassword"))
