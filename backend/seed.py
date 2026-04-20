"""
Seed script — заполняет БД отелями, типами комнат и комнатами.
Пользователей НЕ создаёт.

Запуск:
  python -m backend.app.seed_data
  (из корня проекта, где лежит папка backend/)
"""

from backend.app.db.session import SessionLocal
from backend.app.models.hotel import Hotel
from backend.app.models.room import Room
from backend.app.models.room_type import RoomType
from sqlalchemy import select
import random


# ──────────────────────────────────────────────
# Данные
# ──────────────────────────────────────────────

ROOM_TYPES = [
    {"type_name": "general",   "description": "Стандартный номер с базовыми удобствами"},
    {"type_name": "deluxe",    "description": "Улучшенный номер с видом и мини-баром"},
    {"type_name": "family",    "description": "Просторный семейный номер"},
    {"type_name": "suite",     "description": "Люкс с отдельной гостиной"},
    {"type_name": "president", "description": "Президентский люкс — максимальный комфорт"},
]

HOTELS = [
    # Казахстан
    {"name": "The Ritz-Carlton Almaty",     "city": "Almaty",     "address": "Аль-Фараби 77/7",             "stars": 5, "description": "Пятизвёздочный отель в самом сердце Алматы с видом на горы"},
    {"name": "Rixos Almaty",                "city": "Almaty",     "address": "Сейфуллина 506/99",           "stars": 5, "description": "Роскошный отель с спа-центром и ресторанами"},
    {"name": "Rahat Palace Hotel",          "city": "Almaty",     "address": "Сатпаева 29/6",               "stars": 5, "description": "Классический люкс-отель в деловом центре"},
    {"name": "Holiday Inn Almaty",          "city": "Almaty",     "address": "Тимирязева 97",               "stars": 4, "description": "Комфортный бизнес-отель международной сети"},
    {"name": "Kazakhstan Hotel",            "city": "Almaty",     "address": "Достык 52",                   "stars": 3, "description": "Историческая гостиница в центре города"},

    {"name": "Hilton Astana",               "city": "Astana",     "address": "Сарыарка 46",                 "stars": 5, "description": "Современный отель рядом с Байтереком"},
    {"name": "St. Regis Astana",            "city": "Astana",     "address": "Кабанбай Батыра 54",          "stars": 5, "description": "Ультра-люкс в столице с панорамным видом"},
    {"name": "Marriott Astana",             "city": "Astana",     "address": "Достык 1",                    "stars": 4, "description": "Деловой отель у Expo территории"},
    {"name": "Park Inn Astana",             "city": "Astana",     "address": "Туркестан 22",                "stars": 3, "description": "Доступный комфорт в левобережье"},

    {"name": "Rixos Borovoe",               "city": "Borovoe",    "address": "Курортная зона 1",            "stars": 5, "description": "Курортный отель на берегу озера Боровое"},
    {"name": "Keremet Hotel",               "city": "Shymkent",   "address": "Байтурсынова 15",             "stars": 3, "description": "Уютный отель в центре Шымкента"},

    # Международные
    {"name": "Grand Hotel Europa",          "city": "Moscow",     "address": "Тверская 12",                 "stars": 4, "description": "Элегантный отель на главной улице Москвы"},
    {"name": "Bosphorus Palace",            "city": "Istanbul",   "address": "Sultanahmet Mah. 24",         "stars": 5, "description": "Исторический бутик-отель с видом на Босфор"},
    {"name": "Dubai Marina Towers",         "city": "Dubai",      "address": "Marina Walk, Tower B",        "stars": 5, "description": "Небоскрёб-отель на набережной Dubai Marina"},
    {"name": "Sakura Inn",                  "city": "Tokyo",      "address": "Shinjuku 3-14-1",             "stars": 3, "description": "Традиционный японский отель с онсэном"},
    {"name": "Alpine Lodge",               "city": "Zürich",     "address": "Bahnhofstrasse 88",            "stars": 4, "description": "Горный уют в центре Цюриха"},
    {"name": "Georgian Pearl",              "city": "Tbilisi",    "address": "Rustaveli Ave 17",             "stars": 4, "description": "Стильный бутик-отель в старом Тбилиси"},
    {"name": "Silk Road Inn",               "city": "Samarkand",  "address": "Registan Sq 3",               "stars": 3, "description": "Гостиница у площади Регистан"},
    {"name": "Caspian Breeze",              "city": "Baku",       "address": "Neftchilar Ave 55",            "stars": 4, "description": "Современный отель на набережной Каспия"},
    {"name": "Nomad Palace",                "city": "Bishkek",    "address": "Манас проспект 40",            "stars": 3, "description": "Отель в центре Бишкека с национальным колоритом"},
]

