const socket = io();

socket.on("connect", () => {
    console.log("Connected! to Socket...");
})

socket.on("log_entry", (data) => {
    const container = document.getElementById("log-output");
    if (data.new === true) {
        container.innerHTML = ""
    }
    container.innerHTML += data.log
    container.scrollTop = container.scrollHeight;

})

socket.on("mod_list", (data) => {
    console.log(data.mod_list);
    const mods_container = document.getElementById("mod-list");
    mods_container.innerHTML = "";
    for (const mod of data.mod_list) {
        const div = document.createElement("div");
        div.className = "mod"
        console.log(mod)
        div.innerHTML = mod.name + "<span class='mod-underscore'>_</span>" + "<span class='mod-version'>" + mod.version + "</span>";
        mods_container.appendChild(div);
    }
})

socket.emit("mod_list")
socket.emit("log_entry")


function shutdownServer() {
    fetch("/shutdown-server", {method: "POST"})
}

function startServer() {
    fetch("/start-server", {method: "POST"})
}

function updateServer() {
    fetch("/start-update", {method: "POST"})
}

function setServerStatus(isOnline) {
    const status_indicator = document.getElementById("status-indicator");
    const status_text = document.getElementById("status-text");
    status_indicator.classList.remove("status-online", "status-offline", "status-update");
    if (isOnline === true) {
        status_indicator.classList.add("status-online");
        status_text.textContent = "Online";
    } else if (isOnline === "update") {
        status_indicator.classList.add("status-update");
        status_text.textContent = "Update in progress";
    } else {
        status_indicator.classList.add("status-offline");
        status_text.textContent = "Offline";
    }
}

async function fetchServerInfo() {
    try {
        const response = await fetch("api/server-status", {method: "GET"});
        if (!response.ok) {
            throw new Error("Server not responding");
        }
        const data = await response.json();
        setServerStatus(data.server_online);
        populate_players(data.player);
    } catch(error) {
        console.error("Fetch error:", error);
        setServerStatus(false);
    }
}

function startPolling(interval) {
    fetchServerInfo().then(() => {
        setInterval(fetchServerInfo, interval);
    })
}

function populate_players(players) {
    const players_online = document.getElementById("players-online");
    players_online.innerHTML = "";
    if (players.length > 0) {

        for (const player of players) {
            const span = document.createElement("span");
            span.textContent = player;
            players_online.appendChild(span);
        }
    }else{
        const span = document.createElement("span");
        span.textContent = "Nobody online";
        players_online.appendChild(span);
    }
}

window.onload = function(){
    startPolling(5000)
}

