document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

   
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
               
                this.classList.add('is-loading');
                
                clearTimeout(this.searchTimeout);
               
                this.searchTimeout = setTimeout(() => {
                    this.classList.remove('is-loading');
                }, 500);
            });
        }
    }

   
    const assignmentCards = document.querySelectorAll('.assignment-card');
    assignmentCards.forEach(function(card) {
        const dueDate = card.querySelector('.due-date');
        if (dueDate) {
            const dueDateValue = new Date(dueDate.textContent);
            const now = new Date();
            
            if (dueDateValue < now) {
                card.classList.add('overdue');
            } else if (card.querySelector('.status-completed')) {
                card.classList.add('completed');
            }
        }
    });

   
    const gradeElements = document.querySelectorAll('.grade-points');
    gradeElements.forEach(function(element) {
        const points = parseInt(element.textContent);
        const maxPoints = parseInt(element.dataset.maxPoints);
        const percentage = (points / maxPoints) * 100;
        
        element.classList.remove('grade-excellent', 'grade-good', 'grade-satisfactory', 'grade-poor');
        
        if (percentage >= 90) {
            element.classList.add('grade-excellent');
        } else if (percentage >= 80) {
            element.classList.add('grade-good');
        } else if (percentage >= 70) {
            element.classList.add('grade-satisfactory');
        } else {
            element.classList.add('grade-poor');
        }
    });

   
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                event.preventDefault();
            }
        });
    });

  
    const activeAssignments = document.querySelectorAll('.assignment-card:not(.overdue):not(.completed)');
    if (activeAssignments.length > 0) {
        setInterval(function() {
            activeAssignments.forEach(function(card) {
                const dueDate = card.querySelector('.due-date');
                if (dueDate) {
                    const dueDateValue = new Date(dueDate.textContent);
                    const now = new Date();
                    
                    if (dueDateValue < now && !card.classList.contains('overdue')) {
                        card.classList.add('overdue');
                        // Show notification
                        showNotification('Новое просроченное задание!', 'warning');
                    }
                }
            });
        }, 60000);
    }

  
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Загрузка...';
                this.disabled = true;
            }
        });
    });
});


function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'только что';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} мин. назад`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} ч. назад`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} дн. назад`;
    }
}

window.HomeworkBoard = {
    showNotification,
    formatDate,
    formatTimeAgo
};
