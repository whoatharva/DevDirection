/**
 * api.js — Centralized API client
 * All backend communication goes through here.
 */

const API = '/api/v1';

async function apiFetch(path, options = {}) {
  const url = `${API}${path}`;
  const defaults = {
    headers: { 'Content-Type': 'application/json' },
  };
  const config = { ...defaults, ...options };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);
  config.signal = controller.signal;

  try {
    const res = await fetch(url, config);
    clearTimeout(timeout);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      if (res.status === 400 && err.detail && err.detail.toLowerCase().includes('already exists')) {
          return { success: true, message: 'User already exists' };
      }
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return await res.json();
  } catch (e) {
    clearTimeout(timeout);
    if (e.name === 'AbortError') throw new Error('Request timed out (30s)');
    throw e;
  }
}

// ─── Quiz ──────────────────────────────────────────────────────────────────────

async function apiGetQuestions() {
  return apiFetch('/quiz/questions');
}

async function apiSubmitQuiz(userId, answers) {
  return apiFetch('/quiz/submit', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, answers }),
  });
}

async function apiGetAttempts(userId) {
  return apiFetch(`/quiz/attempts/${userId}`);
}

// ─── Roadmap ───────────────────────────────────────────────────────────────────

async function apiGenerateRoadmap(userId) {
  return apiFetch('/roadmap/generate', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  });
}

async function apiGenerateHierarchicalRoadmap(userId) {
  return apiFetch('/roadmap/hierarchical', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  });
}

async function apiCreateCustomRoadmap(userId, roadmapData) {
  return apiFetch('/roadmap/create-custom', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, roadmap_data: roadmapData }),
  });
}

async function apiGetMilestoneDetails(milestoneId) {
  return apiFetch(`/milestone/${milestoneId}`);
}

async function apiGetCustomRoadmaps(userId) {
  return apiFetch(`/roadmap/custom/user/${userId}`);
}

// ─── Users ─────────────────────────────────────────────────────────────────────

async function apiGetUsers() {
  return apiFetch('/users');
}

async function apiGetUser(userId) {
  return apiFetch(`/users/${userId}`);
}

async function apiCreateUser(userData) {
  return apiFetch('/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
}
