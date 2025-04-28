from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models.user import User
from backend.schemas.user import UserCreate, UserLogin, TokenPayload
from backend.schemas.recover import EmailSchema, ResetPassword
from backend.utils.security import hash_password, verify_password
from backend.auth.jwt_handler import create_access_token, decode_access_token, create_one_time_use_token
from backend.auth.email import send_confirmation_mail, send_password_reset_link, GmailService
from backend.core.config import SMTP_CONFIGURATION, RESET
from backend.dependencies.auth import get_current_user
from backend.utils.crud import is_user_existing

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva cuenta de usuario.

    **Parámetros**
    - `email`: Dirección de correo del usuario
    - `username`: Nombre de usuario único
    - `password`: Contraseña con al menos 8 caracteres

    **Respuesta**
    - Envía un correo de confirmación con un token (SMTP activado)
    - Crea una cuenta verificada (SMTP desactivado)
    """
    if is_user_existing(db, user.email, user.username):
        raise HTTPException(status_code=400, detail="Account already exist on db")

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
        role="user",
        is_verified=SMTP_CONFIGURATION == "deactivate"  # True if SMTP is OFF
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)# <---- AFTER commit to get ID!!

    if SMTP_CONFIGURATION != "deactivate":
        token = create_one_time_use_token(str(new_user.id))
        smtp = GmailService()
        send_confirmation_mail(new_user.email, token, smtp)

    return {"message": "User pending to validation.", "smtp": SMTP_CONFIGURATION}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Logueo de un usuario.

    **Parámetros**
    - `email`: Dirección de correo registrada
    - `password`: Contraseña del usuario

    **Respuesta**
    - Devuelve un token JWT si es exitoso
    """
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if db_user.is_verified is False:
        raise HTTPException(status_code=401, detail="Account is not activated")

    token = create_access_token({
        "sub": str(db_user.id),
        "mail": db_user.email,
        "username": db_user.username,
        "role": db_user.role
    })
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
async def forgot_password(data: EmailSchema, db: Session = Depends(get_db)):
    """
    Primer paso para restablecer contraseña

    **Parámetros**
    - `email`: Correo registrado para enviar instrucciones

    **Respuesta**
    - Envía un correo para restablecer la contraseña (SMTP activado)
    - Envia la URL que nos redirige a /reset-password (SMTP desactivado)
    """
    email = data.email
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="No mail matches")

    token = create_one_time_use_token(str(db_user.id))
    flag = SMTP_CONFIGURATION != "deactivate"
    msg = f"{RESET}/reset-password?token={token}"
    if flag:
        smtp = GmailService()
        send_password_reset_link(db_user.email, token, smtp)
        msg = "Mail sent successfully."

    return {"message": msg, "smtp": SMTP_CONFIGURATION}

@router.post("/reset-password")
async def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    """
    Restablece la contraseña del usuario usando un token válido.

    **Parámetros**
    - `token`: Token recibido por correo
    - `new_password`: Nueva contraseña (debe ser distinta)

    **Respuesta**
    - Informa al usuario (contraseña actualizada correctamente).
    """
    payload = decode_access_token(data.token, True)
    id = payload.get("sub")
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid token")
    hash = hash_password(data.new_password)
    if db_user.hashed_password == hash:
        raise HTTPException(status_code=404, detail="Must be a different password")
    db_user.hashed_password = hash
    db.commit()
    return {"message": "Password changed successfully."}

@router.post("/confirm-email")
async def confirm_email(data: TokenPayload, db: Session = Depends(get_db)):
    """
    Confirma el correo del usuario mediante un token de un solo uso.

    **Parámetros**
    - `token`: Token de confirmación recibido por correo

    **Parámetros**
    - Informa al usuario, `is_verified` cambia a True
    """
    payload = decode_access_token(data.token, True)
    id = payload.get("sub")
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Not valid token")
    if db_user.is_verified:
        return {"message": "The account is already verified."}
    db_user.is_verified = True
    db.commit()

    return {"message": "Account activated successfully."}

@router.post("/refresh-token")
def refresh_token(db: Session = Depends(get_db),
        user: User = Depends(get_current_user)):
    """
    Refresca el token de acceso utilizando un token de refresco válido.

    **Parámetros**
    - El token se pasa en el encabezado Authorization como 'Bearer {current_token}'.

    **Respuesta**
    - Devuelve un nuevo token de acceso.
    """
    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Crear un nuevo token de acceso
    new_access_token = create_access_token({
        "sub": str(db_user.id),
        "mail": db_user.email,
        "username": db_user.username,
        "role": db_user.role
    })

    return {"access_token": new_access_token, "token_type": "bearer"}