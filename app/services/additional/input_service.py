from datetime import datetime, date


class Inputs:

    @staticmethod
    def text(prompt: str) -> str | None:
            x = input(prompt).strip()
            if x == "0":
                print("Canceled!")
                return None
            return x
    @staticmethod
    def text_int(prompt: str, min_value: int | None = None, max_value: int | None = None ):
            while True:
                s = input(prompt)
                try:
                    value = int(s)
                except ValueError:
                    print("Enter integer!")
                    continue
                if min_value is not None and value < min_value:
                    print(f"Enter value greater than {min_value}")
                    continue
                if max_value is not None and value > max_value:
                    print(f"Enter value less than {max_value}")
                    continue
                return value

    @staticmethod
    def text_float(prompt: str, min_value: int | None = None, max_value: int | None = None):
        while True:
            s = input(prompt)
            try:
                value = float(s)
            except ValueError:
                print("Enter integer!")
                continue
            if min_value is not None and value < min_value:
                print(f"Enter value greater than {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Enter value less than {max_value}")
                continue
            return value

    @staticmethod
    def text_yes_no(prompt: str = "Enter ur choice, yes or no (y/n)?") -> bool:
            while True:
                s = input(prompt).lower().strip()
                if s in ("y", "yes"):
                    return True
                if s in ("n", "no"):
                    return False
                print("pls enter y/n (y or n) ")
    @staticmethod
    def text_date_range(prompt: str = "Enter date range (YYYY-MM-DD):") -> tuple[date, date] | None:
            while True:
                d_in = input(prompt + " From(0 to exit): ").strip()
                if d_in == "0":
                    return None
                try:
                    d_in = datetime.strptime(d_in, "%Y-%m-%d").date()
                except ValueError:
                    print("Enter valid date (YYYY-MM-DD) format only")
                    continue
                if d_in < date.today():
                    print("Date must be today or in future")
                    continue
                d_out = input(prompt + " To(0 to exit): ").strip()
                if d_out == "0":
                    return None
                try:
                    d_out = datetime.strptime(d_out, "%Y-%m-%d").date()
                except ValueError:
                    print("Enter valid date (YYYY-MM-DD) format only")
                    continue
                if d_in > d_out:
                    print("From date must be before To date")
                    continue
                return d_in, d_out

    @staticmethod
    def text_email(prompt: str = "Enter email:") -> str | None:
        while True:
            email = input(prompt).strip()
            if email == "0":
                print("Canceled!")
                return None
            if " " in email:
                print("Email cannot contain spaces")
                continue
            if email.count("@") != 1:
                print("Email must contain one @")
                continue
            index = email.index("@")
            if index < 1:
                print("Email must start with letter")
                continue

            if index + 1 >= len(email):
                print("Email must contain domain after @")
                continue

            if email[index + 1] == '.':
                print("Email must end with letter")
                continue
            if email.find(".", index) == -1:
                print("Email must contain dot")
                continue
            last_dot = email.rfind(".")
            if len(email[last_dot + 1:]) < 2:
                print("Email must contain at least 2 letters after dot")
                continue
            return email

    @staticmethod
    def text_password(prompt: str = "Enter password:") -> str | None:
        while True:
            password = input(prompt).strip()
            if password == "0":
                print("Canceled!")
                return None
            if len(password) < 8:
                print("Password must be at least 8 characters long")
                continue
            return password