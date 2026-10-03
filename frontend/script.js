const form = document.getElementById("requestForm");
const message = document.getElementById("message");

const API_URL = "https://whitepriorix.onrender.com";

console.log("WhitePriorix JavaScript loaded");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    console.log("Form submitted");

    const studentName = document.getElementById("studentName").value;
    const studentId = document.getElementById("studentId").value;
    const problem = document.getElementById("problem").value;
    const requestType = document.getElementById("requestType").value;

    message.innerHTML = "Submitting request...";

    try {
        const url =
            API_URL + "/requests?" +
            "student_name=" + encodeURIComponent(studentName) +
            "&student_id=" + encodeURIComponent(studentId) +
            "&problem=" + encodeURIComponent(problem) +
            "&request_type=" + encodeURIComponent(requestType);

        const response = await fetch(url, {
            method: "POST"
        });

        const data = await response.json();

        console.log("Backend response:", data);

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        message.innerHTML =
            "<strong>Request submitted successfully!</strong><br>" +
            "Student ID: " +
            data.request.student_id +
            "<br>" +
            "Your priority is " +
            data.request.priority +
            ".";

        form.reset();

    } catch (error) {
        console.error("ERROR:", error);

        message.innerHTML =
            "❌ Could not connect to WhitePriorix.";
    }
});