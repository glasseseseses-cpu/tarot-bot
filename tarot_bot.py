import random
import discord
from discord.ext import commands
from datetime import date
import os

# =====================
# Bot基本設定
# =====================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================
# 1日1回制限用データ
# =====================
last_tarot_date = {}

# =====================
# タロットカード（大アルカナ・正逆）
# =====================
tarot_cards = [
    ("愚者", "正位置", "新しい始まり、自由、可能性"),
    ("愚者", "逆位置", "無計画、迷走"),
    ("魔術師", "正位置", "才能、創造力、実行力"),
    ("魔術師", "逆位置", "空回り、不誠実"),
    ("女教皇", "正位置", "直感、知性、静かな理解"),
    ("女教皇", "逆位置", "混乱、感情の揺れ"),
    ("女帝", "正位置", "愛情、豊かさ、成長"),
    ("女帝", "逆位置", "依存、停滞"),
    ("皇帝", "正位置", "安定、責任、支配力"),
    ("皇帝", "逆位置", "未熟、混乱"),
    ("恋人", "正位置", "選択、愛、調和"),
    ("恋人", "逆位置", "迷い、不一致"),
    ("戦車", "正位置", "勝利、前進、意志"),
    ("戦車", "逆位置", "暴走、停滞"),
    ("隠者", "正位置", "内省、探求、知恵"),
    ("隠者", "逆位置", "孤立、逃避"),
    ("運命の輪", "正位置", "転機、幸運、流れ"),
    ("運命の輪", "逆位置", "停滞、不運"),
    ("死神", "正位置", "終わりと再生、変化"),
    ("死神", "逆位置", "変化への拒否"),
    ("星", "正位置", "希望、癒し、未来"),
    ("星", "逆位置", "不安、失望"),
    ("月", "正位置", "不安、幻想"),
    ("月", "逆位置", "真実、解放"),
    ("太陽", "正位置", "成功、幸福"),
    ("太陽", "逆位置", "過信、失敗"),
    ("審判", "正位置", "復活、目覚め"),
    ("審判", "逆位置", "後悔、停滞"),
    ("世界", "正位置", "完成、達成"),
    ("世界", "逆位置", "未完成、足踏み"),
]

# =====================
# Bot人格（完全固定）
# =====================
persona = {
    "name": "占い師・ヤヨイ＝ユーティライネン",
    "self_pronoun": "ボク",
    "opening": [
        "🃏 *……来たね。カードを引こうか*",
        "🃏 *静かに。ボクが視る*",
    ],
    "body_positive": [
        "流れは悪くない。無理に抗わなくていい。",
        "少なくとも、希望はまだ残ってるよ。",
    ],
    "body_negative": [
        "正直に言うね。今は慎重になった方がいい。",
        "停滞気味。でも、それは永遠じゃない。",
    ],
    "ending": [
        "答えはカードが示した。どう動くかは{name}次第。",
        "今日はここまで。また必要になったら呼んで。",
    ],
    "limit": [
        "……{name}、今日はもう占ったよ。欲張りは嫌い。",
        "同じ日に何度も占いはしない。明日また来て。",
    ]
}

# =====================
# 起動時
# =====================
@bot.event
async def on_ready():
    print(f"起動しました：{bot.user}")

# =====================
# tarotコマンド
# =====================
@bot.command()
async def tarot(ctx, *, question: str = None):
    user_id = ctx.author.id
    today = date.today()
    name = ctx.author.display_name

    # --- 1日1回制限 ---
    if user_id in last_tarot_date and last_tarot_date[user_id] == today:
        line = random.choice(persona["limit"]).format(name=name)
        await ctx.send(line)
        return

    last_tarot_date[user_id] = today

    # --- カード選択 ---
    card_name, position, meaning = random.choice(tarot_cards)

    opening = random.choice(persona["opening"])
    ending = random.choice(persona["ending"]).format(name=name)

    # --- 質問文処理 ---
    if question:
        question = question.rstrip("？?")
        question_line = f"{persona['self_pronoun']}は「{question}」について視た。"
    else:
        question_line = f"{persona['self_pronoun']}は、今の流れを視た。"

    # --- 正逆で語り分岐 ---
    if position == "正位置":
        body = random.choice(persona["body_positive"])
    else:
        body = random.choice(persona["body_negative"])

    message = (
        f"{opening}\n"
        f"{question_line}\n"
        f"**《{card_name}・{position}》**\n"
        f"{body}\n"
        f"意味：{meaning}\n"
        f"{ending}"
    )

    await ctx.send(message)

# =====================
# Bot起動
# =====================
bot.run(os.getenv("DISCORD_TOKEN"))

import threading
import http.server
import socketserver
import os

def dummy_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=dummy_server, daemon=True).start()
