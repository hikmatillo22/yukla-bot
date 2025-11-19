import os
import re
import json
from typing import List, Dict, Any, Optional, Union
import logging
from pathlib import Path

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AdminPanel:
    def __init__(self, bot, data_dir: str = "data", step_dir: str = "step"):
        self.bot = bot
        self.data_dir = Path(data_dir)
        self.step_dir = Path(step_dir)
        
        # Fayl nomlari
        self.files = {
            'admins': "admins.txt",
            'channels': "channels.txt",
            'blocks': "blocks.txt",
            'stats': "statistics.txt",
            'bot_status': "bot_status.txt"
        }
        
        self.ensure_directories()
        self.setup_keyboards()
        
    def ensure_directories(self):
        """Kerakli papkalarni yaratish"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.step_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Papkalar muvaffaqiyatli yaratildi")
        except Exception as e:
            logger.error(f"Papkalarni yaratishda xato: {e}")
            raise
    
    def setup_keyboards(self):
        """Klaviatura tugmalarini sozlash"""
        try:
            self.main_panel = {
                'inline_keyboard': [
                    [{'text': '📝 Xabar tizimi', 'callback_data': 'mail_system'}],
                    [{'text': '📢 Kanallar boshqaruvi', 'callback_data': 'channel_management'}],
                    [{'text': '🔐 Blok tizimi', 'callback_data': 'block_system'}],
                    [{'text': '⚙️ Bot sozlamalari', 'callback_data': 'bot_settings'}],
                    [{'text': '👥 Adminlar boshqaruvi', 'callback_data': 'admin_management'}],
                    [{'text': '📊 Statistika', 'callback_data': 'statistics'}]
                ]
            }
            
            self.message_manager = {
                'inline_keyboard': [
                    [{'text': '🔄 Forward xabar yuborish', 'callback_data': 'forward_message'}],
                    [{'text': '📨 Oddiy xabar yuborish', 'callback_data': 'simple_message'}],
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.channel_manager = {
                'inline_keyboard': [
                    [{'text': '➕ Kanal qoʻshish', 'callback_data': 'add_channel'}],
                    [{'text': '➖ Kanalni oʻchirish', 'callback_data': 'delete_channel'}],
                    [{'text': '📋 Kanallar roʻyxati', 'callback_data': 'channel_list'}],
                    [{'text': '🗑️ Kanallar roʻyxatini tozalash', 'callback_data': 'clear_channels'}],
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.block_manager = {
                'inline_keyboard': [
                    [{'text': '✅ Blokdan olish', 'callback_data': 'unblock_user'}],
                    [{'text': '❌ Bloklash', 'callback_data': 'block_user'}],
                    [{'text': '📋 Bloklanganlar roʻyxati', 'callback_data': 'blocked_list'}],
                    [{'text': '🗑️ Bloklanganlar roʻyxatini tozalash', 'callback_data': 'clear_blocks'}],
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.bot_manager = {
                'inline_keyboard': [
                    [{'text': '✅ Botni yoqish', 'callback_data': 'enable_bot'}],
                    [{'text': '❌ Botni o\'chirish', 'callback_data': 'disable_bot'}],
                    [{'text': '📊 Statistika', 'callback_data': 'show_statistics'}],
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.admin_manager = {
                'inline_keyboard': [
                    [{'text': '➕ Admin qoʻshish', 'callback_data': 'add_admin'}],
                    [{'text': '➖ Adminlikdan olish', 'callback_data': 'remove_admin'}],
                    [{'text': '📋 Adminlar roʻyxati', 'callback_data': 'admin_list'}],
                    [{'text': '🗑️ Adminlar roʻyxatini tozalash', 'callback_data': 'clear_admins'}],
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.back_button = {
                'inline_keyboard': [
                    [{'text': '◀️ Orqaga', 'callback_data': 'back_to_main'}]
                ]
            }
            
            self.confirm_clear = {
                'inline_keyboard': [
                    [{'text': '✅ Ha', 'callback_data': 'confirm_clear'}],
                    [{'text': '❌ Yo\'q', 'callback_data': 'cancel_clear'}]
                ]
            }
            
        except Exception as e:
            logger.error(f"Klaviaturalarni sozlashda xato: {e}")
            raise
    
    def read_file(self, filename: str, default: str = "") -> str:
        """Fayldan ma'lumot o'qish"""
        try:
            filepath = self.data_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    return content if content else default
            return default
        except Exception as e:
            logger.error(f"Faylni o'qishda xato {filename}: {e}")
            return default
    
    def write_file(self, filename: str, content: str):
        """Faylga ma'lumot yozish"""
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            logger.info(f"Faylga yozildi: {filename}")
        except Exception as e:
            logger.error(f"Faylga yozishda xato {filename}: {e}")
            raise
    
    def append_file(self, filename: str, content: str) -> bool:
        """Faylga ma'lumot qo'shish"""
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content.strip() + '\n')
            logger.info(f"Faylga qo'shildi: {filename}")
            return True
        except Exception as e:
            logger.error(f"Faylga qo'shishda xato {filename}: {e}")
            return False
    
    def read_list_file(self, filename: str) -> List[str]:
        """Fayldan ro'yxat o'qish"""
        content = self.read_file(filename)
        if not content:
            return []
        return [item.strip() for item in content.split('\n') if item.strip()]
    
    def write_list_file(self, filename: str, items: List[str]):
        """Ro'yxatni faylga yozish"""
        content = '\n'.join([item.strip() for item in items if item.strip()])
        self.write_file(filename, content)
    
    def get_user_step(self, user_id: int) -> str:
        """Foydalanuvchi holatini olish"""
        try:
            user_dir = self.step_dir / str(user_id)
            step_file = user_dir / "step.txt"
            
            if step_file.exists():
                with open(step_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            return ""
        except Exception as e:
            logger.error(f"Step faylini o'qishda xato {user_id}: {e}")
            return ""
    
    def set_user_step(self, user_id: int, step: str, data: str = ""):
        """Foydalanuvchi holatini o'rnatish"""
        try:
            user_dir = self.step_dir / str(user_id)
            user_dir.mkdir(parents=True, exist_ok=True)
            
            step_file = user_dir / "step.txt"
            with open(step_file, 'w', encoding='utf-8') as f:
                f.write(step)
            
            if data:
                data_file = user_dir / "data.txt"
                with open(data_file, 'w', encoding='utf-8') as f:
                    f.write(data)
                    
            logger.debug(f"User {user_id} step set to: {step}")
        except Exception as e:
            logger.error(f"Step fayliga yozishda xato {user_id}: {e}")
    
    def get_user_data(self, user_id: int) -> str:
        """Foydalanuvchi ma'lumotlarini olish"""
        try:
            user_dir = self.step_dir / str(user_id)
            data_file = user_dir / "data.txt"
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            return ""
        except Exception as e:
            logger.error(f"Data faylini o'qishda xato {user_id}: {e}")
            return ""
    
    def clear_user_step(self, user_id: int):
        """Foydalanuvchi holatini tozalash"""
        try:
            user_dir = self.step_dir / str(user_id)
            if user_dir.exists():
                for file in user_dir.glob("*"):
                    file.unlink()
                user_dir.rmdir()
            logger.debug(f"User {user_id} step cleared")
        except Exception as e:
            logger.error(f"Step faylini o'chirishda xato {user_id}: {e}")
    
    def is_admin(self, user_id: int) -> bool:
        """Foydalanuvchi admin ekanligini tekshirish"""
        try:
            admins = self.read_list_file(self.files['admins'])
            if not admins:
                # Dastlabki admin
                self.write_list_file(self.files['admins'], [str(user_id)])
                return True
            
            return str(user_id) in admins
        except Exception as e:
            logger.error(f"Admin tekshirishda xato {user_id}: {e}")
            return False
    
    def get_channels(self) -> List[str]:
        """Kanallar ro'yxatini olish"""
        return self.read_list_file(self.files['channels'])
    
    def get_blocked_users(self) -> List[str]:
        """Bloklangan foydalanuvchilar ro'yxati"""
        return self.read_list_file(self.files['blocks'])
    
    def get_admins(self) -> List[str]:
        """Adminlar ro'yxati"""
        return self.read_list_file(self.files['admins'])
    
    def get_statistics(self) -> List[str]:
        """Statistika ma'lumotlari"""
        return self.read_list_file(self.files['stats'])
    
    def is_bot_active(self) -> bool:
        """Bot faol yoki yo'qligini tekshirish"""
        status = self.read_file(self.files['bot_status'])
        return status != "off"
    
    def validate_user_id(self, user_id: str) -> bool:
        """User ID ni tekshirish"""
        return user_id.isdigit() and len(user_id) >= 6
    
    def validate_channel(self, channel: str) -> bool:
        """Kanal havolasini tekshirish"""
        pattern = r'^@[a-zA-Z][a-zA-Z0-9_]{4,}$'
        return bool(re.match(pattern, channel))
    
    def handle_callback_query(self, call):
        """Callback query larni boshqarish"""
        try:
            user_id = call.from_user.id
            data = call.data
            
            if not self.is_admin(user_id):
                self.answer_callback_query(call.id, "❌ Siz admin emassiz!")
                return
            
            if data == 'back_to_main':
                self.clear_user_step(user_id)
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.main_panel
                )
            
            elif data == 'mail_system':
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "📝 Xabar tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.message_manager
                )
            
            elif data == 'channel_management':
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "📢 Kanallar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.channel_manager
                )
            
            elif data == 'block_system':
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "🔐 Blok tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.block_manager
                )
            
            elif data == 'bot_settings':
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "⚙️ Bot sozlamalari boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.bot_manager
                )
            
            elif data == 'admin_management':
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "👥 Adminlar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.admin_manager
                )
            
            elif data == 'forward_message':
                self.set_user_step(user_id, "waiting_forward")
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "🔄 Foydalanuvchilarga yuboriladigan xabarni forward qiling yoki yuboring!",
                    reply_markup=self.back_button
                )
            
            elif data == 'add_channel':
                self.set_user_step(user_id, "waiting_channel")
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "📡 Kanal qo'shish uchun kanal havolasini yuboring!\n\n🔰 Format: @channel_username",
                    reply_markup=self.back_button
                )
            
            elif data == 'delete_channel':
                channels = self.get_channels()
                if not channels:
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "❌ Botga ulangan kanallar mavjud emas!",
                        reply_markup=self.channel_manager
                    )
                    return
                
                self.set_user_step(user_id, "deleting_channel")
                channels_text = '\n'.join([f"• {ch}" for ch in channels])
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    f"🗑️ O'chiriladigan kanal havolasini yuboring:\n\n{channels_text}",
                    reply_markup=self.back_button
                )
            
            elif data == 'channel_list':
                channels = self.get_channels()
                if not channels:
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "❌ Botga ulangan kanallar mavjud emas!",
                        reply_markup=self.channel_manager
                    )
                else:
                    channels_text = '\n'.join([f"• {ch}" for ch in channels])
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        f"📋 Botga ulangan kanallar ({len(channels)} ta):\n\n{channels_text}",
                        reply_markup=self.channel_manager
                    )
            
            elif data == 'clear_channels':
                channels = self.get_channels()
                if not channels:
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "❌ Botga ulangan kanallar mavjud emas!",
                        reply_markup=self.channel_manager
                    )
                else:
                    self.set_user_step(user_id, "confirm_clear_channels")
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "⚠️ Barcha kanallar ro'yxatini o'chirishni tasdiqlaysizmi?",
                        reply_markup=self.confirm_clear
                    )
            
            elif data == 'confirm_clear':
                current_step = self.get_user_step(user_id)
                if current_step == "confirm_clear_channels":
                    self.write_list_file(self.files['channels'], [])
                    self.clear_user_step(user_id)
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "✅ Barcha kanallar ro'yxati muvaffaqiyatli o'chirildi!",
                        reply_markup=self.channel_manager
                    )
                elif current_step == "confirm_clear_blocks":
                    self.write_list_file(self.files['blocks'], [])
                    self.clear_user_step(user_id)
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "✅ Barcha bloklanganlar ro'yxati muvaffaqiyatli o'chirildi!",
                        reply_markup=self.block_manager
                    )
                elif current_step == "confirm_clear_admins":
                    self.write_list_file(self.files['admins'], [str(user_id)])
                    self.clear_user_step(user_id)
                    self.edit_message_text(
                        call.message.chat.id,
                        call.message.message_id,
                        "✅ Barcha adminlar ro'yxati muvaffaqiyatli o'chirildi! (Siz admin qilib qoldirildingiz)",
                        reply_markup=self.admin_manager
                    )
            
            elif data == 'cancel_clear':
                self.clear_user_step(user_id)
                self.edit_message_text(
                    call.message.chat.id,
                    call.message.message_id,
                    "❌ Tozalash bekor qilindi!",
                    reply_markup=self.main_panel
                )
            
            # Qolgan callback lar uchun shu tartibda davom eting...
            
            self.answer_callback_query(call.id)
            
        except Exception as e:
            logger.error(f"Callback query boshqarishda xato: {e}")
            self.answer_callback_query(call.id, "❌ Xatolik yuz berdi!")
    
    def handle_message(self, message):
        """Xabarlarni boshqarish"""
        try:
            user_id = message.from_user.id
            text = message.text or message.caption or ""
            
            if not self.is_admin(user_id):
                return
            
            step = self.get_user_step(user_id)
            
            # Admin paneli bosilganda
            if text == "/admin" or text == "👨🏻‍💻 Boshqaruv paneli":
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    "👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.main_panel
                )
                return
            
            # Holatlar bo'yicha boshqarish
            if step:
                self.handle_user_step(user_id, text, message)
            else:
                self.handle_admin_command(user_id, text, message)
                
        except Exception as e:
            logger.error(f"Xabar boshqarishda xato: {e}")
    
    def handle_admin_command(self, user_id: int, text: str, message):
        """Admin komandalarini boshqarish"""
        try:
            # Bu yerda to'g'ridan-to'g'ri matnli komandalarni boshqarish
            # Asosan inline keyboard orqali boshqariladi
            pass
        except Exception as e:
            logger.error(f"Admin komanda boshqarishda xato: {e}")
    
    def handle_user_step(self, user_id: int, text: str, message):
        """Foydalanuvchi holatlarini boshqarish"""
        try:
            step = self.get_user_step(user_id)
            
            if text == "/cancel" or text == "◀️ Orqaga":
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    "👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
                    reply_markup=self.main_panel
                )
                return
            
            if step == "waiting_forward":
                self.handle_forward_message(user_id, message)
            
            elif step == "waiting_channel":
                self.handle_add_channel(user_id, text)
            
            elif step == "deleting_channel":
                self.handle_delete_channel(user_id, text)
            
            elif step == "waiting_block_user":
                self.handle_block_user(user_id, text)
            
            elif step == "waiting_unblock_user":
                self.handle_unblock_user(user_id, text)
            
            elif step == "waiting_add_admin":
                self.handle_add_admin(user_id, text)
            
            elif step == "waiting_remove_admin":
                self.handle_remove_admin(user_id, text)
                
        except Exception as e:
            logger.error(f"User step boshqarishda xato: {e}")
            self.send_message(user_id, "❌ Xatolik yuz berdi! Qaytadan urinib ko'ring.")
    
    def handle_forward_message(self, user_id: int, message):
        """Forward xabarni boshqarish"""
        try:
            users = self.get_statistics()
            if not users:
                self.send_message(user_id, "❌ Foydalanuvchilar ro'yxati bo'sh!", reply_markup=self.message_manager)
                return
            
            success_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    if message.content_type == 'text':
                        self.send_message(
                            int(user),
                            message.text,
                            parse_mode='HTML'
                        )
                    else:
                        self.copy_message(
                            int(user),
                            message.chat.id,
                            message.message_id
                        )
                    success_count += 1
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Xabar yuborishda xato {user}: {e}")
            
            self.clear_user_step(user_id)
            self.send_message(
                user_id,
                f"📊 Xabar yuborish natijasi:\n\n✅ Muvaffaqiyatli: {success_count}\n❌ Muvaffaqiyatsiz: {failed_count}",
                reply_markup=self.message_manager
            )
            
        except Exception as e:
            logger.error(f"Forward xabar boshqarishda xato: {e}")
            self.send_message(user_id, "❌ Xabar yuborishda xatolik!")
    
    def handle_add_channel(self, user_id: int, channel: str):
        """Kanal qo'shish"""
        try:
            if not self.validate_channel(channel):
                self.send_message(
                    user_id,
                    "❌ Noto'g'ri kanal formati!\n\n🔰 To'g'ri format: @channel_username",
                    reply_markup=self.back_button
                )
                return
            
            channels = self.get_channels()
            if channel in channels:
                self.send_message(
                    user_id,
                    "⚠️ Bu kanal allaqachon qo'shilgan!",
                    reply_markup=self.channel_manager
                )
            else:
                channels.append(channel)
                self.write_list_file(self.files['channels'], channels)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Kanal muvaffaqiyatli qo'shildi: {channel}",
                    reply_markup=self.channel_manager
                )
                
        except Exception as e:
            logger.error(f"Kanal qo'shishda xato: {e}")
            self.send_message(user_id, "❌ Kanal qo'shishda xatolik!")
    
    def handle_delete_channel(self, user_id: int, channel: str):
        """Kanalni o'chirish"""
        try:
            channels = self.get_channels()
            if channel in channels:
                channels.remove(channel)
                self.write_list_file(self.files['channels'], channels)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Kanal muvaffaqiyatli o'chirildi: {channel}",
                    reply_markup=self.channel_manager
                )
            else:
                self.send_message(
                    user_id,
                    "❌ Bunday kanal topilmadi!",
                    reply_markup=self.channel_manager
                )
                
        except Exception as e:
            logger.error(f"Kanal o'chirishda xato: {e}")
            self.send_message(user_id, "❌ Kanal o'chirishda xatolik!")
    
    def handle_block_user(self, user_id: int, target_user: str):
        """Foydalanuvchini bloklash"""
        try:
            if not self.validate_user_id(target_user):
                self.send_message(
                    user_id,
                    "❌ Noto'g'ri user ID formati!\n\n🔰 Faqat raqamlardan foydalaning.",
                    reply_markup=self.back_button
                )
                return
            
            blocked_users = self.get_blocked_users()
            if target_user in blocked_users:
                self.send_message(
                    user_id,
                    "⚠️ Ushbu foydalanuvchi allaqachon bloklangan!",
                    reply_markup=self.block_manager
                )
            else:
                blocked_users.append(target_user)
                self.write_list_file(self.files['blocks'], blocked_users)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Foydalanuvchi bloklandi: {target_user}",
                    reply_markup=self.block_manager
                )
                
        except Exception as e:
            logger.error(f"Foydalanuvchi bloklashda xato: {e}")
            self.send_message(user_id, "❌ Bloklashda xatolik!")
    
    def handle_unblock_user(self, user_id: int, target_user: str):
        """Foydalanuvchini blokdan olish"""
        try:
            blocked_users = self.get_blocked_users()
            if target_user in blocked_users:
                blocked_users.remove(target_user)
                self.write_list_file(self.files['blocks'], blocked_users)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Foydalanuvchi blokdan olindi: {target_user}",
                    reply_markup=self.block_manager
                )
            else:
                self.send_message(
                    user_id,
                    "❌ Ushbu foydalanuvchi bloklanmagan!",
                    reply_markup=self.block_manager
                )
                
        except Exception as e:
            logger.error(f"Blokdan olishda xato: {e}")
            self.send_message(user_id, "❌ Blokdan olishda xatolik!")
    
    def handle_add_admin(self, user_id: int, new_admin: str):
        """Yangi admin qo'shish"""
        try:
            if not self.validate_user_id(new_admin):
                self.send_message(
                    user_id,
                    "❌ Noto'g'ri user ID formati!\n\n🔰 Faqat raqamlardan foydalaning.",
                    reply_markup=self.back_button
                )
                return
            
            admins = self.get_admins()
            if new_admin in admins:
                self.send_message(
                    user_id,
                    "⚠️ Ushbu foydalanuvchi allaqachon admin!",
                    reply_markup=self.admin_manager
                )
            else:
                admins.append(new_admin)
                self.write_list_file(self.files['admins'], admins)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Yangi admin qo'shildi: {new_admin}",
                    reply_markup=self.admin_manager
                )
                
        except Exception as e:
            logger.error(f"Admin qo'shishda xato: {e}")
            self.send_message(user_id, "❌ Admin qo'shishda xatolik!")
    
    def handle_remove_admin(self, user_id: int, admin_id: str):
        """Admindan olish"""
        try:
            admins = self.get_admins()
            if admin_id in admins:
                if admin_id == str(user_id):
                    self.send_message(
                        user_id,
                        "❌ O'zingizni adminlikdan ola olmaysiz!",
                        reply_markup=self.admin_manager
                    )
                    return
                
                admins.remove(admin_id)
                self.write_list_file(self.files['admins'], admins)
                self.clear_user_step(user_id)
                self.send_message(
                    user_id,
                    f"✅ Adminlikdan olindi: {admin_id}",
                    reply_markup=self.admin_manager
                )
            else:
                self.send_message(
                    user_id,
                    "❌ Ushbu foydalanuvchi admin emas!",
                    reply_markup=self.admin_manager
                )
                
        except Exception as e:
            logger.error(f"Adminlikdan olishda xato: {e}")
            self.send_message(user_id, "❌ Adminlikdan olishda xatolik!")
    
    # Telegram API metodlari
    def send_message(self, chat_id: int, text: str, reply_markup=None, parse_mode='HTML', **kwargs):
        """Xabar yuborish"""
        try:
            return self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=True,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Xabar yuborishda xato {chat_id}: {e}")
            raise
    
    def edit_message_text(self, chat_id: int, message_id: int, text: str, reply_markup=None, parse_mode='HTML'):
        """Xabarni tahrirlash"""
        try:
            return self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Xabarni tahrirlashda xato: {e}")
            raise
    
    def copy_message(self, chat_id: int, from_chat_id: int, message_id: int, reply_markup=None):
        """Xabarni nusxalash"""
        try:
            return self.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"Xabarni nusxalashda xato: {e}")
            raise
    
    def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False):
        """Callback query ga javob berish"""
        try:
            return self.bot.answer_callback_query(
                callback_query_id=callback_query_id,
                text=text,
                show_alert=show_alert
            )
        except Exception as e:
            logger.error(f"Callback query ga javob berishda xato: {e}")
            raise

# Foydalanish misoli
"""
import telebot

# Botni yaratish
bot = telebot.TeleBot("YOUR_BOT_TOKEN")
admin_panel = AdminPanel(bot)

# Callback query lar uchun handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    admin_panel.handle_callback_query(call)

# Barcha xabarlar uchun handler
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    admin_panel.handle_message(message)

# Start komandasi
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if admin_panel.is_admin(user_id):
        admin_panel.send_message(
            user_id,
            "👋 Assalomu alaykum! Boshqaruv paneliga kirish uchun /admin buyrug'ini yuboring."
        )
    else:
        admin_panel.send_message(
            user_id,
            "👋 Assalomu alaykum! Botga xush kelibsiz."
        )

# Admin komandasi
@bot.message_handler(commands=['admin'])
def handle_admin(message):
    user_id = message.from_user.id
    if admin_panel.is_admin(user_id):
        admin_panel.clear_user_step(user_id)
        admin_panel.send_message(
            user_id,
            "👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!",
            reply_markup=admin_panel.main_panel
        )
    else:
        admin_panel.send_message(user_id, "❌ Sizda admin huquqi yo'q!")

if __name__ == "__main__":
    logger.info("Bot ishga tushdi...")
    bot.polling(none_stop=True)
"""