import json
import os
import traceback

import firebase_admin
import requests
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from firebase_admin import credentials
from requests import HTTPError

import errors

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")
firebase_cred_path = os.path.abspath("./soccer-poule-api-firebase-admin.json")
cred = credentials.Certificate(firebase_cred_path)
app = firebase_admin.initialize_app(cred)


def sign_in_with_email_and_password(email: str, password: str):
    """
    Get Firebase user using email + password
    :param email: email string
    :param password: password string
    :return: Firebase user object
    """

    api_key = os.getenv('FIREBASE_APIKEY')
    request_ref = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()


def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        response = auth.verify_session_cookie(token, app=app)
        return response
    except Exception:
        raise credentials_exception


def sign_in(email, password):
    response = sign_in_with_email_and_password(email=email, password=password)
    user = auth.get_user(response['localId'], app=app)
    if not user or user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Could not validate credentials", "type": errors.INVALID_LOGIN},
            headers={"WWW-Authenticate": "Bearer"}
        )

    session = auth.create_session_cookie(response['idToken'], 1209600, app=app)
    response = {
        "access_token": session,
        "token_type": "bearer"
    }
    return response


def validate_token(token):
    try:
        auth.verify_session_cookie(token, app=app)
        return True
    except Exception as e:
        return False


def update_password(uid, password):
    return auth.update_user(uid, password=password, app=app)


def update_profile(uid, display_name):
    try:
        return auth.update_user(uid, display_name=display_name, app=app)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{
            "msg": "Update profile ERROR in Portal API",
            "type": errors.FIREBASE_ERROR
        }])


# def reset_password_email(email):
#     try:
#         return f_app.send_password_reset_email(email)
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{
#             "msg": "Reset password ERROR in Portal API",
#             "type": errors.EMAIL_NOT_FOUND
#         }])
#
#
# def reset_password_code(code, password):
#     try:
#         return f_app.verify_password_reset_code(code, password)
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[{
#             "msg": "Reset password ERROR in Portal API",
#             "type": errors.RESET_ERROR
#         }])