# X-OPTIMUS TG BOT

<p align="center">
  <img src="assets/menu.jpg" alt="X-OPTIMUS TG BOT Menu" width="600">
</p>

A powerful Telegram bot built with Python.

​⚠️ IMPORTANT UPDATE SAFETY WARNING
​<div align="center">
<div style="
background-color: #ffcccc;
border: 2px solid #cc0000;
color: #cc0000;
padding: 15px;
border-radius: 8px;
font-weight: 700;
width: 90%;
margin: 20px auto;
text-align: center;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
">
🚨 WARNING: HIGHLY INTERCONNECTED CODEBASE 🚨



All files are interconnected and will be overwritten during the update.


The ONLY file protected from changes is <code style="background-color: #ff9999; padding: 3px 6px; border-radius: 3px;">config_data/config.env</code>.



DO NOT make local changes to any other script or plugin outside of this file!
</div>
</div>

---

## **REQUIREMENTS**

Before deploying the bot, you need to obtain the following credentials:

- **API ID** and **API Hash**: Get them from [https://my.telegram.org](https://my.telegram.org)
- **Session String**: Generate it by clicking the button below

<p align="center">
  <a href="https://optimus-frontend-blush.vercel.app/">
    <img src="https://img.shields.io/badge/Generate-Session%20String-blue?style=for-the-badge&logo=telegram" alt="Generate Session String">
  </a>
</p>

---

## **DEPLOYMENT METHODS**

### **1. Deploy on Render**

<p align="center">
  <a href="https://render.com/deploy">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

Click the button above to deploy directly to Render. The `render.yaml` file is already configured.

**Required Environment Variables:**
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `SESSION_STRING` - Your session string from the link above

Simply fill in these variables during deployment and your bot will be up and running!
<div align="center">
<div style="background-color: black; color: white; padding: 10px; border-radius: 5px; font-weight: bold; width: 80%; margin: 10px auto;">
IT WILL UPADTE AUTOMATICALLY NO NEED TO UPDATE COMMAND
</div>
</div>

---

### **2. Deploy on Koyeb**

<p align="center">
  <a href="https://app.koyeb.com/deploy">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb">
  </a>
</p>

Click the button above to deploy directly to Koyeb. The `koyeb.yaml` file is already configured.

**Required Environment Variables:**
- `API_ID` - Your Telegram API ID
- `API_HASH` - Your Telegram API Hash
- `SESSION_STRING` - Your session string from the link above

Your bot will be deployed and running on Koyeb's infrastructure!
<div align="center">
<div style="background-color: black; color: white; padding: 10px; border-radius: 5px; font-weight: bold; width: 80%; margin: 10px auto;">
IT WILL UPADTE AUTOMATICALLY NO NEED TO UPDATE COMMAND
</div>
</div>

---

### **3. Deploy on Panel**

1. **Upload Files**: Upload all bot files to your panel
2. **unzip**:If it is zip uzip it
3. **MOVE FILES**:Move files to container (../)
4. **Set Startup Command**: Set `main.py` as the startup file
5. **Configure Environment Variables**: Add the following env variable in container_data/config.env:
   - `API_ID`
   - `API_HASH`
   - `SESSION_STRING`
6. **Start the Bot**: Click start and your bot will begin running
7. <div align="center">
<div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 5px; width: 60%; margin: 10px auto; font-family: monospace;">
/update COMMAND MUST BE USED FOR UP TO DATE USE
</div>
</div>

---

## **CREDITS**

**Made by Lucas**

- Telegram: [@codlucas](https://t.me/codlucas)
- GitHub: [COD-LUCAS](https://github.com/COD-LUCAS)

---

*For support and updates, contact via Telegram or check the GitHub repository.*
