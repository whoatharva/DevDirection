/**
 * user.js — User management & custom roadmap creation
 */

// ─── Custom Roadmap Form ───────────────────────────────────────────────────────

function loadExampleCustomRoadmap() {
  const fields = {
    'cr-title': 'AI Engineer Career Path',
    'cr-description': 'Comprehensive roadmap to become an AI/ML Engineer',
    'cr-goal': 'AI/ML Engineer',
    'cr-level': 'intermediate',
    'cr-skills': 'Python, Mathematics, Statistics',
    'cr-interests': 'Machine Learning, Deep Learning, NLP',
    'cr-time': 'full-time',
  };

  for (const [id, value] of Object.entries(fields)) {
    const el = document.getElementById(id);
    if (el) el.value = value;
  }
  showToast('Example data loaded!', 'success');
}

async function createCustomRoadmap() {
  const title = document.getElementById('cr-title')?.value;
  const description = document.getElementById('cr-description')?.value;
  const goal = document.getElementById('cr-goal')?.value;
  const level = document.getElementById('cr-level')?.value;
  const skills = document.getElementById('cr-skills')?.value;
  const interests = document.getElementById('cr-interests')?.value;
  const time = document.getElementById('cr-time')?.value;

  if (!title || !goal) {
    showToast('Please fill in at least Title and Target Goal', 'warning');
    return;
  }

  const userId = selectedUserId || 'guest_user';
  const roadmapData = {
    title,
    description: description || '',
    target_goal: goal,
    current_level: level || 'beginner',
    current_skills: skills ? skills.split(',').map(s => s.trim()) : [],
    interests: interests ? interests.split(',').map(s => s.trim()) : [],
    time_commitment: time || 'part-time',
    roadmap_type: 'custom',
  };

  const btn = document.getElementById('createCustomBtn');
  btn.disabled = true;
  btn.textContent = '⏳ Creating...';

  try {
    const result = await apiCreateCustomRoadmap(userId, roadmapData);
    showToast('Custom roadmap created!', 'success');

    // Switch to roadmap tab and display it
    currentRoadmapData = result;
    switchTab('roadmap');
    renderCustomRoadmapResult(result);
  } catch (err) {
    showToast(`Failed: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '🚀 Create Roadmap';
  }
}

function renderCustomRoadmapResult(data) {
  const phases = data.phases || [];
  let html = `
    <div class="roadmap-header">
      <h3>🎯 ${data.title || 'Custom Roadmap'}</h3>
      <div class="roadmap-stats">
        <div class="stat-item">
          <span class="stat-number">${phases.length}</span>
          <span class="stat-label">Phases</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${phases.reduce((t, p) => t + (p.milestones?.length || 0), 0)}</span>
          <span class="stat-label">Milestones</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${data.total_estimated_duration || 'N/A'}</span>
          <span class="stat-label">Duration</span>
        </div>
      </div>
    </div>

    <div class="detail-section">
      <h3>📊 Overview</h3>
      <p><strong>Description:</strong> ${data.description || 'N/A'}</p>
      <p><strong>Target:</strong> ${data.user_data?.target_goal || 'N/A'}</p>
    </div>
  `;

  phases.forEach((phase, pi) => {
    html += `
      <div class="phase-block">
        <h4>Phase ${pi + 1}: ${phase.name || phase.title || 'Untitled'}</h4>
        <p class="text-muted mb-md">${phase.description || ''}</p>
        ${(phase.milestones || []).map((m, mi) => `
          <div class="milestone-card" onclick="showMilestoneDetails('${m.id}', '${(m.title || '').replace(/'/g, "\\'")}')">
            <div class="title">${mi + 1}. ${m.title}</div>
            <div class="desc">${m.description || ''}</div>
            <div class="meta-tags">
              <span class="tag tag-duration">${m.estimated_duration || 'N/A'}</span>
              <span class="tag tag-type">${capitalize(m.type || 'learning')}</span>
              <span class="tag tag-difficulty">${capitalize(m.difficulty || 'beginner')}</span>
            </div>
            <div class="tag-click">ℹ️ Click for details</div>
          </div>
        `).join('')}
      </div>
    `;
  });

  const resultSection = document.getElementById('resultSection');
  resultSection.classList.remove('hidden');
  document.getElementById('resultContent').innerHTML = html;
}
