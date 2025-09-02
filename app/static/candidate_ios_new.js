/**
 * 求职者iOS新风格JavaScript
 * 包含深色模式、侧边栏控制、滚动效果、页面动画等功能
 */

// 全局变量
let currentTheme = 'light';
let isSidebarOpen = false;
let scrollY = 0;

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * 应用初始化
 */
function initializeApp() {
    initializeTheme();
    initializeNavbar();
    initializeSidebar();
    initializeScrollEffects();
    initializeAnimations();
    initializeLoadingStates();
    initializeNotifications();
    applySoftPalette();
    applyRainbowIcons();
}

/**
 * 主题系统初始化
 */
function initializeTheme() {
    // 检查本地存储的主题设置
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        // 检查系统主题偏好
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
    }
    
    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * 设置主题
 * @param {string} theme - 主题名称 ('light' 或 'dark')
 */
function setTheme(theme) {
    currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // 更新主题图标
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    // 触发主题变化事件
    document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
}

/**
 * 切换主题
 */
function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    
    // 添加切换动画
    document.body.style.transition = 'all 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

/**
 * 导航栏初始化
 */
function initializeNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    
    // 滚动时导航栏效果
    window.addEventListener('scroll', () => {
        scrollY = window.scrollY;
        
        if (scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * 侧边栏初始化
 */
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (!sidebar || !sidebarOverlay) return;
    
    // 点击遮罩关闭侧边栏
    sidebarOverlay.addEventListener('click', closeSidebar);
    
    // ESC键关闭侧边栏
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isSidebarOpen) {
            closeSidebar();
        }
    });
}

/**
 * 切换侧边栏
 */
function toggleSidebar() {
    if (isSidebarOpen) {
        closeSidebar();
    } else {
        openSidebar();
    }
}

/**
 * 打开侧边栏
 */
function openSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (!sidebar || !sidebarOverlay) return;
    
    sidebar.classList.add('open');
    sidebarOverlay.classList.add('show');
    isSidebarOpen = true;
    
    // 禁用body滚动
    document.body.style.overflow = 'hidden';
    
    // 添加打开动画
    sidebar.style.animation = 'slideInLeft 0.3s ease';
}

/**
 * 关闭侧边栏
 */
function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (!sidebar || !sidebarOverlay) return;
    
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('show');
    isSidebarOpen = false;
    
    // 恢复body滚动
    document.body.style.overflow = '';
    
    // 添加关闭动画
    sidebar.style.animation = 'slideInLeft 0.3s ease reverse';
}

/**
 * 用户菜单控制
 */
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    if (!dropdown) return;
    
    dropdown.classList.toggle('show');
    
    // 点击外部关闭菜单
    if (dropdown.classList.contains('show')) {
        setTimeout(() => {
            document.addEventListener('click', closeUserMenu);
        }, 0);
    }
}

/**
 * 关闭用户菜单
 */
function closeUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {
        dropdown.classList.remove('show');
    }
    document.removeEventListener('click', closeUserMenu);
}

/**
 * 滚动效果初始化
 */
function initializeScrollEffects() {
    // 平滑滚动到指定元素
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 滚动动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // 观察需要动画的元素
    document.querySelectorAll('.card, .stat-card, .btn').forEach(el => {
        observer.observe(el);
    });
}

/**
 * 动画系统初始化
 */
function initializeAnimations() {
    // 页面加载动画
    const animatedElements = document.querySelectorAll('.section-title, .section-subtitle, .card, .btn');
    
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // 视差滚动效果
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        parallaxElements.forEach(el => {
            const speed = el.dataset.parallax || 0.5;
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * 加载状态初始化
 */
function initializeLoadingStates() {
    // 页面加载完成
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
        
        // 隐藏加载动画
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.classList.remove('show');
        }
    });
    
    // 显示加载动画
    window.addEventListener('beforeunload', () => {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('show');
        }
    });
}

/**
 * 显示加载动画
 */
function showLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('show');
    }
}

/**
 * 隐藏加载动画
 */
function hideLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('show');
    }
}

/**
 * 平滑滚动到顶部
 */
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

/**
 * 显示通知
 * @param {string} message - 通知消息
 * @param {string} type - 通知类型 ('success', 'warning', 'error', 'info')
 * @param {number} duration - 显示时长（毫秒）
 */
function showNotification(message, type = 'info', duration = 3000) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // 自动隐藏
    if (duration > 0) {
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    }
}

/**
 * 获取通知图标
 * @param {string} type - 通知类型
 * @returns {string} 图标类名
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        warning: 'exclamation-triangle',
        error: 'times-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间
 * @returns {Function} 防抖后的函数
 */
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

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 限制时间
 * @returns {Function} 节流后的函数
 */
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

/**
 * 格式化数字
 * @param {number} num - 要格式化的数字
 * @returns {string} 格式化后的字符串
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * 格式化日期
 * @param {Date|string} date - 日期对象或字符串
 * @returns {string} 格式化后的日期字符串
 */
function formatDate(date) {
    const d = new Date(date);
    const now = new Date();
    const diff = now - d;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) {
        return '今天';
    } else if (days === 1) {
        return '昨天';
    } else if (days < 7) {
        return `${days}天前`;
    } else {
        return d.toLocaleDateString('zh-CN');
    }
}

/**
 * 复制到剪贴板
 * @param {string} text - 要复制的文本
 * @returns {Promise<boolean>} 是否复制成功
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('已复制到剪贴板', 'success');
        return true;
    } catch (err) {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showNotification('已复制到剪贴板', 'success');
            return true;
        } catch (err) {
            showNotification('复制失败', 'error');
            return false;
        } finally {
            document.body.removeChild(textArea);
        }
    }
}

/**
 * 检测设备类型
 * @returns {string} 设备类型 ('mobile', 'tablet', 'desktop')
 */
function getDeviceType() {
    const ua = navigator.userAgent;
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
        return 'tablet';
    }
    if (/mobile|android|iphone|ipod|blackberry|opera mini|iemobile/i.test(ua)) {
        return 'mobile';
    }
    return 'desktop';
}

/**
 * 检测是否支持触摸
 * @returns {boolean} 是否支持触摸
 */
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// 导出函数供全局使用
window.toggleTheme = toggleTheme;
window.toggleSidebar = toggleSidebar;
window.toggleUserMenu = toggleUserMenu;
window.scrollToTop = scrollToTop;
window.showNotification = showNotification;
window.copyToClipboard = copyToClipboard;

/**
 * 通知：面试安排轮询与下拉
 */
function initializeNotifications() {
    const btn = document.getElementById('notificationButton');
    const dropdown = document.getElementById('notificationDropdown');
    const badge = document.getElementById('notificationBadge');
    const list = document.getElementById('notificationList');
    if (!btn || !dropdown || !badge || !list) return;

    // 点击外部关闭
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target) && !btn.contains(e.target)) {
            dropdown.classList.remove('show');
        }
    });

    // 定时轮询
    const url = btn.getAttribute('data-notify-url');
    if (!url) return;

    async function fetchNotifications() {
        try {
            const resp = await fetch(url, { headers: { 'Accept': 'application/json' } });
            if (!resp.ok) return;
            const data = await resp.json();
            const items = Array.isArray(data.items) ? data.items : [];
            // 更新角标
            if (items.length > 0) {
                badge.style.display = 'inline-block';
                badge.textContent = String(items.length);
            } else {
                badge.style.display = 'none';
            }
            // 渲染列表
            list.innerHTML = '';
            if (items.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'notification-empty';
                empty.textContent = '暂无新的面试通知';
                list.appendChild(empty);
            } else {
                items.forEach(it => {
                    const el = document.createElement('div');
                    el.className = 'notification-item';
                    el.innerHTML = `
                        <div class="title">${escapeHtml(it.title || '面试安排')}</div>
                        <div class="meta">${escapeHtml(it.time || '')} · ${escapeHtml(it.location || '')}</div>
                    `;
                    list.appendChild(el);
                });
            }
        } catch (err) {
            // 静默失败，避免影响其他功能
        }
    }

    fetchNotifications();
    setInterval(fetchNotifications, 30000);
}

