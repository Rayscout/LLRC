(function(){
  const qs = (s, el=document) => el.querySelector(s);
  const qsa = (s, el=document) => Array.from(el.querySelectorAll(s));

  const header = qs('.site-header');
  const navToggle = qs('#navToggle');
  const navList = qs('#navList');
  const links = qsa('[data-scroll]');
  const sections = qsa('section[id]');

  function smoothScrollTo(targetId){
    const el = qs(`#${targetId}`);
    if(!el) return;
    const headerH = header && header.offsetHeight || 64;
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
        if(navList && navList.classList.contains('open')){
          navList.classList.remove('open');
          navToggle && navToggle.setAttribute('aria-expanded','false');
        }
      }
    })
  })

  function onScrollActive(){
    const scrollY = window.scrollY + ((header && header.offsetHeight) || 64) + 100;
    let current = 'home';
    sections.forEach(sec => { if(scrollY >= sec.offsetTop) current = sec.id; })
    qsa('.nav-list a').forEach(a => {
      const sec = a.getAttribute('data-section');
      if(sec){ a.classList.toggle('active', sec === current); }
    })
  }
  window.addEventListener('scroll', onScrollActive);
  onScrollActive();

  navToggle && navToggle.addEventListener('click', ()=>{
    const open = !navList.classList.contains('open');
    navList.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', String(open));
  })

  // Modal for portfolio details
  const modal = qs('#detailsModal');
  const modalTitle = qs('#modalTitle');
  const modalDesc = qs('#modalDesc');
  const modalImg = qs('#modalImg');
  const modalLink = qs('#modalLink');
  function openModal({title, desc, img, link}){
    if(!modal) return;
    modalTitle && (modalTitle.textContent = title || '');
    modalDesc && (modalDesc.textContent = desc || '');
    if(modalImg){ modalImg.src = img || ''; modalImg.alt = title || ''; }
    if(modalLink){
      if(link){ modalLink.href = link; modalLink.style.display='inline-flex'; }
      else { modalLink.style.display='none'; }
    }
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
  }
  function closeModal(){ if(!modal) return; modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); }
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
  modal && qsa('#detailsModal [data-modal-close]').forEach(el => el.addEventListener('click', closeModal))
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
    if(!track) return 1;
    const total = qsa('.t-card', track).length;
    return Math.max(1, Math.ceil(total / itemsPerPage()));
  }
  function renderSlider(){
    if(!track) return;
    const total = totalPages();
    page = Math.min(page, total - 1);
    qsa('.t-card', track).forEach((card, idx)=>{
      const ip = itemsPerPage();
      const start = page * ip;
      const end = start + ip;
      card.style.display = (idx >= start && idx < end) ? '' : 'none';
    })
    if(prevBtn) prevBtn.disabled = (page <= 0);
    if(nextBtn) nextBtn.disabled = (page >= total - 1);
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

  // ensure theme toggle works even if core script not loaded
  const themeToggle = document.getElementById('themeToggle');
  if(themeToggle){
    const apply = (dark) => {
      document.body.classList.toggle('dark', !!dark);
      try{ themeToggle.checked = !!dark; }catch(e){}
      localStorage.setItem('mode', dark ? 'dark' : 'light');
    };
    const saved = localStorage.getItem('mode');
    apply(saved === 'dark');
    themeToggle.addEventListener('click', ()=> apply(!document.body.classList.contains('dark')));
    themeToggle.addEventListener('change', ()=> apply(themeToggle.checked));
    const lab = document.getElementById('themeToggleLabel');
    lab && lab.addEventListener('click', (e)=>{ if(e.target !== themeToggle){ e.preventDefault(); themeToggle.click(); } });
  }

  // --- AnimationManager from template to enable visual effects ---
  class AnimationManager {
    constructor(){
      this.observers = new Map();
      this.init();
    }
    init(){
      this.setupScrollProgress();
      this.setupHeaderEffects();
      this.setupScrollAnimations();
      this.setupParallaxEffects();
      this.setupCardInteractions();
      this.setupFloatingShapes();
      this.setupParticleSystem();
    }
    setupScrollProgress(){
      const progressBar = document.querySelector('.scroll-progress');
      if(!progressBar) return;
      window.addEventListener('scroll', () => {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
      });
    }
    setupHeaderEffects(){
      const headerEl = document.querySelector('.site-header');
      if(!headerEl) return;
      let lastScrollY = window.scrollY;
      window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        if (currentScrollY > 100) {
          headerEl.style.background = 'rgba(255, 255, 255, 0.95)';
          headerEl.style.backdropFilter = 'blur(10px)';
          headerEl.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        } else {
          headerEl.style.background = '#fff';
          headerEl.style.backdropFilter = 'none';
          headerEl.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        }
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
          headerEl.style.transform = 'translateY(-100%)';
        } else {
          headerEl.style.transform = 'translateY(0)';
        }
        lastScrollY = currentScrollY;
      });
    }
    setupScrollAnimations(){
      const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
      const featureObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.classList.add('animate');
          else entry.target.classList.remove('animate');
        });
      }, observerOptions);
      document.querySelectorAll('.feature-card, .feature-item').forEach(card => featureObserver.observe(card));
    }
    setupParallaxEffects(){
      window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        document.querySelectorAll('.parallax').forEach(el => { el.style.transform = `translateY(${scrolled * 0.5}px)`; });
      });
    }
    setupCardInteractions(){
      document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const centerX = rect.width / 2;
          const centerY = rect.height / 2;
          const rotateX = (y - centerY) / 10;
          const rotateY = (centerX - x) / 10;
          card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });
        card.addEventListener('mouseleave', () => {
          card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
        });
      });
    }
    setupFloatingShapes(){
      const shapesContainer = document.getElementById('floatingShapes');
      if(!shapesContainer) return;
      const shapes = ['triangle', 'circle', 'square', 'diamond'];
      for (let i = 0; i < 20; i++) {
        const shape = document.createElement('div');
        const shapeType = shapes[Math.floor(Math.random() * shapes.length)];
        shape.className = `shape ${shapeType}`;
        shape.style.left = Math.random() * 100 + '%';
        shape.style.top = Math.random() * 100 + '%';
        shape.style.animationDelay = Math.random() * 15 + 's';
        shape.style.animationDuration = (Math.random() * 10 + 10) + 's';
        shapesContainer.appendChild(shape);
      }
    }
    setupParticleSystem(){
      const particleContainer = document.getElementById('particleSystem');
      if(!particleContainer) return;
      for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 6) + 's';
        particleContainer.appendChild(particle);
      }
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    try { new AnimationManager(); } catch(e){}
    setTimeout(()=>{ document.body.style.opacity = '1'; }, 100);
  });
})();


