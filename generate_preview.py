from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Canvas ─────────────────────────────────────────────────────────────────
W, H = 1440, 5200
img = Image.new("RGB", (W, H), "#0a0e1a")
d = ImageDraw.Draw(img)

# ── Fonts (fallback to default if not installed) ────────────────────────────
def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except:
                pass
    return ImageFont.load_default()

F_XL  = font(54, bold=True)
F_LG  = font(38, bold=True)
F_MD  = font(28, bold=True)
F_SM  = font(22)
F_SMB = font(22, bold=True)
F_XS  = font(18)
F_XXS = font(15)
F_CODE= font(18)

# ── Colors ──────────────────────────────────────────────────────────────────
BG        = "#0a0e1a"
BG2       = "#0f1629"
BG_CARD   = "#141d35"
ACCENT    = "#6c63ff"
ACCENT2   = "#00d4ff"
ACCENT3   = "#ff6584"
TXT       = "#f0f4ff"
TXT2      = "#8892b0"
TXT_MUTED = "#4a5568"
BORDER    = "#1a2240"
GREEN     = "#22c55e"
WHITE     = "#ffffff"

# ── Helper: rounded rect ────────────────────────────────────────────────────
def rrect(draw, box, r, fill=None, outline=None, width=1):
    x0,y0,x1,y1 = box
    if fill:
        draw.rounded_rectangle([x0,y0,x1,y1], radius=r, fill=fill)
    if outline:
        draw.rounded_rectangle([x0,y0,x1,y1], radius=r, outline=outline, width=width)

# ── Helper: gradient bar ────────────────────────────────────────────────────
def gradient_bar(draw, x0, y0, x1, y1, c1=(108,99,255), c2=(0,212,255)):
    width = x1 - x0
    for i in range(width):
        t = i / max(width-1,1)
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(x0+i, y0), (x0+i, y1)], fill=(r,g,b))

