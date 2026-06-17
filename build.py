#!/usr/bin/env python3
"""build.py — sinh index.html từ data/site-data.json (FOTW-EL static site).
Tách data khỏi HTML để tránh lỗi cắt-dán chuỗi (bài học org-site)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "data", "site-data.json")))

# nhúng DATA dạng JSON an toàn (không string-concat thủ công)
data_js = json.dumps(DATA, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>FOTW-EL · Funnel Library (nội bộ)</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:#58a6ff;text-decoration:none}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 80px}
.hd{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.hd h1{font-size:22px;font-weight:700}
.sub{color:#8b949e;font-size:13px;margin-bottom:20px}
.stats{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.pill{background:#161b22;border:1px solid #30363d;border-radius:20px;padding:5px 13px;font-size:12.5px;color:#c9d1d9;cursor:pointer;transition:.15s;user-select:none}
.pill:hover{border-color:#58a6ff}
.pill.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:14px;cursor:pointer;transition:.15s;position:relative}
.card:hover{border-color:#58a6ff;transform:translateY(-2px)}
.card .em{font-size:26px;margin-bottom:6px}
.card .nm{font-weight:600;font-size:15px;margin-bottom:4px}
.card .ty{font-size:11.5px;color:#8b949e}
.badge{position:absolute;top:10px;right:10px;font-size:10px;padding:2px 7px;border-radius:10px;background:#238636;color:#fff;font-weight:600}
.badge.todo{background:#30363d;color:#8b949e}
.det{display:none;background:#0d1117;border:1px solid #30363d;border-radius:12px;margin-top:14px;padding:0;overflow:hidden}
.det.open{display:block}
.det-hd{background:#161b22;padding:16px 18px;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:12px}
.det-hd .em{font-size:32px}
.det-hd h2{font-size:19px}
.det-hd .web{font-size:12.5px;color:#8b949e}
.sec{border-bottom:1px solid #21262d}
.sec-h{padding:12px 18px;font-weight:600;font-size:14px;color:#f0883e;background:#13171d;cursor:pointer;user-select:none}
.les{padding:14px 18px;border-top:1px solid #21262d;display:none}
.les.open{display:block}
.les-t{font-weight:600;font-size:14px;margin-bottom:8px;color:#79c0ff;cursor:pointer}
.les-x{font-size:13.5px;color:#c9d1d9;white-space:pre-wrap;margin-bottom:8px}
.les img{max-width:100%;border-radius:8px;margin:6px 0;border:1px solid #30363d}
.les iframe{width:100%;height:340px;border:1px solid #30363d;border-radius:8px;margin:6px 0}
.close{float:right;color:#8b949e;cursor:pointer;font-size:18px}
.empty{color:#8b949e;font-style:italic;padding:10px 0}
</style>
</head>
<body>
<div class="wrap">
  <div class="hd"><span style="font-size:28px">🔬</span><h1>FOTW-EL · Funnel Library</h1></div>
  <div class="sub">Clone nội bộ Funnel of the Week — thư viện phân tích funnel DTC · <span id="meta"></span></div>
  <div class="stats" id="filters"></div>
  <div id="detailHost"></div>
  <div class="grid" id="grid"></div>
</div>
<script>
const DATA = __DATA__;
let activeType = "all";

function typeCounts(){
  const c={}; DATA.funnels.forEach(f=>{c[f.type]=(c[f.type]||0)+1});
  return c;
}
function renderFilters(){
  const c=typeCounts();
  const types=Object.keys(c).sort((a,b)=>c[b]-c[a]);
  const host=document.getElementById("filters");
  const all=`<span class="pill ${activeType==='all'?'on':''}" data-t="all">Tất cả ${DATA.funnels.length}</span>`;
  host.innerHTML=all+types.map(t=>`<span class="pill ${activeType===t?'on':''}" data-t="${t}">${t} ${c[t]}</span>`).join("");
  host.querySelectorAll(".pill").forEach(p=>p.onclick=()=>{activeType=p.dataset.t;renderFilters();renderGrid();});
}
function renderGrid(){
  const g=document.getElementById("grid");
  const list=DATA.funnels.filter(f=>activeType==="all"||f.type===activeType);
  g.innerHTML=list.map((f,idx)=>`
    <div class="card" data-slug="${f.slug}">
      <div class="badge ${f.done?'':'todo'}">${f.done?'✓ Full':'· list'}</div>
      <div class="em">${f.emoji||'📋'}</div>
      <div class="nm">${f.name}</div>
      <div class="ty">${f.rawType||f.type}</div>
    </div>`).join("");
  g.querySelectorAll(".card").forEach(c=>c.onclick=()=>openDetail(c.dataset.slug));
}
function esc(s){return (s||"").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function openDetail(slug){
  const f=DATA.funnels.find(x=>x.slug===slug);
  const host=document.getElementById("detailHost");
  if(!f.done||!f.sections){
    host.innerHTML=`<div class="det open"><div class="det-hd"><span class="em">${f.emoji}</span><div><h2>${f.name}</h2><div class="web">${f.rawType} · chưa scrape chi tiết</div></div><span class="close" onclick="document.getElementById('detailHost').innerHTML=''">✕</span></div><div style="padding:18px" class="empty">Breakdown chi tiết chưa được scrape. Mở bản gốc: <a href="${f.url}" target="_blank">${f.url}</a></div></div>`;
    host.scrollIntoView({behavior:"smooth"});return;
  }
  const secs=f.sections.map((s,si)=>`
    <div class="sec">
      <div class="sec-h" onclick="this.parentNode.querySelectorAll('.les').forEach(l=>l.classList.toggle('open'))">▸ ${s.name} (${s.lessons.length})</div>
      ${s.lessons.map(l=>`
        <div class="les ${si===0?'open':''}">
          <div class="les-t" onclick="this.parentNode.classList.toggle('open')">${l.title}</div>
          <div class="les-x">${esc(l.text)}</div>
          ${(l.images||[]).map(im=>`<img src="${im}" loading="lazy">`).join("")}
          ${(l.iframes||[]).map(fr=>`<iframe src="${fr}" loading="lazy" allowfullscreen></iframe>`).join("")}
        </div>`).join("")}
    </div>`).join("");
  host.innerHTML=`<div class="det open">
    <div class="det-hd"><span class="em">${f.emoji}</span><div><h2>${f.name}</h2><div class="web">${f.rawType} · <a href="https://${f.website}" target="_blank">${f.website||''}</a></div></div><span class="close" onclick="document.getElementById('detailHost').innerHTML=''">✕</span></div>
    ${secs}
  </div>`;
  host.scrollIntoView({behavior:"smooth"});
}
document.getElementById("meta").textContent = DATA.meta.scraped+"/"+DATA.meta.total+" scraped đầy đủ";
renderFilters(); renderGrid();
</script>
</body>
</html>"""

out = HTML.replace("__DATA__", data_js)
open(os.path.join(HERE, "index.html"), "w").write(out)
print(f"✓ index.html built — {DATA['meta']['total']} funnel, {DATA['meta']['scraped']} full")
