from highrise import BaseBot, Position, User
from highrise.models import SessionMetadata
import asyncio

class MyBot(BaseBot):
    # تعريف أوامر الرقص بمعرف الإيموت
    dance_commands = {
        "!1": "dance-macarena",
        "!2": "dance-5417",
        "!3": "dance-tiktok2",
        # يمكن إضافة أوامر أخرى لاحقًا
    }
    # تعريف مواقع للتليبور (مثال: "home", "stage", "upstairs")
    teleport_positions = {
        "a": Position(20.0, 0.0, 6.0, "FrontLeft"),
        "stage": Position(5.0, 0.0, 5.0, "FrontRight"),
        "upstairs": Position(0.0, 3.0, 0.0, "FrontLeft"),  # مثال لفصل طابق
        # أضف مواقع أخرى حسب الحاجة
    }

    def _init_(self):
        super()._init_()
        self.loop_tasks = {}  # لتخزين مهام الرقص المتكرر لكل مستخدم

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        # تخزين معرف البوت
        self.bot_id = session_metadata.user_id
        # تحريك البوت إلى الموقع المحدد عند البدء
        initial_pos = Position(10.5, 0.0, 2.0, "FrontLeft")
        await self.highrise.teleport(self.bot_id, initial_pos)
        # إرسال رسالة ترحيبية (اختياري)
        await self.highrise.chat("hawa ja tani !")
        # بدء المهمة الدورية لإرسال رسالة كل فترة
        asyncio.create_task(self.periodic_message_loop())

    async def periodic_message_loop(self):
        # إرسال رسالة كل 60 ثانية
        while True:
            await asyncio.sleep(60)
            await self.highrise.chat("mra mra tfkroniiii.")

    async def on_user_join(self, user: User, position: Position) -> None:
        # رسالة ترحيب للمستخدم الجديد
        await self.highrise.chat(f"mrhba @{user.username}!  room roomk  🎉")
        # إرسال إيموت ترحيبي (مثل المصافحة)
        await self.highrise.send_emote("emote-hello")
        await self.highrise.react("heart", user.id)

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.strip()
        msg_lower = msg.lower()

        # أوامر الرقص المحددة (!1, !2, ...)
        if msg in self.dance_commands:
            emote_id = self.dance_commands[msg]
            await self.highrise.send_emote(User.id)
            return

        # أمر loop لبدء رقص متكرر للمستخدم
        if msg_lower.startswith("!loop"):
            parts = msg_lower.split()
            if len(parts) > 1 and f"!{parts[1]}" in self.dance_commands:
                key = f"!{parts[1]}"
                emote_loop = self.dance_commands[key]
                # إذا المستخدم ليس في دورة رقص حالياً
                if user.id not in self.loop_tasks:
                    # إنشاء مهمة رقص متكرر لهذا المستخدم
                    task = asyncio.create_task(self.dance_loop(user.id, emote_loop))
                    self.loop_tasks[user.id] = task
                    await self.highrise.chat(f"بدء الرقص المتكرر {parts[1]} لـ {user.username} 💃")
            return

        # أمر stop لإيقاف الرقص المتكرر
        if msg_lower == "!stop":
            if user.id in self.loop_tasks:
                self.loop_tasks[user.id].cancel()
                del self.loop_tasks[user.id]
                await self.highrise.chat(f"تم إيقاف الرقص المتكرر لـ {user.username}.")
            return

        # أوامر teleport لنقل المستخدم
        if msg_lower.startswith("!teleport"):
            parts = msg_lower.split()
            if len(parts) > 1:
                key = parts[1]
                if key in self.teleport_positions:
                    target_pos = self.teleport_positions[key]
                    try:
                        await self.highrise.teleport(user.id, target_pos)
                    except Exception as e:
                        await self.highrise.chat(f"خطأ في النقل: {e}")
            return

    async def dance_loop(self, user_id: str, emote_id: str) -> None:
        # تكرار إرسال إيموت الرقص لكل 5 ثواني
        try:
            while True:
                await self.highrise.send_emote(emote_id, target_user_id=user_id)
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            # عند إلغاء المهمة (أمر stop)، نوقف الحلقة بهدوء
            return

    
# لتشغيل البوت: highrise mybot:MyBot <room_id> <api_token>