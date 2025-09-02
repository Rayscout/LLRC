// 员工系统图标颜色随机分配器
// 基于图中的五种颜色：浅黄色、珊瑚色、青色、天蓝色、浅绿色

// 定义颜色数组
const iconColors = [
    '#F4E4BC', // 浅黄色/奶油色
    '#FFB6A3', // 珊瑚色/浅红色
    '#7FB3B3', // 青色/青绿色
    '#A8D8EA', // 天蓝色/浅蓝色
    '#B8E6B8'  // 浅绿色/薄荷绿
];

// 对应的深色文字颜色
const textColors = [
    '#8B7355', // 深棕色
    '#8B4513', // 深橙色
    '#2F4F4F', // 深青色
    '#4682B4', // 深蓝色
    '#228B22'  // 深绿色
];

// 随机获取颜色
function getRandomColor() {
    return iconColors[Math.floor(Math.random() * iconColors.length)];
}

// 获取对应的文字颜色
function getTextColor(backgroundColor) {
    const index = iconColors.indexOf(backgroundColor);
    return index !== -1 ? textColors[index] : '#333';
}

// 为图标分配随机颜色
function assignRandomColors() {
    // 统计卡片图标
    const statCards = document.querySelectorAll('.stat-card i');
    statCards.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 操作卡片图标
    const actionCards = document.querySelectorAll('.action-card h3 i');
    actionCards.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 活动图标
    const activityIcons = document.querySelectorAll('.activity-icon');
    activityIcons.forEach((icon, index) => {
        const bgColor = iconColors[index % iconColors.length];
        const textColor = getTextColor(bgColor);
        icon.style.background = bgColor;
        icon.querySelector('i').style.color = textColor;
    });

    // 页面标题图标
    const pageTitles = document.querySelectorAll('h1 i.fas');
    pageTitles.forEach(icon => {
        icon.style.color = iconColors[2]; // 使用青色作为标题颜色
    });

    // 表单和操作按钮图标
    const formIcons = document.querySelectorAll('.form-group i, .section-title i');
    formIcons.forEach(icon => {
        icon.style.color = iconColors[2]; // 使用青色
    });

    // 课程分类图标
    const courseCategories = document.querySelectorAll('.course-category i');
    courseCategories.forEach((icon, index) => {
        const color = iconColors[index % 3]; // 只使用前三种颜色
        icon.style.color = color;
    });

    // 目标管理图标
    const goalItems = document.querySelectorAll('.goal-item i');
    goalItems.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 反馈管理图标
    const feedbackItems = document.querySelectorAll('.feedback-item i');
    feedbackItems.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 项目经验图标
    const projectItems = document.querySelectorAll('.project-item i');
    projectItems.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 学习进度图标
    const learningItems = document.querySelectorAll('.learning-item i');
    learningItems.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 绩效分析图标
    const performanceItems = document.querySelectorAll('.performance-item i');
    performanceItems.forEach((icon, index) => {
        const color = iconColors[index % iconColors.length];
        icon.style.color = color;
    });

    // 添加悬停效果
    addHoverEffects();
}

// 添加悬停效果
function addHoverEffects() {
    const icons = document.querySelectorAll('.stat-card i, .action-card h3 i, .activity-icon i');
    
    icons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 延迟一点执行，确保所有元素都已加载
    setTimeout(assignRandomColors, 100);
});

// 为动态加载的内容重新分配颜色
function refreshIconColors() {
    setTimeout(assignRandomColors, 100);
}

// 导出函数供其他脚本使用
window.iconColorRandomizer = {
    assignRandomColors,
    refreshIconColors,
    getRandomColor
};
