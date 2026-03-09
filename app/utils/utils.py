from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text, BIGINT, String, Numeric, Date
from datetime import date
from typing import Any, Optional

int_big = Annotated[int, mapped_column(BIGINT)]
text = Annotated[str, mapped_column(Text)]
str_100 = Annotated[str, mapped_column(String(100))]
numeric_10_2 = Annotated[float, mapped_column(Numeric(10,2))]
date_ = Annotated[date, mapped_column(Date)]
