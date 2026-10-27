# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN, CLOSE = 9, 21
MAX_HOURS = 3
MAX_PER_DAY = 2


def _is_int(x):
    # True/False 는 파이썬에서 int 의 일종이지만 시각으로 인정하지 않는다
    return type(x) is int


def _valid_place(room, day):
    return room in ROOMS and day in DAYS


class RoomBooking:
    def __init__(self):
        # (강의실, 요일) -> [(start, end, name), ...]
        self._bookings = {}

    def book(self, room, day, start, end, name):
        if not _valid_place(room, day):
            return False
        if not (_is_int(start) and _is_int(end)):
            return False
        # 이름이 비었거나 공백뿐이면 누가 예약했는지 알 수 없으므로 거절
        if not isinstance(name, str) or not name.strip():
            return False
        if start < OPEN or end > CLOSE:
            return False
        if start >= end:
            return False
        if end - start > MAX_HOURS:
            return False

        slots = self._bookings.get((room, day), [])
        # 끝나는 시각에 바로 시작하는 것은 겹치지 않는다
        if any(start < e and s < end for s, e, _ in slots):
            return False

        # 같은 요일이면 강의실이 달라도 합산
        count = sum(
            1
            for (r, d), items in self._bookings.items()
            if d == day
            for _, _, n in items
            if n == name
        )
        if count >= MAX_PER_DAY:
            return False

        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_int(start):
            return False
        slots = self._bookings.get((room, day), [])
        for i, (s, e, n) in enumerate(slots):
            if s == start:
                if n != name:
                    return False
                del slots[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        return sorted(self._bookings.get((room, day), []))
