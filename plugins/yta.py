const { Module } = require('../main');
const config = require('../config');
const axios = require('axios');
const fs = require('fs');

const isPrivateBot = config.MODE !== 'public';

const activeDownloads = new Map();

Module({
    pattern: 'yta(?:\\s+(.*))?',
    fromMe: isPrivateBot,
    desc: 'Download YouTube audio',
    type: 'downloader',
    usage: 'yta <url or song name>'
}, async (message, match) => {

    const input = match[1] || message.text.split(" ").slice(1).join(" ");

    if (!input) {
        await message.client.sendMessage(message.jid, {
            text: "❌ Please give a YouTube URL or song name."
        });
        return;
    }

    const downloadKey = `${message.jid}_${input}`;

    if (activeDownloads.has(downloadKey)) return;
    activeDownloads.set(downloadKey, true);

    await message.client.sendMessage(message.jid, {
        react: { text: '⌛', key: message.data.key }
    });

    let tempFilePath = null;

    try {
        const API = `https://api-aswin-sparky.koyeb.app/api/downloader/song?search=${encodeURIComponent(input)}`;

        const response = await axios.get(API, {
            timeout: 30000,
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        const { title, url: downloadUrl } = response.data.data;

        tempFilePath = `./yta_${Date.now()}.mp3`;

        const stream = await axios.get(downloadUrl, {
            responseType: 'stream'
        });

        const file = fs.createWriteStream(tempFilePath);
        stream.data.pipe(file);

        await new Promise(res => file.on('finish', res));

        await message.client.sendMessage(message.jid, {
            audio: { stream: fs.createReadStream(tempFilePath) },
            mimetype: 'audio/mp4',
            fileName: `${title}.mp3`
        });

        await message.client.sendMessage(message.jid, {
            react: { text: '✅', key: message.data.key }
        });

    } catch (err) {
        console.log(err);

        await message.client.sendMessage(message.jid, {
            react: { text: '❌', key: message.data.key }
        });

    } finally {
        activeDownloads.delete(downloadKey);
        if (tempFilePath && fs.existsSync(tempFilePath)) fs.unlinkSync(tempFilePath);
    }

});
