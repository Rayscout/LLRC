// 粒子 Logo 动效（改写自 v0 参考示例，去除 React 依赖，适配原生 JS）
(function () {
	const AWS_LOGO_PATH = "M86 66l2 9c0 3 1 5 3 8v2l-1 3-7 4-2 1-3-1-4-5-3-6c-8 9-18 14-29 14-9 0-16-3-20-8-5-4-8-11-8-19s3-15 9-20c6-6 14-8 25-8a79 79 0 0 1 22 3v-7c0-8-2-13-5-16-3-4-8-5-16-5l-11 1a80 80 0 0 0-14 5h-2c-1 0-2-1-2-3v-5l1-3c0-1 1-2 3-2l12-5 16-2c12 0 20 3 26 8 5 6 8 14 8 25v32zM46 82l10-2c4-1 7-4 10-7l3-6 1-9v-4a84 84 0 0 0-19-2c-6 0-11 1-15 4-3 2-4 6-4 11s1 8 3 11c3 2 6 4 11 4zm80 10-4-1-2-3-23-78-1-4 2-2h10l4 1 2 4 17 66 15-66 2-4 4-1h8l4 1 2 4 16 67 17-67 2-4 4-1h9c2 0 3 1 3 2v2l-1 2-24 78-2 4-4 1h-9l-4-1-1-4-16-65-15 64-2 4-4 1h-9zm129 3a66 66 0 0 1-27-6l-3-3-1-2v-5c0-2 1-3 2-3h2l3 1a54 54 0 0 0 23 5c6 0 11-2 14-4 4-2 5-5 5-9l-2-7-10-5-15-5c-7-2-13-6-16-10a24 24 0 0 1 5-34l10-5a44 44 0 0 1 20-2 110 110 0 0 1 12 3l4 2 3 2 1 4v4c0 3-1 4-2 4l-4-2c-6-2-12-3-19-3-6 0-11 0-14 2s-4 5-4 9c0 3 1 5 3 7s5 4 11 6l14 4c7 3 12 6 15 10s5 9 5 14l-3 12-7 8c-3 3-7 5-11 6l-14 2z M274 144A220 220 0 0 1 4 124c-4-3-1-6 2-4a300 300 0 0 0 263 16c5-2 10 4 5 8z M287 128c-4-5-28-3-38-1-4 0-4-3-1-5 19-13 50-9 53-5 4 5-1 36-18 51-3 2-6 1-5-2 5-10 13-33 9-38z";

	function initParticles() {
		const canvas = document.getElementById('bg-particles');
		if (!canvas) return;
		const ctx = canvas.getContext('2d');
		if (!ctx) return;

		const mouse = { x: 0, y: 0 };
		let isTouching = false;
		let isMobile = false;
		let particles = [];
		let textImageData = null;
		let animationId = 0;

		function updateCanvasSize() {
			canvas.width = window.innerWidth;
			canvas.height = window.innerHeight;
			isMobile = window.innerWidth < 768;
		}

		function drawLogosAndGetScale() {
			if (!ctx) return 1;
			ctx.save();
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			ctx.fillStyle = 'white';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'middle';

			// 三行文本，随屏幕自适应
			const isSmall = canvas.width < 768;
			const title1 = 'RucRut · 智能招聘系统';
			const title2 = '欢迎使用智能招聘平台';
			const subtitle = '发布岗位、投递简历、AI 生成面试题与反馈，一站式完成招聘流程。';

			// 自适应字号并放大主标题，增强清晰度
			const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
			const size1 = clamp(canvas.width * 0.02, 16, 28);
			const size2 = clamp(canvas.width * 0.085, 40, 120); // 放大
			const size3 = clamp(canvas.width * 0.022, 14, 24);
			const lineGap = isSmall ? 16 : 22;

			const totalHeight = size1 + size2 + size3 + lineGap * 2;
			let cy = canvas.height / 2 - totalHeight / 2;

			ctx.font = `600 ${size1}px system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', Arial`;
			ctx.lineWidth = isSmall ? 1.2 : 2.0; ctx.strokeStyle = 'white';
			ctx.strokeText(title1, canvas.width / 2, cy + size1 / 2);
			ctx.fillText(title1, canvas.width / 2, cy + size1 / 2);
			cy += size1 + lineGap;

			ctx.font = `800 ${size2}px system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', Arial`;
			ctx.strokeText(title2, canvas.width / 2, cy + size2 / 2);
			ctx.fillText(title2, canvas.width / 2, cy + size2 / 2);
			cy += size2 + lineGap;

			ctx.font = `500 ${size3}px system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', Arial`;
			ctx.strokeText(subtitle, canvas.width / 2, cy + size3 / 2);
			ctx.fillText(subtitle, canvas.width / 2, cy + size3 / 2);

			textImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			ctx.restore();
			return 1;
		}

		function createParticle(scale) {
			if (!ctx || !canvas || !textImageData) return null;
			const data = textImageData.data;
			for (let attempt = 0; attempt < 100; attempt++) {
				const x = Math.floor(Math.random() * canvas.width);
				const y = Math.floor(Math.random() * canvas.height);
				if (data[(y * canvas.width + x) * 4 + 3] > 128) {
					// 对于文本，统一散射颜色
					const isAWSLogo = false;
					return {
						x,
						y,
						baseX: x,
						baseY: y,
						size: Math.random() * 0.9 + 1.1,
						color: 'white',
						scatteredColor: '#FF9900',
						isAWS: isAWSLogo,
						life: Math.random() * 100 + 50,
					};
				}
			}
			return null;
		}

		function createInitialParticles(scale) {
			const baseParticleCount = 11000; // 增加粒子基数提高清晰度
			const factor = Math.sqrt((canvas.width * canvas.height) / (1920 * 1080));
			const count = Math.floor(baseParticleCount * factor);
			for (let i = 0; i < count; i++) {
				const p = createParticle(scale);
				if (p) particles.push(p);
			}
		}

		function animate(scale) {
			if (!ctx || !canvas) return;
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			ctx.fillStyle = 'black';
			ctx.fillRect(0, 0, canvas.width, canvas.height);

			const maxDistance = 240;
			for (let i = 0; i < particles.length; i++) {
				const p = particles[i];
				const dx = mouse.x - p.x;
				const dy = mouse.y - p.y;
				const dist = Math.sqrt(dx * dx + dy * dy);
				if (dist < maxDistance && (isTouching || !('ontouchstart' in window))) {
					const force = (maxDistance - dist) / maxDistance;
					const angle = Math.atan2(dy, dx);
					p.x = p.baseX - Math.cos(angle) * force * 60;
					p.y = p.baseY - Math.sin(angle) * force * 60;
					ctx.fillStyle = p.scatteredColor;
				} else {
					p.x += (p.baseX - p.x) * 0.1;
					p.y += (p.baseY - p.y) * 0.1;
					ctx.fillStyle = 'white';
				}
				ctx.fillRect(p.x, p.y, p.size, p.size);
				p.life--;
				if (p.life <= 0) {
					const np = createParticle(scale);
					if (np) {
						particles[i] = np;
					} else {
						particles.splice(i, 1);
						i--;
					}
				}
			}
			const base = 7000;
			const target = Math.floor(base * Math.sqrt((canvas.width * canvas.height) / (1920 * 1080)));
			while (particles.length < target) {
				const np = createParticle(scale);
				if (np) particles.push(np);
			}
			animationId = requestAnimationFrame(() => animate(scale));
		}

		function resetAndRedraw() {
			updateCanvasSize();
			const scale = drawLogosAndGetScale();
			particles = [];
			createInitialParticles(scale);
			cancelAnimationFrame(animationId);
			animate(scale);
		}

		// 初始化
		updateCanvasSize();
		const scale = drawLogosAndGetScale();
		createInitialParticles(scale);
		animate(scale);

		// 事件绑定（改为 window 级别，避免被前景元素遮挡鼠标/触控事件）
		window.addEventListener('resize', resetAndRedraw);
		window.addEventListener('mousemove', (e) => {
			mouse.x = e.clientX;
			mouse.y = e.clientY;
		});
		window.addEventListener('mouseout', (e) => {
			if (!('ontouchstart' in window) && (!e.relatedTarget || e.relatedTarget.nodeName === 'HTML')) {
				mouse.x = 0; mouse.y = 0;
			}
		});
		window.addEventListener('touchstart', () => { isTouching = true; }, { passive: true });
		window.addEventListener('touchend', () => { isTouching = false; mouse.x = 0; mouse.y = 0; }, { passive: true });
		window.addEventListener('touchmove', (e) => {
			if (e.touches && e.touches.length > 0) {
				e.preventDefault();
				mouse.x = e.touches[0].clientX;
				mouse.y = e.touches[0].clientY;
			}
		}, { passive: false });
	}

	document.addEventListener('DOMContentLoaded', () => {
		// 仅在登录页加载：需要有 id=bg-particles 的 canvas
		if (!document.getElementById('bg-particles')) {
			const c = document.createElement('canvas');
			c.id = 'bg-particles';
			c.style.position = 'fixed';
			c.style.top = '0';
			c.style.left = '0';
			c.style.width = '100%';
			c.style.height = '100%';
			c.style.zIndex = '-1';
			document.body.appendChild(c);
		}
		initParticles();
	});
})();


