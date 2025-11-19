# Yukla Bot v5 — Full package (aiogram 3.22.0 + Pyrogram)

Ushbu paket quyidagilarni o'z ichiga oladi:
- aiogram v3.22 bot: downloader, image-gen, phone-osint, insta-info, AI chat.
- Pyrogram client (API_ID/API_HASH) integratsiyasi — qo'shimcha imkoniyatlar va reaktsiya effekti uchun ishlatiladi.
- Reaction effects: `.react <name>` yuborilganda bot animation/gif yuboradi.
- Python Flask Admin panel (`admin_panel.py`) va `adminpnel.php` (original PHP fayl) loyihaga qo'shildi.
- O'yinlar: .quiz, .roll
- `/yordam` ko'rsatadi barcha buyruqlar nuqtali formatda.

**Ishga tushirish**
1. Unzip va loyha papkasiga o'ting.
2. `config.py` ichidagi `TOKEN`, `OPENROUTER_KEY`, `API_ID`, `API_HASH`, `ADMIN_SECRET` ni to'ldiring.
3. Virtualenv yaratib aktivlang va paketlarni o'rnating:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Botni ishga tushiring: `./run.sh`
5. Admin panelni ishga tushiring: `python admin_panel.py` (localhost:5000)
