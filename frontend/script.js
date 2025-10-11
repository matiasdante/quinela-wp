// Configuración de la API
const API_BASE_URL = '/api';

// Control de refrescos
let currentResultsIntervalId = null;
let isLoadingCurrentResults = false;

// Función para hacer peticiones a la API
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            cache: 'no-store'
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

// Función para mostrar loading
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '<div class="loading">Cargando...</div>';
}

// Función para mostrar error
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="error">Error: ${message}</div>`;
}

// Cargar resultados actuales
async function loadCurrentResults() {
    if (isLoadingCurrentResults) return;
    isLoadingCurrentResults = true;
    showLoading('current-results');
    try {
        const response = await fetchAPI('/current');
        if (response.success) {
            displayCurrentResults(response.data);
        } else {
            showError('current-results', response.error);
        }
    } catch (error) {
        showError('current-results', 'No se pudieron cargar los resultados actuales');
    } finally {
        isLoadingCurrentResults = false;
    }
}

// Mostrar resultados actuales
function displayCurrentResults(results) {
    const container = document.getElementById('current-results');
    container.innerHTML = '';
    
    for (const [provincia, resultados] of Object.entries(results)) {
        const card = document.createElement('div');
        card.className = 'card';

        let content = `<h3>${provincia}</h3>`;

        if (Array.isArray(resultados)) {
            content += '<ul class="results-list">';
            resultados.forEach(([sorteo, numero]) => {
                content += `
                    <li>
                        <span>${sorteo}</span>
                        <span class="number">${numero}</span>
                    </li>
                `;
            });
            content += '</ul>';
        } else {
            content += `<p>${resultados}</p>`;
        }

        card.innerHTML = content;
        container.appendChild(card);
    }
    
    afterRenderCurrentResults();
}

// Función para refrescar los datos
async function refreshData() {
    await loadCurrentResults();
}

// Agregar botón de refrescar
function addRefreshButton() {
    const header = document.querySelector('.header');
    const refreshBtn = document.createElement('button');
    refreshBtn.textContent = '🔄 Actualizar';
    refreshBtn.className = 'btn';
    refreshBtn.onclick = refreshData;
    header.appendChild(refreshBtn);
}

// Animaciones de aparición en scroll
function setupScrollAnimations() {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) {
        document.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
        return;
    }
    if (!window.__revealObserver) {
        window.__revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    window.__revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
    }
    document.querySelectorAll('.reveal:not(.in-view)').forEach(el => window.__revealObserver.observe(el));
}

// Marcar elementos para animación
function markChildrenReveal(container) {
    if (!container) return;
    [...container.children].forEach((child, i) => {
        child.classList.add('reveal');
        child.style.transitionDelay = `${Math.min(i * 60, 360)}ms`;
    });
    setupScrollAnimations();
}

// Hook después de renderizar resultados
function afterRenderCurrentResults() {
    const container = document.getElementById('current-results');
    markChildrenReveal(container);
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    setupScrollAnimations();
    addRefreshButton();
    refreshData();

    // Refrescar resultados cada 30 segundos
    currentResultsIntervalId = setInterval(loadCurrentResults, 30 * 1000);

    // Pausar refresco cuando la pestaña no está visible
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (currentResultsIntervalId) {
                clearInterval(currentResultsIntervalId);
                currentResultsIntervalId = null;
            }
        } else {
            if (!currentResultsIntervalId) {
                loadCurrentResults();
                currentResultsIntervalId = setInterval(loadCurrentResults, 30 * 1000);
            }
        }
    });
});