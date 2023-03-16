# Ideally, users should come from a database
users = {"electric_websockets_cp_1": "012c3680-d93d-42db-969e-3ce277129078"}


async def check_credentials(username: str, password: str) -> bool:
    if username in users and password == users[username]:
        return True
    return False
