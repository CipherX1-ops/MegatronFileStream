from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant

from Megatron.bot import StreamBot
from Megatron.vars import Var
from Megatron.utils.human_readable import humanbytes
from Megatron.utils.database import Database
from Megatron.handlers.fsub import force_subscribe
 
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m : Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started the bot."
        )
    firstname = m.from_user.first_name
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL:
            fsub = await force_subscribe(b, m)
            if fsub == 400:
                return
        await m.reply(
            text=f"""Hey Dear {m.from_user.mention(style="md")} 🙋🏻‍♂️\nI'm Telegram File to Link Generator Bot.\n\nSend me any file & get the fast direct download link!\n\n⚠ **Don't forget to read the [rules](https://t.me/FutureTechnologyOfficial/1257) first!**\n\nسلام {m.from_user.mention(style="md")} عزیز 🙋🏻‍♂️\nمن بات تبدیل فایل به لینک هستم\nفایل تلگرامی خود را ارسال کنید تا لینک دانلود پر سرعت آن را دریافت نمایید\n\n**⚠ لطفا قبل از استفاده از بات [قوانین](https://t.me/FutureTechnologyOfficial/1257) را مطالعه نمایید!**\n\nهمچنین با زدن دستور /nim می‌توانید لینک های دریافتی خود را نیم بها نمایید.""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('✵ Updates Channel ✵', url='https://t.me/FutureTechnologyOfficial'), InlineKeyboardButton('✵ Support Group ✵', url='https://t.me/joinchat/riq-psSksFtiMDU8')],
                    [InlineKeyboardButton('✵ Developer ✵', url='https://t.me/CipherXBot')]
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL:
            fsub = await force_subscribe(b, m)
            if fsub == 400:
                return
        u = await b.get_chat_member(int(Var.UPDATES_CHANNEL), m.from_user.id)
        if u.status == "kicked" or u.status == "banned":
            await b.send_message(
                chat_id=m.from_user.id,
                text="✨ You're Banned due not to pay attention to the [rules](https://t.me/FutureTechnologyOfficial/1257). Contact [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8) if you think you've banned wrongly.\n\n✨ شما به علت عدم رعایت [قوانین](https://t.me/FutureTechnologyOfficial/1257) بن شده اید. اگر فکر میکنید بن شدن شما اشتباه بوده و قوانین را رعایت کرده اید می توانید با [گروه پشتیبانی](https://t.me/joinchat/riq-psSksFtiMDU8) در ارتباط باشید.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )

@StreamBot.on_message(filters.command('upgrade') & filters.private & ~filters.edited)
async def upgrade(b, m : Message):
    await m.reply(
        text=f"""─────────────\n➰ **Daily Plan :**\n✗ 5 days - 5 dollar\n✗ 10 days - 10 dollar\n✗ 20 days - 20 dollar\n••••••••••••••••\n➰ **Monthly Plan :**\n✗ 1 month - 30 dollar\n✗ 3 months - 80 dollar\n✗ 6 months - 150 dollar\n••••••••••••••••\n➰ **Annual Plan :**\n✗ 1 year - 290 dollar\n─────────────\n─────────────\n➰ **پلن روزانه :**\n✗ 5 روزه - 5000 تومان \n✗ 10 روزه - 10000 تومان\n✗ 20 روزه - 20000 تومان\n••••••••••••••••\n➰ **پلن ماهانه :**\n✗ 1 ماهه - 30000 تومان\n✗ 3 ماهه - 80000 تومان\n✗ 6 ماهه - 150000 تومان\n••••••••••••••••\n➰ **پلن سالانه :**\n✗ 1 ساله - 290000 تومان\n─────────────\n✨ برای خرید روی دکمه زیر کلیک کنید""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('✨ Buy & Contact ✨', url='https://t.me/CipherXBot')]
            ]
        ),
        disable_web_page_preview=True
    )

@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(b, m : Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL:
        fsub = await force_subscribe(b, m)
        if fsub == 400:
            return
    u = await b.get_chat_member(int(Var.UPDATES_CHANNEL), m.from_user.id)
    if u.status == "kicked" or u.status == "banned":
        await b.send_message(
            chat_id=m.from_user.id,
            text="✨ You're Banned due not to pay attention to the [rules](https://t.me/FutureTechnologyOfficial/1257). Contact [Support Group](https://t.me/joinchat/riq-psSksFtiMDU8) if you think you've banned wrongly.\n\n✨ شما به علت عدم رعایت [قوانین](https://t.me/FutureTechnologyOfficial/1257) بن شده اید. اگر فکر میکنید بن شدن شما اشتباه بوده و قوانین را رعایت کرده اید می توانید با [گروه پشتیبانی](https://t.me/joinchat/riq-psSksFtiMDU8) در ارتباط باشید.",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
    else:
        await m.reply_text(
            text="✨ Send me any file, I'll give you its direct download link\n\nAlso I'm supported in channels. Add me to channel as admin to make me workable\n\n✨ فایل تلگرامی خود را برای من بفرستید تا لینک دانلود مستقیم آن را برای شما بفرستم\n\nهمچنین با ارتقای من به عنوان ادمین در چنل خود می توانید از امکانات من استفاده کنید، بدین صورت که در زمان پست فایل جدید در چنل دکمه شیشه ای دریافت لینک مستقیم فایل پست شده در زیر پست ایجاد می گردد.",
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✵ Support Group ✵", url="https://t.me/joinchat/riq-psSksFtiMDU8"), InlineKeyboardButton("✵ Update Channel ✵", url="https://t.me/FutureTechnologyOfficial")],
                    [InlineKeyboardButton("✵ Developer ✵", url="https://t.me/CipherXBot")]
                ]
            )
        )
