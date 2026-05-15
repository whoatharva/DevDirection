// quiz.js
let quizQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let currentUserId = 'guest';

function normaliseQuestion(q) {
  let opts = q.options || q.choices || [];
  opts = opts.map((o, i) => {
    if (typeof o === 'string') {
      // Extract leading number from strings like "0 = No", "1 = Somewhat"
      const match = o.match(/^(\d+)\s*[=\-:]\s*(.+)/)
      if (match) {
        return { text: match[2].trim(), score: parseInt(match[1]) }
      }
      return { text: o, score: i }
    }
    return o
  })
  return { ...q, options: opts }
}

async function startQuiz() {
  let userId = localStorage.getItem('career_user_id');
  if (!userId) {
    userId = 'user_' + Date.now();
    localStorage.setItem('career_user_id', userId);
    
    // Auto-register user asynchronously immediately so it exists for roadmap generation
    try {
      await fetch('/api/v1/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: userId,
          name: "Quiz User",
          education: "Not specified",
          skills: [],
          interests: [],
          career_goals: [],
          time_commitment: "part-time",
          learning_style: "mixed"
        })
      });
    } catch(e) {
       // if it fails or returns 400 'already exists', ignore and continue safely.
    }
  }
  currentUserId = userId;
  
  document.getElementById('quiz-intro').style.display = 'none';
  const content = document.getElementById('quiz-content');
  content.style.display = 'block';

  document.getElementById('quiz-progress-container').style.display = 'block';
  if (typeof showSkeleton === 'function') showSkeleton('quiz-content');

  try {
    const rawQuestions = await apiGetQuestions();
    quizQuestions = rawQuestions.map(normaliseQuestion);
    
    const savedProgress = localStorage.getItem('quiz_progress');
    if (savedProgress) {
      try {
        userAnswers = JSON.parse(savedProgress);
        currentQuestionIndex = Math.min(userAnswers.length, quizQuestions.length - 1);
      } catch(e) {
        userAnswers = [];
        currentQuestionIndex = 0;
      }
    } else {
      userAnswers = [];
      currentQuestionIndex = 0;
    }
    
    renderQuestion();
  } catch (e) {
    content.innerHTML = `<div class="error-banner">${e.message}</div>`;
  }
}

function renderQuestion() {
  if (currentQuestionIndex >= quizQuestions.length) {
    submitQuiz();
    return;
  }

  const q = quizQuestions[currentQuestionIndex];
  const progressPct = (currentQuestionIndex / quizQuestions.length) * 100;
  document.getElementById('quiz-progress').style.width = `${progressPct}%`;
  const content = document.getElementById('quiz-content');

  if (!q.options || q.options.length === 0) {
      content.innerHTML = `<div class="error-banner">Invalid question format: missing options.</div>`;
      return;
  }

  let html = `
        <div style="position: relative; min-height: 70vh; display: flex; flex-direction: column; justify-content: center;">
            <!-- Abstract tech badges securely inside bounds -->
            <div class="desktop-only" style="position: absolute; left: 0; top: 25%; opacity: 0.9; transform: rotate(-5deg); pointer-events: none;">
              <span class="tag" style="font-size: 14px; padding: 8px 16px; background: rgba(99, 102, 241, 0.1); color: #818cf8; border-color: rgba(99, 102, 241, 0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.1);">Algorithms</span>
            </div>
            <div class="desktop-only" style="position: absolute; left: 5%; bottom: 25%; opacity: 0.7; transform: rotate(8deg); pointer-events: none;">
              <span class="tag" style="font-size: 13px; padding: 6px 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">API Design</span>
            </div>
            <div class="desktop-only" style="position: absolute; right: 0; top: 30%; opacity: 0.9; transform: rotate(6deg); pointer-events: none;">
              <span class="tag" style="font-size: 14px; padding: 8px 16px; background: rgba(16, 185, 129, 0.1); color: #34d399; border-color: rgba(16, 185, 129, 0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.1);">Cloud Ops</span>
            </div>
            <div class="desktop-only" style="position: absolute; right: 5%; bottom: 20%; opacity: 0.6; transform: rotate(-6deg); pointer-events: none;">
              <span class="tag" style="font-size: 13px; padding: 6px 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">Databases</span>
            </div>

            <div class="quiz-container" style="animation: fadeIn 0.3s ease-in-out; text-align: center; position: relative; z-index: 2; background: rgba(24, 24, 27, 0.6); padding: 48px 32px; border-radius: 24px; border: 1px solid var(--border); box-shadow: 0 8px 32px rgba(0,0,0,0.2); backdrop-filter: blur(12px);">
                <div class="quiz-meta" style="margin-bottom: 16px; font-weight: 500;">Question ${currentQuestionIndex + 1} of ${quizQuestions.length}</div>
                <div class="quiz-question" style="font-size: 2rem; line-height: 1.4; margin-bottom: 40px; max-width: 700px; margin-left: auto; margin-right: auto;">${q.text}</div>
                
                <div class="quiz-options" style="max-width: 500px; width: 100%; margin: 0 auto;">
                    ${q.options.map((opt, i) => `
                        <button class="option-btn" style="text-align: center; padding: 16px 24px; font-size: 1.1rem; border-radius: 12px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03);" onclick="selectQuizOption(this, '${q.id || q.qid}', '${typeof opt.score !== "undefined" ? opt.score : i}')">
                            ${opt.text || opt}
                        </button>
                    `).join('')}
                </div>
                
                ${currentQuestionIndex > 0 ? `
                <div class="quiz-footer" style="justify-content: center; margin-top: 32px; display: flex;">
                    <button class="btn btn-secondary visible" style="border-radius: 32px; padding: 10px 24px;" onclick="prevQuestion()">← Back</button>
                </div>
                ` : '<div style="height: 60px;"></div>'}
            </div>
        </div>
    `;

  content.innerHTML = html;
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    renderQuestion();
  }
}

