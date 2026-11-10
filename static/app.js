const $ = (id) => document.getElementById(id);
const RATE = 16000;
const XP_PER_LEVEL = 50;
const DAILY_GOAL = 3;
let data = null;
let lang = "hi-IN";
let running = 0; // bumps on every start or back, so an old flow stops
let combo = 0; // correct answers in a row this session

const C = () => data.content[lang];
const G = () => data.progress.game;
const BRAND = { "hi-IN": "Taara", "pa-IN": "Taara" };
const pick = (list) => list[Math.floor(Math.random() * list.length)];

const ICONS = {
  phone: '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
  mic: '<svg viewBox="0 0 24 24"><path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11z"/></svg>',
  star: '<svg viewBox="0 0 24 24"><path d="M12 2.5l2.8 6.3 6.9.6-5.2 4.6 1.6 6.8L12 17.2l-6.1 3.6 1.6-6.8-5.2-4.6 6.9-.6z"/></svg>',
  flame: '<svg viewBox="0 0 24 24"><path d="M12 2c1 3.5-1.5 5.2-1.5 7.7 0 1.4 1 2.3 2.1 2.3 1.6 0 2.4-1.6 1.9-3.5 2.4 1.6 3.5 4 3.5 6.2A6 6 0 0 1 6 15c0-4.6 4.4-7 6-13z"/></svg>',
  bolt: '<svg viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="#fff"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
  medal: '<svg viewBox="0 0 24 24"><path d="M6 2h5l1.5 5-3.5 3zM18 2h-5l-1.5 5 3.5 3z"/><circle cx="12" cy="15.5" r="6.5"/><path fill="#fff" opacity=".85" d="m12 11.6 1.2 2.5 2.7.3-2 1.8.6 2.7-2.5-1.4-2.5 1.4.6-2.7-2-1.8 2.7-.3z"/></svg>',
  taara: '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M32 12H68A22 22 0 0 1 90 34V56A22 22 0 0 1 68 78H40L23 92L29.5 77.9A22 22 0 0 1 10 56V34A22 22 0 0 1 32 12Z" fill="#3346a8"/><polygon points="50.0,28.0 54.3,39.0 66.2,39.7 57.0,47.3 60.0,58.8 50.0,52.4 40.0,58.8 43.0,47.3 33.8,39.7 45.7,39.0" fill="#f4b63f" stroke="#f4b63f" stroke-width="5" stroke-linejoin="round"/><circle cx="74" cy="26" r="4" fill="#ffd77a"/></svg>',
};
function icons(root = document) {
  root.querySelectorAll("[data-icon]").forEach((el) => (el.innerHTML = ICONS[el.dataset.icon]));
}
function iconSpan(name, cls = "") {
  const s = document.createElement("span");
  s.className = cls;
  s.innerHTML = ICONS[name];
  return s;
}

function toast(msg) {
  const t = $("toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (t.hidden = true), 5000);
}

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(typeof body.detail === "string" ? body.detail : "Something went wrong");
  return body;
}
const post = (path, body) => api(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

// ---------- confetti ----------
function confetti(amount = 120) {
  const canvas = $("confetti");
  const ctx = canvas.getContext("2d");
  canvas.width = innerWidth;
  canvas.height = innerHeight;
  const colors = ["#3346a8", "#f4b63f", "#e8614c", "#2f9a6d", "#9aa8f0"];
  const bits = Array.from({ length: amount }, () => ({
    x: innerWidth / 2 + (Math.random() - .5) * 120, y: innerHeight * .45,
    vx: (Math.random() - .5) * 12, vy: -Math.random() * 12 - 4,
    s: 5 + Math.random() * 6, r: Math.random() * 6, c: pick(colors),
  }));
  const end = performance.now() + 1700;
  (function frame(now) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    bits.forEach((b) => {
      b.vy += .35; b.x += b.vx; b.y += b.vy; b.r += .1;
      ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.r);
      ctx.fillStyle = b.c; ctx.fillRect(-b.s / 2, -b.s / 4, b.s, b.s / 2); ctx.restore();
    });
    if (now < end) requestAnimationFrame(frame); else ctx.clearRect(0, 0, canvas.width, canvas.height);
  })(performance.now());
}

// ---------- speaking ----------
const player = new Audio();
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
async function say(key, run) {
  if (run !== running) throw new Error("stopped");
  const { url } = await post("/api/line", { lang, key });
  if (run !== running) throw new Error("stopped");
  $("avatar").classList.add("talking");
  try {
    player.src = url;
    await player.play();
    await new Promise((resolve) => { player.onended = resolve; player.onpause = resolve; });
  } finally {
    $("avatar").classList.remove("talking");
  }
  await wait(250);
}

let lastPraise = -1;
function praiseKey() {
  if (combo > 0 && combo % 3 === 0) return "shared:streak";
  let i;
  do { i = Math.floor(Math.random() * C().praise.length); } while (i === lastPraise && C().praise.length > 1);
  lastPraise = i;
  return `praise:${i}`;
}
let greeted = false;
async function greet(run) {
  if (greeted || !data.progress.profile.name) return;
  greeted = true;
  await say("greet", run);
}
const encourageKey = () => `encourage:${Math.floor(Math.random() * C().encourage.length)}`;

// ---------- listening ----------
function wav(samples) {
  const buf = new ArrayBuffer(44 + samples.length * 2);
  const v = new DataView(buf);
  const s = (o, t) => [...t].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  s(0, "RIFF"); v.setUint32(4, 36 + samples.length * 2, true); s(8, "WAVEfmt ");
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, RATE, true); v.setUint32(28, RATE * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true);
  s(36, "data"); v.setUint32(40, samples.length * 2, true);
  samples.forEach((x, i) => v.setInt16(44 + i * 2, Math.max(-1, Math.min(1, x)) * 32767, true));
  return new Blob([buf], { type: "audio/wav" });
}

