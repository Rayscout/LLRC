/**
 * 链接优化器 - 提升超链接的用户体验和性能
 */

class LinkOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.setupLinkOptimizations();
        this.setupExternalLinks();
        this.setupPreloadLinks();
    }

    /**
     * 设置链接优化
     */
    setupLinkOptimizations() {
        // 为所有内部链接添加优化
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href) return;

            // 内部链接优化
            if (href.startsWith('/') || href.startsWith('#') || href.includes(window.location.hostname)) {
                this.optimizeInternalLink(link, e);
            }
        });
    }

    /**
     * 优化内部链接
     */
    optimizeInternalLink(link, event) {
        const href = link.getAttribute('href');
        
        // 如果链接有data-preload属性，预加载页面
        if (link.hasAttribute('data-preload')) {
            this.preloadPage(href);
        }

        // 如果链接有data-smooth属性，平滑滚动
        if (link.hasAttribute('data-smooth') && href.startsWith('#')) {
            event.preventDefault();
            this.smoothScroll(href);
        }

        // 添加点击反馈
        this.addClickFeedback(link);
    }

    /**
     * 设置外部链接
     */
    setupExternalLinks() {
        const externalLinks = document.querySelectorAll('a[data-external]');
        
        externalLinks.forEach(link => {
            // 添加外部链接图标
            this.addExternalIcon(link);
            
            // 设置新窗口打开
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
            
            // 添加安全提示
            this.addSecurityNotice(link);
        });
    }

    /**
     * 设置链接预加载
     */
    setupPreloadLinks() {
        // 预加载用户可能访问的页面
        const preloadLinks = [
            '/talent/employee_management/profile',
            '/talent/employee_management/performance',
            '/talent/employee_management/learning_recommendation/dashboard'
        ];

        // 延迟预加载，避免影响初始页面加载
        setTimeout(() => {
            preloadLinks.forEach(link => {
                this.preloadPage(link);
            });
        }, 3000);
    }

    /**
     * 预加载页面
     */
    preloadPage(url) {
        if (this.isPreloaded(url)) return;

        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;
        link.setAttribute('data-preloaded', 'true');
        
        document.head.appendChild(link);
        
        // 标记为已预加载
        this.markAsPreloaded(url);
    }

    /**
     * 检查页面是否已预加载
     */
    isPreloaded(url) {
        return document.querySelector(`link[href="${url}"][data-preloaded]`) !== null;
    }

    /**
     * 标记页面为已预加载
     */
    markAsPreloaded(url) {
        sessionStorage.setItem(`preloaded_${url}`, 'true');
    }

    /**
     * 平滑滚动
     */
    smoothScroll(targetId) {
        const target = document.querySelector(targetId);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    /**
     * 添加点击反馈
     */
    addClickFeedback(link) {
        // 添加点击动画
        link.style.transition = 'transform 0.1s ease';
        link.style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            link.style.transform = 'scale(1)';
        }, 100);
    }

    /**
     * 添加外部链接图标
     */
    addExternalIcon(link) {
        if (!link.querySelector('.external-icon')) {
            const icon = document.createElement('i');
            icon.className = 'fas fa-external-link-alt external-icon';
            icon.style.marginLeft = '5px';
            icon.style.fontSize = '0.8em';
            icon.style.color = '#666';
            
            link.appendChild(icon);
        }
    }

    /**
     * 添加安全提示
     */
    addSecurityNotice(link) {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#')) {
                const confirmed = confirm(`即将跳转到外部网站：${href}\n\n请注意网络安全，确保链接来源可靠。`);
                if (!confirmed) {
                    e.preventDefault();
                }
            }
        });
    }

    /**
     * 创建快速跳转链接
     */
    createQuickLink(text, url, options = {}) {
        const link = document.createElement('a');
        link.href = url;
        link.textContent = text;
        link.className = 'quick-link';
        
        // 应用选项
        if (options.external) {
            link.setAttribute('data-external', 'true');
        }
        if (options.preload) {
            link.setAttribute('data-preload', 'true');
        }
        if (options.smooth) {
            link.setAttribute('data-smooth', 'true');
        }
        
        return link;
    }

    /**
     * 批量创建快速链接
     */
    createQuickLinks(container, links) {
        links.forEach(linkData => {
            const link = this.createQuickLink(
                linkData.text, 
                linkData.url, 
                linkData.options || {}
            );
            container.appendChild(link);
        });
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    window.linkOptimizer = new LinkOptimizer();
});

// 导出供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LinkOptimizer;
}
