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

async function fetchServerStatus() {
    try {
        const response = await fetch("api/server-status", {method: "GET"});
        if (!response.ok) {
            throw new Error("Server not responding");
        }
        const data = await response.json();
        setServerStatus(data.server_online);
    } catch(error) {
        console.error("Fetch error:", error);
        setServerStatus(false);
    }

}

function startPolling(interval) {
    fetchServerStatus().then(() => {
        setInterval(fetchServerStatus, interval);
    })
}


window.onload = function(){
    startPolling(5000)
}