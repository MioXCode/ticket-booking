import pandas as pd
import os
from datetime import datetime
from tabulate import tabulate
import sys


csv_file = "/home/tomio/Documents/Project/ticket-booking/csv/data_tiket.csv"
BACKUP_DIR = "/home/tomio/Documents/Project/ticket-booking/backup/"


def init_csv():

    if not os.path.exists(csv_file):
        df = pd.DataFrame(
            columns=[
                "ID Transaksi",
                "Judul Film",
                "Jumlah Tiket",
                "Jam Tayang",
                "Total Harga",
                "Tanggal Pemesanan",
            ]
        )
        df.to_csv(csv_file, index=False)

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def backup_data():

    if os.path.exists(csv_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.csv")
        df = pd.read_csv(csv_file)
        df.to_csv(backup_file, index=False)
        print(f"Backup berhasil dibuat: {backup_file}")


def show_movies():

    movies = {
        1: {
            "judul": "Film A",
            "jam_tayang": ["14:00", "16:30", "19:00"],
            "harga": 50000,
            "tiket_tersedia": 50,
            "genre": "Action",
            "durasi": "120 menit",
        },
        2: {
            "judul": "Film B",
            "jam_tayang": ["13:00", "15:30", "21:00"],
            "harga": 60000,
            "tiket_tersedia": 40,
            "genre": "Comedy",
            "durasi": "105 menit",
        },
        3: {
            "judul": "Film C",
            "jam_tayang": ["12:00", "15:00", "18:00"],
            "harga": 45000,
            "tiket_tersedia": 30,
            "genre": "Horror",
            "durasi": "90 menit",
        },
    }

    headers = [
        "No",
        "Judul",
        "Jam Tayang",
        "Harga",
        "Tiket Tersedia",
        "Genre",
        "Durasi",
    ]
    table_data = []

    for no, data in movies.items():
        table_data.append(
            [
                no,
                data["judul"],
                ", ".join(data["jam_tayang"]),
                f"Rp {data['harga']:,}",
                data["tiket_tersedia"],
                data["genre"],
                data["durasi"],
            ]
        )

    print("\n=== DAFTAR FILM ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    return movies


def add_tiket(no_film, jumlah_tiket, jam_terpilih):

    movies = show_movies()

    if no_film not in movies:
        print("Error: Nomor film tidak valid!")
        return False

    film = movies[no_film]
    if jam_terpilih not in film["jam_tayang"]:
        print("Error: Jam tayang tidak valid!")
        return False

    if jumlah_tiket > film["tiket_tersedia"]:
        print("Error: Tiket tidak mencukupi!")
        return False

    if jumlah_tiket <= 0:
        print("Error: Jumlah tiket harus lebih dari 0!")
        return False

    total_harga = jumlah_tiket * film["harga"]

    transaction_id = datetime.now().strftime("TRX%Y%m%d%H%M%S")

    new_data = pd.DataFrame(
        [
            [
                transaction_id,
                film["judul"],
                jumlah_tiket,
                jam_terpilih,
                total_harga,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ]
        ],
        columns=[
            "ID Transaksi",
            "Judul Film",
            "Jumlah Tiket",
            "Jam Tayang",
            "Total Harga",
            "Tanggal Pemesanan",
        ],
    )

    try:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv(csv_file, index=False)
        print("\nPemesanan Berhasil!")
        print(f"ID Transaksi: {transaction_id}")
        print(f"Film: {film['judul']}")
        print(f"Jam Tayang: {jam_terpilih}")
        print(f"Jumlah Tiket: {jumlah_tiket}")
        print(f"Total Harga: Rp {total_harga:,}")
        return True
    except Exception as e:
        print(f"Error saat menyimpan data: {str(e)}")
        return False


def lihat_riwayat():

    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        if len(df) > 0:
            print("\n=== RIWAYAT PEMESANAN ===")

            df["Total Harga"] = df["Total Harga"].apply(lambda x: f"Rp {x:,}")
            print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
        else:
            print("Belum ada riwayat pemesanan.")
    else:
        print("Belum ada riwayat pemesanan.")


def menu():

    while True:
        print("\n" + "=" * 50)
        print("SISTEM PEMESANAN TIKET BIOSKOP".center(50))
        print("=" * 50)
        print("\n1. Pesan Tiket")
        print("2. Lihat Riwayat")
        print("3. Backup Data")
        print("4. Keluar\n")
        print("=" * 50)

        try:
            pil_menu = input("Pilih Menu (1-4): ")

            if pil_menu == "1":
                show_movies()
                try:
                    no_film = int(input("\nMasukkan nomor film: "))
                    movies = show_movies()
                    if no_film in movies:
                        print(
                            f"\nJam tayang tersedia: {', '.join(movies[no_film]['jam_tayang'])}"
                        )
                        jam_terpilih = input("Pilih jam tayang: ")
                        jumlah_tiket = int(input("Masukkan jumlah tiket: "))
                        add_tiket(no_film, jumlah_tiket, jam_terpilih)
                    else:
                        print("Nomor film tidak valid!")
                except ValueError:
                    print("Error: Input harus berupa angka!")
            elif pil_menu == "2":
                lihat_riwayat()
            elif pil_menu == "3":
                backup_data()
            elif pil_menu == "4":
                print("\nTerima kasih telah menggunakan layanan kami!")
                sys.exit(0)
            else:
                print("Pilihan tidak valid. Silakan pilih kembali.")
        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh pengguna.")
            sys.exit(0)


if __name__ == "__main__":
    try:
        init_csv()
        menu()
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        sys.exit(1)
