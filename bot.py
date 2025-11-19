import asyncio, logging, os, json, aiohttp, random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from middleware.rate_limit import RateLimitMiddleware
from downloader import fetch_and_parse, choose_media_type
from media_fetcher import download_to_file, remove_file
from reactions import REACTIONS
from config import TOKEN, IMAGE_API, PHONE_OSINT_API, DOWNLOADER_API, INSTA_API, OPENROUTER_KEY, OWNER_MENTION, BOT_MENTION, MAX_DOWNLOAD_BYTES, ADMIN_ID
# pyrogram client import (optional usage)
try:
    from pyrogram_client import user_client
except Exception:
    user_client = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.message.middleware(RateLimitMiddleware(delay=1.0))

COMMANDS = [
    ('.download <url>', 'Video va audio yuklab beradi'),
    ('.image <prompt>', 'Rasm yaratadi (IMAGE_API)'),
    ('.phone <number>', "Telefon bo'yicha OSINT"),
    ('.insta <username>', 'Instagram info (uzbekcha format)'),
    ('.chat <text>', 'AI Chat (OpenRouter)'),
    ('.quiz', 'Oyin: savol-javob'),
    ('.roll', 'Oyin: tasodifiy 1-6'),
    ('.react <name>', 'Reaksiya effekti yuboradi (misol: clap, wow, laugh)'),
    ('.yordam', "Yordam oynasi (dot-format)"),
]

HELP_TEXT = '\n'.join([f"{c} — {d}" for c,d in COMMANDS])

@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    await message.answer('Salom! .yordam buyrug\'i orqali barcha buyruqlarni ko\'ring.')

@dp.message(Command('yordam'))
async def help_cmd(message: types.Message):
    await message.answer(HELP_TEXT)

@dp.message()
async def fallback(message: types.Message):
    text = (message.text or '').strip()
    if not text:
        return
    low = text.lower()
    if low.startswith(('/download', '.download', 'download')):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            return await message.answer('Iltimos URL yuboring: .download <url>')
        return await handle_download(message, parts[1].strip())
    if low.startswith(('/image', '.image', 'image')):
        prompt = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1))>1 else ''
        return await handle_image(message, prompt)
    if low.startswith(('/phone', '.phone', 'phone')):
        num = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1))>1 else ''
        return await handle_phone(message, num)
    if low.startswith(('/insta', '.insta', 'insta')):
        uname = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1))>1 else ''
        return await handle_insta(message, uname)
    if low.startswith(('/chat', '.chat', 'chat')):
        txt = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1))>1 else ''
        return await handle_chat(message, txt)
    if low.startswith(('/quiz', '.quiz', 'quiz')):
        return await handle_quiz(message)
    if low.startswith(('/roll', '.roll', 'roll')):
        return await handle_roll(message)
    if low.startswith(('/react', '.react', 'react')):
        name = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1))>1 else ''
        return await handle_react(message, name)
    if low.startswith(('/admin', '.admin', 'admin')):
        if message.from_user.id != ADMIN_ID:
            return await message.answer('Siz admin emassiz.')
        return await message.answer('Admin panelga kirish uchun admin_panel.py ni ishga tushiring yoki admin.py dan foydalaning.')
    await message.answer('Noaniq buyruq. .yordam yordam beradi.')

