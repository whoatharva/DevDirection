// ui.js
document.addEventListener('DOMContentLoaded', () => {
  // Tab switching
  const tabs = document.querySelectorAll('.nav-tab');
  const panels = document.querySelectorAll('.tab-panel');

  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      // Remove active classes
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.style.display = 'none');

      // Add active to clicked
      tab.classList.add('active');
      const targetId = `tab-${tab.getAttribute('data-tab')}`;
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.style.display = 'block';
      } else {
        const errorPanel = document.getElementById('tab-404');
        if (errorPanel) errorPanel.style.display = 'block';
      }

      // Close mobile menu if open
      const navLinks = document.querySelector('.nav-links');
      if (navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
      }
    });
  });

  // Handle modal closes if you use modals later
});

function displayError(containerId, message) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="error-banner">${message}</div>`;
  el.style.display = 'block';
}

function clearError(containerId) {
  const el = document.getElementById(containerId);
  if (el) {
    el.innerHTML = '';
    el.style.display = 'none';
  }
}

function showSkeleton(containerId) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.style.display = 'block';
  el.innerHTML = `
        <div class="skeleton" style="width: 40%; height: 32px; margin-bottom: 24px;"></div>
        <div class="skeleton" style="width: 100%; height: 16px;"></div>
        <div class="skeleton" style="width: 90%; height: 16px;"></div>
        <div class="skeleton" style="width: 95%; height: 16px; margin-bottom: 32px;"></div>
        <div class="skeleton" style="width: 100%; height: 200px;"></div>
    `;
}