let stopNow = null;
let helpKey = null;
async function record(opts = {}) {
  const { quietStop = 1.2, maxSecs = 12, idleSecs = 8 } = opts;
  // Stops 1.2 s after the child stops talking, after 12 s, or after 8 s of nothing.
  const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true } });
  const ctx = new AudioContext();
  const src = ctx.createMediaStreamSource(stream);
  const node = ctx.createScriptProcessor(4096, 1, 1);
  const chunks = [];
  let spoke = false, quiet = 0, total = 0;
  await new Promise((resolve) => {
    stopNow = resolve;
    node.onaudioprocess = (e) => {
      const d = new Float32Array(e.inputBuffer.getChannelData(0));
      chunks.push(d);
      const secs = d.length / ctx.sampleRate;
      const level = Math.sqrt(d.reduce((a, x) => a + x * x, 0) / d.length);
      total += secs;
      if (level > 0.015) { spoke = true; quiet = 0; } else quiet += secs;
      if ((spoke && quiet > quietStop) || total > maxSecs || (!spoke && total > idleSecs)) resolve();
    };
    src.connect(node);
    node.connect(ctx.destination);
  });
  stopNow = null;
  node.disconnect(); src.disconnect(); stream.getTracks().forEach((t) => t.stop());
  const inRate = ctx.sampleRate;
  await ctx.close();
  const all = new Float32Array(chunks.reduce((a, c) => a + c.length, 0));
  let at = 0;
  chunks.forEach((c) => { all.set(c, at); at += c.length; });
  const ratio = inRate / RATE;
  const out = new Float32Array(Math.floor(all.length / ratio));
  for (let i = 0; i < out.length; i++) out[i] = all[Math.floor(i * ratio)];
  return wav(Array.from(out));
}

let currentAsk = null;
let currentLesson = null;
async function listen(lesson, mode, run, trId = "") {
  for (;;) {
    if (run !== running) throw new Error("stopped");
    $("inEnglish").hidden = !currentEn;
    $("skipBtn").hidden = currentMode !== "call";
    $("turn").hidden = false;
    let blob;
    try { blob = await record(); }
    catch (e) { $("turn").hidden = true; throw e.name === "NotAllowedError" ? new Error("Please allow the microphone.") : e; }
    $("turn").hidden = true;
    if (run !== running) throw new Error("stopped");
    if (helpKey === "skip") {
      helpKey = null;
      return { label: "skip", heard: "", missed: [] };
    }
    if (helpKey) {
      const key = helpKey;
      helpKey = null;
      await say(key, run);
      continue;
    }
    const form = new FormData();
    form.append("audio", blob, "answer.wav");
    form.append("lang", lang);
    form.append("lesson_id", lesson.id);
    form.append("mode", mode);
    if (trId) form.append("tr_id", trId);
    const result = await api("/api/answer", { method: "POST", body: form });
    showHeard(result, lesson);
    return result;
  }
}
function askHelp(key) { if (stopNow) { helpKey = key; stopNow(); } }
$("mic").onclick = () => stopNow && stopNow();
$("again").onclick = () => currentAsk && askHelp(currentAsk);
let currentSlow = null;
$("slowly").onclick = () => currentSlow && askHelp(currentSlow);
let currentEn = null;
$("inEnglish").onclick = () => currentEn && askHelp(currentEn);
let currentMode = "";
$("skipBtn").onclick = () => askHelp("skip");

const words = (s) => s.toLowerCase().normalize("NFC").replace(/[^\p{L}\p{M}\p{N}\s]/gu, " ").split(/\s+/).filter(Boolean);
const targetWords = (lesson) => lesson.target.replace(/[,।?!.]/g, " ").split(/\s+/).filter(Boolean);
function showHeard(result, lesson) {
  $("heard").hidden = false;
  result.missed = [];
  if (!result.heard) {
    $("heardText").textContent = "I didn't hear anything that time.";
    $("chips").replaceChildren();
    return;
  }
  $("heardText").textContent = `I heard: “${result.heard}”`;
  const got = new Set(words(result.heard));
  const native = targetWords(lesson);
  const roman = words(lesson.target_roman);
  $("chips").replaceChildren(...native.map((w, i) => {
    const chip = document.createElement("span");
    const hit = got.has(words(w)[0]) || (roman.length === native.length && got.has(roman[i]));
    if (!hit) result.missed.push(i);
    chip.className = hit ? "chip got" : result.label === "said_it" ? "chip" : "chip miss";
    chip.textContent = w;
    return chip;
  }));
}

// ---------- teaching ----------
function bubble(label, text, roman, en, model = false) {
  $("bubble").hidden = false;
  $("bubble").classList.toggle("model", model);
  $("bubbleLabel").textContent = label;
  $("bubbleText").textContent = text;
  $("bubbleRoman").textContent = roman;
  $("bubbleEn").textContent = en;
}

async function teach(lesson, mode, run) {
  const c = C();
  currentMode = mode;
  currentLesson = lesson;
  currentSlow = `slow:${lesson.id}`;
  currentEn = `en:${lesson.id}`;
  currentAsk = `${mode === "call" ? "q" : "ask"}:${lesson.id}`;
  if (mode === "word") bubble("New word", lesson.target, lesson.target_roman, lesson.target_en);
  else bubble(mode === "call" ? `${c.elder_roman} (pretend) asks` : `When ${c.elder_roman} asks`, lesson.ask, lesson.ask_roman, lesson.ask_en);
  $("heard").hidden = true;
  await say(currentAsk, run);
  const first = await listen(lesson, mode, run);
  if (first.label === "skip") return 1;
  if (first.label === "said_it") {
    combo += 1;
    renderStats();
    if (first.by !== "match") bubble("Another way to say it", lesson.target, lesson.target_roman, lesson.target_en, true);
    await say(praiseKey(), run);
    return 3;
  }
  combo = 0;
  renderStats();
  if (first.label === "english" && first.heard) {
    // Turn what the child actually said into the family language, then they repeat it.
    let item = null;
    const meant = first.english || first.heard;
    try { item = await post("/api/translate", { lang, text: meant }); } catch { item = null; }
    if (item && run === running) {
      await say("shared:english", run);
      bubble(`In ${c.language_name} you say`, item.native, item.roman, `You said: “${meant}”`, true);
      currentAsk = `tr:${item.id}`;
      currentSlow = currentAsk;
      currentEn = null;
      await say(currentAsk, run);
      const again = await listen({ ...lesson, target: item.native, target_roman: item.roman }, mode, run, item.id);
      if (again.label === "skip") return 1;
      if (again.label === "said_it") {
        combo += 1;
        renderStats();
        await say(praiseKey(), run);
        return 2;
      }
      await say(encourageKey(), run);
      return 1;
    }
  }
  const total = targetWords(lesson).length;
  const partial = first.heard && first.missed.length > 0 && first.missed.length < total && first.label !== "english";
  if (partial) {
    // Point out the exact words to fix, said slowly, then try the whole phrase again.
    await say("shared:fix", run);
    for (const i of first.missed.slice(0, 2)) await say(`word:${lesson.id}:${i}`, run);
  } else {
    await say(first.label === "english" ? "shared:english" : "shared:nevermind", run);
  }
  bubble("Say it with Taara", lesson.target, lesson.target_roman, lesson.target_en, true);
  currentAsk = `model:${lesson.id}`;
  await say(currentAsk, run);
  const second = await listen(lesson, mode, run);
  if (second.label === "skip") return 1;
  if (second.label === "said_it") {
    combo += 1;
    renderStats();
    await say(praiseKey(), run);
    return 2;
  }
  await say(encourageKey(), run);
  return 1;
}

