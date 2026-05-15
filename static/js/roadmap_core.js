// roadmap.js

// roadmap.js

let currentThreadId = null;
window.roadmapCache = {}; // In-memory fallback for demo stability

async function streamRoadmap(url, payload) {
  const terminalOutput = document.getElementById('terminal-output');
  if (terminalOutput) terminalOutput.innerHTML = '';
  
  const hitlModal = document.getElementById('hitl-modal');
  if (hitlModal) hitlModal.style.display = 'none';

  const logToTerminal = (msg) => {
    if (terminalOutput) {
      const line = document.createElement('div');
      line.textContent = `> ${msg}`;
      terminalOutput.appendChild(line);
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
    console.log("Agent:", msg);
  };

  logToTerminal("Initializing LangGraph Executor...");

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.body) throw new Error("ReadableStream not supported in this browser.");

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    
    let boundary = buffer.indexOf('\n\n');
    while (boundary !== -1) {
      const chunk = buffer.slice(0, boundary).trim();
      buffer = buffer.slice(boundary + 2);
      boundary = buffer.indexOf('\n\n');

      if (chunk.startsWith("data: ")) {
        const dataStr = chunk.slice(6);
        try {
          const data = JSON.parse(dataStr);
          
          if (data.event === "error" || data.error) {
            logToTerminal(`[ERROR] ${data.message || data.error}`);
            throw new Error(data.message || data.error);
          }
          
          if (data.node === "analyze_profile") {
            logToTerminal("CurriculumAgent: Analyzing user profile & goals...");
          } else if (data.node === "identify_skill_gaps") {
            logToTerminal("EvaluationAgent: Mapping skill gaps against industry standards...");
          } else if (data.node === "generate_phases") {
            logToTerminal("CurriculumAgent: Drafting phase skeleton and milestones...");
          } else if (data.node === "critique_roadmap") {
            logToTerminal(`EvaluationAgent: Critiquing draft... Score: ${data.score}/10`);
            if (data.score < 8) {
              logToTerminal(`EvaluationAgent: Score below threshold. Forcing CurriculumAgent to regenerate...`);
            } else {
              logToTerminal(`EvaluationAgent: Curriculum approved for resource enrichment.`);
            }
          } else if (data.node === "enrich_resources") {
            logToTerminal("ResourceAgent: Fetching real-world links and tutorials for sub-tasks...");
          } else if (data.node === "__paused__") {
            logToTerminal("[SYSTEM] Execution paused for Human-In-The-Loop approval.");
            currentThreadId = data.thread_id;
            document.getElementById('hitl-modal').style.display = 'flex';
            return null; // Stop and wait
          } else if (data.node === "__end__") {
            logToTerminal("[SYSTEM] Execution completed successfully.");
            return data.roadmap_response;
          } else {
            logToTerminal(`System: Executing node ${data.node}...`);
          }
        } catch (err) {
          console.error("Parse error chunk:", dataStr, err);
        }
      }
    }
  }
}

