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
    currentQuestionIndex = 0;
    userAnswers = [];
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
        <div class="quiz-container">
            <div class="quiz-meta">Question ${currentQuestionIndex + 1} of ${quizQuestions.length}</div>
            <div class="quiz-question">${q.text}</div>
            <div class="quiz-options">
                ${q.options.map((opt, i) => `
                    <button class="option-btn" onclick="selectQuizOption(this, '${q.id}', '${typeof opt.score !== "undefined" ? opt.score : i}')">
                        ${opt.text || opt}
                    </button>
                `).join('')}
            </div>
        </div>
    `;

  content.innerHTML = html;
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

  setTimeout(() => {
    nextQuestion();
  }, 300);
}

function nextQuestion() {
  currentQuestionIndex++;
  renderQuestion();
}

async function submitQuiz() {
  document.getElementById('quiz-progress').style.width = `100%`;
  const content = document.getElementById('quiz-content');
  if (typeof showSkeleton === 'function') showSkeleton('quiz-content');

  try {
    const formattedAnswers = userAnswers.map(a => ({ qid: a.qid, score: parseInt(a.value) || 3 }));
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