const XP_FOR = { 3: 15, 2: 10, 1: 5 };
const TITLES = { 3: ["Brilliant!", "Perfect!", "You nailed it!", "Superstar!"], 2: ["Great job!", "Well done!", "You got it!"], 1: ["Good try!", "Nice effort!", "Keep going!"] };

async function award(lesson, stars) {
  data.progress = await post("/api/score", { lang, lesson_id: lesson.id, stars, xp: XP_FOR[stars], streak: combo });
  renderStats();
}

function showResult(stars, xp, title) {
  $("result").hidden = false;
  $("resultStars").replaceChildren(...[1, 2, 3].map((n) => iconSpan("star", n <= stars ? "on" : "")));
  $("resultTitle").textContent = title || pick(TITLES[stars]);
  $("resultXp").textContent = `+${xp} XP`;
  if (stars >= 2) confetti(stars === 3 ? 140 : 70);
  $("result").scrollIntoView({ behavior: "smooth", block: "center" });
}

// ---------- build-the-sentence game ----------
function shuffled(list) {
  if (list.length < 2) return list.slice();
  let out;
  do { out = list.slice().sort(() => Math.random() - .5); } while (out.join(" ") === list.join(" "));
  return out;
}
function puzzle(lesson) {
  const answer = targetWords(lesson);
  if (answer.length < 2) return Promise.resolve(false);
  return new Promise((resolve) => {
    $("puzzle").hidden = false;
    $("puzzleHint").textContent = `Tap the words in order: ${lesson.target_en || lesson.target_roman}`;
    const placed = [];
    const draw = () => {
      $("slots").className = "slots";
      $("slots").replaceChildren(...placed.map((w) => Object.assign(document.createElement("span"), { className: "slot", textContent: w })));
      const left = answer.slice();
      placed.forEach((w) => left.splice(left.indexOf(w), 1));
      $("pool").replaceChildren(...pool.filter((w, i) => {
        const used = placed.filter((p) => p === w).length;
        return pool.slice(0, i + 1).filter((p) => p === w).length > used;
      }).map((w) => {
        const b = document.createElement("button");
        b.className = "word";
        b.textContent = w;
        b.onclick = () => { placed.push(w); draw(); check(); };
        return b;
      }));
    };
    const pool = shuffled(answer);
    const finish = (won) => { $("puzzle").hidden = true; resolve(won); };
    const check = () => {
      if (placed.length < answer.length) return;
      if (placed.join(" ") === answer.join(" ")) {
        $("slots").classList.add("right");
        confetti(60);
        setTimeout(() => finish(true), 900);
      } else {
        $("slots").classList.add("wrong");
        setTimeout(() => { placed.length = 0; draw(); }, 650);
      }
    };
    $("puzzleReset").onclick = () => { placed.length = 0; draw(); };
    $("puzzleSkip").onclick = () => finish(false);
    draw();
  });
}

// ---------- screens ----------
function show(view) {
  ["home", "stage", "parents", "translator", "listen", "message"].forEach((id) => ($(id).hidden = id !== view));
  window.scrollTo(0, 0);
}

function openStage(modeText, total, index) {
  running += 1;
  show("stage");
  ["bubble", "heard", "turn", "result", "puzzle", "next", "options", "chatLog", "chatForm"].forEach((id) => ($(id).hidden = true));
  $("coachName").textContent = C().buddy_roman;
  $("modeTag").hidden = !modeText;
  $("modeTag").textContent = modeText || "";
  drawDots(total, index);
  return running;
}
function drawDots(total, index) {
  $("dots").replaceChildren(...Array.from({ length: total }, (_, i) => {
    const d = document.createElement("span");
    d.className = i < index ? "done" : i === index ? "on" : "";
    return d;
  }));
}

async function guarded(fn) {
  try { await fn(); }
  catch (e) { if (e.message !== "stopped") toast(e.message); }
}

async function runLesson(lesson) {
  const lessons = C().lessons;
  const index = lessons.indexOf(lesson);
  const run = openStage("", lessons.length, index);
  await guarded(async () => {
    await greet(run);
    const stars = await teach(lesson, "lesson", run);
    await award(lesson, stars);
    showResult(stars, XP_FOR[stars]);
    await wait(900);
    if (run !== running) return;
    const won = await puzzle(lesson);
    if (run !== running) return;
    if (won) {
      data.progress = await post("/api/score", { lang, xp: 5, streak: combo });
      renderStats();
      $("resultXp").textContent = `+${XP_FOR[stars] + 5} XP (with bonus)`;
    }
    const nextLesson = lessons[index + 1];
    $("next").hidden = false;
    $("nextBtn").hidden = !nextLesson;
    $("nextBtn").textContent = "Next phrase";
    $("nextBtn").onclick = () => start(() => runLesson(nextLesson));
  });
}

