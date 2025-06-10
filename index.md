---
layout: splash
title: "Home"
permalink: /
---

---
<div class="banner-box" style="text-align: center;">
  <h1>VOIDREAD</h1>
  <p id="quote-box"></p>
</div>

<script>
  const quotes = [
    "He who gazes into the fog must be prepared to lose their way — or find something far older staring back.",
    "The Fool knows not the path, yet steps forward. That is the beginning of all power.",
    "What is locked was meant to be opened — by will, by wit, or by wrong.",
    "Each whisper in the static is a secret waiting for the right madness to decode it.",
    "Records sealed in silence scream the loudest to those who listen deeply.",
    "Those who map the unknown are marked by it.",
    "Not every glyph was meant to be read. Some were meant to be endured.",
    "Truth is often buried — not by time, but by intent.",
    "There is no light at the end. Only deeper questions and better tools.",
    "A cipher unsolved is just a god in disguise."
  ];

  const quote = quotes[Math.floor(Math.random() * quotes.length)];
  document.getElementById("quote-box").textContent = `${quote}`;
</script>
---
Welcome to **Voidread** — a place where knowledge grows, ideas take shape, and mysteries unfold.

### 🔍 Explore:
- 🐧 [Linux]({{ '/linux/' | relative_url }}) — For linux related posts.
- 🪟 [Windows]({{ '/windows/' | relative_url }}) — For windows related posts.
- 🧠 [AD Mindmap]({{ '/ad-mindmap/' | relative_url }}) — Your full reference to Active Directory.

---
