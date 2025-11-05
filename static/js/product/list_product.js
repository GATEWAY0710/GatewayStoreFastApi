// --- Configuration & Endpoints ---
const LIST_API_ENDPOINT = 'http://127.0.0.1:8000/product'; // product list endpoint

// Pages
const VIEW_PRODUCT_PAGE = '../product/view_product.html';
const UPDATE_PRODUCT_PAGE = '../product/update_product.html';

// --- DOM Elements ---
const loadBtn = document.getElementById('load-data-btn');
const statusMessage = document.getElementById('status-message');
const table = document.getElementById('product-table');
const tableBody = document.getElementById('product-list-body');

// --- Main Fetch Function ---
async function fetchProducts() {
    statusMessage.innerHTML = '<span class="text-indigo-600 font-semibold">Loading products...</span>';
    table.classList.add('hidden');
    tableBody.innerHTML = '';

    try {
        const response = await fetch(LIST_API_ENDPOINT, { method: 'GET' });
        const data = await response.json();

        if (!response.ok || data.status !== true) {
            statusMessage.innerHTML = `<span class="text-red-600 font-bold">Error:</span> Failed to fetch products.`;
            console.error('API Error:', data);
            return;
        }

        if (!data.products || data.products.length === 0) {
            statusMessage.innerHTML = '<span class="text-yellow-600">No products found.</span>';
            return;
        }

        // Render each product
        data.products.forEach(product => {
            const row = tableBody.insertRow();
            row.className = 'hover:bg-gray-50 transition duration-150';

            // 1. Product Name
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm font-medium text-gray-900">${product.name}</div>`;

            // 2. Remaining Qty (take from first stock item if exists)
            let remainingQty = 0;
            if (product.stock_items && product.stock_items.length > 0) {
                remainingQty = product.stock_items.reduce((sum, stock) => sum + (stock.remaining_quantity || 0), 0);
            }
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm text-gray-700">${remainingQty}</div>`;

            // 3. Selling Price (use first stock item or average if needed)
            let sellingPrice = 'N/A';
            if (product.stock_items && product.stock_items.length > 0) {
                sellingPrice = product.stock_items[0].selling_price || 'N/A';
            }
            row.insertCell().innerHTML = `<div class="px-6 py-4 text-sm text-gray-700 price-mono">${sellingPrice}</div>`;


            // 4. Product Actions
            const actionsCell = row.insertCell();
            actionsCell.className = "px-6 py-4 whitespace-nowrap text-center text-sm font-medium space-x-2";
            actionsCell.innerHTML = `
                <a href="${VIEW_PRODUCT_PAGE}?name=${encodeURIComponent(product.name)}"
                   class="text-green-600 hover:text-green-900 transition duration-150">
                    View Details
                </a>
                <a href="${UPDATE_PRODUCT_PAGE}?name=${encodeURIComponent(product.name)}"
                   class="text-orange-600 hover:text-orange-900 transition duration-150">
                    Update
                </a>
            `;
        });

        statusMessage.innerHTML = `<span class="text-green-600 font-semibold">Loaded ${data.products.length} products.</span>`;
        table.classList.remove('hidden');

    } catch (error) {
        statusMessage.innerHTML = `<span class="text-red-600 font-bold">Network Error:</span> Could not fetch products.`;
        console.error('Error fetching products:', error);
    }
}

// --- Initialization ---
loadBtn.addEventListener('click', fetchProducts);
