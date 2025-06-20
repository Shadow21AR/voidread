---
layout: splash
title: "Locked Posts"
permalink: /locked/
author: "sado"
---

# Locked Posts

<div class="post-grid">
  {% assign locked_posts = site.data.locked %}
  {% for post in locked_posts %}
    <div class="post-card">
      <a href="{{'/locked/' | relative_url}}{{ post.title | slugify }}.html">
        <div class="post-title">{{ post.title }}</div>
        <div class="post-date">Password Required</div>
        <div class="post-excerpt">{{ post.description | strip_html | truncate: 120 }}</div>
      </a>
    </div>
  {% endfor %}
</div>
