from model.database import User,get_user_by_email,create_user

def register_user( email: str, password: str):
    if get_user_by_email(email):
        return {'success': False, 'message': 'Email already registered'}
    new_user = User(email=email,password=password)
    new_user = create_user(new_user)
    return {'success': True, 'message': 'User created', 'data': new_user.dict()}
