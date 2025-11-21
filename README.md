# X-OPTIMUS TG BOT

<p align="center">
  <img src="assets/readme.jpg" alt="X-OPTIMUS TG BOT Menu" width="600">
</p>

<p align="center">
  <strong>A feature-rich Telegram automation bot developed in Python</strong><br>
  Offering extensive management capabilities and seamless integration
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Telegram-Bot-0088CC?logo=telegram" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

---

## 📦 PREREQUISITES

Before deploying your bot, you'll need these essential credentials:

### 1️⃣ API Credentials
Get your **API ID** and **API Hash** from [my.telegram.org](https://my.telegram.org)

<p align="center">
  <a href="https://youtube.com/shorts/9A04yQnUD5I?si=qLCV9B-Trwi6-1Vj">
    <img src="https://img.shields.io/badge/🎥_Watch_Tutorial-Get_API_Credentials-FF0000?style=for-the-badge&logo=youtube" alt="API Credentials Tutorial">
  </a>
</p>

### 2️⃣ Session String
Generate your session string using our secure tool:

<p align="center">
  <a href="https://optimus-frontend-blush.vercel.app/">
    <img src="https://img.shields.io/badge/🔑_Generate-Session%20String-0088CC?style=for-the-badge&logo=telegram" alt="Session String Generator">
  </a>
</p>

---

## 🚀 DEPLOYMENT OPTIONS

Choose your preferred platform and deploy in minutes!

### 🟣 Option 1: Render Platform

<p align="center">
  <a href="https://render.com/deploy">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

**Quick Setup:**
- One-click deployment with pre-configured `render.yaml`
- Add environment variables during setup:
  - `API_ID` - Your Telegram API ID
  - `API_HASH` - Your Telegram API Hash
  - `SESSION_STRING` - Generated session string
- ✅ **Auto-updates enabled** - Always stays current

---

### 🔵 Option 2: Koyeb Platform

<p align="center">
  <a href="https://app.koyeb.com/deploy">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb">
  </a>
</p>

**Quick Setup:**
- Seamless deployment with included `koyeb.yaml`
- Configure environment variables:
  - `API_ID` - Your Telegram API ID
  - `API_HASH` - Your Telegram API Hash
  - `SESSION_STRING` - Generated session string
- Global infrastructure for optimal performance
- ✅ **Auto-updates enabled** - Stays synchronized automatically

---

### ⚙️ Option 3: Control Panel Deployment

**Step-by-Step Guide:**

1. **Upload Files** - Transfer all bot files to your hosting panel
2. **Extract** - Unzip if uploaded as compressed archive
3. **Position Files** - Move to container root directory (`../`)
4. **Configure Startup** - Set `main.py` as entry point
5. **Environment Setup** - Add to `config_data/config.env`:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   SESSION_STRING=your_session_string
-Launch - Start the bot from your control panel

-🔧 Note: **Manual** updates required using **/update** command


## 🟢 KEEP YOUR BOT ONLINE 24/7

Render's free plan sleeps after 15 minutes of inactivity. Here's how to keep it awake:

### ✅ Step 1: Verify Web Server
Ensure your bot runs a web server and has a Render URL like:
https://your-bot-name.onrender.com
### ✅ Step 2: Create UptimeRobot Account
Visit [uptimerobot.com](https://uptimerobot.com/) and sign up

### ✅ Step 3: Add Monitor
Click **Add New Monitor** and configure:

| Field | Value |
|-------|-------|
| **Monitor Type** | HTTP(s) |
| **Friendly Name** | Your Bot Name |
| **URL** | `https://your-render-url.onrender.com/` |
| **Monitoring Interval** | Every 5 minutes |
| **Status** | Enabled ✓ |

**How it works:** UptimeRobot pings your bot every 5 minutes → Render sees activity → Bot stays awake 24/7! 🎉

---

## 🏆 DEVELOPER

<p align="center">
  <strong>Created with ❤️ by Lucas</strong>
</p>

<p align="center">
  <a href="https://t.me/codlucas">
    <img src="https://img.shields.io/badge/Telegram-@codlucas-0088CC?style=for-the-badge&logo=telegram" alt="Telegram">
  </a>
  <a href="https://github.com/COD-LUCAS">
    <img src="https://img.shields.io/badge/GitHub-COD--LUCAS-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

---

## 💬 SUPPORT & COMMUNITY

Need help or have suggestions?

- 💡 **Telegram Support:** [@codlucas](https://t.me/codlucas)
- 📚 **Documentation:** [GitHub Repository](https://github.com/COD-LUCAS)
- 🐛 **Report Issues:** [Issue Tracker](https://github.com/COD-LUCAS/issues)

---

## ⚠️ IMPORTANT ARCHITECTURE NOTICE

> **Interconnected File Structure**
> 
> This project uses a synchronized architecture where all components update together. The only file safe to modify locally is:
> 
> **`config_data/config.env`** ← Your configuration file
> 
> **⚡ Important:** Custom changes to other files will be overwritten during updates. All modifications should be made through the configuration file or by forking the repository.

---

<p align="center">
  <sub>Built with Python • Powered by Telegram • Made with passion</sub>
</p>
