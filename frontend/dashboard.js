const queueContainer = document.getElementById("queue");
const serveButton = document.getElementById("serveButton");
const dashboardMessage = document.getElementById("dashboardMessage");


// Load queue
async function loadQueue() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/queue"
        );

        const data = await response.json();

        console.log("Queue:", data);

        displayQueue(data.queue);

    } catch (error) {

        console.error(error);

        queueContainer.innerHTML =
            "Could not load queue.";

    }
}


// Display queue
function displayQueue(queue) {

    if (queue.length === 0) {

        queueContainer.innerHTML =
            "<p>No requests waiting.</p>";

        return;
    }


    queueContainer.innerHTML = "";


    queue.forEach((request, index) => {

        const requestCard = document.createElement("div");

        requestCard.className = "request-item";

        requestCard.innerHTML = `
            <h3>#${index + 1} ${request.student_name}</h3>

            <p>
                <strong>Problem:</strong>
                ${request.problem}
            </p>

            <p>
                <strong>Request Type:</strong>
                ${request.request_type}
            </p>

            <p>
                <strong>Priority:</strong>
                ${request.priority}
            </p>
        `;

        queueContainer.appendChild(requestCard);

    });
}


// Serve next request
serveButton.addEventListener("click", async function() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/serve-next",
            {
                method: "POST"
            }
        );

        const data = await response.json();

        console.log("Served:", data);


        if (data.served_request) {

            dashboardMessage.innerHTML =
                `<strong>Now serving:</strong>
                 ${data.served_request.student_name}
                 — ${data.served_request.problem}`;

        } else {

            dashboardMessage.innerHTML =
                "The queue is empty.";

        }


        loadQueue();

    } catch (error) {

        console.error(error);

        dashboardMessage.innerHTML =
            "Could not connect to server.";

    }

});


// Load queue when page opens
loadQueue();