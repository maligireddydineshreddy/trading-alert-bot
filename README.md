

```markdown
# 🚀 Universal Trading Alert Bot

A real-time trading alert platform supporting:

- 💱 Forex
- 🪙 Crypto
- 🥇 Commodities
- 📊 Indices

The bot monitors live market prices and sends instant alerts through:

- Telegram Notifications
- Pushover Emergency Notifications


---

# ✨ Features

## 📈 Market Monitoring

Supported markets:

### Forex (FXCM)

Examples:

- EURUSD
- GBPUSD
- USDJPY
- GBPJPY


### Crypto (Binance)

Examples:

- BTCUSDT
- ETHUSDT
- SOLUSDT
- XRPUSDT


### Commodities

Examples:

- XAUUSD
- XAGUSD
- USOIL
- COPPER


### Indices

Examples:

- SPX500
- US30
- NAS100


---

# 🔔 Notifications

## Telegram

Every user receives:

- Price hit alerts
- Alert completion messages
- Bot status information


## Pushover

Optional emergency notification system.

Features:

- User-specific Pushover keys
- Key validation
- Emergency priority alerts
- Test notifications


---

# 🏗 Project Structure


```
trading-alert-bot/

│
├── bot.py
├── monitor.py
├── database.py
├── fxcm.py
├── crypto.py
├── pushover.py
│
├── requirements.txt
├── Dockerfile
├── README.md
├── .env.example
│
└── data/
    └── trading_alerts.db
```


---

# ⚙️ Requirements

Before deployment you need:

- GitHub account
- Railway account
- Telegram account
- FXCM demo account
- Binance API access (public market data)
- Pushover account (optional)


---

# 🚀 Deploy on Railway


## Step 1 — Fork Repository

Open the GitHub repository.

Click:

```
Fork
```

Create your own copy.


---

# Step 2 — Create Railway Project


Go to Railway:

https://railway.app


Login with GitHub.


Click:

```
New Project
```

Select:

```
Deploy from GitHub Repo
```


Choose:

```
trading-alert-bot
```


Railway will automatically start building.


---

# Step 3 — Add Environment Variables


Open:

```
Railway Project
        ↓
Service
        ↓
Variables
```


Add the following:


## Telegram Bot Token


```
BOT_TOKEN=
```


Create one:

1. Open Telegram
2. Search:

```
@BotFather
```

3. Send:

```
/newbot
```

4. Copy the token.


---

## FXCM Credentials


```
FXCM_USERNAME=
FXCM_PASSWORD=
FXCM_URL=
```


Create a demo account:

FXCM Demo Account


---

## Pushover App Token


(Optional)


```
PUSHOVER_APP_TOKEN=
```


Create:

- Pushover account
- Application
- Copy API token


---

## Database Location


Add:


```
DATA_DIR=/app/data
```


---

# Step 4 — Add Railway Volume


The bot uses SQLite database storage.

Without a volume:

- Restart = database lost
- Redeploy = users lost
- Alerts lost


Go to:


```
Railway
 ↓
Service
 ↓
Volumes
 ↓
Add Volume
```


Set mount path:


```
/app/data
```


---

# Step 5 — Deploy


Railway will automatically:

1. Install dependencies
2. Start Python application
3. Run bot.py


Successful logs:


```
STEP 1

STEP 2

Connecting FXCM...

STEP 3

STEP 4

🚀 Bot Started

📡 Monitor running
```


---

# 📱 Using The Bot


Open your Telegram bot.


Send:


```
/start
```


Main menu:


```
📈 Add Alert
📋 My Alerts

🗑 Remove Alert
🔔 Notification Settings

ℹ️ Status
```


---

# 🔔 Setting Up Pushover


Open:

```
Notification Settings
```


If disabled:


```
🔑 Enter Pushover Key
```


Paste your Pushover User Key.


The bot will:

1. Validate key
2. Save key
3. Enable notifications


---

# 🖥 Local Installation


Clone repository:


```bash
git clone YOUR_REPOSITORY_URL

cd trading-alert-bot
```


Install dependencies:


```bash
pip install -r requirements.txt
```


Create environment file:


```
.env
```


Add variables:


```
BOT_TOKEN=

FXCM_USERNAME=
FXCM_PASSWORD=
FXCM_URL=

PUSHOVER_APP_TOKEN=

DATA_DIR=./data
```


Run:


```bash
python bot.py
```


---

# 🔐 Security


Never upload:


```
.env
*.db
*.sqlite
logs/
```


Your repository should contain:


```
.env.example
```


not:


```
.env
```


---

# 🗄 Database


The bot uses SQLite.


Stored data:


- Users
- Pushover settings
- Active alerts
- Alert history


Database location:


```
/app/data/trading_alerts.db
```


Railway Volume is required for persistence.


---

# 🛠 Troubleshooting


## Bot does not start


Check Railway logs:

```
Deployments
 ↓
Logs
```


Common causes:

- Missing environment variables
- Incorrect FXCM credentials
- Missing dependencies


---

## FXCM disconnected


Check:


```
FXCM_USERNAME
FXCM_PASSWORD
FXCM_URL
```


---

## Pushover not working


Check:


```
PUSHOVER_APP_TOKEN
```


and verify user key.


---

# 📌 Future Improvements

Possible additions:

- Database backup system
- User onboarding
- Multiple notification channels
- Web dashboard
- User authentication


---

# 📜 License

Open source project.

Use responsibly.
```

---

This README is written so **a third-party developer can deploy the bot on Railway without asking you anything**. It also explains the critical part you discovered: **Railway Volume must be mounted at `/app/data` or the database will disappear after redeploys.**
