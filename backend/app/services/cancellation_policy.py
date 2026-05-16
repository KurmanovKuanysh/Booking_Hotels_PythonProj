from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.exceptions import PolicyHaveActiveHotelError
from backend.app.models import CancellationPolicy, Hotel


class CancellationPolicyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_policy(self, data) -> CancellationPolicy:
        new = CancellationPolicy(
            name=data.name,
            hours_before=data.hours_before,
            penalty_percent=data.penalty_percent,
        )
        self.session.add(new)
        await self.session.commit()
        await self.session.refresh(new)
        return new

    async def delete_policy(self, policy_id: int) -> bool:
        policy = await self.session.scalar(
            select(CancellationPolicy).where(CancellationPolicy.id == policy_id)
        )
        if policy:
            active_hotels = await self.session.scalar(
                select(Hotel).where(Hotel.policy_id == policy_id)
            )
            if active_hotels:
                raise PolicyHaveActiveHotelError
            await self.session.delete(policy)
            await self.session.commit()
            return True
        return False