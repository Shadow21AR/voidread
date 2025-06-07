---
layout: splash
title: Active Directory Mindmap
permalink: /ad-mindmap/
---
# Active Directory Mindmap

Explore various aspects of Active Directory through the sections below or [visit the external AD mindmap](https://shadow21ar.github.io/AD-mindmap){:target="_blank" rel="noopener noreferrer"}.

<div class="post-grid">
  {% assign ad_manifest = site.data.ad_manifest %}
  {% assign ad_pages = site.ad %}

  {% for entry in ad_manifest %}
    {% assign matched = nil %}
    {% for p in ad_pages %}
      {% if p.path contains entry.file %}
        {% assign matched = p %}
        {% break %}
      {% endif %}
    {% endfor %}
    {% if matched %}
      <div class="post-card">
        <a href="{{ matched.url | relative_url }}" target="_blank" rel="noopener noreferrer">
          <div class="post-title">{{ entry.title }}</div>
          <div class="post-excerpt">{{ matched.description }}</div>
        </a>
      </div>
    {% endif %}
  {% endfor %}
</div>

## Reference

- `ocd-mindmaps`  
  [https://orange-cyberdefense.github.io/ocd-mindmaps/](https://orange-cyberdefense.github.io/ocd-mindmaps/)
