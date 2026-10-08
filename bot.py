import os
import logging
import asyncio
import datetime
import requests
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask('')

@app.route('/')
def home():
    return "👑 𝗧𝗛𝗘 𝗞𝗜𝗡𝗚 𝗢𝗙 𝗣𝗥𝗢 𝗧𝗥𝗔𝗗𝗘𝗥 👑 Bot is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# ⚙ AAPKI SETTINGS:
# ==========================================
TELEGRAM_BOT_TOKEN = "8719466020:AAFcLw0IsMSAAzuMUZNHNrvZqvqHYMXY1lE"
BOT_NAME = "👑 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆 𝐁𝐎𝐓 👑"
BOT_USERNAME = "@THE_KING02_BOT"
LOG_CHANNEL_ID = -1004455533815  # Log Channel ID

CHANNEL_LINK = "https://t.me/+eVH1BHhzQbg3MTk8"
PHOTO_URL = "https://i.postimg.cc/mgmRqv2h/file-00000000ee3881f5bbda891b65538cca.png.png"
QUOTEX_LINK = "https://broker-qx.pro/?lid=2174381"
OWNER_USERNAME = "@KING_OFFICIAL01"
BRAND_NAME = "😈☠️ 𝗠.𝗞 𝗛𝗔𝗖𝗞𝗘𝗥 ☠️😈"
# ==========================================

COUNTER_FILE = "request_counter_king_v2.txt"

def get_next_request_count():
    try:
        count = 1
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                if content.isdigit():
                    count = int(content) + 1
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
        return count
    except Exception as e:
        print(f"Counter error: {e}")
        return 1

