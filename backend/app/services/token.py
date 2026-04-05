from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from datetime import datetime, timezone

from backend.app.models.token import RefreshToken


class TokenService:
    def __init__(self, session: Session):
        self.session = session

    def save_refresh_token(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_revoked=False,
        )
        self.session.add(db_token)
        self.session.commit()
        self.session.refresh(db_token)
        return db_token

    def get_refresh_token(self, token: str) -> RefreshToken:
        db_token = self.session.scalar(
            select(RefreshToken)
            .where(RefreshToken.token == token)
        )
        if db_token is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if db_token.is_revoked:
            raise HTTPException(status_code=401, detail="Token revoked")
        if db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired")

        return db_token

    def revoke_refresh_token(self, token: str) -> bool:
        db_token = self.session.scalar(
            select(RefreshToken)
            .where(RefreshToken.token == token)
        )
        if db_token is None:
            raise HTTPException(status_code=404, detail="Invalid token")
        db_token.is_revoked = True
        self.session.commit()
        return True

    def revoke_all_user_tokens(self, user_id: int) -> None:
        self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(is_revoked=True)
        )
        self.session.commit()

    def clean_up_expired_tokens(self) -> int:
        now = datetime.now(timezone.utc)

        sql = delete(RefreshToken).where(
            (RefreshToken.expires_at < now) |
            (RefreshToken.is_revoked == True)
        )
        result = self.session.execute(sql)
        self.session.commit()
        return result.rowcount
