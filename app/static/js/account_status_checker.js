/**
 * 账号状态检查器
 * 定期检查用户账号状态，如果被注销则自动退出
 */

class AccountStatusChecker {
    constructor() {
        this.checkInterval = 30000; // 30秒检查一次
        this.init();
    }

    init() {
        // 立即检查一次
        this.checkAccountStatus();
        
        // 设置定期检查
        setInterval(() => {
            this.checkAccountStatus();
        }, this.checkInterval);
        
        // 页面可见性变化时检查
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.checkAccountStatus();
            }
        });
    }

    async checkAccountStatus() {
        try {
            const response = await fetch('/api/check-account-status', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.status === 'deactivated') {
                    this.handleAccountDeactivated(data.message);
                } else if (data.status === 'active') {
                    this.updateStatusDisplay('active', '账号状态：活跃');
                }
            }
        } catch (error) {
            console.error('检查账号状态失败:', error);
        }
    }

    handleAccountDeactivated(message) {
        // 显示注销通知
        this.showDeactivationNotification(message);
        
        // 3秒后自动退出
        setTimeout(() => {
            this.forceLogout();
        }, 3000);
    }

    showDeactivationNotification(message) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = 'deactivation-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-exclamation-triangle"></i>
                <div class="notification-text">
                    <h4>账号已被注销</h4>
                    <p>${message}</p>
                    <p>3秒后自动退出登录...</p>
                </div>
            </div>
        `;

        // 添加样式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ffebee;
            border: 2px solid #f44336;
            border-radius: 8px;
            padding: 20px;
            max-width: 400px;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease-out;
        `;

        // 添加动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        // 添加到页面
        document.body.appendChild(notification);

        // 更新状态显示
        this.updateStatusDisplay('deactivated', '账号状态：已注销');
    }

    updateStatusDisplay(status, text) {
        const statusElement = document.querySelector('.account-status');
        if (statusElement) {
            statusElement.className = `account-status ${status}`;
            statusElement.innerHTML = `
                <i class="fas fa-${status === 'active' ? 'check-circle' : 'exclamation-triangle'}"></i>
                ${text}
                ${status === 'deactivated' ? '<p class="status-message">您的账号已被注销，请联系管理员。</p>' : ''}
            `;
        }
    }

    forceLogout() {
        // 清除本地存储
        localStorage.clear();
        sessionStorage.clear();
        
        // 重定向到登录页面
        window.location.href = '/auth/sign';
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new AccountStatusChecker();
});
