// Кастомные JavaScript функции

document.addEventListener("DOMContentLoaded", function () {
    // Автоматическое скрытие сообщений через 5 секунд
    const alerts = document.querySelectorAll(".alert:not(.persistent-alert)");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Анимация карточек при прокрутке
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, observerOptions);

    // Применяем анимацию к карточкам
    document.querySelectorAll(".tour-card").forEach((card) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";
        card.style.transition = "all 0.6s ease";
        observer.observe(card);
    });

    // Подтверждение удаления
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            if (!confirm("Вы уверены, что хотите удалить эту запись?")) {
                e.preventDefault();
            }
        });
    });

    // Плавная прокрутка для якорей
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                target.scrollIntoView({
                    behavior: "smooth",
                });
            }
        });
    });
});

// Функция для обновления общей цены
function updateTotalPrice(tourPrice, personsElement, totalElement) {
    const persons = parseInt(personsElement.value) || 1;
    const totalPrice = tourPrice * persons;
    totalElement.textContent = totalPrice.toLocaleString("ru-RU") + " руб.";
}
