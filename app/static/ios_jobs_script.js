/**
 * iOS风格岗位展示页面JavaScript功能
 * 包含搜索、筛选、模态框、主题切换等功能
 */

class JobsPage {
    constructor() {
        this.currentJobs = [];
        this.filteredJobs = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        this.isLoading = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.initThemeToggle();
        this.initSearch();
        this.initFilters();
        this.initScrollEffects();
        this.loadInitialJobs();
    }

    bindEvents() {
        // 搜索输入框事件
        const searchInput = document.getElementById('jobSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.handleSearch.bind(this));
            searchInput.addEventListener('focus', this.handleSearchFocus.bind(this));
        }

        // 搜索清除按钮
        const clearBtn = document.getElementById('searchClearBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', this.clearSearch.bind(this));
        }

        // 筛选标签事件
        const filterTags = document.querySelectorAll('.filter-tag');
        filterTags.forEach(tag => {
            tag.addEventListener('click', this.handleFilterClick.bind(this));
        });

        // 加载更多按钮
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', this.loadMoreJobs.bind(this));
        }

        // 键盘事件
        document.addEventListener('keydown', this.handleKeyboard.bind(this));

        // 滚动事件
        window.addEventListener('scroll', this.handleScroll.bind(this));
    }

    initThemeToggle() {
        const themeBtn = document.getElementById('iosThemeToggle');
        if (themeBtn) {
            themeBtn.addEventListener('click', this.toggleTheme.bind(this));
            
            // 同步与base.html的主题状态
            this.syncThemeState();
        }
    }

    syncThemeState() {
        const body = document.body;
        const themeBtn = document.getElementById('iosThemeToggle');
        
        if (body.classList.contains('dark')) {
            document.documentElement.setAttribute('data-theme', 'dark');
            if (themeBtn) {
                themeBtn.classList.add('active');
                themeBtn.innerHTML = '<i class="uil uil-sun"></i>';
            }
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            if (themeBtn) {
                themeBtn.classList.remove('active');
                themeBtn.innerHTML = '<i class="uil uil-moon"></i>';
            }
        }
    }

    toggleTheme() {
        const body = document.body;
        const themeBtn = document.getElementById('iosThemeToggle');
        
        if (body.classList.contains('dark')) {
            body.classList.remove('dark');
            document.documentElement.setAttribute('data-theme', 'light');
            if (themeBtn) {
                themeBtn.classList.remove('active');
                themeBtn.innerHTML = '<i class="uil uil-moon"></i>';
            }
            localStorage.setItem('theme', 'light');
        } else {
            body.classList.add('dark');
            document.documentElement.setAttribute('data-theme', 'dark');
            if (themeBtn) {
                themeBtn.classList.add('active');
                themeBtn.innerHTML = '<i class="uil uil-sun"></i>';
            }
            localStorage.setItem('theme', 'dark');
        }
    }

    initSearch() {
        const searchInput = document.getElementById('jobSearchInput');
        if (searchInput) {
            // 防抖搜索
            this.debouncedSearch = this.debounce(this.performSearch.bind(this), 300);
        }
    }

    handleSearch(event) {
        const query = event.target.value.trim();
        this.searchQuery = query;
        
        // 显示/隐藏清除按钮
        const clearBtn = document.getElementById('searchClearBtn');
        if (clearBtn) {
            clearBtn.style.display = query ? 'block' : 'none';
        }
        
        // 执行搜索
        this.debouncedSearch();
    }

    handleSearchFocus() {
        const searchInput = document.getElementById('jobSearchInput');
        if (searchInput) {
            searchInput.parentElement.style.transform = 'scale(1.02)';
        }
    }

    clearSearch() {
        const searchInput = document.getElementById('jobSearchInput');
        if (searchInput) {
            searchInput.value = '';
            this.searchQuery = '';
            searchInput.parentElement.style.transform = 'scale(1)';
            
            const clearBtn = document.getElementById('searchClearBtn');
            if (clearBtn) {
                clearBtn.style.display = 'none';
            }
            
            this.performSearch();
        }
    }

    performSearch() {
        if (!this.currentJobs.length) return;
        
        this.filteredJobs = this.currentJobs.filter(job => {
            const matchesSearch = !this.searchQuery || 
                job.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                (job.company_name && job.company_name.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
                (job.description && job.description.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
                (job.skills_required && job.skills_required.toLowerCase().includes(this.searchQuery.toLowerCase()));
            
            const matchesFilter = this.matchesFilter(job);
            
            return matchesSearch && matchesFilter;
        });
        
        this.renderJobs();
    }

    initFilters() {
        // 筛选逻辑已在handleFilterClick中实现
    }

    handleFilterClick(event) {
        const clickedTag = event.currentTarget;
        const filter = clickedTag.dataset.filter;
        
        // 更新活跃状态
        document.querySelectorAll('.filter-tag').forEach(tag => {
            tag.classList.remove('active');
        });
        clickedTag.classList.add('active');
        
        this.currentFilter = filter;
        this.performSearch();
    }

    matchesFilter(job) {
        switch (this.currentFilter) {
            case 'high-match':
                return job.match_score >= 70;
            case 'recent':
                const daysAgo = (Date.now() - new Date(job.date_posted).getTime()) / (1000 * 60 * 60 * 24);
                return daysAgo <= 7;
            case 'remote':
                return job.job_type === '远程' || 
                       (job.description && job.description.toLowerCase().includes('远程'));
            default:
                return true;
        }
    }

    initScrollEffects() {
        // 导航栏滚动效果
        let lastScrollTop = 0;
        const navbar = document.querySelector('.ios-navbar');
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // 向下滚动
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // 向上滚动
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop;
        });
    }

    loadInitialJobs() {
        // 获取页面上的岗位数据
        const jobCards = document.querySelectorAll('.job-card');
        this.currentJobs = Array.from(jobCards).map(card => ({
            id: card.dataset.jobId,
            title: card.querySelector('.job-title')?.textContent || '',
            company_name: card.querySelector('.company-name')?.textContent || '',
            location: card.querySelector('.job-location')?.textContent || '',
            description: card.querySelector('.job-description')?.textContent || '',
            job_type: card.querySelector('.job-type')?.textContent || '',
            salary: card.querySelector('.job-salary')?.textContent || '',
            experience_years: card.querySelector('.job-experience')?.textContent || '',
            skills_required: card.querySelector('.job-skills')?.textContent || '',
            date_posted: card.querySelector('.job-posted')?.textContent || '',
            match_score: parseInt(card.dataset.matchScore) || 0
        }));
        
        this.filteredJobs = [...this.currentJobs];
    }

    renderJobs() {
        const jobsGrid = document.getElementById('jobsGrid');
        if (!jobsGrid) return;
        
        // 清空现有内容
        jobsGrid.innerHTML = '';
        
        if (this.filteredJobs.length === 0) {
            this.showEmptyState();
            return;
        }
        
        // 渲染岗位卡片
        this.filteredJobs.forEach((job, index) => {
            const jobCard = this.createJobCard(job, index);
            jobsGrid.appendChild(jobCard);
        });
        
        // 隐藏空状态
        this.hideEmptyState();
    }

    createJobCard(job, index) {
        const card = document.createElement('article');
        card.className = 'job-card';
        card.dataset.jobId = job.id;
        card.dataset.matchScore = job.match_score;
        card.style.animationDelay = `${index * 0.1}s`;
        
        card.innerHTML = `
            <div class="match-indicator">
                <div class="match-score">${job.match_score}%</div>
                <div class="match-bar">
                    <div class="match-fill" style="width: ${job.match_score}%"></div>
                </div>
            </div>
            
            <div class="job-header">
                <h3 class="job-title">${job.title}</h3>
                <div class="company-info">
                    <span class="company-name">${job.company_name}</span>
                    <span class="job-location">
                        <i class="uil uil-map-marker"></i>
                        ${job.location}
                    </span>
                </div>
            </div>
            
            <div class="job-details">
                <div class="job-meta">
                    <span class="job-type">${job.job_type}</span>
                    <span class="job-salary">${job.salary}</span>
                    ${job.experience_years ? `<span class="job-experience">${job.experience_years}</span>` : ''}
                </div>
                
                <div class="job-description">
                    ${job.description.length > 150 ? job.description.substring(0, 150) + '...' : job.description}
                </div>
                
                ${job.skills_required ? `
                <div class="job-skills">
                    ${job.skills_required.split(',').slice(0, 3).map(skill => 
                        `<span class="skill-tag">${skill.trim()}</span>`
                    ).join('')}
                    ${job.skills_required.split(',').length > 3 ? 
                        `<span class="skill-more">+${job.skills_required.split(',').length - 3}</span>` : ''
                    }
                </div>
                ` : ''}
            </div>
            
            <div class="job-actions">
                <button class="action-btn primary" onclick="jobsPage.viewJobDetail('${job.id}')">
                    <i class="uil uil-eye"></i>
                    查看详情
                </button>
                <button class="action-btn secondary" onclick="jobsPage.saveJob('${job.id}')">
                    <i class="uil uil-heart"></i>
                    收藏
                </button>
            </div>
            
            <div class="job-posted">
                <i class="uil uil-clock"></i>
                ${job.date_posted}
            </div>
        `;
        
        return card;
    }

    showEmptyState() {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.style.display = 'block';
        }
    }

    hideEmptyState() {
        const emptyState = document.querySelector('.empty-state');
        if (emptyState) {
            emptyState.style.display = 'none';
        }
    }

    loadMoreJobs() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.innerHTML = '<i class="uil uil-spinner"></i> 加载中...';
            loadMoreBtn.disabled = true;
        }
        
        // 模拟加载更多数据
        setTimeout(() => {
            // 这里可以添加实际的API调用
            this.isLoading = false;
            
            if (loadMoreBtn) {
                loadMoreBtn.innerHTML = '<i class="uil uil-refresh"></i> 加载更多岗位';
                loadMoreBtn.disabled = false;
            }
            
            // 显示提示
            this.showToast('暂无更多岗位');
        }, 1500);
    }

    viewJobDetail(jobId) {
        // 这里可以添加获取岗位详情的API调用
        const job = this.currentJobs.find(j => j.id === jobId);
        if (!job) return;
        
        this.showJobModal(job);
    }

    showJobModal(job) {
        const modal = document.getElementById('jobModal');
        const modalTitle = document.getElementById('modalJobTitle');
        const modalBody = document.getElementById('modalJobBody');
        
        if (modal && modalTitle && modalBody) {
            modalTitle.textContent = job.title;
            
            modalBody.innerHTML = `
                <div class="job-detail-content">
                    <div class="detail-section">
                        <h3>公司信息</h3>
                        <p><strong>公司名称：</strong>${job.company_name}</p>
                        <p><strong>工作地点：</strong>${job.location}</p>
                        <p><strong>职位类型：</strong>${job.job_type}</p>
                        <p><strong>薪资范围：</strong>${job.salary}</p>
                        ${job.experience_years ? `<p><strong>经验要求：</strong>${job.experience_years}</p>` : ''}
                    </div>
                    
                    <div class="detail-section">
                        <h3>职位描述</h3>
                        <p>${job.description}</p>
                    </div>
                    
                    ${job.skills_required ? `
                    <div class="detail-section">
                        <h3>技能要求</h3>
                        <div class="skills-list">
                            ${job.skills_required.split(',').map(skill => 
                                `<span class="skill-tag">${skill.trim()}</span>`
                            ).join('')}
                        </div>
                    </div>
                    ` : ''}
                    
                    <div class="detail-section">
                        <h3>匹配度分析</h3>
                        <div class="match-analysis">
                            <div class="match-score-large">${job.match_score}%</div>
                            <div class="match-description">
                                ${this.getMatchDescription(job.match_score)}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }

    getMatchDescription(score) {
        if (score >= 90) return '非常匹配！这个岗位非常适合您的技能和经验。';
        if (score >= 70) return '高度匹配，建议优先考虑申请。';
        if (score >= 50) return '中等匹配，可以考虑申请。';
        if (score >= 30) return '部分匹配，需要补充相关技能。';
        return '匹配度较低，建议提升相关技能后再考虑。';
    }

    closeJobModal() {
        const modal = document.getElementById('jobModal');
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    saveJob(jobId) {
        // 这里可以添加收藏岗位的API调用
        this.showToast('岗位已收藏');
        
        // 更新按钮状态
        const saveBtn = event.target.closest('.action-btn');
        if (saveBtn) {
            saveBtn.innerHTML = '<i class="uil uil-heart-fill"></i> 已收藏';
            saveBtn.style.background = 'var(--accent-secondary)';
            saveBtn.disabled = true;
        }
    }

    showToast(message, type = 'info') {
        // 创建提示框
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="uil uil-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // 添加样式
        toast.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-medium);
            padding: var(--spacing-md) var(--spacing-lg);
            box-shadow: 0 4px 20px var(--shadow-secondary);
            z-index: 3000;
            transform: translateX(100%);
            transition: transform var(--transition-medium);
            max-width: 300px;
        `;
        
        document.body.appendChild(toast);
        
        // 显示动画
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // 自动隐藏
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }

    handleKeyboard(event) {
        // ESC键关闭模态框
        if (event.key === 'Escape') {
            this.closeJobModal();
        }
        
        // Ctrl/Cmd + K 聚焦搜索框
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            const searchInput = document.getElementById('jobSearchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
    }

    handleScroll() {
        // 滚动到顶部按钮显示/隐藏
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollToTopBtn = document.querySelector('.scroll-to-top');
        
        if (scrollTop > 300) {
            if (!scrollToTopBtn) {
                this.createScrollToTopButton();
            }
        } else if (scrollToTopBtn) {
            scrollToTopBtn.remove();
        }
    }

    createScrollToTopButton() {
        const btn = document.createElement('button');
        btn.className = 'scroll-to-top';
        btn.innerHTML = '<i class="uil uil-arrow-up"></i>';
        btn.title = '回到顶部';
        
        btn.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--accent-primary);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 20px var(--shadow-secondary);
            transition: all var(--transition-medium);
            z-index: 1000;
            opacity: 0;
            transform: scale(0.8);
        `;
        
        btn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        document.body.appendChild(btn);
        
        // 显示动画
        setTimeout(() => {
            btn.style.opacity = '1';
            btn.style.transform = 'scale(1)';
        }, 100);
    }

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
}

// 全局函数（供HTML调用）
function viewJobDetail(jobId) {
    if (window.jobsPage) {
        window.jobsPage.viewJobDetail(jobId);
    }
}

function saveJob(jobId) {
    if (window.jobsPage) {
        window.jobsPage.saveJob(jobId);
    }
}

function closeJobModal() {
    if (window.jobsPage) {
        window.jobsPage.closeJobModal();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    window.jobsPage = new JobsPage();
});

// 页面可见性变化时同步主题
document.addEventListener('visibilitychange', () => {
    if (window.jobsPage && !document.hidden) {
        window.jobsPage.syncThemeState();
    }
});
