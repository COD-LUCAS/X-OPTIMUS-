# X-OPTIMUS TG BOT

<p align="center">
  <img src="assets/menu.jpg" alt="X-OPTIMUS TG BOT Menu" width="600">
</p>

A feature-rich Telegram automation bot developed in Python, offering extensive management capabilities and seamless integration.

---

## 🔔 IMPORTANT NOTICE

> **⚠️ CODEBASE ARCHITECTURE ALERT**
>
> This project uses an interconnected file structure where all components are synchronized during updates.
>
> **Protected configuration file:** `config_data/config.env`
>
> 💡 **Avoid modifying other files locally** - any custom changes will be overwritten when updating!

---

## 📦 PREREQUISITES

To get started with the bot, gather these essential credentials:

1. **API ID** and **API Hash** - Obtain from [my.telegram.org](https://my.telegram.org)
   
   <a href="https://youtube.com/shorts/9A04yQnUD5I?si=qLCV9B-Trwi6-1Vj">
     <img src="https://img.shields.io/badge/🎥_Tutorial-Get_API_Credentials-FF0000?style=for-the-badge&logo=youtube" alt="API Credentials Tutorial">
   </a>

2. **Session String** - Create one using the tool below

<p align="center">
  <a href="https://optimus-frontend-blush.vercel.app/">
    <img src="https://img.shields.io/badge/🔑_Generate-Session%20String-0088CC?style=for-the-badge&logo=telegram" alt="Session String Generator">
  </a>
</p>

---

## 🌐 DEPLOYMENT OPTIONS

### Option 1: Render Platform

<p align="center">
  <a href="https://render.com/deploy">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

Launch instantly on Render using the pre-configured `render.yaml` file.

**Environment Variables Required:**
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `SESSION_STRING` - Generated session string

Add these during deployment and you're ready to go!

> 🔄 **Auto-update feature included** - Always stays current automatically

---

### Option 2: Koyeb Platform

<p align="center">
  <a href="https://app.koyeb.com/deploy">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb">
  </a>
</p>

Deploy seamlessly to Koyeb with the included `koyeb.yaml` configuration.

**Environment Variables Required:**
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `SESSION_STRING` - Generated session string

Leverage Koyeb's worldwide infrastructure for optimal performance!

> 🔄 **Auto-update feature included** - Stays synchronized without manual intervention

---

### Option 3: Control Panel Deployment

**Deployment workflow:**

1. **File Upload** - Transfer all bot files to your hosting panel
2. **Archive Extraction** - Unzip if uploaded as compressed file
3. **Directory Setup** - Relocate files to container root (`../`)
4. **Startup Configuration** - Set `main.py` as the entry point
5. **Environment Setup** - Add these variables to `config_data/config.env`:
   - `API_ID`
   - `API_HASH`
   - `SESSION_STRING`
6. **Launch** - Activate the bot from your panel
7. **Version Management** - Execute `/update` command when new versions are available

> 🔧 **Manual updates needed** - Use `/update` command for version upgrades

---

## 🏆 DEVELOPER

**Created by:** Lucas

- 💬 Telegram: [@codlucas](https://t.me/codlucas)
- 🔗 GitHub: [COD-LUCAS](https://github.com/COD-LUCAS)

---

## 💬 GET HELP

Need assistance or have suggestions?
- Reach out on Telegram: [@codlucas](https://t.me/codlucas)
- Visit the [GitHub repository](https://github.com/COD-LUCAS) for docs and issue tracking

---
