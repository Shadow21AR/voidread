---
layout: splash
title: "Windows Posts"
permalink: /windows/
author: "sado"
---
# Windows Posts
Browse all posts related to Windows:
<div class="post-grid">
  {% for post in site.posts %}
    {% if post.tags contains "windows" %}
      <div class="post-card">
        <a href="{{ post.url | relative_url }}">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-date">{{ post.date | date: "%B %d, %Y" }}</div>
          <div class="post-excerpt">{{ post.description | strip_html | truncate: 120 }}</div>
        </a>
      </div>
    {% endif %}
  {% endfor %}
</div>