// roadmap.js

// roadmap.js

async function generateRoadmapForUser(userId) {
  const roadmapTabBtn = document.querySelector('[data-tab="roadmap"]');
  if (roadmapTabBtn) {
    roadmapTabBtn.click();
  }

  document.getElementById('roadmap-selection').style.display = 'none';
  const resultDiv = document.getElementById('roadmap-result');
  resultDiv.style.display = 'block';

  const loadingOverlay = document.getElementById('ai-loading');
  if (loadingOverlay) loadingOverlay.style.display = 'flex';

  clearError('roadmap-error');
  resultDiv.innerHTML = '';

  try {
    try {
      if (typeof apiCreateUser === 'function') {
        await apiCreateUser({
          user_id: userId,
          name: "Generated User",
          education: "Not specified",
          skills: [],
          interests: [],
          career_goals: [],
          experience_level: "beginner",
          preferred_learning_style: "practical",
          time_commitment: "Flexible"
        });
      }
    } catch (e) {
      console.log("User might already exist. Proceeding...", e.message);
    }

    const data = await apiGenerateRoadmap(userId);
    if (loadingOverlay) loadingOverlay.style.display = 'none';
    
    console.log("Full Roadmap API Response:", data);
    
    resultDiv.classList.remove('hidden', 'd-none');
    resultDiv.style.display = 'block';
    const rTab = document.querySelector('[data-tab="roadmap"]');
    if (rTab) rTab.click();

    const summaryId = 'roadmap-summary-container';
    const phasesId = 'roadmap-phases-container';
    const skillsId = 'roadmap-skills-container';
    const mermaidId = 'roadmap-mermaid-container';

    resultDiv.innerHTML = `
      <div id="${summaryId}"></div>
      <div id="${mermaidId}" style="margin-bottom: 48px;"></div>
      <div id="${phasesId}"></div>
      <div id="${skillsId}"></div>
    `;

    if (window.renderHero) window.renderHero(data, summaryId);
    if (window.renderSummaryBar) window.renderSummaryBar(data, summaryId);
    if (window.renderPhases) window.renderPhases(data, phasesId);
    if (window.renderSkillGaps) window.renderSkillGaps(data, skillsId);
    if (window.renderMermaid) window.renderMermaid(data, mermaidId);
  } catch (e) {
    if (loadingOverlay) loadingOverlay.style.display = 'none';
    document.getElementById('roadmap-selection').style.display = 'block';
    resultDiv.style.display = 'none';
    displayError('roadmap-error', e.message);
  }
}

async function generateCustomRoadmap() {
  clearError('custom-error');

  const goal = document.getElementById('cr-goal').value;
  const level = document.getElementById('cr-level').value;
  const skillsStr = document.getElementById('cr-skills').value;
  const interestsStr = document.getElementById('cr-interests')?.value || '';
  const timeCommitment = document.getElementById('cr-time')?.value || '5 hours per week';
  const styleEl = document.getElementById('cr-style');
  const style = styleEl ? styleEl.value : 'practical';

  if (!goal) {
    displayError('custom-error', 'Target goal is required');
    return;
  }

  const skills = skillsStr.split(',').map(s => s.trim()).filter(s => s);
  const interests = interestsStr.split(',').map(s => s.trim()).filter(s => s);

  const loadingOverlay = document.getElementById('ai-loading');
  if (loadingOverlay) loadingOverlay.style.display = 'flex';

  try {
    const data = await apiCreateCustomRoadmap('u1', {
      target_role: goal,
      current_level: level,
      skills: skills,
      interests: interests,
      time_commitment: timeCommitment,
      learning_style: style
    });

    if (loadingOverlay) loadingOverlay.style.display = 'none';

    document.querySelector('[data-tab="roadmap"]').click();
    document.getElementById('roadmap-selection').style.display = 'none';
    const resultDiv = document.getElementById('roadmap-result');
    resultDiv.style.display = 'block';

    const customHeader = `
        <div class="card custom-roadmap-header">
            <h3>Custom Roadmap Generated</h3>
            <div class="cr-details">
                <span style="font-weight: 600;">Goal:</span> ${goal} &nbsp;|&nbsp; 
                <span style="font-weight: 600;">Level:</span> ${level} &nbsp;|&nbsp; 
                <span style="font-weight: 600;">Style:</span> ${style} &nbsp;|&nbsp; 
                <span style="font-weight: 600;">Skills:</span> ${skills.join(', ')}
            </div>
        </div>
    `;

    resultDiv.innerHTML = customHeader + '<div id="cr-inner-result"></div>';
    renderRoadmap(data, document.getElementById('cr-inner-result'));
  } catch (e) {
    if (loadingOverlay) loadingOverlay.style.display = 'none';
    displayError('custom-error', e.message);
  }
}

function renderRoadmap(data, container) {
  if (!data) return;

  const summaryId = 'roadmap-summary-container';
  const phasesId = 'roadmap-phases-container';
  const skillsId = 'roadmap-skills-container';
  const mermaidId = 'roadmap-mermaid-container';

  container.innerHTML = `
    <div id="${summaryId}"></div>
    <div id="${mermaidId}" style="margin-bottom: 48px;"></div>
    <div id="${phasesId}"></div>
    <div id="${skillsId}"></div>
  `;

  if (window.renderHero) window.renderHero(data, summaryId);
  if (window.renderSummaryBar) window.renderSummaryBar(data, summaryId);
  if (window.renderPhases) window.renderPhases(data, phasesId);
  if (window.renderSkillGaps) window.renderSkillGaps(data, skillsId);
  if (window.renderMermaid) window.renderMermaid(data, mermaidId);
}
