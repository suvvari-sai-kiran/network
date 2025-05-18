let statusChart;

function fetchStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById("switchTable");
            let upCount = 0;
            let downCount = 0;
            table.innerHTML = "";

            Object.entries(data).forEach(([ip, status]) => {
                let row = table.insertRow();
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);

                cell1.innerHTML = ip;
                if (status === "Online") {
                    cell2.innerHTML = "✅ <span class='up'>Online</span>";
                    upCount++;
                } else {
                    cell2.innerHTML = "❌ <span class='down'>Offline</span>";
                    downCount++;
                }
            });

            document.getElementById("total").textContent = upCount + downCount;
            document.getElementById("upCount").textContent = upCount;
            document.getElementById("downCount").textContent = downCount;

            updateChart(upCount, downCount);
        })
        .catch(error => console.error("Error fetching status:", error));
}

function updateChart(up, down) {
    const ctx = document.getElementById("statusChart").getContext("2d");

    if (statusChart) {
        statusChart.destroy();
    }

    statusChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: [`Online (${up})`, `Offline (${down})`],
            datasets: [{
                data: [up, down],
                backgroundColor: ["green", "red"],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top",
                }
            }
        }
    });
}

setInterval(fetchStatus, 5000);
fetchStatus();
