from datetime import datetime, date


class Inputs:

    def text(self,prompt: str) -> str:
            return input(prompt).strip()
    def text_int(self,prompt: str, min_value: int | None = None, max_value: int | None = None ):
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
    def text_yes_no(self,prompt: str = "Enter ur choice, yes or no (y/n)?") -> bool:
            while True:
                s = input(prompt).lower().strip()
                if s in ("y", "yes"):
                    return True
                if s in ("n", "no"):
                    return False
                print("pls enter y/n (y or n) ")
    def text_date_range(self,prompt: str = "Enter date range (YYYY-MM-DD):") -> tuple[date, date] | None:
            while True:
                d_in = input(prompt + " From: ").strip()
                try:
                    d_in = datetime.strptime(d_in, "%Y-%m-%d").date()
                except ValueError:
                    print("Enter valid date (YYYY-MM-DD) format only")
                    continue
                d_out = input(prompt + " To: ").strip()
                try:
                    d_out = datetime.strptime(d_out, "%Y-%m-%d").date()
                except ValueError:
                    print("Enter valid date (YYYY-MM-DD) format only")
                    continue
                if d_in > d_out:
                    print("From date must be before To date")
                    continue
                return d_in, d_out
    def text_email(self,prompt: str = "Enter email:") -> str | None:
        while True:
            email = input(prompt).strip()
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
