// --- Configuration ---
const API_ENDPOINT = 'http://127.0.0.1:8000/product/product'; // endpoint to get single product by name

// --- DOM Elements ---
const form = document.getElementById('view-product-form');
const responseContainer = document.getElementById('response-container');
const inputName = document.getElementById('view-name');
const submitBtn = document.getElementById('submit-btn');

// --- Helper function to render stock items ---
function renderStockItems(stockItems) {
    if (!stockItems || stockItems.length === 0) return '<p>No stock items found for this product.</p>';

    let html = `
    <table class="min-w-full divide-y divide-gray-200 shadow-md rounded-lg mt-4">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Remaining</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost Price</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Selling Price</th>
                <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Added Date</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
    `;

    stockItems.forEach(stock => {
        html += `
        <tr>
            <td class="px-4 py-2 text-sm text-gray-700">${stock.quantity}</td>
            <td class="px-4 py-2 text-sm text-gray-700">${stock.remaining_quantity}</td>
            <td class="px-4 py-2 text-sm text-gray-700 price-mono">${stock.cost_price}</td>
            <td class="px-4 py-2 text-sm text-gray-700 price-mono">${stock.selling_price}</td>
            <td class="px-4 py-2 text-sm text-gray-700">${stock.added_date}</td>
        </tr>
        `;
    });

    html += '</tbody></table>';
    return html;
}

// --- Function to fetch product by name ---
async function fetchProduct(productName) {
    responseContainer.innerHTML = '<p class="text-indigo-600">Loading product details...</p>';
    try {
        const response = await fetch(`${API_ENDPOINT}?name=${encodeURIComponent(productName)}`);
        const data = await response.json();

        if (!response.ok || data.status !== true) {
            responseContainer.innerHTML = `<p class="text-red-600">Error fetching product: ${data.message || 'Unknown error'}</p>`;
            return;
        }

        // Render product details
        let html = `
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>Description:</strong> ${data.description || 'N/A'}</p>
            ${data.image ? `<p><strong>Image:</strong><br><img src="../../${data.image.replace("\\","/")}" class="mt-2 max-w-xs rounded-md shadow-md"></p>` : ''}
            <h3 class="mt-4 font-semibold text-gray-700">Stock Items:</h3>
            ${renderStockItems(data.stock_items)}
        `;
        responseContainer.innerHTML = html;

    } catch (error) {
        console.error('Error fetching product:', error);
        responseContainer.innerHTML = `<p class="text-red-600">Network error: Could not fetch product details.</p>`;
    }
}

// --- Initialization ---
const urlParams = new URLSearchParams(window.location.search);
const productName = urlParams.get('name');

if (productName) {
    inputName.value = productName; // prefill the input
    fetchProduct(productName); // auto-fetch on page load
} else {
    responseContainer.innerHTML = '<p class="text-red-500">No product name provided in URL.</p>';
    submitBtn.disabled = true;
}

// --- Form submission (if user manually searches) ---
form.addEventListener('submit', e => {
    e.preventDefault();
    const name = inputName.value.trim();
    if (name) fetchProduct(name);
});
