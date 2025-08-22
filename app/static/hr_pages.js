// HR页面交互增强脚本
document.addEventListener('DOMContentLoaded', function() {
    
    // 滚动渐显动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);
    
    // 观察所有需要动画的元素
    const animatedElements = document.querySelectorAll('.form-container, .list-container, .interviews-list-section, .calendar-container');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
    
    // 表单输入控件增强效果
    const formInputs = document.querySelectorAll('.form-group input, .form-group select, .form-group textarea');
    formInputs.forEach(input => {
        // 焦点效果
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateX(4px)';
            this.parentElement.style.borderColor = 'rgba(255, 255, 255, 0.25)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateX(0)';
            this.parentElement.style.borderColor = '';
        });
        
        // 输入验证反馈
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = 'var(--success-color)';
            } else {
                this.style.borderColor = '';
            }
        });
    });
    
    // 表单分组悬停效果
    const formSections = document.querySelectorAll('.form-section');
    formSections.forEach(section => {
        section.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
            this.style.borderColor = 'rgba(255, 255, 255, 0.25)';
        });
        
        section.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.borderColor = '';
        });
    });
    
    // 表格行悬停效果
    const tableRows = document.querySelectorAll('.data-table tbody tr, .interviews-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.background = 'var(--frosted-gray-light)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = '';
        });
    });
    
    // 日历槽位悬停效果
    const daySlots = document.querySelectorAll('.day-slot');
    daySlots.forEach(slot => {
        slot.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.background = 'var(--frosted-gray-dark)';
        });
        
        slot.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = '';
        });
    });
    
    // 面试事件悬停效果
    const interviewEvents = document.querySelectorAll('.interview-event');
    interviewEvents.forEach(event => {
        event.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
        });
        
        event.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // 状态标签悬停效果
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // 筛选器悬停效果
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
            this.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.1)';
        });
        
        select.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 页面标题悬停效果
    const pageHeaders = document.querySelectorAll('.page-header');
    pageHeaders.forEach(header => {
        header.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.15)';
        });
        
        header.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 表单容器悬停效果
    const formContainers = document.querySelectorAll('.form-container');
    formContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 16px 48px rgba(0, 0, 0, 0.15)';
        });
        
        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 列表容器悬停效果
    const listContainers = document.querySelectorAll('.list-container, .interviews-list-section');
    listContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 16px 48px rgba(0, 0, 0, 0.15)';
        });
        
        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 日历容器悬停效果
    const calendarContainers = document.querySelectorAll('.calendar-container');
    calendarContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 16px 48px rgba(0, 0, 0, 0.15)';
        });
        
        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 页面加载时的入场动画
    function animateOnLoad() {
        const elements = document.querySelectorAll('.form-container, .list-container, .interviews-list-section, .calendar-container');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('animate');
            }, index * 200);
        });
    }
    
    // 延迟执行入场动画
    setTimeout(animateOnLoad, 300);
    
    // 性能优化：节流滚动事件
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    // 应用节流到滚动事件
    const throttledScroll = throttle(() => {
        // 滚动时的渐显检查
        animatedElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible && !el.classList.contains('animate')) {
                el.classList.add('animate');
            }
        });
    }, 100);
    
    window.addEventListener('scroll', throttledScroll);
    
    // 触摸设备优化
    if ('ontouchstart' in window) {
        // 为触摸设备添加触摸反馈
        const touchElements = document.querySelectorAll('.form-section, .day-slot, .interview-event, .status-badge');
        
        touchElements.forEach(el => {
            el.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.98)';
            });
            
            el.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
    }
    
    // 键盘导航支持
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            // 为焦点元素添加视觉反馈
            document.addEventListener('focusin', function(e) {
                if (e.target.classList.contains('form-group')) {
                    e.target.style.transform = 'translateX(4px)';
                    e.target.style.borderColor = 'rgba(255, 255, 255, 0.25)';
                }
            });
            
            document.addEventListener('focusout', function(e) {
                if (e.target.classList.contains('form-group')) {
                    e.target.style.transform = 'translateX(0)';
                    e.target.style.borderColor = '';
                }
            });
        }
    });
    
    // 表单验证增强
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                             if (!field.value.trim()) {
                 isValid = false;
                 field.style.borderColor = 'var(--danger-color)';
                 field.style.animation = 'shake 0.5s ease-in-out';
             } else {
                 field.style.borderColor = '#6b7280';
                 field.style.animation = '';
             }
            });
            
            if (!isValid) {
                e.preventDefault();
                // 添加抖动动画
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes shake {
                        0%, 100% { transform: translateX(0); }
                        25% { transform: translateX(-5px); }
                        75% { transform: translateX(5px); }
                    }
                `;
                document.head.appendChild(style);
            }
        });
    });
    
    // 初始化完成后的回调
    console.log('HR页面交互增强已加载完成！');
});
