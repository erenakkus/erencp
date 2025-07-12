#!/usr/bin/env python3
import os
import sys
import getpass

class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'

def printc(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")

def ask(question, default="E"):
    default = default.upper()
    while True:
        ans = input(f"{question} [{default}/H]: ").strip().upper()
        if ans == "":
            ans = default
        if ans in ["E", "H"]:
            return ans == "E"
        print("Lütfen sadece 'E' veya 'H' yazınız.")

def mandatory_input(prompt):
    while True:
        val = input(prompt).strip()
        if val != "":
            return val
        print("Bu alan boş bırakılamaz, lütfen bir değer girin.")

def main():
    printc("📦  ERENCP – Dosya ve Veritabanı Taşıma Aracı\n", Colors.HEADER)

    remote_ip = mandatory_input("🔹 Karşı sunucu IP adresi: ")
    remote_user = mandatory_input("🔹 Karşı sunucu kullanıcı adı: ")

    use_sshpass = ask("🔐 Şifre ile SSH bağlantısı kullanılsın mı?", "H")
    if use_sshpass:
        remote_pass = getpass.getpass("🔐 Karşı sunucu SSH şifresi: ")
    else:
        remote_pass = None

    remote_path = mandatory_input("🔹 Karşı sunucuda taşınacak dizin (/var/www/html): ")

    db_transfer = ask("🗄️ Veritabanı taşınacak mı?", "H")

    if db_transfer:
        remote_db_name = mandatory_input("🔹 Taşınacak veritabanı adı: ")
        remote_db_user = mandatory_input("🔹 Veritabanı kullanıcı adı (uzak): ")
        remote_db_pass = getpass.getpass("🔐 Veritabanı şifresi (uzak): ")
        
        local_db_import = mandatory_input("🔹 Yeni veritabanı adı (yerel): ")
        local_db_user = mandatory_input("🔹 Veritabanı kullanıcı adı (yerel): ")
        local_db_pass = getpass.getpass("🔐 Veritabanı şifresi (yerel): ")
    else:
        remote_db_name = remote_db_user = remote_db_pass = None
        local_db_import = local_db_user = local_db_pass = None

    local_target_path = None
    while True:
        local_target_path = input("🔹 Yerel sunucuda dosyaların açılacağı dizin: ").strip()
        if local_target_path != "":
            break
        print("Bu alan boş bırakılamaz, lütfen bir değer girin.")

    if not os.path.exists(local_target_path):
        if ask(f"⚠️ {local_target_path} dizini yok, oluşturulsun mu?", "E"):
            try:
                os.makedirs(local_target_path)
                printc(f"[+] {local_target_path} oluşturuldu.", Colors.OKGREEN)
            except Exception as e:
                printc(f"[!] Dizin oluşturulamadı: {e}", Colors.FAIL)
                sys.exit(1)
        else:
            printc("[!] Dizin oluşturulmadı, işlem iptal ediliyor.", Colors.FAIL)
            sys.exit(1)

    zip_filename = "erencp_backup.zip"
    db_filename = "erencp_db.sql"

    ssh_prefix = ""
    scp_prefix = ""
    if use_sshpass and remote_pass:
        ssh_prefix = f"sshpass -p '{remote_pass}' ssh {remote_user}@{remote_ip}"
        scp_prefix = f"sshpass -p '{remote_pass}' scp"
    else:
        ssh_prefix = f"ssh {remote_user}@{remote_ip}"
        scp_prefix = "scp"

    def run_cmd(cmd, error_msg):
        printc(f"🖥️  {cmd}", Colors.OKBLUE)
        if os.system(cmd) != 0:
            printc(error_msg, Colors.FAIL)
            sys.exit(1)

    printc("\n📁 Uzak sunucuda dosyalar zipleniyor...", Colors.HEADER)
    zip_cmd = f"{ssh_prefix} 'cd {remote_path} && zip -r /tmp/{zip_filename} .'"
    run_cmd(zip_cmd, "Zipleme işlemi başarısız oldu!")

    printc("📥 Dosyalar yerel sunucuya indiriliyor...", Colors.HEADER)
    scp_zip_cmd = f"{scp_prefix} {remote_user}@{remote_ip}:/tmp/{zip_filename} {local_target_path}/"
    run_cmd(scp_zip_cmd, "Zip dosyası indirilemedi!")

    printc(f"📂 {local_target_path} dizinine zip açılıyor...", Colors.HEADER)
    unzip_cmd = f"unzip -o {local_target_path}/{zip_filename} -d {local_target_path}/"
    run_cmd(unzip_cmd, "Zip açma işlemi başarısız oldu!")

    if db_transfer:
        printc("🗄️  Uzak sunucuda veritabanı dump alınıyor...", Colors.HEADER)
        dump_cmd = f"{ssh_prefix} 'mysqldump -u{remote_db_user} -p\"{remote_db_pass}\" {remote_db_name} > /tmp/{db_filename}'"
        run_cmd(dump_cmd, "Veritabanı dump işlemi başarısız oldu!")

        printc("📥 Veritabanı dump dosyası indiriliyor...", Colors.HEADER)
        scp_db_cmd = f"{scp_prefix} {remote_user}@{remote_ip}:/tmp/{db_filename} {local_target_path}/"
        run_cmd(scp_db_cmd, "DB dump dosyası indirilemedi!")

        printc(f"🛠️  Yerel veritabanı {local_db_import} kontrol ediliyor...", Colors.HEADER)
        check_db_cmd = f"mysql -u{local_db_user} -p{local_db_pass} -e 'USE {local_db_import};'"
        create_db_cmd = f"mysql -u{local_db_user} -p{local_db_pass} -e 'CREATE DATABASE {local_db_import} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'"

        if os.system(check_db_cmd) != 0:
            printc(f"[!] {local_db_import} veritabanı yok, oluşturuluyor...", Colors.WARNING)
            if os.system(create_db_cmd) != 0:
                printc("[!] Veritabanı oluşturulamadı, çıkılıyor.", Colors.FAIL)
                sys.exit(1)
            else:
                printc(f"[+] {local_db_import} veritabanı oluşturuldu.", Colors.OKGREEN)
        else:
            printc(f"[+] {local_db_import} veritabanı zaten mevcut.", Colors.OKGREEN)

        printc(f"🛠️  Veritabanı {local_db_import} içerik aktarılıyor...", Colors.HEADER)
        import_db_cmd = f"mysql -u{local_db_user} -p{local_db_pass} {local_db_import} < {local_target_path}/{db_filename}"
        run_cmd(import_db_cmd, "Veritabanı içe aktarma başarısız oldu!")

    printc("\n✅ İşlem başarıyla tamamlandı!", Colors.OKGREEN)

if __name__ == "__main__":
    main()
