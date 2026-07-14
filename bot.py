import telebot, json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = telebot.TeleBot("8908913545:AAHkcHb_Mb1vHc4S8Rjojs_PuMmKhvJmRVg")

@bot.message_handler(commands=['start'])
def start(m):
    text = (
        "Welcome! You have entered my crypto bot.\n\n"
        "💵 *Price list:*\n"
        "▪️ 20$ - 100$ — contact creator via PM\n"
        "▪️ 15$ — 1250₽ / 650 Stars\n"
        "▪️ 10$ — 790₽ / 450 Stars\n"
        "▪️ 5$ — 249₽ / 150 Stars\n\n"
        "ℹ️ *Информация:*\n"
        "В меню встроен кошелек, легальный P2P Маркет и игровое Мини-Казино!"
    )
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📱 Открыть Экосистему PING", web_app=WebAppInfo("https://surge.sh")))
    bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(content_types=['web_app_data'])
def data(m):
    try:
        res = json.loads(m.web_app_data.data)
        action = res.get("action")
        
        if action == "transfer":
            tx = f"💸 *Перевод отправлен!*\n\n👤 *Кому:* {res['to']}\n💰 *Сумма:* {res['val']} монет\n🔒 Статус: `Успешно (Симуляция)`"
            bot.send_message(m.chat.id, tx, parse_mode="Markdown")
            
        elif action == "p2p_ad":
            tx = f"📊 *P2P-ордер опубликован!*\n\nℹ️ *Тип:* {res['type']}\n💰 *Объем:* {res['amount']} монет\n🏦 *Оплата:* {res['bank']}"
            bot.send_message(m.chat.id, tx, parse_mode="Markdown")
            
        elif action == "casino_result":
            bet = float(res['bet'])
            status = res['result']
            combo = res['combo']
            
            if status == "jackpot":
                win_amount = bet * 10
                tx = f"🎰 *ДЖЕКПОТ!!!* 🎰\n\n🔥 Комбинация: `[{combo}]` \n💰 Твоя ставка: {bet} монет\n🎉 Выигрыш (x10): *{win_amount} монет!* \n\nБаланс кошелька пополнен."
            elif status == "win":
                win_amount = bet * 2
                tx = f"🎰 *ВЫИГРЫШ!* 🎉\n\n✨ Комбинация: `[{combo}]` \n💰 Твоя ставка: {bet} монет\n📈 Выигрыш (x2): *{win_amount} монет!* \n\nСредства зачислены."
            else:
                tx = f"🎰 *Увы, проигрыш* 💔\n\n📉 Комбаризация: `[{combo}]` \n💰 Ставка: {bet} монет ушли в банк казино. \n\nПопробуй еще раз, удача рядом!"
                
            bot.send_message(m.chat.id, tx, parse_mode="Markdown")
            
    except Exception as e: print(e)

if __name__ == "__main__":
    bot.infinity_polling()
