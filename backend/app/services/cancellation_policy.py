from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import CancellationPolicy, Hotel


class CancellationPolicyService:
    def __init__(self, session: Session):
        self.session = session

    def add_policy(self, data) -> CancellationPolicy:
        new = CancellationPolicy(
            name=data.name,
            hours_before=data.hours_before,
            penalty_percent=data.penalty_percent,
        )
        self.session.add(new)
        self.session.commit()
        self.session.refresh(new)
        return new

    def delete_policy(self, policy_id: int) -> bool:
        policy = self.session.scalar(
            select(CancellationPolicy).where(CancellationPolicy.id == policy_id)
        )
        if policy:
            active_hotels = self.session.scalar(
                select(Hotel).where(Hotel.cancellation_policy_id == policy_id)
            )
            if active_hotels:
                raise "PolicyHaveActiveHotelError"
            self.session.delete(policy)
            self.session.commit()
            return True
        return False