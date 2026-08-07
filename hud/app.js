// E.D.I.T.H. Tactical HUD & 3D Holographic Arc Reactor Core

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  init3DOrb('orb-3d-canvas-container', 120, 120);
  init3DOrb('hud-3d-container', 320, 320);
  simulateTelemetry();
});

// Clock Display
function initClock() {
  const clockEl = document.getElementById('clock-display');
  function updateTime() {
    const now = new Date();
    const utcStr = now.toISOString().substring(11, 19) + ' UTC';
    if (clockEl) clockEl.textContent = utcStr;
  }
  updateTime();
  setInterval(updateTime, 1000);
}

// View Switching
function switchView(viewName) {
  const orbWidget = document.getElementById('floating-orb-widget');
  const fullHud = document.getElementById('full-hud-view');
  
  if (viewName === 'floating') {
    document.body.classList.add('mode-floating');
    if (orbWidget) orbWidget.classList.remove('hidden');
    if (fullHud) fullHud.classList.add('hidden');
  } else {
    document.body.classList.remove('mode-floating');
    if (orbWidget) orbWidget.classList.add('hidden');
    if (fullHud) fullHud.classList.remove('hidden');
  }
}

function toggleExpandOrb(event) {
  if (event) event.stopPropagation();
  const expandedCard = document.getElementById('orb-expanded-card');
  if (expandedCard) {
    expandedCard.classList.toggle('hidden');
  }
}

// Three.js 3D Holographic Arc Reactor Orb Renderer
function init3DOrb(containerId, width, height) {
  const container = document.getElementById(containerId);
  if (!container || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.z = 4.5;

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Outer Wireframe Sphere
  const outerGeo = new THREE.IcosahedronGeometry(1.6, 2);
  const outerMat = new THREE.MeshBasicMaterial({
    color: 0x00f0ff,
    wireframe: true,
    transparent: true,
    opacity: 0.45
  });
  const outerSphere = new THREE.Mesh(outerGeo, outerMat);
  scene.add(outerSphere);

  // Middle Wireframe Shell
  const midGeo = new THREE.IcosahedronGeometry(1.2, 1);
  const midMat = new THREE.MeshBasicMaterial({
    color: 0x0051ff,
    wireframe: true,
    transparent: true,
    opacity: 0.6
  });
  const midSphere = new THREE.Mesh(midGeo, midMat);
  scene.add(midSphere);

  // Inner Core Glowing Sphere
  const coreGeo = new THREE.SphereGeometry(0.65, 32, 32);
  const coreMat = new THREE.MeshBasicMaterial({
    color: 0x00f0ff,
    transparent: true,
    opacity: 0.85
  });
  const coreMesh = new THREE.Mesh(coreGeo, coreMat);
  scene.add(coreMesh);

  // Orbiting Particle Ring
  const particleCount = 120;
  const particleGeo = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount; i++) {
    const angle = (i / particleCount) * Math.PI * 2;
    const radius = 2.0 + (Math.random() - 0.5) * 0.3;
    positions[i * 3] = Math.cos(angle) * radius;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 0.4;
    positions[i * 3 + 2] = Math.sin(angle) * radius;
  }

  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const particleMat = new THREE.PointsMaterial({
    color: 0x00f0ff,
    size: 0.05,
    transparent: true,
    opacity: 0.8
  });
  const particleRing = new THREE.Points(particleGeo, particleMat);
  scene.add(particleRing);

  // Animation Loop
  let time = 0;
  function animate() {
    requestAnimationFrame(animate);
    time += 0.02;

    outerSphere.rotation.x += 0.005;
    outerSphere.rotation.y += 0.008;

    midSphere.rotation.x -= 0.008;
    midSphere.rotation.y -= 0.012;

    particleRing.rotation.y += 0.01;

    const scale = 1.0 + Math.sin(time * 3) * 0.08;
    coreMesh.scale.set(scale, scale, scale);

    renderer.render(scene, camera);
  }

  animate();
}

