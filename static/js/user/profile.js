const BASE_URL = "http://127.0.0.1:8000/profile";
const responseContainer = document.getElementById("response-container");
const form = document.getElementById("profile-form");

// Display messages
function displayMessage(message, type = "info") {
    let color =
        type === "error"
            ? "text-red-600"
            : type === "success"
            ? "text-green-600"
            : "text-gray-600";
    responseContainer.className = `${color} mt-2`;
    responseContainer.textContent = message;
}

// Load profile data
async function loadProfile() {
    const userId = localStorage.getItem("user_id");
    const token = localStorage.getItem("access_token");

    if (!userId || !token) {
        displayMessage("You are not logged in. Redirecting...");
        return (window.location.href = "/static/html/user/login.html");
    }

    try {
        const res = await fetch(`${BASE_URL}/${userId}`, {
            headers: { Authorization: `Bearer ${token}` },
        });

        const data = await res.json();

        if (res.ok && data.status) {
            // ✅ Fill form fields directly
            document.getElementById("first_name").value = data.first_name || "";
            document.getElementById("middle_name").value = data.middle_name || "";
            document.getElementById("last_name").value = data.last_name || "";
            document.getElementById("phone_number").value = data.phone_number || "";

            form.dataset.mode = "update"; // Mark as update mode
            displayMessage("Profile loaded successfully.", "success");
        } else {
            form.dataset.mode = "create";
            displayMessage("No profile found. Please create one.", "info");
        }
    } catch (error) {
        console.error(error);
        displayMessage("Network error while fetching profile.", "error");
    }
}

// Handle create/update profile
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userId = localStorage.getItem("user_id");
    const token = localStorage.getItem("access_token");

    if (!userId || !token) {
        displayMessage("Not authorized.", "error");
        return;
    }

    const profileData = {
        first_name: document.getElementById("first_name").value.trim(),
        middle_name: document.getElementById("middle_name").value.trim(),
        last_name: document.getElementById("last_name").value.trim(),
        phone_number: document.getElementById("phone_number").value.trim(),
    };

    const mode = form.dataset.mode || "create";
    const url = mode === "update" ? `${BASE_URL}/update` : BASE_URL;
    const method = mode === "update" ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(profileData),
        });

        const result = await response.json();

        if (response.ok && result.status) {
            displayMessage(
                mode === "update"
                    ? "Profile updated successfully!"
                    : "Profile created successfully!",
                "success"
            );
            form.dataset.mode = "update";
        } else {
            displayMessage(result.message || "Error saving profile.", "error");
        }
    } catch (err) {
        console.error(err);
        displayMessage("Network error.", "error");
    }
});

// Initialize
document.addEventListener("DOMContentLoaded", loadProfile);
