---
layout: splash
title: "All Posts"
permalink: /all_posts/
author: "sado"
---
# All Posts
<div class="post-grid">
  {% for post in site.posts %}
      <div class="post-card">
        <a href="{{ post.url | relative_url }}">
          <div class="post-title">{{ post.title }}</div>
          <div class="post-date">{{ post.date | date: "%B %d, %Y" }}</div>
          <div class="post-excerpt">{{ post.excerpt | strip_html | truncate: 120 }}</div>
        </a>
      </div>
  {% endfor %}
</div>
