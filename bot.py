import discord
import requests
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# DiscordボットのトークンとSlackのWebhook URLを環境変数から取得
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# Intentsの設定
intents = discord.Intents.default()
intents.voice_states = True  # ボイスチャンネルの状態を監視
intents.guilds = True
intents.members = True  # メンバー情報を取得

# Discordクライアントの初期化
client = discord.Client(intents=intents)

EXCLUDED_CHANNELS = ['1on1']

def send_slack_message(message):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print(f"Slack webhook failed with status {response.status_code}: {response.text}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if (before.channel and before.channel.name in EXCLUDED_CHANNELS) or (after.channel and after.channel.name in EXCLUDED_CHANNELS):
        return

    if before.channel is None and after.channel is not None:
        # メンバーがボイスチャンネルに参加した
        message = f"{member.display_name} がボイスチャンネル 「{after.channel.name}」 に参加しました！"
        send_slack_message(message)
    # elif before.channel is not None and after.channel is None:
    #     message = f"{member.display_name} がボイスチャンネル 「{before.channel.name}」 から退出しました！"
    #     send_slack_message(message)
    elif before.channel != after.channel:
        message = f"{member.display_name} がボイスチャンネル 「{before.channel.name}」 から 「{after.channel.name}」 に移動しました！"
        send_slack_message(message)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
