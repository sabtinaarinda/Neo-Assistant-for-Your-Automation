fake_db = {
    "budi": {"umur": 20, "kota": "Jakarta"},
    "sinta": {"umur": 22, "kota": "Bandung"},
    "andi": {"umur": 19, "kota": "Surabaya"},
}

def find_user(name):
    name = name.lower()
    if name in fake_db:
        data = fake_db[name]
        return f"User ditemukan: {name.title()} | Umur: {data['umur']} | Kota: {data['kota']}"
    return "User tidak ditemukan!"