function callPlan() {
  // Hello first, bye last, and 4 random questions in between, so every call is different.
  const c = C();
  const first = c.lessons.find((l) => l.id === "hello");
  const last = c.lessons.find((l) => l.id === "bye");
  const special = c.lessons.filter((l) => l.special);
  const pool = [...c.lessons.filter((l) => l !== first && l !== last && !l.special), ...c.call_extras];
  const pickN = (list, n) => list.map((x) => [Math.random(), x]).sort((a, b) => a[0] - b[0]).slice(0, n).map((x) => x[1]);
  // Always include this relative's own questions, plus two random ones.
  const middle = pickN([...pickN(special, 2), ...pickN(pool, 2)], 4);
  return [first, ...middle, last].filter(Boolean);
}

async function runCall() {
  const c = C();
  const plan = callPlan();
  const run = openStage(`Pretend game: ${c.buddy_roman} plays ${c.elder_roman}`, plan.length, 0);
  await guarded(async () => {
    await greet(run);
    bubble("Practice call", c.shared.ring.replace(/<[^>]+>/g, ""), "", "");
    await say("shared:ring", run);
    let total = 0;
    for (const [i, lesson] of plan.entries()) {
      drawDots(plan.length, i);
      const stars = await teach(lesson, "call", run);
      total += stars;
      await award(lesson, stars);
    }
    drawDots(plan.length, plan.length);
    bubble("", c.shared.ready.replace(/<[^>]+>/g, ""), "", "");
    data.progress = await post("/api/call-done", { lang });
    data.progress = await post("/api/score", { lang, xp: 20, streak: combo });
    renderStats();
    const avg = Math.max(1, Math.round(total / plan.length));
    showResult(avg, 20, `Call complete. Now call your real ${c.elder_roman}!`);
    await say("shared:ready", run);
    $("next").hidden = false;
    $("nextBtn").hidden = true;
  });
}

async function runTrack(track) {
  const items = track.items;
  const run = openStage(`First words: ${track.title}`, items.length, 0);
  await guarded(async () => {
    await greet(run);
    let total = 0;
    for (const [i, item] of items.entries()) {
      drawDots(items.length, i);
      const stars = await teach(item, "word", run);
      total += stars;
      await award(item, stars);
    }
    drawDots(items.length, items.length);
    $("heard").hidden = true;
    const avg = Math.max(1, Math.round(total / items.length));
    showResult(avg, items.length * 5, `You learnt ${items.length} new words!`);
    $("next").hidden = false;
    $("nextBtn").hidden = true;
  });
}

function goHome() {
  running += 1;
  player.pause();
  helpKey = null;
  if (stopNow) stopNow();
  show("home");
  refresh();
}
$("back").onclick = goHome;
$("back2").onclick = goHome;
$("back3").onclick = goHome;
$("back4").onclick = goHome;
$("back5").onclick = goHome;
$("pathBtn").onclick = goHome;
$("toParents").onclick = () => { show("parents"); render(); };

// ---------- rendering ----------
const starsOf = (id) => G().stars[`${lang}:${id}`] || 0;

function renderStats() {
  $("xp").textContent = G().xp;
  $("streakNow").textContent = combo;
}

// Home shows a short list first so it isn't crowded; one tap shows the rest.
const SHORT_PATH = 5, SHORT_TRACKS = 6;
const showAll = { path: false, tracks: false };
function moreToggle(id, key, total, short, noun) {
  const btn = $(id);
  btn.hidden = total <= short;
  btn.textContent = showAll[key] ? "Show less" : `Show all ${total} ${noun}`;
  btn.onclick = () => { showAll[key] = !showAll[key]; render(); };
}

