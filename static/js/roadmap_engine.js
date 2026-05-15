// roadmap-renderer.js

function showError(message, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.style.display = 'block';

    // Check if the message is roughly JSON/API shaped to get better strings if 4xx occurred. Defaulting simply:
    container.innerHTML = `<div class="error-banner">${message || 'Something went wrong on our end. Please try again.'}</div>`;
}

function showSkeleton(containerId, lines = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.style.display = 'block';
    let html = '';
    for (let i = 0; i < lines; i++) {
        html += '<div class="skeleton"></div>';
    }
    container.innerHTML = html;
}

function hideSkeleton(containerId) {
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = '';
}

function renderMermaid(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Accept either full data object or phases array for backward compat
    const phases = data.phases || (Array.isArray(data) ? data : []);
    if (!phases || phases.length === 0) {
        container.innerHTML = '';
        return;
    }

    container.innerHTML = `<div id="d3-roadmap-wrapper" style="width:100%; overflow-x:auto; background:rgba(24, 24, 27, 0.4); padding: 20px 0; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);"></div>
                           <div id="d3-tooltip" style="position:absolute; visibility:hidden; background:rgba(24, 24, 27, 0.95); backdrop-filter:blur(8px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 16px; font-size: 13px; max-width: 280px; z-index: 1000; box-shadow: 0 8px 32px rgba(0,0,0,0.5); pointer-events:none; color: #f4f4f5;"></div>`;

    const wrapper = container.querySelector('#d3-roadmap-wrapper');
    const tooltip = container.querySelector('#d3-tooltip');

    // Layout parameters
    const nodeWidth = 200;
    const nodeHeight = 64;
    const horizontalSpacing = 60;
    const verticalSpacing = 120; // 120px row height config
    const startX = 280;
    const startY = 40;

    let maxMilestones = 0;
    phases.forEach(p => {
        if (p.milestones && p.milestones.length > maxMilestones) {
            maxMilestones = p.milestones.length;
        }
    });

    const width = Math.max(800, startX + maxMilestones * (nodeWidth + horizontalSpacing) + 50);
    const height = phases.length * verticalSpacing + 80;

    wrapper.style.background = 'rgba(24, 24, 27, 0.4)';
    wrapper.style.border = '1px solid rgba(255, 255, 255, 0.08)';
    wrapper.style.borderRadius = '12px';
    wrapper.style.padding = '32px';

    if (typeof d3 === 'undefined') {
        container.innerHTML = '<div class="error-banner">D3.js failed to load. Please refresh the page.</div>';
        return;
    }

    const svg = d3.select(wrapper).append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("font-family", "-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif");

    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 8)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "rgba(255, 255, 255, 0.2)");

    svg.append("defs").append("marker")
        .attr("id", "curve-arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 8)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#6366f1");

    // Add Drop shadow filter for hover state
    const filter = svg.select("defs").append("filter")
        .attr("id", "drop-shadow")
        .attr("x", "-20%")
        .attr("y", "-20%")
        .attr("width", "140%")
        .attr("height", "140%");

    filter.append("feDropShadow")
        .attr("dx", "0")
        .attr("dy", "2")
        .attr("stdDeviation", "8")
        .attr("flood-color", "rgba(45,91,227,0.15)");

    const nodes = [];
    const links = [];
    let lastNodeOfPrevPhase = null;

    phases.forEach((phase, pIdx) => {
        const py = startY + pIdx * verticalSpacing;

        // Neural Shorthand Mapper to prevent overlaps - RESTORED AS REQUESTED
        const abbreviations = {
            "MACHINE LEARNING": "ML",
            "ARTIFICIAL INTELLIGENCE": "AI",
            "NATURAL LANGUAGE PROCESSING": "NLP",
            "DEEP LEARNING": "DL",
            "DATA ENGINEERING": "DE",
            "FULL STACK DEVELOPMENT": "FSD",
            "BACKEND DEVELOPMENT": "BE",
            "FRONTEND DEVELOPMENT": "FE",
            "SOFTWARE ENGINEERING": "SWE",
            "INFRASTRUCTURE": "INFRA",
            "CYBERSECURITY": "CYBER",
            "DATA SCIENCE": "DS"
        };

        let displayName = phase.name.replace(/^PHASE \d+:?\s*/i, "").toUpperCase();
        for (const [full, short] of Object.entries(abbreviations)) {
            displayName = displayName.replace(full, short);
        }

        svg.append("text")
            .attr("x", 20)
            .attr("y", py + nodeHeight / 2 + 5)
            .attr("text-anchor", "start")
            .style("font-weight", 700)
            .style("font-size", "11px")
            .style("fill", "#a1a1aa")
            .style("text-transform", "uppercase")
            .text(`PHASE ${pIdx + 1}: ${displayName.length > 25 ? displayName.substring(0, 22) + "..." : displayName}`);

        let prevNode = null;
        const milestones = phase.milestones || [];

        milestones.forEach((ms, mIdx) => {
            const px = startX + mIdx * (nodeWidth + horizontalSpacing);
            const nodeData = {
                id: ms.id || (pIdx + '_' + mIdx),
                x: px,
                y: py,
                title: ms.title,
                difficulty: ms.difficulty || 'beginner',
                description: ms.description || '',
                duration: ms.estimated_duration || ''
            };
            nodes.push(nodeData);

            if (prevNode) {
                links.push({ source: prevNode, target: nodeData, type: 'intra' });
            }
            prevNode = nodeData;
        });

        if (lastNodeOfPrevPhase && milestones.length > 0) {
            links.push({
                source: lastNodeOfPrevPhase,
                target: nodes[nodes.length - milestones.length],
                type: 'inter'
            });
        }

        if (milestones.length > 0) {
            lastNodeOfPrevPhase = nodes[nodes.length - 1];
        }
    });

    svg.selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("fill", "none")
        .attr("stroke", d => d.type === 'intra' ? "rgba(255, 255, 255, 0.15)" : "#6366f1")
        .attr("stroke-width", 1.5)
        .attr("stroke-dasharray", d => d.type === 'inter' ? "4 3" : "none")
        .attr("opacity", d => d.type === 'inter' ? 0.6 : 1)
        .attr("marker-end", d => d.type === 'intra' ? "url(#arrow)" : "url(#curve-arrow)")
        .attr("d", d => {
            if (d.type === 'intra') {
                return `M${d.source.x + nodeWidth},${d.source.y + nodeHeight / 2} L${d.target.x - 4},${d.target.y + nodeHeight / 2}`;
            } else {
                const curX = d.source.x + nodeWidth;
                const curY = d.source.y + nodeHeight / 2;
                const tgtX = d.target.x + nodeWidth / 2;
                const tgtY = d.target.y - 4;
                return `M${curX},${curY} C${curX + 60},${curY} ${tgtX},${curY + verticalSpacing / 2} ${tgtX},${tgtY}`;
            }
        });

    const diffStyles = {
        beginner: { fill: 'rgba(99, 102, 241, 0.1)', stroke: '#6366f1' },
        intermediate: { fill: 'rgba(16, 185, 129, 0.1)', stroke: '#10b981' },
        advanced: { fill: 'rgba(245, 158, 11, 0.1)', stroke: '#f59e0b' },
        expert: { fill: 'rgba(239, 68, 68, 0.1)', stroke: '#ef4444' }
    };

    container.style.position = 'relative';

    const nodeGroups = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`)
        .style("cursor", "pointer")
        .style("transition", "transform 0.2s ease")
        .style("transform-origin", d => `${d.x + nodeWidth / 2}px ${d.y + nodeHeight / 2}px`)
        .on("mouseenter", function (event, d) {
            d3.select(this)
                .style("transform", `translate(${d.x}px,${d.y}px) scale(1.03)`)
                .style("filter", "url(#drop-shadow)");
            d3.select(this).select("rect")
                .attr("stroke-width", 2.5);
        })
        .on("mouseleave", function (event, d) {
            d3.select(this)
                .style("transform", `translate(${d.x}px,${d.y}px) scale(1)`)
                .style("filter", "none");
            d3.select(this).select("rect")
                .attr("stroke-width", 1.5);
            // Hide tooltip ONLY when click outside, requested: Dismiss tooltip on second click or outside
        })
        .on("click", function (event, d) {
            const currentVis = tooltip.style("visibility");
            const currentTarget = tooltip.attr("data-target");

            if (currentVis === "visible" && currentTarget === d.id) {
                tooltip.style("visibility", "hidden");
                tooltip.attr("data-target", "");
                return;
            }

            tooltip.html(`
                <div style="font-weight: 600; color: #f4f4f5; margin-bottom: 6px;">${d.title}</div>
                <div style="color: #a1a1aa; line-height: 1.6; margin-bottom: 12px;">${d.description}</div>
                <div style="text-align: right;"><span style="display:inline-block; padding: 4px 8px; background: rgba(255,255,255,0.1); border-radius: 4px; font-size: 11px; font-weight: 600; color: #a1a1aa;">⌚ ${d.duration}</span></div>
            `);

            let tx = d.x + nodeWidth / 2 - 120;
            let ty = d.y + nodeHeight + 15;
            if (tx < 0) tx = 10;

            tooltip.style("left", tx + "px")
                .style("top", ty + "px")
                .style("visibility", "visible")
                .style("padding", "12px 16px")
                .style("border-radius", "6px")
                .style("box-shadow", "none")
                .attr("data-target", d.id);

            event.stopPropagation();
        });

    nodeGroups.append("rect")
        .attr("width", nodeWidth)
        .attr("height", nodeHeight)
        .attr("rx", 8)
        .attr("fill", d => (diffStyles[d.difficulty.toLowerCase()] || diffStyles.beginner).fill)
        .attr("stroke", d => (diffStyles[d.difficulty.toLowerCase()] || diffStyles.beginner).stroke)
        .attr("stroke-width", 1.5);

    nodeGroups.append("foreignObject")
        .attr("x", 8)
        .attr("y", 8)
        .attr("width", nodeWidth - 16)
        .attr("height", nodeHeight - 16)
        .append("xhtml:div")
        .style("width", "100%")
        .style("height", "100%")
        .style("display", "flex")
        .style("align-items", "center")
        .style("justify-content", "center")
        .style("text-align", "center")
        .style("font-size", "12px")
        .style("font-weight", "500")
        .style("color", "#f4f4f5")
        .style("line-height", "1.4")
        .style("user-select", "none")
        .text(d => d.title);

    d3.select(document).on("click", () => {
        tooltip.style("visibility", "hidden");
        tooltip.attr("data-target", "");
    });
}

function toggleSubtasks(element) {
    // If element is the card itself or a child
    const card = element.closest('.milestone-card');
    if (!card) return;
    card.classList.toggle('expanded');
    const isExpanded = card.classList.contains('expanded');
    const btn = card.querySelector('.subtask-st-btn');
    if (btn) btn.textContent = isExpanded ? '▾ Hide learning steps' : '▸ View learning steps';
}

function renderMilestoneCard(ms, index, totalMilestones) {
    const difficultyStr = (ms.difficulty || 'beginner').toLowerCase();

    // Add difficulty-color logic directly as an allowed exception for dynamic non-var colors, OR map it to simple classes.
    // Given CSS classes for colors aren't present except general badges, we keep the inline border-color because it's dynamic.
    const diffColorMap = {
        beginner: '#34d399',
        intermediate: '#60a5fa',
        advanced: '#fbbf24',
        expert: '#f87171'
    };
    const diffColor = diffColorMap[difficultyStr] || diffColorMap['beginner'];

    const typeStr = (ms.type || 'learning').toLowerCase();

    const skillsHtml = (ms.skills_developed && ms.skills_developed.length > 0) ? `
        <div class="milestone-skills-container">
            <div class="skills-gain-label">Skills you'll gain:</div>
            ${ms.skills_developed.map(skill => `<span class="tag">${skill}</span>`).join('')}
        </div>
    ` : '';

    let subtasksHtml = '';
    if (ms.sub_tasks && ms.sub_tasks.length > 0) {
        let listItems = ms.sub_tasks.map((st, i) => {
            const stURL = st.resource_url ? st.resource_url : `https://google.com/search?q=${encodeURIComponent(st.resource_title)}`;
            return `
                <div class="subtask-item">
                    <div class="subtask-number">${i + 1}</div>
                    <div>
                        <div>
                            <span class="subtask-item-title">${st.task_title || 'Task'}</span> 
                            <span class="subtask-item-time">${st.estimated_time || ''}</span>
                        </div>
                        <a href="${stURL}" target="_blank" class="subtask-item-link" onclick="event.stopPropagation()">→ ${st.resource_title || 'Resource'} <span class="subtask-item-ai">Handpicked by AI</span></a>
                    </div>
                </div>
            `;
        }).join('');

        subtasksHtml = `
            <button class="subtask-st-btn" onclick="toggleSubtasks(this)">▸ View learning steps</button>
            <div class="subtasks-panel">
                <div class="subtask-panel-inner">
                    ${listItems}
                </div>
            </div>
        `;
    }

    return `
        <div class="card milestone-card completion-card" onclick="toggleSubtasks(this)" style="border-left: 4px solid ${diffColor}; position:relative; overflow:hidden; cursor:pointer; transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.05)'" onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
            <div class="milestone-completed-circle"></div>
            <div class="milestone-step-label">Step ${index} of ${totalMilestones}</div>
            
            <div class="milestone-header">
                <h4>${ms.title}</h4>
                <span class="badge badge-${typeStr}">${typeStr}</span>
            </div>
            
            <p class="milestone-desc">${ms.description}</p>
            
            ${skillsHtml}
            ${subtasksHtml}
            
            <div class="milestone-footer">
                <div class="milestone-duration">${ms.estimated_duration}</div>
                <span class="badge badge-${difficultyStr}">${difficultyStr}</span>
            </div>
        </div>
    `;
}

