---
layout: splash
title: "All Posts"
permalink: /all_posts/
author: "sado"
---
# All Posts

<div class="filter-controls">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="linux">Linux</button>
  <button class="filter-btn" data-filter="windows">Windows</button>
</div>

<div class="post-grid">
  {% for post in site.posts %}
    <div class="post-card" data-tags="{{ post.tags | join: ' ' }}">
      <a href="{{ post.url | relative_url }}">
        <div class="post-title">{{ post.title }}</div>
        <div class="post-date">
          {{ post.date | date: "%B %d, %Y" }}
          {% if post.tags contains 'linux' %}
            <span class="badge badge-linux"><i class="fab fa-linux"></i> Linux</span>
          {% elsif post.tags contains 'windows' %}
            <span class="badge badge-windows"><i class="fab fa-windows"></i> Windows</span>
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
      const tags = card.getAttribute('data-tags');
      if (filter === 'all' || tags.includes(filter)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
});
</script>
