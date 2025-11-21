const { Module } = require('../main');
const config = require('../config');
const axios = require('axios');
const fs = require('fs');

const isPrivateBot = config.MODE !== 'public';

// Track ongoing downloads
const activeDownloads = new Map();

Module({
    pattern: 'yta ?(.*)',
    fromMe: isPrivateBot,
    desc: 'Download YouTube audio by URL or search',
    type: 'downloader',
    usage: 'yta <youtube url | song name>'
}, async (message, match) => {

    const input = match[1];

    if (!input) {
        await message.client.sendMessage(message.jid, {
            react: { text: '❌', key: message.data.key }
        });
        return;
    }

    const downloadKey = `${message.jid}_${input}`;

    // Prevent duplicate downloads
    if (activeDownloads.has(downloadKey)) {
        console.log('Download already in progress, ignoring duplicate request');
        return;
    }

    activeDownloads.set(downloadKey, true);

    // React: loading
    await message.client.sendMessage(message.jid, {
        react: { text: '⌛', key: message.data.key }
    });

    let tempFilePath = null;

    try {
        // NEW API (Very stable)
        const API = `https://api-aswin-sparky.koyeb.app/api/downloader/song?search=${encodeURIComponent(input)}`;

        const response = await axios.get(API, {
            timeout: 30000,
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        const data = response.data;

        if (!data?.status || !data?.data) {
            throw new Error('Invalid API response');
        }

        const { title, url: downloadUrl } = data.data;

        if (!downloadUrl) throw new Error('No download URL found');

        tempFilePath = `./temp_yta_${message.jid.split('@')[0]}_${Date.now()}.mp3`;

        const audioResponse = await axios.get(downloadUrl, {
            responseType: 'stream',
            timeout: 60000,
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        const writeStream = fs.createWriteStream(tempFilePath);
        audioResponse.data.pipe(writeStream);

        await new Promise((res, rej) => {
            writeStream.on('finish', res);
            writeStream.on('error', rej);
        });

        if (!fs.existsSync(tempFilePath)) {
            throw new Error('Audio file not created');
        }

        const stats = fs.statSync(tempFilePath);
        if (stats.size < 1024) {
            throw new Error('File too small');
        }

        // Send audio
        await message.client.sendMessage(message.jid, {
            audio: { stream: fs.createReadStream(tempFilePath) },
            mimetype: 'audio/mp4',
            fileName: `${title.replace(/[<>:"/\\|?*]/g, '').substring(0, 100)}.mp3`
        });

        // Success react
        await message.client.sendMessage(message.jid, {
            react: { text: '✅', key: message.data.key }
        });

    } catch (err) {
        console.log("YTA ERROR:", err.message);

        await message.client.sendMessage(message.jid, {
            react: { text: '❌', key: message.data.key }
        });

    } finally {
        activeDownloads.delete(downloadKey);

        if (tempFilePath) {
            setTimeout(() => {
                try {
                    if (fs.existsSync(tempFilePath)) {
                        fs.unlinkSync(tempFilePath);
                    }
                } catch {}
            }, 2000);
        }

        // Clean leftover temp files
        setTimeout(() => {
            try {
                const files = fs.readdirSync('./').filter(f => f.startsWith('temp_yta_'));

                for (const file of files) {
                    try {
                        const fpath = './' + file;
                        const age = (Date.now() - fs.statSync(fpath).mtime.getTime()) / 60000;

                        if (age > 5) fs.unlinkSync(fpath);
                    } catch {}
                }
            } catch {}
        }, 2000);
    }

});
