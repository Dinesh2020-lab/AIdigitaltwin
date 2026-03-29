// LOGIN
function login() {
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    if (user === "admin" && pass === "dialysis123") {
        window.location.href = "dashboard.html";
    } else {
        alert("Invalid Credentials");
    }
}


// TIMER
let seconds = 0;
setInterval(() => {
    seconds++;
    let hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
    let mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    let secs = String(seconds % 60).padStart(2, '0');

    let timer = document.getElementById("timer");
    if (timer) timer.innerText = `${hrs}:${mins}:${secs}`;
}, 1000);


// LIVE DATA SIMULATION
function randomUpdate() {
    document.getElementById("hr").innerText = 60 + Math.floor(Math.random() * 20);
    document.getElementById("spo2").innerText = 95 + Math.floor(Math.random() * 5);
    document.getElementById("temp").innerText = (36 + Math.random()).toFixed(1);
}

setInterval(randomUpdate, 2000);


// ECG CHART
const ctx = document.getElementById('ecgChart');

if (ctx) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 20}, (_, i) => i),
            datasets: [{
                label: 'ECG',
                data: Array.from({length: 20}, () => Math.random() * 2),
                borderColor: '#00f5d4',
                fill: false,
            }]
        },
        options: {
            animation: false,
            scales: {
                x: { display: false },
                y: { display: false }
            }
        }
    });
}
document.getElementById("bfr").oninput = e =>
    document.getElementById("bfrVal").innerText = e.target.value;

document.getElementById("dfr").oninput = e =>
    document.getElementById("dfrVal").innerText = e.target.value;

document.getElementById("ufr").oninput = e =>
    document.getElementById("ufrVal").innerText = e.target.value;

document.getElementById("tmp").oninput = e =>
    document.getElementById("tmpVal").innerText = e.target.value;

document.getElementById("tempCtrl").oninput = e =>
    document.getElementById("tempVal").innerText = e.target.value;

document.getElementById("hep").oninput = e =>
    document.getElementById("hepVal").innerText = e.target.value;
// ================= BACKEND CONNECTION =================
async function analyzeData() {
    const pressure = document.getElementById("pressure").value;
    const flow = document.getElementById("flow").value;
    const time = document.getElementById("time").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pressure: parseInt(pressure),
                flow: parseInt(flow),
                time: parseInt(time)
            })
        });

        const data = await response.json();

        // Update UI
        document.getElementById("aiRisk").innerText = "Risk: " + data.risk;
        document.getElementById("aiSuggestion").innerText = "Suggestion: " + data.suggestion;

    } catch (error) {
        console.error("Error:", error);
        alert("Backend not connected");
    }
}