function selectQuizOption(btn, qId, value) {
  const parent = btn.parentElement;
  parent.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');

  const existing = userAnswers.find(a => a.qid === qId);
  if (existing) {
    existing.value = value;
  } else {
    userAnswers.push({ qid: qId, value: value });
  }

  localStorage.setItem('quiz_progress', JSON.stringify(userAnswers));

  setTimeout(() => {
    nextQuestion();
  }, 400); // slightly longer delay for smooth feeling
}

function nextQuestion() {
  currentQuestionIndex++;
  renderQuestion();
}

async function submitQuiz() {
  document.getElementById('quiz-progress').style.width = `100%`;
  const content = document.getElementById('quiz-content');
  if (typeof showSkeleton === 'function') showSkeleton('quiz-content');

  localStorage.removeItem('quiz_progress');

  try {
    const formattedAnswers = userAnswers.map(a => {
      let s = parseInt(a.value);
      return { qid: a.qid, score: isNaN(s) ? 3 : s };
    });
    const result = await apiSubmitQuiz(currentUserId, formattedAnswers);
    
    // Save userId back to localStorage after successful submit
    localStorage.setItem('career_user_id', currentUserId);

    let html = `
            <div class="quiz-container">
                <div class="page-header">
                    <h2>Quiz Completed!</h2>
                    <p>Here are your results across key competencies:</p>
                </div>
                
                <div class="results-chart">
        `;

    for (const [category, score] of Object.entries(result.scores || {})) {
      // Direct assignment as the API already calculates out of 100 via the backend fixes.
      const pct = Math.min(100, Math.max(0, Math.round(parseFloat(score) || 0)));
      html += `
                <div class="chart-row">
                    <div class="chart-label">${category.charAt(0).toUpperCase() + category.slice(1)}</div>
                    <div class="chart-bar-wrapper">
                        <div class="chart-bar-fill" style="width: 0%; transition: width 0.8s ease-out;" data-width="${pct}%"></div>
                    </div>
                    <div class="chart-pct">${pct}%</div>
                </div>
            `;
    }

    html += `
                </div>
                <div class="quiz-footer-actions">
                    <button class="btn btn-secondary" onclick="document.querySelector('.nav-tab[data-tab=\\'roadmap\\']').click()">Back to Dashboard</button>
                    <button class="btn btn-primary" onclick="handleGenerateMyRoadmap()">Generate My Roadmap →</button>
                </div>
            </div>
        `;

    content.innerHTML = html;

    setTimeout(() => {
      content.querySelectorAll('.chart-bar-fill').forEach(bar => {
        bar.style.width = bar.getAttribute('data-width');
      });
    }, 50);

  } catch (e) {
    content.innerHTML = `<div class="error-banner">${e.message}</div>`;
  }
}

async function handleGenerateMyRoadmap() {
    document.querySelector('.nav-tab[data-tab="roadmap"]').click();
    if (typeof generateRoadmapForUser === 'function') {
        await generateRoadmapForUser(currentUserId);
    }
}