function render() {
  const c = C();
  const g = G();
  document.documentElement.lang = lang === "pa-IN" ? "pa" : "hi";
  document.querySelectorAll(".langs button").forEach((b) => b.classList.toggle("on", b.dataset.lang === lang));
  $("brand").textContent = BRAND[lang];
  document.title = "Taara – Aapki India Se Dost";
  $("mock").hidden = !data.mock;
  $("callSub").textContent = `${c.elder_roman}'s usual questions`;
  $("trCardTitle").textContent = `Say it in ${c.language_name}`;
  $("trTitle").textContent = `Say it in ${c.language_name}`;
  $("trGlyph").textContent = lang === "pa-IN" ? "A → ਅ" : "A → अ";
  $("trIntro").textContent = `Type or say anything in English. ${c.buddy_roman} shows you how to say it in ${c.language_name}.`;
  renderStats();

  const level = Math.floor(g.xp / XP_PER_LEVEL) + 1;
  const into = g.xp % XP_PER_LEVEL;
  $("levelName").textContent = `Level ${level}`;
  $("heroTitle").textContent = `Get ready to talk with ${c.elder_roman}`;
  const prof = data.progress.profile;
  $("hiName").textContent = prof.name ? `Hi ${prof.name}!` : "Hi there!";
  $("editName").textContent = prof.name ? "Change name" : "Set your name";
  $("relatives").replaceChildren(...c.relatives.map((r) => {
    const b = document.createElement("button");
    b.className = `rel${r.id === c.relative.id ? " on" : ""}`;
    b.title = r.en;
    b.append(document.createTextNode(r.native), Object.assign(document.createElement("small"), { textContent: r.roman }));
    b.onclick = async () => {
      data.progress = await post("/api/profile", { lang, relative: r.id });
      prepared[lang] = false;
      refresh();
    };
    return b;
  }));
  $("msgCardTitle").textContent = `Message for ${c.elder_roman}`;
  $("chatCardTitle").textContent = `Pretend call with ${c.elder_roman}`;
  $("chatCard").querySelector("small").textContent = `Say anything. ${c.buddy_roman}, pretending to be ${c.elder_roman}, talks back in ${c.language_name} and helps when you use English.`;
  const pf = $("profileForm").elements;
  if (!$("profileForm").contains(document.activeElement)) {
    pf.namedItem("name").value = prof.name;
    pf.namedItem("gender").value = prof.gender;
  }
  $("levelBar").style.width = `${(into / XP_PER_LEVEL) * 100}%`;
  $("levelText").textContent = `${XP_PER_LEVEL - into} XP to level ${level + 1}`;
  const today = g.today.date === new Date().toISOString().slice(0, 10) ? g.today.count : 0;
  $("goalText").textContent = `Today: ${Math.min(today, DAILY_GOAL)} of ${DAILY_GOAL} phrases`;

  const nextIndex = c.lessons.findIndex((l) => !starsOf(l.id));
  $("continueBtn").textContent = nextIndex === -1 ? "Practise again" : `Continue: phrase ${nextIndex + 1}`;
  $("continueBtn").onclick = () => start(() => runLesson(c.lessons[Math.max(0, nextIndex)]));
  $("count").textContent = `${c.lessons.filter((l) => starsOf(l.id)).length} of ${c.lessons.length} done`;

  $("path").replaceChildren(...c.lessons.map((l, i) => {
    const li = document.createElement("li");
    const b = document.createElement("button");
    const stars = starsOf(l.id);
    b.className = `step${stars ? " done" : ""}${i === nextIndex ? " next" : ""}`;
    const node = document.createElement("span");
    node.className = "node";
    if (stars) node.innerHTML = ICONS.check; else node.textContent = i + 1;
    const body = document.createElement("span");
    body.className = "step-body";
    const native = Object.assign(document.createElement("div"), { className: "native", textContent: l.target });
    const sub = Object.assign(document.createElement("div"), { className: "sub", textContent: l.family ? "Family phrase" : l.special ? `${c.elder_roman}'s question · ${l.title}` : l.title });
    if (l.family || l.special) sub.classList.add("fam");
    body.append(native, sub);
    const mini = document.createElement("span");
    mini.className = "mini-stars";
    [1, 2, 3].forEach((n) => mini.append(iconSpan("star", n <= stars ? "on" : "")));
    b.append(node, body, mini);
    b.onclick = () => start(() => runLesson(l));
    li.append(b);
    if (!showAll.path && i >= SHORT_PATH) li.hidden = true;
    return li;
  }));
  moreToggle("morePath", "path", c.lessons.length, SHORT_PATH, "phrases");

  $("tracks").replaceChildren(...c.tracks.map((t) => {
    const b = document.createElement("button");
    b.className = "track";
    const done = t.items.filter((x) => starsOf(x.id)).length;
    const title = Object.assign(document.createElement("b"), { textContent: t.title });
    const sample = Object.assign(document.createElement("span"), { className: "native", textContent: t.items.slice(0, 3).map((x) => x.target).join(" · ") });
    const meter = document.createElement("div");
    meter.className = "meter";
    meter.append(Object.assign(document.createElement("span"), { style: `width:${(done / t.items.length) * 100}%` }));
    b.title = `${done} of ${t.items.length} words`;
    b.append(title, sample, meter);
    b.onclick = () => runTrack(t);
    if (!showAll.tracks && c.tracks.indexOf(t) >= SHORT_TRACKS) b.hidden = true;
    return b;
  }));
  moreToggle("moreTracks", "tracks", c.tracks.length, SHORT_TRACKS, "word sets");

  const BADGES = [["first", "First words"], ["streak3", "3 in a row"], ["call", "Practice call"], ["all", "All phrases"]];
  $("badges").replaceChildren(...BADGES.map(([id, name]) => {
    const d = document.createElement("div");
    d.className = `badge${g.badges.includes(id) ? " on" : ""}`;
    d.append(iconSpan("medal", "medal"), document.createTextNode(name));
    return d;
  }));

  $("lblAsk").textContent = `What ${c.elder_roman} asks (in ${c.language_name})`;
  $("lblTarget").textContent = `What your child should say (in ${c.language_name})`;
  $("progress").replaceChildren(...c.lessons.map((l) => {
    const row = document.createElement("div");
    row.className = "row";
    const stars = starsOf(l.id);
    const ph = Object.assign(document.createElement("span"), { textContent: `${l.target} · ${l.target_roman}` });
    const st = Object.assign(document.createElement("span"), { className: `st${stars >= 2 ? " said" : ""}`, textContent: stars ? `${stars} of 3 stars` : "Not yet" });
    row.append(ph, st);
    return row;
  }), Object.assign(document.createElement("p"), { className: "muted", textContent: `Total XP: ${g.xp} · Practice calls finished: ${data.progress.calls_done[lang] || 0} · Best streak: ${g.best_streak}` }));

  $("customList").replaceChildren(...c.lessons.filter((l) => l.family).map((l) => {
    const row = document.createElement("div");
    row.className = "row";
    const text = Object.assign(document.createElement("span"), { textContent: `${l.ask} → ${l.target}` });
    const del = Object.assign(document.createElement("button"), { className: "btn small", textContent: "Remove" });
    del.onclick = async () => { await api(`/api/custom/${lang}/${l.id}`, { method: "DELETE" }); refresh(); };
    row.append(text, del);
    return row;
  }));

  $("log").replaceChildren(...data.progress.log.filter((x) => x.lang === lang).slice(-6).reverse().map((x) => {
    const li = document.createElement("li");
    li.textContent = `“${x.heard}” (${x.label.replace("_", " ")})`;
    return li;
  }));
}

async function refresh() { data = await api("/api/content"); if ($("stage").hidden) render(); else renderStats(); }

