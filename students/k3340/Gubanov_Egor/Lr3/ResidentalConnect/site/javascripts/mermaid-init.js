// Инициализация Mermaid для рендеринга диаграмм
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, загружен ли Mermaid
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#2196F3',
                primaryTextColor: '#fff',
                primaryBorderColor: '#1976D2',
                lineColor: '#424242',
                secondaryColor: '#FFC107',
                tertiaryColor: '#4CAF50'
            },
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            }
        });
        
        // Рендерим все диаграммы с классом mermaid
        const mermaidElements = document.querySelectorAll('pre.mermaid, code.mermaid');
        mermaidElements.forEach(function(element) {
            const code = element.textContent || element.innerText;
            if (code.trim()) {
                try {
                    mermaid.render('mermaid-' + Math.random().toString(36).substr(2, 9), code, function(svgCode) {
                        element.outerHTML = svgCode;
                    });
                } catch (e) {
                    console.error('Ошибка рендеринга Mermaid:', e);
                }
            }
        });
    } else {
        // Если Mermaid загружается асинхронно, ждем его
        const checkMermaid = setInterval(function() {
            if (typeof mermaid !== 'undefined') {
                clearInterval(checkMermaid);
                mermaid.initialize({ startOnLoad: true });
            }
        }, 100);
        
        // Таймаут на случай, если Mermaid не загрузится
        setTimeout(function() {
            clearInterval(checkMermaid);
        }, 5000);
    }
});

