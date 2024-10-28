from fastapi import APIRouter


admin_router = APIRouter()

import src.entities.admin.routes.login
import src.entities.admin.routes.refresh_token
import src.entities.admin.routes.redeem_user_points
import src.entities.admin.routes.create_bin
import src.entities.admin.routes.generate_codes
