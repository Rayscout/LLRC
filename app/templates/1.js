(function () {
  // Data matching the React version
  const revenueData = [
    { name: 'Sun', value: 8 },
    { name: 'Mon', value: 10 },
    { name: 'Tue', value: 12 },
    { name: 'Wed', value: 11 },
    { name: 'Thu', value: 9 },
    { name: 'Fri', value: 11 },
    { name: 'Sat', value: 12 },
  ];

  const guestsData = [
    { name: 'Sun', value: 8000 },
    { name: 'Mon', value: 10000 },
    { name: 'Tue', value: 12000 },
    { name: 'Wed', value: 9000 },
    { name: 'Thu', value: 6000 },
    { name: 'Fri', value: 8000 },
  ];

  const roomsData = [
    { name: 'Sun', occupied: 15, booked: 10, available: 25 },
    { name: 'Mon', occupied: 20, booked: 12, available: 18 },
    { name: 'Tue', occupied: 18, booked: 15, available: 17 },
    { name: 'Wed', occupied: 22, booked: 10, available: 18 },
    { name: 'Thu', occupied: 20, booked: 15, available: 15 },
    { name: 'Fri', occupied: 18, booked: 12, available: 20 },
    { name: 'Sat', occupied: 15, booked: 10, available: 25 },
  ];

  const foodOrdersData = [
    { name: 'Breakfast', value: 35 },
    { name: 'Lunch', value: 45 },
    { name: 'Dinner', value: 55 },
    { name: 'Room Service', value: 25 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const bookingData = [
    { id: 1, name: 'Ram Kailash', phone: '9905598912', bookingId: 'SDK89635', nights: 2, roomType: '1 King Room', guests: 2, paid: 'rsp.150', cost: 'rsp.1500', avatar: '/placeholder.svg?height=32&width=32' },
    { id: 2, name: 'Samira Karki', phone: '9815394203', bookingId: 'SDK89635', nights: 4, roomType: ['1 Queen', '1 King Room'], guests: 5, paid: 'paid', cost: 'rsp.5500', avatar: '/placeholder.svg?height=32&width=32' },
    { id: 3, name: 'Jeevan Rai', phone: '9865328452', bookingId: 'SDK89635', nights: 1, roomType: ['1 Deluxe', '1 King Room'], guests: 3, paid: 'rsp.150', cost: 'rsp.2500', avatar: '/placeholder.svg?height=32&width=32' },
    { id: 4, name: 'Bindu Sharma', phone: '9845653124', bookingId: 'SDK89635', nights: 3, roomType: ['1 Deluxe', '1 King Room'], guests: 2, paid: 'rsp.150', cost: 'rsp.3000', avatar: '/placeholder.svg?height=32&width=32' },
  ];

  const invoices = [
    { id: 'INV-2023-001', guest: 'Ram Kailash', date: '26 Jul 2023', amount: 'rsp.1500', status: 'Paid', items: [] },
    { id: 'INV-2023-002', guest: 'Samira Karki', date: '25 Jul 2023', amount: 'rsp.5500', status: 'Paid', items: [] },
    { id: 'INV-2023-003', guest: 'Jeevan Rai', date: '24 Jul 2023', amount: 'rsp.2500', status: 'Pending', items: [] },
  ];

  const foodOrders = [
    { id: 'FO-1234', guest: 'Ram Kailash', room: '101', items: ['Chicken Curry', 'Naan Bread', 'Rice'], total: 'rsp.850', status: 'Delivered', time: '12:30 PM' },
    { id: 'FO-1235', guest: 'Samira Karki', room: '205', items: ['Vegetable Pasta', 'Garlic Bread', 'Tiramisu'], total: 'rsp.1200', status: 'Preparing', time: '1:15 PM' },
    { id: 'FO-1236', guest: 'Jeevan Rai', room: '310', items: ['Club Sandwich', 'French Fries', 'Coke'], total: 'rsp.650', status: 'On the way', time: '1:45 PM' },
  ];

  const calendarEvents = [
    { date: 2, guest: 'Carl Larson II', nights: 2, guests: 2 },
    { date: 9, guest: 'Mrs. Emmett Morar', nights: 2, guests: 2 },
    { date: 24, guest: 'Marjorie Klocko', nights: 2, guests: 2 },
  ];

  // Mount helpers
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function setTitleBySection(section) {
    const title = section === 'dashboard' ? 'Dashboard'
      : section === 'check-in-out' ? 'Check In-Out'
      : section === 'rooms' ? 'Rooms'
      : section === 'messages' ? 'Messages'
      : section === 'customer-review' ? 'Customer Review'
      : section === 'billing' ? 'Billing System'
      : section === 'food-delivery' ? 'Food Delivery'
      : 'Premium Version';
    $('#pageTitle').textContent = title;
  }

  function showSection(id) {
    $$('#pageTitle');
    const map = {
      'dashboard': '#section-dashboard',
      'billing': '#section-billing',
      'food-delivery': '#section-food-delivery',
      'check-in-out': '#section-coming',
      'rooms': '#section-coming',
      'messages': '#section-coming',
      'customer-review': '#section-coming',
      'premium': '#section-coming',
    };
    $$('[data-section]').forEach(el => el.classList.add('is-hidden'));
    const target = $(map[id]);
    if (target) target.classList.remove('is-hidden');
    setTitleBySection(id);
    if (id !== 'dashboard' && id !== 'billing' && id !== 'food-delivery') {
      const text = id === 'check-in-out' ? 'Check In-Out'
        : id === 'rooms' ? 'Rooms'
        : id === 'messages' ? 'Messages'
        : id === 'customer-review' ? 'Customer Review'
        : 'Premium';
      $('#coming-text').textContent = `${text} module is currently being built. Please check back later.`;
    }
  }

  // Sidebar interactions
  function setupSidebar() {
    const sidebar = $('#sidebar');
    const open1 = $('#openSidebarBtn');
    const open2 = $('#openSidebarBtnHeader');
    const close = $('#closeSidebarBtn');
    const open = () => sidebar.classList.add('is-open');
    const hide = () => sidebar.classList.remove('is-open');
    if (open1) open1.addEventListener('click', open);
    if (open2) open2.addEventListener('click', open);
    if (close) close.addEventListener('click', hide);

    $$('.nav__item').forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.nav__item').forEach(b => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        const section = btn.getAttribute('data-section');
        showSection(section);
        hide();
      });
    });
  }

  // Render charts (simple)
  function renderRevenue() {
    const el = $('#chart-revenue');
    if (!el) return;
    const max = Math.max(...revenueData.map(d => d.value));
    el.innerHTML = '';
    revenueData.forEach(d => {
      const bar = document.createElement('div');
      bar.className = 'bar';
      bar.style.height = `${(d.value / max) * 100}%`;
      el.appendChild(bar);
    });
  }

  function renderGuestsLine() {
    const svg = $('#chart-guests');
    if (!svg) return;
    const max = Math.max(...guestsData.map(d => d.value));
    const pts = guestsData.map((d, i) => {
      const x = (i / (guestsData.length - 1)) * 100;
      const y = 50 - (d.value / max) * 45; // padding
      return `${x},${y}`;
    }).join(' ');
    svg.innerHTML = `<polyline fill="none" stroke="#3B82F6" stroke-width="2" points="${pts}" />` +
      guestsData.map(p => {
        const i = guestsData.indexOf(p);
        const x = (i / (guestsData.length - 1)) * 100;
        const y = 50 - (p.value / max) * 45;
        return `<circle cx="${x}" cy="${y}" r="1.6" fill="#fff" stroke="#3B82F6" stroke-width="1.2" />`;
      }).join('');
  }

  function renderRooms() {
    const el = $('#chart-rooms');
    if (!el) return;
    const max = Math.max(...roomsData.map(d => Math.max(d.occupied, d.booked, d.available)));
    el.innerHTML = '';
    roomsData.forEach(d => {
      const g = document.createElement('div');
      g.style.display = 'grid';
      g.style.gridTemplateColumns = 'repeat(3, 1fr)';
      g.style.alignItems = 'end';
      g.style.gap = '4px';
      const mk = (val, cls) => { const b = document.createElement('div'); b.className = `bar ${cls}`; b.style.height = `${(val / max) * 100}%`; return b; };
      g.appendChild(mk(d.occupied, 'bar--blue'));
      g.appendChild(mk(d.booked, 'bar--green'));
      g.appendChild(mk(d.available, '')); // amber default
      el.appendChild(g);
    });
  }

  // Tables
  function renderBookings() {
    const tbody = $('#table-bookings tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    bookingData.forEach(b => {
      const tr = document.createElement('tr');
      const roomType = Array.isArray(b.roomType) ? b.roomType.join(', ') : b.roomType;
      tr.innerHTML = `
        <td>
          <div class="row a-center gap-8">
            <span class="avatar"></span>
            <div>
              <div style="font-weight:600">${b.name}</div>
              <div class="xsmall muted">${b.phone}</div>
            </div>
          </div>
        </td>
        <td>${b.bookingId}</td>
        <td>${b.nights}</td>
        <td>${roomType}</td>
        <td>${b.guests} Guests</td>
        <td>${b.paid === 'paid' ? '<span class="status status--paid">paid</span>' : b.paid}</td>
        <td>${b.cost}</td>
        <td><div class="action-btns"><button class="icon-btn">✎</button><button class="icon-btn">🗑</button></div></td>
      `;
      tbody.appendChild(tr);
    });
  }

  function renderInvoices() {
    const tbody = $('#table-invoices tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    invoices.forEach(inv => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-weight:600">${inv.id}</td>
        <td>${inv.guest}</td>
        <td>${inv.date}</td>
        <td>${inv.amount}</td>
        <td>${inv.status}</td>
        <td class="t-right"><button class="icon-btn">⋯</button></td>
      `;
      tbody.appendChild(tr);
    });
  }

  function renderOrders() {
    const tbody = $('#table-orders tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    foodOrders.forEach(o => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-weight:600">${o.id}</td>
        <td>${o.guest}</td>
        <td>${o.room}</td>
        <td><div class="vstack">${o.items.map(i => `<span class="xsmall">${i}</span>`).join('')}</div></td>
        <td>${o.total}</td>
        <td>${o.status}</td>
        <td><button class="icon-btn">⋯</button></td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Calendar
  function renderCalendar() {
    const grid = $('#calendar-grid');
    if (!grid) return;
    const days = [
      'SU','MO','TU','WE','TH','FR','SA',
      '31','1','2','3','4','5','6',
      '7','8','9','10','11','12','13',
      '14','15','16','17','18','19','20',
      '21','22','23','24','25','26','27',
      '28','29','30','31','1','2','3'
    ];
    grid.innerHTML = '';
    days.forEach((d, idx) => {
      const cell = document.createElement('div');
      cell.className = 'day';
      if (idx < 7) { cell.style.fontWeight = '600'; }
      if (idx >= 35 && idx <= 41) cell.classList.add('day--muted');
      if (idx === 9 || idx === 11 + 1 || idx === 26) { /* rough markers */ }
      cell.textContent = d;
      if (d === '2' || d === '9' || d === '24') {
        const dot = document.createElement('span'); dot.className = 'dot'; cell.appendChild(dot);
      }
      grid.appendChild(cell);
    });

    const wrap = $('#calendar-events');
    if (!wrap) return;
    wrap.innerHTML = '';
    calendarEvents.forEach(e => {
      const row = document.createElement('div');
      row.className = 'row a-center gap-8';
      row.innerHTML = `
        <span class="avatar"></span>
        <div>
          <div class="small" style="font-weight:600">${e.guest}</div>
          <div class="xsmall muted">${e.nights} Nights | ${e.guests} Guests</div>
        </div>
      `;
      wrap.appendChild(row);
    });
  }

  function renderPieLegend() {
    const legend = $('#pie-legend');
    if (!legend) return;
    legend.innerHTML = '';
    foodOrdersData.forEach((entry, idx) => {
      const item = document.createElement('div');
      item.className = 'row a-center gap-8';
      item.innerHTML = `<span class="dot" style="background:${COLORS[idx % COLORS.length]}"></span><span class="xsmall">${entry.name}: ${entry.value}</span>`;
      legend.appendChild(item);
    });
  }

  // Tabs (Booking)
  function setupTabs() {
    $$('.tabs .tab').forEach(tab => {
      tab.addEventListener('click', () => {
        $$('.tabs .tab').forEach(t => t.classList.remove('is-active'));
        tab.classList.add('is-active');
        // No-op filter; you can implement filtering by tab value if needed
      });
    });
  }

  // Return to dashboard from Coming Soon
  function setupBackButton() {
    const btn = $('#backToDashboard');
    if (btn) btn.addEventListener('click', () => {
      showSection('dashboard');
      $$('.nav__item').forEach(b => {
        if (b.getAttribute('data-section') === 'dashboard') b.classList.add('is-active');
        else b.classList.remove('is-active');
      });
    });
  }

  // Mount
  window.addEventListener('DOMContentLoaded', () => {
    setupSidebar();
    setupTabs();
    setupBackButton();

    renderRevenue();
    renderGuestsLine();
    renderRooms();
    renderBookings();
    renderInvoices();
    renderOrders();
    renderCalendar();
    renderPieLegend();
  });
})();


