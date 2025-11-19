<?php
// Admin paneli funksiyalari
$admin = array($administrator, $admins); // Adminlar ro'yxati

if(in_array($cid, $admin)) {
    // Boshqaruv paneli
    if($text == "👨🏻‍💻 Boshqaruv paneli") {
        unlink("step/$cid/$cid.txt");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>👨🏻‍💻 Boshqaruv paneliga xush kelibsiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $panel,
        ]);
    }

    // Pochta tizimi
    if($text == "📝 Pochta tizimi") {
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>📝 Pochta tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $message_manager,
        ]);
    }

    // Forward xabar yuborish
    if($text == "💬 Forward xabar yuborish") {
        file_put_contents("step/$cid/$cid.txt", "forward");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>👥 Foydalanuvchilarga yuboriladigan xabarni forward qiling!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
            'disable_web_page_preview' => true,
        ]);
    }

    // Kanallar boshqaruvi
    if($text == "📢 Kanallar boshqaruvi") {
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>📢 Kanallar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $channel_manager,
        ]);
    }

    // Kanal qo'shish
    if($text == "📢 Kanal qoʻshish") {
        file_put_contents("step/$cid/$cid.txt", "kanal");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>📡 Kanal qo'shish uchun kanal havolasini yuboring!\n🔰 Masalan: @JM_Blogs</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
        ]);
    }

    // Kanalni o'chirish
    if($text == "📢 Kanalni oʻchirish") {
        file_put_contents("step/$cid/$cid.txt", "delete");
        $soni = substr_count($kanal, "@");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>📡 Kanalni oʻchirish uchun kanal havolasini yuboring!\n\n🔰 Masalan: @JM_Blogs\n\n👇 Botga ulangan kanallar:\n$kanal\n\n📝 Jami kanallar soni: $soni ta</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
        ]);
    }

    // Kanallar ro'yxati
    if($text == "📋 Kanallar roʻyxati") {
        if($kanal == null) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botga ulangan kanallar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        } else {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Kanallar roʻyxati:\n$kanal</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        }
    }

    // Kanallar ro'yxatini o'chirish
    if($text == "📋 Kanallar roʻyxatini oʻchirish") {
        if($kanal == null) {
            unlink("data/kanal.txt");
            unlink("data/channel.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botga ulangan kanallar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        } else {
            unlink("data/kanal.txt");
            unlink("data/channel.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Kanallar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        }
    }

    // Blok tizimi
    if($text == "🔐 Blok tizimi") {
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>🔐 Blok tizimi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $blok_manager,
        ]);
    }

    // Blokdan olish
    if($text == "✅ Blokdan olish") {
        file_put_contents("step/$cid/$cid.txt", "unblock");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>🚫 Blokdan olinadigan foydalanuvchini ID raqamini kiriting!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
        ]);
    }

    // Bloklash
    if($text == "❌ Bloklash") {
        file_put_contents("step/$cid/$cid.txt", "block");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>🚫 Bloklanadigan foydalanuvchini ID raqamini kiriting!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
        ]);
    }

    // Bloklanganlar ro'yxati
    if($text == "📋 Bloklanganlar roʻyxati") {
        if($blocks == null) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botdan bloklanganlar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        } else {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botdan bloklanganlar roʻyxati:\n$blocks</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        }
    }

    // Bloklanganlar ro'yxatini o'chirish
    if($text == "📋 Bloklanganlar roʻyxatini oʻchirish") {
        if($blocks == null) {
            unlink("data/blocks.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botdan bloklanganlar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        } else {
            unlink("data/blocks.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Bloklanganlar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        }
    }

    // Bot sozlamalari
    if($text == "⚙ Bot sozlamalari") {
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>⚙ Bot sozlamalari boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $bot_manager,
        ]);
    }

    // Botni yoqish
    if($text == "✅ Botni yoqish") {
        unlink("data/bot.txt");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>⚠️ Bot muvaffaqiyatli yoqildi!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $bot_manager,
        ]);
    }

    // Botni o'chirish
    if($text == "❌ Botni o'chirish") {
        file_put_contents("data/bot.txt", "off");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>⚠️ Bot muvaffaqiyatli oʻchirildi!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $bot_manager,
        ]);
    }

    // Adminlar boshqaruvi
    if($text == "📋 Adminlar boshqaruvi") {
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>📋 Adminlar boshqaruvi boʻlimidasiz!\n📋 Quyidagi boʻlimlardan birini tanlang!</b>",
            'parse_mode' => 'html',
            'reply_markup' => $admins_manager,
        ]);
    }

    // Admin qo'shish
    if($text == "➕ Admin qoʻshish") {
        file_put_contents("step/$cid/$cid.txt", "setadmins");
        bot('sendMessage', [
            'chat_id' => $cid,
            'text' => "<b>👨‍💻 Administrator qoʻshish uchun foydalanuvchi ID raqamini kiriting</b>",
            'parse_mode' => 'html',
            'reply_markup' => $ortga,
        ]);
    }

    // Adminlikdan olish
    if($text == "🛑 Adminlikdan olish") {
        if($admins == null) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botda administratorlar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        } else {
            file_put_contents("step/$cid/$cid.txt", "deladmins");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>👨‍💻 Administratorni olib tashlash uchun foydalanuvchi ID raqamini kiriting</b>",
                'parse_mode' => 'html',
                'reply_markup' => $ortga,
            ]);
        }
    }

    // Adminlar ro'yxati
    if($text == "📋 Adminlar roʻyxati") {
        if($admins == null) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botda administratorlar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        } else {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Administratorlar roʻyxati:\n$admins</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        }
    }

    // Adminlar ro'yxatini o'chirish
    if($text == "📋 Adminlar roʻyxatini oʻchirish") {
        if($admins == null) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Botda administratorlar mavjud emas!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        } else {
            unlink("data/admins.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 Administratorlar roʻyxati muvaffaqiyatli oʻchirildi!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        }
    }

    // Step larni boshqarish
    if($step == "forward" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        unlink("step/$cid/$cid.txt");
        $explode = explode("\n", $statistika);
        foreach($explode as $id) {
            $forward = bot('forwardMessage', [
                'chat_id' => $id, 
                'from_chat_id' => $cid, 
                'message_id' => $mid, 
            ]);
        }
        
        if($forward) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>👥 Forward xabaringiz barcha bot foydalanuvchilariga yuborildi!✅</b>",
                'parse_mode' => 'html',
                'reply_markup' => $message_manager,
            ]);
        }
    }

    if($step == "kanal" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        if(mb_stripos($kanal, "$text") !== false) {
            // Kanal allaqachon mavjud
        } else {
            file_put_contents("data/kanal.txt", "$kanal\n$text");
            file_put_contents("data/channel.txt", "true");
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📡 Kanalingiz botga muvaffaqiyatli qo'shildi!\n🤖 Endi botni kanalingizga admin qiling!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        }
    }

    if($step == "delete" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        if(mb_stripos($kanal, "$text") !== false) {
            $k = str_replace("\n" . $text . "", "", $kanal);
            file_put_contents("data/kanal.txt", $k);
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>🔰 $text muvaffaqiyatli oʻchirildi! ✅</b>",
                'parse_mode' => 'html',
                'reply_markup' => $channel_manager,
            ]);
        }
    }

    if($step == "unblock" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        unlink("step/$cid/$cid.txt");
        if(mb_stripos($blocks, $text) == false) {
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>👨🏻‍💻 Ushbu foydalanuvchi botdan bloklanmagan!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        } else {
            $bl = str_replace("$text", " ", $blocks);
            file_put_contents("data/blocks.txt", "$bl");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>🔰 Foydalanuvchi blokdan olindi! ✅</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
            bot('sendMessage', [
                'chat_id' => $text,
                'text' => "<b>🎉 Siz blokdan muvaffaqiyatli olindingiz!\n\n🔄 Yana botni ishlatishingiz mumkin!\n\n🤖 Botga qayta /start bosing ✅</b>",
                'parse_mode' => 'html',
                'reply_markup' => $home,
            ]);
        }
    }

    if($step == "block" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        if(mb_stripos($blocks, $text) == false) {
            file_put_contents("data/blocks.txt", "$blocks\n$text");
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>🔰 Foydalanuvchi bloklandi! ✅</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
            bot('sendMessage', [
                'chat_id' => $text,
                'text' => "<b>🚫 Siz bizning botimizdan bloklandingiz!\n\n🔄 Endi botdan foydalana olmaysiz!\n\n👨‍💻 Blokdan chiqish uchun bot administratoriga murojaat qiling!</b>",
                'parse_mode' => 'html',
                'reply_markup' => json_encode(['remove_keyboard' => true])
            ]);
        } else {
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>👨🏻‍💻 Ushbu foydalanuvchi botdan allaqachon bloklangan!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $blok_manager,
            ]);
        }
    }

    if($step == "setadmins" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        if(is_numeric($text)) {
            if(mb_stripos($statistika, $text) !== false) {
                file_put_contents("data/admins.txt", "$admins\n$text");
                unlink("step/$cid/$cid.txt");
                bot('sendMessage', [
                    'chat_id' => $cid,
                    'text' => "<b>📝 <a href = 'tg://user?id=$text'>$text</a> ID raqamli foydalanuvchi botga administrator qilib tayinlandi!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $admins_manager,
                ]);
                bot('sendMessage', [
                    'chat_id' => $text,
                    'text' => "<b>👨‍💻 Siz botga administrator qilib tayinlandingiz!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $home,
                ]);
            } else {
                unlink("step/$cid/$cid.txt");
                bot('sendMessage', [
                    'chat_id' => $cid,
                    'text' => "<b>👨‍💻 Ushbu foydalanuvchi bazada mavjud emas!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $admins_manager,
                ]);
            }
        } else {
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 ID raqam kiritayotganda faqat raqamlardan foydalaning!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        }
    }

    if($step == "deladmins" && $text != "/start" && $text != $back && $text != "👨🏻‍💻 Boshqaruv paneli") {
        if(is_numeric($text)) {
            if(mb_stripos($admins, $text) !== false) {
                $ad = str_replace("\n" . $text . "", "", $admins);
                file_put_contents("data/admins.txt", $ad);
                unlink("step/$cid/$cid.txt");
                bot('sendMessage', [
                    'chat_id' => $cid,
                    'text' => "<b>📋 <a href = 'tg://user?id=$text'>$text</a> ID raqamli foydalanuvchi bot administratorligidan olib tashlandi!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $admins_manager,
                ]);
                bot('sendMessage', [
                    'chat_id' => $text,
                    'text' => "<b>👨‍💻 Siz bot administratorligidan olib tashlandingiz!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $home,
                ]);
            } else {
                bot('sendMessage', [
                    'chat_id' => $cid,
                    'text' => "<b>📋 <a href = 'tg://user?id=$text'>$text</a> ID raqamli foydalanuvchi botda administrator emas!</b>",
                    'parse_mode' => 'html',
                    'reply_markup' => $admins_manager,
                ]);
            }
        } else {
            unlink("step/$cid/$cid.txt");
            bot('sendMessage', [
                'chat_id' => $cid,
                'text' => "<b>📋 ID raqam kiritayotganda faqat raqamlardan foydalaning!</b>",
                'parse_mode' => 'html',
                'reply_markup' => $admins_manager,
            ]);
        }
    }
}
?>