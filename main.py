from fastapi import FastAPI, HTTPException, Request, Depends, status
from services.model.database import Token, User
from services.middleware import create_access_token, get_current_active_user
from services.login import authenticate_user
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from decouple import config
from services.register import create_user
from services.login import create_user

app = FastAPI()

@app.put("/users/", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    req = await request.json()
    return (create_user(req))


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
