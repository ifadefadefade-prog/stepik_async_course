from fastapi import FastAPI, Depends, HTTPException, Query, Request
from models import UserLogin, User
from db import USERS_DATA, get_user, product_list
from dependencies import get_current_user
from security import create_jwt_token, username_from_request
from rbacx import Guard, Subject, Action, Resource, Context
from rbacx.adapters.fastapi import require_access
from rbacx.policy.loader import FilePolicySource, HotReloader

from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter


import asyncio
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


async def global_key_func(request: Request):
    username = username_from_request(request)
    user = get_user(username)
    if not user:
        return "user:guest"
    return f"user:{user.username}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379")
    await FastAPILimiter.init(redis_connection,
                              identifier=global_key_func,
                              prefix="global")
    guard = Guard(policy={})
    reloader = HotReloader(
        guard,
        FilePolicySource("policy.json"),
        initial_load=True,
    )
    app.state.guard = guard
    app.state.reloader = reloader

    yield

    reloader.stop()
    await FastAPILimiter.close()
    await redis_connection.close()


app = FastAPI(lifespan=lifespan)


def rate_limit_global(current_user: User =
                      Depends(get_current_user)):
    role_limits = {
        "admin": (1000, 60),
        "user": (100, 60),
        "guest": (5, 60)
    }
    if "admin" in current_user.roles:
        primary_role = "admin"
    elif "user" in current_user.roles:
        primary_role = "user"
    else:
        primary_role = "guest"
    times, seconds = role_limits.get(primary_role, (1, 60))
    return RateLimiter(times=times, seconds=seconds)


def rbac_dependency(action, resource):
    async def dependency(request: Request):
        guard: Guard = request.app.state.guard
        subject, act, res, ctx = make_env_builder(action, resource)(request)
        allowed = await guard.is_allowed_async(subject, act, res, ctx)
        if not allowed:
            raise HTTPException(403)
    return Depends(dependency)


def make_env_builder(action_name: str, resource_type: str):
    def build_env(request):
        username = username_from_request(request)
        user_obj = get_user(username)
        roles = user_obj.roles if user_obj else []
        subject = Subject(id=username, roles=roles)
        action = Action(action_name)
        resource = Resource(type=resource_type)
        context = Context()
        return subject, action, resource, context
    return build_env


@app.post("/login")
async def login(user_in: UserLogin):
    for user in USERS_DATA:
        if (user["username"] == user_in.username
                and user["password"] == user_in.password):
            token = create_jwt_token({"sub": user_in.username})
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Неверные учетные данные")


@app.get("/admin", dependencies=[rbac_dependency("view_admin", "page"),
                                 Depends(rate_limit_global)])
async def admin_info(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user.username}! "
                   f"Welcome to the admin page."
    }


@app.get("/user", dependencies=[rbac_dependency("view_user", "page"),
                                Depends(rate_limit_global),])
async def user_info(current_user: User = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user.username}! "
                   f"Welcome to the user page."
    }


@app.get("/about_me")
async def about_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/protected_resource", dependencies=[rbac_dependency("view_user", "page"),
                                              Depends(rate_limit_global),])
async def protected_resource(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": f"Hello, {current_user.username}! "
                   f"Welcome to the protected_resource page."
    }


@app.get("/products", dependencies=[rbac_dependency("view_user", "page"),
                                    Depends(rate_limit_global),])
async def get_product_list(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": f"Hello, {current_user.username}, check products list!",
        "products": product_list
    }


@app.post("/products", dependencies=[rbac_dependency("view_user", "page"),
                                     Depends(rate_limit_global),])
async def set_new_product(
    new_item: str = Query(
        default=None, description="Название нового продукта"
    ),
    current_user: User = Depends(get_current_user)
):
    if new_item is None:
        raise HTTPException(404, "Продукт None")
    product_list.append(new_item)
    return {
        "message": f"{current_user.username} add new item: {new_item}!"
    }


@app.delete("/products/{del_item}", dependencies=[rbac_dependency("view_user", "page"),
                                                  Depends(rate_limit_global),])
async def delete_product(
    del_item: str,
    current_user: User = Depends(get_current_user)
):
    if del_item not in product_list:
        raise HTTPException(404, f"Продукт '{del_item}' не найден")
    product_list.remove(del_item)
    return {
        "message": f"{current_user.username} del item: {del_item}!"
    }