import psutil

def check_ram():
    ram = psutil.virtual_memory()
    percent = ram.percent
    avail_gb = ram.available / (1024**3)

    return f"Sisa RAM: {avail_gb:.2f} GB (Digunakan: {percent}%)."
