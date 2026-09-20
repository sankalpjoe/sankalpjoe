"""Generate original, self-contained SVG art and a GitHub-safe profile README."""
import html
import json
import math
import random
import textwrap
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, LINE = "#090d14", "#10161f", "#26323d"
INK, MUTED, MINT = "#f1f0e8", "#a4b1bf", "#c5f58a"
FONT = "Arial, Helvetica, sans-serif"
MONO = "'Courier New', monospace"


def text(x, y, value, size=16, color=INK, weight=400, mono=False, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{MONO if mono else FONT}" '
            f'font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>'
            f'{html.escape(str(value))}</text>')


def lines(x, y, value, width, size=18, color=MUTED, leading=27):
    return "".join(text(x, y + i * leading, line, size, color)
                   for i, line in enumerate(textwrap.wrap(value, width)))


def line(x1, y1, x2, y2, color=LINE, extra=""):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" fill="none" {extra}/>'


def circle(x, y, r, color, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'


def path(points, color, opacity=1, width=1, closed=False):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points) + (" Z" if closed else "")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'


def svg(width, height, body, title, description=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>'
            '<defs><radialGradient id="glow"><stop stop-color="#9f88ff" stop-opacity=".18"/>'
            '<stop offset="1" stop-color="#090d14" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="accent" x2="1" y2="1"><stop stop-color="#c5f58a"/>'
            '<stop offset=".5" stop-color="#9bc5ec"/><stop offset="1" stop-color="#b9a4ff"/></linearGradient>'
            '</defs><style>.orbit{transform-box:fill-box;transform-origin:center;animation:turn 60s linear infinite}'
            '.pulse{animation:breathe 5s ease-in-out infinite}'
            '.cipher{stroke-dasharray:6 10;animation:cipher 5s linear infinite}'
            '.travel{animation:travel 7s linear infinite}'
            '@keyframes turn{to{transform:rotate(360deg)}}'
            '@keyframes breathe{50%{opacity:.35}}'
            '@keyframes cipher{to{stroke-dashoffset:-64}}'
            '@keyframes travel{0%{transform:translateX(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateX(260px);opacity:0}}'
            '@media(prefers-reduced-motion:reduce){.orbit,.pulse,.cipher,.travel{animation:none}}</style>'
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="20" fill="{BG}" stroke="{LINE}"/>'
            + body + '</svg>\n')


def torus(cx, cy, scale=1):
    # A projected torus, drawn as curves. Decorative geometry, never a data chart.
    result = circle(cx, cy, 260 * scale, "url(#glow)")
    def point(u, v):
        x = (144 + 56 * math.cos(v)) * math.cos(u)
        y = (144 + 56 * math.cos(v)) * math.sin(u)
        z = 56 * math.sin(v)
        yy = y * .48 - z * .88
        xx = x * .92 - yy * -.39
        yy = x * -.39 + yy * .92
        return cx + xx * scale, cy + yy * scale
    for j in range(38):
        pts = [point(i * math.tau / 130, j * math.tau / 38) for i in range(131)]
        result += path(pts, "#b9a4ff" if j % 3 else MINT, .22 if j % 3 else .45, .85 * scale)
    for i in range(42):
        pts = [point(i * math.tau / 42, j * math.tau / 70) for j in range(71)]
        result += path(pts, "#b9a4ff", .18, .7 * scale)
    result += f'<g class="orbit">'
    result += f'<ellipse cx="{cx}" cy="{cy}" rx="{224*scale}" ry="{224*scale}" fill="none" stroke="{LINE}" stroke-dasharray="3 12"/>'
    result += circle(cx + 224 * scale, cy, 4 * scale, MINT)
    result += circle(cx - 224 * scale, cy, 3 * scale, "#b9a4ff") + '</g>'
    return result


