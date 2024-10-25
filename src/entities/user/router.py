from fastapi import APIRouter

user_router = APIRouter()

import src.entities.user.routes.info
import src.entities.user.routes.login
import src.entities.user.routes.refresh_token
import src.entities.user.routes.signup
import src.entities.user.routes.transactions
