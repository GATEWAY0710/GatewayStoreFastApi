const API_ENDPOINT = "http://127.0.0.1:8000/users{admin}"; // adjust if your backend uses a different route
const form = document.getElementById("create-admin-form");
const responseContainer = document.getElementById("response-container");
const submitBtn = document.getElementById("submit-btn");

// Display messages
function setStatus(message, isError = false) {
    const statusClass = isError
        ? "bg-red-100 border-red-400 text-red-700"
        : "bg-green-100 border-green-400 text-green-700";
    responseContainer.className = `p-4 rounded-lg text-sm border ${statusClass}`;
    responseContainer.innerHTML = message;
}

// Form submit
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirm_password = document.getElementById("confirm_password").value.trim();

    if (password !== confirm_password) {
        setStatus("<strong>Error:</strong> Passwords do not match!", true);
        return;
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
        setStatus("<strong>Error:</strong> You must be logged in as an admin to create a new admin.", true);
        return;
    }

    const payload = { email, username, password, confirm_password };

    setStatus("Sending request... Please wait.", false);
    submitBtn.disabled = true;

    try {
        const res = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // <-- pass JWT token
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok) {
            setStatus(`
                <strong>✅ Admin Created!</strong><br>
                ID: ${data.id || "N/A"}<br>
                Email: ${data.email || "N/A"}<br>
                Username: ${data.username || "N/A"}<br>
                Role: ${data.role || "N/A"}<br>
                <hr>
                <pre>${JSON.stringify(data, null, 2)}</pre>
            `, false);
        } else {
            const msg = data.message || JSON.stringify(data);
            setStatus(`<strong>Error:</strong> ${msg}`, true);
        }
    } catch (err) {
        console.error(err);
        setStatus("<strong>Network error:</strong> Could not connect to server.", true);
    } finally {
        submitBtn.disabled = false;
    }
});
