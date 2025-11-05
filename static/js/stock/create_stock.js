// --- Configuration ---
const API_PRODUCTS = 'http://127.0.0.1:8000/product';
const API_STOCK = 'http://127.0.0.1:8000/stock_entry';

// --- DOM Elements ---
const form = document.getElementById('stock-form');
const productSelect = document.getElementById('product-select');
const responseContainer = document.getElementById('response-container');
const submitBtn = document.getElementById('submit-btn');

// --- Helper ---
function setStatus(message, isError = false, preContent = null) {
    const statusClass = isError ? 'bg-red-100 border-red-400 text-red-700' : 'bg-green-100 border-green-400 text-green-700';
    responseContainer.className = `p-4 rounded-lg text-sm border ${statusClass}`;
    responseContainer.innerHTML = preContent ? message + `<pre>${preContent}</pre>` : message;
}

// --- Load Products ---
async function loadProducts() {
    productSelect.innerHTML = `<option value="">-- Loading products... --</option>`;
    try {
        const res = await fetch(API_PRODUCTS);
        const data = await res.json();

        if (!res.ok || !data.products) {
            setStatus("Failed to load products.", true);
            productSelect.innerHTML = `<option value="">-- Error loading products --</option>`;
            return;
        }

        if (data.products.length === 0) {
            productSelect.innerHTML = `<option value="">-- No products found --</option>`;
            return;
        }

        productSelect.innerHTML = `<option value="">-- Select a product --</option>`;
        data.products.forEach(product => {
            productSelect.innerHTML += `<option value="${encodeURIComponent(product.name)}">${product.name}</option>`;
        });

    } catch (err) {
        console.error(err);
        productSelect.innerHTML = `<option value="">-- Network error --</option>`;
        setStatus("Network error fetching products.", true);
    }
}

// --- Submit Stock ---
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const productName = productSelect.value;
    if (!productName) {
        setStatus("Please select a product.", true);
        return;
    }

    const data = {
        quantity: parseInt(document.getElementById('quantity').value),
        cost_price: parseFloat(document.getElementById('cost_price').value),
        selling_price: parseFloat(document.getElementById('selling_price').value)
    };

    const apiUrl = `${API_STOCK}?product_name=${productName}`;
    submitBtn.disabled = true;
    setStatus("Adding stock...");

    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await res.json().catch(() => res.text());
        if (!res.ok) {
            setStatus("Failed to add stock.", true, JSON.stringify(result, null, 2));
            return;
        }

        setStatus("Stock added successfully!", false, JSON.stringify(result, null, 2));

    } catch (err) {
        console.error(err);
        setStatus("Network error.", true, err.message);
    } finally {
        submitBtn.disabled = false;
    }
});

// --- Initialize ---
document.addEventListener('DOMContentLoaded', loadProducts);
