---
layout: single
title: "Windows Articles"
permalink: /windows/
author: "sado"
toc: true
toc_sticky: true
---
<style>
.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 2rem;
}

.post-card {
  background-color: #1e1e1e;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 1.2rem;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 0 10px rgba(120, 120, 120, 0.2);
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 15px rgba(138, 180, 248, 0.3);
}

.post-card a {
  color: #cfcfcf;
  text-decoration: none;
}

.post-title {
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #8ab4f8;
}

.post-date {
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 0.6rem;
}

.post-excerpt {
  font-size: 0.9rem;
  color: #c0c0c0;
}
</style>
Browse all posts related to Windows:
<div class="post-grid">
  {% for post in site.posts %}
    {% if post.tags contains "windows" %}
      <div class="post-card">
        <a href="{{ post.url | relative_url }}">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-date">{{ post.date | date: "%B %d, %Y" }}</div>
          <div class="post-excerpt">{{ post.excerpt | strip_html | truncate: 120 }}</div>
        </a>
      </div>
    {% endif %}
  {% endfor %}
</div>
