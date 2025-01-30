import snap7
import time
import requests
# Настройки PLC
plc_ip = "192.168.0.100"
rack = 0
slot = 1
db_number = 84  # Номер Data Block
start_offset = 0  # Смещение от начала блока
bit_position = 4  # Позиция бита в данных (например, 0-й бит)
# Настройки Telegram
telegram_token = "7690392481:AAG0d13SAIWLqpkBS5wC3jb7uf-Fu27lwZc"
telegram_chat_id = "1555267566"
def read_plc_bit(plc_ip, rack, slot, db_number, start_offset, bit_position):
    client = snap7.client.Client()
    try:
        client.connect(plc_ip, rack, slot)
        if client.get_connected():
            print(f"Подключено к {plc_ip}")
            size = 1  # Читаем 1 байт
            data = client.db_read(db_number, start_offset, size)
            bit_value = (data[0] & (1 << bit_position)) == 0
            return bit_value
        else:
            print("Не удалось подключиться к PLC")
            return False
    except Exception as e:
        print(f"Ошибка при подключении к PLC: {e}")
        return False
    finally:
        client.disconnect()
        print("Соединение закрыто")
async def send_telegram_message(chat_id: str, message: str):
    application = Application.builder().token(telegram_token).build()
    await application.bot.send_message(chat_id=chat_id, text=message)
def main():
    while True:
        bit_value = read_plc_bit(plc_ip, rack, slot, db_number, start_offset, bit_position)
        if not bit_value:
            print("Бит равен 0. Отправка сообщения в Telegram...")
            while True:
                TOKEN = "7690392481:AAG0d13SAIWLqpkBS5wC3jb7uf-Fu27lwZc"
                chat_id = "1555267566"
                message = "Пиздец нащяльнике"
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(
                    url).json())
        else:
            print("Бит установлен в 1. Нет необходимости отправлять сообщение.")

        # Пауза перед следующей проверкой (например, каждые 5 секунд)
        time.sleep(5)
if __name__ == "__main__":
    main()