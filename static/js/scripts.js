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
        span.textContent = "No one online";
        players_online.appendChild(span);
    }
}

function populate_mods() {
    const mods_container = document.getElementById("mods-container");
    mods_container.innerHTML = "";
}



window.onload = function(){
startPolling(5000)
}

