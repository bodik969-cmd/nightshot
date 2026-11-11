# NightShot

A consent-based camera page that sends a user-captured photo to the configured Telegram chat.

## Configure
Set these environment variables on your hosting provider:
- `BOT_TOKEN`: the NEW token from BotFather (keep it secret; never put it in frontend code or share it).
- `CHAT_ID`: `1513272617`

The bot must be started by the receiving Telegram account before it can message that account.

## Deploy
1. Upload this folder to a private GitHub repository.
2. Create a new Web Service on Render and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add the two environment variables above.
6. Deploy. Use the HTTPS URL Render provides; camera access requires HTTPS (or localhost).

The page asks for consent, then the visitor must separately press the camera button and the capture/send button. It does not take photos automatically.