# ── Helper: centered text ───────────────────────────────────────────────────
def ctext(draw, x, y, text, f, fill):
    bbox = draw.textbbox((0,0), text, font=f)
    tw = bbox[2]-bbox[0]
    draw.text((x - tw//2, y), text, font=f, fill=fill)

# ── Helper: section background ──────────────────────────────────────────────
def section_bg(y0, y1, alt=False):
    d.rectangle([0,y0,W,y1], fill=BG2 if alt else BG)

# ── Helper: grid lines overlay ─────────────────────────────────────────────
def draw_grid(y0, y1):
    for x in range(0, W, 60):
        d.line([(x,y0),(x,y1)], fill="#0d1225", width=1)
    for y in range(y0, y1, 60):
        d.line([(0,y),(W,y)], fill="#0d1225", width=1)

# ── Helper: glow circle ────────────────────────────────────────────────────
def glow_circle(img_pil, cx, cy, radius, color, alpha=30):
    overlay = Image.new("RGBA", img_pil.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    steps = 12
    for i in range(steps):
        a = int(alpha * (1 - i/steps) * (1 - i/steps))
        r = radius + i*18
        od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color+(a,))
    img_rgba = img_pil.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    return img_rgba.convert("RGB")

# ═══════════════════════════════════════════════════════════════════
#  SECTION 1 — NAV + HERO  (y: 0–900)
# ═══════════════════════════════════════════════════════════════════
draw_grid(0, 900)
img = glow_circle(img, 1150, 300, 260, (108,99,255))
img = glow_circle(img, 250, 750, 200, (0,212,255))
d = ImageDraw.Draw(img)

# NAV
d.rectangle([0,0,W,70], fill="#0a0e1ab0")
d.rectangle([0,69,W,70], fill=BORDER)
d.text((60,18), "< MJ />", font=font(28,bold=True), fill=ACCENT)
nav_items = ["Home","About","Skills","Experience","Projects","Contact"]
nx = 700
for i,item in enumerate(nav_items):
    clr = ACCENT if i==0 else TXT2
    d.text((nx,22), item, font=F_XS, fill=clr)
    nx += 120

# HERO LEFT
# Badge
rrect(d, [60,115,320,152], 20, fill="#1a1535", outline=ACCENT)
d.ellipse([76,128,92,144], fill=GREEN)
d.text((100,126), "Available for opportunities", font=F_XXS, fill=ACCENT)

# Title
d.text((60,170), "Hi, I'm", font=font(46,bold=True), fill=TXT)
# Gradient "Mahaboob Shaik"
for xi in range(680):
    t = xi/679
    r2 = int(108*(1-t)+0*t)
    g2 = int(99*(1-t)+212*t)
    b2 = int(255*(1-t)+255*t)
    d.rectangle([60+xi,235,61+xi,295], fill=(r2,g2,b2))
d.text((60,235), "Mahaboob Shaik", font=font(54,bold=True), fill=(0,0,0,0))
# Overlay text using mask trick — just draw it directly with gradient simulation
# (Pillow doesn't support gradient text natively; we'll use a lighter hack)
d.text((60,235), "Mahaboob Shaik", font=font(54,bold=True), fill=ACCENT)

# Role line
d.text((60,310), "I build  ", font=F_SM, fill=TXT2)
d.text((170,310), "Full Stack Web Apps", font=F_SMB, fill=ACCENT2)

# Description
desc_lines = [
    "Experienced developer with 4.8+ years of expertise crafting",
    "scalable solutions across PHP, React, Angular, Node.js,",
    "Flutter and more. Currently building enterprise-grade",
    "solutions at Infosys."
]
dy = 360
for line in desc_lines:
    d.text((60,dy), line, font=F_XS, fill=TXT2)
    dy += 26

# CTA buttons
rrect(d, [60,480,250,524], 10, fill=ACCENT)
d.text((97,492), "View My Work", font=F_SMB, fill=WHITE)
rrect(d, [270,480,440,524], 10, outline=ACCENT, width=2)
d.text((295,492), "Let's Connect", font=F_SMB, fill=TXT)

# Stats
sx = 60
for val, label in [("4.8+","Years Exp."),("10+","Technologies"),("5+","Projects")]:
    d.text((sx,560), val, font=font(34,bold=True), fill=ACCENT)
    d.text((sx,605), label, font=F_XXS, fill=TXT_MUTED)
    sx += 170
    if sx < 400:
        d.line([(sx-30,562),(sx-30,620)], fill=BORDER, width=1)

# CODE CARD (right)
cx0,cy0,cx1,cy1 = 760, 100, 1340, 520
rrect(d, [cx0,cy0,cx1,cy1], 16, fill=BG_CARD, outline=ACCENT+"55")
# Gradient top border
gradient_bar(d, cx0, cy0, cx1, cy0+3)
# Header
d.rectangle([cx0,cy0,cx1,cy0+44], fill="#0a0d1a")
d.ellipse([cx0+16,cy0+14,cx0+28,cy0+26], fill="#ff5f57")
d.ellipse([cx0+36,cy0+14,cx0+48,cy0+26], fill="#ffbd2e")
d.ellipse([cx0+56,cy0+14,cx0+68,cy0+26], fill="#28c840")
d.text((cx0+86,cy0+13), "developer.js", font=F_XXS, fill=TXT_MUTED)

code_lines = [
    ("const ", "6c63ff"), ("developer", "82aaff"), (" = {", "f0f4ff"),
]
code_block = [
    ('const developer = {',          None),
    ('  name: "Mahaboob Shaik",',    None),
    ('  role: "Tech Analyst",',      None),
    ('  company: "Infosys",',        None),
    ('  experience: 4.8,',           None),
    ('  skills: [',                  None),
    ('    "PHP", "React",',          None),
    ('    "Angular", "Node.js",',    None),
    ('    "Flutter", "Laravel"',     None),
    ('  ],',                         None),
    ('  passion: "Building great software"', None),
    ('};',                           None),
]
color_map = {
    'const': '#c792ea', '"': '#c3e88d', 'name': '#89ddff',
}
cy_code = cy0+60
for line, _ in code_block:
    # Simple colorization
    col = F_CODE
    fill_c = TXT2
    if line.strip().startswith('const'):
        fill_c = "#c792ea"
    elif '":' in line or 'name' in line or 'role' in line or 'company' in line or 'exp' in line or 'skill' in line or 'pass' in line:
        fill_c = "#89ddff"
    elif '"' in line and ':' not in line:
        fill_c = "#c3e88d"
    elif any(c.isdigit() for c in line) and ':' in line:
        fill_c = TXT2
    d.text((cx0+24, cy_code), line, font=F_CODE, fill=fill_c)
    cy_code += 30

# ═══════════════════════════════════════════════════════════════════
#  SECTION 2 — ABOUT  (y: 900–1500)
# ═══════════════════════════════════════════════════════════════════
section_bg(900, 1500, alt=True)
d.rectangle([900,899,W,900], fill=BORDER)

# Section header
d.text((640,930), "// about me", font=font(18), fill=ACCENT)
ctext(d, W//2, 965, "Who I Am", F_LG, TXT)
gradient_bar(d, W//2-60, 1015, W//2+60, 1019)

# Avatar area (right side)
acx, acy = 1050, 1220
# Rings
d.ellipse([acx-130,acy-130,acx+130,acy+130], outline=ACCENT+"55", width=2)
d.ellipse([acx-165,acy-165,acx+165,acy+165], outline=ACCENT2+"33", width=2)
# Avatar circle with gradient
for ri in range(100,0,-1):
    t = (100-ri)/100
    r2 = int(108*(1-t)+0*t)
    g2 = int(99*(1-t)+212*t)
    b2 = int(255)
    # draw concentric circles for gradient
    d.ellipse([acx-ri,acy-ri,acx+ri,acy+ri], fill=(r2,g2,b2))
gradient_bar(d, acx-100, acy-100, acx+100, acy+100, (108,99,255),(0,212,255))
rrect(d,[acx-100,acy-100,acx+100,acy+100],100,fill=ACCENT)
ctext(d, acx, acy-28, "MJ", font(72,bold=True), WHITE)

# Floating badges
badges = [
    ("PHP",    "#777bb6", acx-230, acy-150),
    ("React",  "#61dafb", acx+110, acy-110),
    ("Flutter","#45a8e0", acx-230, acy+80),
    ("Node.js","#689f38", acx+110, acy+110),
]
for label, col, bx, by in badges:
    bw = len(label)*12+30
    rrect(d,[bx,by,bx+bw,by+32],16,fill=col+"22",outline=col+"66")
    d.text((bx+12,by+7), label, font=F_XXS, fill=col)

# About text (left)
about_text = [
    ("A passionate Full Stack Developer based in Hyderabad, India,", F_SMB, TXT),
    ("with nearly 5 years of hands-on experience delivering robust", F_SMB, TXT),
    ("software solutions across web and mobile platforms.", F_SMB, TXT),
    ("", F_XS, TXT2),
    ("Technology Analyst at Infosys — leading enterprise PHP", F_XS, TXT2),
    ("projects for global clients like Pfizer. My journey spans", F_XS, TXT2),
    ("backend architecture to mobile app development.", F_XS, TXT2),
    ("", F_XS, TXT2),
    ("I thrive in agile environments, love code reviews, and am", F_XS, TXT2),
    ("constantly leveling up my skills with emerging technologies.", F_XS, TXT2),
]
ty = 1060
for text, f, col in about_text:
    if text:
        d.text((60, ty), text, font=f, fill=col)
    ty += 28

# Detail items
details = [
    ("📅  DOB: 20 June 1998",             1280),
    ("🏠  Location: Hyderabad, India",     1310),
    ("🎓  B.Tech ECE — MGIT (2019)",       1340),
    ("🌐  Languages: English, Hindi, Telugu, Urdu", 1370),
]
for text, dy_ in details:
    d.text((60, dy_), text, font=F_XS, fill=TXT2)

# ═══════════════════════════════════════════════════════════════════
#  SECTION 3 — SKILLS  (y: 1500–2220)
# ═══════════════════════════════════════════════════════════════════
section_bg(1500, 2220)
d.rectangle([0,1499,W,1500], fill=BORDER)

d.text((640,1530), "// technical skills", font=font(18), fill=ACCENT)
ctext(d, W//2, 1565, "My Tech Stack", F_LG, TXT)
gradient_bar(d, W//2-60, 1615, W//2+60, 1619)

skill_cats = [
    ("🌐 Frontend",  ["React","Angular","HTML5","CSS3","Bootstrap","JavaScript","jQuery"],
     ACCENT, 60,  1650),
    ("⚙ Backend",   ["PHP","Laravel","CodeIgniter","Node.js","REST APIs","Web Services"],
     ACCENT2, 520, 1650),
    ("📱 Mobile",    ["Flutter","Dart","Android / iOS"],
     "#a855f7", 980, 1650),
    ("📊 Databases", ["MySQL","MongoDB"],
     ACCENT3,  60, 1900),
    ("🔧 Tools",     ["Git","Agile/Scrum","Code Reviews","ASP.NET MVC"],
     "#f59e0b", 520, 1900),
    ("💡 Soft Skills",["Leadership","Team Collaboration","Time Management","Problem Solving"],
     GREEN,    980, 1900),
]

for cat_name, tags, accent_col, sx, sy in skill_cats:
    # Card
    rrect(d, [sx,sy,sx+380,sy+200], 16, fill=BG_CARD, outline=BORDER)
    gradient_bar(d, sx, sy, sx+380, sy+3,
                 tuple(int(accent_col.lstrip('#')[i:i+2],16) for i in (0,2,4)),
                 (0,212,255))
    d.text((sx+16,sy+18), cat_name, font=F_SMB, fill=TXT)
    # Tags
    tx, ty2 = sx+16, sy+58
    for tag in tags:
        tw = len(tag)*9+20
        if tx+tw > sx+360:
            tx = sx+16
            ty2 += 36
        rrect(d,[tx,ty2,tx+tw,ty2+26],13,fill=accent_col+"22",outline=accent_col+"55")
        d.text((tx+10,ty2+5), tag, font=F_XXS, fill=accent_col)
        tx += tw+8

# Legend
lx = W//2 - 220
ctext(d, W//2, 2160, "■ Expert   ■ Proficient   ■ Familiar", F_XXS, TXT_MUTED)

# ═══════════════════════════════════════════════════════════════════
#  SECTION 4 — EXPERIENCE  (y: 2220–3300)
# ═══════════════════════════════════════════════════════════════════
section_bg(2220, 3300, alt=True)
d.rectangle([0,2219,W,2220], fill=BORDER)

d.text((630,2250), "// work history", font=font(18), fill=ACCENT)
ctext(d, W//2, 2285, "Experience", F_LG, TXT)
gradient_bar(d, W//2-60, 2335, W//2+60, 2339)

exp_data = [
    ("Technology Analyst", "Infosys", "Nov 2022 – Present",
     ["Proactively managing multiple enterprise PHP projects simultaneously.",
      "Collaborating with cross-functional teams for innovative solutions.",
      "Employing agile methodologies and best practices for efficiency.",
      "Identifying and resolving software defects and performance issues.",
      "Participating in code reviews, fostering knowledge-sharing culture."],
     ["PHP","Agile","Laravel","Enterprise"], 2370),
    ("Mobile Developer", "NoHung (Freelance)", "May 2022 – Apr 2023",
     ["Delivered impactful PHP and mobile solutions, optimizing UX.",
      "Developed a rider application using the Flutter framework.",
      "Collaborated with clients, delivering tailored solutions on time.",
      "Employed proactive problem-solving for smooth app operation."],
     ["PHP","Flutter","Freelance","Mobile"], 2720),
    ("Full Stack Developer", "Asthra Interactive Media", "Sep 2019 – Oct 2022",
     ["Developed robust backend solutions ensuring seamless functionality.",
      "Collaborated with designers and front-end developers on mobile apps.",
      "Transitioned from backend to mobile developer, showing versatility.",
      "Managed multiple projects simultaneously with timely delivery."],
     ["PHP","Flutter","Full Stack","LMS","CRM"], 3000),
]

for role, company, period, points, tags, ey in exp_data:
    # Timeline dot
    d.ellipse([240,ey+18,258,ey+36], fill=ACCENT)
    d.ellipse([243,ey+21,255,ey+33], fill=ACCENT)
    d.line([(249,ey+36),(249,ey+300)], fill=BORDER, width=2)

    # Card
    card_h = 60 + len(points)*28 + 50
    rrect(d, [270,ey,1380,ey+card_h], 16, fill=BG_CARD, outline=BORDER)

    # Header
    d.text((295,ey+18), role, font=F_MD, fill=TXT)
    d.text((295,ey+55), company, font=F_SMB, fill=ACCENT)
    # Period badge
    bw = len(period)*10+20
    rrect(d,[1380-bw-20,ey+18,1380-20,ey+46],12,fill=BG,outline=BORDER)
    d.text((1380-bw-10,ey+24), period, font=F_XXS, fill=TXT_MUTED)

    # Points
    py = ey+88
    for pt in points:
        d.text((310,py), "▹", font=F_XS, fill=ACCENT)
        d.text((330,py), pt, font=F_XS, fill=TXT2)
        py += 28

    # Tags
    tx2 = 295
    for tag in tags:
        tw2 = len(tag)*10+20
        rrect(d,[tx2,py+8,tx2+tw2,py+32],12,fill=ACCENT+"22",outline=ACCENT+"44")
        d.text((tx2+10,py+13), tag, font=F_XXS, fill=ACCENT)
        tx2 += tw2+8

# ═══════════════════════════════════════════════════════════════════
#  SECTION 5 — PROJECTS  (y: 3300–4500)
# ═══════════════════════════════════════════════════════════════════
section_bg(3300, 4500)
d.rectangle([0,3299,W,3300], fill=BORDER)

d.text((680,3330), "// portfolio", font=font(18), fill=ACCENT)
ctext(d, W//2, 3365, "Featured Projects", F_LG, TXT)
gradient_bar(d, W//2-60, 3415, W//2+60, 3419)

projects = [
    ("🎯", "Enterprise", "Infosys — Pfizer", "Mission Control 2",
     "Enterprise-level mission control platform for Pfizer. Led a cross-\n"
     "functional team overseeing implementation and execution, ensuring\n"
     "seamless integration of new processes and technologies.",
     ["PHP","Laravel","MySQL","JavaScript"], "May 2023 – Present",
     60, 3450, True),
    ("📋", "Healthcare", "Infosys — Pfizer", "Registry Quality Control Mgmt System",
     "Comprehensive clinical trial records management. Built 4 functional\n"
     "dashboards: QC Operations, QC Review, Queries, Administration.\n"
     "Ensured seamless functionality for all stakeholders.",
     ["PHP","Laravel","MySQL","React"], "Sep 2023 – Present",
     760, 3450, True),
    ("🚗", "Mobile", "NoHung", "Rider Application",
     "Full-stack freelance project featuring a Flutter-based rider app\n"
     "with PHP backend. Implemented innovative features enhancing\n"
     "user experience and satisfaction.",
     ["Flutter","Dart","PHP","MySQL"], "May 2022 – Apr 2023",
     60, 3930, False),
    ("🎓", "EdTech", "Asthra Interactive Media", "Prime Learning Platform",
     "Built and optimized an LMS from the ground up, including a sales\n"
     "CRM website and multiple LMS websites delivering seamless\n"
     "user experiences for education platforms.",
     ["PHP","CodeIgniter","Flutter","MySQL"], "Oct 2019 – Aug 2022",
     760, 3930, False),
]

for icon, badge, company, title, desc, tech, period, px, py_, featured in projects:
    pw = 660
    card_h = 410 if featured else 380

    # Card background
    bc = ACCENT+"33" if featured else BORDER
    rrect(d, [px,py_,px+pw,py_+card_h], 16, fill=BG_CARD, outline=bc, width=2 if featured else 1)
    if featured:
        gradient_bar(d, px, py_, px+pw, py_+4)

    # Icon + badge
    d.text((px+20, py_+18), icon, font=font(36), fill=TXT)
    bw3 = len(badge)*10+20
    rrect(d,[px+pw-bw3-16,py_+20,px+pw-16,py_+46],12,fill=ACCENT,outline=None)
    d.text((px+pw-bw3-6,py_+25), badge, font=F_XXS, fill=WHITE)

    d.text((px+20,py_+68), company, font=F_XXS, fill=TXT_MUTED)
    d.text((px+20,py_+92), title, font=F_SMB, fill=TXT)

    # Desc
    dy2 = py_+130
    for line in desc.split('\n'):
        d.text((px+20, dy2), line.strip(), font=F_XXS, fill=TXT2)
        dy2 += 24

    # Tech tags
    tx3 = px+20
    ty3 = dy2+12
    for t in tech:
        tw3 = len(t)*9+18
        rrect(d,[tx3,ty3,tx3+tw3,ty3+26],4,fill=BG,outline=BORDER)
        d.text((tx3+8,ty3+5), t, font=F_XXS, fill=TXT_MUTED)
        tx3 += tw3+6

    # Period
    d.text((px+20,ty3+38), f"📅  {period}", font=F_XXS, fill=TXT_MUTED)

# ═══════════════════════════════════════════════════════════════════
#  SECTION 6 — CONTACT  (y: 4500–5000)
# ═══════════════════════════════════════════════════════════════════
section_bg(4500, 5000, alt=True)
d.rectangle([0,4499,W,4500], fill=BORDER)

d.text((660,4530), "// get in touch", font=font(18), fill=ACCENT)
ctext(d, W//2, 4565, "Let's Connect", F_LG, TXT)
gradient_bar(d, W//2-60, 4615, W//2+60, 4619)
ctext(d, W//2, 4635, "Have a project in mind? I'd love to hear from you.", F_XS, TXT2)

contacts = [
    ("📞", "Phone", "+91 98481 63611",    220),
    ("✉", "Email", "mahaboobjani665@gmail.com", 620),
    ("📍", "Location", "Hyderabad, India", 1050),
]
for icon, label, value, cx_ in contacts:
    cw = 340
    rrect(d,[cx_,4680,cx_+cw,4920],16,fill=BG_CARD,outline=BORDER)
    gradient_bar(d,cx_,4916,cx_+cw,4920,(108,99,255),(0,212,255))
    ctext(d, cx_+cw//2, 4700, icon, font(44), TXT)
    ctext(d, cx_+cw//2, 4770, label, F_XXS, TXT_MUTED)
    ctext(d, cx_+cw//2, 4800, value, F_XS, TXT2)

# ═══════════════════════════════════════════════════════════════════
#  FOOTER  (y: 5000–5200)
# ═══════════════════════════════════════════════════════════════════
section_bg(5000, 5200)
d.rectangle([0,4999,W,5000], fill=BORDER)
ctext(d, W//2, 5050, "< MJ />", font(32,bold=True), ACCENT)
ctext(d, W//2, 5100, "© 2024 Mahaboob Shaik. Crafted with passion in Hyderabad.", F_XS, TXT_MUTED)
ctext(d, W//2, 5135, "All particulars are true to the best of my knowledge and belief.", F_XXS, TXT_MUTED)

# ── Save ───────────────────────────────────────────────────────────
out = "/home/user/developer_blog/blog_preview.png"
img.save(out, "PNG", quality=95)
print(f"Saved: {out}  ({W}x{H})")
