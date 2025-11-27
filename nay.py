from colorama import Fore, Style, init
import os

#ImportTools
from file_tool import organize_downloads
from system_tool import check_ram
from database_tool import find_user
from calendar_tool import list_events, add_event  

init()

def ai_response(user_input):
    text = user_input.lower()

    
    if "rapikan" in text or "organize" in text:
        path = os.path.expanduser("~/Downloads")
        return organize_downloads(path)

    #cekRam
    if "cek ram" in text or "sisa ram" in text:
        return check_ram()

    #MencariData
    if "cari data" in text or "user" in text:
        nama = text.split("user")[-1].strip()
        return find_user(nama)

    #goggleCalendar_lihatAgenda
    if "lihat agenda" in text:
        tanggal = text.replace("lihat agenda", "").strip()
        if tanggal == "":
            return "Masukkan tanggalnya. Contoh: lihat agenda tanggal 2 desember"
        return list_events(tanggal)

    #googleCalendar_TambahAgenda 
    if "tambah agenda" in text:
        teks = text.replace("tambah agenda", "").strip()
        if "judul" not in teks:
            return ("Format salah.\n"
                    "Contoh: tambah agenda 7 Desember jam 7:00 yyk gatering")

        bagian = teks.split("judul")
        tanggal = bagian[0].strip()
        judul = bagian[1].strip()

        return add_event(tanggal, judul)

    return "Maaf, aku belum mengerti perintah itu."

def main():
    print(Fore.BLUE + "=============== SELAMAT DATANG DI WELCOM ===============")
    print(Fore.BLUE + "=========== Neo Assistant for Your Automation ===========")
    print(Fore.LIGHTMAGENTA_EX + "Ketik 'exit' untuk keluar.\n")

    while True:
        user = input(Fore.GREEN + "Anda : " + Style.RESET_ALL)
        
        if user.lower() == "exit":
            print(Fore.YELLOW + "AI : Sampai jumpa!\n")
            break

        response = ai_response(user)
        print(Fore.WHITE + "AI :", response, "\n")

if __name__ == "__main__":
    main()
