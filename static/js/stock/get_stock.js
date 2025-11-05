// --- Configuration & Endpoints ---
const API_ENDPOINT = 'http://127.0.0.1:8000/stock_entry/'; // Endpoint expects ID as query parameter

// --- DOM Elements ---
const form = document.getElementById('get-stock-form');
const responseContainer = document.getElementById('response-container');
const submitBtn = document.getElementById('submit-btn');

// --- Helper Function ---
function setStatus(message, isError = false, preContent = null) {
    const statusClass = isError ? 'bg-red-100 border-red-400 text-red-700' : 'bg-green-100 border-green-400 text-green-700';
    responseContainer.className = `p-4 rounded-lg text-sm border ${statusClass}`;

    if (preContent) {
        responseContainer.innerHTML = message + `<pre>${preContent}</pre>`;
    } else {
        responseContainer.innerHTML = message;
    }
}


// --- Form Submission Handler ---
form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const stockId = document.getElementById('stock_id').value;

    setStatus('<p class="text-center text-purple-600">Sending request... Please wait.</p>', false);
    submitBtn.disabled = true;

    // Construct the final API URL with the stock_id query parameter
    const apiUrl = `${API_ENDPOINT}?id=${encodeURIComponent(stockId)}`;

    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            // NOTE: Add 'Authorization' header here if the endpoint is protected by JWT
        });

        const responseData = await response.json().catch(() => response.text());
        const isSuccess = response.ok && responseData && responseData.status === true;

        if (!response.ok) {
            const errorDetails = typeof responseData === 'string' ? responseData : JSON.stringify(responseData, null, 2);
            setStatus(`<p class="text-red-600 font-bold">HTTP Error! Status: ${response.status}</p><p class="text-red-500">Details:</p>`, true, errorDetails);
            return;
        }

        const result = responseData;
        const statusColor = result.status ? 'text-green-700' : 'text-red-700';

        // Final success message display
        setStatus(`
            <p class="font-bold text-base ${statusColor}">Status: ${result.status ? '✅ Success' : '❌ Failure'}</p>
            <p class="mt-2">Message: ${result.message || 'Stock details retrieved successfully'}</p>
            <hr class="my-3 border-gray-300">
            <p>Total Quantity: <strong class="text-gray-900">${result.quantity}</strong></p>
            <p>Remaining Quantity: <strong class="text-gray-900">${result.remaining_quantity}</strong></p>
            <p>Cost Price: <span class="price-mono">${result.cost_price || 'N/A'}</span></p>
            <p>Selling Price: <span class="price-mono">${result.selling_price || 'N/A'}</span></p>
            <p>Added Date: ${result.added_date || 'N/A'}</p>
            <hr class="my-3 border-gray-300">
            <p class="font-medium mt-3">Full JSON Response:</p>
        `, false, JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('Get stock error:', error);
        setStatus(`<p class="text-red-600 font-bold">Network/Client Error:</p>`, true, error.message);
    } finally {
        submitBtn.disabled = false;
    }
});