// iOS风格HR界面交互脚本
class IOSHRInterface {
    constructor() {
        this.currentSection = 0;
        this.sections = [];
        this.isScrolling = false;
        this.lastScrollTop = 0;
        this.init();
    }

    init() {
        this.setupScrollContainer();
        this.setupParallaxBackground();
        this.setupAnimations();
        this.setupNavigation();
        this.setupInteractiveElements();
        this.setupSmoothTransitions();
        this.setupHelpSystem(); // 添加帮助系统初始化
        this.setupQuickActions(); // 添加快速操作初始化
        this.setupFeatureOverview(); // 添加功能概览初始化
        this.setupStepGuide(); // 添加步骤指引初始化
    }

    // 设置滚动容器
    setupScrollContainer() {
        const container = document.querySelector('.ios-scroll-container');
        if (!container) return;

        this.sections = Array.from(document.querySelectorAll('.ios-section'));
        
        // 启用滚动捕捉
        container.style.scrollSnapType = 'y mandatory';
        
        // 监听滚动事件
        container.addEventListener('scroll', (e) => {
            this.handleScroll(e);
        });

        // 触摸设备支持
        let startY = 0;
        let startScrollTop = 0;

        container.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
            startScrollTop = container.scrollTop;
        });

        container.addEventListener('touchmove', (e) => {
            if (this.isScrolling) return;
            
            const deltaY = startY - e.touches[0].clientY;
            const newScrollTop = startScrollTop + deltaY;
            
            // 平滑滚动到最近的section
            this.scrollToNearestSection(newScrollTop);
        });
    }

    // 处理滚动事件
    handleScroll(e) {
        if (this.isScrolling) return;

        const container = e.target;
        const scrollTop = container.scrollTop;
        const windowHeight = container.clientHeight;
        
        // 计算当前section
        const currentSection = Math.round(scrollTop / windowHeight);
        
        if (currentSection !== this.currentSection) {
            this.currentSection = currentSection;
            // 移除这行，不再根据滚动位置更新导航状态
            // this.updateNavigation();
            this.triggerSectionAnimations(currentSection);
        }

        // 视差效果
        this.updateParallax(scrollTop);
        
        this.lastScrollTop = scrollTop;
    }

    // 滚动到最近的section
    scrollToNearestSection(scrollTop) {
        const windowHeight = window.innerHeight;
        const targetSection = Math.round(scrollTop / windowHeight);
        
        this.smoothScrollTo(targetSection * windowHeight);
    }

    // 平滑滚动
    smoothScrollTo(targetY) {
        this.isScrolling = true;
        
        const container = document.querySelector('.ios-scroll-container');
        const startY = container.scrollTop;
        const distance = targetY - startY;
        const duration = 800;
        const startTime = performance.now();

        const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            container.scrollTop = startY + distance * easeOutCubic(progress);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                this.isScrolling = false;
            }
        };

        requestAnimationFrame(animate);
    }

    // 设置视差背景
    setupParallaxBackground() {
        const parallaxBg = document.querySelector('.ios-parallax-bg');
        if (!parallaxBg) return;

        // 创建浮动形状
        for (let i = 0; i < 6; i++) {
            const shape = document.createElement('div');
            shape.className = 'ios-parallax-shape';
            shape.style.width = `${Math.random() * 100 + 50}px`;
            shape.style.height = shape.style.width;
            shape.style.left = `${Math.random() * 100}%`;
            shape.style.top = `${Math.random() * 100}%`;
            shape.style.animationDelay = `${Math.random() * 20}s`;
            shape.style.animationDuration = `${Math.random() * 10 + 15}s`;
            
            parallaxBg.appendChild(shape);
        }
    }

    // 更新视差效果
    updateParallax(scrollTop) {
        const shapes = document.querySelectorAll('.ios-parallax-shape');
        const speed = 0.5;
        
        shapes.forEach((shape, index) => {
            const yPos = (scrollTop * speed * (index + 1) * 0.1) % window.innerHeight;
            shape.style.transform = `translateY(${yPos}px) rotate(${scrollTop * 0.1}deg)`;
        });
    }

    // 设置动画
    setupAnimations() {
        // 观察器选项
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -10% 0px'
        };

        // 创建观察器
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, observerOptions);

        // 观察所有需要动画的元素
        const animatedElements = document.querySelectorAll('.ios-fade-in, .ios-fade-in-up, .ios-scale-in');
        animatedElements.forEach(el => observer.observe(el));
    }

    // 触发section动画
    triggerSectionAnimations(sectionIndex) {
        const section = this.sections[sectionIndex];
        if (!section) return;

        const animatedElements = section.querySelectorAll('.ios-fade-in, .ios-fade-in-up, .ios-scale-in');
        
        animatedElements.forEach((el, index) => {
            setTimeout(() => {
                this.animateElement(el);
            }, index * 100);
        });
    }

    // 动画元素
    animateElement(element) {
        if (element.classList.contains('animated')) return;
        
        element.classList.add('animated');
        
        // 根据类名应用不同的动画
        if (element.classList.contains('ios-fade-in')) {
            element.style.animation = 'iosFadeIn 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards';
        } else if (element.classList.contains('ios-fade-in-up')) {
            element.style.animation = 'iosFadeInUp 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards';
        } else if (element.classList.contains('ios-scale-in')) {
            element.style.animation = 'iosScaleIn 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards';
        }
    }

    // 设置导航
    setupNavigation() {
        // 设置移动端菜单切换
        const navToggle = document.querySelector('.ios-nav-toggle');
        const navMenu = document.querySelector('.ios-nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navToggle.classList.toggle('active');
                navMenu.classList.toggle('active');
            });

            // 点击导航链接后关闭移动端菜单
            const navLinks = document.querySelectorAll('.ios-nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (navToggle.classList.contains('active')) {
                        navToggle.classList.remove('active');
                        navMenu.classList.remove('active');
                    }
                });
            });
        }

        // 设置滚动时导航栏样式变化
        this.setupNavScrollEffect();

        // 设置导航栏按钮事件
        this.setupNavActions();
    }

    // 设置导航栏滚动效果
    setupNavScrollEffect() {
        const nav = document.querySelector('.ios-nav');
        if (!nav) return;

        let lastScrollTop = 0;
        const scrollThreshold = 50;

        const handleNavScroll = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > scrollThreshold) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }

            lastScrollTop = scrollTop;
        };

        // 监听页面滚动
        window.addEventListener('scroll', handleNavScroll);
        
        // 监听滚动容器滚动
        const scrollContainer = document.querySelector('.ios-scroll-container');
        if (scrollContainer) {
            scrollContainer.addEventListener('scroll', handleNavScroll);
        }
    }

    // 设置导航栏操作按钮
    setupNavActions() {
        const actionButtons = document.querySelectorAll('.ios-nav-button');
        
        actionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e);
                
                // 根据按钮类型执行不同操作
                const action = button.dataset.action;
                if (action) {
                    this.handleNavAction(action);
                }
            });
        });
    }

    // 处理导航栏操作
    handleNavAction(action) {
        switch (action) {
            case 'profile':
                this.showProfileMenu();
                break;
            case 'notifications':
                this.showNotifications();
                break;
            case 'settings':
                this.showSettings();
                break;
            case 'logout':
                this.handleLogout();
                break;
            default:
                console.log('Unknown action:', action);
        }
    }

    // 显示个人资料菜单
    showProfileMenu() {
        // 创建下拉菜单
        const profileMenu = document.createElement('div');
        profileMenu.className = 'ios-profile-menu';
        profileMenu.innerHTML = `
            <div class="ios-profile-menu-item" data-action="profile">
                <i class="fas fa-user"></i>
                <span>个人资料</span>
            </div>
            <div class="ios-profile-menu-item" data-action="settings">
                <i class="fas fa-cog"></i>
                <span>设置</span>
            </div>
            <div class="ios-profile-menu-item" data-action="logout">
                <i class="fas fa-sign-out-alt"></i>
                <span>退出登录</span>
            </div>
        `;
        
        // 添加点击事件
        const menuItems = profileMenu.querySelectorAll('.ios-profile-menu-item');
        menuItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const action = item.getAttribute('data-action');
                this.handleProfileMenuAction(action);
                profileMenu.remove();
            });
        });
        
        // 添加到页面
        document.body.appendChild(profileMenu);
        
        // 点击其他地方关闭菜单
        const closeMenu = (e) => {
            if (!profileMenu.contains(e.target)) {
                profileMenu.remove();
                document.removeEventListener('click', closeMenu);
            }
        };
        
        // 延迟添加事件监听器，避免立即触发
        setTimeout(() => {
            document.addEventListener('click', closeMenu);
        }, 100);
    }
    
    // 处理个人资料菜单操作
    handleProfileMenuAction(action) {
        switch (action) {
            case 'profile':
                window.location.href = '/smartrecruit/hr/profile/hr_profile';
                break;
            case 'settings':
                window.location.href = '/smartrecruit/hr/profile/hr_settings';
                break;
            case 'logout':
                if (confirm('确定要退出登录吗？')) {
                    window.location.href = '/auth/logout';
                }
                break;
            default:
                console.log('未知操作:', action);
        }
    }

    // 显示通知
    showNotifications() {
        // 创建通知提示
        const notification = document.createElement('div');
        notification.className = 'ios-notification';
        notification.innerHTML = `
            <i class="fas fa-bell"></i>
            <span>暂无新通知</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // 显示设置
    showSettings() {
        // 创建设置提示
        const settings = document.createElement('div');
        settings.className = 'ios-notification';
        settings.innerHTML = `
            <i class="fas fa-cog"></i>
            <span>设置功能开发中</span>
        `;
        
        document.body.appendChild(settings);
        
        setTimeout(() => {
            settings.remove();
        }, 3000);
    }

    // 处理退出登录
    handleLogout() {
        if (confirm('确定要退出登录吗？')) {
            // 这里可以添加退出登录的逻辑
            console.log('用户退出登录');
        }
    }

    // 设置交互元素
    setupInteractiveElements() {
        // 按钮点击效果
        const buttons = document.querySelectorAll('.ios-button');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e);
            });
        });

        // 卡片悬停效果
        const cards = document.querySelectorAll('.ios-card, .ios-metric-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.enhanceCard(card);
            });
            
            card.addEventListener('mouseleave', () => {
                this.resetCard(card);
            });
        });

        // 输入框焦点效果
        const inputs = document.querySelectorAll('.ios-input');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                this.focusInput(input);
            });
            
            input.addEventListener('blur', () => {
                this.blurInput(input);
            });
        });
    }

    // 创建涟漪效果
    createRippleEffect(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // 增强卡片效果
    enhanceCard(card) {
        card.style.transform = 'translateY(-8px) scale(1.02)';
        card.style.boxShadow = '0 12px 32px rgba(0, 0, 0, 0.15)';
    }

    // 重置卡片效果
    resetCard(card) {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '';
    }

    // 输入框聚焦效果
    focusInput(input) {
        input.style.transform = 'scale(1.02)';
        input.style.boxShadow = '0 0 0 3px rgba(0, 122, 255, 0.1)';
    }

    // 输入框失焦效果
    blurInput(input) {
        input.style.transform = 'scale(1)';
        input.style.boxShadow = '';
    }

    // 设置平滑过渡
    setupSmoothTransitions() {
        // 页面切换动画
        document.addEventListener('DOMContentLoaded', () => {
            document.body.style.opacity = '0';
            document.body.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                document.body.style.transition = 'all 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
                document.body.style.opacity = '1';
                document.body.style.transform = 'translateY(0)';
            }, 100);
        });

        // 链接点击过渡
        const links = document.querySelectorAll('a[href^="#"], a[href^="/"]');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.getAttribute('href').startsWith('#')) return;
                
                e.preventDefault();
                const href = link.getAttribute('href');
                
                // 页面退出动画
                document.body.style.transition = 'all 0.4s cubic-bezier(0.25, 1, 0.5, 1)';
                document.body.style.opacity = '0';
                document.body.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    window.location.href = href;
                }, 400);
            });
        });
    }

    // 工具方法：防抖
    debounce(func, wait) {
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

    // 工具方法：节流
    throttle(func, limit) {
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

    // 设置帮助系统
    setupHelpSystem() {
        this.setupHelpTriggers();
        this.setupContextHelp();
        this.setupFeatureTooltips();
    }

    // 设置帮助触发器
    setupHelpTriggers() {
        const helpTriggers = document.querySelectorAll('.ios-help-trigger');
        helpTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.showHelp(e.currentTarget.dataset.help);
            });
        });
    }

    // 显示帮助
    showHelp(helpId) {
        const helpPopup = document.getElementById(`help-${helpId}`);
        if (helpPopup) {
            // 关闭其他所有帮助弹窗
            document.querySelectorAll('.ios-help-popup.active').forEach(popup => {
                popup.classList.remove('active');
            });
            
            // 切换当前帮助弹窗
            helpPopup.classList.toggle('active');
            
            // 点击外部关闭帮助弹窗
            if (helpPopup.classList.contains('active')) {
                setTimeout(() => {
                    document.addEventListener('click', this.closeHelpOnOutsideClick.bind(this, helpPopup), { once: true });
                }, 100);
            }
        }
    }

    // 点击外部关闭帮助弹窗
    closeHelpOnOutsideClick(helpPopup, event) {
        if (!helpPopup.contains(event.target) && !event.target.closest('.ios-help-trigger')) {
            helpPopup.classList.remove('active');
        }
    }

    // 设置上下文帮助
    setupContextHelp() {
        // 为所有帮助弹窗添加关闭按钮
        document.querySelectorAll('.ios-help-popup').forEach(popup => {
            const closeButton = document.createElement('button');
            closeButton.className = 'ios-help-close';
            closeButton.innerHTML = '×';
            closeButton.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: none;
                border: none;
                font-size: 1.5rem;
                color: var(--ios-text-tertiary);
                cursor: pointer;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all var(--ios-transition-fast);
            `;
            
            closeButton.addEventListener('mouseenter', () => {
                closeButton.style.background = 'rgba(0, 0, 0, 0.1)';
                closeButton.style.color = 'var(--ios-text-primary)';
            });
            
            closeButton.addEventListener('mouseleave', () => {
                closeButton.style.background = 'none';
                closeButton.style.color = 'var(--ios-text-tertiary)';
            });
            
            closeButton.addEventListener('click', () => {
                popup.classList.remove('active');
            });
            
            popup.appendChild(closeButton);
        });
    }

    // 设置功能工具提示
    setupFeatureTooltips() {
        const tooltips = document.querySelectorAll('.ios-feature-tooltip');
        tooltips.forEach(tooltip => {
            const tooltipText = tooltip.querySelector('.ios-tooltip-text');
            if (tooltipText) {
                // 添加延迟显示
                let showTimeout;
                let hideTimeout;
                
                tooltip.addEventListener('mouseenter', () => {
                    clearTimeout(hideTimeout);
                    showTimeout = setTimeout(() => {
                        tooltipText.style.visibility = 'visible';
                        tooltipText.style.opacity = '1';
                    }, 300);
                });
                
                tooltip.addEventListener('mouseleave', () => {
                    clearTimeout(showTimeout);
                    hideTimeout = setTimeout(() => {
                        tooltipText.style.visibility = 'hidden';
                        tooltipText.style.opacity = '0';
                    }, 200);
                });
            }
        });
    }

    // 显示功能引导
    showFeatureGuide() {
        const guide = document.querySelector('.ios-feature-guide');
        if (guide) {
            guide.style.animation = 'iosFadeInUp 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards';
        }
    }

    // 隐藏功能引导
    hideFeatureGuide() {
        const guide = document.querySelector('.ios-feature-guide');
        if (guide) {
            guide.style.animation = 'iosFadeOut 0.5s ease-out forwards';
        }
    }

    // 设置快速操作
    setupQuickActions() {
        const quickActionButtons = document.querySelectorAll('.ios-quick-actions .ios-button');
        quickActionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e);
                this.handleQuickAction(button.textContent.trim());
            });
        });
    }

    // 处理快速操作
    handleQuickAction(action) {
        switch (action) {
            case '发布新职位':
                window.location.href = '/hr/recruitment/publish';
                break;
            case '查看申请':
                window.location.href = '/hr/dashboard/candidates';
                break;
            case '安排面试':
                window.location.href = '/hr/dashboard/interviews';
                break;
            default:
                console.log('未知的快速操作:', action);
        }
    }

    // 设置功能概览
    setupFeatureOverview() {
        const featureCards = document.querySelectorAll('.ios-feature-card');
        featureCards.forEach(card => {
            card.addEventListener('click', () => {
                this.enhanceCard(card);
                setTimeout(() => {
                    this.resetCard(card);
                }, 200);
            });
        });
    }

    // 设置步骤指引
    setupStepGuide() {
        const steps = document.querySelectorAll('.ios-step');
        steps.forEach((step, index) => {
            const isStatic = step.getAttribute('data-static') === 'true';
            if (!isStatic) {
                // 添加点击事件，可以展开显示更多信息
                step.addEventListener('click', () => {
                    this.showStepDetails(index);
                });
                // 添加悬停效果
                step.addEventListener('mouseenter', () => {
                    step.style.transform = 'translateY(-4px) scale(1.02)';
                });
                step.addEventListener('mouseleave', () => {
                    step.style.transform = 'translateY(0) scale(1)';
                });
            } else {
                step.style.cursor = 'default';
            }
        });
    }

    // 显示步骤详情
    showStepDetails(stepIndex) {
        const stepDetails = [
            {
                title: '选择职位',
                description: '从下拉菜单中选择要管理的职位，或者创建新的职位需求。',
                tips: ['确保职位信息完整', '设置合适的申请截止日期', '明确技能要求']
            },
            {
                title: '查看候选人',
                description: '浏览申请该职位的候选人列表，查看简历和基本信息。',
                tips: ['使用筛选器快速定位', '关注技能匹配度', '查看申请时间']
            },
            {
                title: '进行评估',
                description: '对候选人进行初步评估，记录评估结果和反馈意见。',
                tips: ['客观评估技能水平', '记录评估理由', '及时更新状态']
            }
        ];
        
        const detail = stepDetails[stepIndex];
        if (detail) {
            this.showStepDetailModal(detail);
        }
    }

    // 显示步骤详情模态框
    showStepDetailModal(detail) {
        const modal = document.createElement('div');
        modal.className = 'ios-step-detail-modal';
        modal.innerHTML = `
            <div class="ios-modal-content">
                <div class="ios-modal-header">
                    <h3>${detail.title}</h3>
                    <button class="ios-modal-close">×</button>
                </div>
                <div class="ios-modal-body">
                    <p>${detail.description}</p>
                    <h4>操作提示：</h4>
                    <ul>
                        ${detail.tips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
        
        // 添加样式
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: var(--ios-spacing-lg);
            animation: iosFadeIn 0.3s ease-out;
        `;
        
        const modalContent = modal.querySelector('.ios-modal-content');
        modalContent.style.cssText = `
            background: white;
            border-radius: var(--ios-radius-large);
            max-width: 500px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: var(--ios-shadow-heavy);
            animation: iosScaleIn 0.3s ease-out;
        `;
        
        // 关闭按钮事件
        const closeButton = modal.querySelector('.ios-modal-close');
        closeButton.addEventListener('click', () => {
            modal.remove();
        });
        
        // 点击外部关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        document.body.appendChild(modal);
    }
}

// 添加涟漪动画CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    new IOSHRInterface();
});

// 导出类供其他脚本使用
window.IOSHRInterface = IOSHRInterface;
