<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
<title>CPU Cycle Lab</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>
:root{
  --bg:#E9EDE8; --panel:#F8FAF6; --panel-2:#EEF2EC; --ink:#16201B; --muted:#5A6760; --line:#C6CFC8;
  --copper:#A9561F; --copper-soft:#F3DFCF;
  --addr:#2A62C4; --data:#A87706; --ctrl:#A8336F;
  --good:#1D7F47; --good-soft:#D6EEDF; --bad:#BC3A2C; --bad-soft:#F6DAD5;
  --display:"Bricolage Grotesque", "Arial Narrow", system-ui, sans-serif;
  --body:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono:"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --dur:700ms;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0D1311; --panel:#141C19; --panel-2:#1A2420; --ink:#E2EAE4; --muted:#8F9D95; --line:#2A3632;
    --copper:#E38D52; --copper-soft:#3A2618;
    --addr:#76A2F2; --data:#E3B745; --ctrl:#E77BB2;
    --good:#5CC98A; --good-soft:#15301F; --bad:#F07A6A; --bad-soft:#3A1B17;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0D1311; --panel:#141C19; --panel-2:#1A2420; --ink:#E2EAE4; --muted:#8F9D95; --line:#2A3632;
  --copper:#E38D52; --copper-soft:#3A2618;
  --addr:#76A2F2; --data:#E3B745; --ctrl:#E77BB2;
  --good:#5CC98A; --good-soft:#15301F; --bad:#F07A6A; --bad-soft:#3A1B17;
}
*{box-sizing:border-box}
body{background:var(--bg); color:var(--ink); font-family:var(--body); font-size:15px; line-height:1.5}
.app{max-width:1400px; margin:0 auto; padding-inline:20px; padding-block:18px 40px; display:flex; flex-direction:column; gap:16px}
button{font:inherit; color:inherit; cursor:pointer}
button:focus-visible, textarea:focus-visible, input:focus-visible, select:focus-visible{outline:2px solid var(--copper); outline-offset:2px}
.mono{font-family:var(--mono)}

