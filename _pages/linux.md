---
layout: splash
title: "Linux Posts"
permalink: /linux/
author: "sado"
---
# Linux Posts
Browse all posts related to Linux:
<div class="post-grid">
  {% for post in site.posts %}
    {% if post.tags contains "linux" %}
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