def hero(mobile=False):
    w, h = (600, 810) if mobile else (1200, 540)
    rng = random.Random(117)
    b = "".join(circle(rng.randrange(22, w-22), rng.randrange(22, h-22), rng.choice([.6, .8, 1.2]),
                       "#9caec1", f'opacity="{rng.uniform(.12,.4):.2f}"') for _ in range(90))
    b += text(38, 44, "SJ / FIELD NOTES", 14, MINT, mono=True, extra='letter-spacing="2"')
    b += text(w-38, 44, "VOL. 01", 13, MUTED, mono=True, extra='text-anchor="end"')
    b += line(38, 66, w-38, 66)
    if mobile:
        b += torus(310, 280, .84)
        b += text(36, 466, "Sankalp", 66, INK, 700)
        b += text(36, 534, "Joshi.", 66, INK, 700)
        b += text(36, 591, "Making the improbable", 27, MINT)
        b += text(36, 626, "computable.", 27, MINT)
        b += text(36, 685, "Quantum computing · AI · useful software", 19, MUTED)
        b += line(36, 718, 564, 718)
        b += text(36, 760, "@SANKALPJOE", 16, MUTED, mono=True)
        b += text(564, 760, "EXPLORE ↓", 16, MINT, mono=True, extra='text-anchor="end"')
    else:
        b += torus(930, 272, 1.04)
        b += text(46, 155, "AT THE EDGE OF PHYSICS & INTELLIGENCE", 13, MUTED, mono=True, extra='letter-spacing="1.8"')
        b += text(42, 246, "Sankalp Joshi.", 80, INK, 700, extra='letter-spacing="-3"')
        b += text(46, 310, "Making the improbable", 35, MINT)
        b += text(46, 354, "computable.", 35, MINT)
        b += text(46, 405, "Quantum computing · AI · useful software", 20, MUTED)
        b += line(38, 470, 1162, 470)
        b += text(46, 511, "@SANKALPJOE", 14, MUTED, mono=True)
        b += text(1160, 511, "RESEARCH / EXPERIMENTS / THINGS THAT WORK", 12, MUTED, mono=True, extra='text-anchor="end"')
    return svg(w, h, b, "Sankalp Joshi — making the improbable computable",
               "Quantum computing, AI and useful software. Original animated orbital artwork.")


def status(repo):
    if repo["name"] == "sankalpjoe":
        return "Profile"
    if repo["archived"]:
        return "Archived"
    if not repo["size"]:
        return "Empty"
    if repo["fork"]:
        return "Fork"
    return "Public"