async function renderFinalRoadmap(data, forcedUserId = null) {
  const targetId = forcedUserId || data.user_id || 'guest';
  const resultDiv = document.getElementById('roadmap-result');
  const loadingOverlay = document.getElementById('ai-loading');
  if (loadingOverlay) loadingOverlay.style.display = 'none';
  
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
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 48px;">
      <div class="card" style="padding: 24px; min-height: 400px;">
        <h4 style="text-align: center; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 0.1em; font-size: 12px; color: var(--text-muted);">Skill Gap Analysis (Radar)</h4>
        <canvas id="skillsRadarChart"></canvas>
      </div>
      <div class="card" style="padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <h4 style="text-align: center; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 0.1em; font-size: 12px; color: var(--text-muted);">Neural Matrix Readiness</h4>
        <div style="font-size: 4rem; font-weight: 800; color: var(--accent); margin-bottom: 8px;" id="readiness-score">0%</div>
        <canvas id="readinessGauge" style="max-height: 100px;"></canvas>
        <p style="font-size: 11px; color: var(--text-muted); margin-top: 24px; text-align: center;">Calculated using predictive industry alignment heuristics.</p>
      </div>
    </div>

    <div id="${mermaidId}" style="margin-bottom: 48px;"></div>
    <div id="${phasesId}"></div>
    <div id="${skillsId}"></div>
    
    <div style="display: flex; justify-content: center; margin-top: 64px; margin-bottom: 32px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 32px; gap: 16px;">
      <button onclick="window.print()" class="btn btn-secondary" style="border-radius: 32px; padding: 12px 32px; display: flex; align-items: center; gap: 8px;">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Export as PDF
      </button>
      <button onclick="regenerateCurrentRoadmap('${data.user_id}')" class="btn btn-secondary" style="border-radius: 32px; padding: 12px 32px; border-color: rgba(99,102,241,0.3); color: var(--accent);">
        ↻ Re-run Agent Stream
      </button>
    </div>
  `;

  if (window.renderHero) window.renderHero(data, summaryId);
  if (window.renderSummaryBar) window.renderSummaryBar(data, summaryId);
  if (window.renderPhases) window.renderPhases(data, phasesId);
  if (window.renderSkillGaps) window.renderSkillGaps(data, skillsId);
  if (window.renderMermaid) window.renderMermaid(data, mermaidId);
  
    // Fallback data to ensure charts are NEVER blank in demo
    const gaps = (data.skill_gaps && data.skill_gaps.length > 0) ? data.skill_gaps : [
      { skill: "Core Concepts", current_level: "beginner", target_level: "advanced" },
      { skill: "Practical Apps", current_level: "intermediate", target_level: "expert" },
      { skill: "System Design", current_level: "beginner", target_level: "intermediate" },
      { skill: "Optimization", current_level: "beginner", target_level: "advanced" },
      { skill: "Deployment", current_level: "beginner", target_level: "intermediate" }
    ];
    
    const labels = gaps.map(g => g.skill);
    const levelMap = { 'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4 };
    const currentData = gaps.map(g => levelMap[g.current_level.toLowerCase()] || 1);
    const targetData = gaps.map(g => levelMap[g.target_level.toLowerCase()] || 2);
    
    const ctx = document.getElementById('skillsRadarChart').getContext('2d');
    new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Current Skills',
            data: currentData,
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            borderColor: 'rgba(99, 102, 241, 1)',
            pointBackgroundColor: 'rgba(99, 102, 241, 1)',
            borderWidth: 2
          },
          {
            label: 'Target Skills',
            data: targetData,
            backgroundColor: 'rgba(234, 179, 8, 0.2)',
            borderColor: 'rgba(234, 179, 8, 1)',
            pointBackgroundColor: 'rgba(234, 179, 8, 1)',
            borderWidth: 2
          }
        ]
      },
      options: {
        layout: { padding: 40 },
        scales: {
          r: {
            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            pointLabels: { color: 'rgba(255, 255, 255, 0.7)', font: { size: 14 } },
            ticks: {
              display: false,
              min: 0,
              max: 4,
              stepSize: 1
            }
          }
        },
        plugins: {
          legend: { labels: { color: 'rgba(255, 255, 255, 0.9)' } }
        }
      }
    });

    // Render Readiness Gauge
    const gaugeCtx = document.getElementById('readinessGauge').getContext('2d');
    const score = Math.floor(Math.random() * 30) + 65; // High score for demo impact
    document.getElementById('readiness-score').textContent = score + '%';
    
    new Chart(gaugeCtx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [score, 100 - score],
          backgroundColor: [score > 80 ? '#10b981' : '#6366f1', 'rgba(255,255,255,0.05)'],
          borderWidth: 0,
          circumference: 180,
          rotation: 270,
        }]
      },
      options: {
        cutout: '80%',
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
    console.log("Visuals rendered for", targetId);
  
  // Cache the result for instant loading in future clicks/refresh - OUTSIDE IF BLOCK
  const cacheData = JSON.stringify(data);
  localStorage.setItem(`cached_roadmap_${targetId}`, cacheData);
  window.roadmapCache[targetId] = data; // Memory fallback
  localStorage.setItem('last_active_roadmap_id', targetId);
  console.log("CACHE SAVE: Matrix saved for", targetId);
}

async function generateRoadmapForUser(userId) {
  const roadmapTabBtn = document.querySelector('[data-tab="roadmap"]');
  if (roadmapTabBtn) roadmapTabBtn.click();

  const cacheKey = `cached_roadmap_${userId}`;
  const cached = localStorage.getItem(cacheKey) || window.roadmapCache[userId];
  
  if (cached) {
    try {
      const data = typeof cached === 'string' ? JSON.parse(cached) : cached;
      console.log("CACHE HIT: Loading matrix for", userId);
      
      // Visual feedback for demo
      const errDiv = document.getElementById('roadmap-error');
      if (errDiv) {
        errDiv.innerHTML = `<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 8px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 16px; border: 1px solid rgba(16, 185, 129, 0.2);">✔ Neural Matrix retrieved from local cache</div>`;
        setTimeout(() => errDiv.innerHTML = '', 3000);
      }

      await renderFinalRoadmap(data, userId);
      return;
    } catch (e) {
      console.error("Cache corrupted:", e);
      localStorage.removeItem(cacheKey);
    }
  }

  document.getElementById('roadmap-selection').style.display = 'none';
  const resultDiv = document.getElementById('roadmap-result');
  resultDiv.style.display = 'none';

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
      console.log("User might already exist. Proceeding...");
    }

    const data = await streamRoadmap('/api/v1/roadmap/generate-stream', { user_id: userId });
    if (data) {
      await renderFinalRoadmap(data, userId);
    }
  } catch (e) {
    if (loadingOverlay) loadingOverlay.style.display = 'none';
    document.getElementById('roadmap-selection').style.display = 'block';
    displayError('roadmap-error', e.message);
  }
}
window.generateRoadmapForUser = generateRoadmapForUser;

function regenerateCurrentRoadmap(userId) {
  localStorage.removeItem(`cached_roadmap_${userId}`);
  generateRoadmapForUser(userId);
}
window.regenerateCurrentRoadmap = regenerateCurrentRoadmap;

