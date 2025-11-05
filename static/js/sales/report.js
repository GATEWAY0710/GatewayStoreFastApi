// --- CONFIGURATION & ENDPOINTS ---
const BASE_URL = 'http://127.0.0.1:8000/report';

const SALES_REPORT_API = `${BASE_URL}`; // Requires year/month/day
const PL_API = `${BASE_URL}/profit-loss`; // Requires year/month/day
const SALES_STATUS_API = `${BASE_URL}/sales-status`; // No params
const PERFORMANCE_API = `${BASE_URL}/product-performance`; // No params
const LOW_STOCK_API = `${BASE_URL}/low-stock-alert`; // No params

// --- DOM Elements ---
const form = document.getElementById('report-form');
const loadingStatus = document.getElementById('loading-status');
const generateBtn = document.getElementById('generate-btn');

// Chart instances
let salesChartInstance = null;
let plChartInstance = null;

// --- UTILITY FUNCTIONS ---
function formatNaira(amount) {
    const number = parseFloat(String(amount).replace(/[^0-9.]/g, '')) || 0;
    return new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 0,
    }).format(number);
}

function formatRatio(successful, unsuccessful) {
    const total = successful + unsuccessful;
    if (total === 0) return 'N/A';
    return `${((successful / total) * 100).toFixed(1)}%`;
}

// --- CHART RENDERING ---
function renderSalesChart(totalSales, periodStr) {
    const ctx = document.getElementById('salesChart')?.getContext('2d');
    if (!ctx) return;

    if (salesChartInstance) salesChartInstance.destroy();

    salesChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [periodStr || ''],
            datasets: [{
                label: `Total Sales (${periodStr || ''})`,
                data: [totalSales],
                backgroundColor: 'rgba(79, 70, 229, 0.8)',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, ticks: { callback: formatNaira } } }
        }
    });

    const salesPeriodEl = document.getElementById('sales-period-title');
    if (salesPeriodEl) salesPeriodEl.textContent = `(${periodStr || ''})`;

    const salesTotalEl = document.getElementById('sales-total-amount');
    if (salesTotalEl) salesTotalEl.textContent = `Total Revenue: ${formatNaira(totalSales)}`;
}

function renderProfitLossChart(revenue, cost, netProfit, periodStr) {
    const ctx = document.getElementById('profitLossChart')?.getContext('2d');
    if (!ctx) return;

    if (plChartInstance) plChartInstance.destroy();

    plChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Total Cost', 'Net Profit'],
            datasets: [{
                data: [cost, netProfit],
                backgroundColor: ['rgba(239, 68, 68, 0.8)', 'rgba(16, 185, 129, 0.8)'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });

    const plPeriodEl = document.getElementById('pl-period-title');
    if (plPeriodEl) plPeriodEl.textContent = `(${periodStr || ''})`;

    const netProfitEl = document.getElementById('pl-net-profit');
    if (netProfitEl) {
        netProfitEl.textContent = `Net Profit: ${formatNaira(netProfit)}`;
        netProfitEl.classList.remove('text-green-600', 'text-red-600');
        netProfitEl.classList.add(netProfit >= 0 ? 'text-green-600' : 'text-red-600');
    }
}

// --- DATA FETCHING WITH TOKEN ---
async function fetchReport(year, month, day) {
    const token = localStorage.getItem('access_token') || '<YOUR_ACCESS_TOKEN>';
    const headers = { 'Authorization': `Bearer ${token}` };
    const dateQuery = `year=${year}${month ? `&month=${month}` : ''}${day ? `&day=${day}` : ''}`;

    const fetchWithAuth = async (url) => {
        try {
            const res = await fetch(url, { headers });
            if (!res.ok) return { status: false, error: res.statusText };
            return await res.json();
        } catch (err) {
            return { status: false, error: err.message };
        }
    };

    const [sales, pl, salesStatus, performance, lowStock] = await Promise.all([
        fetchWithAuth(`${SALES_REPORT_API}?${dateQuery}`),
        fetchWithAuth(`${PL_API}?${dateQuery}`),
        fetchWithAuth(SALES_STATUS_API),
        fetchWithAuth(PERFORMANCE_API),
        fetchWithAuth(LOW_STOCK_API)
    ]);

    return { sales, pl, salesStatus, performance, lowStock };
}

// --- RENDERING & INITIALIZATION ---
form?.addEventListener('submit', async (event) => {
    event.preventDefault();

    const year = document.getElementById('year')?.value;
    const month = document.getElementById('month')?.value;
    const day = document.getElementById('day')?.value;

    if (!year) return alert("Please enter the year.");

    loadingStatus?.classList.remove('hidden');
    generateBtn.disabled = true;

    try {
        const { sales, pl, salesStatus, performance, lowStock } = await fetchReport(year, month, day);

        // --- KPIs ---
        const salesRatioEl = document.getElementById('sales-success-ratio');
        if (salesRatioEl) salesRatioEl.textContent = formatRatio(salesStatus.successful_sales || 0, salesStatus.unsuccessful_sales || 0);

        const salesTotalEl = document.getElementById('sales-total');
        if (salesTotalEl) salesTotalEl.textContent = (salesStatus.successful_sales || 0) + (salesStatus.unsuccessful_sales || 0);

        const lowStockEl = document.getElementById('low-stock-count');
        if (lowStockEl) lowStockEl.textContent = lowStock.alerts?.length || 0;


        const topProductEl = document.getElementById('top-product-name');
        if (topProductEl) topProductEl.textContent = performance.highest_sold?.product_name || 'N/A';

        const topUnitsEl = document.getElementById('top-units-sold');
        if (topUnitsEl) topUnitsEl.textContent = performance.highest_sold?.units_sold?.toLocaleString() || 'N/A';

        const lowestProductEl = document.getElementById('lowest-name');
        if (lowestProductEl) lowestProductEl.textContent = performance.lowest_sold?.product_name || 'N/A';

        const lowestUnitsEl = document.getElementById('lowest-units-sold');
        if (lowestUnitsEl) lowestUnitsEl.textContent = performance.lowest_sold?.units_sold?.toLocaleString() || 'N/A';

        // --- Charts ---
        renderSalesChart(parseFloat(String(sales.total_sales).replace(/[^0-9.]/g, '')) || 0, sales.period || '');
        renderProfitLossChart(
            parseFloat(String(pl.total_revenue).replace(/[^0-9.]/g, '')) || 0,
            parseFloat(String(pl.total_cost).replace(/[^0-9.]/g, '')) || 0,
            parseFloat(String(pl.net_profit).replace(/[^0-9.]/g, '')) || 0,
            pl.period || ''
        );

    } catch (error) {
        console.error('Report Generation Failed:', error);
        alert(`An error occurred: ${error.message}`);
    } finally {
        loadingStatus?.classList.add('hidden');
        generateBtn.disabled = false;
    }
});

// Set default year to current year
document.addEventListener('DOMContentLoaded', () => {
    const yearInput = document.getElementById('year');
    if (yearInput) yearInput.value = new Date().getFullYear();
});

            console.log('Low stock response:', lowStock);

