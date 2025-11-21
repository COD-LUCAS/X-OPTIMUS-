const { Module } = require('../main');
const config = require('../config');
const axios = require('axios');
const fs = require('fs');

const isPrivateBot = config.MODE !== 'public';

const activeDownloads = new Map();

Module({
    pattern: 'yta',
    fromMe: isPrivateBot,
    desc: 'Download YouTube audio',
    type: 'downloader',
    usage: 'yta <url or song name>'
}, async (message, match) => {

    // Works on all bots — takes text after command
    const input = message.text.split(" ").slice(1).join(" ");

    if (!input) {
        return await message.client.sendMessage(message.jid, { text: "❌ Give YouTube URL or song name." });
    }

    const downloadKey = `${message.jid}_${input}`;
    if (activeDownloads.has(downloadKey)) return;
    activeDownloads.set(downloadKey, true);

    await message.client.sendMessage(message.jid, {
        react: { text: '⌛', key: message.data.key }
    });

    let temp = null;

    try {
        const API = `https://api-aswin-sparky.koyeb.app/api/downloader/song?search=${encodeURIComponent(input)}`;
        const res = await axios.get(API);

        const { title, url } = res.data.data;

        temp = `yta_${Date.now()}.mp3`;

        const audio = await axios.get(url, { responseType: "stream" });
        const file = fs.createWriteStream(temp);
        audio.data.pipe(file);

        await new Promise((res) => file.on("finish", res));

        await message.client.sendMessage(message.jid, {
            audio: { stream: fs.createReadStream(temp) },
            mimetype: 'audio/mp4',
            fileName: `${title}.mp3`
        });

        await message.client.sendMessage(message.jid, {
            react: { text: '✅', key: message.data.key }
        });

    } catch (e) {
        await message.client.sendMessage(message.jid, {
            react: { text: '❌', key: message.data.key }
        });

    } finally {
        activeDownloads.delete(downloadKey);
        if (temp && fs.existsSync(temp)) fs.unlinkSync(temp);
    }
});