function renderPhases(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Accept either full data object or phases array for backward compat
    const phases = data.phases || (Array.isArray(data) ? data : []);
    const userData = data.user_data || null;

    if (!phases || phases.length === 0) {
        container.innerHTML = '';
        return;
    }

    let html = '<div class="timeline">';

    let totalMilestones = 0;
    phases.forEach(p => totalMilestones += (p.milestones || []).length);

    let globalMilestoneCounter = 1;

    let topSkill = '';
    let topInterest = '';
    if (userData) {
        if (userData.skills && userData.skills.length > 0) topSkill = userData.skills[0];
        if (userData.interests && userData.interests.length > 0) topInterest = userData.interests[0];
    }

    phases.forEach((phase, idx) => {
        let accentClass = `phase-${(idx % 4) + 1}-accent`;

        let personalizationCallout = '';
        if (topSkill || topInterest) {
            let parts = [];
            if (topSkill) parts.push(`background in ${topSkill}`);
            if (topInterest) parts.push(`interest in ${topInterest}`);
            personalizationCallout = `<div class="phase-callout">Based on your ${parts.join(' and ')}</div>`;
        }

        html += `
            <div class="timeline-phase">
                <div class="phase-header ${accentClass}">
                    <div>
                        <h3>${phase.name}</h3>
                        <div class="phase-desc">${phase.description}</div>
                        ${personalizationCallout}
                    </div>
                    <div class="phase-header-right">
                        <span class="badge badge-beginner">${phase.duration || 'Flexible'}</span>
                        <div class="phase-objectives-count">${(phase.objectives || []).length} objectives</div>
                    </div>
                </div>
                
                <div class="milestone-grid">
                    ${(phase.milestones || []).map(m => {
            let res = renderMilestoneCard(m, globalMilestoneCounter, totalMilestones);
            globalMilestoneCounter++;
            return res;
        }).join('')}
                </div>
            </div>
        `;

        if (idx < phases.length - 1) {
            html += `<div class="timeline-down-arrow">↓</div>`;
        }
    });

    html += `</div>
        <div class="motivational-footer">
            <h2>You have everything it takes.</h2>
            <p>Thousands of students have followed roadmaps like this one and landed their dream roles. One milestone at a time.</p>
        </div>
    `;

    container.innerHTML = html;
}

