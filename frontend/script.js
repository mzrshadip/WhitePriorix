const form = document.getElementById("requestForm");
const message = document.getElementById("message");

console.log("WhitePriorix JavaScript loaded");


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    console.log("Form submitted");


    const studentName =
        document.getElementById("studentName").value;

    const problem =
        document.getElementById("problem").value;

    const requestType =
        document.getElementById("requestType").value;


    message.innerHTML = "Submitting request...";


    try {

        const url =
            "http://127.0.0.1:8000/requests?" +
            "student_name=" + encodeURIComponent(studentName) +
            "&problem=" + encodeURIComponent(problem) +
            "&request_type=" + encodeURIComponent(requestType);


        const response = await fetch(url, {
            method: "POST"
        });


        const data = await response.json();


        console.log("Backend response:", data);


        if (!response.ok) {

            throw new Error(
                data.detail || "Request failed"
            );

        }


        message.innerHTML =
            "<strong>Request submitted successfully!</strong><br>" +
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