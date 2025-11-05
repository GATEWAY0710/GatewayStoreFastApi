// --- Configuration ---
const LIST_API_ENDPOINT = 'http://127.0.0.1:8000/stock_entry';
const GET_STOCK_PAGE = '/static/html/stock/get_stock.html';
const UPDATE_STOCK_PAGE = '/static/html/stock/update_stock.html';

// --- DOM Elements ---
const loadBtn = document.getElementById('load-data-btn');
const statusMessage = document.getElementById('status-message');
const table = document.getElementById('stock-table');
const tableBody = document.getElementById('stock-list-body');

// --- Navigation Helper ---
function navigateTo(url) {
    window.location.href = url;
}

// --- Render Stock Row ---
function renderStockRow(stock, index) {
    const stockId = stock.id || `STK_${index + 1}`;
    const row = tableBody.insertRow();
    row.className = 'hover:bg-gray-50 transition duration-150';

    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${stockId}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700">${stock.product_name || 'N/A'}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700">${stock.quantity || 0}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700">${stock.remaining_quantity || 0}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700 price-mono">${stock.cost_price || 'N/A'}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700 price-mono">${stock.selling_price || 'N/A'}</div>`;
    row.insertCell().innerHTML = `<div class="px-4 py-4 whitespace-nowrap text-sm text-gray-700">${stock.added_date || 'N/A'}</div>`;

    const actionsCell = row.insertCell();
    actionsCell.className = "px-6 py-4 whitespace-nowrap text-center text-sm font-medium space-x-2";
    actionsCell.innerHTML = `
        <button onclick="navigateTo('${GET_STOCK_PAGE}?stock_id=${encodeURIComponent(stockId)}')"
                class="text-purple-600 hover:text-purple-900 transition duration-150">
            Details
        </button>
        <button onclick="navigateTo('${UPDATE_STOCK_PAGE}?stock_id=${encodeURIComponent(stockId)}')"
                class="text-orange-600 hover:text-orange-900 transition duration-150">
            Update
        </button>
    `;
}

// --- Fetch Stocks ---
async function fetchStocks() {
    statusMessage.innerHTML = '<span class="text-teal-600 font-semibold">Loading...</span>';
    table.classList.add('hidden');
    tableBody.innerHTML = '';

    try {
        const response = await fetch(LIST_API_ENDPOINT, { method: 'GET' });
        const data = await response.json().catch(() => response.text());

        if (!response.ok || data.status !== true) {
            statusMessage.innerHTML = `<span class="text-red-600 font-bold">Error:</span> ${data.message || 'Failed to load stocks'}`;
            return;
        }

        if (!data.stocks || data.stocks.length === 0) {
            statusMessage.innerHTML = '<span class="text-yellow-600">No stock items found.</span>';
            return;
        }

        // Sort stocks by added_date descending (newest first)
        data.stocks.sort((a, b) => new Date(b.added_date) - new Date(a.added_date));

        data.stocks.forEach(renderStockRow);

        statusMessage.innerHTML = `<span class="text-green-600 font-semibold">Loaded ${data.stocks.length} stock item(s).</span>`;
        table.classList.remove('hidden');

    } catch (err) {
        console.error(err);
        statusMessage.innerHTML = `<span class="text-red-600 font-bold">Network Error:</span> Cannot reach API.`;
    }
}

// --- Initialization ---
loadBtn.addEventListener('click', fetchStocks);
