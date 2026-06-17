#!/usr/bin/env python3
"""build.py — sinh index.html từ data/site-data.json.
Clone UX/UI Funnel of the Week (light theme, top nav, filter chips, grid thumbnail,
lesson 2-cột curriculum). Responsive PC + mobile. Data tách JSON (parse-safe)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "data", "site-data.json")))
data_js = json.dumps(DATA, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>FOTW-EL · Funnel Library</title>
<style>
:root{
  --bg:#f7f9fa; --card:#fff; --ink:#1c1c1e; --ink2:#6b7280; --line:#e5e7eb;
  --accent:#1f6feb; --accent2:#7c3aed; --shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --radius:14px; --nav-h:60px;
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
html,body{background:var(--bg);color:var(--ink);font:15px/1.55 InterVariable,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent);text-decoration:none}
img{max-width:100%}
/* ---- TOP NAV ---- */
.nav{position:sticky;top:0;z-index:50;height:var(--nav-h);background:var(--card);border-bottom:1px solid var(--line);
  display:flex;align-items:center;gap:14px;padding:0 18px}
.nav .logo{font-weight:800;font-size:17px;letter-spacing:.5px;cursor:pointer;white-space:nowrap}
.nav .logo span{color:var(--accent2)}
.nav .tabs{display:flex;gap:4px;margin-left:8px}
.nav .tab{padding:7px 13px;border-radius:20px;font-size:13.5px;color:var(--ink2);cursor:pointer;font-weight:500}
.nav .tab.on{background:#eef2ff;color:var(--accent)}
.nav .grow{flex:1}
.nav .search{display:flex;align-items:center;gap:7px;background:var(--bg);border:1px solid var(--line);border-radius:20px;padding:7px 13px;min-width:140px;color:var(--ink2);font-size:13px}
.nav .search input{border:0;background:transparent;outline:0;font-size:13.5px;width:100%;color:var(--ink)}
.nav .av{width:32px;height:32px;border-radius:50%;background:var(--accent2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}
/* ---- WRAP ---- */
.wrap{max-width:1180px;margin:0 auto;padding:22px 18px 90px}
.hero{background:linear-gradient(120deg,#7c3aed,#db2777);border-radius:var(--radius);padding:30px 28px;color:#fff;margin-bottom:20px;box-shadow:var(--shadow)}
.hero h1{font-size:26px;font-weight:800;margin-bottom:6px}
.hero p{opacity:.92;font-size:14.5px}
/* ---- FILTER CHIPS (premium) ---- */
.chips-wrap{margin-bottom:22px}
.chips-lbl{font-size:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--ink2);margin-bottom:11px;display:flex;align-items:center;gap:7px}
.chips-lbl::before{content:"";width:18px;height:2px;background:linear-gradient(90deg,var(--accent2),var(--accent));border-radius:2px}
.chips{display:flex;gap:9px;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:7px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 14px;font-size:13.5px;color:#374151;cursor:pointer;
  transition:transform .15s cubic-bezier(.34,1.56,.64,1),box-shadow .2s,border-color .2s,background .2s;white-space:nowrap;user-select:none;font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.chip .ico{font-size:15px;line-height:1}
.chip .cnt{font-size:11.5px;font-weight:700;background:var(--bg);color:var(--ink2);border-radius:8px;padding:1px 7px;min-width:20px;text-align:center;transition:.2s}
.chip:hover{border-color:#c7d2fe;transform:translateY(-2px);box-shadow:0 6px 16px rgba(79,70,229,.12)}
.chip.on{background:linear-gradient(135deg,#7c3aed,#4f46e5);border-color:transparent;color:#fff;box-shadow:0 6px 18px rgba(99,102,241,.35);transform:translateY(-1px)}
.chip.on .cnt{background:rgba(255,255,255,.22);color:#fff}
/* ---- GRID ---- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;cursor:pointer;transition:.18s;box-shadow:var(--shadow);display:flex;flex-direction:column}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.10)}
.card .thumb{aspect-ratio:16/10;background:linear-gradient(135deg,#a78bfa,#f0abfc);position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}
.card .thumb img{width:100%;height:100%;object-fit:cover}
.card .thumb .em{font-size:46px}
.card .bd{padding:13px 15px}
.card .nm{font-weight:700;font-size:15px;margin-bottom:3px;color:var(--ink)}
.card .ty{font-size:12px;color:var(--ink2)}
.card .badge{position:absolute;top:9px;right:9px;font-size:10px;padding:3px 8px;border-radius:10px;background:#16a34a;color:#fff;font-weight:700;letter-spacing:.3px}
.card .badge.todo{background:rgba(0,0,0,.45);backdrop-filter:blur(4px)}
/* ---- DETAIL (lesson view 2-cột) ---- */
.overlay{position:fixed;inset:0;z-index:100;background:var(--bg);display:none;flex-direction:column}
.overlay.open{display:flex}
.ov-top{height:var(--nav-h);background:var(--card);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:0 18px;flex-shrink:0}
.ov-top .back{cursor:pointer;font-size:20px;color:var(--ink);padding:4px 8px;border-radius:8px}
.ov-top .back:hover{background:var(--bg)}
.ov-top h2{font-size:16px;font-weight:700}
.ov-top .grow{flex:1}
.ov-body{flex:1;display:flex;overflow:hidden}
.ov-content{flex:1;overflow-y:auto;padding:28px 32px;-webkit-overflow-scrolling:touch}
.ov-content .lhd{color:var(--ink2);font-size:13px;margin-bottom:6px}
.ov-content .ltitle{font-size:23px;font-weight:800;margin-bottom:18px;display:flex;align-items:center;gap:10px}
.ov-content .ltext{font-size:15.5px;line-height:1.7;white-space:pre-wrap;color:#2c2c2e}
.ov-content .ltext a{color:var(--accent);font-weight:600}
.ov-content img{border-radius:10px;border:1px solid var(--line);margin:14px 0;display:block}
.ov-content .embed{margin:14px 0}
.ov-content iframe{width:100%;height:420px;border:1px solid var(--line);border-radius:10px}
.ov-content .embed-link{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0;font-size:13.5px}
/* curriculum sidebar phải */
.ov-side{width:320px;background:var(--card);border-left:1px solid var(--line);overflow-y:auto;flex-shrink:0}
.ov-side .sh{padding:16px 18px 10px;font-weight:700;font-size:15px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--card);display:flex;align-items:center;justify-content:space-between}
.sec-block{border-bottom:1px solid var(--line)}
.sec-name{padding:12px 18px 8px;font-weight:700;font-size:13px;color:var(--ink2);text-transform:uppercase;letter-spacing:.4px}
.les-item{padding:9px 18px 9px 18px;display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13.5px;color:#374151;border-left:3px solid transparent}
.les-item:hover{background:var(--bg)}
.les-item.on{background:#eef2ff;border-left-color:var(--accent);color:var(--accent);font-weight:600}
.les-item .dot{width:16px;height:16px;border:2px solid var(--line);border-radius:50%;flex-shrink:0}
.les-item.on .dot{border-color:var(--accent)}
.nav-arrows{display:flex;gap:8px;margin-left:auto}
.nav-arrows button{width:34px;height:34px;border:1px solid var(--line);background:var(--card);border-radius:8px;cursor:pointer;font-size:15px;color:var(--ink)}
.nav-arrows button:hover{background:var(--bg)}
.nav-arrows button:disabled{opacity:.35;cursor:default}
.empty{color:var(--ink2);font-style:italic;padding:40px 0;text-align:center}
.mob-cur-btn{display:none}
/* ---- RESPONSIVE: TABLET ---- */
@media(max-width:900px){
  .ov-side{width:280px}
  .nav .search{min-width:90px}
}
/* ---- RESPONSIVE: MOBILE ---- */
@media(max-width:680px){
  .nav{gap:8px;padding:0 12px}
  .nav .tabs{display:none}
  .nav .logo{font-size:15px}
  .nav .search{min-width:0;width:38px;padding:7px;justify-content:center}
  .nav .search input{display:none}
  .wrap{padding:16px 12px 80px}
  .hero{padding:22px 18px}
  .hero h1{font-size:21px}
  /* filter: thanh cuộn ngang 1 hàng (native app style) */
  .chips-wrap{margin-bottom:18px;margin-left:-12px;margin-right:-12px}
  .chips-lbl{padding:0 12px}
  .chips{flex-wrap:nowrap;overflow-x:auto;scroll-snap-type:x proximity;padding:2px 12px 8px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .chips::-webkit-scrollbar{display:none}
  .chip{scroll-snap-align:start;flex-shrink:0;padding:9px 15px}
  .grid{grid-template-columns:1fr 1fr;gap:11px}
  .card .bd{padding:10px 11px}
  .card .nm{font-size:13.5px}
  .card .ty{font-size:11px}
  /* lesson view: content full, curriculum thành drawer */
  .ov-content{padding:18px 16px}
  .ov-content .ltitle{font-size:19px}
  .ov-side{position:fixed;top:var(--nav-h);right:0;bottom:0;width:84%;max-width:340px;transform:translateX(100%);transition:.25s;z-index:120;box-shadow:-4px 0 20px rgba(0,0,0,.15)}
  .ov-side.open{transform:translateX(0)}
  .ov-content iframe{height:300px}
  .mob-cur-btn{display:flex;align-items:center;gap:6px;background:var(--ink);color:#fff;border:0;border-radius:20px;padding:8px 14px;font-size:13px;cursor:pointer;font-weight:600}
}
@media(max-width:400px){
  .grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="nav">
  <div class="logo" onclick="closeDetail()">F<span>UNNEL</span> · EL</div>
  <div class="tabs"><div class="tab on">📚 Filter Funnels</div></div>
  <div class="grow"></div>
  <div class="search">🔍<input id="q" placeholder="Tìm funnel..." oninput="onSearch(this.value)"></div>
  <div class="av">EL</div>
</div>
<div class="wrap" id="home">
  <div class="hero"><h1>Funnel Library 🔬</h1><p id="heroSub"></p></div>
  <div class="chips-wrap"><div class="chips-lbl">Lọc theo loại funnel</div><div class="chips" id="chips"></div></div>
  <div class="grid" id="grid"></div>
</div>

<!-- lesson overlay -->
<div class="overlay" id="overlay">
  <div class="ov-top">
    <span class="back" onclick="closeDetail()">←</span>
    <h2 id="ovTitle"></h2>
    <div class="grow"></div>
    <button class="mob-cur-btn" onclick="toggleCur()">☰ Lessons</button>
    <div class="nav-arrows"><button id="prevBtn" onclick="step(-1)">←</button><button id="nextBtn" onclick="step(1)">→</button></div>
  </div>
  <div class="ov-body">
    <div class="ov-content" id="ovContent"></div>
    <div class="ov-side" id="ovSide"></div>
  </div>
</div>

<script>
const DATA = __DATA__;
let activeType="all", search="", curFunnel=null, flatLessons=[], curIdx=0;

const TYPE_ICON={"eCom":"🛒","Info Product":"📘","Quiz":"❓","Advertorial":"📰","VSL":"🎬","eCom Quiz":"🛒","Advertorial Quiz":"📰","Book":"📚","SaaS":"💻","Call":"📞","Agency":"🏢","Lead Gen":"🎯"};
function typeCounts(){const c={};DATA.funnels.forEach(f=>c[f.type]=(c[f.type]||0)+1);return c;}
function renderChips(){
  const c=typeCounts(), types=Object.keys(c).sort((a,b)=>c[b]-c[a]);
  const all=`<span class="chip ${activeType==='all'?'on':''}" onclick="setType('all')"><span class="ico">🗂️</span>Tất cả<span class="cnt">${DATA.funnels.length}</span></span>`;
  document.getElementById("chips").innerHTML=all+
    types.map(t=>`<span class="chip ${activeType===t?'on':''}" onclick="setType('${t}')"><span class="ico">${TYPE_ICON[t]||'📋'}</span>${t}<span class="cnt">${c[t]}</span></span>`).join("");
}
function setType(t){activeType=t;renderChips();renderGrid();}
function onSearch(v){search=v.toLowerCase();renderGrid();}
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function linkify(s){return esc(s).replace(/(https?:\/\/[^\s]+)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>');}
function renderGrid(){
  let list=DATA.funnels.filter(f=>activeType==="all"||f.type===activeType);
  if(search) list=list.filter(f=>f.name.toLowerCase().includes(search)||f.rawType.toLowerCase().includes(search));
  document.getElementById("grid").innerHTML=list.map(f=>`
    <div class="card" onclick="openDetail('${f.slug}')">
      <div class="thumb">
        <div class="badge ${f.done?'':'todo'}">${f.done?'✓ Full':'list'}</div>
        ${f.thumb?`<img src="${f.thumb}" loading="lazy" onerror="this.style.display='none';this.parentNode.innerHTML+='<div class=em>${f.emoji||'📋'}</div>'">`:`<div class="em">${f.emoji||'📋'}</div>`}
      </div>
      <div class="bd"><div class="nm">${f.emoji||''} ${f.name}</div><div class="ty">${f.rawType}</div></div>
    </div>`).join("")||`<div class="empty">Không có funnel khớp.</div>`;
}
function openDetail(slug){
  const f=DATA.funnels.find(x=>x.slug===slug); curFunnel=f;
  document.getElementById("ovTitle").textContent=(f.emoji||'')+" "+f.name;
  const ov=document.getElementById("overlay"); ov.classList.add("open");
  if(!f.done||!f.sections){
    document.getElementById("ovSide").innerHTML="";
    document.getElementById("ovContent").innerHTML=`<div class="empty">📋 Breakdown chi tiết chưa scrape.<br><br>Loại: ${f.rawType}</div>`;
    return;
  }
  // flatten lessons
  flatLessons=[]; f.sections.forEach((s,si)=>s.lessons.forEach((l,li)=>flatLessons.push({...l,section:s.name,si,li})));
  curIdx=0; renderSide(); renderLesson();
}
function renderSide(){
  const f=curFunnel;
  let html=`<div class="sh">Lessons <span style="cursor:pointer;color:var(--ink2)" onclick="toggleCur()" class="mob-only">✕</span></div>`;
  f.sections.forEach((s,si)=>{
    html+=`<div class="sec-block"><div class="sec-name">${s.name}</div>`;
    s.lessons.forEach((l,li)=>{
      const idx=flatLessons.findIndex(x=>x.si===si&&x.li===li);
      html+=`<div class="les-item ${idx===curIdx?'on':''}" data-idx="${idx}" onclick="goLesson(${idx})"><span class="dot"></span>${l.title}</div>`;
    });
    html+=`</div>`;
  });
  document.getElementById("ovSide").innerHTML=html;
}
function renderLesson(){
  const l=flatLessons[curIdx]; if(!l)return;
  let media=(l.media||[]).map(m=>{
    if(m.type==='img')return `<img src="${m.url}" loading="lazy">`;
    if(/youtube|youtu\.be|vimeo|loom/.test(m.url))return `<div class="embed"><iframe src="${m.url.replace('watch?v=','embed/')}" loading="lazy" allowfullscreen></iframe></div>`;
    if(/drive\.google/.test(m.url)){const id=(m.url.match(/[-\w]{25,}/)||[])[0];return id?`<div class="embed"><iframe src="https://drive.google.com/file/d/${id}/preview" loading="lazy"></iframe></div>`:`<a class="embed-link" href="${m.url}" target="_blank">📎 ${m.url.slice(0,50)}</a>`;}
    return `<a class="embed-link" href="${m.url}" target="_blank">🔗 ${m.url.slice(0,55)}</a>`;
  }).join("");
  document.getElementById("ovContent").innerHTML=`
    <div class="lhd">Lesson ${curIdx+1} of ${flatLessons.length} · ${l.section}</div>
    <div class="ltitle">${l.title}</div>
    <div class="ltext">${linkify(l.text)||'<span style="color:var(--ink2)">(Lesson chủ yếu hình ảnh bên dưới)</span>'}</div>
    ${media}`;
  document.getElementById("ovContent").scrollTop=0;
  document.getElementById("prevBtn").disabled=curIdx===0;
  document.getElementById("nextBtn").disabled=curIdx===flatLessons.length-1;
  document.querySelectorAll(".les-item").forEach(e=>e.classList.toggle("on",+e.dataset.idx===curIdx));
}
function goLesson(i){curIdx=i;renderLesson();if(window.innerWidth<=680)document.getElementById("ovSide").classList.remove("open");}
function step(d){const n=curIdx+d;if(n>=0&&n<flatLessons.length){curIdx=n;renderLesson();}}
function toggleCur(){document.getElementById("ovSide").classList.toggle("open");}
function closeDetail(){document.getElementById("overlay").classList.remove("open");}
document.addEventListener("keydown",e=>{if(!document.getElementById("overlay").classList.contains("open"))return;if(e.key==="ArrowLeft")step(-1);if(e.key==="ArrowRight")step(1);if(e.key==="Escape")closeDetail();});
document.getElementById("heroSub").textContent=`${DATA.meta.total} funnel DTC · ${DATA.meta.scraped} breakdown đầy đủ · clone nội bộ`;
renderChips();renderGrid();
</script>
</body>
</html>"""

out = HTML.replace("__DATA__", data_js)
open(os.path.join(HERE, "index.html"), "w").write(out)
print(f"✓ index.html built — {DATA['meta']['total']} funnel, {DATA['meta']['scraped']} full")
