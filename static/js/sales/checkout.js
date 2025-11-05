// --- Configuration ---
const API_BASE_URL = 'http://127.0.0.1:8000';
const CREATE_SALE_ENDPOINT = `${API_BASE_URL}/sales`;
const access_token = localStorage.getItem('access_token') || '';

let cart = [];
let saleReference = null;

// DOM Elements
const cartSection = document.getElementById('cartSection');
const cartItems = document.getElementById('cartItems');
const emptyCart = document.getElementById('emptyCart');
const cartSummary = document.getElementById('cartSummary');
const verificationSection = document.getElementById('verificationSection');
const messageDiv = document.getElementById('message');
const checkoutBtn = document.getElementById('checkoutBtn');
const verifyBtn = document.getElementById('verifyBtn');
const orderDetails = document.getElementById('orderDetails');
const totalItemsEl = document.getElementById('totalItems');
const subtotalEl = document.getElementById('subtotal');
const taxEl = document.getElementById('tax');
const totalEl = document.getElementById('total');

// --- Utility Functions ---
function showMessage(msg, type='info'){
    const styles = {
        success:'bg-green-100 text-green-800 border border-green-200',
        error:'bg-red-100 text-red-800 border border-red-200',
        info:'bg-blue-100 text-blue-800 border border-blue-200'
    };
    messageDiv.textContent = msg;
    messageDiv.className=`mb-6 p-4 rounded-lg ${styles[type]}`;
    messageDiv.classList.remove('hidden');
}
function hideMessage(){ messageDiv.classList.add('hidden'); }

// --- Cart Functions ---
function initializeCart(){
    const storedCart = localStorage.getItem('cart');
    cart = storedCart ? JSON.parse(storedCart).map(i=>({
        product_id:i.product_id,
        quantity:i.quantity,
        name:i.name || 'Product',
        price:Number(i.price)||0
    })) : [];
    displayCart();
}

function displayCart(){
    if(!cart || cart.length===0){
        cartItems.innerHTML='';
        emptyCart.classList.remove('hidden');
        cartSummary.classList.add('hidden');
        return;
    }
    emptyCart.classList.add('hidden');
    cartSummary.classList.remove('hidden');

    cartItems.innerHTML = cart.map((item,index)=>`
        <div class="flex items-center justify-between bg-white border-2 border-gray-200 rounded-lg p-4">
            <div class="flex items-center space-x-4 flex-1">
                <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center">IMG</div>
                <div class="flex-1">
                    <h3 class="font-semibold text-gray-800">${item.name}</h3>
                    <p class="text-sm text-gray-500">ID: ${item.product_id}</p>
                    <p class="text-sm text-gray-600">₦${item.price.toFixed(2)}</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <button onclick="updateQuantity(${index},-1)" class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300">-</button>
                <span>${item.quantity}</span>
                <button onclick="updateQuantity(${index},1)" class="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300">+</button>
                <span class="w-20 text-right font-bold">₦${(item.price*item.quantity).toFixed(2)}</span>
                <button onclick="removeFromCart(${index})" class="text-red-500 hover:text-red-700">×</button>
            </div>
        </div>
    `).join('');
    updateCartSummary();
}

function updateCartSummary(){
    const subtotal = cart.reduce((sum,i)=>sum+i.price*i.quantity,0);
    const tax = subtotal*0.1;
    const total = subtotal+tax;
    const totalItems = cart.reduce((sum,i)=>sum+i.quantity,0);
    totalItemsEl.textContent=totalItems;
    subtotalEl.textContent=subtotal.toFixed(2);
    taxEl.textContent=tax.toFixed(2);
    totalEl.textContent=total.toFixed(2);
}

window.updateQuantity=function(i,change){
    const newQty = cart[i].quantity+change;
    if(newQty>0){ cart[i].quantity=newQty; localStorage.setItem('cart',JSON.stringify(cart)); displayCart(); }
};

window.removeFromCart=function(i){ cart.splice(i,1); localStorage.setItem('cart',JSON.stringify(cart)); displayCart(); showMessage('Item removed','info'); };

// --- Sale Creation ---
async function createSales(){
    if(!cart || cart.length===0){ showMessage('Cart is empty','error'); return; }
    try{
        showMessage('Processing order...','info');
        checkoutBtn.disabled=true;

        const salePromises = cart.map(item=>
            fetch(CREATE_SALE_ENDPOINT,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${access_token}`
                },
                body:JSON.stringify({ product_id:item.product_id, quantity:item.quantity })
            }).then(r=>r.json())
        );

        const salesResults = await Promise.all(salePromises);
        saleReference = salesResults[0].reference;
        showMessage('Order created! Please verify payment','success');
        displayOrderSummary(salesResults);

        cartSection.classList.add('hidden');
        verificationSection.classList.remove('hidden');
        cart=[]; localStorage.removeItem('cart');

    }catch(err){ console.error(err); showMessage(`Error: ${err.message}`,'error'); checkoutBtn.disabled=false; }
}

// --- Display Summary ---
function displayOrderSummary(sales){
    let html='';
    sales.forEach(s=>{
        html+=`
        <div class="bg-white border-2 border-gray-200 rounded-lg p-4">
            <div class="flex justify-between"><span>Sale ID:</span><span>${s.sale_id||'N/A'}</span></div>
            <div class="flex justify-between"><span>Product ID:</span><span>${s.product_id||'N/A'}</span></div>
            <div class="flex justify-between"><span>Quantity:</span><span>${s.quantity||0}</span></div>
            <div class="flex justify-between"><span>Reference:</span><span class="font-mono text-sm">${s.reference}</span></div>
            <div class="flex justify-between font-bold"><span>Amount:</span><span>₦${(s.total_amount||s.amount||0).toFixed(2)}</span></div>
        </div>`;
    });
    const grandTotal = sales.reduce((sum,s)=>sum+(s.total_amount||s.amount||0),0);
    html+=`<div class="bg-green-50 border-2 border-green-200 rounded-lg p-4 font-bold text-lg flex justify-between">
        <span>Grand Total:</span><span>₦${grandTotal.toFixed(2)}</span></div>`;
    orderDetails.innerHTML=html;
}

// --- Verify Payment ---
async function verifyPayment(){
    if(!saleReference){ showMessage('No reference found','error'); return; }
    try{
        showMessage('Verifying payment...','info');
        verifyBtn.disabled=true;

        const resp = await fetch(`${API_BASE_URL}/sales/verify/${saleReference}`,{
            method:'POST',
            headers:{ 'Content-Type':'application/json','Authorization':`Bearer ${access_token}` },
            body:JSON.stringify({})
        });
        const data = await resp.json();
        if(!resp.ok) throw new Error(data.detail||'Verification failed');
        showMessage('Payment verified!','success');
        verifyBtn.textContent='Payment Verified';
        setTimeout(()=>window.location.href='index.html',2000);
    }catch(err){ console.error(err); showMessage(`Verification error: ${err.message}`,'error'); verifyBtn.disabled=false; }
}

// --- Event Listeners ---
checkoutBtn.addEventListener('click',createSales);
verifyBtn.addEventListener('click',verifyPayment);

// --- Initialize ---
initializeCart();
