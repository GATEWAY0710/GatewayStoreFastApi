// --- Configuration ---
const API_ENDPOINT = 'http://127.0.0.1:8000/users';
const PROFILE_PAGE = '/static/html/user/profile.html';

// --- DOM Elements ---
const loadBtn = document.getElementById('load-data-btn');
const statusMessage = document.getElementById('status-message');
const table = document.getElementById('user-table');
const tableBody = document.getElementById('user-list-body');

// --- Fetch Users ---
async function fetchUsers() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        statusMessage.innerHTML = `<span class="text-red-600">You must be logged in to view users.</span>`;
        return;
    }

    statusMessage.innerHTML = `<span class="text-blue-600">Loading users...</span>`;
    table.classList.add('hidden');
    tableBody.innerHTML = '';

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();

        if (!response.ok || !data.users) {
            statusMessage.innerHTML = `<span class="text-red-600">Error fetching users. ${data.message || ''}</span>`;
            return;
        }

        if (data.users.length === 0) {
            statusMessage.innerHTML = `<span class="text-yellow-600">No users found.</span>`;
            return;
        }

        data.users.forEach(user => {
            const row = tableBody.insertRow();
            row.className = 'hover:bg-gray-50 transition duration-150';

            row.insertCell().innerHTML = `<div class="px-6 py-4 text-xs text-gray-500">${user.id}</div>`;
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm font-medium text-gray-900">${user.username}</div>`;
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm text-gray-500">${user.email}</div>`;
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm font-bold text-red-700">${user.role}</div>`;

            // Get Profile Button
            const actionsCell = row.insertCell();
            actionsCell.className = "px-6 py-4 text-center";
            actionsCell.innerHTML = `
                <a href="${PROFILE_PAGE}?user_id=${encodeURIComponent(user.id)}"
                   class="text-blue-600 hover:text-blue-900 font-medium">
                    Get Profile
                </a>
            `;
        });

        table.classList.remove('hidden');
        statusMessage.innerHTML = `<span class="text-green-600">Loaded ${data.users.length} users successfully.</span>`;

    } catch (error) {
        console.error(error);
        statusMessage.innerHTML = `<span class="text-red-600">Network error while fetching users.</span>`;
    }
}

loadBtn.addEventListener('click', fetchUsers);
