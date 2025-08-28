// HR页面滚动修复脚本
// 确保所有HR页面都能正常滚动

document.addEventListener('DOMContentLoaded', function() {
    console.log('HR滚动修复脚本已加载');
    
    // 强制启用页面滚动
    function enableScrolling() {
        // 移除可能阻止滚动的样式
        document.documentElement.style.overflow = 'auto';
        document.documentElement.style.overflowX = 'auto';
        document.documentElement.style.overflowY = 'auto';
        
        document.body.style.overflow = 'auto';
        document.body.style.overflowX = 'auto';
        document.body.style.overflowY = 'auto';
        
        // 确保页面可以滚动
        document.documentElement.style.height = 'auto';
        document.body.style.height = 'auto';
        
        // 移除可能阻止触摸滚动的样式
        document.documentElement.style.touchAction = 'auto';
        document.body.style.touchAction = 'auto';
        
        console.log('已启用页面滚动');
    }
    
    // 修复特定容器的滚动
    function fixContainerScrolling() {
        const containers = [
            '.hr-dashboard',
            '.ios-style',
            '.hr-page',
            '.candidates-container',
            '.hr-page-container',
            '.publish-job-container',
            '.jobs-container',
            '.hr-interviews',
            '.ios-container',
            '.ios-section'
        ];
        
        containers.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (element) {
                    element.style.overflow = 'auto';
                    element.style.overflowX = 'auto';
                    element.style.overflowY = 'auto';
                    element.style.height = 'auto';
                    element.style.minHeight = '100vh';
                    element.style.touchAction = 'auto';
                    
                    // 确保内容可以滚动
                    element.style.position = 'relative';
                    element.style.zIndex = '1';
                }
            });
        });
        
        console.log('已修复容器滚动');
    }
    
    // 修复触摸滚动
    function fixTouchScrolling() {
        // 为所有可滚动元素添加触摸滚动支持
        const scrollableElements = document.querySelectorAll('*');
        scrollableElements.forEach(element => {
            if (getComputedStyle(element).overflow !== 'visible') {
                element.style.webkitOverflowScrolling = 'touch';
                element.style.msOverflowStyle = 'auto';
            }
        });
        
        console.log('已修复触摸滚动');
    }
    
    // 移除可能阻止滚动的事件监听器
    function removeScrollBlockers() {
        // 移除可能阻止滚动的preventDefault调用
        const originalPreventDefault = Event.prototype.preventDefault;
        Event.prototype.preventDefault = function() {
            // 只阻止默认行为，不阻止滚动
            if (this.type !== 'wheel' && this.type !== 'touchmove') {
                originalPreventDefault.call(this);
            }
        };
        
        console.log('已移除滚动阻止器');
    }
    
    // 启用鼠标滚轮滚动
    function enableWheelScrolling() {
        document.addEventListener('wheel', function(e) {
            // 允许滚轮事件
            e.stopPropagation();
        }, { passive: true });
        
        document.addEventListener('touchmove', function(e) {
            // 允许触摸滚动
            e.stopPropagation();
        }, { passive: true });
        
        console.log('已启用滚轮和触摸滚动');
    }
    
    // 修复iOS Safari的滚动问题
    function fixIOSSafariScrolling() {
        // 检测iOS设备
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
        
        if (isIOS) {
            // iOS Safari特殊处理
            document.body.style.webkitOverflowScrolling = 'touch';
            document.body.style.position = 'relative';
            
            // 修复iOS Safari的100vh问题
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
            
            window.addEventListener('resize', () => {
                const vh = window.innerHeight * 0.01;
                document.documentElement.style.setProperty('--vh', `${vh}px`);
            });
            
            console.log('已修复iOS Safari滚动');
        }
    }
    
    // 执行所有修复
    function applyAllFixes() {
        enableScrolling();
        fixContainerScrolling();
        fixTouchScrolling();
        removeScrollBlockers();
        enableWheelScrolling();
        fixIOSSafariScrolling();
        
        console.log('所有滚动修复已应用');
    }
    
    // 立即应用修复
    applyAllFixes();
    
    // 延迟再次应用修复，确保所有内容都已加载
    setTimeout(applyAllFixes, 100);
    setTimeout(applyAllFixes, 500);
    setTimeout(applyAllFixes, 1000);
    
    // 监听页面变化，动态应用修复
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // 新元素被添加时，应用滚动修复
                setTimeout(applyAllFixes, 100);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 监听窗口大小变化
    window.addEventListener('resize', function() {
        setTimeout(applyAllFixes, 100);
    });
    
    // 监听滚动事件，确保滚动正常工作
    window.addEventListener('scroll', function() {
        // 滚动事件正常触发，说明滚动功能正常
    }, { passive: true });
    
    console.log('HR滚动修复脚本初始化完成');
});

// 导出函数供其他脚本使用
window.HRScrollFix = {
    enableScrolling: function() {
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
    },
    fixContainerScrolling: function() {
        const containers = document.querySelectorAll('.hr-dashboard, .ios-style, .hr-page');
        containers.forEach(container => {
            container.style.overflow = 'auto';
        });
    }
};

