from fastapi.testclient import TestClient
from backend.main import app
from backend.schemas import UserCreate, UserOut
from backend.utils.jwt import create_access_token
from datetime import timedelta

client = TestClient(app)


# Test de Registro de Usuario
def test_register():
    user_data = {
        "email": "dummy@example.com",
        "password": "password123"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()


# Test de Login
def test_login():
    user_data = {
        "email": "dummy_login@example.com",
        "password": "password123"
    }
    client.post("/auth/register", json=user_data)  # Registrar el usuario

    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test de Verificación de Correo
def test_verify_email():
    # Registro de un usuario
    user_data = {
        "email": "dummy@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200

    # Crear token de verificación de ejemplo
    token = create_access_token({"sub": "1"}, timedelta(minutes=15))

    # Verificar correo con token generado
    verify_response = client.get(f"/auth/verify?token={token}")
    assert verify_response.status_code == 200
    assert verify_response.json()["message"] == "Email verified successfully"


# Test de Actualización de Perfil
def test_update_profile():
    # Registro y login del usuario
    user_data = {
        "email": "dummy@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Actualizar el perfil (cambiar el email)
    updated_data = {
        "email": "updatedemail@example.com",
        "password": "newpassword123"
    }

    update_response = client.put("/auth/me", json=updated_data, headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == 200
    assert update_response.json()["email"] == updated_data["email"]


# Test de Stats (Solo Admin)
def test_get_stats():
    # Primero, crea un usuario admin para las pruebas
    admin_data = {
        "email": "adminuser@example.com",
        "password": "password123"
    }
    admin_response = client.post("/auth/register", json=admin_data)
    assert admin_response.status_code == 200
    admin_user = admin_response.json()

    # Asignamos is_admin a True (esto debería hacerse normalmente en el backend)
    admin_user["is_admin"] = True

    # Login como admin
    login_response = client.post("/auth/login", data={"username": admin_user["email"], "password": "password123"})
    token = login_response.json()["access_token"]

    # Petición de stats
    response = client.get("/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "total_users" in response.json()
    assert "active_users" in response.json()

