// --- Configuration & Endpoints ---
const SIGNUP_API = 'http://127.0.0.1:8000/users';
// Using the absolute path for reliable redirection:
const LOGIN_PAGE = '/static/html/user/login.html';

// --- DOM Elements ---
const form = document.getElementById('signup-form');
const responseContainer = document.getElementById('response-container');
const submitBtn = document.getElementById('submit-btn');

// --- Helper Function ---
function displayMessage(message, type = 'info') {
    let bgColor, textColor;
    if (type === 'error') {
        bgColor = 'bg-red-100';
        textColor = 'text-red-700';
    } else if (type === 'success') {
        bgColor = 'bg-green-100';
        textColor = 'text-green-700';
    } else { // info/loading
        bgColor = 'bg-gray-100';
        textColor = 'text-gray-600';
    }
    responseContainer.className = `mt-6 p-3 rounded-lg text-sm ${bgColor} ${textColor}`;
    responseContainer.innerHTML = message;
}

// --- Core Sign Up Logic ---
form.addEventListener('submit', async function(event) {
    event.preventDefault();
    displayMessage('Creating account... Please wait.', 'info');
    submitBtn.disabled = true;

    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    if (password !== confirm_password) {
        displayMessage('Error: Passwords do not match!', 'error');
        submitBtn.disabled = false;
        return;
    }

    const signupData = { email, username, password, confirm_password };

    try {
        // 1. Send Sign Up Request
        const response = await fetch(SIGNUP_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(signupData),
        });

        const result = await response.json();

        if (!response.ok || result.status !== true) {
            // Handle HTTP errors or API-specific failure messages
            const msg = result.message || JSON.stringify(result) || `Sign up failed. Status: ${response.status}`;
            displayMessage(`Error: ${msg}`, 'error');
            return;
        }

        displayMessage(`Success! Account created for user ${result.username}. Redirecting to Login...`, 'success');

        // Wait a moment before redirecting
        setTimeout(() => {
            window.location.href = LOGIN_PAGE;
        }, 2000);

    } catch (error) {
        displayMessage(`Network Error: Could not connect to API. Check console.`, 'error');
        console.error('Sign up error:', error);
    } finally {
        // Only re-enable the button if an error occurred, otherwise the timeout handles the redirect
        if (responseContainer.className.includes('bg-red-100')) {
             submitBtn.disabled = false;
        }
    }
});