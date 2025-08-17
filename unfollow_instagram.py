from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Konfigurasi
UNFOLLOW_LIMIT = 368
BATCH_DELAY = 20
SLEEP_BETWEEN = 3
SLEEP_AFTER_BATCH = 60

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Buka Instagram
driver.get('https://www.instagram.com/')
time.sleep(5)

# Login manual
input("📌 Login ke Instagram di browser, lalu tekan ENTER di terminal...")

USERNAME_KAMU = 'b4takkkk_'
driver.get(f"https://www.instagram.com/{USERNAME_KAMU}/")
print("🔃 Membuka halaman profil...")
time.sleep(5)

# Klik tombol "following" (angka)
print("🔘 Klik tombol jumlah following...")
following_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))
)
following_button.click()
time.sleep(3)

# Tunggu popup daftar akun muncul
print("🪟 Menunggu daftar akun muncul...")
scroll_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow')]"))
)

# Scroll semua akun
last_height, height = 0, 1
while last_height != height:
    last_height = height
    time.sleep(1)
    height = driver.execute_script("""
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight;
    """, scroll_box)

# Unfollow
unfollowed = 0
clicked_buttons = set()

while unfollowed < UNFOLLOW_LIMIT:
    buttons = scroll_box.find_elements(By.XPATH, ".//button")

    for index, button in enumerate(buttons):
        if unfollowed >= UNFOLLOW_LIMIT:
            break
        if index in clicked_buttons:
            continue

        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button.click()
            clicked_buttons.add(index)

            # Tunggu tombol konfirmasi muncul
            try:
                confirm_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Unfollow') or contains(text(), 'Berhenti')]"))
                )
                confirm_button.click()
            except:
                pass  # Jika tidak muncul, lanjutkan

            unfollowed += 1
            print(f"✅ Unfollowed: {unfollowed}/{UNFOLLOW_LIMIT}")
            time.sleep(SLEEP_BETWEEN)

            if unfollowed % BATCH_DELAY == 0:
                print("⏸️ Istirahat sebentar...")
                time.sleep(SLEEP_AFTER_BATCH)

        except Exception as e:
            print(f"⚠️ Error saat unfollow: {e}")
            time.sleep(2)
            continue

print("🎉 Selesai unfollow.")
driver.quit()