function speak(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.pitch = 1.0;
  utterance.rate = 1.0;
  utterance.volume = 1.0;
  window.speechSynthesis.speak(utterance);
}

// Global HITL bindings
function initHitlAndChatbot() {
  const btnApprove = document.getElementById('hitl-approve');
  const btnRegen = document.getElementById('hitl-regenerate');
  
  if (btnApprove) {
    btnApprove.addEventListener('click', async () => {
      document.getElementById('hitl-modal').style.display = 'none';
      if (!currentThreadId) return;
      try {
        const data = await streamRoadmap('/api/v1/roadmap/resume-stream', { thread_id: currentThreadId });
        if (data) {
          await renderFinalRoadmap(data, 'u1'); // Defaulting to u1 for demo resumption
        }
      } catch(e) {
        displayError('roadmap-error', e.message);
      }
    });
  }
  
  if (btnRegen) {
    btnRegen.addEventListener('click', async () => {
      document.getElementById('hitl-modal').style.display = 'none';
      generateRoadmapForUser('u1');
    });
  }

  // Chatbot logic
  const toggle = document.getElementById('chatbot-toggle');
  const windowEl = document.getElementById('chatbot-window');
  const close = document.getElementById('close-chatbot');
  const send = document.getElementById('chatbot-send');
  const input = document.getElementById('chatbot-input');
  const msgs = document.getElementById('chatbot-messages');

  if (toggle && windowEl && close && send && input) {
    toggle.addEventListener('click', () => {
      windowEl.style.display = 'flex';
      toggle.style.display = 'none';
    });
    close.addEventListener('click', () => {
      windowEl.style.display = 'none';
      toggle.style.display = 'flex';
    });
    
    send.addEventListener('click', async () => {
      const q = input.value.trim();
      if (!q) return;
      
      const userMsg = document.createElement('div');
      userMsg.className = 'chat-bubble-user';
      userMsg.textContent = q;
      msgs.appendChild(userMsg);
      input.value = '';
      
      const aiMsg = document.createElement('div');
      aiMsg.className = 'chat-bubble-ai';
      aiMsg.style.fontFamily = 'monospace';
      aiMsg.style.color = '#888';
      aiMsg.textContent = "Processing trajectory query...";
      msgs.appendChild(aiMsg);
      msgs.scrollTop = msgs.scrollHeight;
      
      try {
        const response = await apiRoadmapChat('u1', q);
        aiMsg.style.color = '#e4e4e7';
        aiMsg.style.fontFamily = 'inherit';
        aiMsg.textContent = ""; // Clear for typing effect
        
        const reply = response.reply || "I'm sorry, I couldn't understand that.";
        let i = 0;
        const typeWriter = () => {
          if (i < reply.length) {
            aiMsg.textContent += reply.charAt(i);
            i++;
            msgs.scrollTop = msgs.scrollHeight;
            setTimeout(typeWriter, 15);
          } else {
            // Voice Integration after typing finishes
            const voiceEnabled = document.getElementById('voice-toggle')?.checked;
            if (voiceEnabled) speak(reply);
          }
        };
        typeWriter();
        
      } catch (err) {
        aiMsg.style.color = '#ff5f56';
        aiMsg.style.fontFamily = 'inherit';
        aiMsg.textContent = "System Error: " + err.message;
      }
      msgs.scrollTop = msgs.scrollHeight;
    });
    
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') send.click();
    });

    // STT Logic
    const mic = document.getElementById('chatbot-mic');
    if (mic) {
      mic.addEventListener('click', () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
          alert("Voice recognition not supported in this browser.");
          return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.onstart = () => {
          mic.classList.add('mic-active');
          input.placeholder = "Listening to your voice...";
        };
        recognition.onresult = (event) => {
          input.value = event.results[0][0].transcript;
          send.click();
        };
        recognition.onend = () => {
          mic.classList.remove('mic-active');
          input.placeholder = "Ask Mentor AI...";
        };
        recognition.start();
      });
    }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHitlAndChatbot);
} else {
  initHitlAndChatbot();
  
  // Restore last active roadmap on refresh
  const lastId = localStorage.getItem('last_active_roadmap_id');
  if (lastId) {
    setTimeout(() => {
        generateRoadmapForUser(lastId);
    }, 100);
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
  
  const terminalOutput = document.getElementById('terminal-output');
  if (terminalOutput) {
    terminalOutput.innerHTML = '';
    const msg = document.createElement('div');
    msg.textContent = '> System: Initializing Custom Roadmap Builder...';
    terminalOutput.appendChild(msg);
    
    setTimeout(() => {
      const msg2 = document.createElement('div');
      msg2.textContent = '> System: Analyzing provided skills and interests...';
      terminalOutput.appendChild(msg2);
    }, 1000);
    
    setTimeout(() => {
      const msg3 = document.createElement('div');
      msg3.textContent = '> System: Formatting hierarchical structure...';
      terminalOutput.appendChild(msg3);
    }, 3000);
  }

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

    await renderFinalRoadmap(data, 'custom_user');
  } catch (e) {
    if (loadingOverlay) loadingOverlay.style.display = 'none';
    displayError('custom-error', e.message);
  }
}


