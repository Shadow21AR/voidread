---
layout: splash
title: "Locked Posts"
permalink: /locked/
author: "sado"
---

# Locked Posts

<div class="filter-controls" style="margin-bottom: 1rem;">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="locked">Locked</button>
  <button class="filter-btn" data-filter="open">Open</button>
</div>

<div class="post-grid">
  {% assign locked_posts = site.data.locked %}
  {% for post in locked_posts %}
    <div class="post-card" data-status="{% if post.locked == false %}false{% else %}true{% endif %}">
      <a href="{{'/locked/' | relative_url}}{{ post.title | slugify }}.html">
        <div class="post-title">{{ post.title }}</div>
        <div class="post-date">
          {% if post.locked == false %}
            <span class="badge badge-open"><i class="fas fa-unlock"></i> Open Access</span>
          {% else %}
            <span class="badge badge-locked"><i class="fas fa-lock"></i> Password Required</span>
          {% endif %}
        </div>
        <div class="post-excerpt">{{ post.description | strip_html | truncate: 120 }}</div>
      </a>
    </div>
  {% endfor %}
</div>

<script>
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.dataset.filter;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.post-card').forEach(card => {
      const status = card.dataset.status === 'false' ? 'open' : 'locked';
      card.style.display = (filter === 'all' || filter === status) ? 'block' : 'none';
    });
  });
});
</script>