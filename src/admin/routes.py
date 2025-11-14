from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.admin.services import get_db
from src.auth.dependencies import require_role
from src.users.models import UserRole, User
from src.users.schemas import UserResponse, UserUpdate
from src.users.services import get_all_users, get_user
from src.auth.services import get_current_user

router = APIRouter()

@router.get("/users", response_model=list[UserResponse],
             dependencies=[Depends(require_role([UserRole.admin]))])
def list_users(db: Session = Depends(get_db)):
    """
    Liste tous les utilisateurs (admin only)
    """
    return get_all_users(db)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}/role", response_model=UserResponse,
             dependencies=[Depends(require_role([UserRole.admin]))])
def update_user_role(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Permet à un admin de modifier le rôle d’un utilisateur.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    if update_data.role is None:
        raise HTTPException(status_code=400, detail="Role field required!")

    user.role = update_data.role
    db.commit()
    db.refresh(user)
    return user