function renderSummaryBar(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Accept either full data object or summary object
    const summary = data.summary || data || {};
    const title = summary.title || data.user || 'Your Career Path';
    const totalDuration = summary.total_duration || 'N/A';
    const phasesCount = summary.phases_count || (data.phases ? data.phases.length : 0);
    const milestonesCount = summary.milestones_count || 0;

    container.innerHTML = `
        <div class="hero-personal">
    
            
            <h1 class="hero-title">Your path to <span style="color:var(--accent);">${title}</span> starts here.</h1>
            <p class="hero-subtitle">
                We've broken your journey into ${phasesCount} phases and ${milestonesCount} milestones. Follow them in order and you'll be job-ready in ${totalDuration}.
            </p>
            
            <div class="stat-chip-container">
                <div class="stat-chip">📅 ${totalDuration}</div>
                <div class="stat-chip">🏁 ${phasesCount} Phases</div>
                <div class="stat-chip">✅ ${milestonesCount} Milestones</div>
            </div>
        </div>
    `;
}

function renderSkillGaps(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Accept either full data object or skill_gaps array
    const skillGaps = data.skill_gaps || (Array.isArray(data) ? data : []);
    if (!skillGaps || skillGaps.length === 0) {
        container.innerHTML = '';
        return;
    }

    let html = `
        <div class="skill-gaps">
            <h3 style="margin-bottom:16px;">Skill Gaps Analysis</h3>
            <div class="card" style="padding: 0; overflow-x: auto;">
                <table class="skill-gaps-table">
                    <thead>
                        <tr>
                            <th>Skill</th>
                            <th>Current Level</th>
                            <th>Target Level</th>
                            <th>Gap Size</th>
                            <th>Learning Path</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${skillGaps.map(gap => {
        let squares = '■□□';
        if (gap.gap_size === 'medium') squares = '■■□';
        if (gap.gap_size === 'large') squares = '■■■';
        return `
                                <tr>
                                    <td><strong>${gap.skill}</strong></td>
                                    <td><span class="badge badge-${(gap.current_level || 'beginner').toLowerCase()}">${gap.current_level}</span></td>
                                    <td><span class="badge badge-${(gap.target_level || 'beginner').toLowerCase()}">${gap.target_level}</span></td>
                                    <td class="gap-size-squares">${squares}</td>
                                    <td>${(gap.learning_path || []).join(', ')}</td>
                                </tr>
                            `;
    }).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    container.innerHTML = html;
}

// Attach export values for module usages if needed, but since we use standard script tags we just let them be globals.
window.renderMermaid = renderMermaid;
window.renderPhases = renderPhases;
window.renderMilestoneCard = renderMilestoneCard;
window.renderSkillGaps = renderSkillGaps;
window.renderSummaryBar = renderSummaryBar;
window.showError = showError;
window.showSkeleton = showSkeleton;
window.hideSkeleton = hideSkeleton;
