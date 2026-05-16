from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.hotel import HotelService
from backend.app.api.deps import get_db
from backend.app.schemas.hotel import HotelRead
from backend.app.models.filter import FHotel

router = APIRouter(tags=["Hotels"])

async def get_hotel_service(
        db: AsyncSession = Depends(get_db)
):
    return HotelService(db)

@router.get("/hotels", response_model=list[HotelRead])
async def get_hotels(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100),
        service: HotelService = Depends(get_hotel_service),
):
    offset = (page - 1) * size
    return await service.get_hotels(limit=size,offset=offset)

@router.get("/hotels/search/address", response_model=list[HotelRead])
async def get_hotels_by_address(
        address: str,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.get_hotels_by_address(address)

@router.get("/hotels/search/name", response_model=list[HotelRead])
async def get_hotels_by_name(
        name: str,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.get_hotels_by_name(name)

@router.get("/hotels/search/filter", response_model=list[HotelRead])
async def get_hotels_by_filter(
        filters: FHotel = Depends(),
        service: HotelService = Depends(get_hotel_service),
):
    return await service.list_hotels_by_filter(
        filters=filters
    )

@router.get("/hotels/popular", response_model=list[HotelRead])
async def get_popular_hotels(
        limit: int = 5,
        service: HotelService = Depends(get_hotel_service),
):
    return await service.get_popular_hotels(limit=limit)
