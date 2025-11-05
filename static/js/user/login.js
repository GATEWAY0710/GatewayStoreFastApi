// --- Configuration & Endpoints ---
const LOGIN_API = 'http://127.0.0.1:8000/auth/token';
const ADMIN_PAGE = "/static/html/admin_dashboard.html";
const CUSTOMER_HOME_PAGE = "/static/html/sales/home.html";

// --- DOM Elements ---
const form = document.getElementById('login-form');
const responseContainer = document.getElementById('response-container');

// --- Helper Function ---
function displayMessage(message, type = 'info') {
    let bgColor, textColor;
    if (type === 'error') {
        bgColor = 'bg-red-100';
        textColor = 'text-red-700';
    } else if (type === 'success') {
        bgColor = 'bg-green-100';
        textColor = 'text-green-700';
    } else {
        bgColor = 'bg-gray-100';
        textColor = 'text-gray-600';
    }
    responseContainer.className = `mt-6 p-3 rounded-lg text-sm ${bgColor} ${textColor}`;
    responseContainer.innerHTML = message;
}

// --- Decode JWT Helper ---
function decodeJwt(token) {
    try {
        const payloadBase64 = token.split('.')[1];
        const decoded = JSON.parse(atob(payloadBase64));
        return decoded;
    } catch (e) {
        console.error("❌ JWT Decode Error:", e);
        return null;
    }
}

// --- Core Login and Redirect Logic ---
form.addEventListener('submit', async function (event) {
    event.preventDefault();
    displayMessage('Authenticating... Please wait.', 'info');

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const loginData = { email, password };

    try {
        // 1. Send Login Request
        const response = await fetch(LOGIN_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData),
        });

        const authResult = await response.json();

        if (!response.ok || authResult.status !== true) {
            const msg = authResult.message || `Login failed. Status: ${response.status}`;
            displayMessage(`Error: ${msg}`, 'error');
            return;
        }

        // 2. Store Tokens in Local Storage
        const accessToken = authResult.access_token;
        const refreshToken = authResult.refresh_token;

        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);

        // 3. Decode token to get role & user info
        const decoded = decodeJwt(accessToken);
        console.log("Decoded JWT Payload:", decoded);

        const role = decoded?.roles?.[0] || 'Customer'; // fallback
        const emailFromToken = decoded?.sub || email;
        const userId = decoded?.user_id || null;

        localStorage.setItem('user_role', role);
        localStorage.setItem('user_email', emailFromToken);
        localStorage.setItem('user_id', userId);

        // 4. Redirect based on role
        displayMessage(`Login successful as ${role}. Redirecting...`, 'success');

        if (role.toLowerCase() === 'admin') {
            window.location.href = ADMIN_PAGE;
        } else {
            window.location.href = CUSTOMER_HOME_PAGE;
        }

    } catch (error) {
        displayMessage(`Network Error: Could not connect to the server at ${LOGIN_API}.`, 'error');
        console.error('Login error:', error);
    }
});