// ---------- English to Hindi tool ----------
let trItem = null;
async function playKey(key) {
  const { url } = await post("/api/line", { lang, key });
  player.src = url;
  await player.play();
}
function showTranslation(item, english) {
  trItem = item;
  $("trResult").hidden = false;
  $("trYouSaid").textContent = `“${english}” in ${C().language_name}`;
  $("trNative").textContent = item.native;
  $("trRoman").textContent = item.roman;
  playKey(`tr:${item.id}`).catch((e) => toast(e.message));
}
$("trCard").onclick = () => { show("translator"); render(); $("trInput").focus(); };
$("trForm").onsubmit = async (e) => {
  e.preventDefault();
  const text = $("trInput").value.trim();
  if (!text) return;
  try { showTranslation(await post("/api/translate", { lang, text }), text); }
  catch (err) { toast(err.message); }
};
let trRecording = false;
$("trMic").onclick = async () => {
  if (trRecording) return stopNow && stopNow();
  trRecording = true;
  $("trMic").classList.add("live");
  $("trMicLabel").textContent = "Listening… tap to stop";
  try {
    const blob = await record();
    $("trMicLabel").textContent = "Thinking…";
    const form = new FormData();
    form.append("audio", blob, "english.wav");
    form.append("lang", lang);
    const item = await api("/api/translate-audio", { method: "POST", body: form });
    $("trInput").value = item.heard;
    showTranslation(item, item.heard);
  } catch (err) {
    toast(err.name === "NotAllowedError" ? "Please allow the microphone." : err.message);
  }
  trRecording = false;
  $("trMic").classList.remove("live");
  $("trMicLabel").textContent = "Or say it in English";
};
$("trHear").onclick = () => trItem && playKey(`tr:${trItem.id}`).catch((e) => toast(e.message));
$("trPractice").onclick = () => trItem && practiceTranslation(trItem);

async function practiceTranslation(item) {
  const c = C();
  const run = openStage(`Say it in ${c.language_name}`, 1, 0);
  const pseudo = { id: `tr-${item.id}`, ask: item.english, ask_roman: "", target: item.native, target_roman: item.roman, target_en: item.english };
  currentLesson = pseudo;
  currentAsk = `tr:${item.id}`;
  currentSlow = currentAsk;
  currentEn = null;
  await guarded(async () => {
    bubble(`In ${c.language_name} you say`, item.native, item.roman, `“${item.english}”`, true);
    await say(currentAsk, run);
    let result = await listen(pseudo, "translate", run, item.id);
    let stars = 3;
    if (result.label !== "said_it") {
      await say("shared:nevermind", run);
      await say(currentAsk, run);
      result = await listen(pseudo, "translate", run, item.id);
      stars = result.label === "said_it" ? 2 : 1;
    }
    if (stars > 1) { combo += 1; await say(praiseKey(), run); } else { combo = 0; await say(encourageKey(), run); }
    data.progress = await post("/api/score", { lang, xp: XP_FOR[stars], streak: combo });
    renderStats();
    showResult(stars, XP_FOR[stars]);
    $("next").hidden = false;
    $("nextBtn").hidden = true;
  });
}

// ---------- parent tools ----------
$("sendDadi").onclick = () => {
  const learnt = C().lessons.filter((l) => starsOf(l.id)).map((l) => `• ${l.target}`);
  if (!learnt.length) return toast("Finish a phrase first, then send it.");
  const text = lang === "pa-IN"
    ? `ਸਤ ਸ੍ਰੀ ਅਕਾਲ ${C().elder} ਜੀ! ਅੱਜ ਮੈਂ ਪੰਜਾਬੀ ਵਿੱਚ ਇਹ ਬੋਲਣਾ ਸਿੱਖਿਆ:\n${learnt.join("\n")}\nਅੱਜ ਸ਼ਾਮ ਫ਼ੋਨ ਤੇ ਗੱਲ ਕਰਦੇ ਹਾਂ!`
    : `नमस्ते ${C().elder} जी! आज मैंने हिंदी में ये बोलना सीखा:\n${learnt.join("\n")}\nआज शाम फ़ोन पर बात करते हैं!`;
  window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank", "noopener");
};

$("customForm").onsubmit = async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target));
  try {
    await post("/api/custom", { lang, ...form });
    e.target.reset();
    prepared[lang] = false;
    toast("Added. It's now on the path.");
    refresh();
  } catch (err) { toast(err.message); }
};
$("reset").onclick = async () => { await api("/api/reset", { method: "POST" }); combo = 0; refresh(); };

// Make all of Taara's lines once per language, then they replay for free.
const prepared = {};
async function start(fn) {
  if (!prepared[lang]) {
    const slow = setTimeout(() => toast(`Getting ${C().buddy_roman} ready… (only slow the first time)`), 800);
    try { await post("/api/prepare", { lang }); prepared[lang] = true; }
    catch (e) { clearTimeout(slow); return toast(e.message); }
    clearTimeout(slow);
    $("toast").hidden = true;
  }
  fn();
}
$("callCard").onclick = () => start(runCall);
document.querySelectorAll(".langs button").forEach((b) => (b.onclick = () => { lang = b.dataset.lang; greeted = false; render(); }));

// ---------- little ones: listen, find the colour, count ----------
const SWATCH = ["#e53935", "#1e66d0", "#f6c90e", "#2e9e4f"];
const trackItems = (id) => C().tracks.find((t) => t.id === id).items;
const shuffle = (list) => list.map((x) => [Math.random(), x]).sort((a, b) => a[0] - b[0]).map((x) => x[1]);

let listenTrack = "colours";
function renderListen() {
  const tracks = C().tracks;
  if (!tracks.find((t) => t.id === listenTrack)) listenTrack = tracks[0].id;
  $("listenTabs").replaceChildren(...tracks.map((t) => {
    const b = Object.assign(document.createElement("button"), { className: `tab${t.id === listenTrack ? " on" : ""}`, textContent: t.title });
    b.onclick = () => { listenTrack = t.id; renderListen(); };
    return b;
  }));
  const items = trackItems(listenTrack);
  $("listenGrid").replaceChildren(...items.map((item, i) => {
    const b = document.createElement("button");
    b.className = "word-card";
    if (listenTrack === "colours") b.append(Object.assign(document.createElement("span"), { className: "swatch-mini", style: `background:${SWATCH[i]}` }));
    b.append(
      Object.assign(document.createElement("span"), { className: "native", textContent: item.target }),
      Object.assign(document.createElement("span"), { className: "roman", textContent: item.target_roman }),
      Object.assign(document.createElement("small"), { textContent: item.target_en }),
    );
    b.onclick = async () => {
      document.querySelectorAll(".word-card.playing").forEach((x) => x.classList.remove("playing"));
      b.classList.add("playing");
      try { await playKey(`slow:${item.id}`); } catch (e) { toast(e.message); }
    };
    return b;
  }));
}
$("tdListen").onclick = () => { show("listen"); renderListen(); };

