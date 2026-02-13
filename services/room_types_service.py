from models.room_types import RoomType

def choose_room_type():
    print("Choose what type of room u want!")
    print('''
1) DELUXE
2) GENERAL
3) PRESIDENT
4) FAMILY
0) back
    ''')
    while True:
        choice = input("Enter choice: ")

        if choice == "0":
            break
        elif choice == "1":
            return RoomType.DELUXE
        elif choice == "2":
            return RoomType.GENERAL
        elif choice == "3":
            return RoomType.PRESIDENT
        elif choice == "4":
            return RoomType.FAMILY
        else:
            print("Enter again right choice")