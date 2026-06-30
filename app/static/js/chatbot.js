/* Yanxi's portfolio chat widget — a rule-based "ask me anything" bot.
 *
 * No LLM / no API key: it matches the visitor's question to an intent by keywords,
 * then replies with one of several hand-written variations (first person, playful).
 * Easter-egg topics (favorites, MBTI, jokes…) aren't shown on the page — only the bot knows.
 *
 * Sticker hook: every reply may carry an optional `sticker` (image URL). It's left null
 * for now; future stickers (self-drawn or a GIPHY/Tenor media URL) just fill this field —
 * the renderer already shows it. No other change needed.
 */
(function () {
  "use strict";

  // ---- Knowledge base -----------------------------------------------------
  // Each intent: keywords (EN + 中文) -> one of `responses` (picked at random),
  // plus playful follow-up `chips`. `sticker` is the reserved future hook.
  var INTENTS = [
    {
      id: "greeting",
      keywords: ["hi", "hello", "hey", "yo", "howdy", "你好", "在吗", "哈喽"],
      responses: [
        "Hey there! 👋 I'm Yanxi's little assistant. Ask me anything about her — projects, hobbies, travels… or something fun 👀",
        "Hi! 😊 Curious about Yanxi? Ask away — her work, her hobbies, where she's been, or try a cheeky question 👀",
      ],
      sticker: null,
    },
    {
      id: "help",
      keywords: ["help", "what can i ask", "what can you do", "topics", "menu", "options", "能问什么", "帮助", "怎么用"],
      responses: [
        "You can ask me about Yanxi's:\n• Projects & work\n• Education\n• Hobbies\n• Places she's visited\n• Skills & tech\n• How to reach her\n…or ask me something fun 👀",
      ],
      sticker: null,
    },
    {
      id: "fun",
      keywords: ["surprise me", "something fun", "anything fun", "tell me something", "surprise", "好玩", "有趣"],
      responses: [
        "Ooh, I love that! 😄 You could ask me about her cats 🐱, her favorite country 🌍, the music she's obsessed with 🎶, her MBTI, what she's been into lately — or even try saying \"I love you\" 😏. Pick one!",
        "Let's play! 🎉 Try asking about her cats 🐱, milk tea vs coffee 🧋, her favorite project, where she's traveled, or her spirit personality (MBTI). Go on, pick something 👇",
      ],
      chips: [
        { label: "Does she have pets?", q: "does she have pets" },
        { label: "Favorite country?", q: "what is your favorite country" },
        { label: "What music?", q: "what music do you like" },
      ],
      sticker: null,
    },
    {
      id: "about",
      keywords: ["who are you", "who is yanxi", "about", "introduce", "tell me about", "介绍", "是谁"],
      responses: [
        "Yanxi Pan is a CS grad student at Northeastern University (Silicon Valley) and an MLH Fellow. She builds AI-powered tools that bridge language models and real user needs — full-stack dev, NLP pipelines, and turning research prototypes into polished products. 🚀",
      ],
      sticker: null,
    },
    {
      id: "projects",
      keywords: ["project", "projects", "work", "experience", "built", "build", "portfolio", "做过", "项目", "工作", "经历"],
      responses: [
        "Oh, she's built a few things she's proud of! ✨\n• Fanfic Assistant — an AI platform for long-form creative writing\n• SQL Buddy — an AI-powered SQL learning tool\n• NLP research on LLM semantic understanding\n• An LLM medical-dialogue evaluation platform\nWant to know her favorite one? 👀",
      ],
      chips: [
        { label: "Which one's her favorite?", q: "what is your favorite project" },
        { label: "What does she like to do for fun?", q: "hobbies" },
      ],
      sticker: null,
    },
    {
      id: "education",
      keywords: ["education", "school", "study", "studies", "degree", "university", "college", "学历", "教育", "学校", "读书"],
      responses: [
        "She's pursuing a Master of Science in Computer Science at Northeastern University — Silicon Valley. 🎓",
      ],
      sticker: null,
    },
    {
      id: "hobbies",
      keywords: ["hobby", "hobbies", "fun", "free time", "interest", "interests", "爱好", "兴趣", "喜欢做什么"],
      responses: [
        "So many! 🎶 Listening to music, singing, playing The Sims 4, writing (fan fiction!), drawing, and badminton. Ask about any of them — or what she's been into lately 👀",
      ],
      chips: [
        { label: "What's she into lately?", q: "what have you been into lately" },
        { label: "What music does she like?", q: "what music do you like" },
      ],
      sticker: null,
    },
    {
      id: "places",
      keywords: ["travel", "traveled", "country", "countries", "visited", "places", "been to", "去过", "国家", "旅行", "旅游"],
      responses: [
        "She's been to Russia 🇷🇺, Japan 🇯🇵, Thailand 🇹🇭, the United States 🇺🇸, China 🇨🇳, Hungary 🇭🇺 (Budapest!), and Germany 🇩🇪. Ask her which is her favorite 👀",
      ],
      chips: [
        { label: "Which country is her favorite?", q: "what is your favorite country" },
      ],
      sticker: null,
    },
    {
      id: "skills",
      keywords: ["skill", "skills", "tech", "stack", "language", "languages", "programming", "code", "技能", "技术", "编程"],
      responses: [
        "Her toolkit: Python, Java, TypeScript, JavaScript, SQL on the language side; React, Django, FastAPI on frameworks; plus LLMs, PyTorch, Hugging Face, GCP and more. 🛠️",
      ],
      sticker: null,
    },
    {
      id: "contact",
      keywords: ["contact", "email", "reach", "github", "linkedin", "hire", "connect", "联系", "邮箱"],
      responses: [
        "You can reach Yanxi at pan.yanxi@northeastern.edu 📧, or find her on GitHub (@YennieP) and LinkedIn. 🔗",
      ],
      sticker: null,
    },

    // ---- Easter eggs (not shown anywhere on the page) ----------------------
    {
      id: "fav_project",
      keywords: ["favorite project", "favourite project", "best project", "favorite work", "最喜欢的项目", "最爱的项目"],
      responses: [
        "Fanfic Assistant, hands down! 💛 It's tied to her hobby of writing fan fiction, so building it let her think both as a developer (how do I architect and ship this?) and as a user (which features do I actually need?). Best of both worlds.",
      ],
      sticker: null,
    },
    {
      id: "fav_country",
      keywords: ["favorite country", "favourite country", "best country", "favorite place", "最喜欢的国家", "最爱的国家"],
      responses: [
        "China first, of course — it's where she grew up! 🇨🇳 To her it's the most livable place in the world: convenience, variety, value. If she ever had money to burn, she'd live in China.\n\nBut honestly every country has its own fascinating culture, so it's hard to choose. If she had to put it in literary terms: Russian literature is \"like feeling a Siberian blizzard — cold and sharp, yet bringing a strange clarity amid the shivering.\" American literature is \"a grand debate about freedom and loneliness, ideals and disillusionment.\" Latin American literature is \"a fertile land woven from myth, history, politics, and passion — full of magical-realist charm.\" …and so on. 📚",
      ],
      sticker: null,
    },
    {
      id: "music",
      keywords: ["music", "song", "songs", "listen", "artist", "band", "音乐", "歌", "听歌"],
      responses: [
        "She loves music that sweeps her up like a tsunami of emotion — where she resonates with the singer or songwriter. 🌊 Lately she's obsessed with \"Forbidden Fruit\" by Tommee Profitt / Sam Tinnesz / Brooke. If you also love being wrapped in a flood of feeling, she recommends it! 🎧",
      ],
      sticker: null,
    },
    {
      id: "drink",
      keywords: ["drink", "coffee", "tea", "boba", "milk tea", "bubble tea", "咖啡", "奶茶", "喝"],
      responses: [
        "Milk tea forever! 🧋 No contest.",
      ],
      sticker: null,
    },
    {
      id: "mbti",
      keywords: ["mbti", "personality", "introvert", "extrovert", "istj", "intj", "性格", "人格"],
      responses: [
        "She's an ISTJ — occasionally tests as INTJ, but it's ISTJ most of the time. 🗂️",
      ],
      sticker: null,
    },
    {
      id: "lately",
      keywords: ["lately", "recently", "these days", "right now", "currently", "into lately", "最近", "在忙", "在做什么"],
      responses: [
        "Lately she's been polishing her little projects (oh, her babies! 🥹) and drawing — fan art, specifically. She's even studying human anatomy, all so she can draw better. 🎨",
      ],
      sticker: null,
    },
    {
      id: "dream_job",
      keywords: ["dream job", "dream", "career goal", "want to be", "梦想", "理想工作"],
      responses: [
        "The highest-paying one. 😄💰",
      ],
      sticker: null,
    },
    {
      id: "food",
      keywords: ["food", "eat", "favorite food", "cuisine", "吃", "美食", "喜欢吃"],
      responses: [
        "She loves Chinese, Japanese, and Korean food, plus burgers, pizza, and lasagna — no particular ranking, they're all winners. 🍜🍕",
      ],
      sticker: null,
    },
    {
      id: "drawing",
      keywords: ["draw", "drawing", "art", "paint", "sketch", "anatomy", "画画", "画", "绘画"],
      responses: [
        "She's working hard on drawing — fan art mostly — and even studying human anatomy to get better. It's a totally different form of expression from writing, and she loves exploring feelings from new angles. ✍️🎨",
      ],
      sticker: null,
    },
    {
      id: "pets",
      keywords: ["pet", "pets", "cat", "cats", "kitty", "animal", "dog", "dudu", "yinhu", "宠物", "猫", "养", "动物"],
      responses: [
        "Yes — two cats! 🐱 A British Shorthair named Dudu and a Chinese Li Hua named Yinhu. Dudu has the softest fur — I love petting her and burying my face in it — but she's such a tsundere and doesn't really like being hugged QWQ. Yinhu, on the other hand, is super affectionate: she loves being coddled and will hop right onto me asking for pets! Both of them are my good babies XD",
      ],
      sticker: null,
    },
    {
      id: "languages",
      keywords: ["speak", "languages do you", "what languages", "bilingual", "会说", "语言"],
      responses: [
        "She speaks Mandarin Chinese and English. 🗣️",
      ],
      sticker: null,
    },
    {
      id: "robot",
      keywords: ["are you a robot", "are you ai", "are you real", "are you human", "你是机器人", "是不是ai", "是真人吗"],
      responses: [
        "Guilty as charged — I'm a little rule-based bot, no fancy AI brain. 🤖 But everything I say about Yanxi is 100% her. Ask me something!",
      ],
      sticker: null,
    },
    {
      id: "love",
      keywords: ["i love you", "love you", "marry me", "我爱你", "喜欢你"],
      responses: [
        "What a coincidence — I love myself too! 🥰 Hope you love yourself just as much. (sending hearts 💕)",
      ],
      sticker: null,
    },
    {
      id: "joke",
      keywords: ["joke", "funny", "make me laugh", "讲个笑话", "笑话"],
      responses: [
        "Why do programmers prefer dark mode? Because light attracts bugs. 🐛😄",
        "There are 10 types of people: those who understand binary, and those who don't. 😉",
      ],
      sticker: null,
    },
    {
      id: "thanks",
      keywords: ["thank", "thanks", "thx", "谢谢", "多谢"],
      responses: [
        "Anytime! 😊 Anything else you'd like to know about Yanxi?",
      ],
      sticker: null,
    },
    {
      id: "bye",
      keywords: ["bye", "goodbye", "see you", "cya", "再见", "拜拜"],
      responses: [
        "Bye! 👋 Thanks for stopping by — come chat again anytime.",
      ],
      sticker: null,
    },
  ];

  var FALLBACK = {
    responses: [
      "Hmm, I can only chat about Yanxi's background, projects, education, hobbies, travels, skills, and contact info — try one of those! Or ask me something fun 👀",
      "That one's beyond me 😅 But I'd love to tell you about her projects, hobbies, travels, or something playful — give it a try!",
    ],
  };

  // Playful starter chips shown on open and after fallback. Picked/rotated for variety.
  var STARTER_CHIPS = [
    { label: "What has she built?", q: "projects" },
    { label: "What does she do for fun?", q: "hobbies" },
    { label: "Where has she traveled?", q: "places visited" },
    { label: "Ask something fun", q: "surprise me" },
    { label: "Does she have pets?", q: "does she have pets" },
    { label: "How do I reach her?", q: "contact" },
    { label: "Coffee or tea?", q: "coffee or tea" },
  ];

  // ---- Matching -----------------------------------------------------------
  function normalize(text) {
    return (text || "")
      .toLowerCase()
      .replace(/[!?.,;:'"()\[\]{}<>/\\|@#$%^&*_+=~`-]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function hasCJK(s) {
    return /[一-龥]/.test(s);
  }

  // Whole-word match for Latin keywords (so "yo" doesn't match inside "you",
  // "hi" inside "this", etc.); plain substring for CJK keywords (no spaces).
  function keywordHit(norm, kw) {
    if (hasCJK(kw)) return norm.indexOf(kw) >= 0;
    var escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp("(^|\\s)" + escaped + "(\\s|$)").test(norm);
  }

  // How many intents each keyword appears in. Used to down-weight keywords that are
  // shared across intents (TF-IDF idea: a word unique to one intent is a stronger
  // signal than a common one). Computed once from INTENTS.
  var KEYWORD_DF = (function () {
    var df = {};
    for (var i = 0; i < INTENTS.length; i++) {
      var seen = {};
      var kws = INTENTS[i].keywords;
      for (var k = 0; k < kws.length; k++) {
        if (!seen[kws[k]]) { seen[kws[k]] = true; df[kws[k]] = (df[kws[k]] || 0) + 1; }
      }
    }
    return df;
  })();

  // Weight a keyword by specificity instead of a flat +2/+1:
  //   weight = (words in the phrase) / (how many intents use this keyword)
  // → longer, more distinctive phrases count more; generic shared words count less.
  function keywordWeight(kw) {
    var words = kw.split(/\s+/).length;
    return words / (KEYWORD_DF[kw] || 1);
  }

  // If the top two intents are closer than this, treat the match as ambiguous
  // (low confidence) and send it to the fallback instead of guessing wrong.
  var CONFIDENCE_MARGIN = 0.5;

  function match(text) {
    var norm = normalize(text);
    if (!norm) return null;

    var scored = [];
    for (var i = 0; i < INTENTS.length; i++) {
      var intent = INTENTS[i];
      var score = 0;
      for (var k = 0; k < intent.keywords.length; k++) {
        if (keywordHit(norm, intent.keywords[k])) score += keywordWeight(intent.keywords[k]);
      }
      if (score > 0) scored.push({ intent: intent, score: score });
    }
    if (!scored.length) return null; // nothing matched → fallback

    scored.sort(function (a, b) { return b.score - a.score; });
    // Tie / near-tie → ambiguous → don't guess; let the fallback guide the user.
    if (scored.length > 1 && scored[0].score - scored[1].score < CONFIDENCE_MARGIN) {
      return null;
    }
    return scored[0].intent;
  }

  function pick(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // Guide questions the user already clicked this session (by query string).
  // In-memory only, so it resets on page refresh — exactly the desired behavior.
  var clickedChips = {};

  function unclicked(list) {
    return (list || []).filter(function (c) { return !clickedChips[c.q]; });
  }

  // Sample up to n starter suggestions the user hasn't already used.
  function sampleChips(n) {
    var pool = unclicked(STARTER_CHIPS);
    var out = [];
    for (var i = 0; i < n && pool.length; i++) {
      out.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
    }
    return out;
  }

  // ---- UI -----------------------------------------------------------------
  var els = {};
  var opened = false;
  var greeted = false;
  var skipTyping = false;

  function build() {
    var root = document.createElement("div");
    root.id = "yanxi-chatbot";
    root.innerHTML =
      '<button class="chatbot-toggle" aria-label="Open chat" type="button">' +
      '<svg class="chatbot-toggle-icon" viewBox="0 0 24 24" width="26" height="26" ' +
      'fill="currentColor" aria-hidden="true">' +
      '<path d="M4 3 H20 a3 3 0 0 1 3 3 V14 a3 3 0 0 1 -3 3 H15 l-3 3.5 L9 17 H4 ' +
      'a3 3 0 0 1 -3 -3 V6 a3 3 0 0 1 3 -3 Z"/></svg></button>' +
      '<div class="chatbot-panel" role="dialog" aria-label="Ask about Yanxi">' +
      '  <div class="chatbot-header">' +
      '    <span>Ask me about Yanxi 💬</span>' +
      '    <button class="chatbot-close" aria-label="Close chat" type="button">&times;</button>' +
      '  </div>' +
      '  <div class="chatbot-messages"></div>' +
      '  <div class="chatbot-chips"></div>' +
      '  <form class="chatbot-input">' +
      '    <input type="text" placeholder="Ask me anything…" autocomplete="off" aria-label="Your question">' +
      '    <button type="submit" aria-label="Send">➤</button>' +
      '  </form>' +
      '</div>';
    document.body.appendChild(root);

    els.toggle = root.querySelector(".chatbot-toggle");
    els.panel = root.querySelector(".chatbot-panel");
    els.close = root.querySelector(".chatbot-close");
    els.messages = root.querySelector(".chatbot-messages");
    els.chips = root.querySelector(".chatbot-chips");
    els.form = root.querySelector(".chatbot-input");
    els.input = els.form.querySelector("input");

    els.toggle.addEventListener("click", togglePanel);
    els.close.addEventListener("click", closePanel);
    els.form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = els.input.value.trim();
      if (!q) return;
      addUserMessage(q);
      els.input.value = "";
      respond(q);
    });
    // Click anywhere in the messages area to skip the typewriter.
    els.messages.addEventListener("click", function () {
      skipTyping = true;
    });
  }

  function togglePanel() {
    if (opened) return closePanel();
    opened = true;
    els.panel.classList.add("is-open");
    els.toggle.classList.add("is-open");
    els.input.focus();
    if (!greeted) {
      greeted = true;
      var g = pick(intentById("greeting").responses);
      addBotMessage(g);
    }
  }

  function closePanel() {
    opened = false;
    els.panel.classList.remove("is-open");
    els.toggle.classList.remove("is-open");
  }

  function intentById(id) {
    for (var i = 0; i < INTENTS.length; i++) if (INTENTS[i].id === id) return INTENTS[i];
    return null;
  }

  function addUserMessage(text) {
    var el = document.createElement("div");
    el.className = "chatbot-msg user";
    el.textContent = text;
    els.messages.appendChild(el);
    scrollDown();
  }

  function renderChips(chips) {
    els.chips.innerHTML = "";
    if (!chips || !chips.length) return;
    chips.forEach(function (chip) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "chatbot-chip";
      b.textContent = chip.label;
      b.addEventListener("click", function () {
        clickedChips[chip.q] = true; // don't suggest this one again this session
        addUserMessage(chip.label);
        respond(chip.q);
      });
      els.chips.appendChild(b);
    });
    // Chips take vertical space below the messages area; re-scroll AFTER the
    // browser lays them out, so the last message stays visible.
    requestAnimationFrame(scrollDown);
  }

  // What to show below a reply: this intent's unused follow-ups, else fresh
  // starter suggestions; once the user has clicked them all, invite free-form questions.
  function showSuggestions(intentChips) {
    var chips = unclicked(intentChips);
    if (!chips.length) chips = sampleChips(3);
    if (chips.length) renderChips(chips);
    else renderInvite();
  }

  function renderInvite() {
    els.chips.innerHTML =
      '<span class="chatbot-invite">That’s all my quick questions — type your own to ask me anything!</span>';
    requestAnimationFrame(scrollDown);
  }

  // Bot message with typing delay + typewriter, then optional sticker + chips.
  function addBotMessage(text, chips, sticker) {
    renderChips([]); // hide chips while "typing"
    var typing = document.createElement("div");
    typing.className = "chatbot-msg bot typing";
    typing.innerHTML = "<span></span><span></span><span></span>";
    els.messages.appendChild(typing);
    scrollDown();

    var delay = 450 + Math.random() * 350;
    setTimeout(function () {
      els.messages.removeChild(typing);
      var el = document.createElement("div");
      el.className = "chatbot-msg bot";
      els.messages.appendChild(el);
      typewrite(el, text, function () {
        if (sticker) {
          var img = document.createElement("img");
          img.className = "chatbot-sticker";
          img.src = sticker;
          img.alt = "";
          el.appendChild(img);
          scrollDown();
        }
        showSuggestions(chips);
      });
    }, delay);
  }

  // Reveal text progressively; long text types faster; clicking skips to full.
  function typewrite(el, text, done) {
    skipTyping = false;
    var i = 0;
    var speed = text.length > 140 ? 8 : 22; // ms per char
    function step() {
      if (skipTyping) {
        el.textContent = text;
        scrollDown();
        return done && done();
      }
      i++;
      el.textContent = text.slice(0, i);
      scrollDown();
      if (i < text.length) {
        setTimeout(step, speed);
      } else if (done) {
        done();
      }
    }
    step();
  }

  function respond(query) {
    var intent = match(query);
    if (intent) {
      addBotMessage(pick(intent.responses), intent.chips, intent.sticker);
    } else {
      addBotMessage(pick(FALLBACK.responses));
    }
  }

  function scrollDown() {
    els.messages.scrollTop = els.messages.scrollHeight;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
