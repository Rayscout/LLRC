(function(){
  const qs = (s, el=document) => el.querySelector(s);
  const qsa = (s, el=document) => Array.from(el.querySelectorAll(s));

  const header = qs('.site-header');
  const navToggle = qs('#navToggle');
  const navList = qs('#navList');
  const links = qsa('[data-scroll]');
  const sections = qsa('section[id]');

  // Smooth scroll with offset
  function smoothScrollTo(targetId){
    const el = qs(`#${targetId}`);
    if(!el) return;
    const headerH = header.offsetHeight || 64;
    const top = el.getBoundingClientRect().top + window.pageYOffset - headerH;
    window.scrollTo({top, behavior:'smooth'});
  }

  links.forEach(a => {
    a.addEventListener('click', (e)=>{
      const href = a.getAttribute('href');
      if(href && href.startsWith('#')){
        e.preventDefault();
        const id = href.replace('#','');
        smoothScrollTo(id);
        if(navList.classList.contains('open')){
          navList.classList.remove('open');
          navToggle.setAttribute('aria-expanded','false');
        }
      }
    })
  })

  // Active section highlight
  function onScrollActive(){
    const scrollY = window.scrollY + (header.offsetHeight || 64) + 100;
    let current = 'home';
    sections.forEach(sec => {
      const top = sec.offsetTop;
      if(scrollY >= top){ current = sec.id; }
    })
    qsa('.nav-list a').forEach(a => {
      const sec = a.getAttribute('data-section');
      if(sec){ a.classList.toggle('active', sec === current); }
    })
  }
  window.addEventListener('scroll', onScrollActive);
  onScrollActive();

  // Mobile menu
  navToggle.addEventListener('click', ()=>{
    const open = !navList.classList.contains('open');
    navList.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', String(open));
  })

  // Tabs filter
  const tabs = qsa('.tabs .tab');
  const grid = qs('#portfolioGrid');
  tabs.forEach(tab => tab.addEventListener('click', ()=>{
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const filter = tab.getAttribute('data-filter');
    qsa('.tile', grid).forEach(tile =>{
      const cat = tile.getAttribute('data-category');
      const show = filter === 'all' || cat === filter;
      tile.style.display = show ? '' : 'none';
    })
  }))

  // Modal for portfolio details
  const modal = qs('#detailsModal');
  const modalTitle = qs('#modalTitle');
  const modalDesc = qs('#modalDesc');
  const modalImg = qs('#modalImg');
  const modalLink = qs('#modalLink');
  function openModal({title, desc, img, link}){
    modalTitle.textContent = title || '';
    modalDesc.textContent = desc || '';
    modalImg.src = img || '';
    modalImg.alt = title || '';
    if(link){ modalLink.href = link; modalLink.style.display='inline-flex'; }
    else { modalLink.style.display='none'; }
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
  }
  function closeModal(){
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
  }
  qsa('[data-details]').forEach(btn => {
    btn.addEventListener('click', ()=>{
      openModal({
        title: btn.getAttribute('data-title'),
        desc: btn.getAttribute('data-desc'),
        img: btn.getAttribute('data-img'),
        link: btn.getAttribute('data-link')
      })
    })
  })
  // close button only for details modal
  qsa('#detailsModal [data-modal-close]').forEach(el => el.addEventListener('click', closeModal))
  modal.addEventListener('click', (e)=>{ if(e.target === modal) closeModal(); })
  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeModal(); })

  // Auth modal
  const authModal = document.getElementById('authModal');
  const signinForm = document.getElementById('signinForm');
  const signupForm = document.getElementById('signupForm');
  const authTitle = document.getElementById('authTitle');
  const toSignin = document.getElementById('toSignin');
  const toSignup = document.getElementById('toSignup');
  const leftSignup = document.querySelector('#authModal .left-signup');
  const leftSignin = document.querySelector('#authModal .left-signin');
  // inline toggle buttons removed
  const toSigninInline = null;
  const toSignupInline = null;
  qsa('.auth-trigger').forEach(btn=>{
    btn.addEventListener('click',(e)=>{
      e.preventDefault();
      const type = btn.getAttribute('data-auth');
      if(!authModal) return;
      // 为了触发CSS过渡：先使容器可见，再在下一帧添加open类
      authModal.classList.remove('open');
      authModal.style.display = 'flex';
      authModal.setAttribute('aria-hidden','false');
      requestAnimationFrame(()=>{
        authModal.classList.add('open');
        authModal.style.display = '';
      });
      if(type==='signup'){
        if(authTitle) authTitle.textContent = '注册';
        if(signupForm) signupForm.style.display='block';
        if(signinForm) signinForm.style.display='none';
        if(leftSignup) leftSignup.style.display='block';
        if(leftSignin) leftSignin.style.display='none';
      }else{
        if(authTitle) authTitle.textContent = '登录';
        if(signupForm) signupForm.style.display='none';
        if(signinForm) signinForm.style.display='block';
        if(leftSignup) leftSignup.style.display='none';
        if(leftSignin) leftSignin.style.display='block';
      }
    })
  })
  ;(toSignin||{addEventListener:()=>{}}).addEventListener('click',()=>{
    if(authTitle) authTitle.textContent='登录';
    if(signupForm) signupForm.style.display='none';
    if(signinForm) signinForm.style.display='block';
    if(leftSignup) leftSignup.style.display='none';
    if(leftSignin) leftSignin.style.display='block';
  })
  ;(toSignup||{addEventListener:()=>{}}).addEventListener('click',()=>{
    if(authTitle) authTitle.textContent='注册';
    if(signupForm) signupForm.style.display='block';
    if(signinForm) signinForm.style.display='none';
    if(leftSignup) leftSignup.style.display='block';
    if(leftSignin) leftSignin.style.display='none';
  })
  ;(toSigninInline||{addEventListener:()=>{}}).addEventListener('click',()=>{
    if(authTitle) authTitle.textContent='登录';
    if(signupForm) signupForm.style.display='none';
    if(signinForm) signinForm.style.display='block';
    if(leftSignup) leftSignup.style.display='none';
    if(leftSignin) leftSignin.style.display='block';
  })
  ;(toSignupInline||{addEventListener:()=>{}}).addEventListener('click',()=>{
    if(authTitle) authTitle.textContent='注册';
    if(signupForm) signupForm.style.display='block';
    if(signinForm) signinForm.style.display='none';
    if(leftSignup) leftSignup.style.display='block';
    if(leftSignin) leftSignin.style.display='none';
  })
  function closeAuth(){
    if(!authModal) return;
    authModal.classList.remove('open');
    authModal.setAttribute('aria-hidden','true');
    // 避免clip-path残影：动画结束后保持隐藏
    setTimeout(()=>{
      if(!authModal.classList.contains('open')){
        authModal.style.display = '';
      }
    }, 300);
  }
  if(authModal){
    // backdrop click
    authModal.addEventListener('click',(e)=>{ if(e.target===authModal) closeAuth(); })
    // close button in auth modal
    qsa('#authModal [data-modal-close]').forEach(el=> el.addEventListener('click', closeAuth))
  }

  // Skills progress animate on view
  const bars = qsa('.skill .bar');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const el = entry.target;
        const v = el.getAttribute('data-value') || '0';
        el.style.setProperty('--progress', v + '%');
        el.classList.add('filled');
        io.unobserve(el);
      }
    })
  }, { threshold: 0.3 })
  bars.forEach(b => io.observe(b))

  // Reveal-on-scroll for cards/sections
  const animatedBlocks = qsa('.card,.tile,.t-card,.info-card,.product-card,.solution-item,.support-item,.resource-item,.ai-card,.case-card,.contact-item,.section-head');
  let lastY = window.pageYOffset;
  function updateScrollDir(){
    const y = window.pageYOffset;
    document.body.classList.toggle('scroll-down', y > lastY);
    document.body.classList.toggle('scroll-up', y < lastY);
    lastY = y;
  }
  window.addEventListener('scroll', updateScrollDir, { passive: true });
  updateScrollDir();

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const el = entry.target;
      if(entry.isIntersecting){
        el.classList.add('in-view');
        el.classList.remove('out-view');
      }else{
        el.classList.remove('in-view');
        el.classList.add('out-view');
      }
    })
  }, { threshold: 0.15, rootMargin: '0px 0px -15% 0px' });
  animatedBlocks.forEach(el => revealObserver.observe(el));

  // Testimonials slider (paged)
  const track = qs('#testimonialTrack');
  const prevBtn = qs('#prevTestimonials');
  const nextBtn = qs('#nextTestimonials');
  let page = 0;
  function itemsPerPage(){
    if(window.innerWidth >= 1024) return 3;
    if(window.innerWidth >= 768) return 2;
    return 1;
  }
  function totalPages(){
    const total = qsa('.t-card', track).length;
    return Math.max(1, Math.ceil(total / itemsPerPage()));
  }
  function renderSlider(){
    const total = totalPages();
    page = Math.min(page, total - 1);
    qsa('.t-card', track).forEach((card, idx)=>{
      const ip = itemsPerPage();
      const start = page * ip;
      const end = start + ip;
      card.style.display = (idx >= start && idx < end) ? '' : 'none';
    })
    prevBtn.disabled = (page <= 0);
    nextBtn.disabled = (page >= total - 1);
  }
  prevBtn.addEventListener('click', ()=>{ page = Math.max(0, page - 1); renderSlider(); })
  nextBtn.addEventListener('click', ()=>{ page = Math.min(totalPages()-1, page + 1); renderSlider(); })
  window.addEventListener('resize', renderSlider);
  renderSlider();

  // Button ripple effect
  qsa('.btn').forEach(btn=>{
    btn.addEventListener('click',function(e){
      const circle = document.createElement('span');
      const diameter = Math.max(this.clientWidth,this.clientHeight);
      const rect = this.getBoundingClientRect();
      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - diameter/2}px`;
      circle.style.top = `${e.clientY - rect.top - diameter/2}px`;
      circle.classList.add('ripple');
      const old = this.getElementsByClassName('ripple')[0];
      if(old) old.remove();
      this.appendChild(circle);
    })
  })

  // Contact form simulate (removed if form not present)
  const form = qs('#contactForm');
  const submitBtn = qs('#submitBtn');
  if(form && submitBtn){
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
      await new Promise(r=>setTimeout(r, 1200));
      alert('Message sent! Thank you for your message. I\'ll get back to you soon.');
      form.reset();
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send Message';
    })
  }

  // Footer year
  const year = new Date().getFullYear();
  const yearSpan = qs('#year');
  if(yearSpan) yearSpan.textContent = String(year);

  // Scroll to top
  const scrollTopBtn = qs('#scrollTop');
  function onScroll(){
    const y = window.scrollY || document.documentElement.scrollTop;
    scrollTopBtn.classList.toggle('show', y > 480);
  }
  window.addEventListener('scroll', onScroll);
  onScroll();
  scrollTopBtn.addEventListener('click', ()=>window.scrollTo({top:0, behavior:'smooth'}));

  // 背景动效系统
  function createFloatingShapes() {
    const shapesContainer = document.querySelector('.floating-shapes');
    if (!shapesContainer) return;
    
    const shapes = ['triangle', 'circle', 'square', 'diamond'];
    const colors = ['rgba(24, 144, 255, 0.3)', 'rgba(64, 169, 255, 0.4)', 'rgba(24, 144, 255, 0.2)', 'rgba(64, 169, 255, 0.3)'];
    
    for (let i = 0; i < 20; i++) {
      const shape = document.createElement('div');
      shape.className = `shape ${shapes[i % shapes.length]}`;
      shape.style.left = Math.random() * 100 + '%';
      shape.style.top = Math.random() * 100 + '%';
      shape.style.animationDelay = Math.random() * 18 + 's';
      shape.style.animationDuration = (18 + Math.random() * 12) + 's';
      shapesContainer.appendChild(shape);
    }
  }

  function createParticles() {
    const particleContainer = document.querySelector('.particle-system');
    if (!particleContainer) return;
    
    for (let i = 0; i < 28; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 10 + 's';
      particle.style.animationDuration = (10 + Math.random() * 6) + 's';
      particleContainer.appendChild(particle);
    }
  }

  function updateScrollProgress() {
    const scrollProgress = document.querySelector('.scroll-progress');
    if (!scrollProgress) return;
    
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    scrollProgress.style.width = scrollPercent + '%';
  }

  // 初始化背景动效
  createFloatingShapes();
  createParticles();
  
  // 监听滚动更新进度条
  window.addEventListener('scroll', updateScrollProgress);
  updateScrollProgress();
})();