async function runFind(kind) {
  const items = trackItems(kind === "colour" ? "colours" : "numbers");
  const rounds = 5;
  const run = openStage(kind === "colour" ? "Find the colour" : "Count with Taara", rounds, 0);
  await guarded(async () => {
    await greet(run);
    let firstTry = 0;
    for (let r = 0; r < rounds; r++) {
      drawDots(rounds, r);
      const target = pick(items);
      const choices = shuffle([target, ...shuffle(items.filter((x) => x !== target)).slice(0, 2)]);
      bubble(kind === "colour" ? "Find the colour" : "Find the number", target.target, target.target_roman, "");
      const buttons = choices.map((item) => {
        const b = document.createElement("button");
        const idx = items.indexOf(item);
        b.setAttribute("aria-label", item.target_en);
        if (kind === "colour") {
          b.className = "opt swatch";
          b.style.background = SWATCH[idx];
        } else {
          b.className = "opt";
          const g = document.createElement("span");
          g.className = "dots-grid";
          for (let k = 0; k <= idx; k++) g.append(document.createElement("i"));
          b.append(g);
        }
        b.dataset.ok = item === target ? "1" : "";
        return b;
      });
      $("options").hidden = false;
      $("options").replaceChildren(...buttons);
      let tries = 0;
      const tapped = new Promise((resolve) => buttons.forEach((b) => (b.onclick = () => {
        if (b.dataset.ok) { b.classList.add("right"); buttons.forEach((x) => (x.disabled = true)); resolve(); return; }
        tries += 1;
        b.classList.remove("wrong");
        void b.offsetWidth;
        b.classList.add("wrong");
        playKey("shared:tryagain").catch(() => {});
      })));
      say(`find:${target.id}`, run).catch(() => {});
      await tapped;
      player.pause();
      if (run !== running) throw new Error("stopped");
      if (!tries) { firstTry += 1; combo += 1; } else combo = 0;
      renderStats();
      confetti(50);
      await say(praiseKey(), run);
    }
    $("options").hidden = true;
    const stars = firstTry >= 4 ? 3 : firstTry >= 2 ? 2 : 1;
    data.progress = await post("/api/score", { lang, xp: 10, streak: combo });
    renderStats();
    showResult(stars, 10, `${firstTry} of ${rounds} on the first try!`);
    $("next").hidden = false;
    $("nextBtn").hidden = false;
    $("nextBtn").textContent = "Play again";
    $("nextBtn").onclick = () => start(() => runFind(kind));
  });
}
$("tdColour").onclick = () => start(() => runFind("colour"));
$("tdCount").onclick = () => start(() => runFind("count"));

// ---------- quick quiz ----------
async function runQuiz() {
  const all = C().tracks.flatMap((t) => t.items);
  const qs = shuffle(all).slice(0, 5);
  const run = openStage("Quick quiz", qs.length, 0);
  await guarded(async () => {
    await greet(run);
    let score = 0;
    for (const [i, q] of qs.entries()) {
      drawDots(qs.length, i);
      bubble("What does this mean?", q.target, q.target_roman, "");
      const wrongs = shuffle(all.filter((x) => x.target_en !== q.target_en)).slice(0, 2);
      const choices = shuffle([q, ...wrongs]);
      const buttons = choices.map((x) => Object.assign(document.createElement("button"), { className: "opt text", textContent: x.target_en }));
      buttons.forEach((b, k) => (b.dataset.ok = choices[k] === q ? "1" : ""));
      $("options").hidden = false;
      $("options").replaceChildren(...buttons);
      const picked = new Promise((resolve) => buttons.forEach((b) => (b.onclick = () => {
        buttons.forEach((x) => { x.disabled = true; if (x.dataset.ok) x.classList.add("right"); });
        if (!b.dataset.ok) b.classList.add("wrong");
        resolve(Boolean(b.dataset.ok));
      })));
      say(`slow:${q.id}`, run).catch(() => {});
      const right = await picked;
      player.pause();
      if (run !== running) throw new Error("stopped");
      if (right) { score += 1; combo += 1; confetti(50); await say(praiseKey(), run); }
      else { combo = 0; await say("shared:nevermind", run); await wait(600); }
      renderStats();
    }
    $("options").hidden = true;
    const stars = score >= 5 ? 3 : score >= 3 ? 2 : 1;
    data.progress = await post("/api/score", { lang, xp: score * 3, streak: combo });
    renderStats();
    showResult(stars, score * 3, `${score} of ${qs.length} right!`);
    $("next").hidden = false;
    $("nextBtn").hidden = false;
    $("nextBtn").textContent = "Play again";
    $("nextBtn").onclick = () => start(runQuiz);
  });
}
$("quizCard").onclick = () => start(runQuiz);

// ---------- voice message for the real relative ----------
function renderMessage() {
  const c = C();
  $("msgTitle").textContent = `Message for ${c.elder_roman}`;
  $("msgIntro").textContent = `Record a voice note for ${c.elder_roman} in ${c.language_name}. You could say:`;
  const learnt = c.lessons.filter((l) => starsOf(l.id));
  const ideas = (learnt.length ? learnt : c.lessons).slice(0, 4);
  $("msgIdeas").replaceChildren(...ideas.map((l) => {
    const d = document.createElement("div");
    d.className = "idea";
    d.append(Object.assign(document.createElement("div"), { className: "native", textContent: l.target }),
      Object.assign(document.createElement("small"), { textContent: [l.target_roman, l.target_en].filter(Boolean).join(" · ") }));
    return d;
  }));
}
$("msgCard").onclick = () => { show("message"); renderMessage(); };
let msgBlob = null;
let msgRecording = false;
$("msgRecord").onclick = async () => {
  if (msgRecording) return stopNow && stopNow();
  msgRecording = true;
  $("msgRecord").classList.add("live");
  $("msgStatus").textContent = "Recording… tap to stop";
  $("msgDone").hidden = true;
  try {
    msgBlob = await record({ quietStop: 4, maxSecs: 45, idleSecs: 10 });
    $("msgAudio").src = URL.createObjectURL(msgBlob);
    $("msgDone").hidden = false;
    $("msgStatus").textContent = "Listen back, then send it";
  } catch (e) {
    toast(e.name === "NotAllowedError" ? "Please allow the microphone." : e.message);
    $("msgStatus").textContent = "Tap to record";
  }
  msgRecording = false;
  $("msgRecord").classList.remove("live");
};
$("msgAgain").onclick = () => { $("msgDone").hidden = true; $("msgStatus").textContent = "Tap to record"; };
$("msgShare").onclick = async () => {
  if (!msgBlob) return;
  const file = new File([msgBlob], `message-for-${C().elder_roman.toLowerCase()}.wav`, { type: "audio/wav" });
  try {
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({ files: [file], title: `Message for ${C().elder_roman}` });
      return;
    }
  } catch (e) { if (e.name === "AbortError") return; }
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(file), download: file.name });
  document.body.append(a);
  a.click();
  a.remove();
  toast("Saved. Attach it in WhatsApp to send it.");
};