// Telemetry Simulator & Orb Sync
function simulateTelemetry() {
  const cpuValEl = document.getElementById('cpu-val');
  const ramValEl = document.getElementById('ram-val');
  const orbCpu = document.getElementById('orb-cpu');
  const orbRam = document.getElementById('orb-ram');
  const orbNet = document.getElementById('orb-net');
  const cpuCircle = document.getElementById('cpu-circle');
  const ramCircle = document.getElementById('ram-circle');
  const netBar = document.getElementById('net-bar');
  const netText = document.getElementById('net-text');

  setInterval(() => {
    const cpu = Math.floor(18 + Math.random() * 25);
    const ram = Math.floor(40 + Math.random() * 8);
    const net = Math.floor(45 + Math.random() * 40);

    if (cpuValEl) cpuValEl.textContent = cpu + '%';
    if (ramValEl) ramValEl.textContent = ram + '%';
    if (orbCpu) orbCpu.textContent = cpu + '%';
    if (orbRam) orbRam.textContent = ram + '%';
    if (orbNet) orbNet.textContent = net + ' MB/s';
    if (netText) netText.textContent = net + ' MB/s';

    if (cpuCircle) cpuCircle.style.strokeDashoffset = 251 - (251 * cpu) / 100;
    if (ramCircle) ramCircle.style.strokeDashoffset = 251 - (251 * ram) / 100;
    if (netBar) netBar.style.width = Math.min(100, net * 1.2) + '%';
  }, 2500);
}

function appendLog(category, text) {
  const logContainer = document.getElementById('terminal-log');
  const orbLog = document.getElementById('orb-log');

  if (orbLog) orbLog.textContent = `[${category.toUpperCase()}] ${text}`;

  if (logContainer) {
    const entry = document.createElement('div');
    entry.className = `log-entry ${category.toLowerCase()}`;
    entry.textContent = `[${category.toUpperCase()}] ${text}`;
    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;
  }
}

function clearTerminal() {
  const logContainer = document.getElementById('terminal-log');
  if (logContainer) logContainer.innerHTML = '';
}

function triggerProtocol(protocolName) {
  const titles = {
    edith: "PROTOCOL E.D.I.T.H.",
    sentry: "PROTOCOL SENTRY",
    stealth: "PROTOCOL STEALTH",
    house_party: "PROTOCOL HOUSE PARTY",
    overclock: "PROTOCOL OVERCLOCK",
    lockdown: "PROTOCOL LOCKDOWN"
  };

  const name = titles[protocolName] || protocolName.toUpperCase();
  appendLog('user', `Initiating command: ${name}`);

  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.run_protocol(protocolName).then(res => appendLog('edith', res));
  } else {
    setTimeout(() => {
      appendLog('edith', `Command Confirmed: ${name} active. All defensive subsystems aligned, boss.`);
    }, 400);
  }
}

function handleOrbInput(event) {
  if (event.key === 'Enter') submitOrbCommand();
}

function submitOrbCommand() {
  const input = document.getElementById('orb-input');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;
  input.value = '';
  processCommand(val);
}

function handleInput(event) {
  if (event.key === 'Enter') submitCommand();
}

function submitCommand() {
  const input = document.getElementById('cmd-input');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;
  input.value = '';
  processCommand(val);
}

function processCommand(val) {
  appendLog('user', val);

  if (window.pywebview && window.pywebview.api) {
    const lower = val.toLowerCase();
    if (lower.includes('telemetry') || lower.includes('system') || lower.includes('diagnostic')) {
      window.pywebview.api.get_telemetry().then(res => appendLog('edith', res));
    } else if (lower.includes('search') || lower.includes('web') || lower.includes('news')) {
      window.pywebview.api.web_search(val).then(res => appendLog('edith', res));
    } else {
      window.pywebview.api.run_protocol(val).then(res => appendLog('edith', res));
    }
  } else {
    setTimeout(() => {
      const lower = val.toLowerCase();
      if (lower.includes('diagnostic') || lower.includes('telemetry') || lower.includes('status')) {
        appendLog('edith', 'Telemetry check complete. CPU at 24% capacity, Memory nominal, storage 62% available.');
      } else if (lower.includes('news') || lower.includes('world')) {
        appendLog('edith', 'Fetching global headline feeds... World news summary ready on feed monitor.');
      } else {
        appendLog('edith', `Acknowledged command: "${val}". Processing via E.D.I.T.H. neural matrix...`);
      }
    }, 500);
  }
}
