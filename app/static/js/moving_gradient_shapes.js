/*
 LLRC Header Start
 文件功能: 前端 JavaScript 脚本：app/static/js/moving_gradient_shapes.js
 创建时间: 2025-08-24 10:31
 创建人: 张宇成
 更新记录:
 - 2025-08-24 11:01 by 苏杰
 LLRC Header End
*/
/*
FILE-HEADER-AUTO-ADDED
文件: app/static/js/moving_gradient_shapes.js
功能: 通用模块
创建时间: 2025-08-30 09:35
创建人: 李雨梦
更新记录:
- 2025-08-30 11:51 by 侯东杨
*/
// 员工系统移动渐变色形状脚本
// 基于图中的天蓝色/浅蓝色

document.addEventListener('DOMContentLoaded', function() {
    // 创建移动渐变色背景
    createMovingGradientBackground();
});

function createMovingGradientBackground() {
    // 检查是否已存在背景容器
    let backgroundContainer = document.querySelector('.moving-gradient-background');
    
    if (backgroundContainer) {
        backgroundContainer.remove();
    }
    
    // 创建背景容器
    backgroundContainer = document.createElement('div');
    backgroundContainer.className = 'moving-gradient-background';
    
    // 创建多个移动渐变色形状
    const shapes = [
        { size: 'small', delay: 0 },
        { size: 'medium', delay: -5 },
        { size: 'small', delay: -10 },
        { size: 'large', delay: -15 },
        { size: 'medium', delay: -20 },
        { size: 'small', delay: -25 },
        { size: 'medium', delay: -30 },
        { size: 'small', delay: -35 }
    ];
    
    shapes.forEach((shape, index) => {
        const gradientShape = document.createElement('div');
        gradientShape.className = `gradient-shape ${shape.size}`;
        
        // 设置随机初始位置
        const randomX = Math.random() * window.innerWidth;
        const randomY = Math.random() * window.innerHeight;
        gradientShape.style.left = randomX + 'px';
        gradientShape.style.top = randomY + 'px';
        
        // 设置动画延迟
        gradientShape.style.animationDelay = shape.delay + 's';
        
        // 移除颜色设置，现在使用CSS中的径向渐变光晕效果
        
        backgroundContainer.appendChild(gradientShape);
    });
    
    // 将背景容器添加到页面
    document.body.appendChild(backgroundContainer);
    
    // 添加窗口大小变化监听器
    window.addEventListener('resize', function() {
        // 重新创建背景以适应新的窗口大小
        setTimeout(createMovingGradientBackground, 100);
    });
}

// 导出函数供外部使用
window.createMovingGradientBackground = createMovingGradientBackground;
window.refreshGradientBackground = createMovingGradientBackground;