// ---------- free talk ----------
let typed = null;
function addMsg(who, item, extra = "") {
  const d = document.createElement("div");
  d.className = `msg ${who}`;
  if (who === "hint") d.append(Object.assign(document.createElement("div"), { className: "label", textContent: extra }));
  d.append(Object.assign(document.createElement("div"), { className: "native", textContent: item.native || item.text }));
  if (item.roman) d.append(Object.assign(document.createElement("div"), { className: "roman", textContent: item.roman }));
  if (item.english && who === "them") d.append(Object.assign(document.createElement("div"), { className: "en", textContent: item.english }));
  $("chatLog").append(d);
  d.scrollIntoView({ behavior: "smooth", block: "end" });
}

async function runChat() {
  const c = C();
  const run = openStage(`Pretend game: ${c.buddy_roman} plays ${c.elder_roman}`, 0, 0);
  currentMode = "chat";
  currentEn = null;
  const history = [];
  let ended = false;
  let englishTurns = 0;
  $("chatEnd").onclick = () => { ended = true; if (stopNow) stopNow(); };
  await guarded(async () => {
    await greet(run);
    $("chatLog").hidden = false;
    $("chatLog").replaceChildren();
    $("turn").classList.add("chat");
    const opener = c.lessons.find((l) => l.id === "hello");
    addMsg("them", { native: opener.ask, roman: opener.ask_roman, english: opener.ask_en });
    history.push({ who: "them", text: opener.ask });
    await say(`q:${opener.id}`, run);
    for (let turn = 0; turn < 10 && !ended; turn++) {
      if (run !== running) throw new Error("stopped");
      $("chatForm").hidden = false;
      $("turn").hidden = false;
      typed = null;
      let blob = null;
      try { blob = await record({ quietStop: 1.5, maxSecs: 20, idleSecs: 15 }); }
      catch (e) { throw e.name === "NotAllowedError" ? new Error("Please allow the microphone.") : e; }
      $("turn").hidden = true;
      if (ended || run !== running) break;
      const form = new FormData();
      form.append("lang", lang);
      form.append("history", JSON.stringify(history));
      if (typed) form.append("text", typed); else form.append("audio", blob, "talk.wav");
      $("chatForm").hidden = true;
      const out = await api("/api/chat", { method: "POST", body: form });
      if (!out.heard) { toast("I didn't hear anything. Try again, or type."); turn -= 1; continue; }
      addMsg("me", { text: out.heard });
      history.push({ who: "me", text: out.heard });
      if (out.hint) {
        // The child spoke English: show the family-language version and have them say it before the relative replies.
        englishTurns += 1;
        addMsg("hint", out.hint, `In ${c.language_name} you can say`);
        await say(englishTurns >= 2 ? "shared:hindi_please" : "shared:english", run);
        currentAsk = `tr:${out.hint.id}`;
        await say(currentAsk, run);
        const pseudo = { id: "free-talk", ask: out.heard, ask_roman: "", target: out.hint.native, target_roman: out.hint.roman };
        const again = await listen(pseudo, "chat", run, out.hint.id);
        if (again.label === "said_it") {
          englishTurns = 0;
          combo += 1;
          addMsg("me", { text: again.heard });
        } else {
          combo = 0;
          await say(encourageKey(), run);
        }
        renderStats();
        $("heard").hidden = true;
      } else {
        englishTurns = 0;
      }
      addMsg("them", out.reply);
      history.push({ who: "them", text: out.reply.native });
      await say(`chat:${out.reply.id}`, run);
      combo += 1;
      renderStats();
    }
    $("chatForm").hidden = true;
    $("turn").hidden = true;
    $("turn").classList.remove("chat");
    const turns = history.filter((h) => h.who === "me").length;
    await say("shared:ready", run);
    data.progress = await post("/api/score", { lang, xp: Math.min(25, turns * 3), streak: combo });
    renderStats();
    showResult(turns >= 5 ? 3 : turns >= 2 ? 2 : 1, Math.min(25, turns * 3), `You talked ${turns} times. Now call your real ${c.elder_roman}!`);
    $("next").hidden = false;
    $("nextBtn").hidden = false;
    $("nextBtn").textContent = "Talk again";
    $("nextBtn").onclick = () => start(runChat);
  });
  $("turn").classList.remove("chat");
}
$("chatForm").onsubmit = (e) => {
  e.preventDefault();
  const text = $("chatInput").value.trim();
  if (!text || !stopNow) return;
  typed = text;
  $("chatInput").value = "";
  stopNow();
};
$("chatCard").onclick = () => start(runChat);

// ---------- child profile ----------
$("editName").onclick = () => { show("parents"); render(); $("profileForm").elements.namedItem("name").focus(); };
$("profileForm").onsubmit = async (e) => {
  e.preventDefault();
  const f = e.target.elements;
  try {
    data.progress = await post("/api/profile", { name: f.namedItem("name").value, gender: f.namedItem("gender").value });
    greeted = false;
    toast("Saved");
    refresh();
  } catch (err) { toast(err.message); }
};

icons();
refresh().catch((e) => toast(e.message));
