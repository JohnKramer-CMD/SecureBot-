# Токен бота
TOKEN = "ТОКЕН_ИЗ_BOTFATHER"

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для проверки SSL-сертификата
def check_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expire_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y GMT")
                days_left = (expire_date - datetime.utcnow()).days
                return f"🔒 SSL сертификат сайта {domain} истекает через {days_left} дней."
    except Exception as e:
        return f"❌ Ошибка проверки SSL: {e}"

# Функция для сканирования портов
def scan_ports(domain):
    nm = nmap.PortScanner()
    try:
        nm.scan(domain, '1-1024')  # Сканируем порты с 1 по 1024
        scan_info = nm.all_tcp()   # Получаем информацию по всем найденным TCP портам
        result = f"📡 Результаты сканирования портов для {domain}:\n"
        for port in scan_info:
            result += f"Порт {port}: {'Открыт' if nm[domain].has_tcp(port) else 'Закрыт'}\n"
        return result
    except Exception as e:
        return f"❌ Ошибка сканирования: {e}"

# Обработчик команды /start с inline-кнопками
@dp.message(Command("start"))
async def start_command(message: types.Message):
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    button_ssl = InlineKeyboardButton("Проверка SSL", callback_data="ssl_help")
    button_scan = InlineKeyboardButton("Сканирование портов", callback_data="scan_help")
    button_help = InlineKeyboardButton("Помощь", callback_data="help")
    inline_keyboard.add(button_ssl, button_scan, button_help)

    await message.answer(
        "🔐 Привет! Я SecureBot.\n"
        "Я помогу тебе проверить безопасность сайтов и серверов.\n"
        "Выбери одну из опций ниже или напиши команду вручную.",
        reply_markup=inline_keyboard
    )

# Обработчик callback_data для кнопок
@dp.callback_query_handler(lambda c: c.data == "ssl_help")
async def ssl_help(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Команда /ssl <url> проверяет SSL-сертификат для сайта. Пример: /ssl google.com"
    )

@dp.callback_query_handler(lambda c: c.data == "scan_help")
async def scan_help(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "Команда /scan <url> сканирует порты сайта. Пример: /scan google.com"
    )

@dp.callback_query_handler(lambda c: c.data == "help")
async def help_command(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "💡 Вот список всех команд и их назначений:\n\n"
        "/start - Приветственное сообщение и информация о боте\n"
        "/ssl <url> - Проверка SSL-сертификата сайта. Пример: /ssl google.com\n"
        "/scan <url> - Сканирование портов сайта. Пример: /scan google.com"
    )

# Обработчик команды /ssl
@dp.message(Command("ssl"))
async def ssl_command(message: types.Message):
    url = message.text.split(" ")
    if len(url) < 2:
        await message.answer("⚠️ Введи команду в формате:\n<code>/ssl site.com</code>")
        return

    domain = url[1].replace("https://", "").replace("http://", "").strip("/")
    result = check_ssl(domain)
    await message.answer(result)

# Обработчик команды /scan
@dp.message(Command("scan"))
async def scan_command(message: types.Message):
    url = message.text.split(" ")
    if len(url) < 2:
        await message.answer("⚠️ Введи команду в формате:\n<code>/scan site.com</code>")
        return

    domain = url[1].replace("https://", "").replace("http://", "").strip("/")
    result = scan_ports(domain)
    await message.answer(result)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
