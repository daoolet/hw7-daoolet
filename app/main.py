from fastapi import Cookie, FastAPI, Form, Request, Response, templating, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt

from flowers_repository import Flower, FlowersRepository
from purchases_repository import Purchase, PurchasesRepository
from users_repository import User, UsersRepository

app = FastAPI()
templates = templating.Jinja2Templates("../templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ваше решение сюда

# --------------- SIGN UP

@app.get("/signup")
def get_signup(request: Request):
    return Response("Registered - OK", status_code=200)

@app.post("/signup")
def post_sigup(user: User):
    user_exists = users_repository.get_by_email(email=user.email)

    if user_exists:
        raise HTTPException(status_code = 400, detail="User with this username already exists")
    
    users_repository.save(
        User(email=user.email, full_name=user.full_name, password=user.password)
    )


    return Response("successfully", status_code=200)


# --------------- LOGIN

def create_access_token(user_id: str) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "kek", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "kek", "HS256")
    return data["user_id"]

@app.get("/login")
def get_login():
    return Response("Logged in - OK", status_code=200)

@app.post("/login")
def post_login(data: OAuth2PasswordRequestForm = Depends()):
    user = users_repository.get_by_email(data.username)
    if not user:
        return Response("Loggin Failed: Wrong email or password")

    if user.password == data.password:
        token = create_access_token(user.email)
 
    return {"access_token": token, "type": "bearer"}


# --------------- PROFILE

@app.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme)
):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)

    return Response("200 OK", status_code=200)


# --------------- FLOWERS

@app.get("/flowers", response_model = list[Flower])
def get_flowers():

    flowers = flowers_repository.get_all()

    return flowers

@app.post("/flowers")
def post_flowers(flower: Flower):
    
    flowers_repository.save(
        Flower(name=flower.name, count=flower.count, cost=flower.cost)
    )

    return {"flower_id": flower.id}

# --------------- CART

@app.get("/cart/items")
def get_cart():
     
    cart_flowers = flowers_repository.get_cart_flowers()
    total_cost = sum(i.cost for i in cart_flowers)


    
    return {"total_cost": total_cost, "cart_flowers": cart_flowers}

@app.post("/cart/items")
def post_cart(flower_id: int = Form(...)):
    
    current_flower = flowers_repository.get_by_id(flower_id)
    flowers_repository.add_cart_flowers(current_flower)

    response = Response("Added to cart - OK", status_code=200)
    response.set_cookie("flower_id", flower_id)

    return response


# конец решения