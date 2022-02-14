import time

INTERVAL = {}

async def check_spam(user_id: int):
    if str(user_id) in INTERVAL:
        now_time = time.time()
        last_time = INTERVAL[str(user_id)]
        if round(now_time - last_time) < 120:
            return True, round(last_time - now_time + 120)
        elif round(now_time - last_time) >= 120:
            del INTERVAL[str(user_id)]
            return False, None
    elif str(user_id) not in INTERVAL:
        INTERVAL[str(user_id)] = time.time()
        return False, None