async def handle_download(message: types.Message, url: str):
    info = await message.answer('⏳ Yuklanmoqda...')
    try:
        medias = await asyncio.to_thread(fetch_and_parse, DOWNLOADER_API, url)
    except Exception as e:
        return await info.edit_text(f'API xatosi: {e}')
    if not medias:
        return await info.edit_text('❌ Hech qanday media topilmadi.')
    videos=[]; audios=[]
    for m in medias:
        u=m.get('url'); t=m.get('type') or ''
        chosen=choose_media_type(u,t)
        if chosen=='video' or 'video' in str(t).lower():
            videos.append((u,m))
        elif chosen=='audio' or 'audio' in str(t).lower():
            audios.append((u,m))
    await info.edit_text(f'✅ Topildi: {len(videos)} video, {len(audios)} audio.')
    for idx,(u,meta) in enumerate(videos, start=1):
        caption = f"ega: {OWNER_MENTION}\nvido: {BOT_MENTION} tomonidan yuklandi\n{meta.get('title','')}"
        path=None
        try:
            path = await asyncio.to_thread(download_to_file, u, MAX_DOWNLOAD_BYTES)
            if not path or not os.path.exists(path): raise Exception('Yuklab olinmadi')
            f=FSInputFile(path)
            await message.answer_video(f, caption=caption)
        except Exception as e:
            logger.exception('Video send failed')
            await message.reply(f'Video yuborilmadi: {e}\nURL: {u}')
        finally:
            if path: remove_file(path)
        await asyncio.sleep(0.7)
    for idx,(u,meta) in enumerate(audios, start=1):
        caption = f"audio: {BOT_MENTION} tomonidan yuklandi\nega: {OWNER_MENTION}\n{meta.get('title','')}"
        path=None
        try:
            path = await asyncio.to_thread(download_to_file, u, MAX_DOWNLOAD_BYTES)
            if not path or not os.path.exists(path): raise Exception('Yuklab olinmadi')
            f=FSInputFile(path)
            await message.answer_audio(f, caption=caption)
        except Exception as e:
            logger.exception('Audio send failed')
            await message.reply(f'Audio yuborilmadi: {e}\nURL: {u}')
        finally:
            if path: remove_file(path)
        await asyncio.sleep(0.7)
    await message.answer('🎉 Barchasi yuborildi!')

async def handle_image(message: types.Message, prompt: str):
    if not prompt: return await message.answer('Iltimos prompt yozing: .image <prompt>')
    info = await message.answer('🖼️ Rasm yaratilmoqda...')
    url = IMAGE_API + aiohttp.helpers.quote(prompt)
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=120) as resp:
                if resp.status != 200: return await info.edit_text(f'Rasm API xatosi: {resp.status}')
                data = await resp.read()
        import tempfile
        fd,path = tempfile.mkstemp(suffix='.jpg'); os.close(fd)
        with open(path,'wb') as f: f.write(data)
        await message.answer_photo(FSInputFile(path), caption=f'Rasm: {prompt}\n{BOT_MENTION}')
        os.remove(path); await info.delete()
    except Exception as e:
        logger.exception('Image gen failed'); await info.edit_text(f'Rasm yaratilmayapti: {e}')

async def handle_phone(message: types.Message, number: str):
    if not number: return await message.answer('Telefon raqam yuboring: .phone <number>')
    info = await message.answer('🔎 Telefon tekshirilmoqda...')
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(PHONE_OSINT_API + aiohttp.helpers.quote(number), timeout=30) as resp:
                if resp.status != 200: return await info.edit_text(f'API xatosi: {resp.status}')
                js = await resp.json()
        data = js.get('data') or js
        mapping = {'telefon_raqami':'Telefon','raqam_turi':'Turi','operator':'Operator','mamlakat':'Mamlakat','shahar':'Shahar','kontinent':'Kontinent','vaqt_zonasi':'Vaqt zonasi','valyuta':'Valyuta','tili':'Tili','geolokatsiya':'Geolokatsiya'}
        lines = [f"{mapping.get(k,k)}: {v}" for k,v in data.items()]
        await message.answer('\n'.join(lines)); await info.delete()
    except Exception as e:
        logger.exception('Phone OSINT failed'); await info.edit_text(f'Xato: {e}')

