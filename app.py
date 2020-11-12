import traceback

import uvicorn
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

import errors
from models.token import Token
from routers.match_results.routing import match_router
from tools.Firebase import sign_in

service_name = "Soccer-Poule-API"
app = FastAPI()


origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


@app.post("/v1/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        response = sign_in(email=form_data.username, password=form_data.password)
        return response
    except Exception:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Incorrect username or password", "type": errors.INVALID_LOGIN},
            headers={"WWW-Authenticate": "Bearer"},
        )

app.include_router(
    match_router,
    prefix="/v1/match",
    tags=["Matches"],
    responses={404: {"description": "Not found"}},
)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, workers=3)
