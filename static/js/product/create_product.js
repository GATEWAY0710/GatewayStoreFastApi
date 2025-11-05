// --- Configuration & Endpoints ---
const API_ENDPOINT = 'http://127.0.0.1:8000/product'; // Assuming standard endpoint

// --- DOM Elements ---
const form = document.getElementById('product-form');
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

    setStatus('<p class="text-center text-blue-600">Sending request... Please wait.</p>', false);
    submitBtn.disabled = true;

    // FormData automatically handles 'multipart/form-data' for file uploads
    const formData = new FormData(form);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
            // NOTE: Do NOT set Content-Type header when using FormData with a file
        });

        const responseData = await response.json().catch(() => response.text());
        const isSuccess = response.ok && responseData && responseData.status === true;

        if (!response.ok) {
            const errorDetails = typeof responseData === 'string' ? responseData : JSON.stringify(responseData, null, 2);
            setStatus(`<p class="font-bold">HTTP Error! Status: ${response.status}</p><p>Details:</p>`, true, errorDetails);
            return;
        }

        // Success response handling
        const result = responseData;
        const statusColor = result.status ? 'text-green-700' : 'text-red-700';

        // Final success message display
        setStatus(`
            <p class="font-bold text-base ${statusColor}">Status: ${result.status ? '✅ Success' : '❌ Failure'}</p>
            <p class="mt-2">Message: ${result.message || 'Product created successfully'}</p>
            <hr class="my-3 border-gray-300">
            <p>Name: <strong class="text-gray-900">${result.name || 'N/A'}</strong></p>
            <p>Description: ${result.description || 'N/A'}</p>
            <p>Image URL: 
                <a href="${result.image}" target="_blank" class="text-blue-500 hover:underline">${result.image ? 'View Image' : 'N/A'}</a>
            </p>
            <hr class="my-3 border-gray-300">
            <p class="font-medium mt-3">Full JSON Response:</p>
        `, false, JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('Submission error:', error);
        setStatus(`<p class="text-red-600 font-bold">Network/Client Error:</p>`, true, error.message);
    } finally {
        submitBtn.disabled = false;
    }
});