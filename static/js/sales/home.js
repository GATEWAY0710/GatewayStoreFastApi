// -------------------------------------------------------------------
// --- CONFIGURATION ---
// -------------------------------------------------------------------
const LIST_PRODUCTS_API = 'http://127.0.0.1:8000/product'; // list of product names
const SINGLE_PRODUCT_API = 'http://127.0.0.1:8000/product/product?name='; // fetch single product by name
const SALES_API_ENDPOINT = 'http://127.0.0.1:8000/sales';
const API_BASE_URL = 'http://127.0.0.1:8000';
const LOGIN_PAGE = '/static/html/user/login.html';
const PROFILE_PAGE = '/static/html/user/profile.html';

// -------------------------------------------------------------------
// --- STATE & DOM ELEMENTS ---
// -------------------------------------------------------------------
let cart = {};

const productGrid = document.getElementById('product-grid');
const statusMessage = document.getElementById('status-message');
const navBar = document.getElementById('main-nav');
const cartSummary = document.getElementById('cart-summary');
const cartItemCount = document.getElementById('cart-item-count');
const cartTotalDisplay = document.getElementById('cart-total');
const globalCheckoutBtn = document.getElementById('global-checkout-btn');

// -------------------------------------------------------------------
// --- UTILITY FUNCTIONS ---
// -------------------------------------------------------------------
function formatNaira(amount) {
    const number = parseFloat(String(amount).replace(/[^0-9.]/g, ''));
    return new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 2,
    }).format(number);
}

function showMessage(msg, type = 'info') {
    statusMessage.classList.remove('hidden');
    statusMessage.innerHTML = `<p class="${type === 'error' ? 'text-red-600' : type === 'success' ? 'text-green-600' : 'text-blue-600'} font-bold">${msg}</p>`;
}

function hideMessage() {
    statusMessage.classList.add('hidden');
}

// -------------------------------------------------------------------
// --- AUTH & NAVBAR ---
// -------------------------------------------------------------------
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = LOGIN_PAGE;
}

function checkAuthState() {
    const accessToken = localStorage.getItem('access_token');
    navBar.innerHTML = '';

    if (accessToken) {
        const profileLink = document.createElement('a');
        profileLink.href = PROFILE_PAGE;
        profileLink.className = 'text-gray-600 hover:text-indigo-600 font-medium';
        profileLink.textContent = 'My Profile';
        navBar.appendChild(profileLink);

        const logoutBtn = document.createElement('button');
        logoutBtn.className = 'px-4 py-2 bg-red-600 text-white rounded-lg shadow-md hover:bg-red-700 transition duration-150';
        logoutBtn.textContent = 'Logout';
        logoutBtn.onclick = logout;
        navBar.appendChild(logoutBtn);
    } else {
        const loginBtn = `<a href="${LOGIN_PAGE}" class="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow-md hover:bg-indigo-700 transition duration-150">Login</a>`;
        navBar.innerHTML += loginBtn;
    }
}

// -------------------------------------------------------------------
// --- CART LOGIC ---
// -------------------------------------------------------------------
function updateCartSummary() {
    let totalItems = 0;
    let totalPrice = 0;

    for (const id in cart) {
        totalItems += cart[id].qty;
        totalPrice += cart[id].qty * cart[id].price;
    }

    cartItemCount.textContent = totalItems;
    cartTotalDisplay.textContent = formatNaira(totalPrice);

    if (totalItems > 0) {
        cartSummary.classList.remove('hidden');
        globalCheckoutBtn.disabled = false;
    } else {
        cartSummary.classList.add('hidden');
        globalCheckoutBtn.disabled = true;
    }
}

function addToCart(productId, productName, price, maxQty) {
    const sanitizedName = productName.replace(/\s/g, '_');
    const quantityInput = document.getElementById(`qty-${sanitizedName}`);
    const selectedQty = parseInt(quantityInput.value);

    if (selectedQty <= 0 || isNaN(selectedQty)) {
        showMessage("Please select a valid quantity.", 'error');
        return;
    }

    let currentQtyInCart = cart[productId] ? cart[productId].qty : 0;
    let newTotalQty = currentQtyInCart + selectedQty;

    if (newTotalQty > maxQty) {
        showMessage(`Cannot add ${selectedQty}. Total items exceed stock (${maxQty}).`, 'error');
        return;
    }

    cart[productId] = {
        id: productId,
        name: productName,
        qty: newTotalQty,
        price: price,
        max: maxQty
    };

    showMessage(`${selectedQty} × ${productName} added to cart!`, 'success');
    updateCartSummary();
}

