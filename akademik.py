import mysql.connector

# === KONEKSI DATABASE ===
db = mysql.connector.connect(
    host="localhost",
    user="root",      # ganti sesuai user MySQL
    password="",      # ganti sesuai password MySQL
    database="akademik"
)
cursor = db.cursor()

# === LOGIN ===
def login():
    print("\n=== SISTEM AKADEMIK ===")
    print("1. Login Admin")
    print("2. Login Mahasiswa")
    print("0. Keluar")
    pilihan = input("Pilih login sebagai (1/2/0): ")

    if pilihan == "0":
        print("Keluar...")
        exit()

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if not user:
        print("Login gagal! Cek username/password.")
        return None

    role = user[3]
    if pilihan == "1" and role == "admin":
        print(f"Login berhasil sebagai Admin ({username})")
        return ("admin", user)
    elif pilihan == "2" and role == "mahasiswa":
        print(f"Login berhasil sebagai Mahasiswa ({username})")
        return ("mahasiswa", user)
    else:
        print("Role tidak sesuai dengan pilihan login.")
        return None

# === KELOLA MAHASISWA ===
def menu_mahasiswa_admin():
    while True:
        print("\n--- KELOLA MAHASISWA ---")
        print("1. Lihat Data Mahasiswa")
        print("2. Tambah Mahasiswa")
        print("3. Update Mahasiswa")
        print("4. Hapus Mahasiswa")
        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("SELECT * FROM mahasiswa")
            for m in cursor.fetchall():
                print(f"NIM: {m[0]} | Nama: {m[1]} | Jurusan: {m[2]} | Angkatan: {m[3]}")

        elif pilih == "2":
            nim = input("Masukkan NIM: ")
            nama = input("Masukkan Nama: ")
            jurusan = input("Masukkan Jurusan: ")
            angkatan = int(input("Masukkan Angkatan: "))
            cursor.execute("INSERT INTO mahasiswa VALUES (%s,%s,%s,%s)", (nim, nama, jurusan, angkatan))
            cursor.execute("INSERT INTO users (username,password,role,nim) VALUES (%s,%s,'mahasiswa',%s)",
                           (nim, nim, nim))
            db.commit()
            print("Mahasiswa berhasil ditambahkan!")

        elif pilih == "3":
            nim = input("Masukkan NIM Mahasiswa yang mau diupdate: ")
            nama = input("Nama baru: ")
            jurusan = input("Jurusan baru: ")
            angkatan = int(input("Angkatan baru: "))
            cursor.execute("UPDATE mahasiswa SET nama=%s,jurusan=%s,angkatan=%s WHERE nim=%s",
                           (nama, jurusan, angkatan, nim))
            db.commit()
            print("Data mahasiswa berhasil diupdate!")

        elif pilih == "4":
            nim = input("Masukkan NIM Mahasiswa yang mau dihapus: ")
            try:
                cursor.execute("DELETE FROM mahasiswa WHERE nim=%s", (nim,))
                cursor.execute("DELETE FROM users WHERE nim=%s", (nim,))
                db.commit()
                print("Mahasiswa berhasil dihapus!")
            except mysql.connector.Error as e:
                print(f"Gagal menghapus: {e}")

        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === KELOLA DOSEN ===
def menu_dosen_admin():
    while True:
        print("\n--- KELOLA DOSEN ---")
        print("1. Lihat Data Dosen")
        print("2. Tambah Dosen")
        print("3. Update Dosen")
        print("4. Hapus Dosen")
        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("SELECT * FROM dosen")
            for d in cursor.fetchall():
                print(f"NIDN: {d[0]} | Nama: {d[1]} | Prodi: {d[2]}")

        elif pilih == "2":
            nidn = input("Masukkan NIDN: ")
            nama = input("Masukkan Nama: ")
            prodi = input("Masukkan Prodi: ")
            cursor.execute("INSERT INTO dosen VALUES (%s,%s,%s)", (nidn, nama, prodi))
            cursor.execute("INSERT INTO users (username,password,role,nidn) VALUES (%s,%s,'dosen',%s)",
                           (nidn, nidn, nidn))
            db.commit()
            print("Dosen berhasil ditambahkan!")

        elif pilih == "3":
            nidn = input("Masukkan NIDN yang mau diupdate: ")
            nama = input("Nama baru: ")
            prodi = input("Prodi baru: ")
            cursor.execute("UPDATE dosen SET nama=%s,prodi=%s WHERE nidn=%s", (nama, prodi, nidn))
            db.commit()
            print("Data dosen berhasil diupdate!")

        elif pilih == "4":
            nidn = input("Masukkan NIDN yang mau dihapus: ")
            try:
                cursor.execute("DELETE FROM dosen WHERE nidn=%s", (nidn,))
                cursor.execute("DELETE FROM users WHERE nidn=%s", (nidn,))
                db.commit()
                print("Dosen berhasil dihapus!")
            except mysql.connector.Error as e:
                print(f"Gagal menghapus: {e}")

        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === KELOLA MATA KULIAH ===
