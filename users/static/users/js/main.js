// require('dotenv').config(); // import dotenv package 

var loginBtn = document.getElementById('discord-btn')
loginBtn.onclick = loginDiscord;

function loginDiscord() {
    var client_id = '833554127652519957'; // process.env.DISCORD_APP_CLIENT_ID; // process.env -> object that has environment variables
    window.location.href = `https://discord.com/api/oauth2/authorize?client_id=${client_id}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fusers%2Flogin&response_type=code&scope=identify%20email%20guilds&prompt=none`;
}