// -------------------------------------------------------------------
// --- PAY ALL LOGIC ---
// -------------------------------------------------------------------
globalCheckoutBtn.addEventListener('click', async () => {
    if (!Object.keys(cart).length) {
        showMessage('Cart is empty!', 'error');
        return;
    }

    const items = Object.values(cart).map(item => ({
        product_id: item.id,
        quantity: item.qty
    }));

    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
        window.location.href = LOGIN_PAGE;
        return;
    }

    try {
        globalCheckoutBtn.disabled = true;
        globalCheckoutBtn.textContent = 'Processing payment...';
        hideMessage();

        // --- Step 1: Create Sale ---
        const createRes = await fetch(SALES_API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ items })
        });

        const createData = await createRes.json();
        if (!createRes.ok || !createData.status) throw new Error(createData.message || 'Failed to create sale');

        const saleReference = createData.reference;
        console.log('Sale created:', createData);

        // --- Step 2: Verify Payment ---
        const verifyRes = await fetch(`${API_BASE_URL}/sales/verify/${saleReference}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const verifyData = await verifyRes.json();
        if (!verifyRes.ok || !verifyData.status) throw new Error(verifyData.message || 'Payment verification failed');

        showMessage(`Payment successful! Reference: ${saleReference}`, 'success');
        cart = {};
        updateCartSummary();

    } catch (err) {
        console.error(err);
        showMessage(err.message, 'error');
    } finally {
        globalCheckoutBtn.disabled = false;
        globalCheckoutBtn.textContent = 'Pay All';
    }
});

// -------------------------------------------------------------------
// --- PRODUCT FETCHING & RENDERING ---
// -------------------------------------------------------------------
async function getProductDetails(productName) {
    try {
        const response = await fetch(`${SINGLE_PRODUCT_API}${encodeURIComponent(productName)}`);
        const data = await response.json();

        if (!response.ok || !data.status) {
            console.error('Single product fetch error:', data);
            return null;
        }

        const product = data;
        const imageUrl = product.image && !product.image.startsWith('http')
            ? API_BASE_URL + '/' + product.image.replace(/\\/g, '/')
            : product.image;

        const remainingQty = product.stock_items?.reduce((sum, stock) => sum + (stock.remaining_quantity || 0), 0) || 0;
        const sellingPrice = product.stock_items && product.stock_items.length > 0
            ? parseFloat(String(product.stock_items[0].selling_price).replace(/[^0-9.]/g, '')) || 0
            : 0;

        return {
            id: product.id,
            name: product.name,
            description: product.description,
            image_url: imageUrl,
            remaining_quantity: remainingQty,
            selling_price: sellingPrice
        };
    } catch (error) {
        console.error('Error fetching product details:', error);
        return null;
    }
}

async function fetchAndDisplayProducts() {
    statusMessage.classList.remove('hidden');
    productGrid.innerHTML = '';

    try {
        // Step 1: Get list of product names
        const response = await fetch(LIST_PRODUCTS_API);
        const data = await response.json();

        if (!response.ok || !data.status || !data.products) {
            showMessage(data.message || 'Error fetching products', 'error');
            return;
        }

        hideMessage();

        // Step 2: Fetch each product individually to get correct remaining_quantity
        for (const product of data.products) {
            const details = await getProductDetails(product.name);
            if (!details || details.remaining_quantity <= 0) continue;

            const sanitizedName = details.name.replace(/\s/g, '_');
            const inputId = `qty-${sanitizedName}`;
            const imageHTML = details.image_url
                ? `<img src="${details.image_url}" alt="${details.name}" class="product-image h-40 rounded-md mb-4">`
                : `<div class="h-40 flex items-center justify-center text-sm font-bold mb-4 rounded-md image-placeholder">[Image N/A]</div>`;

            const card = document.createElement('div');
            card.className = "product-card bg-white rounded-lg shadow-lg overflow-hidden p-4";
            card.innerHTML = `
                ${imageHTML}
                <h3 class="text-xl font-bold text-gray-800">${details.name}</h3>
                <p class="text-sm text-gray-500 mt-1 h-10 overflow-hidden">${details.description}</p>
                <div class="flex justify-between items-center mt-4">
                    <span class="text-2xl font-extrabold text-indigo-600">${formatNaira(details.selling_price)}</span>
                    <span class="text-sm text-gray-500">Stock: ${details.remaining_quantity}</span>
                </div>
                <div class="flex items-center space-x-2 mt-4">
                    <label for="${inputId}" class="text-sm font-medium text-gray-700">Qty:</label>
                    <input type="number" id="${inputId}" value="1" min="1" max="${details.remaining_quantity}" 
                        class="w-16 px-2 py-1 border border-gray-300 rounded-md text-center focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <button id="add-btn-${sanitizedName}" 
                    class="w-full mt-4 py-2 bg-indigo-500 text-white rounded-md font-semibold hover:bg-indigo-600 transition duration-150 shadow">
                    Add to Cart
                </button>
            `;
            productGrid.appendChild(card);

            document.getElementById(`add-btn-${sanitizedName}`).addEventListener('click', () => {
                addToCart(details.id, details.name, details.selling_price, details.remaining_quantity);
            });
        }

    } catch (error) {
        showMessage('Network error: Could not fetch products.', 'error');
        console.error(error);
    }
}

// -------------------------------------------------------------------
// --- INITIALIZATION ---
// -------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    checkAuthState();
    fetchAndDisplayProducts();
});