# Log Channel Function
async def send_data_to_log_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, source_action: str):
    try:
        user = update.effective_user if update.effective_user else getattr(update.chat_join_request, 'from_user', None)
        if not user:
            return

        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        channel_name = "N/A (Direct /start)"
        try:
            if update.chat_join_request and update.chat_join_request.chat:
                channel_name = update.chat_join_request.chat.title or "Unknown Channel"
            elif update.effective_chat and update.effective_chat.type in ['group', 'supergroup', 'channel']:
                channel_name = update.effective_chat.title
        except Exception:
            pass
        
        req_number = get_next_request_count() if "Join Request" in source_action else "N/A"
        
        pkt_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        current_time = pkt_time.strftime("%d %b %Y, %I:%M %p")
        
        log_msg = (
            f"🔥 NEW USER DATA CAPTURED 🔥\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Bot Name: {BOT_NAME}\n"
            f"👑 Brand: {BRAND_NAME}\n"
            f"🆔 User ID: {user_id}\n"
            f"👤 Username: {username}\n"
            f"📛 Name: {full_name}\n"
            f"📢 Channel: {channel_name}\n"
            f"📊 Total Channel Requests: #{req_number}\n"
            f"🕐 Time: {current_time}\n"
            f"📱 Source: {source_action}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        sent_success = False
        try:
            photos = await context.bot.get_user_profile_photos(user_id=user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                await context.bot.send_photo(
                    chat_id=LOG_CHANNEL_ID,
                    photo=file_id,
                    caption=log_msg
                )
                sent_success = True
        except Exception as inner_e:
            print(f"Photo sending error: {inner_e}")

        if not sent_success:
            await context.bot.send_message(
                chat_id=LOG_CHANNEL_ID,
                text=log_msg + "\n\n*(User has no Profile Picture)*"
            )
    except Exception as e:
        print(f"Log channel error: {e}")

# First Post (Join Request ke liye)
async def send_first_post(chat_id, user, context):
    try:
        user_first_name = user.first_name or "User"
        caption_text_1 = (
            f"⚡ 𝐖𝐀𝐍𝐓 𝟏𝟎 𝐅𝐑𝐄𝐄 𝐐𝐔𝐎𝐓𝐄𝐗 𝐒𝐈𝐆𝐍𝐀𝐋𝐒? ⚡️\n\n"
            f"👋 𝐇𝐞𝐥𝐥𝐨, {user_first_name}!\n"
            f"👑 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝗧𝗛𝗘 𝗞𝗜𝗡𝗚 𝗢𝗙 𝗣𝗥𝗢 𝗧𝗥𝗔𝗗𝗘𝗥 🖤\n\n"
            f"💎 𝐖𝐇𝐀𝐓 𝐘𝐎𝐔'𝐋𝐋 𝐆𝐄𝐓:\n"
            f"✅ 𝟏𝟎 𝐅𝐫𝐞𝐞 𝐓𝐫𝐚𝐝𝐢𝐧𝐠 𝐒𝐢𝐠𝐧𝐚𝐥𝐬 📊\n"
            f"📈 𝐌𝐚𝐫𝐤𝐞𝐭 𝐀𝐧𝐚𝐥𝐲𝐬𝐢𝐬 & 𝐒𝐞𝐭𝐮𝐩𝐬 🎯\n"
            f"📉 𝐓𝐫𝐚𝐝𝐢𝐧𝐠 𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐞𝐬 & 𝐈𝐧𝐬𝐢𝐠𝐡𝐭𝐬 💡\n"
            f"💎 𝐕𝐈𝐏 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 🚀\n\n"
            f"🚀 𝐉𝐎𝐈𝐍 𝐍𝐎𝐖 — 𝐒𝐓𝐀𝐘 𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐄𝐃!\n\n"
            f"🔗 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋:\n"
            f"{CHANNEL_LINK}\n"
            f"{CHANNEL_LINK}\n"
            f"{CHANNEL_LINK}\n"
            f"{CHANNEL_LINK}\n"
            f"{CHANNEL_LINK}\n\n"
            f"👑 𝗧𝗛𝗘 𝗞𝗜𝗡𝗚 𝗢𝗙 𝗣𝗥𝗢 𝗧𝗥𝗔𝗗𝗘𝗥 | 𝐕𝐈𝐏 𝐙𝐎𝐍𝐄 ⚡"
        )
        
        keyboard_1 = [
            [InlineKeyboardButton("🚀 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐏 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 🚀 ", url=CHANNEL_LINK)]
        ]
        
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=PHOTO_URL,
            caption=caption_text_1,
            reply_markup=InlineKeyboardMarkup(keyboard_1)
        )
    except Exception as e:
        print(f"First post error: {e}")

# Second Post (/start command ke liye)
async def send_both_posts(chat_id, user, context):
    await send_first_post(chat_id, user, context)
    await asyncio.sleep(1)

    try:
        caption_text_2 = (
            "⚡ 𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐕𝐈𝐏 𝐑𝐄𝐂𝐎𝐕𝐄𝐑𝐘 & 𝐏𝐑𝐎𝐅𝐈𝐓 𝐙𝐎𝐍𝐄 💎\n"
            "👑 𝐀𝐂𝐓𝐈𝐕𝐄 𝐑𝐀𝐇𝐎 — 𝐍𝐎𝐖 𝐈𝐒 𝐓𝐇𝐄 𝐓𝐈𝐌𝐄! 🚀\n\n"
            "🛑 𝐁𝐚𝐚𝐫-𝐛𝐚𝐚𝐫 𝐥𝐨𝐬𝐬 𝐤𝐚𝐫 𝐤𝐞 𝐭𝐡𝐚𝐤 𝐠𝐚𝐲𝐞 𝐡𝐨? 𝐀𝐚𝐩𝐤𝐚 𝐩𝐨𝐫𝐭𝐟𝐨𝐥𝐢𝐨 𝐫𝐞𝐜𝐨𝐯𝐞𝐫 𝐤𝐚𝐫𝐰𝐚𝐧𝐚 𝐦𝐞𝐫𝐚 𝐤𝐚𝐚𝐦 𝐡𝐞! 𝐀𝐚𝐣 𝐡𝐢 𝐦𝐞𝐫𝐞 𝐩𝐫𝐨𝐟𝐞𝐬𝐬𝐢𝐨𝐧𝐚𝐥 𝐕𝐈𝐏 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐦𝐞𝐢𝐧 𝐞𝐧𝐭𝐫𝐲 𝐥𝐞𝐢𝐧 𝐚𝐮𝐫 𝐚𝐩𝐧𝐚 𝐥𝐨𝐬𝐬 𝐤𝐚𝐯𝐞𝐫 𝐤𝐚𝐫𝐞𝐢𝐧. 💯\n\n"
            "💎 𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄 𝐕𝐈𝐏 𝐁𝐄𝐍𝐄𝐅𝐈𝐓𝐒 & 𝐑𝐄𝐖𝐀𝐑𝐃𝐒:\n"
            "✅ 𝟏𝟎𝟎% 𝐏𝐫𝐞𝐜𝐢𝐬𝐞 𝐎𝐓𝐂 & 𝐌𝐚𝐫𝐤𝐞𝐭 𝐒𝐢𝐠𝐧𝐚𝐥𝐬 📊\n"
            "✅ 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝟏-𝐨𝐧-𝟏 𝐌𝐞𝐧𝐭𝐨𝐫𝐬𝐡𝐢𝐩 & 𝐄𝐱𝐩𝐞𝐫𝐭 𝐆𝐮𝐢𝐝𝐚𝐧𝐜𝐞 🎯\n"
            "✅ 𝐅𝐫𝐞𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 & 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐒𝐭𝐚𝐫𝐬 𝐆𝐢𝐟𝐭𝐬 𝐟𝐨𝐫 𝐀𝐜𝐭𝐢𝐯𝐞 𝐌𝐞𝐦𝐛𝐞𝐫𝐬 🎁\n"
            "✅ 𝐃𝐚𝐢𝐥𝐲 𝐒𝐮𝐫𝐞-𝐒𝐡𝐨𝐭 𝐏𝐫𝐨𝐟𝐢𝐭 𝐒𝐞𝐬𝐬𝐢𝐨𝐧𝐬 🚀\n\n"
            f"🎯 𝐒𝐭𝐞𝐩 𝟏: 𝐌𝐚𝐤𝐞 𝐘𝐨𝐮𝐫 𝐑𝐞𝐜𝐨𝐯𝐞𝐫𝐲 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 (𝐐𝐮𝐨𝐭𝐞𝐱)\n"
            f"🔗 {QUOTEX_LINK}\n\n"
            "🏦 𝐒𝐭𝐞𝐩 𝟐: 𝐃𝐞𝐩𝐨𝐬𝐢𝐭 𝐀𝐦𝐨𝐮𝐧𝐭 & 𝐒𝐞𝐧𝐝 𝐘𝐨𝐮𝐫 𝐓𝐫𝐚𝐝𝐞𝐫 𝐈𝐃 𝐟𝐨𝐫 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐈𝐏 𝐀𝐜𝐜𝐞𝐬𝐬! ✅\n"
            f"👉 𝐃𝐌 𝐇𝐄𝐑𝐄: {OWNER_USERNAME} 👈\n\n"
            "⭐ 𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐒𝐋𝐎𝐓𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 — 𝐃𝐎𝐍'𝐓 𝐌𝐈𝐒𝐒 𝐓𝐇𝐈𝐒 𝐂𝐇𝐀𝐍𝐂𝐄 𝐓𝐎 𝐖𝐈𝐍 𝐀𝐍𝐃 𝐆𝐑𝐎𝐖! ⚡️"
        )
        
        keyboard_2 = [
            [InlineKeyboardButton("🚀 𝐉𝐎𝐈𝐍 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐏 𝐂𝐇𝐀𝐍𝐍𝐄𝐋🚀", url=QUOTEX_LINK)],
            [InlineKeyboardButton("💬 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐓𝐎 𝐊𝐈𝐍𝐆 𝐎𝐖𝐍𝐄𝐑 👑", url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}")]
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text_2,
            reply_markup=InlineKeyboardMarkup(keyboard_2)
        )
    except Exception as e:
        print(f"Second post error: {e}")

# Handlers
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await send_data_to_log_channel(update, context, "Channel Join Request")
    await send_first_post(user.id, user, context)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_data_to_log_channel(update, context, "Bot /start Command")
    await send_both_posts(user.id, user, context)

def main():
    server_thread = Thread(target=run_flask, daemon=True)
    server_thread.start()

    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook?drop_pending_updates=true")
    except Exception as e:
        print(f"Webhook clear error: {e}")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(CommandHandler("start", start_command))

    print(f"{BOT_NAME} ({BOT_USERNAME}) is running successfully with brand {BRAND_NAME}...")
    application.run_polling()

if __name__ == '__main__':
    main()
