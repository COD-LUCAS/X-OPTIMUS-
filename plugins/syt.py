const { Module } = require('../main');
const config = require('../config');
const axios = require('axios');
const fs = require('fs');

const isPrivateBot = config.MODE !== 'public';

// Global map to track ongoing downloads
const activeDownloads = new Map();

Module({
    pattern: 'syt ?(.*)',
    fromMe: isPrivateBot,
    desc: 'Download audio from YouTube URL',
    type: 'downloader',
    usage: 'track [YouTube URL]'
}, async (message, match) => {
    const input = match[1];

    if (!input) {
        await message.client.sendMessage(message.jid, {
            react: { text: '❌', key: message.data.key }
        });
        return;
    }

    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)/;
    if (!youtubeRegex.test(input)) {
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

    await message.client.sendMessage(message.jid, {
        react: { text: '⌛', key: message.data.key }
    });

    let tempFilePath = null;

    try {
        const API_BASE_URL = 'https://api-aswin-sparky.koyeb.app/api/downloader/song';
        const apiUrl = `${API_BASE_URL}?search=${encodeURIComponent(input)}`;

        const response = await axios.get(apiUrl, {
            timeout: 30000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        });

        const data = response.data;

        if (!data || !data.status || !data.data) {
            throw new Error('Invalid API response');
        }

        const trackInfo = data.data;
        const { title, url: downloadUrl } = trackInfo;

        if (!downloadUrl || !title) {
            throw new Error('Missing download URL or title');
        }

        tempFilePath = `./temp_audio_${message.jid.split('@')[0]}_${Date.now()}.mp3`;

        const audioResponse = await axios.get(downloadUrl, {
            responseType: 'stream',
            timeout: 60000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        });

        const writeStream = fs.createWriteStream(tempFilePath);

        audioResponse.data.pipe(writeStream);

        await new Promise((resolve, reject) => {
            writeStream.on('finish', resolve);
            writeStream.on('error', reject);
        });

        if (!fs.existsSync(tempFilePath)) {
            throw new Error('File not created');
        }

        const stats = fs.statSync(tempFilePath);
        if (stats.size < 1024) {
            throw new Error('File too small');
        }

        await message.client.sendMessage(message.jid, {
            audio: { stream: fs.createReadStream(tempFilePath) },
            mimetype: 'audio/mp4',
            fileName: `${title.replace(/[<>:"/\\|?*]/g, '').substring(0, 100)}.mp3`
        });

        await message.client.sendMessage(message.jid, {
            react: { text: '✅', key: message.data.key }
        });

    } catch (error) {
        console.error('Track download error:', error.message);

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
                        console.log('Cleaned up temp file:', tempFilePath);
                    }
                } catch (cleanupError) {
                    console.error('Cleanup error:', cleanupError.message);
                }
            }, 3000);
        }

        setTimeout(() => {
            try {
                const files = fs.readdirSync('./');
                const tempFiles = files.filter(file => file.startsWith('temp_audio_'));

                tempFiles.forEach(file => {
                    try {
                        const filePath = `./${file}`;
                        const stats = fs.statSync(filePath);
                        const ageMinutes = (Date.now() - stats.mtime.getTime()) / (1000 * 60);

                        if (ageMinutes > 5) {
                            fs.unlinkSync(filePath);
                            console.log('Cleaned up old file:', file);
                        }
                    } catch (err) {
                        console.error('File cleanup error:', err.message);
                    }
                });
            } catch (dirError) {
                console.error('Directory cleanup error:', dirError.message);
            }
        }, 1000);
    }
});
