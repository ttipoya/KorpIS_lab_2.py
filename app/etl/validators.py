import re
from datetime import datetime
from typing import Optional

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?\d[\d\-\s()]{4,}\d$")

class DataValidator:
    def validate_email(self, email: Optional[str]) -> bool:
        if not email or not isinstance(email, str):
            return False
        return bool(EMAIL_RE.match(email.strip()))

    def validate_phone(self, phone: Optional[str]) -> bool:
        if not phone or not isinstance(phone, str):
            return False
        return bool(PHONE_RE.match(phone.strip()))

    def validate_date(self, v: Optional[str]) -> bool:
        if not v or not isinstance(v, str):
            return False
        for fmt in ('%Y-%m-%d','%d.%m.%Y','%Y/%m/%d','%d/%m/%Y'):
            try:
                datetime.strptime(v.strip(), fmt)
                return True
            except Exception:
                continue
        return False

    def parse_date(self, v: Optional[str]):
        if not v or not isinstance(v, str):
            return None
        for fmt in ('%Y-%m-%d','%d.%m.%Y','%Y/%m/%d','%d/%m/%Y'):
            try:
                return datetime.strptime(v.strip(), fmt).date()
            except Exception:
                continue
        return None
