// const redis = require('redis');

// const client = redis.createClient({
//     password: process.env.REDIS_PASSWORD,
//     socket: {
//         host: process.env.REDIS_HOST,
//         port: process.env.REDIS_PORT
//     }
// })

// client.on('error', (err) => { console.error("Redis Client Error: ", err) });

// module.exports = client;

const redis = require('redis');

const client = redis.createClient({
    url: process.env.REDIS_URL
});

client.on('error', (err) => {
    console.error("Redis Client Error:", err);
});