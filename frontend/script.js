// Configuración de la API
const API_BASE_URL = '/api';
// Control de refrescos
let currentResultsIntervalId = null;
let isLoadingCurrentResults = false;

// Función para hacer peticiones a la API
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            // Evitar caches del navegador para asegurar datos frescos
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
    if (isLoadingCurrentResults) return; // Evitar solapamientos
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

// Cargar análisis mensual
async function loadMonthlyAnalysis() {
    showLoading('monthly-stats');
    try {
        const response = await fetchAPI('/analytics/monthly');
        if (response.success) {
            displayMonthlyAnalysis(response.data);
        } else {
            showError('monthly-stats', response.error);
        }
    } catch (error) {
        showError('monthly-stats', 'No se pudo cargar el análisis mensual');
    }
}

// Mostrar análisis mensual
function displayMonthlyAnalysis(data) {
    const statsContainer = document.getElementById('monthly-stats');
    const numbersContainer = document.getElementById('frequent-numbers');
    
    if (data.statistics) {
        statsContainer.innerHTML = `
            <div class="stat">
                <div class="stat-number">${data.total_draws || 0}</div>
                <div class="stat-label">Sorteos</div>
            </div>
            <div class="stat">
                <div class="stat-number">${data.statistics.total_unique_numbers || 0}</div>
                <div class="stat-label">Números Únicos</div>
            </div>
            <div class="stat">
                <div class="stat-number">${data.statistics.avg_frequency || 0}</div>
                <div class="stat-label">Frecuencia Promedio</div>
            </div>
        `;
        
        if (data.most_frequent) {
            numbersContainer.innerHTML = '';
            data.most_frequent.slice(0, 10).forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="number">${item.numero}</span>
                    <span class="percentage">${item.frequency} veces (${item.percentage}%)</span>
                `;
                numbersContainer.appendChild(li);
            });
        }
        afterRenderMonthly();
    } else {
        statsContainer.innerHTML = '<div class="loading">No hay datos disponibles</div>';
        numbersContainer.innerHTML = '<li>No hay datos disponibles</li>';
    }
}

// Cargar recomendaciones
async function loadRecommendations() {
    const container = document.getElementById('recommendations');
    showLoading('recommendations');
    try {
        const response = await fetchAPI('/recommendations');
        if (response.success && response.data.recommendations) {
            displayRecommendations(response.data);
        } else {
            container.innerHTML = '<div class="loading">No hay recomendaciones disponibles</div>';
        }
    } catch (error) {
        showError('recommendations', 'No se pudieron cargar las recomendaciones');
    }
}

// Mostrar recomendaciones
function displayRecommendations(data) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';
    
    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.slice(0, 5).forEach(rec => {
            const div = document.createElement('div');
            div.className = 'recommendation';
            div.innerHTML = `
                <div class="type">${rec.type}</div>
                <strong>Número ${rec.numero}</strong>
                <div>${rec.reason}</div>
                <div style="font-size: 0.9em; margin-top: 5px;">
                    Confianza: ${rec.confidence}% | Frecuencia: ${rec.frequency}
                </div>
            `;
            container.appendChild(div);
        });
        
        if (data.disclaimer) {
            const disclaimer = document.createElement('p');
            disclaimer.style.cssText = 'font-size: 1rem; color: #d0d0d0; margin-top: 15px;';
            disclaimer.textContent = data.disclaimer;
            container.appendChild(disclaimer);
        }
        afterRenderRecommendations();
    } else {
        container.innerHTML = '<div class="loading">No hay recomendaciones disponibles</div>';
    }
}

// Función para refrescar todos los datos
async function refreshData() {
    await Promise.all([
        loadCurrentResults(),
        loadMonthlyAnalysis(),
        loadRecommendations()
    ]);
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    setupScrollAnimations();
    refreshData();

    // Refrescar solo los resultados actuales cada 30 segundos
    currentResultsIntervalId = setInterval(loadCurrentResults, 30 * 1000);

    // Refrescar análisis y recomendaciones cada 5 minutos
    setInterval(refreshData, 5 * 60 * 1000);

    // Pausar el refresco cuando la pestaña no está visible (ahorra recursos)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (currentResultsIntervalId) {
                clearInterval(currentResultsIntervalId);
                currentResultsIntervalId = null;
            }
        } else {
            // Reanudar y hacer un fetch inmediato al volver
            if (!currentResultsIntervalId) {
                loadCurrentResults();
                currentResultsIntervalId = setInterval(loadCurrentResults, 30 * 1000);
            }
        }
    });
});

// Agregar botón de refrescar (opcional)
function addRefreshButton() {
    const header = document.querySelector('.header');
    const refreshBtn = document.createElement('button');
    refreshBtn.textContent = '🔄 Actualizar';
    refreshBtn.className = 'btn';
    refreshBtn.onclick = refreshData;
    header.appendChild(refreshBtn);
}

// Agregar el botón de refrescar cuando se carga la página
document.addEventListener('DOMContentLoaded', addRefreshButton);

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
    // observar los que aún no están visibles
    document.querySelectorAll('.reveal:not(.in-view)').forEach(el => window.__revealObserver.observe(el));
}

// Marcar dinámicos para animar cuando se cargan
function markChildrenReveal(container) {
    if (!container) return;
    [...container.children].forEach((child, i) => {
        child.classList.add('reveal');
        // pequeño retraso escalonado visual (se maneja por CSS transition)
        child.style.transitionDelay = `${Math.min(i * 60, 360)}ms`;
    });
    setupScrollAnimations();
}

// Hookear después de renderizados para agregar clases reveal
function afterRenderCurrentResults() {
    const container = document.getElementById('current-results');
    markChildrenReveal(container);
}
function afterRenderRecommendations() {
    const container = document.getElementById('recommendations');
    markChildrenReveal(container);
}
function afterRenderMonthly() {
    const stats = document.getElementById('monthly-stats');
    const list = document.getElementById('frequent-numbers');
    markChildrenReveal(stats);
    markChildrenReveal(list);
}