# Шаблоны комнат по звёздности отеля
# (room_type_name, capacity, price_range, floors)
ROOM_TEMPLATES = {
    5: [
        ("general",   2, (25000, 40000),  (1, 3)),
        ("general",   2, (28000, 42000),  (1, 3)),
        ("deluxe",    2, (50000, 70000),  (3, 6)),
        ("deluxe",    3, (55000, 75000),  (4, 8)),
        ("family",    4, (65000, 90000),  (2, 5)),
        ("family",    5, (70000, 95000),  (2, 5)),
        ("suite",     3, (90000, 130000), (5, 10)),
        ("suite",     4, (100000, 150000),(6, 12)),
        ("president", 6, (200000, 400000),(8, 15)),
        ("president", 4, (180000, 350000),(10, 20)),
    ],
    4: [
        ("general",   2, (12000, 20000),  (1, 3)),
        ("general",   2, (13000, 22000),  (1, 4)),
        ("general",   3, (15000, 25000),  (1, 3)),
        ("deluxe",    2, (25000, 40000),  (3, 6)),
        ("deluxe",    3, (30000, 45000),  (3, 6)),
        ("family",    4, (35000, 55000),  (2, 5)),
        ("family",    5, (40000, 60000),  (2, 4)),
        ("suite",     3, (60000, 90000),  (4, 8)),
    ],
    3: [
        ("general",   2, (6000, 12000),  (1, 3)),
        ("general",   2, (7000, 13000),  (1, 3)),
        ("general",   3, (8000, 14000),  (1, 2)),
        ("deluxe",    2, (14000, 22000), (2, 4)),
        ("family",    4, (18000, 28000), (1, 3)),
        ("family",    5, (20000, 30000), (1, 3)),
    ],
}

ROOM_DESCRIPTIONS = {
    "general":   [
        "Уютный номер с двуспальной кроватью и рабочей зоной",
        "Стандартный номер с кондиционером и Wi-Fi",
        "Комфортный номер с видом на город",
        "Номер с ортопедическим матрасом и телевизором",
    ],
    "deluxe":    [
        "Улучшенный номер с мини-баром и панорамным окном",
        "Делюкс с отдельной ванной и халатами",
        "Просторный делюкс с видом на горы",
        "Номер повышенного комфорта с балконом",
    ],
    "family":    [
        "Семейный номер с двумя спальнями",
        "Просторный номер с детской зоной и диваном",
        "Семейный люкс с мини-кухней",
        "Номер для семьи с игровым уголком",
    ],
    "suite":     [
        "Люкс с гостиной, спальней и джакузи",
        "Сьют с панорамным видом и рабочим кабинетом",
        "Двухкомнатный люкс с кухней",
        "Роскошный сьют с террасой",
    ],
    "president": [
        "Президентский люкс — две спальни, гостиная, столовая",
        "VIP-апартаменты с личным дворецким",
        "Пентхаус с собственным бассейном и террасой",
        "Королевский сьют на последнем этаже",
    ],
}


def seed():
    session = SessionLocal()
    random.seed(42)  # воспроизводимые данные

    try:
        # ── Проверяем, есть ли уже данные ──
        existing_hotels = session.scalars(select(Hotel)).first()
        if existing_hotels:
            print("⚠️  В БД уже есть отели. Пропускаем сидинг.")
            print("   Если хочешь пересидить — очисти таблицы hotel, room, room_type вручную.")
            return

        # ── 1. Room Types ──
        existing_types = session.scalars(select(RoomType)).all()
        type_map = {rt.type_name: rt for rt in existing_types}

        for rt_data in ROOM_TYPES:
            if rt_data["type_name"] not in type_map:
                rt = RoomType(**rt_data)
                session.add(rt)
                session.flush()
                type_map[rt.type_name] = rt
                print(f"  + RoomType: {rt.type_name}")
            else:
                print(f"  ✓ RoomType уже есть: {rt_data['type_name']}")

        # ── 2. Hotels ──
        hotel_objects = []
        for h_data in HOTELS:
            hotel = Hotel(**h_data)
            session.add(hotel)
            session.flush()
            hotel_objects.append(hotel)
            print(f"  + Hotel: {hotel.name} ({hotel.city}) ★{hotel.stars}")

        # ── 3. Rooms ──
        room_count = 0
        for hotel in hotel_objects:
            star_key = int(hotel.stars)
            if star_key > 5:
                star_key = 5
            if star_key < 3:
                star_key = 3
            templates = ROOM_TEMPLATES.get(star_key, ROOM_TEMPLATES[3])

            room_num_counter = 100
            for type_name, capacity, (price_min, price_max), (floor_min, floor_max) in templates:
                rt = type_map[type_name]
                floor = random.randint(floor_min, floor_max)
                room_num_counter += 1
                room_number = str(floor * 100 + (room_num_counter % 100))

                price = round(random.randint(price_min, price_max) / 500) * 500  # округляем до 500

                desc = random.choice(ROOM_DESCRIPTIONS[type_name])

                room = Room(
                    h_id=hotel.id,
                    room_number=room_number,
                    r_t_id=rt.id,
                    capacity=capacity,
                    price_per_day=float(price),
                    floor=floor,
                    description=desc,
                )
                session.add(room)
                room_count += 1

        session.commit()
        print(f"\n✅ Сидинг завершён!")
        print(f"   Типов комнат: {len(type_map)}")
        print(f"   Отелей:       {len(hotel_objects)}")
        print(f"   Номеров:      {room_count}")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Ошибка: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()