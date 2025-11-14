# Architecture du projet

## Structure actuelle du projet

```
core
├── app.py
├── config.py
├── extensions.py
└── setup.py

src
├── admin
│   ├── routes.py
│   └── services.py
├── auth
│   ├── dependencies.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
├── db
│   └── database.py
├── routes
│   └── __init__.py
├── users
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
└── websocket.py
```

Fichiers racine :

```
.env
.gitignore
alembic.ini
LICENSE
requirements.txt
server.py
README.md
```

---

## Description des modules

### core/

* app.py : Initialise FastAPI et attache les routeurs.
* config.py : Variables d'environnement et configuration générale.
* extensions.py : Middleware CORS et autres extensions.
* setup.py : Métadonnées du projet.

### src/db/

* database.py : Connexion à PostgreSQL, Base, SessionLocal.

### src/auth/

* schemas.py : Schémas Pydantic pour login, register, tokens.
* models.py : Modèle UserAuth ou stockage des refresh tokens.
* services.py : Logique d'authentification (login, register, JWT).
* dependencies.py : get_current_user(), vérification JWT.
* routes.py : Endpoints /register, /login, /refresh, /logout.

### src/users/

* models.py : Modèle User (profil, rôles).
* schemas.py : Schémas Pydantic pour CRUD utilisateurs.
* services.py : CRUD utilisateur et logique métier.
* routes.py : Routes utilisateurs protégées (read, update personnel).

### src/admin/

* routes.py : Routes réservées aux admins.
* services.py : Gestion des rôles et actions admin.

### src/websocket.py

* ws_router : Endpoint websocket `/ws`.

---

## Flux d’authentification JWT

1. Register : création utilisateur, génération access + refresh token.
2. Login : vérification mot de passe, génération tokens.
3. Accès aux routes protégées : header Authorization avec access token, validation via get_current_user().
4. Refresh token : envoi refresh token, vérification DB, rotation tokens.
5. Logout : suppression refresh token, expiration naturelle access token.

---

## Format d’import des routeurs (src/routes/**init**.py)

```python
from fastapi import APIRouter
from src.users.routes import router as users_router
from src.admin.routes import router as admin_router
from src.auth.routes import router as auth_router
from src.websocket import ws_router

router = APIRouter()

# Inclut les sous-routers
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(ws_router)
```

Dans app.py :

```python
from src.routes import router as main_router

app.include_router(main_router)
```

---

## Roadmap du projet

### Phase 1 — Auth

* Auth module complet (register, login, refresh, logout)
* Protection routes via get_current_user()
* Rotation sécurisée refresh tokens

### Phase 2 — Users

* Ajout des rôles
* CRUD utilisateurs
* Update personnel (sans modifier rôle)

### Phase 3 — Admin

* Base du module
* Gestion des rôles utilisateurs
* Dashboard admin

### Phase 4 — Back-End Avancé

* Pagination standardisée
* Permissions RBAC
* Gestion logs d’audit

### Phase 5 — Websocket

* Auth websockets
* Notifications en temps réel

### Phase 6 — Déploiement

* Dockerisation
* CI/CD
* Déploiement serveur / cloud
