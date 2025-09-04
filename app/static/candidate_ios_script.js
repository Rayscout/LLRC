/*
 LLRC Header Start
 文件功能: 前端 JavaScript 脚本：app/static/candidate_ios_script.js
 创建时间: 2025-08-19 10:28
 创建人: 潘显雨
 更新记录:
 - 2025-08-19 10:58 by 潘显雨
- 2025-08-26 15:50 by 谢佳悦
- 2025-09-03 11:09 by 苏杰
 LLRC Header End
*/
/*
FILE-HEADER-AUTO-ADDED
文件: app/static/candidate_ios_script.js
功能: 通用模块
创建时间: 2025-08-21 09:55
创建人: 张宇成
更新记录:
- 2025-08-31 12:17 by 谢佳悦
*/
// 求职者iOS风格JavaScript - 苹果官网丝滑过渡效果

document.addEventListener('DOMContentLoaded', function() {
    // 初始化主题
    initTheme();
    
    // 初始化导航栏效果
    initNavbar();
    
    // 初始化滚动动画
    initScrollAnimations();
    
    // 初始化交互效果
    initInteractions();
});

// 主题管理
function initTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    const html = document.documentElement;
    
    // 从localStorage获取保存的主题
    const savedTheme = localStorage.getItem('candidate-theme');
    if (savedTheme) {
        html.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else {
        // 检查系统主题偏好
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = prefersDark ? 'dark' : 'light';
        html.setAttribute('data-theme', theme);
        updateThemeIcon(theme);
    }
    
    // 主题切换事件
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('candidate-theme', newTheme);
            updateThemeIcon(newTheme);
            
            // 添加切换动画
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
    }
    
    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('candidate-theme')) {
            const theme = e.matches ? 'dark' : 'light';
            html.setAttribute('data-theme', theme);
            updateThemeIcon(theme);
        }
    });
}

function updateThemeIcon(theme) {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
}

// 导航栏效果
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // 滚动时导航栏背景加深
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // 导航栏隐藏/显示效果（可选）
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // 激活当前导航项
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        // 移除所有active类
        link.classList.remove('active');
        
        // 检查当前路径是否匹配
        const href = link.getAttribute('href');
        if (href && (currentPath === href || currentPath.startsWith(href.replace('/smartrecruit/candidate', '')))) {
            link.classList.add('active');
        }
    });
    
    // 添加导航链接点击反馈
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 添加点击反馈
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // 调试信息
            console.log('导航链接点击:', this.textContent.trim(), 'href:', this.getAttribute('href'));
            
            // 确保链接正常工作
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                // 链接有效，允许正常跳转
                console.log('允许跳转到:', this.getAttribute('href'));
            } else {
                e.preventDefault();
                console.warn('导航链接无效:', this.getAttribute('href'));
            }
        });
    });
}

// 滚动动画
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                
                // 根据元素类型添加不同的动画
                if (element.classList.contains('card')) {
                    element.classList.add('animate-fade-in-up');
                } else if (element.classList.contains('job-card')) {
                    element.classList.add('animate-slide-in-left');
                } else if (element.classList.contains('section')) {
                    element.classList.add('animate-fade-in-up');
                }
                
                observer.unobserve(element);
            }
        });
    }, observerOptions);
    
    // 观察需要动画的元素
    const animatedElements = document.querySelectorAll('.card, .job-card, .section');
    animatedElements.forEach(el => observer.observe(el));
}

// 交互效果
function initInteractions() {
    // 按钮点击波纹效果
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // 卡片悬停效果增强
    const cards = document.querySelectorAll('.card, .job-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // 平滑滚动到锚点
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 工具函数
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-color);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        backdrop-filter: var(--blur-bg);
        -webkit-backdrop-filter: var(--blur-bg);
    `;
    
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// 加载状态管理
function showLoading(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        element.innerHTML = '<div class="loading"></div>';
        element.style.textAlign = 'center';
        element.style.padding = '40px';
    }
}

function hideLoading(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        element.innerHTML = '';
        element.style.textAlign = '';
        element.style.padding = '';
    }
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
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
    };
}

// 视差滚动效果
function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    const handleParallax = throttle(() => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-parallax') || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }, 16);
    
    window.addEventListener('scroll', handleParallax);
}

// 初始化视差效果
if (document.querySelector('[data-parallax]')) {
    initParallax();
}

// 导出全局函数
window.CandidateUI = {
    showNotification,
    showLoading,
    hideLoading,
    debounce,
    throttle
};