def metrics(data, mobile=False):
    repos = data["repos"]
    projects = [r for r in repos if r["name"] != "sankalpjoe" and not r["fork"]]
    vals = [(len(repos), "PUBLIC REPOSITORIES"),
            (sum(bool(r["size"]) for r in projects), "PROJECTS WITH CONTENT"),
            (sum(r["stargazers_count"] for r in projects), "PROJECT STARS"),
            (sum(r["archived"] for r in projects), "ARCHIVED PROJECTS")]
    stamp = datetime.fromisoformat(data["fetched_at"]).strftime("%d %b %Y").upper()
    w, h = (600, 336) if mobile else (1200, 190)
    b = circle(31, 30, 4, MINT) + text(45, 35, "PUBLIC SIGNAL", 13, MINT, mono=True)
    b += text(w-26, 35, stamp, 12, MUTED, mono=True, extra='text-anchor="end"')
    for i, (value, label) in enumerate(vals):
        x = 30 + (i % 2) * 300 if mobile else 32 + i * 298
        y = 111 + (i // 2) * 138 if mobile else 114
        if i and (not mobile or i % 2):
            b += line(x-17, y-38, x-17, y+38)
        b += text(x, y, f"{value:02d}", 51, INK, 700, extra='letter-spacing="-2"')
        b += text(x, y+31, label, 12, MUTED, mono=True)
    return svg(w, h, b, "Public GitHub snapshot", "; ".join(f"{v} {k.lower()}" for v, k in vals) + f". Fetched {stamp}.")


def artwork(kind, color):
    # Each mini illustration uses a 320 x 190 coordinate space.
    b = circle(168, 97, 140, "url(#glow)")
    if kind == "lattice":
        def lattice_point(a, c):
            return 160+(a-c)*21, 20+(a+c)*11
        for i in range(7):
            b += path([lattice_point(i,j) for j in range(7)],color,.25)
            b += path([lattice_point(j,i) for j in range(7)],color,.25)
        for a in range(7):
            for c in range(7):
                b += circle(*lattice_point(a,c),1.8,color,'opacity=".4"')
        b += '<g class="cipher">'+path([lattice_point(0,2),lattice_point(6,2),lattice_point(6,5),lattice_point(1,5)],color,.9,2)+'</g>'
        b += circle(160,83,32,PANEL,f'stroke="{color}" stroke-opacity=".7"')
        b += f'<path d="M149 81 V73 A11 11 0 0 1 171 73 V81" fill="none" stroke="{color}" stroke-width="2"/>'
        b += f'<rect x="145" y="80" width="30" height="23" rx="4" fill="{BG}" stroke="{color}"/>'
        b += circle(160,89,3,color,'class="pulse"')+line(160,91,160,97,color)
        b += text(18,181,"KEM / HYBRID / EXPERIMENTS",10,MUTED,mono=True)
    elif kind == "circuit":
        for y in (40,90,140):
            b += text(6,y+4,"|0⟩",11,MUTED,mono=True)+line(32,y,300,y,color,'opacity=".4"')
        for x,y,label in ((60,40,"H"),(60,90,"Ry"),(60,140,"H"),(207,40,"Rz"),(207,90,"H"),(207,140,"Ry")):
            b += f'<rect x="{x-15}" y="{y-12}" width="30" height="24" rx="4" fill="{PANEL}" stroke="{color}"/>'
            b += text(x,y+4,label,12,color,mono=True,extra='text-anchor="middle"')
        b += line(134,40,134,90,color)+circle(134,40,4,color)+circle(134,90,9,BG,f'stroke="{color}"')
        b += line(128,90,140,90,color)+line(134,84,134,96,color)
        b += line(164,90,164,140,color)+circle(164,90,4,color)+circle(164,140,9,BG,f'stroke="{color}"')
        b += line(158,140,170,140,color)+line(164,134,164,146,color)
        for i,y in enumerate((40,90,140)):
            b += circle(33,y,3,MINT,f'class="travel" style="animation-delay:-{i*2}s"')
            b += f'<path d="M267 {y+6} A9 9 0 0 1 285 {y+6} M276 {y+6} L283 {y-5}" stroke="{color}" fill="none"/>'
        b += text(19,181,"ENCODE → EVOLVE → SAMPLE",10,MUTED,mono=True)
    elif kind == "radar":
        for r in (28, 55, 82):
            b += circle(167, 96, r, "none", f'stroke="{color}" stroke-opacity=".27"')
        b += line(68, 96, 266, 96) + line(167, 1, 167, 189)
        b += '<g class="pulse">'
        for x, y in [(121, 56), (203, 76), (185, 123), (128, 133), (224, 132)]:
            b += circle(x, y, 10, color, 'opacity=".08"') + circle(x, y, 3, color)
        b += '</g>' + path([(167,96),(208,24),(244,59)], color, .7)
        b += text(12, 176, "05 CITIES / SIGNAL → CONTEXT", 10, MUTED, mono=True)
    elif kind == "wave":
        for j in range(10):
            pts = [(x, 103 - 50*math.sin(x/50+j*.22)*math.exp(-((x-160)/95)**2)+j*3) for x in range(8,312,3)]
            b += path(pts, color, .18+j*.06)
        for i in range(22):
            x=18+i*13
            height=58*math.exp(-((x-165)/55)**2)
            b += f'<rect x="{x}" y="{170-height}" width="6" height="{height}" fill="{color}" opacity=".35"/>'
        b += text(12, 24, "|ψ⟩ → P(x)", 13, color, mono=True)
    elif kind == "portal":
        for cx in (106, 222):
            for i in range(13):
                b += f'<ellipse cx="{cx}" cy="95" rx="{28+i*2}" ry="{48+i*2.5}" fill="none" stroke="{color}" opacity="{.15+i*.035}"/>'
        b += path([(113, 25),(186,25),(203,42)], MINT, .8)
        b += path([(211, 165),(142,165),(124,148)], color, .8)
        b += text(146, 101, "↔", 30, MINT)
    elif kind == "mesh":
        def pt(a,b):
            return (165+(a-b)*16, 95+(a+b-8)*8-45*math.exp(-((a-4)**2+(b-4)**2)/5))
        for a in range(10):
            b += path([pt(a,j) for j in range(10)], color, .5)
            b += path([pt(j,a) for j in range(10)], color, .35)
        b += circle(*pt(4,4),4,MINT)
        b += text(20, 176, "CLUSTER → OPTIMIZE → EVALUATE", 10, MUTED, mono=True)
    elif kind == "network":
        points=[(52,64),(89,26),(158,45),(224,30),(272,75),(215,109),(271,152),(176,164),(119,125),(49,151),(31,108)]
        for a,c in [(0,1),(0,2),(0,10),(1,2),(2,3),(2,5),(2,8),(3,4),(4,5),(5,6),(5,7),(5,8),(6,7),(7,8),(8,9),(8,10),(9,10),(0,8)]:
            b += line(*points[a],*points[c],color,'opacity=".28"')
        for i,(x,y) in enumerate(points):
            b+=circle(x,y,13 if i in (2,5,8) else 5,color,f'opacity="{.15 if i in (2,5,8) else .7}"')
            if i in (2,5,8): b+=circle(x,y,4,color)
        b+=text(11,187,"SYNTHETIC DELHI / QAOA",10,MUTED,mono=True)
    elif kind == "horizon":
        b+=circle(103,59,29,"#e7ba83")+circle(225,58,28,color)+circle(237,49,27,BG)
        for i in range(9):
            pts=[(x,128+i*6-25*math.sin(x/50+i*.12)) for x in range(8,314,3)]
            b+=path(pts,color,.3+i*.055)
        b+=line(163,8,163,173,LINE,'stroke-dasharray="3 5"')
    elif kind == "docs":
        for i in range(3):
            x,y=92+i*30,22+i*15
            b+=f'<rect x="{x}" y="{y}" width="100" height="122" rx="8" fill="{PANEL}" stroke="{color}" stroke-opacity="{.3+i*.25}"/>'
            for k in range(4): b+=line(x+18,y+31+k*17,x+77-(k%2)*16,y+31+k*17,color,'opacity=".4"')
        b+=text(15,180,"MERGE / CONVERT / COMPRESS",10,MUTED,mono=True)
    else:
        rng=random.Random(14)
        for i in range(34):
            hh=rng.randint(5,56)
            b+=line(15+i*5,94-hh/2,15+i*5,94+hh/2,color,'stroke-width="2"')
        b+=path([(194,94),(220,94),(214,88)],color,.7)
        for j,width in enumerate((60,43,51,32)):
            b+=line(237,69+j*17,237+width,69+j*17,color,'stroke-width="3"')
        b+=text(16,176,"TRANSCRIPT → SUMMARY",10,MUTED,mono=True)
    return b


def card(project, repo, index, mobile=False):
    w,h=(600,535) if mobile else (1200,272)
    col=project["color"]
    b=text(28,37,f"{index:02d} / {project['category']}",12,col,mono=True,extra='letter-spacing="1"')
    b+=text(w-28,37,"ARCHIVED" if repo["archived"] else "↗",16,MUTED,mono=True,extra='text-anchor="end"')
    if mobile:
        b+=f'<g transform="translate(133 55) scale(1.05)">{artwork(project["art"],col)}</g>'
        b+=text(28,303,project["title"],32,INK,700,extra='letter-spacing="-.7"')
        b+=lines(28,339,project["subtitle"],47,20,col,27)
        b+=lines(28,402,project["description"],49,20,MUTED,27)
        b+=line(28,484,572,484)
        b+=text(28,514," · ".join(project["tags"]),14,MUTED,mono=True)
    else:
        b+=text(32,88,project["title"],34,INK,700,extra='letter-spacing="-.8"')
        b+=text(33,124,project["subtitle"],19,col)
        b+=lines(33,162,project["description"],76,17,MUTED,24)
        b+=text(33,240," / ".join(project["tags"]),13,MUTED,mono=True)
        b+=line(828,64,828,239)
        b+=f'<g transform="translate(852 52)">{artwork(project["art"],col)}</g>'
    return svg(w,h,b,project["title"],project["description"]+" Technologies: "+", ".join(project["tags"])+". Illustration is conceptual.")


def language_totals(data):
    totals=Counter()
    for repo in data["repos"]:
        if not repo["fork"] and not repo["archived"] and repo["name"]!="sankalpjoe":
            totals.update(repo["languages"])
    ordered=totals.most_common()
    if len(ordered)>5:
        ordered=ordered[:5]+[("Other",sum(n for _,n in ordered[5:]))]
    return ordered


def spectrum(data,mobile=False):
    w,h=(600,420) if mobile else (1200,340)
    ordered=language_totals(data)
    total=sum(n for _,n in ordered)
    colors=["#b9a4ff",MINT,"#91c7ff","#e7ba83","#e998bc","#7e8d9d"]
    b=text(28,39,"CODE SPECTRUM",13,MINT,mono=True,extra='letter-spacing="1"')
    b+=text(28,79,"What the public projects are made of.",24,INK,700)
    if not total:
        return svg(w,h,b+text(28,145,"No language data reported by GitHub yet.",19,MUTED),"Code spectrum")
    x=28
    for (name,n),col in zip(ordered,colors):
        ww=(w-56)*n/total
        b+=f'<rect x="{x:.2f}" y="110" width="{ww:.2f}" height="16" fill="{col}"/>'
        x+=ww
    for i,((name,n),col) in enumerate(zip(ordered,colors)):
        xx=30+(i%2)*284 if mobile else 30+(i%3)*388
        yy=174+(i//2)*71 if mobile else 174+(i//3)*58
        b+=circle(xx+4,yy-5,4,col)+text(xx+17,yy,name,16,INK)
        percent=n/total*100
        b+=text(xx+17,yy+22,f"{percent:.1f}%" if percent>=.1 else "<0.1%",14,MUTED,mono=True)
    note="GitHub language bytes; notebooks include JSON and outputs."
    note2="Excludes forks, archived repositories and this profile."
    b+=text(28,h-47,note,13,MUTED)+text(28,h-24,note2,13,MUTED)
    return svg(w,h,b,"Code spectrum",note+" "+note2)


def footer(mobile=False):
    w,h=(600,240) if mobile else (1200,206)
    b=text(32,39,"NEXT / AN INTERESTING PROBLEM",12,MINT,mono=True,extra='letter-spacing="1"')
    b+=text(30,97,"Let's compare notes.",35,INK,700)
    b+=text(32,137,"Quantum ideas. Generative models. Useful things.",18,MUTED)
    b+=line(32,h-48,w-32,h-48)
    b+=text(32,h-20,"SANKALP JOSHI",12,MUTED,mono=True)
    b+=text(w-32,h-20,"GITHUB.COM/SANKALPJOE ↗",12,MINT,mono=True,extra='text-anchor="end"')
    return svg(w,h,b,"Let's compare notes — Sankalp Joshi on GitHub")


def picture(asset,alt,link=None):
    img=(f'<picture>\n  <source media="(max-width: 600px)" srcset="assets/{asset}-mobile.svg">\n'
         f'  <img src="assets/{asset}.svg" width="100%" alt="{html.escape(alt,quote=True)}">\n</picture>')
    return f'<a href="{html.escape(link,quote=True)}">\n{img}\n</a>' if link else img


def markdown(data,config):
    repos={r["name"]:r for r in data["repos"]}
    projects=[p for p in config["projects"] if p["repo"] in repos and repos[p["repo"]]["size"]]
    parts=['<!-- Generated by scripts/refresh.py. Edit profile.json and scripts/render_profile.py. -->',
           '<a name="top"></a>', picture("hero","Sankalp Joshi. Making the improbable computable. Quantum computing, AI and useful software."),
           '<p align="center">\n<a href="#selected-work">Selected work</a> &nbsp; / &nbsp; <a href="#code-spectrum">Code spectrum</a> &nbsp; / &nbsp; <a href="#repository-index">Every public repo</a> &nbsp; / &nbsp; <a href="https://github.com/sankalpjoe?tab=repositories">Explore on GitHub ↗</a>\n</p>',
           'I explore the overlap between **quantum computing**, **machine learning**, and software that solves practical problems. My public work spans financial distributions, hybrid generative models, urban optimization, information dashboards, and everyday tools.',
           picture("signal","Public repository, project, star and archive counts from GitHub. See the full repository index below."),
           '## Selected work', 'From quantum experiments to tools you can use. Open a panel to explore its repository.']
    for i,p in enumerate(projects,1):
        parts.append(picture("project-"+p["repo"],p["title"]+" — "+p["description"],repos[p["repo"]]["html_url"]))
    parts += ['## Code spectrum',picture("spectrum","Language share by bytes in public repositories, excluding archives, forks and this profile."),
              '**Working vocabulary:** Qiskit · Amazon Braket · PennyLane · PyTorch · Transformers · Python · JavaScript / TypeScript · Streamlit',
              '## Repository index', 'Every public repository is listed here, including archived work and repositories with no content. New public repositories appear on the next successful refresh.',
              '| Repository | What you’ll find | State |\n| :--- | :--- | :--- |']
    curated={p["repo"]:p["description"] for p in config["projects"]}
    curated.update(config["catalogue_descriptions"])
    for r in sorted(data["repos"],key=lambda r:(r["archived"],r["name"].casefold())):
        desc=curated.get(r["name"]) or r["description"] or "No public description provided yet."
        if status(r)=="Empty": desc="No content in the public repository yet."
        safe=lambda s:html.escape(str(s)).replace("|","&#124;").replace("\n"," ").replace("\r"," ")
        parts.append(f'| <a href="{html.escape(r["html_url"],quote=True)}">{safe(r["name"])}</a> | {safe(desc)} | {status(r)} |')
    # Keep the table's rows contiguous in Markdown.
    table_start=next(i for i,p in enumerate(parts) if p.startswith('| Repository'))
    table="\n".join(parts[table_start:])
    parts=parts[:table_start]+[table]
    stamp=datetime.fromisoformat(data["fetched_at"]).strftime("%d %B %Y at %H:%M UTC")
    parts += [f'<sub>Public GitHub snapshot: {stamp}. [View source data](data/public-repos.json) · [Refresh workflow](https://github.com/sankalpjoe/sankalpjoe/actions/workflows/refresh-profile.yml). Project illustrations are conceptual; counts and language shares come from GitHub.</sub>',
              picture("footer","Let's compare notes. Find Sankalp Joshi on GitHub.","https://github.com/sankalpjoe"),
              '<p align="right"><a href="#top">Back to the observatory ↑</a></p>']
    return "\n\n".join(parts)+"\n"


def render(data):
    config=json.loads((ROOT/"profile.json").read_text(encoding="utf-8"))
    outputs={"readme.md":markdown(data,config)}
    for mobile in (False,True):
        suffix="-mobile" if mobile else ""
        outputs[f"assets/hero{suffix}.svg"]=hero(mobile)
        outputs[f"assets/signal{suffix}.svg"]=metrics(data,mobile)
        outputs[f"assets/spectrum{suffix}.svg"]=spectrum(data,mobile)
        outputs[f"assets/footer{suffix}.svg"]=footer(mobile)
        repos={r["name"]:r for r in data["repos"]}
        projects=[p for p in config["projects"] if p["repo"] in repos and repos[p["repo"]]["size"]]
        for i,p in enumerate(projects,1):
            outputs[f'assets/project-{p["repo"]}{suffix}.svg']=card(p,repos[p["repo"]],i,mobile)
    return outputs