async def handle_insta(message: types.Message, username: str):
    if not username: return await message.answer('Iltimos username yuboring: .insta <username>')
    info = await message.answer('⏳ Instagram ma\'lumot olinmoqda...')
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(INSTA_API + aiohttp.helpers.quote(username) + '&get=info', timeout=30) as resp:
                if resp.status != 200: return await info.edit_text(f'API xatosi: {resp.status}')
                js = await resp.json()
        # Format in Uzbek short style as requested
        d = js
        success = d.get('success') or d.get('status') in (True,'ok')
        if not success:
            return await info.edit_text('Insta API: ma\'lumot topilmadi.')
        username = d.get('username') or d.get('data',{}).get('username') or ''
        full_name = d.get('full_name') or d.get('data',{}).get('full_name') or ''
        bio = d.get('bio') or d.get('data',{}).get('bio') or ''
        followers = d.get('followers') or d.get('data',{}).get('followers') or 0
        following = d.get('following') or d.get('data',{}).get('following') or 0
        posts = d.get('posts') or d.get('data',{}).get('posts') or 0
        profile_pic = d.get('profile_pic') or d.get('data',{}).get('profile_pic') or ''
        text = f"📸 Instagram Profil Ma'lumoti\n\n@{username}\n\n👤 Ism: {full_name}\n📝 Bio: {bio}\n👥 Obunachilar: {followers}\n➡️ Obuna bo'lganlar: {following}\n📦 Postlar soni: {posts}\n\n🖼 Profil rasmi:\n{profile_pic}"
        await message.answer(text); await info.delete()
    except Exception as e:
        logger.exception('Insta API failed'); await info.edit_text(f'Xato: {e}')

async def handle_chat(message: types.Message, text: str):
    if not text: return await message.answer('Suhbat matnini yuboring: .chat <savol>')
    info = await message.answer('🤖 AI javob yozilmoqda...')
    try:
        headers = {'Authorization': f'Bearer {OPENROUTER_KEY}','Content-Type':'application/json'}
        payload = {'model':'qwen/qwen3-coder:free','messages':[{'role':'user','content': text}]}
        async with aiohttp.ClientSession() as s:
            async with s.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=payload, timeout=60) as resp:
                if resp.status != 200:
                    txt = await resp.text(); return await info.edit_text(f'AI API xatosi: {resp.status}\n{txt}')
                js = await resp.json()
        ans = js.get('choices',[{}])[0].get('message',{}).get('content') or js.get('choices',[{}])[0].get('delta') or str(js)
        await message.answer(str(ans)); await info.delete()
    except Exception as e:
        logger.exception('AI chat failed'); await info.edit_text(f'Xato: {e}')

async def handle_quiz(message: types.Message):
    qlist = [("O'zbekiston poytaxti qaysi?", "Toshkent"),("Python dasturlash tili kim tomonidan yaratilgan?", "Guido van Rossum"),("2+2 nechchi?", "4")]
    q,a = random.choice(qlist)
    bot._last_quiz_answer = a
    await message.answer(f"Quiz: {q}\nJavobni yozing (1 ta so'z).\n(q ni to'g'ri javobini yozsangiz, men e'lon qilaman)")

async def handle_roll(message: types.Message):
    r = random.randint(1,6)
    await message.answer(f"🎲 Sizning zar: {r}")

async def handle_react(message: types.Message, name: str):
    # send reaction animation/gif from available REACTIONS mapping
    if not name: return await message.answer('Iltimos reaksiya nomini yozing: .react clap')
    key = name.lower()
    url = REACTIONS.get(key)
    if not url:
        return await message.answer('Bunday reaksiya topilmadi. Mavjudlar: ' + ', '.join(REACTIONS.keys()))
    info = await message.answer('React yuborilmoqda...')
    try:
        path = await asyncio.to_thread(download_to_file, url, MAX_DOWNLOAD_BYTES)
        await message.answer_animation(FSInputFile(path), caption=f'Reaction: {name}')
    except Exception as e:
        logger.exception('React failed')
        await message.reply(f'Reaction yuborilmadi: {e}')
    finally:
        try: remove_file(path)
        except: pass
        await info.delete()

# simple quiz answer catcher
@dp.message()
async def catch_answers(message: types.Message):
    if hasattr(bot, '_last_quiz_answer') and message.text:
        if message.text.strip().lower() == bot._last_quiz_answer.strip().lower():
            await message.reply('Tabriklaymiz! Javob to\'g\'ri.')
            delattr(bot, '_last_quiz_answer')
            return
    # fall back handled earlier
    return

async def main():
    logger.info('Bot ishga tushdi...')
    # optionally start pyrogram user client in background
    if user_client:
        try:
            user_client.start()
        except Exception:
            pass
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot to\'xtadi')
