import random
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import select, text
from backend.app.db.session import SessionLocal
from backend.app.models.hotel import Hotel
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from backend.app.models.booking import Booking, Status
from backend.app.models.review import Review

# Твои параметры
USER_IDS = [13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25]
ROOM_TYPE_IDS = [1, 2, 3, 4, 5]

HOTELS_DATA = [
    {"name": "Esentai Royal", "city": "Almaty", "stars": 5, "address": "Аль-Фараби 77/7"},
    {"name": "Astana Garden", "city": "Astana", "stars": 4, "address": "Мангилик Ел 10"},
    {"name": "Shymkent Plaza Hotel", "city": "Shymkent", "stars": 4, "address": "пр. Тауке Хана"},
    {"name": "Caspian Star", "city": "Aktau", "stars": 5, "address": "15-й микрорайон"},
    {"name": "Medeu Camp", "city": "Almaty", "stars": 3, "address": "Горная 465"},
]

REVIEWS_TEMPLATES = {
    5: ["Превосходно! Очень понравилось.", "Лучший отель в моей жизни.", "Чисто, уютно, сервис 10/10."],
    4: ["Хорошее место, рекомендую.", "Все понравилось, но завтрак мог быть лучше.", "Удобное расположение."],
    3: ["Обычный отель. Ничего особенного.", "Цена соответствует качеству.", "Нормально, но в номере было шумно."],
}

def seed():
    session = SessionLocal()
    try:
        # 1. Очистка (не трогаем room_types и users)
        print("🧹 Очистка данных (отели, комнаты, брони, отзывы)...")
        session.execute(text("TRUNCATE TABLE review RESTART IDENTITY CASCADE;"))
        session.execute(text("TRUNCATE TABLE bookings RESTART IDENTITY CASCADE;"))
        session.execute(text("TRUNCATE TABLE rooms RESTART IDENTITY CASCADE;"))
        session.execute(text("TRUNCATE TABLE hotels RESTART IDENTITY CASCADE;"))
        session.commit()

        # 2. Создание отелей
        print("🏢 Создание отелей...")
        hotel_objs = []
        for h in HOTELS_DATA:
            hotel = Hotel(
                name=h["name"],
                city=h["city"],
                stars=h["stars"],
                address=h["address"],
                description="Описание создано автоматически при сидинге.",
                rating_sum=Decimal("0.0"),
                rating_count=0
            )
            session.add(hotel)
            hotel_objs.append(hotel)
        session.flush()

        # 3. Создание комнат (используем существующие room_types 1-5)
        print("🔑 Создание комнат...")
        rooms_pool = []
        for hotel in hotel_objs:
            for i in range(1, 6): # по 5 комнат на отель
                room = Room(
                    h_id=hotel.id,
                    room_number=f"{hotel.id}{i:02d}",
                    r_t_id=random.choice(ROOM_TYPE_IDS),
                    capacity=random.randint(1, 4),
                    price_per_day=Decimal(str(random.randint(12000, 95000))),
                    floor=random.randint(1, 12),
                    description="Комфортабельный номер со всеми удобствами."
                )
                session.add(room)
                rooms_pool.append(room)
        session.flush()

        # 4. Бронирования и Отзывы
        print("📅 Заполнение истории юзеров (13-25)...")
        b_count = 0
        r_count = 0

        for u_id in USER_IDS:
            # Делаем по 3-5 бронирований на каждого юзера
            for _ in range(random.randint(3, 5)):
                room = random.choice(rooms_pool)

                days_ago = random.randint(5, 60)
                check_in = datetime.now() - timedelta(days=days_ago)
                check_out = check_in + timedelta(days=random.randint(1, 5))

                booking = Booking(
                    user_id=u_id,
                    r_id=room.id,
                    check_in=check_in,
                    check_out=check_out,
                    status=Status.CONFIRMED, # Как ты и просил
                    total_price=room.price_per_day * 2,
                    guest_count=random.randint(1, room.capacity)
                )
                session.add(booking)
                session.flush()
                b_count += 1

                # Генерируем отзыв к бронированию
                rating_val = random.choices([5, 4, 3], weights=[40, 45, 15])[0]
                review = Review(
                    user_id=u_id,
                    booking_id=booking.id,
                    hotel_id=room.h_id,
                    rating=Decimal(str(rating_val)),
                    comment=random.choice(REVIEWS_TEMPLATES[rating_val])
                )
                session.add(review)

                # ОБНОВЛЯЕМ РЕЙТИНГ ОТЕЛЯ
                hotel_to_update = session.get(Hotel, room.h_id)
                hotel_to_update.rating_sum += Decimal(str(rating_val))
                hotel_to_update.rating_count += 1
                r_count += 1

        session.commit()
        print(f"\n✅ Сидинг успешно завершен!")
        print(f"--- Создано отелей: {len(hotel_objs)}")
        print(f"--- Создано комнат: {len(rooms_pool)}")
        print(f"--- Бронирований:   {b_count}")
        print(f"--- Отзывов:        {r_count}")

    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка сидинга: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()