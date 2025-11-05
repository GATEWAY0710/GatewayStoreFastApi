// --- Configuration & Endpoints ---
// CORRECTED ENDPOINT: Use the clean base URL for the stock entry API
const API_ENDPOINT = 'http://127.0.0.1:8000/stock_entry';

// --- DOM Elements ---
const form = document.getElementById('stock-update-form');
const responseContainer = document.getElementById('response-container');
const displayStockId = document.getElementById('display-stock-id');
const submitBtn = document.getElementById('submit-btn');

let stockId = '';

// --- Initialization Logic (Runs immediately when the script loads) ---

// 1. Extract stock_id from URL query
const urlParams = new URLSearchParams(window.location.search);
stockId = urlParams.get('stock_id');

if (stockId) {
    displayStockId.textContent = decodeURIComponent(stockId);
} else {
    displayStockId.innerHTML = '<span class="text-red-500">Error: Stock ID not found in URL query.</span>';
    submitBtn.disabled = true;
}

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

    if (submitBtn.disabled) {
        return;
    }

    setStatus('<p class="text-center text-orange-600">Sending price update request... Please wait.</p>', false);
    submitBtn.disabled = true;

    // Prepare the JSON data for the request body
    const data = {
        cost_price: parseFloat(document.getElementById('cost_price').value),
        selling_price: parseFloat(document.getElementById('selling_price').value)
    };

    // Construct the final API URL with the stock_id query parameter
    // CORRECT URL CONSTRUCTION: Base URL + ?stock_id=ID
    const apiUrl = `${API_ENDPOINT}?stock_id=${encodeURIComponent(stockId)}`;

    try {
        const response = await fetch(apiUrl, {
            // Using PATCH for partial updates (prices only)
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
                // NOTE: Add Authorization header (JWT) here if the endpoint is protected
            },
            body: JSON.stringify(data),
        });

        const responseData = await response.json().catch(() => response.text());
        const isSuccess = response.ok && responseData && responseData.status === true;

        if (!response.ok) {
            const errorDetails = typeof responseData === 'string' ? responseData : JSON.stringify(responseData, null, 2);
            setStatus(`<p class="text-red-600 font-bold">HTTP Error! Status: ${response.status}</p><p class="text-red-500">Details:</p>`, true, errorDetails);
            return;
        }

        // Success response handling
        const result = responseData;
        const statusColor = result.status ? 'text-green-700' : 'text-red-700';

        // Final success message display
        setStatus(`
            <p class="font-bold text-base ${statusColor}">Status: ${result.status ? '✅ Success' : '❌ Failure'}</p>
            <p class="mt-2">Message: ${result.message || 'Prices updated successfully'}</p>
            <hr class="my-3 border-gray-300">
            <p>New Cost Price: <span class="font-mono">${result.cost_price || 'N/A'}</span></p>
            <p>New Selling Price: <span class="font-mono">${result.selling_price || 'N/A'}</span></p>
            <hr class="my-3 border-gray-300">
            <p class="font-medium mt-3">Full JSON Response:</p>
        `, false, JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('Stock update error:', error);
        setStatus(`<p class="text-red-600 font-bold">Network/Client Error:</p>`, true, error.message);
    } finally {
        submitBtn.disabled = false;
    }
});