function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) dropdown.classList.toggle('show');
}

function escapeHtml(str) {
    return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

window.toggleNotificationDropdown = toggleNotificationDropdown;

/**
 * 将柔和配色随机分配给按钮和小标题图标
 * 调色板：#FFE4B5、#FAEBD7、#FFE4B5、#F0F8FF、#E6E6FA、#ADD8E6
 */
function applySoftPalette() {
    const palette = ['#FFE4B5', '#FAEBD7', '#FFE4B5', '#F0F8FF', '#E6E6FA', '#ADD8E6'];

    // 按钮（含主要与次要）
    const buttons = document.querySelectorAll('.btn, .btn-primary, .btn-secondary, .ios-button');
    let idx = 0;
    buttons.forEach(btn => {
        const color = palette[idx % palette.length];
        idx++;
        btn.style.backgroundColor = color;
        btn.style.borderColor = color;
        btn.style.color = '#101010';
        btn.addEventListener('mouseenter', () => { btn.style.filter = 'brightness(0.97)'; });
        btn.addEventListener('mouseleave', () => { btn.style.filter = ''; });
    });

    // 小标题图标
    const titleIcons = document.querySelectorAll('h2 i, h3 i, h4 i, .section-title i, .section-subtitle i, .card-title i, .ios-recent-title i, .ios-metric-icon i');
    titleIcons.forEach((icon, i) => {
        icon.style.color = palette[i % palette.length];
    });
}

/**
 * 为标题与卡片添加简洁图标（柔和彩虹色系，适配浅背景）
 */
function applyRainbowIcons() {
    // 图标前景色使用图中配色（不含背景黄）
    const colors = ['#FF6B6B', '#3DD5C9', '#4DB7E5', '#A9D6C6'];
    // 图标背景统一使用图中的柔和黄色
    const bgYellow = '#FDE7A1';
    const icons  = ['fa-star', 'fa-heart', 'fa-seedling', 'fa-bolt', 'fa-gem'];

    // 注入一次性样式，保证间距美观
    (function ensureIconStyles(){
        if (document.getElementById('candidate-inline-icon-style')) return;
        const style = document.createElement('style');
        style.id = 'candidate-inline-icon-style';
        style.textContent = `
            .inline-title-icon{margin-right:8px;vertical-align:middle;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.06)}
        `;
        document.head.appendChild(style);
    })();

    // 将 HEX 增加透明度
    function hexToRgba(hex, a){
        const h = hex.replace('#','');
        const r = parseInt(h.substring(0,2),16);
        const g = parseInt(h.substring(2,4),16);
        const b = parseInt(h.substring(4,6),16);
        return `rgba(${r}, ${g}, ${b}, ${a})`;
    }

    // 给标题添加图标
    const titles = document.querySelectorAll('.section-title, h2, h3, h4, .card-title');
    titles.forEach((title, i) => {
        // 避免重复添加
        if (title.querySelector('.inline-title-icon')) return;
        const icon = document.createElement('i');
        const color = colors[Math.floor(Math.random() * colors.length)];
        const fs = window.getComputedStyle(title).fontSize || '20px';
        icon.className = `fas ${icons[i % icons.length]} inline-title-icon`;
        icon.style.color = '#101010';
        icon.style.width = fs;
        icon.style.height = fs;
        icon.style.fontSize = fs; // 与文字同大小
        icon.style.backgroundColor = hexToRgba(bgYellow, 0.36);
        title.prepend(icon);
    });

    // 移除曾添加的卡片角标
    document.querySelectorAll('.card-badge').forEach(el => el.remove());
}
