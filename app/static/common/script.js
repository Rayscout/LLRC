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
  navToggle && navToggle.addEventListener('click', ()=>{
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
  modal && modal.addEventListener('click', (e)=>{ if(e.target === modal) closeModal(); })
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
  const toSigninInline = null;
  const toSignupInline = null;
  qsa('.auth-trigger').forEach(btn=>{
    btn.addEventListener('click',(e)=>{
      e.preventDefault();
      const type = btn.getAttribute('data-auth');
      if(!authModal) return;
      authModal.classList.add('open');
      authModal.setAttribute('aria-hidden','false');
      if(type==='signup'){
        authTitle && (authTitle.textContent = '注册');
        signupForm && (signupForm.style.display='block');
        signinForm && (signinForm.style.display='none');
        leftSignup && (leftSignup.style.display='block');
        leftSignin && (leftSignin.style.display='none');
      }else{
        authTitle && (authTitle.textContent = '登录');
        signupForm && (signupForm.style.display='none');
        signinForm && (signinForm.style.display='block');
        leftSignup && (leftSignup.style.display='none');
        leftSignin && (leftSignin.style.display='block');
      }
    })
  })
  ;(toSignin||{addEventListener:()=>{}}).addEventListener('click',()=>{
    authTitle && (authTitle.textContent='登录');
    signupForm && (signupForm.style.display='none');
    signinForm && (signinForm.style.display='block');
    leftSignup && (leftSignup.style.display='none');
    leftSignin && (leftSignin.style.display='block');
  })
  ;(toSignup||{addEventListener:()=>{}}).addEventListener('click',()=>{
    authTitle && (authTitle.textContent='注册');
    signupForm && (signupForm.style.display='block');
    signinForm && (signinForm.style.display='none');
    leftSignup && (leftSignup.style.display='block');
    leftSignin && (leftSignin.style.display='none');
  })
  ;(toSigninInline||{addEventListener:()=>{}}).addEventListener('click',()=>{
    authTitle && (authTitle.textContent='登录');
    signupForm && (signupForm.style.display='none');
    signinForm && (signinForm.style.display='block');
    leftSignup && (leftSignup.style.display='none');
    leftSignin && (leftSignin.style.display='block');
  })
  ;(toSignupInline||{addEventListener:()=>{}}).addEventListener('click',()=>{
    authTitle && (authTitle.textContent='注册');
    signupForm && (signupForm.style.display='block');
    signinForm && (signinForm.style.display='none');
    leftSignup && (leftSignup.style.display='block');
    leftSignin && (leftSignin.style.display='none');
  })
  function closeAuth(){
    if(!authModal) return;
    authModal.classList.remove('open');
    authModal.setAttribute('aria-hidden','true');
  }
  if(authModal){
    authModal.addEventListener('click',(e)=>{ if(e.target===authModal) closeAuth(); })
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
  }, { threshold: 0.2, rootMargin: '0px 0px -20% 0px' });
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
    prevBtn && (prevBtn.disabled = (page <= 0));
    nextBtn && (nextBtn.disabled = (page >= total - 1));
  }
  prevBtn && prevBtn.addEventListener('click', ()=>{ page = Math.max(0, page - 1); renderSlider(); })
  nextBtn && nextBtn.addEventListener('click', ()=>{ page = Math.min(totalPages()-1, page + 1); renderSlider(); })
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

  // Footer year
  const year = new Date().getFullYear();
  const yearSpan = qs('#year');
  if(yearSpan) yearSpan.textContent = String(year);

  // Scroll to top
  const scrollTopBtn = qs('#scrollTop');
  function onScroll(){
    const y = window.scrollY || document.documentElement.scrollTop;
    scrollTopBtn && scrollTopBtn.classList.toggle('show', y > 480);
  }
  window.addEventListener('scroll', onScroll);
  onScroll();
  scrollTopBtn && scrollTopBtn.addEventListener('click', ()=>window.scrollTo({top:0, behavior:'smooth'}));
})();