def menu_matkul_admin():
    while True:
        print("\n--- KELOLA MATA KULIAH ---")
        print("1. Lihat Mata Kuliah")
        print("2. Tambah Mata Kuliah")
        print("3. Update Mata Kuliah")
        print("4. Hapus Mata Kuliah")
        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("SELECT * FROM matkul")
            for mk in cursor.fetchall():
                print(f"Kode: {mk[0]} | Nama: {mk[1]} | SKS: {mk[2]} | NIDN: {mk[3]}")

        elif pilih == "2":
            kode = input("Kode MK: ")
            nama = input("Nama MK: ")
            sks = int(input("SKS: "))
            nidn = input("NIDN Dosen: ")
            cursor.execute("INSERT INTO matkul VALUES (%s,%s,%s,%s)", (kode, nama, sks, nidn))
            db.commit()
            print("Mata kuliah berhasil ditambahkan!")

        elif pilih == "3":
            kode = input("Kode MK yang mau diupdate: ")
            nama = input("Nama baru: ")
            sks = int(input("SKS baru: "))
            nidn = input("NIDN baru: ")
            cursor.execute("UPDATE matkul SET nama_mk=%s,sks=%s,nidn=%s WHERE kode_mk=%s",
                           (nama, sks, nidn, kode))
            db.commit()
            print("Mata kuliah berhasil diupdate!")

        elif pilih == "4":
            kode = input("Kode MK yang mau dihapus: ")
            cursor.execute("DELETE FROM matkul WHERE kode_mk=%s", (kode,))
            db.commit()
            print("Mata kuliah berhasil dihapus!")

        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === KELOLA KRS ===
def menu_krs_admin():
    while True:
        print("\n--- KELOLA KRS ---")
        print("1. Lihat Data KRS")
        print("2. Tambah KRS")
        print("3. Update KRS")
        print("4. Hapus KRS")
        print("0. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("SELECT * FROM krs")
            for k in cursor.fetchall():
                print(f"NIM: {k[1]} | Kode MK: {k[2]} | Semester: {k[3]} | Nilai: {k[4]}")

        elif pilih == "2":
            nim = input("Masukkan NIM: ")
            kode = input("Masukkan Kode Matkul: ")
            try:
                semester = int(input("Masukkan Semester (angka): "))
            except ValueError:
                print("Semester harus berupa angka!")
                continue
            nilai = input("Masukkan Nilai: ")
            cursor.execute("INSERT INTO krs (nim,kode_mk,semester,nilai) VALUES (%s,%s,%s,%s)",
                           (nim, kode, semester, nilai))
            db.commit()
            print("KRS berhasil ditambahkan!")

        elif pilih == "3":
            nim = input("Masukkan NIM: ")
            kode = input("Masukkan Kode Matkul: ")
            try:
                semester = int(input("Masukkan Semester (angka): "))
            except ValueError:
                print("Semester harus berupa angka!")
                continue
            nilai = input("Nilai baru: ")
            cursor.execute("UPDATE krs SET nilai=%s WHERE nim=%s AND kode_mk=%s AND semester=%s",
                           (nilai, nim, kode, semester))
            db.commit()
            print("KRS berhasil diupdate!")

        elif pilih == "4":
            nim = input("Masukkan NIM: ")
            kode = input("Masukkan Kode Matkul: ")
            try:
                semester = int(input("Masukkan Semester (angka): "))
            except ValueError:
                print("Semester harus berupa angka!")
                continue
            cursor.execute("DELETE FROM krs WHERE nim=%s AND kode_mk=%s AND semester=%s",
                           (nim, kode, semester))
            db.commit()
            print("KRS berhasil dihapus!")

        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === MENU ADMIN ===
def menu_admin():
    while True:
        print("\n--- MENU ADMIN ---")
        print("1. Kelola Mahasiswa")
        print("2. Kelola Dosen")
        print("3. Kelola Mata Kuliah")
        print("4. Kelola KRS")
        print("0. Logout")
        pilih = input("Pilih: ")

        if pilih == "1":
            menu_mahasiswa_admin()
        elif pilih == "2":
            menu_dosen_admin()
        elif pilih == "3":
            menu_matkul_admin()
        elif pilih == "4":
            menu_krs_admin()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === MENU MAHASISWA ===
def menu_mahasiswa(user):
    nim = user[4]
    cursor.execute("SELECT * FROM mahasiswa WHERE nim=%s", (nim,))
    mhs = cursor.fetchone()
    print(f"\nSelamat datang, {mhs[1]} (NIM: {mhs[0]})")

    while True:
        print("\n--- MENU MAHASISWA ---")
        print("1. Lihat Profil")
        print("2. Lihat Nilai per Semester")
        print("3. Lihat Mata Kuliah")
        print("4. Lihat Data Dosen")
        print("0. Logout")
        pilih = input("Pilih: ")

        if pilih == "1":
            print(f"NIM: {mhs[0]} | Nama: {mhs[1]} | Jurusan: {mhs[2]} | Angkatan: {mhs[3]}")
        elif pilih == "2":
            try:
                semester = int(input("Masukkan Semester: "))
            except ValueError:
                print("Semester harus berupa angka!")
                continue
            cursor.execute("""
                SELECT matkul.nama_mk, matkul.sks, krs.nilai 
                FROM krs 
                JOIN matkul ON krs.kode_mk = matkul.kode_mk 
                WHERE krs.nim=%s AND krs.semester=%s
            """, (nim, semester))
            hasil = cursor.fetchall()
            if not hasil:
                print("Belum ada nilai.")
            else:
                print(f"\n--- Nilai Semester {semester} ---")
                for row in hasil:
                    print(f"{row[0]} ({row[1]} SKS) -> Nilai: {row[2]}")
        elif pilih == "3":
            cursor.execute("SELECT * FROM matkul")
            for mk in cursor.fetchall():
                print(f"Kode: {mk[0]} | Nama: {mk[1]} | SKS: {mk[2]} | NIDN: {mk[3]}")
        elif pilih == "4":
            cursor.execute("SELECT * FROM dosen")
            for dsn in cursor.fetchall():
                print(f"NIDN: {dsn[0]} | Nama: {dsn[1]} | Prodi: {dsn[2]}")
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")

# === MAIN PROGRAM ===
while True:
    user_login = login()
    if user_login:
        role, user = user_login
        if role == "admin":
            menu_admin()
        elif role == "mahasiswa":
            menu_mahasiswa(user)
