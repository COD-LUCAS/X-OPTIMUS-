# X-OPTIMUS TG BOT

<p align="center">
  <img src="assets/menu.jpg" alt="X-OPTIMUS TG BOT Menu" width="600">
</p>

A powerful Telegram bot built with Python that provides comprehensive automation and management features.

---

## ⚠️ CRITICAL UPDATE WARNING

> **🚨 IMPORTANT: HIGHLY INTERCONNECTED CODEBASE**
>
> All files in this project are interconnected and will be **automatically overwritten** during updates.
>
> **The ONLY file protected from changes is:** `config_data/config.env`
>
> ⚡ **DO NOT make local modifications to any other scripts or plugins** - your changes will be lost during the next update!

---

## 📋 REQUIREMENTS

Before deploying the bot, you'll need to obtain the following credentials:

1. **API ID** and **API Hash** - Get these from [my.telegram.org](https://my.telegram.org)
   
   <a href="https://youtube.com/shorts/9A04yQnUD5I?si=qLCV9B-Trwi6-1Vj">
     <img src="https://img.shields.io/badge/📺_Watch-How_to_Get_API_ID_&_HASH-red?style=for-the-badge&logo=youtube" alt="How to Get API ID and HASH">
   </a>

2. **Session String** - Generate using the button below

<p align="center">
  <a href="https://optimus-frontend-blush.vercel.app/">
    <img src="https://img.shields.io/badge/Generate-Session%20String-blue?style=for-the-badge&logo=telegram" alt="Generate Session String">
  </a>
</p>

---

## 🚀 DEPLOYMENT METHODS

### Method 1: Deploy on Render

<p align="center">
  <a href="https://render.com/deploy">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

Click the button above to deploy directly to Render. The `render.yaml` configuration file is pre-configured.

**Required Environment Variables:**
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `SESSION_STRING` - Your generated session string

Simply fill in these variables during deployment and your bot will be live!

> ✅ **Automatic Updates Enabled** - No manual update command needed

---

### Method 2: Deploy on Koyeb

<p align="center">
  <a href="https://app.koyeb.com/deploy">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb">
  </a>
</p>

Click the button above to deploy directly to Koyeb. The `koyeb.yaml` configuration file is pre-configured.

**Required Environment Variables:**
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `SESSION_STRING` - Your generated session string

Your bot will be deployed on Koyeb's global infrastructure!

> ✅ **Automatic Updates Enabled** - No manual update command needed

---

### Method 3: Deploy on Panel

**Step-by-step deployment process:**

1. **Upload Files** - Upload all bot files to your panel
2. **Extract Archive** - If uploaded as a zip file, extract it
3. **Move Files** - Move all files to the container root directory (`../`)
4. **Set Startup Command** - Configure `main.py` as the startup file
5. **Configure Environment** - Add the following variables to `config_data/config.env`:
   - `API_ID`
   - `API_HASH`
   - `SESSION_STRING`
6. **Start the Bot** - Click start to launch your bot
7. **Updates** - Use the `/update` command to manually update the bot when needed

> ⚡ **Manual Updates Required** - Run `/update` command to get the latest version

---

## 👨‍💻 CREDITS

**Developer:** Lucas

- 📱 Telegram: [@codlucas](https://t.me/codlucas)
- 💻 GitHub: [COD-LUCAS](https://github.com/COD-LUCAS)

---

## 📞 SUPPORT

For support, feature requests, or updates:
- Contact via Telegram: [@codlucas](https://t.me/codlucas)
- Check the [GitHub repository](https://github.com/COD-LUCAS) for documentation and issues
- 
