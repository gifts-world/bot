from highrise import Highrise
from mybot import MyBot  # إذا كان الكود الأصلي محفوظ في ملف اسمه mybot.py

if __name__ == "_main_":
    Highrise(token="4c216e4498fa8fc8b462f20d7de0afb84ab79520060f4f6f858c10d32a53b37c", room_id="60b507ce5f29accda0a8e4a0").run(MyBot())