/* header */
.top{display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:12px 24px}
.brand h1{font-family:var(--display); font-weight:800; font-size:clamp(28px,4vw,40px); line-height:1; margin:0; letter-spacing:-.01em; text-wrap:balance}
.brand p{margin:6px 0 0; color:var(--muted); font-size:13px}
.brand p b{color:var(--ink); font-weight:600}
.stages{display:flex; gap:6px; flex-wrap:wrap}
.stage{font-family:var(--mono); font-size:13px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; padding:6px 12px; border-radius:999px; border:1.5px solid var(--line); color:var(--muted); transition:all .2s}
.stage.on{background:var(--copper); border-color:var(--copper); color:#fff}
.stage.halt.on{background:var(--ink); border-color:var(--ink); color:var(--bg)}

/* machine */
.machine{display:grid; grid-template-columns:minmax(0,1.25fr) minmax(170px,.6fr) minmax(0,1fr); gap:0; align-items:stretch}
.panel{background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px}
.panel-h{display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:10px}
.tag{font-family:var(--display); font-weight:800; font-size:20px; background:none; border:0; padding:0; text-align:left}
.tag:hover{color:var(--copper)}
.chip{font-family:var(--mono); font-size:12px; border:1px solid var(--line); background:var(--panel-2); border-radius:6px; padding:3px 8px}
.chip:hover{border-color:var(--copper)}
.cpu{border:2px solid var(--ink)}
.units{display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px}
.unit,.reg{background:var(--panel-2); border:1.5px solid var(--line); border-radius:8px; padding:8px 10px; text-align:left; display:flex; flex-direction:column; gap:2px; transition:border-color .2s, background .2s; min-width:0}
.unit:hover,.reg:hover{border-color:var(--copper)}
.lbl{font-family:var(--mono); font-size:12px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; color:var(--muted)}
.unit .val{font-family:var(--mono); font-size:15px; font-weight:600; min-height:1.5em; overflow-wrap:anywhere}
.regs{display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:8px}
.reg .val{font-family:var(--mono); font-size:clamp(20px,2.4vw,28px); font-weight:700; line-height:1.15; font-variant-numeric:tabular-nums}
.reg .val .op{color:var(--copper)}
.reg .sub{font-size:11px; color:var(--muted); line-height:1.2}
.hot{border-color:var(--copper)!important; background:var(--copper-soft)!important}
.caches{display:grid; grid-template-columns:minmax(96px,2.4fr) 4fr 8fr; gap:8px; margin-top:10px; padding-top:10px; border-top:1px dashed var(--line)}
.cache{border:1.5px solid var(--line); border-radius:8px; padding:6px; transition:border-color .2s, background .2s; min-width:0}
.cache-h{background:none; border:0; padding:0; display:flex; justify-content:space-between; width:100%; gap:4px; margin-bottom:5px}
.cache-h .lbl{color:var(--ink)}
.cache-h .cost{font-family:var(--mono); font-size:11px; color:var(--muted); white-space:nowrap}
.slots{display:grid; gap:4px}
#s-l1{grid-template-columns:repeat(2,1fr)} #s-l2{grid-template-columns:repeat(4,1fr)} #s-l3{grid-template-columns:repeat(8,1fr)}
.slot{font-family:var(--mono); font-size:11px; text-align:center; background:var(--panel-2); border-radius:4px; padding:3px 0; line-height:1.25; min-width:0}
.slot b{display:block; font-size:10px; color:var(--muted); font-weight:400}
.slot.empty{color:var(--line)}
.cache.hit{border-color:var(--good); background:var(--good-soft)}
.cache.miss{border-color:var(--bad); background:var(--bad-soft)}
.caches.off{opacity:.35}
.cache-note{grid-column:1/-1; font-size:11px; color:var(--muted); margin:0}

.buses{display:flex; flex-direction:column; justify-content:center; gap:18px; padding:0 10px}
.lane{background:none; border:0; padding:0; text-align:left; display:flex; flex-direction:column; gap:4px; width:100%}
.lane-lbl{font-family:var(--mono); font-size:11px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; display:flex; justify-content:space-between; gap:6px}
.lane-lbl i{font-style:normal; font-weight:400; color:var(--muted); text-transform:none; letter-spacing:0}
.track{position:relative; height:30px; border-radius:6px; background:var(--panel-2); border:1.5px solid var(--line); transition:all .2s}
.track::before{content:""; position:absolute; left:8px; right:8px; top:50%; height:3px; margin-top:-1.5px; border-radius:2px; background:var(--line)}
.lane[data-bus="address"]{--c:var(--addr)} .lane[data-bus="data"]{--c:var(--data)} .lane[data-bus="control"]{--c:var(--ctrl)}
.lane .lane-lbl span:first-child{color:var(--c)}
.lane.lit .track{border-color:var(--c)}
.lane.lit .track::before{background:var(--c)}
.pkt{position:absolute; top:50%; left:0; transform:translate(0,-50%); opacity:0; font-family:var(--mono); font-size:13px; font-weight:700; color:#fff; background:var(--c); padding:2px 8px; border-radius:4px; white-space:nowrap}
.pkt.go-r{left:100%; transform:translate(-100%,-50%); opacity:1; animation:pr var(--dur) ease-in-out}
.pkt.go-l{left:0; transform:translate(0,-50%); opacity:1; animation:pl var(--dur) ease-in-out}
@keyframes pr{from{left:0; transform:translate(0,-50%)} to{left:100%; transform:translate(-100%,-50%)}}
@keyframes pl{from{left:100%; transform:translate(-100%,-50%)} to{left:0; transform:translate(0,-50%)}}
.ends{display:flex; justify-content:space-between; font-family:var(--mono); font-size:10px; color:var(--muted); margin-top:-2px}

.mem .ram{display:grid; grid-template-columns:repeat(10,minmax(0,1fr)); gap:3px}
.cell{background:var(--panel-2); border:1.5px solid transparent; border-radius:4px; padding:2px 0 3px; text-align:center; line-height:1.1; min-width:0; transition:background .2s,border-color .2s}
.cell b{display:block; font-family:var(--mono); font-size:9px; font-weight:400; color:var(--muted)}
.cell span{font-family:var(--mono); font-size:12.5px; font-weight:600; font-variant-numeric:tabular-nums}
.cell.zero span{color:var(--muted); font-weight:400}
.cell.is-pc{border-color:var(--copper)}
.cell.is-pc b{color:var(--copper); font-weight:700}
.cell.rd{background:var(--data); } .cell.rd span,.cell.rd b{color:#fff}
.cell.wr{background:var(--ctrl); } .cell.wr span,.cell.wr b{color:#fff}
.cell.cached::after{content:""; display:block; width:4px; height:4px; border-radius:50%; background:var(--good); margin:1px auto 0}
.memfoot{display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:8px; margin-top:10px}
.out{display:flex; flex-wrap:wrap; gap:4px; align-items:center; font-family:var(--mono); font-size:13px}
.out .o{background:var(--ink); color:var(--bg); padding:1px 7px; border-radius:4px; font-weight:700}
.out.flash .o:last-child{background:var(--copper)}
.legend{font-size:11px; color:var(--muted); display:flex; gap:10px; flex-wrap:wrap}
.legend span::before{content:""; display:inline-block; width:9px; height:9px; border-radius:2px; margin-right:4px; vertical-align:-1px; background:var(--k)}

/* lower */
.lower{display:grid; grid-template-columns:minmax(0,1.15fr) minmax(0,1fr); gap:16px; align-items:start}
.narr-stage{font-family:var(--mono); font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--copper)}
.rtn{font-family:var(--mono); font-size:clamp(22px,2.6vw,30px); font-weight:700; margin:2px 0 6px; line-height:1.2}
.desc{margin:0; max-width:62ch; font-size:16px}
.nmem{margin:6px 0 0; font-size:14px; font-weight:600}
.nmem.good{color:var(--good)} .nmem.bad{color:var(--bad)}
.next{margin:10px 0 0; color:var(--muted); font-size:13px; font-family:var(--mono)}
.fb{margin:0 0 10px; padding:8px 12px; border-radius:8px; font-weight:600}
.fb.good{background:var(--good-soft); color:var(--good)} .fb.bad{background:var(--bad-soft); color:var(--bad)} .fb.neutral{background:var(--panel-2); color:var(--muted)}
.pred{margin-top:12px; padding:12px; border:2px dashed var(--copper); border-radius:10px; background:var(--copper-soft)}
.pred-q{font-weight:600; font-size:17px; margin:0 0 8px}
.pred-row{display:flex; flex-wrap:wrap; gap:8px; align-items:center}
.pred input{font-family:var(--mono); font-size:20px; width:120px; padding:6px 10px; border-radius:6px; border:1.5px solid var(--line); background:var(--panel); color:var(--ink)}
.choice{font-family:var(--mono); font-weight:700; padding:6px 10px; border-radius:6px; border:1.5px solid var(--line); background:var(--panel)}
.choice:hover{border-color:var(--copper)}
.info{margin-top:12px; padding:12px 14px; border-radius:10px; background:var(--panel-2); border:1px solid var(--line)}
.info h3{font-family:var(--display); font-weight:800; font-size:20px; margin:0 0 4px; display:flex; justify-content:space-between; gap:8px; align-items:baseline}
.info h3 small{font-family:var(--mono); font-size:11px; font-weight:400; color:var(--muted)}
.info p{margin:0 0 6px; max-width:65ch}
.info ul{margin:4px 0 6px; padding-left:18px}
.x{background:none; border:0; color:var(--muted); font-size:13px; padding:0; text-decoration:underline}
.controls{display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:14px; padding-top:14px; border-top:1px solid var(--line)}
.btn{border:1.5px solid var(--ink); background:var(--panel); border-radius:8px; padding:8px 14px; font-weight:600}
.btn.primary{background:var(--ink); color:var(--bg)}
.btn:hover{border-color:var(--copper)}
.btn.primary:hover{background:var(--copper); border-color:var(--copper); color:#fff}
.btn kbd{font-family:var(--mono); font-size:11px; opacity:.7; margin-left:4px}
.toggles{display:flex; flex-wrap:wrap; gap:14px; align-items:center; font-size:14px; margin-top:10px}
.toggles label{display:flex; gap:6px; align-items:center; cursor:pointer}
.toggles input[type=range]{width:110px; accent-color:var(--copper)}
.toggles input[type=checkbox]{accent-color:var(--copper); width:16px; height:16px}
.stats{display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:8px; margin-top:14px}
.stat{background:var(--panel-2); border-radius:8px; padding:8px 10px}
.stat b{display:block; font-family:var(--mono); font-size:22px; font-variant-numeric:tabular-nums}
.stat span{font-size:12px; color:var(--muted)}

.prog h2,.chal h2{font-family:var(--display); font-weight:800; font-size:20px; margin:0}
.prog-top{display:flex; flex-wrap:wrap; gap:8px; align-items:center; justify-content:space-between; margin-bottom:8px}
select{font:inherit; font-size:14px; padding:6px 8px; border-radius:6px; border:1.5px solid var(--line); background:var(--panel); color:var(--ink)}
textarea{width:100%; min-height:220px; font-family:var(--mono); font-size:14px; line-height:1.55; padding:10px 12px; border-radius:8px; border:1.5px solid var(--line); background:var(--panel-2); color:var(--ink); resize:vertical; tab-size:8}
.err{color:var(--bad); font-size:13px; margin:6px 0 0; white-space:pre-line}
.ok{color:var(--good); font-size:13px; margin:6px 0 0}
.isa-wrap{overflow-x:auto; margin-top:12px}
table.isa{border-collapse:collapse; width:100%; font-size:13px}
.isa th,.isa td{text-align:left; padding:4px 8px; border-bottom:1px solid var(--line); vertical-align:top}
.isa th{font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); font-weight:600}
.isa td:first-child,.isa td:nth-child(2){font-family:var(--mono); font-weight:700; white-space:nowrap}
.chal{margin-top:16px; padding-top:14px; border-top:1px solid var(--line)}
.chal p.lead{margin:4px 0 10px; color:var(--muted); font-size:13px}
.ch{display:grid; grid-template-columns:auto 1fr auto; gap:4px 10px; align-items:start; padding:9px 0; border-bottom:1px solid var(--line)}
.ch .n{font-family:var(--mono); font-weight:700; color:var(--muted); padding-top:1px}
.ch.pass .n{color:var(--good)}
.ch h4{margin:0; font-size:15px}
.ch h4 em{font-style:normal; font-family:var(--mono); font-size:11px; color:var(--copper); margin-left:6px}
.ch p{margin:0; font-size:14px}
.ch .res{grid-column:2/-1; font-size:13px; margin:0}
.ch .res.good{color:var(--good)} .ch .res.bad{color:var(--bad)}
.btn.sm{padding:4px 10px; font-size:13px}

details.teach{background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 14px}
details.teach summary{cursor:pointer; font-weight:600}
details.teach ol{margin:8px 0 4px; padding-left:20px; max-width:80ch}
details.teach li{margin-bottom:4px}

details.howto{background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 14px}
details.howto summary{cursor:pointer; font-weight:600; font-size:15px}
.howto-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px 20px; margin-top:10px}
.howto-grid h3{font-family:var(--display); font-weight:800; font-size:16px; margin:0 0 4px}
.howto-grid ol,.howto-grid ul{margin:0; padding-left:18px; font-size:14px}
.howto-grid li{margin-bottom:3px}
@media (max-width:980px){
  .machine{grid-template-columns:1fr; gap:12px}
  .buses{padding:0}
  .lower{grid-template-columns:1fr}
}
@media (max-width:560px){
  .app{padding-inline:16px}
  .regs{grid-template-columns:repeat(3,minmax(0,1fr))}
  .caches{grid-template-columns:1fr}
  #s-l3{grid-template-columns:repeat(4,1fr)}
  .cell span{font-size:11px}
}
@media (prefers-reduced-motion: reduce){
  .pkt.go-r,.pkt.go-l{animation:none}
  *{transition:none!important}
}
</style>
</head>
<body>

<div class="app">
  <header class="top">
    <div class="brand">
      <h1>CPU Cycle Lab</h1>
      <p><b>A1.1.1</b> CPU components &amp; buses · <b>A1.1.4</b> Primary memory &amp; cache · <b>A1.1.5</b> Fetch–decode–execute. Click any part to learn what it does.</p>
    </div>
    <div class="stages" aria-label="Cycle stage">
      <span class="stage" id="st-fetch">Fetch</span>
      <span class="stage" id="st-decode">Decode</span>
      <span class="stage" id="st-execute">Execute</span>
      <span class="stage halt" id="st-halt">Halted</span>
    </div>
  </header>

  <details class="howto" id="howto" open>
    <summary>How to use</summary>
    <div class="howto-grid">
      <div><h3>Run a program</h3><ol>
        <li>The deck example is already in RAM. The PC starts at 00 (copper outline).</li>
        <li>Press <b>Step</b> (or Space). Each press is one register step, e.g. MAR ← PC.</li>
        <li>Read the panel below: the step, what happened, and what's next.</li>
        <li>Keep going until <b>Halted</b>. Watch address 05 change.</li></ol></div>
      <div><h3>Predict mode</h3><ul>
        <li>Before most steps you're asked a question, e.g. what the MAR will hold.</li>
        <li>Type your answer and press Enter, or pick an instruction when decoding.</li>
        <li><b>Show me</b> skips the guess. Untick "Predict" to just watch.</li></ul></div>
      <div><h3>Buttons</h3><ul>
        <li><b>Whole instruction</b>: one full fetch–decode–execute.</li>
        <li><b>Run / Pause</b>: plays automatically. Use the Speed slider.</li>
        <li><b>Reset</b>: back to the start.</li>
        <li>Click any part of the computer to see what it does.</li></ul></div>
      <div><h3>Cache experiment</h3><ol>
        <li>Pick <b>Loop: count down from 3</b>.</li>
        <li>Untick <b>Cache on</b>, Run, note the cycles.</li>
        <li>Tick it, Reset, Run again. Compare cycles and hit rate.</li></ol></div>
      <div><h3>Write your own</h3><ol>
        <li>Type one instruction per line (see the table under the Program box).</li>
        <li>Press <b>Load into RAM</b>. Errors show in red.</li>
        <li>Step or Run it, or press a challenge's <b>Check</b>.</li></ol></div>
    </div>
  </details>
  <section class="machine" aria-label="Computer">
    <div class="panel cpu">
      <div class="panel-h">
        <button class="tag" data-info="cpu">CPU</button>
        <button class="chip" data-info="cores">Core 0 · single core</button>
      </div>
      <div class="units">
        <button class="unit" id="u-cu" data-info="cu"><span class="lbl">Control unit</span><span class="val" id="v-cu">—</span></button>
        <button class="unit" id="u-alu" data-info="alu"><span class="lbl">ALU</span><span class="val" id="v-alu">—</span></button>
      </div>
      <div class="regs">
        <button class="reg" id="r-pc" data-info="pc"><span class="lbl">PC</span><span class="val" id="v-pc">00</span><span class="sub">Program counter</span></button>
        <button class="reg" id="r-mar" data-info="mar"><span class="lbl">MAR</span><span class="val" id="v-mar">00</span><span class="sub">Memory address reg.</span></button>
        <button class="reg" id="r-mdr" data-info="mdr"><span class="lbl">MDR</span><span class="val" id="v-mdr">000</span><span class="sub">Memory data reg.</span></button>
        <button class="reg" id="r-ir" data-info="ir"><span class="lbl">IR</span><span class="val" id="v-ir">000</span><span class="sub">Instruction reg.</span></button>
        <button class="reg" id="r-acc" data-info="acc"><span class="lbl">AC</span><span class="val" id="v-acc">000</span><span class="sub">Accumulator</span></button>
      </div>
      <div class="caches" id="caches">
        <div class="cache" id="c-l1"><button class="cache-h" data-info="l1"><span class="lbl">L1</span><span class="cost">1 cycle</span></button><div class="slots" id="s-l1"></div></div>
        <div class="cache" id="c-l2"><button class="cache-h" data-info="l2"><span class="lbl">L2</span><span class="cost">4 cycles</span></button><div class="slots" id="s-l2"></div></div>
        <div class="cache" id="c-l3"><button class="cache-h" data-info="l3"><span class="lbl">L3</span><span class="cost">12 cycles</span></button><div class="slots" id="s-l3"></div></div>
        <p class="cache-note" id="cache-note">Slots show address and value. Cycle costs are a teaching model, not real timings.</p>
      </div>
    </div>

    <div class="buses" aria-label="System bus">
      <button class="lane" data-bus="address" data-info="abus"><span class="lane-lbl"><span>Address bus</span><i>one-way →</i></span><span class="track"><span class="pkt" id="p-address"></span></span></button>
      <button class="lane" data-bus="data" data-info="dbus"><span class="lane-lbl"><span>Data bus</span><i>two-way ⇄</i></span><span class="track"><span class="pkt" id="p-data"></span></span></button>
      <button class="lane" data-bus="control" data-info="cbus"><span class="lane-lbl"><span>Control bus</span><i>two-way ⇄</i></span><span class="track"><span class="pkt" id="p-control"></span></span></button>
      <div class="ends"><span>CPU</span><span>Memory</span></div>
    </div>

    <div class="panel mem">
      <div class="panel-h">
        <button class="tag" data-info="ram">RAM</button>
        <button class="chip" data-info="rom">ROM · BIOS</button>
      </div>
      <div class="ram" id="ram"></div>
      <div class="memfoot">
        <div class="out" id="out" aria-live="polite"><span class="lbl">Output</span></div>
        <div class="legend"><span style="--k:var(--copper)">PC points here</span><span style="--k:var(--data)">read</span><span style="--k:var(--ctrl)">write</span><span style="--k:var(--good)">cached</span></div>
      </div>
    </div>
  </section>

  <section class="lower">
    <div class="panel">
      <div class="fb" id="fb" hidden></div>
      <div class="narr-stage" id="n-stage">Ready</div>
      <div class="rtn" id="n-rtn">PC = 00</div>
      <p class="desc" id="n-desc">The program is loaded into RAM. The program counter holds 00, so the first instruction will be fetched from address 00. Press Step.</p>
      <p class="nmem" id="n-mem"></p>
      <p class="next" id="n-next"></p>

      <div class="pred" id="pred" hidden>
        <p class="pred-q" id="pred-q"></p>
        <div class="pred-row" id="pred-in"></div>
      </div>

      <div class="info" id="info" hidden>
        <h3><span id="info-t"></span><small id="info-ref"></small></h3>
        <div id="info-b"></div>
        <button class="x" id="info-x">Close</button>
      </div>

      <div class="controls">
        <button class="btn primary" id="b-step">Step <kbd>Space</kbd></button>
        <button class="btn" id="b-instr">Whole instruction</button>
        <button class="btn" id="b-run">Run</button>
        <button class="btn" id="b-reset">Reset</button>
      </div>
      <div class="toggles">
        <label><input type="checkbox" id="t-pred" checked> Predict before each step</label>
        <label><input type="checkbox" id="t-cache" checked> Cache on</label>
        <label>Speed <input type="range" id="t-speed" min="0" max="100" value="45"></label>
      </div>
      <div class="stats">
        <div class="stat"><b id="k-cyc">0</b><span>model cycles</span></div>
        <div class="stat"><b id="k-ins">0</b><span>instructions done</span></div>
        <div class="stat"><b id="k-hit">–</b><span>cache hit rate</span></div>
        <div class="stat"><b id="k-pred">0/0</b><span>predictions right</span></div>
      </div>
    </div>

    <div class="panel prog">
      <div class="prog-top">
        <h2>Program</h2>
        <select id="sample" aria-label="Example programs">
          <option value="deck">Deck example: LDA / ADD / STA</option>
          <option value="loop">Loop: count down from 3</option>
          <option value="blank">Blank</option>
        </select>
      </div>
      <textarea id="code" spellcheck="false" aria-label="Assembly program"></textarea>
      <div style="display:flex; gap:8px; margin-top:8px; flex-wrap:wrap">
        <button class="btn primary" id="b-load">Load into RAM</button>
      </div>
      <p id="asm-msg" class="ok"></p>

      <div class="isa-wrap">
        <table class="isa">
          <thead><tr><th>Code</th><th>Machine</th><th>What it does</th></tr></thead>
          <tbody>
            <tr><td>LDA xx</td><td>5xx</td><td>Load the value at address xx into AC</td></tr>
            <tr><td>ADD xx</td><td>1xx</td><td>AC ← AC + value at xx</td></tr>
            <tr><td>SUB xx</td><td>2xx</td><td>AC ← AC − value at xx</td></tr>
            <tr><td>STA xx</td><td>3xx</td><td>Store AC at address xx</td></tr>
            <tr><td>BRA xx</td><td>6xx</td><td>Jump to xx</td></tr>
            <tr><td>BRZ xx</td><td>7xx</td><td>Jump to xx if AC = 0</td></tr>
            <tr><td>BRP xx</td><td>8xx</td><td>Jump to xx if AC ≥ 0</td></tr>
            <tr><td>OUT</td><td>902</td><td>Output AC</td></tr>
            <tr><td>HLT</td><td>000</td><td>Stop</td></tr>
            <tr><td>DAT n</td><td>n</td><td>Not an instruction: reserves a memory cell holding n</td></tr>
          </tbody>
        </table>
      </div>

      <div class="chal">
        <h2>Challenges</h2>
        <p class="lead">Write a program above, then press Check. Labels work: <span class="mono">loop  SUB one</span>, <span class="mono">one  DAT 1</span>.</p>
        <div id="chals"></div>
      </div>
    </div>
  </section>

</div>

<script>
(() => {
const $ = id => document.getElementById(id);
const pad2 = n => String(n).padStart(2, '0');
const fmt3 = n => (n < 0 ? '-' + String(-n).padStart(3, '0') : String(n).padStart(3, '0'));
const clamp = n => Math.max(-999, Math.min(999, n));

/* ---------- content ---------- */
const INFO = {
  cpu: ['Central processing unit', 'A1.1.1', '<p>Carries out most of the processing in a computer. Its main parts are the <b>control unit</b>, the <b>arithmetic logic unit</b>, a set of <b>registers</b> and <b>cache</b>.</p><p>It works by repeating the fetch–decode–execute cycle, once per instruction.</p>'],
  cores: ['Cores', 'A1.1.1', '<p>This simulation shows one core. A <b>single-core</b> CPU runs one instruction stream at a time and shares itself between programs.</p><p>A <b>multi-core</b> CPU (dual, quad, octa) has several cores that run instructions at the same time. It is not automatically 2× or 4× faster: the software must be written to split work across cores.</p><p>A <b>co-processor</b> (for example a GPU) is a separate processor built for one kind of task. The CPU offloads that work to it.</p>'],
  cu: ['Control unit (CU)', 'A1.1.1', '<p>Directs the operation of the processor. It manages the fetch–decode–execute cycle, decodes each instruction in the IR, and sends control signals to memory, the ALU and input/output devices.</p><p>Here it shows the instruction it has decoded.</p>'],
  alu: ['Arithmetic logic unit (ALU)', 'A1.1.1', '<p>Performs arithmetic (add, subtract, multiply, divide) and logic operations (AND, OR, XOR, NOT, comparisons).</p><p>Results go into the accumulator. Here it shows the last calculation or comparison it did.</p>'],
  pc: ['Program counter (PC)', 'A1.1.1', '<p>Holds the <b>address of the next instruction</b> to fetch.</p><p>It is incremented during the fetch stage, before the current instruction is decoded. A branch instruction (BRA, BRZ, BRP) overwrites it with a new address.</p>'],
  mar: ['Memory address register (MAR)', 'A1.1.1', '<p>Holds the <b>address</b> of the memory location currently being read from or written to. Its contents are sent out on the address bus.</p>'],
  mdr: ['Memory data register (MDR)', 'A1.1.1', '<p>Holds the <b>data</b> that has just been read from memory, or that is about to be written to the address in the MAR. It connects to the data bus.</p><p>Sometimes called the memory buffer register (MBR).</p>'],
  ir: ['Instruction register (IR)', 'A1.1.1', '<p>Holds the instruction currently being decoded and executed.</p><p>The control unit splits it into an <b>opcode</b> (what to do, first digit, shown in copper) and an <b>operand</b> (what to do it to, usually an address, last two digits).</p>'],
  acc: ['Accumulator (AC)', 'A1.1.1', '<p>Stores the intermediate results of arithmetic and logic operations carried out by the ALU.</p>'],
  l1: ['L1 cache', 'A1.1.4', '<p>On the core itself: the fastest and smallest cache (typically 32–128 KB per core), often split into L1i (instructions) and L1d (data).</p><p>In this model: 2 slots, 1 cycle.</p><p>The CPU checks L1 first, then L2, then L3, then RAM. Finding the data in cache is a <b>cache hit</b>. Not finding it is a <b>cache miss</b>, and the slower level has to be used.</p>'],
  l2: ['L2 cache', 'A1.1.4', '<p>Larger and slightly slower than L1 (typically 256 KB–2 MB per core). On the CPU or very close to it.</p><p>In this model: 4 slots, 4 cycles.</p>'],
  l3: ['L3 cache', 'A1.1.4', '<p>The largest and slowest cache (typically 2–64 MB), usually <b>shared between all cores</b>. Still much faster than RAM.</p><p>In this model: 8 slots, 12 cycles. When a cache is full, the least recently used item is replaced.</p>'],
  ram: ['RAM', 'A1.1.4', '<p>Random access memory holds the instructions and data of programs that are currently running. It is <b>volatile</b>: contents are lost when power is off.</p><p>In this model a RAM access costs 40 cycles, which is why cache matters.</p><p>Each cell holds a number. RAM cannot tell whether it is an instruction or data. It becomes an instruction when the PC points at it.</p>'],
  rom: ['ROM', 'A1.1.4', '<p>Read-only memory is <b>non-volatile</b>: it keeps its contents with the power off.</p><p>It stores the BIOS/firmware, which runs at start-up: it tests the hardware and loads the operating system from secondary storage into RAM.</p><p>Most modern systems use flash memory for this, so the firmware can be updated.</p>'],
  abus: ['Address bus', 'A1.1.1 · A1.1.5', '<p>Carries memory addresses from the CPU (the MAR) to memory. It is <b>one-way</b>.</p><p>Its width sets how many locations can be addressed: an <i>n</i>-bit address bus can address 2<sup>n</sup> locations. A 32-bit bus addresses 2<sup>32</sup> locations.</p>'],
  dbus: ['Data bus', 'A1.1.1 · A1.1.5', '<p>Carries data and instructions between the CPU, memory and other devices. It is <b>two-way</b>: data is both read and written.</p><p>Its width (commonly 8, 16, 32 or 64 bits) sets how much can move in one transfer.</p>'],
  cbus: ['Control bus', 'A1.1.1 · A1.1.5', '<p>Carries control signals such as <b>read</b>, <b>write</b>, interrupt requests and clock signals. It is <b>two-way</b>: the CPU sends commands and devices send status signals back.</p>']
};

const SAMPLES = {
  deck: `// From the A1.1.5 deck: 23 + 12, stored in address 05
        LDA 4
        ADD 5
        STA 5
        HLT
        DAT 23
        DAT 12`,
  loop: `// Count down from 3. Watch the cache on the second lap.
        LDA start
loop    OUT
        SUB one
        BRZ done
        BRA loop
done    HLT
start   DAT 3
one     DAT 1`,
  blank: `// Write your program here

`
};

const CHALLENGES = [
  { t: 'Add and output', d: 'Store 23 and 12 with DAT. Output their sum.', expect: [35] },
  { t: 'Subtract', d: 'Output 50 − 8.', expect: [42] },
  { t: 'Double it', d: 'Store 17. Output double its value without storing 34 anywhere.', expect: [34] },
  { t: 'Count up', d: 'Output 1, 2, 3, 4, 5 using a loop.', expect: [1, 2, 3, 4, 5], tag: 'loop' },
  { t: 'Multiply', d: 'Output 6 × 4 using repeated addition in a loop.', expect: [24], tag: 'loop' },
  { t: 'Fibonacci', d: 'Output the first eight Fibonacci numbers: 0 1 1 2 3 5 8 13.', expect: [0, 1, 1, 2, 3, 5, 8, 13], tag: 'stretch · HL' }
];

/* ---------- assembler ---------- */
const OPS = { ADD: 1, SUB: 2, STA: 3, STO: 3, LDA: 5, BRA: 6, BRZ: 7, BRP: 8, OUT: 902, HLT: 0, COB: 0, DAT: -1 };
const NEEDS_ADDR = ['ADD', 'SUB', 'STA', 'STO', 'LDA', 'BRA', 'BRZ', 'BRP'];
function assemble(src) {
  const items = [], labels = {}, errors = [];
  src.split('\n').forEach((raw, i) => {
    const line = raw.replace(/(\/\/|;|#).*$/, '').trim();
    if (!line) return;
    const t = line.split(/\s+/);
    let label = null;
    if (!(t[0].toUpperCase() in OPS)) label = t.shift();
    if (!t.length) { errors.push(`Line ${i + 1}: "${label}" is not an instruction`); return; }
    const op = t[0].toUpperCase();
    if (!(op in OPS)) { errors.push(`Line ${i + 1}: unknown instruction "${t[0]}"`); return; }
    if (label) {
      if (!/^[A-Za-z_]\w*$/.test(label)) { errors.push(`Line ${i + 1}: "${label}" is not a valid label`); return; }
      labels[label.toLowerCase()] = items.length;
    }
    items.push({ op, arg: t[1], line: i + 1 });
  });
  if (items.length > 100) errors.push('Program is longer than 100 memory cells');
  const mem = new Array(100).fill(0);
  items.slice(0, 100).forEach((it, a) => {
    let v = 0;
    if (it.arg !== undefined) {
      if (/^-?\d+$/.test(it.arg)) v = parseInt(it.arg, 10);
      else if (labels[it.arg.toLowerCase()] !== undefined) v = labels[it.arg.toLowerCase()];
      else { errors.push(`Line ${it.line}: no label called "${it.arg}"`); return; }
    } else if (NEEDS_ADDR.includes(it.op)) { errors.push(`Line ${it.line}: ${it.op} needs an address`); return; }
    if (it.op === 'DAT') {
      if (v < -999 || v > 999) errors.push(`Line ${it.line}: DAT values must be between -999 and 999`);
      mem[a] = clamp(v);
    } else if (it.op === 'OUT') mem[a] = 902;
    else if (it.op === 'HLT' || it.op === 'COB') mem[a] = 0;
    else {
      if (v < 0 || v > 99) errors.push(`Line ${it.line}: address must be 0–99`);
      mem[a] = OPS[it.op] * 100 + Math.max(0, Math.min(99, v));
    }
  });
  return { mem, errors };
}

/* ---------- machine ---------- */
const LEVELS = [['l1', 2, 1], ['l2', 4, 4], ['l3', 8, 12]];
const RAM_COST = 40;
function freshState(mem, cacheOn) {
  return { mem: mem.slice(), pc: 0, mar: 0, mdr: 0, ir: 0, acc: 0, mn: null, operand: null, out: [], halted: false,
    cache: { l1: [], l2: [], l3: [] }, cacheOn, cycles: 0, instr: 0, hits: 0, misses: 0, queue: [], alu: '', cu: '' };
}
function clone(s) {
  return { ...s, mem: s.mem.slice(), out: s.out.slice(), queue: s.queue.slice(),
    cache: { l1: s.cache.l1.slice(), l2: s.cache.l2.slice(), l3: s.cache.l3.slice() } };
}
function access(s, addr) {
  if (!s.cacheOn) { s.cycles += RAM_COST; s.misses++; return 'ram'; }
  let found = 'ram', cost = RAM_COST;
  for (const [k, , c] of LEVELS) if (s.cache[k].includes(addr)) { found = k; cost = c; break; }
  s.cycles += cost;
  if (found === 'ram') s.misses++; else s.hits++;
  for (const [k, size] of LEVELS) {
    const arr = s.cache[k], i = arr.indexOf(addr);
    if (i >= 0) arr.splice(i, 1);
    arr.unshift(addr);
    if (arr.length > size) arr.pop();
  }
  return found;
}

const MEANING = {
  LDA: o => `load the value at address ${o} into the accumulator`,
  ADD: o => `add the value at address ${o} to the accumulator`,
  SUB: o => `subtract the value at address ${o} from the accumulator`,
  STA: o => `store the accumulator in address ${o}`,
  BRA: o => `jump to address ${o}`,
  BRZ: o => `jump to address ${o} if the accumulator is zero`,
  BRP: o => `jump to address ${o} if the accumulator is zero or positive`,
  OUT: () => 'output the accumulator',
  HLT: () => 'stop the program'
};
function decode(s) {
  const v = s.ir;
  s.operand = null;
  if (v === 902) s.mn = 'OUT';
  else if (v >= 0 && v < 100) s.mn = 'HLT';
  else if (v > 0 && v < 900) {
    s.operand = v % 100;
    s.mn = { 1: 'ADD', 2: 'SUB', 3: 'STA', 5: 'LDA', 6: 'BRA', 7: 'BRZ', 8: 'BRP' }[Math.floor(v / 100)] || '???';
    if (s.mn === '???') s.operand = null;
  } else s.mn = '???';
  s.cu = s.mn === '???' ? 'unknown' : s.mn + (s.operand !== null ? ' ' + pad2(s.operand) : '');
}

function memReadStep(stage) {
  return { stage, rtn: 'MDR ← [MAR]',
    desc: (b, a) => `The address bus carries ${pad2(a.mar)} from the MAR to memory and the control bus signals READ. The contents, ${fmt3(a.mdr)}, return along the data bus into the MDR.`,
    predict: { q: 'What value will arrive in the MDR?', key: 'mdr' },
    run(s) {
      const lvl = access(s, s.mar); s.mdr = s.mem[s.mar];
      return { regs: ['mar', 'mdr'], buses: [{ b: 'address', v: pad2(s.mar), dir: 'r' }, { b: 'control', v: 'READ', dir: 'r' }, { b: 'data', v: fmt3(s.mdr), dir: 'l' }], mem: { addr: s.mar, kind: 'rd' }, level: lvl };
    } };
}
function fetchSteps() {
  return [
    { stage: 'fetch', rtn: 'MAR ← PC', desc: (b, a) => `The PC holds ${pad2(b.pc)}, the address of the next instruction. It is copied into the MAR.`,
      predict: { q: 'What value will the MAR hold?', key: 'mar' },
      run(s) { s.mar = s.pc; return { regs: ['pc', 'mar'] }; } },
    memReadStep('fetch'),
    { stage: 'fetch', rtn: 'PC ← PC + 1', desc: (b, a) => `The PC is incremented to ${pad2(a.pc)} straight away, so it already points at the next instruction before this one is decoded.`,
      predict: { q: 'What will the PC hold now?', key: 'pc' },
      run(s) { s.pc = (s.pc + 1) % 100; return { regs: ['pc'], alu: false }; } },
    { stage: 'fetch', rtn: 'IR ← MDR', desc: (b, a) => `The instruction ${fmt3(a.ir)} is copied from the MDR into the instruction register, ready for the control unit.`,
      run(s) { s.ir = s.mdr; s.mn = null; s.cu = ''; return { regs: ['mdr', 'ir'] }; } },
    { stage: 'decode', rtn: 'CU decodes the IR', desc: (b, a) => {
        if (a.mn === '???') return `${fmt3(a.ir)} does not match any instruction.`;
        const op = a.mn === 'OUT' ? '9' : String(Math.floor(a.ir / 100));
        const opd = a.mn === 'OUT' ? '02' : pad2(a.ir % 100);
        return `The control unit splits ${fmt3(a.ir)} into opcode ${op} and operand ${opd}. It means ${a.mn}: ${MEANING[a.mn](opd)}.`;
      },
      predict: { q: s => `The IR holds ${fmt3(s.ir)}. Which instruction is it?`, key: 'mn', choice: true },
      run(s) { decode(s); s.queue.push(...execSteps(s)); return { regs: ['ir'], cu: true }; } }
  ];
}
function marFromOperand() {
  return { stage: 'execute', rtn: 'MAR ← operand', desc: (b, a) => `The operand ${pad2(a.mar)} is an address. The control unit copies it into the MAR.`,
    predict: { q: 'What value will the MAR hold?', key: 'mar' },
    run(s) { s.mar = s.operand; return { regs: ['ir', 'mar'], cu: true }; } };
}
function execSteps(s) {
  const E = 'execute';
  switch (s.mn) {
    case 'LDA': return [marFromOperand(), memReadStep(E),
      { stage: E, rtn: 'AC ← MDR', desc: (b, a) => `The value ${fmt3(a.acc)} is copied from the MDR into the accumulator.`,
        predict: { q: 'What will the accumulator hold?', key: 'acc' },
        run(s) { s.acc = s.mdr; return { regs: ['mdr', 'acc'] }; } }];
    case 'ADD': case 'SUB': {
      const add = s.mn === 'ADD';
      return [marFromOperand(), memReadStep(E),
        { stage: E, rtn: add ? 'AC ← AC + MDR' : 'AC ← AC − MDR',
          desc: (b, a) => `The ALU ${add ? 'adds' : 'subtracts'} ${fmt3(b.mdr)} ${add ? 'to' : 'from'} ${fmt3(b.acc)}. The result, ${fmt3(a.acc)}, goes back into the accumulator.`,
          predict: { q: 'What will the accumulator hold after the ALU is done?', key: 'acc' },
          run(s) { const r = add ? s.acc + s.mdr : s.acc - s.mdr; s.alu = `${s.acc} ${add ? '+' : '−'} ${s.mdr} = ${r}`; s.acc = clamp(r); return { regs: ['mdr', 'acc'], alu: true }; } }];
    }
    case 'STA': return [marFromOperand(),
      { stage: E, rtn: 'MDR ← AC', desc: (b, a) => `The value to store, ${fmt3(a.mdr)}, is copied from the accumulator into the MDR.`,
        predict: { q: 'What value will the MDR hold?', key: 'mdr' },
        run(s) { s.mdr = s.acc; return { regs: ['acc', 'mdr'] }; } },
      { stage: E, rtn: '[MAR] ← MDR', desc: (b, a) => `The address bus carries ${pad2(a.mar)}, the control bus signals WRITE and the data bus carries ${fmt3(a.mdr)} to memory. Address ${pad2(a.mar)} now holds ${fmt3(a.mdr)}.`,
        predict: { q: s => `What will address ${pad2(s.mar)} hold afterwards?`, key: 'memAtMar' },
        run(s) { const lvl = access(s, s.mar); s.mem[s.mar] = s.mdr;
          return { regs: ['mar', 'mdr'], buses: [{ b: 'address', v: pad2(s.mar), dir: 'r' }, { b: 'control', v: 'WRITE', dir: 'r' }, { b: 'data', v: fmt3(s.mdr), dir: 'r' }], mem: { addr: s.mar, kind: 'wr' }, level: lvl }; } }];
    case 'BRA': return [
      { stage: E, rtn: 'PC ← operand', desc: (b, a) => `An unconditional jump. The PC is overwritten with ${pad2(a.pc)}, so the next fetch comes from there.`,
        predict: { q: 'What will the PC hold?', key: 'pc' },
        run(s) { s.pc = s.operand; return { regs: ['pc'], cu: true }; } }];
    case 'BRZ': case 'BRP': {
      const z = s.mn === 'BRZ';
      return [{ stage: E, rtn: z ? 'If AC = 0: PC ← operand' : 'If AC ≥ 0: PC ← operand',
        desc: (b, a) => { const t = z ? b.acc === 0 : b.acc >= 0; return `The accumulator holds ${fmt3(b.acc)}, so the condition is ${t ? 'true' : 'false'}. ${t ? `The PC is set to ${pad2(a.pc)}.` : `The PC stays at ${pad2(a.pc)}.`}`; },
        predict: { q: 'What will the PC hold after this instruction?', key: 'pc' },
        run(s) { const t = z ? s.acc === 0 : s.acc >= 0; if (t) s.pc = s.operand; s.alu = `${s.acc} ${z ? '= 0' : '≥ 0'}? ${t ? 'yes' : 'no'}`; return { regs: ['acc', 'pc'], alu: true, cu: true }; } }];
    }
    case 'OUT': return [
      { stage: E, rtn: 'Output ← AC', desc: (b) => `The accumulator's value, ${fmt3(b.acc)}, is sent to the output device.`,
        predict: { q: 'What number will be output?', key: 'lastOut' },
        run(s) { s.out.push(s.acc); return { regs: ['acc'], buses: [{ b: 'control', v: 'OUT', dir: 'r' }], out: true }; } }];
    case 'HLT': return [
      { stage: E, rtn: 'Halt', desc: () => 'The control unit stops the cycle. The program has finished.',
        run(s) { s.halted = true; return { cu: true }; } }];
    default: return [
      { stage: E, rtn: 'Invalid instruction', desc: (b) => `${fmt3(b.ir)} is not an instruction this CPU understands. The PC may have run into data. Execution stops.`,
        run(s) { s.halted = true; return { cu: true }; } }];
  }
}
function peek(s) { if (s.halted) return null; if (!s.queue.length) s.queue = fetchSteps(); return s.queue[0]; }
function stepOnce(s) {
  const st = peek(s); if (!st) return null;
  const before = clone(s);
  s.queue.shift(); s.cycles += 1;
  const fx = st.run(s) || {};
  if (st.stage === 'execute' && !s.queue.length) s.instr++;
  return { st, before, fx };
}
const GET = { mar: s => s.mar, mdr: s => s.mdr, pc: s => s.pc, acc: s => s.acc, mn: s => s.mn, memAtMar: s => s.mem[s.mar], lastOut: s => s.out[s.out.length - 1] };
const FMT = { mar: pad2, pc: pad2, mn: v => v };

/* ---------- UI state ---------- */
let loaded = assemble(SAMPLES.deck).mem;
let S = freshState(loaded, true);
let awaiting = null, running = false, timer = null;
const score = { ok: 0, tries: 0 };

const ram = $('ram');
for (let i = 0; i < 100; i++) {
  const c = document.createElement('button');
  c.className = 'cell'; c.id = 'm' + i; c.dataset.addr = i;
  c.innerHTML = `<b>${pad2(i)}</b><span>000</span>`;
  ram.appendChild(c);
}
for (const [k, size] of LEVELS) {
  const el = $('s-' + k);
  for (let i = 0; i < size; i++) { const d = document.createElement('div'); d.className = 'slot empty'; el.appendChild(d); }
}

function speedMs() { const v = +$('t-speed').value; return Math.round(1600 - v * 15); }
function setDur() { document.documentElement.style.setProperty('--dur', Math.min(900, Math.round(speedMs() * 0.7)) + 'ms'); }

function animPkt(bus, v, dir) {
  const el = $('p-' + bus);
  el.textContent = v;
  el.classList.remove('go-r', 'go-l'); void el.offsetWidth;
  el.classList.add(dir === 'r' ? 'go-r' : 'go-l');
}

function render(r) {
  const fx = r ? r.fx : {};
  $('v-pc').textContent = pad2(S.pc);
  $('v-mar').textContent = pad2(S.mar);
  $('v-mdr').textContent = fmt3(S.mdr);
  $('v-acc').textContent = fmt3(S.acc);
  const irEl = $('v-ir');
  if (S.mn && S.mn !== '???') {
    const s3 = fmt3(S.ir);
    irEl.innerHTML = `<span class="op">${s3[0]}</span>${s3.slice(1)}`;
  } else irEl.textContent = fmt3(S.ir);
  $('v-cu').textContent = S.cu || '—';
  $('v-alu').textContent = S.alu || '—';

  document.querySelectorAll('.hot').forEach(e => e.classList.remove('hot'));
  (fx.regs || []).forEach(k => $('r-' + k).classList.add('hot'));
  if (fx.alu) $('u-alu').classList.add('hot');
  if (fx.cu) $('u-cu').classList.add('hot');

  ['address', 'data', 'control'].forEach(b => {
    const lane = document.querySelector(`.lane[data-bus="${b}"]`);
    const m = (fx.buses || []).find(x => x.b === b);
    lane.classList.toggle('lit', !!m);
    if (m) animPkt(b, m.v, m.dir); else $('p-' + b).classList.remove('go-r', 'go-l');
  });

  const cachedSet = new Set([...S.cache.l1, ...S.cache.l2, ...S.cache.l3]);
  for (let i = 0; i < 100; i++) {
    const c = $('m' + i), v = S.mem[i];
    c.lastChild.textContent = fmt3(v);
    c.className = 'cell' + (v === 0 ? ' zero' : '') + (i === S.pc && !S.halted ? ' is-pc' : '') + (S.cacheOn && cachedSet.has(i) ? ' cached' : '')
      + (fx.mem && fx.mem.addr === i ? ' ' + fx.mem.kind : '');
  }

  for (const [k] of LEVELS) {
    const slots = $('s-' + k).children, arr = S.cache[k];
    for (let i = 0; i < slots.length; i++) {
      const a = arr[i];
      if (a === undefined) { slots[i].className = 'slot empty'; slots[i].innerHTML = '<b>··</b>—'; }
      else { slots[i].className = 'slot'; slots[i].innerHTML = `<b>@${pad2(a)}</b>${fmt3(S.mem[a])}`; }
    }
    const el = $('c-' + k);
    el.classList.remove('hit', 'miss');
    if (fx.level && S.cacheOn) {
      if (fx.level === k) el.classList.add('hit');
      else if (fx.level === 'ram') el.classList.add('miss');
    }
  }
  $('caches').classList.toggle('off', !S.cacheOn);
  $('cache-note').textContent = S.cacheOn ? 'Slots show address and value. Cycle costs are a teaching model, not real timings.' : 'Cache is off: every memory access goes to RAM (40 cycles).';

  const stage = S.halted ? 'halt' : (r ? r.st.stage : null);
  ['fetch', 'decode', 'execute', 'halt'].forEach(k => $('st-' + k).classList.toggle('on', stage === k));

  if (r) {
    $('n-stage').textContent = r.st.stage;
    $('n-rtn').textContent = r.st.rtn;
    $('n-desc').textContent = r.st.desc(r.before, S);
    const nm = $('n-mem');
    if (fx.level) {
      const cost = { l1: 1, l2: 4, l3: 12, ram: RAM_COST }[fx.level];
      nm.textContent = fx.level === 'ram'
        ? (S.cacheOn ? `Cache miss: not in L1, L2 or L3, so it came from RAM (${cost} cycles).` : `Read from RAM (${cost} cycles).`)
        : `Cache hit in ${fx.level.toUpperCase()} (${cost} cycle${cost > 1 ? 's' : ''}).`;
      nm.className = 'nmem ' + (fx.level === 'ram' ? 'bad' : 'good');
    } else { nm.textContent = ''; nm.className = 'nmem'; }
  }
  const nx = peek(S);
  $('n-next').textContent = S.halted ? 'Program halted. Press Reset to run it again.' : `Next: ${nx.stage} · ${nx.rtn}`;

  const out = $('out');
  out.innerHTML = '<span class="lbl">Output</span>' + S.out.map(v => `<span class="o">${v}</span>`).join('');
  out.classList.toggle('flash', !!fx.out);

  $('k-cyc').textContent = S.cycles;
  $('k-ins').textContent = S.instr;
  const tot = S.hits + S.misses;
  $('k-hit').textContent = S.cacheOn && tot ? Math.round(100 * S.hits / tot) + '%' : '–';
  $('k-pred').textContent = `${score.ok}/${score.tries}`;
}

function showFb(kind, text) { const f = $('fb'); f.className = 'fb ' + kind; f.textContent = text; f.hidden = false; }
function hideFb() { $('fb').hidden = true; }
function hidePred() { awaiting = null; $('pred').hidden = true; }

function askPredict(st) {
  awaiting = st;
  $('info').hidden = true;
  const q = typeof st.predict.q === 'function' ? st.predict.q(S) : st.predict.q;
  $('pred-q').textContent = `Predict · ${st.rtn}: ${q}`;
  const box = $('pred-in'); box.innerHTML = '';
  if (st.predict.choice) {
    ['LDA', 'ADD', 'SUB', 'STA', 'BRA', 'BRZ', 'BRP', 'OUT', 'HLT'].forEach(m => {
      const b = document.createElement('button'); b.className = 'choice'; b.textContent = m;
      b.onclick = () => answer(m); box.appendChild(b);
    });
  } else {
    const inp = document.createElement('input'); inp.id = 'pred-num'; inp.inputMode = 'numeric'; inp.autocomplete = 'off'; inp.setAttribute('aria-label', 'Your prediction');
    inp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); answer(inp.value); } });
    const chk = document.createElement('button'); chk.className = 'btn primary'; chk.textContent = 'Check';
    chk.onclick = () => answer(inp.value);
    box.append(inp, chk);
    setTimeout(() => inp.focus(), 0);
  }
  const sk = document.createElement('button'); sk.className = 'btn'; sk.textContent = 'Show me';
  sk.onclick = () => answer(null); box.appendChild(sk);
  $('pred').hidden = false;
  hideFb();
}
function answer(ans) {
  const st = awaiting; if (!st) return;
  const c = clone(S); stepOnce(c);
  const exp = GET[st.predict.key](c);
  const shown = (FMT[st.predict.key] || fmt3)(exp);
  hidePred();
  if (ans === null || String(ans).trim() === '') { doStep(); showFb('neutral', `Answer: ${shown}`); return; }
  let ok;
  if (typeof exp === 'number') ok = /^-?\d+$/.test(String(ans).trim()) && parseInt(ans, 10) === exp;
  else ok = String(ans).trim().toUpperCase() === String(exp);
  score.tries++; if (ok) score.ok++;
  doStep();
  showFb(ok ? 'good' : 'bad', ok ? `✓ Correct: ${shown}` : `✗ Not quite. You said ${String(ans).trim()}, the answer is ${shown}.`);
}

function doStep() { $('info').hidden = true; render(stepOnce(S)); }
function onStep() {
  if (running) return;
  if (S.halted) { showFb('neutral', 'The program has halted. Press Reset to run it again.'); return; }
  if (awaiting) { answer(null); return; }
  const st = peek(S);
  if ($('t-pred').checked && st.predict) { askPredict(st); return; }
  hideFb(); doStep();
}
function onInstr() {
  if (running || S.halted) return;
  hidePred(); hideFb();
  let r, n = 0;
  do { r = stepOnce(S); n++; } while (r && !S.halted && !(r.st.stage === 'execute' && !S.queue.length) && n < 50);
  render(r);
}
function tick() {
  if (!running) return;
  if (S.halted) { stopRun(); return; }
  render(stepOnce(S));
  timer = setTimeout(tick, speedMs());
}
function stopRun() { running = false; clearTimeout(timer); $('b-run').textContent = 'Run'; }
function onRun() {
  if (running) { stopRun(); return; }
  if (S.halted) reset();
  hidePred(); hideFb(); $('info').hidden = true;
  running = true; $('b-run').textContent = 'Pause'; tick();
}
function reset() {
  stopRun(); hidePred(); hideFb();
  S = freshState(loaded, $('t-cache').checked);
  $('n-stage').textContent = 'Ready';
  $('n-rtn').textContent = 'PC = 00';
  $('n-desc').textContent = 'The program is loaded into RAM. The program counter holds 00, so the first instruction will be fetched from address 00. Press Step.';
  $('n-mem').textContent = '';
  render(null);
}
function loadProgram() {
  const { mem, errors } = assemble($('code').value);
  const msg = $('asm-msg');
  if (errors.length) { msg.className = 'err'; msg.textContent = errors.join('\n'); return false; }
  loaded = mem; msg.className = 'ok'; msg.textContent = 'Loaded into RAM. PC reset to 00.';
  reset(); return true;
}

function showInfo(key) {
  const d = INFO[key]; if (!d) return;
  $('info-t').textContent = d[0]; $('info-ref').textContent = d[1]; $('info-b').innerHTML = d[2];
  $('info').hidden = false;
}
function showCellInfo(i) {
  const v = S.mem[i];
  let as = '';
  if (v === 902) as = 'OUT';
  else if (v === 0) as = 'HLT (or the number 0)';
  else if (v > 0 && v < 900 && [1, 2, 3, 5, 6, 7, 8].includes(Math.floor(v / 100))) {
    const m = { 1: 'ADD', 2: 'SUB', 3: 'STA', 5: 'LDA', 6: 'BRA', 7: 'BRZ', 8: 'BRP' }[Math.floor(v / 100)];
    as = `${m} ${pad2(v % 100)}`;
  }
  $('info-t').textContent = `Address ${pad2(i)}`;
  $('info-ref').textContent = 'RAM';
  $('info-b').innerHTML = `<p>Holds <b class="mono">${fmt3(v)}</b>.${as ? ` If the PC points here, the CPU will treat it as the instruction <b class="mono">${as}</b>.` : ' This is not a valid instruction, so it can only be data.'}</p><p>If an instruction's operand is ${pad2(i)}, the CPU uses it as the number ${v}.</p>`;
  $('info').hidden = false;
}

document.addEventListener('click', e => {
  const cell = e.target.closest('.cell');
  if (cell) { showCellInfo(+cell.dataset.addr); return; }
  const t = e.target.closest('[data-info]');
  if (t) showInfo(t.dataset.info);
});
$('info-x').onclick = () => { $('info').hidden = true; };
$('b-step').onclick = onStep;
$('b-instr').onclick = onInstr;
$('b-run').onclick = onRun;
$('b-reset').onclick = reset;
$('b-load').onclick = loadProgram;
$('t-cache').onchange = e => { S.cacheOn = e.target.checked; if (!S.cacheOn) S.cache = { l1: [], l2: [], l3: [] }; render(null); };
$('t-pred').onchange = e => { if (!e.target.checked) hidePred(); };
$('t-speed').oninput = setDur;
$('sample').onchange = e => { $('code').value = SAMPLES[e.target.value]; loadProgram(); };
document.addEventListener('keydown', e => {
  const tag = (e.target.tagName || '').toLowerCase();
  if (tag === 'textarea' || tag === 'input' || tag === 'select') return;
  if (e.key === ' ' || e.key === 'ArrowRight') { e.preventDefault(); onStep(); }
});

/* ---------- challenges ---------- */
let passed = {};
try { passed = JSON.parse(localStorage.getItem('cpu-lab-passed') || '{}'); } catch (_) {}
const chWrap = $('chals');
CHALLENGES.forEach((c, i) => {
  const d = document.createElement('div'); d.className = 'ch' + (passed[i] ? ' pass' : ''); d.id = 'ch' + i;
  d.innerHTML = `<span class="n">${passed[i] ? '✓' : i + 1}</span><div><h4>${c.t}${c.tag ? `<em>${c.tag}</em>` : ''}</h4><p>${c.d}</p></div><button class="btn sm">Check</button><p class="res"></p>`;
  d.querySelector('button').onclick = () => checkChallenge(i);
  chWrap.appendChild(d);
});
function checkChallenge(i) {
  const c = CHALLENGES[i], row = $('ch' + i), res = row.querySelector('.res');
  const { mem, errors } = assemble($('code').value);
  if (errors.length) { res.className = 'res bad'; res.textContent = errors[0]; return; }
  const s = freshState(mem, true);
  let n = 0; while (!s.halted && n < 40000) { stepOnce(s); n++; }
  if (!s.halted) { res.className = 'res bad'; res.textContent = 'Your program never reached HLT. Check your loop exits.'; return; }
  const ok = s.out.length === c.expect.length && s.out.every((v, k) => v === c.expect[k]);
  if (ok) {
    res.className = 'res good';
    res.textContent = `Passed in ${s.instr} instructions and ${s.cycles} model cycles. Can you make it shorter?`;
    row.classList.add('pass'); row.querySelector('.n').textContent = '✓';
    passed[i] = true; try { localStorage.setItem('cpu-lab-passed', JSON.stringify(passed)); } catch (_) {}
  } else {
    res.className = 'res bad';
    res.textContent = `Output was ${s.out.length ? s.out.join(', ') : 'nothing'}. Expected ${c.expect.join(', ')}.`;
  }
}

try{const h=document.getElementById('howto');if(localStorage.getItem('cpu-lab-howto')==='closed')h.open=false;h.addEventListener('toggle',()=>{try{localStorage.setItem('cpu-lab-howto',h.open?'open':'closed')}catch(_){}})}catch(_){}
$('code').value = SAMPLES.deck;
setDur();
render(null);
})();
</script>

</body>
</html>s