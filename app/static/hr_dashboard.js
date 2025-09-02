// HR仪表盘交互增强脚本
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
    const animatedElements = document.querySelectorAll('.metric-card, .dashboard-section, .action-card');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
    
    // 鼠标跟踪效果
    const cards = document.querySelectorAll('.metric-card, .action-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            card.style.setProperty('--mouse-x', x + '%');
            card.style.setProperty('--mouse-y', y + '%');
        });
        
        // 鼠标离开时重置
        card.addEventListener('mouseleave', () => {
            card.style.setProperty('--mouse-x', '50%');
            card.style.setProperty('--mouse-y', '50%');
        });
    });
    
    // 增强的悬停效果
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // 添加悬停时的微动画
            this.style.transform = 'translateY(-8px) scale(1.02) rotateX(2deg)';
            
            // 图标旋转动画
            const icon = this.querySelector('.metric-icon i');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
            
            // 数值缩放动画
            const value = this.querySelector('.metric-value');
            if (value) {
                value.style.transform = 'scale(1.05)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            // 恢复原始状态
            this.style.transform = 'translateY(0) scale(1) rotateX(0deg)';
            
            const icon = this.querySelector('.metric-icon i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
            
            const value = this.querySelector('.metric-value');
            if (value) {
                value.style.transform = 'scale(1)';
            }
        });
    });
    
    // 快速操作卡片增强效果
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px) scale(1.05) rotateY(2deg)';
            
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(10deg)';
            }
            
            const title = this.querySelector('h4');
            if (title) {
                title.style.transform = 'translateY(-2px)';
            }
            
            const desc = this.querySelector('p');
            if (desc) {
                desc.style.transform = 'translateY(-1px)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1) rotateY(0deg)';
            
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
            
            const title = this.querySelector('h4');
            if (title) {
                title.style.transform = 'translateY(0)';
            }
            
            const desc = this.querySelector('p');
            if (desc) {
                desc.style.transform = 'translateY(0)';
            }
        });
    });
    
    // 列表项悬停效果
    const listItems = document.querySelectorAll('.job-item, .application-item');
    listItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(8px) scale(1.02)';
            
            const title = this.querySelector('h4');
            if (title) {
                title.style.transform = 'translateX(4px)';
            }
            
            const desc = this.querySelector('p');
            if (desc) {
                desc.style.transform = 'translateX(4px)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
            
            const title = this.querySelector('h4');
            if (title) {
                title.style.transform = 'translateX(0)';
            }
            
            const desc = this.querySelector('p');
            if (desc) {
                desc.style.transform = 'translateX(0)';
            }
        });
    });
    
    // 按钮悬停效果增强
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-small');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (this.classList.contains('btn-small')) {
                this.style.transform = 'translateY(-3px) scale(1.05)';
            } else if (this.classList.contains('btn-secondary')) {
                this.style.transform = 'translateY(-3px) scale(1.05)';
            } else {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
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
    
    // 页面加载时的入场动画
    function animateOnLoad() {
        const elements = document.querySelectorAll('.metric-card, .dashboard-section, .action-card');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('animate');
            }, index * 100);
        });
    }
    
    // 延迟执行入场动画
    setTimeout(animateOnLoad, 300);
    
    // 滚动时的视差效果
    let ticking = false;
    
    function updateParallax() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        const backgroundElements = document.querySelectorAll('.hr-dashboard::before');
        backgroundElements.forEach(el => {
            if (el) {
                el.style.transform = `translateY(${rate}px)`;
            }
        });
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // 添加键盘导航支持
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            // 为焦点元素添加视觉反馈
            document.addEventListener('focusin', function(e) {
                if (e.target.classList.contains('btn-primary') || 
                    e.target.classList.contains('btn-secondary') || 
                    e.target.classList.contains('btn-small')) {
                    e.target.style.outline = '2px solid rgba(102, 126, 234, 0.5)';
                    e.target.style.outlineOffset = '2px';
                }
            });
            
            document.addEventListener('focusout', function(e) {
                if (e.target.classList.contains('btn-primary') || 
                    e.target.classList.contains('btn-secondary') || 
                    e.target.classList.contains('btn-small')) {
                    e.target.style.outline = 'none';
                }
            });
        }
    });
    
    // 触摸设备优化
    if ('ontouchstart' in window) {
        // 为触摸设备添加触摸反馈
        const touchElements = document.querySelectorAll('.metric-card, .action-card, .job-item, .application-item');
        
        touchElements.forEach(el => {
            el.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.98)';
            });
            
            el.addEventListener('touchend', function() {
                this.style.transform = '';
            });
        });
    }
    
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
    
    // 初始化完成后的回调
    console.log('HR仪表盘交互增强已加载完成！');
});

