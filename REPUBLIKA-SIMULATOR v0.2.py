#!/usr/bin/env python3
"""REPUBLIKA SIMULATOR v1.0 -- Single-file Pygame political strategy game.
All persons fictional. Place names are real Philippine geography.
pip install pygame  |  python3 republika_simulator.py
"""
import pygame, sys, json, os, random, math, time
from dataclasses import dataclass, field, asdict

# ── CONSTANTS ────────────────────────────────────────────────
W, H, FPS = 1280, 720, 60
TITLE = "REPUBLIKA SIMULATOR"
SAVES = ["save_slot_1.json","save_slot_2.json","save_slot_3.json"]

C_NAV=(10,22,40); C_DARK=(5,12,25); C_PAN=(15,30,55); C_PAN2=(22,44,75)
C_GOLD=(255,215,0); C_GD=(180,145,0); C_RED=(204,0,0); C_RL=(240,60,60)
C_WHT=(245,245,245); C_GRY=(110,120,140); C_GRN=(50,200,80)
C_YLW=(220,185,30); C_BLU=(40,120,220); C_BLK=(0,0,0)

MONTHS=["","Ene","Peb","Mar","Abr","May","Hun","Hul","Ago","Set","Okt","Nob","Dis"]

# ── LANGUAGE / TRANSLATION ────────────────────────────────────
LANG = "FIL"   # "FIL" | "ENG"  -- toggled by translate button on main menu

STRINGS = {
    # Main menu
    "subtitle"      :{"FIL":"Pamunuan ang Bansa -- Itaguyod ang Bayan",
                       "ENG":"Lead the Nation -- Defend the People"},
    "btn_new"       :{"FIL":"[ BAGONG LARO ]",     "ENG":"[ NEW GAME ]"},
    "btn_load"      :{"FIL":"[ I-LOAD ]",           "ENG":"[ LOAD GAME ]"},
    "btn_settings"  :{"FIL":"[ MGA SETTING ]",      "ENG":"[ SETTINGS ]"},
    "btn_quit"      :{"FIL":"[ LUMABAS ]",          "ENG":"[ QUIT ]"},
    "disclaimer"    :{"FIL":"v1.0  |  Lahat ng pangalan ay gawa-gawa",
                       "ENG":"v1.0  |  All names are entirely fictional"},
    "translate_btn" :{"FIL":"[EN]",               "ENG":"[FIL]"},
    # Setup screens
    "step1_title"   :{"FIL":"HAKBANG 1/4 -- PANGALAN",
                       "ENG":"STEP 1/4 -- YOUR NAME"},
    "step1_prompt"  :{"FIL":"Ilagay ang inyong pangalan, Presidente:",
                       "ENG":"Enter your name, Mr/Ms President:"},
    "step1_err"     :{"FIL":"Maglagay ng pangalan!",
                       "ENG":"Please enter a name!"},
    "step1_confirm" :{"FIL":"[ KUMPIRMAHIN ]",      "ENG":"[ CONFIRM ]"},
    "step2_title"   :{"FIL":"HAKBANG 2/4 -- FOREIGN POLICY STANCE",
                       "ENG":"STEP 2/4 -- FOREIGN POLICY STANCE"},
    "step3_title"   :{"FIL":"HAKBANG 3/4 -- POLITICAL SYSTEM",
                       "ENG":"STEP 3/4 -- POLITICAL SYSTEM"},
    "step3_warn"    :{"FIL":"!  Ang authoritarian path ay may espesyal na events ngunit mapanganib sa demokrasya",
                       "ENG":"!  Authoritarian paths unlock special events but risk democratic stats"},
    "step4_title"   :{"FIL":"HAKBANG 4/4 -- ANTAS NG KAHIRAPAN",
                       "ENG":"STEP 4/4 -- DIFFICULTY LEVEL"},
    "next_btn"      :{"FIL":"[ SUSUNOD ]",          "ENG":"[ NEXT ]"},
    "start_btn"     :{"FIL":"[ SIMULAN ]",          "ENG":"[ START ]"},
    "back_btn"      :{"FIL":"<- BUMALIK",            "ENG":"<- BACK"},
    # Load screen
    "load_title"    :{"FIL":"LOAD GAME -- PILIIN ANG SLOT",
                       "ENG":"LOAD GAME -- CHOOSE A SLOT"},
    "empty_slot"    :{"FIL":"-- WALANG DATOS --",     "ENG":"-- EMPTY SLOT --"},
    # In-game nav
    "nav_policies"  :{"FIL":"PATAKARAN",            "ENG":"POLICIES"},
    "nav_budget"    :{"FIL":"BADYET",               "ENG":"BUDGET"},
    "nav_events"    :{"FIL":"MGA PANGYAYARI",       "ENG":"EVENTS"},
    "nav_typhoon"   :{"FIL":"BAGYO",                "ENG":"TYPHOONS"},
    "nav_diplo"     :{"FIL":"DIPLOMASYA",             "ENG":"DIPLOMACY"},
    "nav_achiev"    :{"FIL":"MGA TAGUMPAY",          "ENG":"ACHIEVEMENTS"},
    "nav_research"  :{"FIL":"PANANALIKSIK",           "ENG":"RESEARCH"},
    "pause_resume"  :{"FIL":"> IPAGPATULOY",        "ENG":"> RESUME"},
    "pause_save"    :{"FIL":"SAVE  I-SAVE",           "ENG":"SAVE  SAVE GAME"},
    "pause_menu"    :{"FIL":"MENU  BUMALIK SA MENU",  "ENG":"MENU  MAIN MENU"},
    "pause_quit"    :{"FIL":"Quit",           "ENG":"Quit"},
    # Annual / typhoon panels
    "annual_title"  :{"FIL":"TAUNANG ULAT",         "ENG":"ANNUAL REVIEW"},
    "ok_btn"        :{"FIL":"[ SUSUNOD ]",          "ENG":"[ CONTINUE ]"},
    "ty_title"      :{"FIL":"TY  ULAT NG BAGYO",   "ENG":"TY  TYPHOON SEASON REPORT"},
    "relief_low"    :{"FIL":"MABABA  P100B",        "ENG":"LOW  P100B"},
    "relief_mid"    :{"FIL":"KATAMTAMAN P250B",     "ENG":"MODERATE  P250B"},
    "relief_high"   :{"FIL":"MATAAS  P400B",        "ENG":"HIGH  P400B"},
    "close_btn"     :{"FIL":"ISARA",                "ENG":"CLOSE"},
    # Game over / victory
    "go_title"      :{"FIL":"TAPOS NA ANG LARO",    "ENG":"GAME OVER"},
    "go_retry"      :{"FIL":"[ MULI ]",             "ENG":"[ RETRY ]"},
    "go_menu"       :{"FIL":"[ MENU ]",             "ENG":"[ MENU ]"},
    "vic_title"     :{"FIL":"KATAPUSAN NG TERMINO -- ULAT",
                       "ENG":"END OF TERM -- FINAL REPORT"},
    "vic_menu"      :{"FIL":"[ BUMALIK SA MENU ]",  "ENG":"[ BACK TO MENU ]"},
    # In-game right panel
    "nat_stats"     :{"FIL":"PAMBANSANG ISTATISTIKA","ENG":"NATIONAL STATS"},
    "for_rel"       :{"FIL":"UGNAYANG PANLABAS",     "ENG":"FOREIGN RELATIONS"},
    "appr_trend"    :{"FIL":"Trend ng Approval",     "ENG":"Approval trend"},
    # In-game top bar labels
    "topbar_appr"   :{"FIL":"Suporta",               "ENG":"Approval"},
    "topbar_term"   :{"FIL":"Termino",               "ENG":"Term"},
    # Policy panel
    "pol_title"     :{"FIL":"PAMAMAHALA NG PATAKARAN","ENG":"POLICY MANAGEMENT"},
    "pol_hint"      :{"FIL":"Aktibo: {a}/{m}  |  Gastos at epekto bawat buwan  |  I-toggle kahit kailan  |  SCROLL",
                       "ENG":"Active: {a}/{m}  |  Cost & effects deducted monthly  |  Toggle anytime  |  SCROLL"},
    "pol_free"      :{"FIL":"LIBRE",                 "ENG":"FREE"},
    "pol_sys_change":{"FIL":"SYS PAGBABAGO NG SISTEMA","ENG":"SYS SYSTEM CHANGE"},
    # Budget panel
    "bud_title"     :{"FIL":"PANGKALAHATANG BADYET",  "ENG":"BUDGET OVERVIEW"},
    "bud_budget"    :{"FIL":"Taunang Badyet",         "ENG":"Annual Budget"},
    "bud_debt"      :{"FIL":"Taunang Utang",          "ENG":"Annual Debt"},
    "bud_rev"       :{"FIL":"Tinatayang Kita",        "ENG":"Est. Revenue"},
    "bud_active"    :{"FIL":"Aktibong Patakaran",     "ENG":"Active Policies"},
    "bud_relief"    :{"FIL":"Badyet sa Kalamidad",    "ENG":"Disaster Relief Alloc"},
    "bud_alloc"     :{"FIL":"PAGLALAAN NG BADYET",    "ENG":"BUDGET ALLOCATION"},
    # Events panel
    "ev_title"      :{"FIL":"TALAAN NG MGA PANGYAYARI","ENG":"EVENT LOG"},
    # Typhoon log
    "ty_log_title"  :{"FIL":"TALAAN NG BAGYO",        "ENG":"TYPHOON LOG"},
    "ty_log_yr"     :{"FIL":"Taon",                   "ENG":"Year"},
    "ty_log_name"   :{"FIL":"Bagyo",                  "ENG":"Storm"},
    "ty_log_cat"    :{"FIL":"Uri",                    "ENG":"Cat"},
    "ty_log_reg"    :{"FIL":"Rehiyon",                "ENG":"Region"},
    "ty_log_dmg"    :{"FIL":"Pinsala(PB)",            "ENG":"Damage(PB)"},
    "ty_log_out"    :{"FIL":"Resulta",                "ENG":"Outcome"},
    # Navbar hint
    "nav_hint"      :{"FIL":"ESC=Menu  SPACE=Susunod na Buwan",
                       "ENG":"ESC=Menu  SPACE=Next Month"},
    # Annual review lines
    "ann_year_done" :{"FIL":"Taon {y} ay tapos na.",      "ENG":"Year {y} is complete."},
    "ann_budget"    :{"FIL":"Badyet: P{b:.0f}B  |  Utang: P{d:.0f}B",
                       "ENG":"Budget: P{b:.0f}B  |  Debt: P{d:.0f}B"},
    "ann_appr"      :{"FIL":"Suporta: {a:.1f}%",         "ENG":"Approval: {a:.1f}%"},
    "ann_deficit"   :{"FIL":"! DEPISITO! P{v:.0f}B",    "ENG":"! DEFICIT! P{v:.0f}B"},
    "ann_corr_warn" :{"FIL":"! Mataas na korapsyon -- krisis ang posible!",
                       "ENG":"! High corruption -- crisis events likely!"},
    "ann_appr_warn" :{"FIL":"! Napakababang suporta -- panganib sa puwesto!",
                       "ENG":"! Very low approval -- your position is at risk!"},
    "ann_policies"  :{"FIL":"Aktibong Patakaran: {n}",   "ENG":"Active Policies: {n}"},
    "ann_typhoons"  :{"FIL":"Typhoon season: {n} bagyo",  "ENG":"Typhoon season: {n} storms"},
    # Typhoon resolve lines
    "ty_hit"        :{"FIL":"{n} bagyo ang humampas ngayong taon.",
                       "ENG":"{n} typhoon(s) struck the country this year."},
    "ty_total"      :{"FIL":"Kabuuang pinsala: P{v:.0f}B",
                       "ENG":"Total estimated damage: P{v:.0f}B"},
    "ty_storms"     :{"FIL":"Mga Bagyo:",              "ENG":"Storms:"},
    "ty_alloc_q"    :{"FIL":"Ilaan ang disaster relief budget:",
                       "ENG":"Allocate disaster relief budget:"},
    # Game over
    "go_reason_imp" :{"FIL":"TINANGGAL SA PWESTO -- Masyadong mababa ang suporta",
                       "ENG":"IMPEACHED -- Approval rating too low"},
    "go_reason_eco" :{"FIL":"PAGBAGSAK NG EKONOMIYA -- Lumampas sa P3T ang depisito",
                       "ENG":"ECONOMIC COLLAPSE -- Deficit exceeded P3T"},
    "go_appr"       :{"FIL":"Panghuling Suporta: {a:.1f}%",    "ENG":"Final Approval: {a:.1f}%"},
    "go_years"      :{"FIL":"Taon ng Serbisyo: {y}",           "ENG":"Years of Service: {y}"},
    # Victory titles
    "vic_s"  :{"FIL":"BAYANI NG BANSA -- Ang inyong pamumuno ay magiging modelo sa kasaysayan.",
                "ENG":"HERO OF THE NATION -- Your leadership will be a model for generations."},
    "vic_a"  :{"FIL":"MAHUSAY NA LIDER -- Ang Pilipinas ay umuunlad dahil sa inyong serbisyo.",
                "ENG":"EXCELLENT LEADER -- The Philippines thrived under your service."},
    "vic_b"  :{"FIL":"KATAMTAMANG PANGULO -- May magagandang nagawa, may kulang din.",
                "ENG":"DECENT PRESIDENT -- Some achievements, but much left undone."},
    "vic_c"  :{"FIL":"MAHINA ANG PAMUMUNO -- Ang bansa ay naghirap sa ilalim ng inyong pamumuno.",
                "ENG":"WEAK LEADERSHIP -- The country struggled under your governance."},
    "vic_f"  :{"FIL":"TRAYDOR SA SAMBAYANAN -- Ang kasaysayan ay hindi magpapatawad sa inyo.",
                "ENG":"BETRAYER OF THE PEOPLE -- History will not forgive you."},
    "vic_stats":{"FIL":"Panghuling Istatistika:","ENG":"Final Stats:"},
    "vic_sys":{"FIL":"Sistemang Pampulitika: {s}","ENG":"Political System: {s}"},
    "vic_yrs":{"FIL":"Taon ng Serbisyo: {y}","ENG":"Years served: {y}"},
    "vic_ty" :{"FIL":"Mga Bagyo: {n}","ENG":"Typhoons: {n}"},
    # Region popup keys (just translate the labels)
    "reg_gdp" :{"FIL":"GDP%","ENG":"GDP%"},
    "reg_ty"  :{"FIL":"Panganib sa Bagyo","ENG":"Typhoon Risk"},
    "reg_reb" :{"FIL":"Mga Rebelde","ENG":"Rebels"},
    "reg_inf" :{"FIL":"Imprastraktura","ENG":"Infra"},
    "reg_pov" :{"FIL":"Kahirapan%","ENG":"Poverty%"},
    # News ticker messages (shown at the bottom of main menu and in-game)
    "ticker_msgs"   :{"FIL":[
        "REPUBLIKA SIMULATOR -- Simulan ang inyong pamumuno...",
        "Ang administrasyon ay naglunsad ng bagong economic plan para sa mga magsasaka...",
        "Bagyo Egay ay lumakas -- Category 4. Signal 3 sa Visayas...",
        "Oposisyon ay nag-rally sa EDSA -- 600,000 ang dumalo...",
        "Inflation ay bumaba ng 0.3% ayon sa PSA ngayong buwan...",
        "Kongreso ay nagdebate ng panukalang batas sa health insurance...",
        "BSP ay nagpanatili ng interest rates -- ekonomista ay nagpapahayag ng pag-asa...",
    ], "ENG":[
        "REPUBLIKA SIMULATOR -- Your mandate awaits...",
        "The administration launches a new economic plan for farmers...",
        "Typhoon Egay intensifies -- Category 4. Signal 3 in Visayas...",
        "Opposition holds EDSA rally -- 600,000 attend...",
        "Inflation drops 0.3% according to this month's PSA report...",
        "Congress debates proposed health insurance reform bill...",
        "BSP holds interest rates -- economists express cautious optimism...",
    ]},
}

def T(key):
    """Return translated string for key using current LANG."""
    entry = STRINGS.get(key)
    if entry is None: return key
    return entry.get(LANG, entry.get("ENG", key))

def E_T(ev, field):
    """Return the right language version of an event string field.
    Events store _en variants; falls back to the base Tagalog field."""
    if LANG == "ENG":
        return ev.get(field+"_en", ev.get(field, ""))
    return ev.get(field, "")

def EC_T(choice):
    """Return translated label+desc for an event choice."""
    if LANG == "ENG":
        return choice.get("lbl_en", choice.get("lbl","")), choice.get("desc_en", choice.get("desc",""))
    return choice.get("lbl", ""), choice.get("desc", "")


POLITICAL_SYSTEMS = [
    ("Presidential Republic",       "Classic PH republic -- checks & balances",               (30,80,160)),
    ("Parliamentary System",        "PM accountable to legislature; +5 Trust +3 Eco",         (30,120,80)),
    ("Federal Republic",            "Strong regions; +8 Infra -5 Inequality",                 (120,80,30)),
    ("Benevolent Authoritarianism", "Strongman rule for good; -15 Corruption +10 Economy; strict press",  (100,55,160)),
    ("Authoritarian Dictatorship",  "Unchecked power; kleptocracy, crackdowns & personality cult",       (140,20,20)),
]
AUTH_SYSTEMS = {"Benevolent Authoritarianism","Authoritarian Dictatorship"}

# ── FONTS ────────────────────────────────────────────────────
F={}
def init_fonts():
    fn=None
    for name in ("Agency FB","AgencyFB","Arial","FreeSans"):
        try:
            tmp=pygame.font.SysFont(name,14)
            if tmp.size("M")[0]>0: fn=name; break
        except: pass
    if not fn: fn=pygame.font.get_default_font()
    F.update({
        "H":pygame.font.SysFont(fn,54,bold=True),
        "h1":pygame.font.SysFont(fn,30,bold=True),
        "h2":pygame.font.SysFont(fn,22,bold=True),
        "bd":pygame.font.SysFont(fn,17),
        "sm":pygame.font.SysFont(fn,13),
        "tk":pygame.font.SysFont(fn,15),
    })
    # Handwriting / script font for the splash quote -- try nicest first
    hw=None
    for name in ("Segoe Script","Brush Script MT","Freestyle Script",
                 "Comic Sans MS","URW Chancery L","Palatino Linotype",
                 "Georgia","Times New Roman","serif"):
        try:
            tmp=pygame.font.SysFont(name,18,italic=True)
            if tmp.size("M")[0]>0: hw=name; break
        except: pass
    if hw is None: hw=fn
    F["quote_lg"]=pygame.font.SysFont(hw,52,italic=True)
    F["quote_sm"]=pygame.font.SysFont(hw,26,italic=True)
    # Symbol font — tries fonts that have full Unicode coverage
    sym=None
    for sn in ("DejaVu Sans","FreeSans","Segoe UI","Arial Unicode MS",
               "Liberation Sans","Noto Sans","Verdana"):
        try:
            tmp=pygame.font.SysFont(sn,16)
            if tmp.size("+")[0]>0: sym=sn; break
        except: pass
    if sym is None: sym=fn
    F["sym14"]=pygame.font.SysFont(sym,14)
    F["sym16"]=pygame.font.SysFont(sym,16)
    F["sym18"]=pygame.font.SysFont(sym,18)

# ── HELPERS ──────────────────────────────────────────────────
def lerp(a,b,t): return a+(b-a)*t
def lc(a,b,t): return tuple(int(lerp(a[i],b[i],max(0,min(1,t)))) for i in range(3))
def clamp(v,lo=0,hi=100): return max(lo,min(hi,v))
def stat_col(v): return C_GRN if v>65 else C_YLW if v>35 else C_RL

def gbg(surf):
    """In-game background: Manila skyline with roads, buildings, and homes."""
    # City dawn/dusk sky -- amber-grey, NOT blue
    for y in range(H):
        t=y/H
        c=lc((38,28,22),(20,18,24),t)
        pygame.draw.line(surf,c,(0,y),(W,y))
    # Distant city glow (warm amber near horizon)
    for r in range(160,0,-10):
        alpha=max(0,40-r//5)
        ov=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(ov,(255,180,60,alpha),(r,r),r)
        surf.blit(ov,(W//2-r,H//2-r-60))
    # Distant city skyline haze (grey-brown, NOT purple)
    mts=[(0,340),(80,290),(160,310),(260,275),(360,300),(460,270),(560,285),(660,275),(710,310)]
    pygame.draw.polygon(surf,(45,40,38),mts+[(710,H),(0,H)])
    # Buildings (background -- grey silhouettes)
    rng=random.Random(77)
    for i in range(28):
        bx=rng.randint(0,W-30); bh=rng.randint(60,200); bw=rng.randint(20,55)
        by=H-bh-120
        c=(30+rng.randint(0,20),35+rng.randint(0,20),50+rng.randint(0,20))
        pygame.draw.rect(surf,c,(bx,by,bw,bh))
        # Windows
        for wy in range(by+8,by+bh-10,14):
            for wx in range(bx+6,bx+bw-6,12):
                wc=(220,200,80) if rng.random()>0.35 else (40,50,70)
                pygame.draw.rect(surf,wc,(wx,wy,8,9))
    # Roads
    pygame.draw.rect(surf,(40,40,40),(0,H-125,W,30))
    pygame.draw.rect(surf,(40,40,40),(0,H-80,W,20))
    for i in range(0,W,60):
        pygame.draw.rect(surf,(200,180,0),(i,H-112,35,6))
    # Homes row (closer)
    for i in range(12):
        hx=i*65+rng.randint(-5,5); hy=H-120; hw=52; hh=50
        pygame.draw.rect(surf,(80+rng.randint(0,30),50+rng.randint(0,20),40+rng.randint(0,20)),(hx,hy,hw,hh))
        roof=[(hx-4,hy),(hx+hw//2,hy-22),(hx+hw+4,hy)]
        pygame.draw.polygon(surf,(100,40,30),roof)
    # Dark overlay for readability
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,20,80)); surf.blit(ov,(0,0))


def gbg_menu(surf, t=0.0):
    """Menu background: bright Filipino sky, beach, mountains, clouds, boats.
    All geometry is scaled to the full 1280x720 surface."""
    # Sky gradient -- top 65% of screen
    sky_h = int(H * 0.65)
    for y in range(sky_h):
        frac = y / sky_h
        if frac < 0.55:
            c = lc((88, 170, 250), (255, 220, 110), frac / 0.55)
        else:
            c = lc((220, 240, 255), (165, 210, 245), (frac - 0.55) / 0.45)
        pygame.draw.line(surf, c, (0, y), (W, y))

    # Sun -- upper right quadrant
    sx, sy = int(W * 0.82), int(H * 0.18)
    for r in range(110, 0, -7):
        alpha = max(0, 85 - r)
        ov = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(ov, (255, 240, 100, alpha), (r, r), r)
        surf.blit(ov, (sx - r, sy - r))
    pygame.draw.circle(surf, (255, 250, 135), (sx, sy), 42)

    # Animated clouds -- across full width
    rng = random.Random(17)
    for i in range(10):
        cx = int((rng.randint(0, W) + t * 14 * rng.uniform(0.3, 1.1)) % W)
        cy = rng.randint(20, int(H * 0.30))
        cw = rng.randint(110, 230); ch = rng.randint(28, 56)
        alpha = int(200 + rng.randint(0, 45))
        cloud = pygame.Surface((cw + 60, ch + 28), pygame.SRCALPHA)
        for bx2, by2, br2 in [(24, ch//2, ch//2+12), (cw//2, 10, ch//2+16), (cw - 6, ch//2, ch//2+10)]:
            pygame.draw.circle(cloud, (255, 255, 255, alpha), (bx2, by2 + 14), br2)
        surf.blit(cloud, (cx - 28, cy - 14))

    # Far mountains -- y anchored at 55% of H, peaks to 38%
    mt_base = int(H * 0.60)
    mt_peak = int(H * 0.38)
    mpoly = [(0, mt_base),
             (80,  int(H*0.44)), (180, int(H*0.50)), (280, int(H*0.40)),
             (400, int(H*0.46)), (510, int(H*0.38)), (620, int(H*0.43)),
             (730, int(H*0.37)), (840, int(H*0.42)), (950, int(H*0.39)),
             (1060,int(H*0.44)), (1170,int(H*0.41)), (W,   int(H*0.45)),
             (W, H), (0, H)]
    pygame.draw.polygon(surf, (68, 92, 52), mpoly)

    # Mid green hills -- y from 65% down
    hill_top = int(H * 0.62)
    hpoly = [(0, int(H*0.70)),
             (110, int(H*0.63)), (230, int(H*0.67)), (350, int(H*0.61)),
             (470, int(H*0.65)), (590, int(H*0.60)), (710, int(H*0.64)),
             (830, int(H*0.61)), (950, int(H*0.66)), (1070,int(H*0.62)),
             (1190,int(H*0.67)), (W,   int(H*0.65)),
             (W, H), (0, H)]
    pygame.draw.polygon(surf, (52, 130, 46), hpoly)

    # Near grass bank -- 72% to bottom
    gpoly = [(0, int(H*0.74)),
             (200, int(H*0.72)), (400, int(H*0.73)), (600, int(H*0.71)),
             (800, int(H*0.73)), (1000,int(H*0.72)), (W,   int(H*0.73)),
             (W, H), (0, H)]
    pygame.draw.polygon(surf, (46, 112, 38), gpoly)

    # Beach sand -- 76% to bottom
    sand_y = int(H * 0.76)
    pygame.draw.polygon(surf, (220, 200, 140), [(0, sand_y), (W, sand_y), (W, H), (0, H)])

    # Ocean -- 78% to bottom, full width
    ocean_y = int(H * 0.78)
    for y in range(ocean_y, H):
        frac = (y - ocean_y) / max(1, H - ocean_y)
        c = lc((50, 148, 220), (14, 75, 158), frac)
        pygame.draw.line(surf, c, (0, y), (W, y))

    # Ocean shimmer lines
    for i in range(12):
        wx = int((i * 110 + t * 30) % W)
        wy = ocean_y + 18 + int(math.sin(t * 1.6 + i) * 6) + i * 10
        if wy >= H: continue
        sw_ = min(90, W - wx)
        if sw_ > 4:
            ov2 = pygame.Surface((sw_, 8), pygame.SRCALPHA)
            ov2.fill((130, 200, 245, 110))
            surf.blit(ov2, (wx, wy))

    # Boats -- spread across full width, at ocean level
    boat_y = int(H * 0.80)
    for i, bx_frac in enumerate([0.10, 0.35, 0.62, 0.85]):
        bx = int(bx_frac * W + math.sin(t * 0.65 + i * 1.8) * 16)
        by = boat_y + i * 6
        if by + 16 > H: continue
        pygame.draw.polygon(surf, (88, 52, 26),
            [(bx-18, by+6), (bx+18, by+6), (bx+12, by+15), (bx-12, by+15)])
        pygame.draw.line(surf, (62, 40, 16), (bx, by+5), (bx, by-24), 2)
        sail_col = [(215, 40, 40), (235, 235, 235), (255, 195, 40), (160, 215, 85)][i]
        pygame.draw.polygon(surf, sail_col, [(bx, by-24), (bx, by+3), (bx+20, by-1)])

    # Palm trees -- four across full width, rooted at grass level
    palm_y = int(H * 0.72)
    for px_, py_ in [(75, palm_y), (420, palm_y), (810, palm_y), (1200, palm_y)]:
        if px_ >= W: continue
        # Trunk (curved upward)
        trunk_pts = [(px_, py_), (px_+3, py_-22), (px_+7, py_-44), (px_+10, py_-62)]
        for j in range(len(trunk_pts)-1):
            pygame.draw.line(surf, (88, 62, 28), trunk_pts[j], trunk_pts[j+1], 5-j)
        tip = trunk_pts[-1]
        # Fronds
        for j in range(7):
            a = math.pi * j / 3.5 - math.pi / 2 + 0.3
            ex = tip[0] + int(math.cos(a) * 48)
            ey = tip[1] + int(math.sin(a) * 26)
            ex = max(0, min(W-1, ex)); ey = max(0, min(H-1, ey))
            pygame.draw.line(surf, (36, 148, 38), tip, (ex, ey), 3)

def wrap(txt,font,mw):
    words=txt.split(); lines=[]; ln=""
    for w in words:
        t=(ln+" "+w).strip()
        if font.size(t)[0]<=mw: ln=t
        else:
            if ln: lines.append(ln)
            ln=w
    if ln: lines.append(ln)
    return lines

def blit_c(surf,txt,font,col,cy,shad=False):
    if shad:
        s=font.render(txt,True,C_BLK); surf.blit(s,(W//2-s.get_width()//2+2,cy+2))
    s=font.render(txt,True,col); surf.blit(s,(W//2-s.get_width()//2,cy))

# Global ref for loaded star surface (set in main after pygame.init)
_PH_STAR_SURF = None

def draw_sun(surf,cx,cy,r=34):
    """Draw Philippine sun — uses loaded PNG if available, else draws procedurally.
    Each of the 8 primary rays fans out into 3 sub-rays (matching the flag exactly)."""
    global _PH_STAR_SURF
    d = r*2 + int(r*1.9)   # total diameter including rays
    if _PH_STAR_SURF is not None:
        try:
            scaled = pygame.transform.smoothscale(_PH_STAR_SURF, (d, d))
            surf.blit(scaled, (cx - d//2, cy - d//2))
            return
        except Exception:
            pass
    # --- Procedural fallback: accurate 8-primary-ray sun ---
    pygame.draw.circle(surf, C_GOLD, (cx, cy), r)
    for i in range(8):
        a_primary = math.pi*2*i/8 - math.pi/2
        # Each primary ray: 1 central pointed ray + 2 flanking thinner rays
        for sub, da, ray_len, base_half in [
            (0,  0.00, r*1.05, 0.12),   # central — longer
            (1,  0.19, r*0.78, 0.07),   # left flank
            (2, -0.19, r*0.78, 0.07),   # right flank
        ]:
            a = a_primary + da
            inner = r + 2
            outer = cx + int(math.cos(a)*(r + ray_len)), cy + int(math.sin(a)*(r + ray_len))
            p1 = (cx+int(math.cos(a+base_half)*inner), cy+int(math.sin(a+base_half)*inner))
            p2 = (cx+int(math.cos(a-base_half)*inner), cy+int(math.sin(a-base_half)*inner))
            pygame.draw.polygon(surf, C_GOLD, [p1, p2, outer])

def draw_bar(surf,x,y,w,h,val,lbl="",invert=False):
    pygame.draw.rect(surf,(18,32,56),(x,y,w,h),border_radius=3)
    fw=int(w*clamp(val)/100)
    col=stat_col(100-val) if invert else stat_col(val)
    if fw>0: pygame.draw.rect(surf,col,(x,y,fw,h),border_radius=3)
    pygame.draw.rect(surf,C_GD,(x,y,w,h),1,border_radius=3)
    if lbl:
        s=F["sm"].render(lbl,True,C_WHT)
        surf.blit(s,(x-s.get_width()-5,y+h//2-s.get_height()//2))
    vs=F["sm"].render(f"{val:.0f}%",True,col)
    surf.blit(vs,(x+w+4,y+h//2-vs.get_height()//2))

# ── SHAPE-DRAWN ICON SYSTEM ──────────────────────────────────
# Draws small recognisable symbols using pygame.draw primitives.
# This avoids all font/emoji rendering issues across all platforms.
def draw_icon(surf, name, x, y, size=14, col=None):
    """Draw a small icon at (x,y) using pygame shapes. No font needed."""
    if col is None: col = C_GOLD
    s = size
    h = s // 2
    cx, cy = x + h, y + h   # centre

    if name in ("check", "tick", "+ok"):
        # Checkmark
        pygame.draw.line(surf,col,(x+2,cy),(x+h-2,y+s-3),2)
        pygame.draw.line(surf,col,(x+h-2,y+s-3),(x+s-2,y+3),2)
    elif name in ("cross", "x", "-no"):
        pygame.draw.line(surf,col,(x+2,y+2),(x+s-2,y+s-2),2)
        pygame.draw.line(surf,col,(x+s-2,y+2),(x+2,y+s-2),2)
    elif name in ("warn", "!"):
        # Triangle warning
        pygame.draw.polygon(surf,col,[(cx,y+1),(x+s-1,y+s-1),(x+1,y+s-1)],2)
        pygame.draw.line(surf,col,(cx,y+4),(cx,y+s-6),2)
        pygame.draw.circle(surf,col,(cx,y+s-4),1)
    elif name in ("save", "disk"):
        pygame.draw.rect(surf,col,(x+1,y+1,s-2,s-2),1)
        pygame.draw.rect(surf,col,(x+3,y+1,s-6,4))
        pygame.draw.rect(surf,col,(x+3,y+s-5,s-6,4),1)
    elif name in ("home",):
        pygame.draw.polygon(surf,col,[(cx,y+2),(x+s-1,y+h+1),(x+1,y+h+1)])
        pygame.draw.rect(surf,col,(x+3,y+h+1,s-6,h-1),1)
    elif name in ("lang", "globe"):
        pygame.draw.circle(surf,col,(cx,cy),h-1,1)
        pygame.draw.line(surf,col,(x+1,cy),(x+s-1,cy),1)
        pygame.draw.ellipse(surf,col,(x+3,y+2,s-6,s-4),1)
    elif name in ("del", "trash"):
        pygame.draw.rect(surf,col,(x+2,y+3,s-4,s-4),1)
        pygame.draw.line(surf,col,(x+1,y+3),(x+s-1,y+3),1)
        pygame.draw.line(surf,col,(x+h-1,y+1),(x+h+1,y+1),2)
        for i in range(3):
            pygame.draw.line(surf,col,(x+4+i*3,y+5),(x+4+i*3,y+s-2),1)
    elif name in ("up", "arrow_up"):
        pygame.draw.polygon(surf,col,[(cx,y+2),(x+s-2,y+s-2),(x+2,y+s-2)])
    elif name in ("down", "arrow_down"):
        pygame.draw.polygon(surf,col,[(cx,y+s-2),(x+s-2,y+2),(x+2,y+2)])
    elif name in ("research", "flask"):
        pygame.draw.line(surf,col,(x+4,y+2),(x+4,y+h),2)
        pygame.draw.line(surf,col,(x+s-4,y+2),(x+s-4,y+h),2)
        pygame.draw.polygon(surf,col,[(x+2,y+h),(cx,y+s-2),(x+s-2,y+h)],1)
    elif name in ("star",):
        pts=[]
        for i in range(5):
            a=math.pi*2*i/5-math.pi/2
            pts.append((cx+int(math.cos(a)*(h-1)),cy+int(math.sin(a)*(h-1))))
            a2=math.pi*2*i/5+math.pi/5-math.pi/2
            pts.append((cx+int(math.cos(a2)*(h//2)),cy+int(math.sin(a2)*(h//2))))
        pygame.draw.polygon(surf,col,pts)
    elif name in ("shield",):
        pygame.draw.polygon(surf,col,[(cx,y+s-1),(x+1,y+4),(x+s-1,y+4)],1)
        pygame.draw.line(surf,col,(x+1,y+4),(x+1,y+h),1)
        pygame.draw.line(surf,col,(x+s-1,y+4),(x+s-1,y+h),1)
    elif name in ("lock",):
        pygame.draw.rect(surf,col,(x+2,y+h-1,s-4,h),1)
        pygame.draw.arc(surf,col,pygame.Rect(x+3,y+1,s-6,h),0,math.pi,2)
    elif name in ("rocket",):
        pygame.draw.polygon(surf,col,[(cx,y+1),(x+s-2,y+s-3),(x+2,y+s-3)])
        pygame.draw.rect(surf,col,(cx-2,y+s-4,4,3))
    elif name in ("satellite",):
        pygame.draw.circle(surf,col,(cx,cy),3,1)
        pygame.draw.line(surf,col,(x+1,cy),(x+s-1,cy),1)
        pygame.draw.rect(surf,col,(x+1,y+3,5,s-6),1)
        pygame.draw.rect(surf,col,(x+s-6,y+3,5,s-6),1)
    elif name in ("news",):
        pygame.draw.rect(surf,col,(x+1,y+2,s-2,s-4),1)
        for i in range(3):
            pygame.draw.line(surf,col,(x+3,y+5+i*4),(x+s-3,y+5+i*4),1)
    elif name in ("award", "trophy"):
        pygame.draw.arc(surf,col,pygame.Rect(x+2,y+1,s-4,h+2),0,math.pi,2)
        pygame.draw.line(surf,col,(cx,y+h+2),(cx,y+s-3),2)
        pygame.draw.line(surf,col,(x+3,y+s-2),(x+s-3,y+s-2),2)
    elif name in ("money", "coin"):
        pygame.draw.circle(surf,col,(cx,cy),h-1,1)
        pygame.draw.line(surf,col,(cx,y+3),(cx,y+s-3),1)
    elif name in ("flag_ph",):
        pygame.draw.rect(surf,col,(x+1,y+2,s-2,h-2))
        pygame.draw.rect(surf,(255,255,255),(x+1,y+h,s-2,h-2))
        pygame.draw.circle(surf,(255,215,0),(x+4,cy),3)
    else:
        # Fallback: small filled circle
        pygame.draw.circle(surf,col,(cx,cy),h-2)

def txt_with_icon(surf, icon_name, text, font, col, x, y, icon_col=None, icon_size=14):
    """Draw a shape icon then text beside it."""
    draw_icon(surf, icon_name, x, y + max(0,(font.get_height()-icon_size)//2), icon_size, icon_col or col)
    s = font.render(text, True, col)
    surf.blit(s, (x + icon_size + 3, y))


def sym_render(txt, size=16, col=None):
    """Render text using the symbol-capable font."""
    fkey = f"sym{size}" if f"sym{size}" in F else "sym16"
    return F.get(fkey, F["bd"]).render(txt, True, col or C_WHT)

def blit_sym(surf, txt, size=16, col=None, x=0, y=0):
    s = sym_render(txt, size, col)
    surf.blit(s, (x, y))
    return s.get_width()

def fade_surf(surf,alpha):
    ov=pygame.Surface((W,H)); ov.set_alpha(alpha); ov.fill(C_BLK); surf.blit(ov,(0,0))

def remap_ev(ev, sw, sh):
    """Re-map mouse-position fields from real window pixels >> internal W×H pixels.
    Must be called on every event before any hit-testing."""
    if sw==W and sh==H: return ev   # no scaling needed
    sx, sy = W/sw, H/sh
    if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        sp=(int(ev.pos[0]*sx), int(ev.pos[1]*sy))
        return pygame.event.Event(ev.type, pos=sp, button=ev.button)
    if ev.type == pygame.MOUSEMOTION:
        sp=(int(ev.pos[0]*sx), int(ev.pos[1]*sy))
        return pygame.event.Event(ev.type, pos=sp, rel=ev.rel, buttons=ev.buttons)
    return ev

# ── SAVE MANAGER ─────────────────────────────────────────────
def _save_dir():
    """Return the directory where save files are stored.
    Works whether the script is run with python file.py, python3 -c, frozen exe, etc."""
    try:
        p = os.path.abspath(sys.argv[0])
        d = os.path.dirname(p)
        if os.path.isdir(d):
            return d
    except Exception:
        pass
    return os.getcwd()

class SaveManager:
    @staticmethod
    def path(slot): return os.path.join(_save_dir(), SAVES[slot])
    @staticmethod
    def save(slot,data):
        data["_ts"]=time.strftime("%Y-%m-%d %H:%M")
        try:
            with open(SaveManager.path(slot),"w") as f: json.dump(data,f,indent=2)
        except OSError as e:
            print(f"[SaveManager] Could not save slot {slot}: {e}")
    @staticmethod
    def load(slot):
        p=SaveManager.path(slot)
        try:
            return json.load(open(p)) if os.path.exists(p) else None
        except (OSError, json.JSONDecodeError):
            return None

# ── GAME STATE ───────────────────────────────────────────────
@dataclass
class GS:
    player_name:str="Presidente"; foreign_stance:str="SOBERANIYA"
    difficulty:str="SENADOR"; political_system:str="Presidential Republic"
    year:int=2025; month:int=1; term:int=1
    budget:float=5000.0; debt:float=500.0
    # Economic indicators (real-world style)
    gdp:float=20000.0        # P billions
    gdp_growth:float=5.8     # % YoY
    unemployment:float=5.2   # %
    inflation:float=4.1      # %
    poverty_rate:float=18.1  # %
    # Core 0-100 stats
    economy:float=50.0; military:float=50.0; public_trust:float=50.0
    corruption:float=40.0; inequality:float=55.0; infrastructure:float=45.0
    health:float=50.0; education:float=50.0; sovereignty:float=50.0
    press_freedom:float=68.0; auth_power:float=0.0
    # Research
    research_points:float=0.0; research_tier:int=0
    research_unlocked:list=field(default_factory=list)
    political_shows_done:list=field(default_factory=list)
    interview_history:list=field(default_factory=list)
    dictator_age:int=0        # years as dictator (triggers old-age event after 15+)
    approval_rating:float=50.0; approval_history:list=field(default_factory=list)
    gdp_history:list=field(default_factory=list)
    consecutive_low:int=0
    rel_us:float=50.0; rel_china:float=50.0; rel_asean:float=58.0; rel_un:float=55.0
    active_policies:list=field(default_factory=list)
    typhoon_history:list=field(default_factory=list)
    event_log:list=field(default_factory=list)
    flags:dict=field(default_factory=dict)
    budget_alloc:dict=field(default_factory=lambda:{
        "health":15,"education":15,"military":12,"infrastructure":20,
        "disaster_relief":8,"social_services":15,"debt_repayment":15})
    disaster_relief_budget:float=250.0
    # Per-island dynamic stats -- updated by compute_regional_stats()
    region_infra:dict=field(default_factory=lambda:{
        "Luzon":72,"NCR":80,"Visayas":55,"Mindanao":44,"Palawan":39})
    region_poverty:dict=field(default_factory=lambda:{
        "Luzon":18.0,"NCR":13.0,"Visayas":32.0,"Mindanao":38.0,"Palawan":28.0})
    region_rebel:dict=field(default_factory=lambda:{
        "Luzon":8,"NCR":2,"Visayas":12,"Mindanao":55,"Palawan":10})


    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls,d):
        gs=cls()
        for k,v in d.items():
            if hasattr(gs,k): setattr(gs,k,v)
        return gs

    def update_economic_indicators(self):
        """Recompute derived stats AND grow GDP — called only from _advance()."""
        self.gdp_growth = round(clamp((self.economy-30)*0.18+2.0,-4,14),1)
        self.gdp = max(5000, self.gdp*(1+self.gdp_growth/100/12))  # monthly compounding
        self.unemployment = round(clamp(20-self.economy*0.18,2,30),1)
        self.inflation = round(clamp(2+(self.corruption*0.06)+(50-self.economy)*0.04,0.5,22),1)
        self.poverty_rate = round(clamp(5+self.inequality*0.35-(self.economy-30)*0.1,2,60),1)

    def recompute_stats_only(self):
        """Recompute stats WITHOUT growing GDP — safe to call every frame."""
        self.gdp_growth = round(clamp((self.economy-30)*0.18+2.0,-4,14),1)
        self.unemployment = round(clamp(20-self.economy*0.18,2,30),1)
        self.inflation = round(clamp(2+(self.corruption*0.06)+(50-self.economy)*0.04,0.5,22),1)
        self.poverty_rate = round(clamp(5+self.inequality*0.35-(self.economy-30)*0.1,2,60),1)

    def compute_regional_stats(self):
        """Update per-island stats based on national decisions each month."""
        # Infrastructure flows to all islands proportional to spending
        infra_delta = (self.infrastructure - 45) * 0.05
        for k in self.region_infra:
            base = {"Luzon":72,"NCR":80,"Visayas":55,"Mindanao":44,"Palawan":39}[k]
            # NCR benefits most from economy, Mindanao from military stability
            bonus = {"Luzon":infra_delta,"NCR":infra_delta*1.4,"Visayas":infra_delta*0.9,
                     "Mindanao":infra_delta*0.7+(self.military-50)*0.03,"Palawan":infra_delta*0.5}[k]
            self.region_infra[k] = round(clamp(base + (self.infrastructure-45)*0.3 + bonus*0.4, 0, 100))
        # Poverty follows inequality + economy
        pov_delta = (self.inequality - 50)*0.15 - (self.economy - 50)*0.08
        for k in self.region_poverty:
            base = {"Luzon":18.0,"NCR":13.0,"Visayas":32.0,"Mindanao":38.0,"Palawan":28.0}[k]
            self.region_poverty[k] = round(clamp(base + pov_delta*{"Luzon":0.8,"NCR":0.6,"Visayas":1.1,"Mindanao":1.2,"Palawan":1.0}[k], 1, 70), 1)
        # Rebel activity inversely tied to military + trust in Mindanao
        mindanao_peace = (self.military - 50)*0.2 + (self.public_trust - 50)*0.1
        self.region_rebel["Mindanao"] = max(5, min(95, 55 - mindanao_peace))
        self.region_rebel["Visayas"] = max(3, min(60, 12 - (self.public_trust-50)*0.08))
        self.region_rebel["Luzon"] = max(2, min(40, 8 - (self.corruption<30)*5))

    def apply_bonuses(self):
        s=self.foreign_stance
        if s=="SOBERANIYA": self.sovereignty+=10; self.public_trust+=5
        elif s=="ALYANSA": self.military+=15; self.economy+=10; self.rel_china-=10
        elif s=="PAKIKIPAG-UGNAYAN": self.infrastructure+=20; self.rel_china+=10; self.sovereignty-=15; self.rel_us-=10
        elif s=="BALANSE": self.rel_us+=5; self.rel_china+=5; self.rel_asean+=5; self.rel_un+=5
        SB={
            "Parliamentary System":{"public_trust":5,"economy":3},
            "Federal Republic":{"infrastructure":8,"inequality":-5},
            "Benevolent Authoritarianism":{"corruption":-25,"economy":12,"public_trust":-4},
            "Authoritarian Dictatorship":{"corruption":20,"inequality":10,"press_freedom":-20,"auth_power":30},
        }
        for stat,d in SB.get(self.political_system,{}).items():
            setattr(self,stat,getattr(self,stat)+d)
        self.clamp()

    def clamp(self):
        for s in ["economy","military","public_trust","corruption","inequality",
                  "infrastructure","health","education","sovereignty","press_freedom",
                  "auth_power","approval_rating","rel_us","rel_china","rel_asean","rel_un"]:
            setattr(self,s,clamp(getattr(self,s)))

    def compute_approval(self):
        b=(self.economy*0.25+self.public_trust*0.22+self.health*0.15
           +(100-self.inequality)*0.15+self.education*0.10
           +self.infrastructure*0.08+self.sovereignty*0.05)
        if self.corruption>70: b-=(self.corruption-70)*0.45
        # Base approval penalty so even good govts have to work harder
        b = b * 0.92
        if self.political_system=="Benevolent Authoritarianism": b=b*0.85+self.economy*0.15
        elif self.political_system=="Authoritarian Dictatorship": b-=15+self.auth_power*0.2
        self.approval_rating=clamp(b)
        self.approval_history.append(round(self.approval_rating,1))
        if len(self.approval_history)>24: self.approval_history=self.approval_history[-24:]
        self.gdp_history.append(round(self.gdp/1000,2))
        if len(self.gdp_history)>24: self.gdp_history=self.gdp_history[-24:]

    def log(self,txt):
        self.event_log.insert(0,f"[{self.year} M{self.month:02d}] {txt}")
        if len(self.event_log)>50: self.event_log=self.event_log[:50]

# ── EVENT POOL ───────────────────────────────────────────────
EVENTS=[
 # CORRUPTION
 {"id":"cc1","cat":"CORRUPTION",
  "title":"KALIHIM SA ISKANDALO","title_en":"CABINET OFFICIAL SCANDAL",
  "flavor":"Si Kalihim Magsalang ay nahuli habang tumatanggap ng malaking suhol mula sa mga kontratista. Viral na ang video.",
  "flavor_en":"Cabinet Secretary Magsalang was caught accepting large bribes from government contractors. The video has gone viral.",
  "choices":[{"lbl":"Usigin sa korte","lbl_en":"Prosecute in court","fx":{"public_trust":8,"corruption":-12},"desc":"","desc_en":""},
             {"lbl":"Takpan -- mapanganib","lbl_en":"Cover it up (risky)","fx":{"corruption":14,"public_trust":-8},"desc":"","desc_en":""},
             {"lbl":"Independyenteng komisyon","lbl_en":"Independent commission","fx":{"public_trust":4,"corruption":-5},"desc":"","desc_en":""},
             {"lbl":"Palayasin + pensiyon","lbl_en":"Dismiss with pension","fx":{"public_trust":-10,"corruption":6},"desc":"","desc_en":""}]},
 {"id":"cc2","cat":"CORRUPTION",
  "title":"ROTTENPOLISYA SA METRO","title_en":"POLICE CORRUPTION IN METRO",
  "flavor":"Malawakang pangingikil ng mga pulis sa Metro Manila. Daan-daang reklamo ang natanggap ng ombudsman.",
  "flavor_en":"Widespread police extortion across Metro Manila. Hundreds of complaints filed with the ombudsman.",
  "choices":[{"lbl":"I-reporma ang PNP","lbl_en":"Reform the police force","fx":{"corruption":-10,"public_trust":6,"military":-4},"desc":"","desc_en":""},
             {"lbl":"Suportahan ang pulis","lbl_en":"Back the police","fx":{"military":5,"corruption":6,"public_trust":-7},"desc":"","desc_en":""},
             {"lbl":"Mag-imbestigahan","lbl_en":"Investigate","fx":{"corruption":-4,"public_trust":3},"desc":"","desc_en":""}]},
 {"id":"cc3","cat":"CORRUPTION",
  "title":"MAYOR NA MAGNANAKAW","title_en":"MAYOR EMBEZZLES FUNDS",
  "flavor":"Isang mayor sa Visayas ay nahuli ng COA na nag-redirect ng calamity funds para sa personal na negosyo.",
  "flavor_en":"A Visayas mayor was caught by state auditors redirecting calamity funds to personal business ventures.",
  "choices":[{"lbl":"I-suspinde at usigin","lbl_en":"Suspend and prosecute","fx":{"corruption":-8,"public_trust":7},"desc":"","desc_en":""},
             {"lbl":"Local autonomy lang","lbl_en":"Respect local autonomy","fx":{"corruption":10,"public_trust":-6},"desc":"","desc_en":""},
             {"lbl":"Audit at babala","lbl_en":"Audit and warn","fx":{"corruption":-4,"public_trust":3},"desc":"","desc_en":""}]},
 # WPS
 {"id":"wps1","cat":"WPS",
  "title":"DAYUHANG BARKO SA EEZ","title_en":"FOREIGN VESSELS IN EEZ",
  "flavor":"47 barkong dayuhan ang natuklasan sa Recto Bank. Ang mga mangingisda ay natatakot nang umalis.",
  "flavor_en":"47 foreign vessels detected at Recto Bank. Local fishermen are being forced to leave the area.",
  "choices":[{"lbl":"Diplomatic protest","lbl_en":"File diplomatic protest","fx":{"sovereignty":8,"rel_china":-5},"desc":"","desc_en":""},
             {"lbl":"I-deploy ang Coast Guard","lbl_en":"Deploy Coast Guard","fx":{"military":6,"sovereignty":5,"rel_china":-8},"desc":"","desc_en":""},
             {"lbl":"Huwag pansinin","lbl_en":"Ignore the incident","fx":{"sovereignty":-12,"public_trust":-5,"rel_china":5},"desc":"","desc_en":""},
             {"lbl":"Humingi ng US support","lbl_en":"Request US support","fx":{"military":8,"rel_us":5,"rel_china":-12},"desc":"","desc_en":""}]},
 {"id":"wps2","cat":"WPS",
  "title":"WATER CANNON ATAKE","title_en":"WATER CANNON ATTACK",
  "flavor":"Isang PCG vessel ang tinanggihan ng dayuhang water cannon. Ang footage ay viral internationally.",
  "flavor_en":"A Philippine Coast Guard vessel was struck by foreign water cannons. Footage is spreading internationally.",
  "choices":[{"lbl":"ICC arbitration","lbl_en":"File ICC arbitration case","fx":{"sovereignty":10,"rel_un":6,"rel_china":-10},"desc":"","desc_en":""},
             {"lbl":"Retaliatory patrol","lbl_en":"Launch retaliatory patrol","fx":{"military":8,"sovereignty":6,"rel_china":-15},"desc":"","desc_en":""},
             {"lbl":"Quiet diplomacy","lbl_en":"Pursue quiet diplomacy","fx":{"rel_china":4,"sovereignty":-7},"desc":"","desc_en":""},
             {"lbl":"EDCA activation","lbl_en":"Invoke EDCA with US","fx":{"military":10,"rel_us":8,"rel_china":-18},"desc":"","desc_en":""}]},
 {"id":"wps3","cat":"WPS",
  "title":"ARTIFICIAL ISLAND CONSTRUCTION","title_en":"ARTIFICIAL ISLAND BUILT",
  "flavor":"Satellite images ay nagpapakita ng bagong istruktura sa isang reef sa loob ng ating EEZ.",
  "flavor_en":"Satellite images reveal new structures built on a reef inside Philippine-claimed waters.",
  "choices":[{"lbl":"UN formal complaint","lbl_en":"File UN formal complaint","fx":{"rel_un":6,"sovereignty":7,"rel_china":-8},"desc":"","desc_en":""},
             {"lbl":"Naval visibility ops","lbl_en":"Naval visibility operations","fx":{"military":5,"sovereignty":5,"rel_china":-10},"desc":"","desc_en":""},
             {"lbl":"Bilateral talks","lbl_en":"Open bilateral talks","fx":{"rel_china":3,"sovereignty":-4},"desc":"","desc_en":""}]},
 # INEQUALITY
 {"id":"ineq1","cat":"INEQUALITY",
  "title":"DEMOLISYON NA MAY RELOKASYON","title_en":"DEMOLITION WITH RELOCATION",
  "flavor":"Plano ng lungsod ang limpyahin ang mga informal settler -- kasama ang housing units, livelihood training, at trabaho para sa bawat pamilya.",
  "flavor_en":"The city plans to clear informal settlements -- with housing units, livelihood training and jobs for every family. UN-Habitat has praised the programme.",
  "choices":[{"lbl":"Ituloy (buong pakete)","lbl_en":"Proceed (full package)","fx":{"infrastructure":8,"inequality":-8,"public_trust":6,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Palawakin -- mas maraming bahay","lbl_en":"Expand -- build more homes","fx":{"infrastructure":5,"inequality":-14,"public_trust":10,"budget":-220},"desc":"","desc_en":""},
             {"lbl":"Kanselahin","lbl_en":"Cancel the project","fx":{"infrastructure":-2,"public_trust":4},"desc":"","desc_en":""}]},
 {"id":"ineq2","cat":"INEQUALITY",
  "title":"DEMOLISYON -- WALANG RELOKASYON","title_en":"DEMOLITION -- NO RELOCATION",
  "flavor":"Pinaplano ang demolisyon ng squatter areas NANG WALANG IBINIBIGAY NA RELOKASYON. Daan-daang pamilya ang nasa kalsada. Malakas ang protesta.",
  "flavor_en":"Demolition of informal settlements is planned WITHOUT any relocation package. Hundreds of families are on the streets. Protests are growing.",
  "choices":[{"lbl":"Ituloy (pabayaan sila)","lbl_en":"Proceed anyway","fx":{"infrastructure":5,"public_trust":-18,"inequality":10},"desc":"","desc_en":""},
             {"lbl":"I-hinto + dagdag relokasyon","lbl_en":"Halt + add relocation","fx":{"infrastructure":3,"public_trust":6,"inequality":-6,"budget":-100},"desc":"","desc_en":""},
             {"lbl":"Kanselahin ang demolisyon","lbl_en":"Cancel demolition","fx":{"public_trust":9,"infrastructure":-3},"desc":"","desc_en":""}]},
 {"id":"ineq3","cat":"INEQUALITY",
  "title":"LUPA PARA SA MAGSASAKA","title_en":"LAND REFORM DEMAND",
  "flavor":"Libu-libong magsasaka sa Negros ang nagrereklamo dahil sa malalaking hacienda na hindi pa napi-proseso ng CARP.",
  "flavor_en":"Thousands of Negros farmers demand action on large haciendas still unprocessed under land reform.",
  "choices":[{"lbl":"Palakasin ang CARP","lbl_en":"Strengthen land reform","fx":{"inequality":-12,"public_trust":9,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Protektahan ang may-ari","lbl_en":"Protect landowners","fx":{"economy":5,"inequality":6,"public_trust":-7},"desc":"","desc_en":""},
             {"lbl":"Mediation committee","lbl_en":"Form mediation panel","fx":{"inequality":-5,"public_trust":3},"desc":"","desc_en":""}]},
 {"id":"ineq4","cat":"INEQUALITY",
  "title":"GUTOM SA PROBINSYA","title_en":"PROVINCIAL HUNGER CRISIS",
  "flavor":"Malnutrition crisis sa Eastern Visayas -- malayo sa food supply at walang sapat na kabuhayan.",
  "flavor_en":"Malnutrition crisis hits Eastern Visayas -- remote areas cut off from food supply and livelihood.",
  "choices":[{"lbl":"Emergency food aid","lbl_en":"Emergency food aid","fx":{"health":7,"inequality":-5,"public_trust":6,"budget":-80},"desc":"","desc_en":""},
             {"lbl":"WFP assistance","lbl_en":"Request WFP assistance","fx":{"health":8,"sovereignty":-3,"rel_un":5},"desc":"","desc_en":""},
             {"lbl":"Huwag pansinin","lbl_en":"Do nothing","fx":{"health":-10,"public_trust":-8,"inequality":5},"desc":"","desc_en":""}]},
 # ECONOMY
 {"id":"eco1","cat":"ECONOMY",
  "title":"MATAAS NA IMPLASYON","title_en":"HIGH INFLATION CRISIS",
  "flavor":"Implasyon ay pumalo sa 9.2% -- pinakamataas sa 14 taon. Presyo ng bigas ay tumaas ng 40%.",
  "flavor_en":"Inflation hits 9.2% -- a 14-year high. Rice prices have surged 40% in three months.",
  "choices":[{"lbl":"IMF loan","lbl_en":"Take IMF loan","fx":{"budget":500,"sovereignty":-9,"economy":5,"debt":300},"desc":"","desc_en":""},
             {"lbl":"Austerity measures","lbl_en":"Impose austerity","fx":{"economy":4,"public_trust":-10,"inequality":4},"desc":"","desc_en":""},
             {"lbl":"Price controls","lbl_en":"Impose price controls","fx":{"public_trust":5,"economy":-5},"desc":"","desc_en":""},
             {"lbl":"Mag-print ng pera","lbl_en":"Print money","fx":{"economy":3,"public_trust":3,"budget":150},"desc":"","desc_en":""}]},
 {"id":"eco2","cat":"ECONOMY",
  "title":"SEMICONDUCTOR INVESTMENT","title_en":"SEMICONDUCTOR INVESTMENT",
  "flavor":"Isang dayuhang tech firm ay nag-aalok ng P200B investment sa semiconductor fab -- may kondisyon: tax holiday.",
  "flavor_en":"A foreign tech firm offers P200B investment in a semiconductor fab -- condition: a full tax holiday.",
  "choices":[{"lbl":"Tanggapin lahat","lbl_en":"Accept all terms","fx":{"economy":14,"sovereignty":-6,"budget":200},"desc":"","desc_en":""},
             {"lbl":"Makipagnegosasyon","lbl_en":"Negotiate better terms","fx":{"economy":9,"sovereignty":2,"budget":100},"desc":"","desc_en":""},
             {"lbl":"Tanggihan","lbl_en":"Decline offer","fx":{"sovereignty":6,"economy":-3},"desc":"","desc_en":""}]},
 {"id":"eco3","cat":"ECONOMY",
  "title":"OFW KRISIS","title_en":"OVERSEAS WORKER CRISIS",
  "flavor":"Rekord na $40B remittances -- ngunit 3 OFW ang na-abuse sa Middle East at hindi tinutulungan ng embahada.",
  "flavor_en":"Record $40B in remittances -- but 3 OFWs were abused in the Middle East with no embassy assistance.",
  "choices":[{"lbl":"Protektahan ang OFW","lbl_en":"Protect OFWs abroad","fx":{"public_trust":8,"economy":3,"rel_un":3},"desc":"","desc_en":""},
             {"lbl":"Prayoridad: ekonomiya","lbl_en":"Prioritise the economy","fx":{"economy":9,"public_trust":-4},"desc":"","desc_en":""},
             {"lbl":"Bagong OFW hotline","lbl_en":"Launch OFW hotline","fx":{"public_trust":5,"economy":2,"budget":-30},"desc":"","desc_en":""}]},
 {"id":"eco4","cat":"ECONOMY",
  "title":"BUMAGSAK ANG PISO","title_en":"PESO COLLAPSES",
  "flavor":"Ang Philippine Peso ay bumaba ng 18% laban sa USD. Importasyon ay napakamahal na ngayon.",
  "flavor_en":"The Philippine Peso has fallen 18% against the US dollar. Imports have become critically expensive.",
  "choices":[{"lbl":"BSP intervention","lbl_en":"BSP market intervention","fx":{"economy":5,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Bayad utang agad","lbl_en":"Accelerate debt repayment","fx":{"debt":-200,"budget":-260,"economy":4},"desc":"","desc_en":""},
             {"lbl":"Maghintay at tingnan","lbl_en":"Wait and see","fx":{"economy":-5,"public_trust":-4},"desc":"","desc_en":""}]},
 # MEDIA
 {"id":"med1","cat":"MEDIA",
  "title":"VIRAL FAKE NEWS","title_en":"VIRAL DISINFORMATION",
  "flavor":"Isang fabricated video ang nag-claim na nagtatago ng mga patay ang administrasyon. 12M views sa 24 oras.",
  "flavor_en":"A fabricated video claims the administration is hiding deaths. 12M views in 24 hours.",
  "choices":[{"lbl":"Counter with facts","lbl_en":"Counter with facts","fx":{"public_trust":6,"press_freedom":3},"desc":"","desc_en":""},
             {"lbl":"Idemanda ang may-gawa","lbl_en":"Sue the creators","fx":{"press_freedom":-14,"public_trust":-4,"auth_power":6},"desc":"","desc_en":""},
             {"lbl":"Huwag pansinin","lbl_en":"Ignore it","fx":{"public_trust":-7},"desc":"","desc_en":""},
             {"lbl":"Social media takedown","lbl_en":"Social media takedown","fx":{"press_freedom":-8,"public_trust":2,"auth_power":4},"desc":"","desc_en":""}]},
 {"id":"med2","cat":"MEDIA",
  "title":"NAPATAY NA MAMAMAHAYAG","title_en":"JOURNALIST MURDERED",
  "flavor":"Si Renata Lim, investigative journalist sa Davao, ay pinatay. Ang CPJ at RSF ay nagbabanta ng sanctions.",
  "flavor_en":"Investigative journalist Renata Lim from Davao has been murdered. CPJ and RSF are threatening sanctions.",
  "choices":[{"lbl":"Agresibong imbestigasyon","lbl_en":"Aggressive investigation","fx":{"press_freedom":7,"public_trust":7,"rel_un":3},"desc":"","desc_en":""},
             {"lbl":"Banggitin lang","lbl_en":"Issue a statement only","fx":{"press_freedom":-5,"rel_un":-3},"desc":"","desc_en":""},
             {"lbl":"I-blame ang NPA","lbl_en":"Blame communist rebels","fx":{"public_trust":-4,"military":3,"press_freedom":-9},"desc":"","desc_en":""}]},
 {"id":"med3","cat":"MEDIA",
  "title":"SOCIAL MEDIA REGULATION BILL","title_en":"SOCIAL MEDIA REGULATION BILL",
  "flavor":"Panukalang batas ang mahigpit na regulation ng social media. Sinusuportahan ng kabinete, nilalabanan ng press groups.",
  "flavor_en":"A bill for strict social media regulation is backed by cabinet but opposed by press freedom groups.",
  "choices":[{"lbl":"Ipasa ang batas","lbl_en":"Pass the bill","fx":{"press_freedom":-13,"auth_power":6,"public_trust":2},"desc":"","desc_en":""},
             {"lbl":"Labanan ito","lbl_en":"Oppose the bill","fx":{"press_freedom":9,"public_trust":6},"desc":"","desc_en":""},
             {"lbl":"Amended version","lbl_en":"Pass amended version","fx":{"press_freedom":-3,"public_trust":3},"desc":"","desc_en":""}]},
 # MILITARY
 {"id":"mil1","cat":"MILITARY",
  "title":"PAG-ATAKE SA TIMOG","title_en":"REBEL ATTACK IN THE SOUTH",
  "flavor":"Isang rebeldeng grupo ang sinalakay ang munisipyo sa Lanao del Sur. 14 sundalo ang napatay.",
  "flavor_en":"A rebel group has attacked a municipality in Lanao del Sur. 14 soldiers have been killed.",
  "choices":[{"lbl":"Military offensive","lbl_en":"Launch military offensive","fx":{"military":9,"health":-6,"public_trust":-4},"desc":"","desc_en":""},
             {"lbl":"Peace talks","lbl_en":"Open peace talks","fx":{"rel_asean":6,"public_trust":6,"military":-4},"desc":"","desc_en":""},
             {"lbl":"Martial law sa rehiyon","lbl_en":"Declare martial law","fx":{"military":10,"public_trust":-16,"press_freedom":-12,"auth_power":12},"desc":"","desc_en":""},
             {"lbl":"Mag-alok ng amnesty","lbl_en":"Offer amnesty","fx":{"public_trust":7,"military":-5,"health":2},"desc":"","desc_en":""}]},
 {"id":"mil2","cat":"MILITARY",
  "title":"TANGKA NG KUDETA","title_en":"COUP ATTEMPT",
  "flavor":"Grupo ng mga heneral ang nagbabanta ng kudeta. Ang AFP ay nahati. Kailangan mong kumilos ngayon.",
  "flavor_en":"A group of generals is threatening a coup. The AFP is divided. You must act now.",
  "choices":[{"lbl":"Makipag-usap sa heneral","lbl_en":"Negotiate with generals","fx":{"military":-6,"public_trust":6},"desc":"","desc_en":""},
             {"lbl":"Arestuhin ang mga lider","lbl_en":"Arrest the ringleaders","fx":{"military":8,"public_trust":4,"auth_power":9},"desc":"","desc_en":""},
             {"lbl":"Loyalty purge","lbl_en":"Purge disloyal officers","fx":{"military":-9,"auth_power":14,"public_trust":-6},"desc":"","desc_en":""}]},
 {"id":"mil3","cat":"MILITARY",
  "title":"MODERNISASYON NG AFP","title_en":"AFP MODERNISATION REQUEST",
  "flavor":"Ang AFP ay humihiling ng bagong fighter jets at submarines. Malaki ang gastos ngunit mahalaga ang seguridad.",
  "flavor_en":"The AFP requests new fighter jets and submarines. Expensive but critical for national security.",
  "choices":[{"lbl":"Full modernization","lbl_en":"Full modernisation","fx":{"military":14,"budget":-300},"desc":"","desc_en":""},
             {"lbl":"Partial upgrade lang","lbl_en":"Partial upgrade only","fx":{"military":7,"budget":-150},"desc":"","desc_en":""},
             {"lbl":"Huwag muna","lbl_en":"Defer for now","fx":{"military":-4,"public_trust":3},"desc":"","desc_en":""}]},
 # FOREIGN
 {"id":"for1","cat":"FOREIGN",
  "title":"US BASE EXPANSION","title_en":"US BASE EXPANSION OFFER",
  "flavor":"Amerika ay nagmumungkahi ng dagdag na EDCA bases. Oposisyon ay malakas ngunit militar ay sumusuporta.",
  "flavor_en":"The US proposes additional EDCA bases. Domestic opposition is strong but the military supports it.",
  "choices":[{"lbl":"Payagan (may bayad)","lbl_en":"Allow (with compensation)","fx":{"military":10,"rel_us":10,"rel_china":-12,"sovereignty":-6,"budget":200},"desc":"","desc_en":""},
             {"lbl":"Makipagnegosasyon","lbl_en":"Negotiate terms","fx":{"military":5,"rel_us":5,"rel_china":-5,"budget":80},"desc":"","desc_en":""},
             {"lbl":"Tumanggi","lbl_en":"Refuse the offer","fx":{"sovereignty":10,"rel_us":-12,"military":-5},"desc":"","desc_en":""}]},
 {"id":"for2","cat":"FOREIGN",
  "title":"BRI INFRASTRUCTURE LOAN","title_en":"BRI INFRASTRUCTURE LOAN",
  "flavor":"Tsina ay nag-aalok ng P500B loan para sa rail line -- may kondisyon na daungan sa isang isla.",
  "flavor_en":"China offers a P500B loan for a rail line -- with a condition: port access on a contested island.",
  "choices":[{"lbl":"Tanggapin","lbl_en":"Accept the loan","fx":{"infrastructure":16,"budget":400,"sovereignty":-14,"rel_china":12,"debt":500},"desc":"","desc_en":""},
             {"lbl":"Counter-offer","lbl_en":"Counter-offer (less strings)","fx":{"infrastructure":9,"budget":150,"sovereignty":-5,"rel_china":5,"debt":200},"desc":"","desc_en":""},
             {"lbl":"Tumanggi","lbl_en":"Decline the loan","fx":{"sovereignty":9,"rel_china":-10},"desc":"","desc_en":""}]},
 {"id":"for3","cat":"FOREIGN",
  "title":"ASEAN SUMMIT HOST","title_en":"ASEAN SUMMIT HOST",
  "flavor":"Ang Pilipinas ay mag-ho-host ng ASEAN summit -- malaking pagkakataon sa diplomasya.",
  "flavor_en":"The Philippines is hosting the ASEAN summit -- a major diplomatic opportunity.",
  "choices":[{"lbl":"Show of leadership","lbl_en":"Show strong leadership","fx":{"rel_asean":11,"sovereignty":5,"budget":-60},"desc":"","desc_en":""},
             {"lbl":"Itaas ang WPS issue","lbl_en":"Raise the WPS issue","fx":{"rel_asean":5,"sovereignty":9,"rel_china":-9},"desc":"","desc_en":""},
             {"lbl":"Passive role lang","lbl_en":"Take a passive role","fx":{"rel_asean":2},"desc":"","desc_en":""}]},
 {"id":"for4","cat":"FOREIGN",
  "title":"CLIMATE AGREEMENT PRESSURE","title_en":"CLIMATE COMMITMENT PRESSURE",
  "flavor":"UN ay tumatawag ng mas ambisyosong climate commitments. NGOs ay nagpapressure sa administrasyon.",
  "flavor_en":"The UN calls for bolder climate commitments. NGOs are pressuring the administration to act.",
  "choices":[{"lbl":"Sumang-ayon sa lahat","lbl_en":"Agree to full commitments","fx":{"rel_un":11,"rel_asean":5,"economy":-4},"desc":"","desc_en":""},
             {"lbl":"Makipagnegosasyon","lbl_en":"Negotiate targets","fx":{"rel_un":5,"economy":-1},"desc":"","desc_en":""},
             {"lbl":"Tumanggi","lbl_en":"Refuse commitments","fx":{"rel_un":-11,"economy":4,"sovereignty":5},"desc":"","desc_en":""}]},
 # HEALTH
 {"id":"hlt1","cat":"HEALTH",
  "title":"EPIDEMYA NG DENGUE","title_en":"DENGUE EPIDEMIC",
  "flavor":"50,000 dengue cases sa Visayas sa loob ng 2 buwan. Ang mga ospital ay puno na.",
  "flavor_en":"50,000 dengue cases in Visayas over 2 months. Hospitals are at full capacity.",
  "choices":[{"lbl":"Emergency health funds","lbl_en":"Emergency health funding","fx":{"health":10,"public_trust":7,"budget":-140},"desc":"","desc_en":""},
             {"lbl":"WHO assistance","lbl_en":"Request WHO assistance","fx":{"health":9,"sovereignty":-3,"rel_un":5},"desc":"","desc_en":""},
             {"lbl":"I-downplay","lbl_en":"Downplay the outbreak","fx":{"health":-11,"public_trust":-9},"desc":"","desc_en":""}]},
 {"id":"hlt2","cat":"HEALTH",
  "title":"BAGONG BIRUS SA CEBU","title_en":"NEW VIRUS IN CEBU",
  "flavor":"Bagong respiratory disease ang lumabas -- 1,200 cases sa isang linggo. WHO ay nag-monitor na.",
  "flavor_en":"A new respiratory disease has emerged -- 1,200 cases in one week. WHO is now monitoring.",
  "choices":[{"lbl":"Lockdown","lbl_en":"Impose lockdown","fx":{"health":11,"economy":-9,"public_trust":3},"desc":"","desc_en":""},
             {"lbl":"Targeted quarantine","lbl_en":"Targeted quarantine","fx":{"health":6,"economy":-3},"desc":"","desc_en":""},
             {"lbl":"Hayaan ang daloy","lbl_en":"No restrictions","fx":{"health":-16,"economy":4,"public_trust":-12},"desc":"","desc_en":""}]},
 {"id":"hlt3","cat":"HEALTH",
  "title":"OSPITAL NA WALANG KWARTO","title_en":"HOSPITAL BED SHORTAGE",
  "flavor":"PhilHealth ay natuklasan na 40% ng ospital sa Mindanao ay hindi accredited. Pasyente ay tinatanggihan.",
  "flavor_en":"PhilHealth audit finds 40% of Mindanao hospitals unaccredited. Patients are being turned away.",
  "choices":[{"lbl":"Emergency hospital budget","lbl_en":"Emergency hospital funding","fx":{"health":8,"budget":-180,"public_trust":5},"desc":"","desc_en":""},
             {"lbl":"PPP sa private hospitals","lbl_en":"Public-private partnership","fx":{"health":5,"economy":3,"sovereignty":-2},"desc":"","desc_en":""},
             {"lbl":"Mag-imbestigahan muna","lbl_en":"Investigate first","fx":{"health":-2,"public_trust":-4},"desc":"","desc_en":""}]},
 # DISASTERS
 {"id":"dis1","cat":"DISASTER",
  "title":"LINDOL SA LUZON","title_en":"MAJOR LUZON EARTHQUAKE",
  "flavor":"7.2 magnitude earthquake sa Metro Manila. Daan-daang gusali ang natumba, libu-libo ang nangangailangan.",
  "flavor_en":"A 7.2 magnitude earthquake strikes Metro Manila. Hundreds of buildings collapsed, thousands need aid.",
  "choices":[{"lbl":"Full emergency response","lbl_en":"Full emergency response","fx":{"health":-5,"public_trust":9,"infrastructure":-11,"budget":-250},"desc":"","desc_en":""},
             {"lbl":"International aid","lbl_en":"Request international aid","fx":{"health":-3,"rel_un":5,"infrastructure":-8,"budget":-100},"desc":"","desc_en":""},
             {"lbl":"Lokal na pagsisikap","lbl_en":"Local effort only","fx":{"health":-9,"sovereignty":3,"public_trust":-4,"infrastructure":-13},"desc":"","desc_en":""}]},
 {"id":"dis2","cat":"DISASTER",
  "title":"BULKANG DALISAYIN","title_en":"VOLCANO ERUPTION",
  "flavor":"Ang Bulkang Dalisayin sa Batangas ay nagsimulang mag-erupt. 200,000 residente ang kailangang i-evacuate.",
  "flavor_en":"Mount Dalisayin in Batangas has begun erupting. 200,000 residents need immediate evacuation.",
  "choices":[{"lbl":"Mandatory evacuation","lbl_en":"Mandatory evacuation","fx":{"health":6,"public_trust":7,"budget":-160,"infrastructure":-4},"desc":"","desc_en":""},
             {"lbl":"Voluntary lang","lbl_en":"Voluntary evacuation","fx":{"health":-6,"public_trust":-4,"budget":-90},"desc":"","desc_en":""},
             {"lbl":"Maghintay","lbl_en":"Wait and monitor","fx":{"health":-14,"public_trust":-12},"desc":"","desc_en":""}]},
 {"id":"dis3","cat":"DISASTER",
  "title":"TULAY NA BUMAGSAK","title_en":"BRIDGE COLLAPSE",
  "flavor":"Ang pinakamatandang tulay sa Luzon ay bumagsak sa gitna ng trapiko. 9 sasakyan ang nahulog sa ilog.",
  "flavor_en":"The oldest bridge in Luzon collapsed during peak traffic. 9 vehicles fell into the river.",
  "choices":[{"lbl":"Emergency repairs","lbl_en":"Emergency repairs","fx":{"infrastructure":5,"budget":-160,"public_trust":5},"desc":"","desc_en":""},
             {"lbl":"Magtayo ng bago","lbl_en":"Build a new bridge","fx":{"infrastructure":13,"budget":-350,"economy":5},"desc":"","desc_en":""},
             {"lbl":"Imbestigahan lang","lbl_en":"Investigate only","fx":{"infrastructure":-3,"public_trust":-6},"desc":"","desc_en":""}]},
 # ELECTIONS
 {"id":"ele1","cat":"ELECTION",
  "title":"DAYAAN SA HALALAN","title_en":"ELECTION FRAUD ALLEGATIONS",
  "flavor":"Mga alegasyon ng ballot stuffing sa 5 probinsya. International observers ay nag-aalala na.",
  "flavor_en":"Ballot stuffing allegations in 5 provinces. International observers are raising concerns.",
  "choices":[{"lbl":"Independent investigation","lbl_en":"Independent investigation","fx":{"public_trust":7,"sovereignty":3,"rel_un":5},"desc":"","desc_en":""},
             {"lbl":"Itatwa ang lahat","lbl_en":"Deny all allegations","fx":{"public_trust":-9,"rel_un":-5},"desc":"","desc_en":""},
             {"lbl":"COMELEC audit","lbl_en":"COMELEC audit","fx":{"public_trust":4,"economy":-2},"desc":"","desc_en":""}]},
 {"id":"ele2","cat":"ELECTION",
  "title":"LAKTAW-BAHAY NA PROTESTA","title_en":"MASS OPPOSITION RALLY",
  "flavor":"Oposisyon ay nag-organisa ng malaking rally sa EDSA. 600,000 ang dumalo.",
  "flavor_en":"The opposition organises a massive rally at EDSA. An estimated 600,000 people attended.",
  "choices":[{"lbl":"Respectuhin ang demokrasya","lbl_en":"Respect democratic rights","fx":{"public_trust":6,"press_freedom":5},"desc":"","desc_en":""},
             {"lbl":"Counter-rally","lbl_en":"Organise counter-rally","fx":{"public_trust":-4,"budget":-25},"desc":"","desc_en":""},
             {"lbl":"Limitahan ang rally","lbl_en":"Restrict the rally","fx":{"public_trust":-12,"press_freedom":-11,"auth_power":9},"desc":"","desc_en":""}]},
 # POLITICS
 {"id":"pol1","cat":"POLITICS",
  "title":"CHARTER CHANGE PUSH","title_en":"CHARTER CHANGE PUSH",
  "flavor":"Mga kongresista ay nagmumungkahi ng ChaChange -- maaaring magbago ng sistema ng pamahalaan.",
  "flavor_en":"Congressmen are pushing for a charter change that could overhaul the system of government.",
  "choices":[{"lbl":"Suportahan ang ChaChange","lbl_en":"Support charter change","fx":{"auth_power":12,"public_trust":-7,"sovereignty":6},"desc":"","desc_en":""},
             {"lbl":"Labanan ito","lbl_en":"Oppose the move","fx":{"public_trust":9,"press_freedom":6},"desc":"","desc_en":""},
             {"lbl":"Pag-aralan muna","lbl_en":"Study it first","fx":{"public_trust":3},"desc":"","desc_en":""}]},
 {"id":"pol2","cat":"POLITICS",
  "title":"BOTO NG KAWALAN NG TIWALA","title_en":"VOTE OF NO CONFIDENCE",
  "flavor":"Ang oposisyon sa parliyamento ay nagpahayag ng vote of no confidence laban sa administrasyon.",
  "flavor_en":"The parliamentary opposition has tabled a vote of no confidence against the administration.",
  "sys":["Parliamentary System"],
  "choices":[{"lbl":"Kausapin ang mga ally","lbl_en":"Whip coalition allies","fx":{"public_trust":5,"economy":3},"desc":"","desc_en":""},
             {"lbl":"Dissolve parliament","lbl_en":"Dissolve parliament","fx":{"public_trust":-9,"auth_power":9},"desc":"","desc_en":""}]},
 {"id":"pol3","cat":"POLITICS",
  "title":"REHIYONAL NA TENSYON","title_en":"REGIONAL AUTONOMY TENSION",
  "flavor":"Ilang rehiyon ay nagtatayo ng sarili nilang hudisyal na sistema -- labas sa Federal framework.",
  "flavor_en":"Several regions are setting up their own judicial systems -- outside the Federal framework.",
  "sys":["Federal Republic"],
  "choices":[{"lbl":"Payagan (federalism works)","lbl_en":"Allow regional autonomy","fx":{"sovereignty":5,"public_trust":5,"infrastructure":3},"desc":"","desc_en":""},
             {"lbl":"I-recentralize","lbl_en":"Recentralise authority","fx":{"public_trust":-5,"economy":3},"desc":"","desc_en":""}]},
 # AUTHORITARIAN
 {"id":"auth1","cat":"SECURITY",
  "title":"DIGMAAN SA DROGA","title_en":"DRUG WAR CAMPAIGN",
  "flavor":"Ang pulis ay nagmumungkahi ng malakas na kampanya laban sa illegal drugs -- controversial internationally.",
  "flavor_en":"The police propose a harsh anti-drug campaign -- controversial at home and internationally.",
  "choices":[{"lbl":"Suportahan ang drug war","lbl_en":"Support the drug war","fx":{"military":7,"public_trust":4,"rel_un":-12,"press_freedom":-6,"auth_power":9},"desc":"","desc_en":""},
             {"lbl":"Rule-of-law approach","lbl_en":"Rule-of-law approach","fx":{"rel_un":6,"public_trust":3,"corruption":-5},"desc":"","desc_en":""},
             {"lbl":"Rehabilitation focus","lbl_en":"Rehabilitation focus","fx":{"health":7,"public_trust":6,"budget":-100},"desc":"","desc_en":""}]},
 {"id":"auth2","cat":"AUTHORITARIAN",
  "title":"MABILIS NA REPORMA","title_en":"RAPID AUTHORITARIAN REFORM",
  "flavor":"Bilang malakas na lider, maaari kang mag-implement ng malawak na reporma nang walang legislative delay.",
  "flavor_en":"As a strong leader, you can implement sweeping reforms without legislative delay.",
  "sys":["Benevolent Authoritarianism"],
  "choices":[{"lbl":"Anti-corruption blitz","lbl_en":"Anti-corruption blitz","fx":{"corruption":-22,"economy":8,"press_freedom":-4},"desc":"","desc_en":""},
             {"lbl":"Education mega-program","lbl_en":"Education mega-program","fx":{"education":16,"economy":5,"budget":-200},"desc":"","desc_en":""},
             {"lbl":"Infrastructure blitz","lbl_en":"Infrastructure blitz","fx":{"infrastructure":16,"budget":-250,"economy":9},"desc":"","desc_en":""}]},
 {"id":"auth3","cat":"AUTHORITARIAN",
  "title":"MGA KAAWAY NG ESTADO","title_en":"ENEMIES OF THE STATE",
  "flavor":"Ang mga kritiko ay nag-oorganisa ng lihim na oposisyon. Maaari mong gamitin ang kapangyarihan laban sa kanila.",
  "flavor_en":"Critics are organising secret opposition. You have the power to act against them.",
  "sys":["Authoritarian Dictatorship"],
  "choices":[{"lbl":"Ikulong ang mga kritiko","lbl_en":"Imprison critics","fx":{"press_freedom":-22,"auth_power":16,"public_trust":-12,"rel_un":-12},"desc":"","desc_en":""},
             {"lbl":"Gamitin ang kanilang assets","lbl_en":"Seize their assets","fx":{"corruption":16,"budget":120,"public_trust":-9},"desc":"","desc_en":""},
             {"lbl":"Hayaan silang magsalita","lbl_en":"Allow free speech","fx":{"press_freedom":5,"public_trust":6},"desc":"","desc_en":""}]},
 {"id":"auth4","cat":"AUTHORITARIAN",
  "title":"KAYAMANAN NG PAMILYA","title_en":"FAMILY WEALTH OPPORTUNITY",
  "flavor":"Isang oportunidad -- ang malaking halaga ng pondo ng gobyerno ay maaaring ilipat sa mga pribadong account.",
  "flavor_en":"An opportunity -- large government funds could be quietly moved to private accounts.",
  "sys":["Authoritarian Dictatorship"],
  "choices":[{"lbl":"Kunin ang pera","lbl_en":"Take the money","fx":{"corruption":28,"budget":300,"public_trust":-18,"inequality":12},"desc":"","desc_en":""},
             {"lbl":"Tanggihan","lbl_en":"Refuse","fx":{"corruption":-5,"public_trust":5},"desc":"","desc_en":""}]},
 {"id":"auth5","cat":"AUTHORITARIAN",
  "title":"SUCCESSION CRISIS","title_en":"SUCCESSION CRISIS",
  "flavor":"Ang iyong pagiging makapangyarihan ay nagdudulot ng tanong: sino ang susunod na lider?",
  "flavor_en":"Your grip on power raises the question: who comes next? Your inner circle is already jostling.",
  "sys":["Benevolent Authoritarianism","Authoritarian Dictatorship"],
  "choices":[{"lbl":"Magtalaga ng kahalili","lbl_en":"Designate a successor","fx":{"auth_power":-5,"public_trust":7,"sovereignty":3},"desc":"","desc_en":""},
             {"lbl":"Magpatuloy nang walang hanggan","lbl_en":"Cling to power indefinitely","fx":{"auth_power":12,"public_trust":-8,"rel_un":-8},"desc":"","desc_en":""}]},
 # SOCIAL
 {"id":"soc1","cat":"SOCIAL",
  "title":"TEACHER SHORTAGE","title_en":"TEACHER SHORTAGE",
  "flavor":"700,000 mag-aaral ang walang regular na guro. DepEd ay labis na nag-eenroll nang walang sapat na manggagawa.",
  "flavor_en":"700,000 students have no permanent teacher. DepEd over-enrolled without hiring enough staff.",
  "choices":[{"lbl":"Mag-hire ng 50,000 guro","lbl_en":"Hire 50,000 teachers","fx":{"education":13,"budget":-220,"public_trust":8},"desc":"","desc_en":""},
             {"lbl":"Online learning expansion","lbl_en":"Expand online learning","fx":{"education":4,"inequality":5},"desc":"","desc_en":""},
             {"lbl":"NGO partnership","lbl_en":"NGO partnership","fx":{"education":7,"budget":-60},"desc":"","desc_en":""}]},
 {"id":"soc2","cat":"SOCIAL",
  "title":"WATER CRISIS SA METRO","title_en":"METRO WATER CRISIS",
  "flavor":"Metro Manila ay nakakaranas ng malubhang water shortage -- ilang linggo na wala sa ilang baranggay.",
  "flavor_en":"Metro Manila faces a severe water shortage -- some barangays have had no supply for weeks.",
  "choices":[{"lbl":"Emergency water supply","lbl_en":"Emergency water supply","fx":{"health":6,"public_trust":7,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Private sector contract","lbl_en":"Private sector contract","fx":{"health":4,"sovereignty":-3,"economy":4},"desc":"","desc_en":""},
             {"lbl":"Rationalize distribution","lbl_en":"Ration distribution","fx":{"health":2,"public_trust":-4},"desc":"","desc_en":""}]},
 {"id":"soc3","cat":"SOCIAL",
  "title":"TRABAHO PARA SA LAHAT","title_en":"UNEMPLOYMENT CRISIS",
  "flavor":"Unemployment ay pumalo sa 12%. Mga kabataan ay nagrereklamo na walang oportunidad.",
  "flavor_en":"Unemployment hits 12%. Young Filipinos say there are no opportunities.",
  "choices":[{"lbl":"Jobs program P180B","lbl_en":"P180B jobs programme","fx":{"inequality":-8,"economy":7,"budget":-180},"desc":"","desc_en":""},
             {"lbl":"Invite foreign investment","lbl_en":"Invite foreign investment","fx":{"economy":10,"sovereignty":-4},"desc":"","desc_en":""},
             {"lbl":"Vocational training","lbl_en":"Vocational training push","fx":{"education":6,"economy":4,"budget":-80},"desc":"","desc_en":""}]},
 # ── POLITICAL CRITICISM & ACCUSATIONS ──────────────────────
 {"id":"opp_scandal","cat":"POLITICS",
  "title":"ISKANDALO SA KONGRESO","title_en":"CONGRESSIONAL SCANDAL",
  "flavor":"Si Sen. Bantay-Bayan ay nag-hold ng press conference na inakusahan ang administrasyon ng pagnanakaw ng P20B mula sa pondo ng kalamidad.",
  "flavor_en":"Sen. Bantay-Bayan held a press conference accusing the administration of stealing P20B from calamity funds.",
  "choices":[
    {"lbl":"I-harap sa imbestigasyon","lbl_en":"Face the investigation","fx":{"public_trust":5,"corruption":-5},"desc":"","desc_en":""},
    {"lbl":"Itatwa at salungatin","lbl_en":"Deny and counter-attack","fx":{"public_trust":-6,"press_freedom":-5,"auth_power":4},"desc":"","desc_en":""},
    {"lbl":"Mag-file ng libel case","lbl_en":"File libel charges","fx":{"press_freedom":-12,"public_trust":-4,"auth_power":8},"desc":"","desc_en":""},
    {"lbl":"Mag-imbestigahan","lbl_en":"Launch own investigation","fx":{"corruption":-8,"public_trust":7,"budget":-40},"desc":"","desc_en":""},
  ]},
 {"id":"opp_rally2","cat":"POLITICS",
  "title":"SENADOR NA NAGSALITA","title_en":"SENATOR SPEAKS OUT",
  "flavor":"Isang kilalang senador ang nagdeklara na ang administrasyon ay 'pinaka-kumpanya ng mga magnanakaw' sa kasaysayan ng bansa.",
  "flavor_en":"A prominent senator declared the administration is 'the biggest criminal enterprise' in the country's history.",
  "choices":[
    {"lbl":"Harapin nang mahinahon","lbl_en":"Respond calmly","fx":{"public_trust":4,"press_freedom":4},"desc":"","desc_en":""},
    {"lbl":"Alisin sa komite","lbl_en":"Strip committee roles","fx":{"auth_power":7,"public_trust":-5},"desc":"","desc_en":""},
    {"lbl":"Legal na aksyon","lbl_en":"Legal action","fx":{"press_freedom":-8,"public_trust":-3,"auth_power":5},"desc":"","desc_en":""},
  ]},
 {"id":"media_expose","cat":"MEDIA",
  "title":"IMBESTIGASYON NG PAHAYAGAN","title_en":"NEWSPAPER EXPOSÉ",
  "flavor":"Ang isang broadsheet ay naglathala ng serye ng mga imbestigasyon tungkol sa mga allegasyon ng kickback sa mga kontrata ng gobyerno.",
  "flavor_en":"A major broadsheet published an investigation into alleged kickbacks in government contracts worth P50B.",
  "choices":[
    {"lbl":"Payagan ang imbestigasyon","lbl_en":"Allow the investigation","fx":{"corruption":-10,"public_trust":6},"desc":"","desc_en":""},
    {"lbl":"Tawagin ang publisher","lbl_en":"Summon the publisher","fx":{"press_freedom":-14,"public_trust":-5,"auth_power":7},"desc":"","desc_en":""},
    {"lbl":"Gumawa ng official response","lbl_en":"Issue official response","fx":{"public_trust":3,"corruption":-4},"desc":"","desc_en":""},
  ]},
 {"id":"rig_election","cat":"ELECTION",
  "title":"PAGKAKATAON SA HALALAN","title_en":"ELECTION OPPORTUNITY",
  "flavor":"Ang iyong punong-tagapayo ay nagmumungkahi ng 'pagtulong' sa mga resulta ng halalan sa 4 na probinsya upang masiguro ang inyong pagtatagumpay.",
  "flavor_en":"Your chief adviser suggests 'assisting' the election results in 4 provinces to ensure your continued rule.",
  "choices":[
    {"lbl":"Tanggihan -- demokrasya muna","lbl_en":"Refuse -- democracy first","fx":{"public_trust":8,"press_freedom":5,"sovereignty":4},"desc":"","desc_en":""},
    {"lbl":"Dayain ang halalan","lbl_en":"Rig the election","fx":{"auth_power":18,"corruption":16,"public_trust":-12,"rel_un":-14,"rigged_election":1},"desc":"","desc_en":""},
    {"lbl":"Bahagyang 'tulong' lang","lbl_en":"Minor 'assistance' only","fx":{"auth_power":8,"corruption":8,"public_trust":-5,"rigged_election":1},"desc":"","desc_en":""},
  ]},
 {"id":"coup_rumour","cat":"MILITARY",
  "title":"TSISMIS NG KUDETA","title_en":"COUP RUMOURS",
  "flavor":"Maaasahang pinagkukunan ng AFP ang nag-uulat ng mga kumikilos na pangkat ng mga opisyal na hindi nasisiyahan sa pamumuno.",
  "flavor_en":"Reliable AFP sources report a faction of disgruntled officers is quietly organising against the administration.",
  "choices":[
    {"lbl":"Arestuhin ang mga suspek","lbl_en":"Arrest the suspects","fx":{"military":8,"public_trust":-4,"auth_power":10},"desc":"","desc_en":""},
    {"lbl":"Makipag-usap sa kanila","lbl_en":"Negotiate with them","fx":{"military":-4,"public_trust":5},"desc":"","desc_en":""},
    {"lbl":"Palakasin ang katapatan","lbl_en":"Strengthen loyalty ops","fx":{"military":5,"budget":-60,"auth_power":6},"desc":"","desc_en":""},
    {"lbl":"Huwag pansinin","lbl_en":"Ignore the rumours","fx":{"military":-8,"coup_overthrow_risk":1},"desc":"","desc_en":""},
  ]},
 # ── DIPLOMACY ───────────────────────────────────────────────
 {"id":"dip_asean_visit","cat":"DIPLOMACY",
  "title":"STATE VISIT SA ASEAN","title_en":"ASEAN STATE VISIT",
  "flavor":"Ang isang ASEAN na lider ay nagdaraos ng opisyal na pagbisita. Ito ay pagkakataon para palakasin ang relasyon.",
  "flavor_en":"An ASEAN head of state is making an official visit. A chance to strengthen regional ties.",
  "choices":[
    {"lbl":"Pormal na state dinner","lbl_en":"Formal state dinner","fx":{"rel_asean":10,"economy":4,"budget":-30},"desc":"","desc_en":""},
    {"lbl":"Trade agreement lamang","lbl_en":"Trade agreement only","fx":{"rel_asean":7,"economy":8},"desc":"","desc_en":""},
    {"lbl":"Itaas ang WPS issue","lbl_en":"Raise WPS issue","fx":{"sovereignty":8,"rel_asean":3,"rel_china":-5},"desc":"","desc_en":""},
  ]},
 {"id":"dip_un_speech","cat":"DIPLOMACY",
  "title":"TALUMPATI SA UN GENERAL ASSEMBLY","title_en":"UN GENERAL ASSEMBLY SPEECH",
  "flavor":"Magsasalita ka sa harap ng UN General Assembly. Ano ang mensahe ng Pilipinas sa mundo?",
  "flavor_en":"You will address the UN General Assembly. What message does the Philippines send to the world?",
  "choices":[
    {"lbl":"Sovereignty at rule of law","lbl_en":"Sovereignty and rule of law","fx":{"rel_un":10,"sovereignty":8,"rel_china":-4},"desc":"","desc_en":""},
    {"lbl":"Economic development","lbl_en":"Economic development focus","fx":{"rel_un":7,"economy":4,"rel_asean":5},"desc":"","desc_en":""},
    {"lbl":"Climate leadership","lbl_en":"Climate leadership","fx":{"rel_un":12,"rel_asean":6,"economy":-2},"desc":"","desc_en":""},
    {"lbl":"Baguhin ang imahe ng bansa","lbl_en":"Rebrand the country's image","fx":{"rel_un":5,"public_trust":5,"economy":3},"desc":"","desc_en":""},
  ]},
 {"id":"dip_us_summit","cat":"DIPLOMACY",
  "title":"US-PH SUMMIT","title_en":"US-PH SUMMIT",
  "flavor":"Ang Presidente ng US ay nag-imbitang magpulong. Ang agenda: trade, military, at South China Sea.",
  "flavor_en":"The US President has invited you to a summit. Agenda: trade, defence, and the South China Sea.",
  "choices":[
    {"lbl":"Palakasin ang alyansa","lbl_en":"Strengthen alliance","fx":{"rel_us":14,"military":8,"rel_china":-10},"desc":"","desc_en":""},
    {"lbl":"Trade-focused lang","lbl_en":"Trade-focused only","fx":{"rel_us":8,"economy":10,"rel_china":-4},"desc":"","desc_en":""},
    {"lbl":"Balanced -- huwag mag-commit","lbl_en":"Balanced -- avoid commitment","fx":{"rel_us":4,"rel_china":2,"sovereignty":5},"desc":"","desc_en":""},
    {"lbl":"Tanggihan ang imbitasyon","lbl_en":"Decline the invitation","fx":{"rel_us":-12,"sovereignty":8,"rel_china":6},"desc":"","desc_en":""},
  ]},
 {"id":"dip_china_state","cat":"DIPLOMACY",
  "title":"ESTADO NG PAGBISITA SA TSINA","title_en":"CHINA STATE VISIT",
  "flavor":"Ang pinuno ng Tsina ay nag-imbita para sa isang state visit sa Beijing -- isang malaking diplomatikong sandali.",
  "flavor_en":"China's leader has invited you for a state visit to Beijing -- a major diplomatic moment.",
  "choices":[
    {"lbl":"Tanggapin -- palakasin ang ugnayan","lbl_en":"Accept -- strengthen ties","fx":{"rel_china":16,"economy":8,"rel_us":-8,"sovereignty":-5},"desc":"","desc_en":""},
    {"lbl":"Tanggapin ngunit itaas ang WPS","lbl_en":"Accept but raise WPS issue","fx":{"rel_china":7,"sovereignty":7,"rel_us":-3},"desc":"","desc_en":""},
    {"lbl":"Tanggihan","lbl_en":"Decline","fx":{"rel_china":-10,"rel_us":6,"sovereignty":9},"desc":"","desc_en":""},
  ]},
 # ── MEDIA INTERVIEWS ────────────────────────────────────────
 {"id":"int_tv","cat":"INTERVIEW","title":"LIVE NA TV INTERVIEW","title_en":"LIVE TV INTERVIEW",
  "flavor":"Si veteran journalist na si Redentor Cruz ay nagtatanong tungkol sa mga alegasyon ng katiwalian at ang estado ng ekonomiya.",
  "flavor_en":"Veteran journalist Redentor Cruz questions you live on air about corruption allegations and the state of the economy.",
  "choices":[
    {"lbl":"Transparent at detalyado","lbl_en":"Transparent and detailed answers","fx":{"public_trust":10,"press_freedom":6},"desc":"","desc_en":""},
    {"lbl":"Diplomatic -- maingat na sagot","lbl_en":"Diplomatic -- carefully worded","fx":{"public_trust":4,"press_freedom":3},"desc":"","desc_en":""},
    {"lbl":"Mapanggalit -- atakihin ang media","lbl_en":"Combative -- attack the media","fx":{"public_trust":-6,"press_freedom":-10,"auth_power":5},"desc":"","desc_en":""},
    {"lbl":"Tumanggi sa interview","lbl_en":"Refuse the interview","fx":{"public_trust":-8,"press_freedom":-5},"desc":"","desc_en":""},
  ]},
 {"id":"int_foreign","cat":"INTERVIEW","title":"INTERNATIONAL PRESS INTERVIEW","title_en":"INTERNATIONAL PRESS INTERVIEW",
  "flavor":"Ang CNN International ay humiling ng exclusive interview. Ito ay malaking pagkakataon para sa imahe ng Pilipinas sa mundo.",
  "flavor_en":"CNN International requests an exclusive interview. A big chance to shape the Philippines' global image.",
  "choices":[
    {"lbl":"Tanggapin -- ipakita ang pag-unlad","lbl_en":"Accept -- showcase progress","fx":{"rel_un":8,"rel_us":5,"public_trust":5},"desc":"","desc_en":""},
    {"lbl":"Tanggapin ngunit limitahan","lbl_en":"Accept with limited topics","fx":{"rel_un":4,"public_trust":2},"desc":"","desc_en":""},
    {"lbl":"Tanggihan -- sovereignty muna","lbl_en":"Decline -- sovereignty first","fx":{"sovereignty":5,"rel_un":-5},"desc":"","desc_en":""},
  ]},
 # ── POLITICAL DEBATES ────────────────────────────────────────
 {"id":"debate_opp","cat":"DEBATE","title":"DEBATE SA OPOSISYON","title_en":"OPPOSITION DEBATE",
  "flavor":"Ang lider ng oposisyon ay humingi ng pampublikong debate sa primetime. Delikado ngunit malaki ang gantimpala.",
  "flavor_en":"The opposition leader demanded a primetime public debate. Risky but high reward.",
  "choices":[
    {"lbl":"Tanggapin at manalo","lbl_en":"Accept and dominate the debate","fx":{"public_trust":14,"press_freedom":5},"desc":"","desc_en":""},
    {"lbl":"Tanggapin -- maingat na lalahok","lbl_en":"Accept -- cautious participation","fx":{"public_trust":6,"press_freedom":4},"desc":"","desc_en":""},
    {"lbl":"Tanggapin -- mahirap ang debate","lbl_en":"Accept -- struggle visibly","fx":{"public_trust":-8,"press_freedom":6},"desc":"","desc_en":""},
    {"lbl":"Tumanggi sa debate","lbl_en":"Refuse the debate","fx":{"public_trust":-10,"press_freedom":-5,"auth_power":4},"desc":"","desc_en":""},
  ]},
 {"id":"debate_economy","cat":"DEBATE","title":"ECONOMIC POLICY DEBATE","title_en":"ECONOMIC POLICY DEBATE",
  "flavor":"Mga eksperto at oposisyon ay nanghamon ng pampublikong debate sa economic policy ng administrasyon.",
  "flavor_en":"Economists and opposition challenge the administration's economic record in a public forum.",
  "choices":[
    {"lbl":"Ipagtanggol nang buo","lbl_en":"Defend boldly with data","fx":{"economy":4,"public_trust":8},"desc":"","desc_en":""},
    {"lbl":"Aminin ang mga pagkakamali","lbl_en":"Admit mistakes, promise reform","fx":{"public_trust":10,"economy":2},"desc":"","desc_en":""},
    {"lbl":"Isipin ang oposisyon","lbl_en":"Deflect -- blame predecessors","fx":{"public_trust":-4,"economy":2},"desc":"","desc_en":""},
  ]},
 # ── POLITICAL SHOWS ──────────────────────────────────────────
 {"id":"pshow_parade","cat":"POLITICAL_SHOW","title":"MILITARY PARADE","title_en":"MILITARY PARADE",
  "flavor":"Ang AFP ay nagmumungkahi ng malaking military parade sa EDSA para ipakita ang lakas ng bansa.",
  "flavor_en":"The AFP proposes a major military parade along EDSA to project national strength.",
  "choices":[
    {"lbl":"Grandeng parade -- lahat ipalabas","lbl_en":"Grand parade -- full display","fx":{"military":8,"public_trust":6,"sovereignty":5,"budget":-60},"desc":"","desc_en":""},
    {"lbl":"Katamtamang parade lang","lbl_en":"Modest parade only","fx":{"military":4,"public_trust":3,"budget":-25},"desc":"","desc_en":""},
    {"lbl":"Huwag -- gastos lang","lbl_en":"Cancel -- waste of funds","fx":{"military":-3,"public_trust":-2},"desc":"","desc_en":""},
  ]},
 {"id":"pshow_world","cat":"POLITICAL_SHOW","title":"WORLD STAGE -- DAVOS","title_en":"WORLD STAGE -- DAVOS",
  "flavor":"Na-imbita ka sa World Economic Forum sa Davos. Pagkakataon para ipakita ang Pilipinas sa mundo.",
  "flavor_en":"You are invited to speak at the World Economic Forum in Davos. Showcase the Philippines globally.",
  "choices":[
    {"lbl":"Pumunta -- aktibong pakikilahok","lbl_en":"Attend -- active participation","fx":{"rel_un":8,"rel_us":5,"rel_asean":5,"economy":4,"budget":-40},"desc":"","desc_en":""},
    {"lbl":"Pumunta -- observation lang","lbl_en":"Attend -- observe only","fx":{"rel_un":4,"economy":2,"budget":-20},"desc":"","desc_en":""},
    {"lbl":"Huwag pumunta","lbl_en":"Skip -- focus on domestic","fx":{"sovereignty":4,"economy":-2},"desc":"","desc_en":""},
  ]},
 {"id":"pshow_stadium","cat":"POLITICAL_SHOW","title":"MALAKING RALLY SA ESTADYUM","title_en":"STADIUM RALLY",
  "flavor":"Ang inyong partido ay nag-oorganisa ng malaking rally sa Rizal Memorial Stadium -- 100,000 tagasuporta.",
  "flavor_en":"Your party organises a massive rally at Rizal Memorial -- 100,000 supporters expected.",
  "choices":[
    {"lbl":"Pumunta -- inspirasyon ang mensahe","lbl_en":"Attend -- inspirational speech","fx":{"public_trust":12,"approval_rating":3,"budget":-30},"desc":"","desc_en":""},
    {"lbl":"Pumunta -- pangako ng bagong programa","lbl_en":"Attend -- announce new programme","fx":{"public_trust":8,"economy":3,"budget":-50},"desc":"","desc_en":""},
    {"lbl":"Huwag pumunta -- posibleng riot","lbl_en":"Skip -- security concerns","fx":{"public_trust":-5},"desc":"","desc_en":""},
  ]},
 # ── OLD AGE (dictator) ───────────────────────────────────────
 {"id":"old_age_health","cat":"AUTHORITARIAN","title":"KALUSUGAN NG PRESIDENTE","title_en":"PRESIDENTIAL HEALTH SCARE",
  "flavor":"Pagkatapos ng maraming taon sa kapangyarihan, ang inyong doktor ay nagsabi na ang inyong katawan ay nagpapakita ng mga senyales ng pagod. Ilang opsyon ang nasa harap mo.",
  "flavor_en":"After many years in power, your doctor reports your body is showing serious signs of strain. You must decide your legacy.",
  "sys":["Benevolent Authoritarianism","Authoritarian Dictatorship"],
  "choices":[
    {"lbl":"Magbitiw -- legacy na matino","lbl_en":"Step down -- leave a clean legacy","fx":{"public_trust":18,"sovereignty":10,"auth_power":-30},"desc":"","desc_en":""},
    {"lbl":"Manatili -- kalusugan ay lihim","lbl_en":"Stay -- hide health issues","fx":{"corruption":8,"public_trust":-10,"auth_power":6},"desc":"","desc_en":""},
    {"lbl":"Mag-appoint ng kahalili","lbl_en":"Appoint a chosen successor","fx":{"public_trust":8,"sovereignty":4,"auth_power":-15},"desc":"","desc_en":""},
  ]},
]

# ── TYPHOON ENGINE ───────────────────────────────────────────
TYPHOON_NAMES=["Amang","Bising","Chedeng","Domeng","Egay","Fabian","Gorio","Herman",
               "Inday","Julian","Karding","Lando","Maricel","Nando","Onyok","Pepito",
               "Quedan","Rosita","Siony","Tonyo","Ulysses","Viring","Warling","Yoyoy",
               "Zosimo","Ambo","Betty","Carlos","Dante","Elsa","Frank","Gladys","Hugo"]
REGION_LIST=["Ilocos","Cagayan Valley","Central Luzon","NCR","CALABARZON",
             "MIMAROPA","Bicol","Western Visayas","Central Visayas","Eastern Visayas",
             "Zamboanga","Northern Mindanao","Davao Region","SOCCSKSARGEN","Caraga","CAR","Palawan"]

class TyphoonEngine:
    def season(self,gs):
        diff={"ESTUDYANTE":1.0,"SENADOR":1.4,"PANGULO":1.9}.get(gs.difficulty,1.4)
        used=set(); out=[]
        for _ in range(random.randint(3,7)):
            pool=[n for n in TYPHOON_NAMES if n not in used]
            nm=random.choice(pool) if pool else "Unang"
            used.add(nm)
            cat=random.choices([1,2,3,4,5],[18,25,28,20,9])[0]
            if gs.difficulty=="PANGULO" and random.random()<0.4: cat=min(5,cat+1)
            reg=random.choice(REGION_LIST)
            base=[8,22,55,120,260][cat-1]
            dmg=base*(1+(60-gs.infrastructure)/80)*diff*random.uniform(0.75,1.35)
            out.append({"name":f"Bagyo {nm}","cat":cat,"region":reg,"damage":round(dmg,1),"month":random.randint(6,11)})
        return out

    def resolve(self,gs,typhoons,relief):
        total=sum(t["damage"] for t in typhoons)
        ratio=relief/max(total,1)
        if ratio<0.55:   outcome="KULANG";   td=(-14,-10,-8)
        elif ratio>1.25: outcome="SOBRA";    td=(9,2,-2)
        else:            outcome="TAMANG";   td=(2,-4,-5)
        gs.public_trust+=td[0]; gs.health+=td[1]; gs.infrastructure+=td[2]
        gs.budget-=min(min(relief,total*1.15),gs.budget)
        gs.clamp()
        for t in typhoons:
            gs.typhoon_history.insert(0,{"year":gs.year,"name":t["name"],"cat":t["cat"],
                                         "region":t["region"],"damage":t["damage"],"outcome":outcome})
        if len(gs.typhoon_history)>60: gs.typhoon_history=gs.typhoon_history[:60]
        return {"outcome":outcome,"total":total,"n":len(typhoons)}

# ── POLICY MANAGER ───────────────────────────────────────────
# ── RESEARCH TREE ────────────────────────────────────────────
# Each research item: id, name, category, cost (one-time PB),
# rp_cost (research points needed), fx (permanent stat bonuses once unlocked),
# prereq (list of ids that must be unlocked first), desc
RESEARCH=[
 # ── MEDICINE & PUBLIC HEALTH ──────────────────────────────
 {"id":"r_vaccines","cat":"MEDICINE","icon":"Vax",
  "name":"National Vaccine Programme","cost":60,"rp_cost":3,"prereq":[],
  "fx":{"health":8,"inequality":-2},
  "desc":"Free vaccines for children & adults; reduces disease burden"},
 {"id":"r_dengue_cure","cat":"MEDICINE","icon":"Dngue",
  "name":"Dengue Vaccine Rollout","cost":40,"rp_cost":4,"prereq":["r_vaccines"],
  "fx":{"health":6,"public_trust":4},
  "desc":"Indigenously produced dengue vaccine deployed nationwide"},
 {"id":"r_cancer","cat":"MEDICINE","icon":"DNA",
  "name":"Cancer Treatment Centres","cost":90,"rp_cost":6,"prereq":["r_vaccines"],
  "fx":{"health":10,"inequality":-4},
  "desc":"Regional oncology hubs with affordable cancer care"},
 {"id":"r_telemedicine","cat":"MEDICINE","icon":"Telemed",
  "name":"Telemedicine Network","cost":35,"rp_cost":3,"prereq":[],
  "fx":{"health":5,"education":2,"inequality":-3},
  "desc":"Remote healthcare consultations for rural & island areas"},
 {"id":"r_genomics","cat":"MEDICINE","icon":"Genomics",
  "name":"Philippine Genomics Institute","cost":120,"rp_cost":8,"prereq":["r_cancer"],
  "fx":{"health":8,"economy":4,"education":5},
  "desc":"Precision medicine & disease surveillance using genomic data"},
 # ── SCIENCE & TECHNOLOGY ──────────────────────────────────
 {"id":"r_internet","cat":"TECH","icon":"GovIT",
  "name":"Open-Source Government Tech","cost":25,"rp_cost":2,"prereq":[],
  "fx":{"corruption":-5,"economy":4,"education":3},
  "desc":"Digital government services & open data platforms"},
 {"id":"r_ai","cat":"TECH","icon":"AI",
  "name":"AI for Governance","cost":80,"rp_cost":6,"prereq":["r_internet"],
  "fx":{"corruption":-8,"economy":9,"education":5},
  "desc":"AI tools for tax collection, fraud detection & service delivery"},
 {"id":"r_satellite","cat":"TECH","icon":"Satellite",
  "name":"Filipino Satellite Programme","cost":150,"rp_cost":9,"prereq":["r_ai"],
  "fx":{"sovereignty":10,"military":5,"economy":6,"education":4},
  "desc":"Indigenous satellite for weather, comms & maritime surveillance"},
 {"id":"r_cyber","cat":"TECH","icon":"Cyber",
  "name":"Cybersecurity National Centre","cost":55,"rp_cost":5,"prereq":["r_internet"],
  "fx":{"military":6,"sovereignty":5,"press_freedom":3},
  "desc":"Defend critical infrastructure from cyber attacks"},
 {"id":"r_quantum","cat":"TECH","icon":"Quantum",
  "name":"Quantum Computing Research Hub","cost":200,"rp_cost":12,"prereq":["r_ai","r_satellite"],
  "fx":{"economy":12,"education":8,"military":4},
  "desc":"Long-term: quantum encryption, computing & materials science"},
 # ── ENERGY ────────────────────────────────────────────────
 {"id":"r_battery","cat":"ENERGY","icon":"Battery",
  "name":"Domestic Battery Technology","cost":70,"rp_cost":5,"prereq":[],
  "fx":{"economy":7,"infrastructure":5,"health":2},
  "desc":"Philippine-made battery cells for EVs and grid storage"},
 {"id":"r_geothermal","cat":"ENERGY","icon":"Geothrm",
  "name":"Advanced Geothermal Research","cost":65,"rp_cost":4,"prereq":[],
  "fx":{"infrastructure":8,"economy":6,"health":3},
  "desc":"Philippines is world #2 in geothermal -- deepen this advantage"},
 {"id":"r_hydrogen","cat":"ENERGY","icon":"GrnH2",
  "name":"Green Hydrogen Programme","cost":110,"rp_cost":8,"prereq":["r_battery","r_geothermal"],
  "fx":{"economy":10,"infrastructure":7,"sovereignty":4},
  "desc":"Produce & export clean hydrogen from renewable sources"},
 # ── AGRICULTURE & FOOD ────────────────────────────────────
 {"id":"r_rice","cat":"AGRI","icon":"Rice",
  "name":"High-Yield Rice Research (IRRI)","cost":30,"rp_cost":3,"prereq":[],
  "fx":{"health":4,"inequality":-5,"economy":4},
  "desc":"Partner with IRRI for climate-resilient high-yield varieties"},
 {"id":"r_aqua","cat":"AGRI","icon":"Aquacultr",
  "name":"Aquaculture Technology","cost":45,"rp_cost":4,"prereq":["r_rice"],
  "fx":{"economy":7,"health":5,"inequality":-4},
  "desc":"Modern fish & seaweed farming -- boost blue economy"},
 {"id":"r_drought","cat":"AGRI","icon":"Drought",
  "name":"Drought-Resistant Crops","cost":50,"rp_cost":4,"prereq":["r_rice"],
  "fx":{"health":5,"inequality":-5,"economy":4},
  "desc":"Biotech crops that survive El Niño droughts & typhoon flooding"},
 # ── DEFENCE ───────────────────────────────────────────────
 {"id":"r_drone","cat":"DEFENCE","icon":"Drone",
  "name":"Unmanned Aerial Vehicle Programme","cost":85,"rp_cost":6,"prereq":[],
  "fx":{"military":10,"sovereignty":7},
  "desc":"Domestically built drones for coast guard & AFP surveillance"},
 {"id":"r_sonar","cat":"DEFENCE","icon":"Sonar",
  "name":"Underwater Sonar Network","cost":95,"rp_cost":7,"prereq":["r_drone"],
  "fx":{"military":8,"sovereignty":10,"rel_us":4},
  "desc":"Passive sonar buoys monitoring contested maritime zones"},
 # ── EDUCATION ─────────────────────────────────────────────
 {"id":"r_stem","cat":"EDUCATION","icon":"STEM",
  "name":"STEM Excellence Programme","cost":40,"rp_cost":3,"prereq":[],
  "fx":{"education":8,"economy":4,"inequality":-3},
  "desc":"Specialised STEM schools + scholarships in all regions"},
 {"id":"r_voc","cat":"EDUCATION","icon":"TESDA",
  "name":"Technical-Vocational Revolution","cost":35,"rp_cost":3,"prereq":[],
  "fx":{"education":6,"economy":7,"inequality":-5},
  "desc":"World-class TESDA programmes aligned with industry demand"},
 {"id":"r_univ_research","cat":"EDUCATION","icon":"Research",
  "name":"Research University Network","cost":75,"rp_cost":6,"prereq":["r_stem"],
  "fx":{"education":10,"economy":8,"health":3},
  "desc":"Link UP, DLSU, Ateneo & state unis into a national R&D network"},
 # ── AEROSPACE & SPACE ─────────────────────────────────────
 {"id":"r_aerospace","cat":"AEROSPACE","icon":"Aerosp",
  "name":"Philippine Aerospace Institute","cost":90,"rp_cost":7,"prereq":[],
  "fx":{"economy":8,"military":5,"education":6,"sovereignty":6},
  "desc":"Found a national aerospace institute -- aircraft MRO, drone design"},
 {"id":"r_rocket","cat":"AEROSPACE","icon":"Rocket",
  "name":"Sounding Rocket Programme","cost":130,"rp_cost":9,"prereq":["r_aerospace"],
  "fx":{"sovereignty":10,"education":7,"economy":5,"military":4},
  "desc":"First Filipino rockets -- weather, research and military applications"},
 {"id":"r_spacesat","cat":"AEROSPACE","icon":"Satellite",
  "name":"PHL-Microsat Constellation","cost":180,"rp_cost":11,"prereq":["r_rocket","r_satellite"],
  "fx":{"sovereignty":14,"economy":10,"military":8,"education":8},
  "desc":"3-satellite constellation for comms, Earth observation & maritime watch"},
 {"id":"r_spacestation","cat":"AEROSPACE","icon":"Space",
  "name":"ASEAN Space Cooperation Hub","cost":280,"rp_cost":16,"prereq":["r_spacesat"],
  "fx":{"sovereignty":18,"rel_asean":12,"economy":14,"education":12},
  "desc":"Lead ASEAN in a shared space research facility -- global prestige"},
 # ── MATERIALS & MANUFACTURING ──────────────────────────────
 {"id":"r_composite","cat":"TECH","icon":"Composit",
  "name":"Advanced Composites Lab","cost":65,"rp_cost":5,"prereq":["r_internet"],
  "fx":{"infrastructure":7,"military":5,"economy":7},
  "desc":"Carbon fibre & advanced alloys for construction, ships & aircraft"},
 {"id":"r_3dprint","cat":"TECH","icon":"3DPrint",
  "name":"Industrial 3D Printing Network","cost":55,"rp_cost":4,"prereq":[],
  "fx":{"economy":9,"infrastructure":5,"inequality":-3},
  "desc":"Localise manufacturing -- 3D-print spare parts for industry & defence"},
]

# Research point gain per month -- scales with education in monthly()
# Base rate is deliberately low to make research feel meaningful
RP_PER_MONTH = 0.8

POLICIES=[
 # ── GOVERNANCE ──────────────────────────────────────────────
 {"id":"anti_corr","name":"ANTI-CORRUPTION TASKFORCE","cost":5,
  "fx":{"corruption":-9,"sovereignty":3},"desc":"Independent anti-graft agency"},
 {"id":"merit","name":"MERITOCRACY IN GOVERNMENT","cost":4,
  "fx":{"corruption":-13,"economy":7},"desc":"Competence-based civil service hiring"},
 {"id":"natid","name":"NATIONAL ID SYSTEM","cost":5,
  "fx":{"economy":5,"corruption":-3},"desc":"Digital ID -- reduces red tape & ghost payrolls"},
 {"id":"foia","name":"FREEDOM OF INFORMATION ACT","cost":2,
  "fx":{"corruption":-7,"press_freedom":8,"public_trust":5},"desc":"Open government data to the public"},
 {"id":"ombudsman","name":"STRENGTHEN OMBUDSMAN","cost":3,
  "fx":{"corruption":-10,"public_trust":6},"desc":"Fully fund and shield the ombudsman's office"},
 {"id":"chach","name":"CHARTER CHANGE PUSH","cost":0,
  "fx":{"auth_power":16,"public_trust":-9},"desc":"High-risk constitutional amendment drive"},
 # ── SYSTEM CHANGE ────────────────────────────────────────────
 {"id":"shift_parliamentary","name":"SHIFT TO PARLIAMENTARY SYSTEM","cost":0,
  "fx":{"public_trust":-5,"economy":4,"auth_power":-8},
  "sys_change":"Parliamentary System","sys_exclude":["Parliamentary System"],
  "desc":"Transition to parliament -- PM replaces President"},
 {"id":"shift_federal","name":"SHIFT TO FEDERAL REPUBLIC","cost":0,
  "fx":{"infrastructure":6,"inequality":-4,"public_trust":-6,"budget":-200},
  "sys_change":"Federal Republic","sys_exclude":["Federal Republic"],
  "desc":"Federalize -- devolve power to regional governments"},
 {"id":"shift_presidential","name":"RESTORE PRESIDENTIAL REPUBLIC","cost":0,
  "fx":{"public_trust":7,"sovereignty":5,"auth_power":-15},
  "sys_change":"Presidential Republic","sys_exclude":["Presidential Republic"],
  "desc":"Return to a directly-elected presidential republic"},
 # ── ECONOMY ─────────────────────────────────────────────────
 {"id":"ubi","name":"UNIVERSAL BASIC INCOME","cost":12,
  "fx":{"inequality":-9,"public_trust":7},"desc":"Direct monthly cash transfers to poorest 20%"},
 {"id":"free_uni","name":"FREE STATE UNIVERSITY","cost":10,
  "fx":{"education":13,"public_trust":7},"desc":"Tuition-free state colleges & universities"},
 {"id":"sme_loans","name":"SME LENDING PROGRAM","cost":6,
  "fx":{"economy":8,"inequality":-4},"desc":"Low-interest loans for small & medium enterprises"},
 {"id":"export_zone","name":"EXPORT PROCESSING ZONES","cost":8,
  "fx":{"economy":11,"sovereignty":-3,"inequality":-3},"desc":"Dedicated manufacturing corridors for exports"},
 {"id":"tourism","name":"NATIONAL TOURISM PUSH","cost":5,
  "fx":{"economy":7,"infrastructure":3,"rel_asean":3},"desc":"Brand & market PH destinations globally"},
 {"id":"asean_trade","name":"ASEAN FREE TRADE DEEPENING","cost":4,
  "fx":{"economy":8,"rel_asean":10,"inequality":-3},"desc":"Eliminate remaining tariff barriers within ASEAN"},
 # ── SOCIAL ──────────────────────────────────────────────────
 {"id":"housing","name":"NATIONAL HOUSING PROGRAM","cost":15,
  "fx":{"inequality":-11,"public_trust":9,"infrastructure":5},"desc":"Mass socialized housing for urban poor"},
 {"id":"agrarian","name":"AGRARIAN REFORM EXTENSION","cost":6,
  "fx":{"inequality":-9,"public_trust":5},"desc":"Accelerate land redistribution under CARP"},
 {"id":"4ps_expand","name":"EXPAND CONDITIONAL CASH TRANSFERS","cost":9,
  "fx":{"inequality":-7,"health":5,"education":4},"desc":"Bigger 4Ps -- health & school conditionalities"},
 {"id":"senior_care","name":"SENIOR CITIZENS CARE PROGRAM","cost":5,
  "fx":{"health":6,"public_trust":6},"desc":"Pension top-up + free medicines for the elderly"},
 {"id":"pwd_rights","name":"PWD RIGHTS & EMPLOYMENT ACT","cost":3,
  "fx":{"inequality":-4,"public_trust":5},"desc":"Enforce disability rights & work incentives"},
 # ── HEALTH ──────────────────────────────────────────────────
 {"id":"univ_health","name":"UNIVERSAL HEALTH CARE","cost":14,
  "fx":{"health":15,"public_trust":10},"desc":"Full PhilHealth coverage for all Filipinos"},
 {"id":"drug_rehab","name":"MANDATORY DRUG REHAB","cost":4,
  "fx":{"health":5,"public_trust":3},"desc":"Treatment-first approach to substance abuse"},
 {"id":"mental_health","name":"MENTAL HEALTH AWARENESS PROGRAM","cost":4,
  "fx":{"health":6,"education":3,"public_trust":4},"desc":"Community mental health centres & hotlines"},
 # ── PRESS / CIVIL LIBERTIES ─────────────────────────────────
 {"id":"media_ch","name":"MEDIA FREEDOM CHARTER","cost":2,
  "fx":{"press_freedom":11,"rel_un":5},"desc":"Statutory protections for journalists"},
 {"id":"cyber_crime","name":"CYBERCRIME LAW REFORM","cost":2,
  "fx":{"press_freedom":6,"economy":3},"desc":"Remove online libel provisions targeting speech"},
 # ── TRANSPORT ────────────────────────────────────────────────
 {"id":"tr_mrt_expand","name":"MRT/LRT METRO EXPANSION","cost":16,
  "fx":{"infrastructure":11,"economy":7,"inequality":-4},"desc":"New LRT/MRT lines & stations across Metro Manila"},
 {"id":"tr_rail_luzon","name":"NORTH-SOUTH COMMUTER RAILWAY","cost":18,
  "fx":{"infrastructure":13,"economy":8,"inequality":-3},"desc":"Fast rail linking Metro Manila to Luzon provinces"},
 {"id":"tr_rail_mindanao","name":"MINDANAO RAILWAY","cost":14,
  "fx":{"infrastructure":11,"inequality":-6,"economy":5},"desc":"Freight & passenger rail across Mindanao"},
 {"id":"tr_expressway","name":"NATIONAL EXPRESSWAY NETWORK","cost":16,
  "fx":{"infrastructure":13,"economy":7,"inequality":-5},"desc":"4-lane toll-free expressways linking all regions"},
 {"id":"tr_ferry","name":"INTER-ISLAND FERRY NETWORK","cost":9,
  "fx":{"infrastructure":8,"economy":5,"inequality":-4},"desc":"Subsidised RoRo ferry routes -- Visayas & Mindanao"},
 {"id":"tr_airport","name":"NEW REGIONAL AIRPORTS","cost":12,
  "fx":{"infrastructure":9,"economy":8,"rel_asean":3},"desc":"Upgrade & build airports in underserved provinces"},
 {"id":"tr_seaport","name":"MAJOR SEAPORT MODERNISATION","cost":11,
  "fx":{"economy":9,"infrastructure":8,"sovereignty":3},"desc":"Upgrade Cebu, Davao & Manila international ports"},
 {"id":"tr_ev_infra","name":"EV CHARGING NETWORK","cost":7,
  "fx":{"infrastructure":5,"economy":4,"health":3},"desc":"Nationwide EV charging stations; reduce emissions"},
 # ── LIVING STANDARDS ─────────────────────────────────────────
 {"id":"ls_water","name":"UNIVERSAL CLEAN WATER ACCESS","cost":11,
  "fx":{"health":10,"inequality":-7,"public_trust":7},"desc":"Piped clean water to all barangays by 2035"},
 {"id":"ls_sanitation","name":"NATIONAL SANITATION PROGRAMME","cost":8,
  "fx":{"health":8,"inequality":-5,"public_trust":5},"desc":"Sewerage, waste management & toilet access"},
 {"id":"ls_electricity","name":"UNIVERSAL ELECTRICITY ACCESS","cost":10,
  "fx":{"infrastructure":8,"inequality":-6,"economy":5},"desc":"Off-grid solar for remote islands & upland communities"},
 {"id":"ls_internet","name":"FREE PUBLIC WIFI ZONES","cost":5,
  "fx":{"education":5,"economy":4,"inequality":-3},"desc":"Free wifi in parks, libraries & public markets"},
 {"id":"ls_market","name":"KADIWA PEOPLES MARKET NETWORK","cost":6,
  "fx":{"inequality":-7,"health":4,"economy":4},"desc":"Government-subsidised markets to lower food prices"},
 {"id":"ls_slum","name":"URBAN RENEWAL PROGRAMME","cost":13,
  "fx":{"infrastructure":9,"inequality":-8,"public_trust":7},"desc":"Upgrade informal settlements with relocation & jobs"},
 # ── MILITARY / SECURITY ─────────────────────────────────────
 {"id":"coast","name":"COAST GUARD EXPANSION","cost":8,
  "fx":{"military":8,"sovereignty":7},"desc":"More vessels & stations across the EEZ"},
 {"id":"afp_modern","name":"AFP MODERNIZATION PHASE III","cost":16,
  "fx":{"military":14,"sovereignty":6},"desc":"New jets, frigates & cyber-defence units"},
 {"id":"wps_patrol","name":"WPS JOINT MARITIME PATROL","cost":6,
  "fx":{"sovereignty":9,"military":5,"rel_china":-7},
  "stance":["SOBERANIYA","BALANSE"],"desc":"Regular patrols with allied navies in disputed waters"},
 {"id":"iron","name":"IRON FIST CAMPAIGN","cost":3,
  "fx":{"military":9,"press_freedom":-11,"auth_power":13},
  "sys":["Benevolent Authoritarianism","Authoritarian Dictatorship"],
  "desc":"Harsh crackdown on crime & political opponents"},
 # ── FOREIGN POLICY ──────────────────────────────────────────
 {"id":"china_deal","name":"CHINA INFRASTRUCTURE DEAL","cost":0,
  "fx":{"infrastructure":13,"sovereignty":-11,"debt":300},
  "stance":["PAKIKIPAG-UGNAYAN","BALANSE"],"desc":"BRI-style loan -- rail & ports with sovereignty strings"},
 {"id":"us_base","name":"US MILITARY BASE RENEWAL","cost":3,
  "fx":{"military":9,"rel_china":-9},
  "stance":["ALYANSA","BALANSE"],"desc":"Renew EDCA bases for US military presence"},
 {"id":"mining_reform","name":"RESPONSIBLE MINING ACT","cost":3,
  "fx":{"economy":5,"health":4,"sovereignty":4},"desc":"Regulate extraction; protect ancestral domains"},
 # ── INFRASTRUCTURE ───────────────────────────────────────────
 {"id":"disaster","name":"DISASTER RESILIENCE FUND","cost":7,
  "fx":{"infrastructure":4},"desc":"Pre-positioned stockpiles & early-warning systems"},
 {"id":"fiber","name":"NATIONWIDE FIBER INTERNET","cost":9,
  "fx":{"economy":7,"education":5},"desc":"Universal broadband connectivity by 2030"},
 {"id":"flood_ctrl","name":"METRO FLOOD CONTROL MASTER PLAN","cost":11,
  "fx":{"infrastructure":8,"health":4,"public_trust":6},"desc":"Dredge & widen major waterways; build retention basins"},
 {"id":"rail_luzon","name":"NORTH-SOUTH COMMUTER RAILWAY","cost":18,
  "fx":{"infrastructure":13,"economy":7,"inequality":-3},"desc":"Fast rail linking Metro Manila to provinces"},
 {"id":"rail_mindanao","name":"MINDANAO RAILWAY PROJECT","cost":14,
  "fx":{"infrastructure":11,"inequality":-6,"economy":5},"desc":"Freight & passenger rail across Mindanao"},
 {"id":"highway_net","name":"NATIONAL HIGHWAY NETWORK","cost":16,
  "fx":{"infrastructure":13,"economy":7,"inequality":-5},"desc":"4-lane expressways linking all major islands & provinces"},
 {"id":"interisland","name":"INTER-ISLAND FERRY NETWORK","cost":9,
  "fx":{"infrastructure":8,"economy":5,"inequality":-4},"desc":"Subsidised RoRo ferry routes -- Visayas & Mindanao"},
 {"id":"seaport","name":"MAJOR SEAPORT MODERNISATION","cost":11,
  "fx":{"economy":9,"infrastructure":8,"sovereignty":3},"desc":"Upgrade Cebu, Davao & Manila international ports"},
 {"id":"smart_grid","name":"NATIONAL SMART POWER GRID","cost":12,
  "fx":{"infrastructure":10,"economy":8},"desc":"Modernise electricity grid -- reduce brownouts nationwide"},
 {"id":"solar_energy","name":"RENEWABLE ENERGY PROGRAM","cost":10,
  "fx":{"infrastructure":7,"economy":5,"health":3},"desc":"Solar & wind farms across Luzon, Visayas, Mindanao"},
 {"id":"nuclear","name":"NUCLEAR POWER PLANT","cost":28,
  "fx":{"economy":14,"infrastructure":11,"health":-5},
  "high_risk_infra":True,
  "desc":"! HIGH RISK if infrastructure < 45 or corruption > 60 -- massive power boost"},
 {"id":"dike_system","name":"NATIONAL DIKE & SEAWALL SYSTEM","cost":10,
  "fx":{"infrastructure":7,"health":4,"sovereignty":4},"desc":"Coastal flood defences for vulnerable provinces"},
 # ── MANUFACTURING ────────────────────────────────────────────
 {"id":"shipyard","name":"NATIONAL SHIPBUILDING INDUSTRY","cost":18,
  "fx":{"economy":11,"military":6,"infrastructure":5},"desc":"State shipyards for commercial & naval vessels"},
 {"id":"semiconductor","name":"SEMICONDUCTOR FABRICATION PLANT","cost":20,
  "fx":{"economy":15,"education":5,"inequality":-4},"desc":"High-tech chip fabs -- follow the Asian tiger model"},
 {"id":"computer_hardware","name":"COMPUTER HARDWARE ASSEMBLY ZONE","cost":12,
  "fx":{"economy":10,"education":4,"inequality":-3},"desc":"Electronics assembly & component manufacturing"},
 {"id":"gold_process","name":"GOLD PROCESSING & REFINERY","cost":8,
  "fx":{"economy":9,"sovereignty":4,"rel_asean":3},"desc":"Refine gold domestically rather than export raw ore"},
 {"id":"steel_mill","name":"INTEGRATED STEEL MILL","cost":16,
  "fx":{"economy":10,"infrastructure":6},"desc":"Domestic steel production to cut import dependency"},
 {"id":"pharma","name":"LOCAL PHARMACEUTICAL INDUSTRY","cost":10,
  "fx":{"economy":7,"health":8,"inequality":-4},"desc":"Manufacture generic medicines domestically"},
 {"id":"food_processing","name":"AGRI-FOOD PROCESSING ZONES","cost":9,
  "fx":{"economy":8,"inequality":-6,"health":4},"desc":"Value-added processing hubs for rice, coconut & sugar"},
 {"id":"auto_ev","name":"ELECTRIC VEHICLE ASSEMBLY ZONE","cost":11,
  "fx":{"economy":9,"infrastructure":4},"desc":"Attract EV manufacturers; green industrialisation"},
 {"id":"bpo_upgrade","name":"BPO SECTOR UPGRADE","cost":7,
  "fx":{"economy":9,"education":4},"desc":"Upskill BPO workforce for AI & higher-value services"},
 # ── RESEARCH INVESTMENT ──────────────────────────────────────
 {"id":"research_lab","name":"NATIONAL RESEARCH INVESTMENT","cost":8,
  "fx":{"education":4,"economy":3},"desc":"Funds R&D -- earns Research Points each month to unlock tech tree"},
]

class PolicyManager:
    def available(self,gs):
        out=[]
        for p in POLICIES:
            if "stance" in p and gs.foreign_stance not in p["stance"]: continue
            if "sys" in p and gs.political_system not in p["sys"]: continue
            if "sys_exclude" in p and gs.political_system in p["sys_exclude"]: continue
            out.append(p)
        return out

    def toggle(self,gs,pid):
        maxp=4 if gs.difficulty=="PANGULO" else 6
        p=next((x for x in POLICIES if x["id"]==pid),None)
        if not p: return "err"
        if "sys_change" in p:
            new_sys=p["sys_change"]
            if gs.political_system==new_sys: return "same"
            old_sys=gs.political_system
            gs.political_system=new_sys
            for stat,d in p.get("fx",{}).items():
                if stat in("budget","debt"): setattr(gs,stat,getattr(gs,stat)+d)
                elif hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
            if new_sys not in AUTH_SYSTEMS:
                gs.active_policies=[x for x in gs.active_policies
                                     if not next((q for q in POLICIES if q["id"]==x and "sys" in q),None)]
            gs.clamp()
            gs.log(f"SYS System changed: {old_sys} >> {new_sys}")
            return f"system_changed:{new_sys}"
        if pid in gs.active_policies: gs.active_policies.remove(pid); return "off"
        if len(gs.active_policies)>=maxp: return f"max{maxp}"
        gs.active_policies.append(pid); return "on"

    def monthly(self,gs):
        """Apply active-policy effects EVERY month:
        - Cost deducted at annual_cost × P10B / 12
        - Stat effects applied at 1/12 of annual value per month
        Players can freely change active policies each month before pressing Next.
        """
        for pid in list(gs.active_policies):
            p=next((x for x in POLICIES if x["id"]==pid),None)
            if not p: continue
            # Monthly cost deduction
            gs.budget -= p["cost"] * 10 / 12
            # Monthly stat gains (1/12 of full annual fx value)
            for stat, d in p["fx"].items():
                if stat == "debt":
                    gs.debt += d / 12
                elif stat in ("economy2","rp_gain"):
                    pass
                elif hasattr(gs, stat):
                    setattr(gs, stat, getattr(gs, stat) + d / 12)
            # Nuclear risk check once per year
            if pid == "nuclear" and gs.month == 12:
                if gs.infrastructure < 45 or gs.corruption > 60:
                    if random.random() < 0.22:
                        gs.health -= 18; gs.public_trust -= 22; gs.infrastructure -= 14
                        gs.log("NUC NUCLEAR INCIDENT -- poor infra/corruption caused a malfunction!")
        # Research: accumulate RP monthly based on education stat + active policies
        rp_gain = RP_PER_MONTH * (0.5 + gs.education/100.0)
        if "research_lab" in gs.active_policies:
            rp_gain *= 2.0
        if "free_uni" in gs.active_policies:
            rp_gain *= 1.4
        if "r_stem" in getattr(gs,"research_unlocked",[]):
            rp_gain *= 1.2
        gs.research_points = getattr(gs,"research_points",0) + rp_gain
        gs.clamp()

    def annual(self,gs):
        """Year-end: check research tier milestones."""
        rp = getattr(gs,"research_points",0)
        tier = int(rp // 10)
        if tier > getattr(gs,"research_tier",0):
            gs.research_tier = tier
            gs.economy += 2; gs.health += 2; gs.education += 2
            gs.log(f"RP Research milestone {tier} -- economy, health & education +2")

class BudgetManager:
    def revenue(self,gs):
        base=4400*(gs.economy/50)
        if gs.political_system=="Benevolent Authoritarianism": base*=1.12
        elif gs.political_system=="Authoritarian Dictatorship": base*=0.82
        return base

    def year_end(self,gs):
        """Year-end budget reconciliation: add annual revenue, subtract base expenses.
        Policy costs are already deducted monthly, so we only do non-policy expenses here."""
        rev=self.revenue(gs)
        base_exp=3800+gs.debt*0.055
        gs.budget+=rev-base_exp
        if gs.budget<-3000: gs.flags["economic_collapse"]=True
        if gs.budget<0: gs.log(f"! Deficit: P{abs(gs.budget):.0f}B")

# ── MAP DATA -- proper 1:1 geo-projection ────────────────────
# Panel: x 0-710, y 42-652. Real PH: lat 4.5-21°N, lon 116-127°E
# x=(lon-116)/(127-116)*(650-55)+55  y=(21-lat)/(21-4.5)*(600-50)+50
MAP_DATA={
 "Luzon":{"poly":[
    (239,50),(265,46),(290,57),(303,92),(316,130),(313,164),
    (302,190),(290,220),(274,238),(258,230),(244,212),(236,198),
    (229,180),(221,168),(214,148),(209,126),(203,106),(206,86),
    (216,66),(228,53),
 ],"col":(30,70,175),"ctr":(258,144)},
 "NCR":{"poly":[
    (225,176),(236,173),(240,191),(227,195)
 ],"col":(20,110,200),"ctr":(234,184)},
 "Palawan":{"poly":[
    (133,228),(148,220),(157,234),(150,258),(138,282),(125,308),
    (110,330),(97,348),(87,358),(80,366),(75,350),(84,332),
    (96,314),(108,292),(120,268),(128,244),(131,230),
 ],"col":(30,70,175),"ctr":(117,290)},
 "Visayas":{"poly":[
    (218,260),(250,250),(271,256),(287,252),(308,258),(324,266),
    (337,282),(349,294),(356,312),(348,334),(334,346),(316,356),
    (296,362),(276,354),(256,342),(236,328),(220,310),(206,294),
    (204,274),
 ],"col":(220,170,0),"ctr":(278,302)},
 "Mindanao":{"poly":[
    (189,382),(210,371),(234,364),(258,360),(282,358),(305,362),
    (323,372),(330,396),(328,416),(316,438),(302,454),(284,466),
    (264,472),(243,468),(222,460),(200,450),(180,440),(162,428),
    (150,414),(144,398),(154,384),(174,378),
 ],"col":(140,72,18),"ctr":(240,414)},
}
REGION_STATS={
 "Luzon"    :{"GDP%":"35%","Typhoon":"High","Rebels":"Low","Infra":72,"Poverty%":"18%"},
 "NCR"      :{"GDP%":"38%","Typhoon":"Medium","Rebels":"None","Infra":80,"Poverty%":"13%"},
 "Visayas"  :{"GDP%":"15%","Typhoon":"V.High","Rebels":"Low","Infra":55,"Poverty%":"32%"},
 "Mindanao" :{"GDP%":"18%","Typhoon":"Medium","Rebels":"High","Infra":44,"Poverty%":"38%"},
 "Palawan"  :{"GDP%":"4%","Typhoon":"Low","Rebels":"Low","Infra":39,"Poverty%":"28%"},
}

# ── ACHIEVEMENTS ─────────────────────────────────────────────
ACHIEVEMENTS = [
    {"id":"golden_age",
     "name":"Golden Age","name_en":"Golden Age","icon":"Trophy",
     "desc":"Economy, Edukasyon, Kalusugan, at Imprastraktura ay higit sa 80 nang sabay",
     "desc_en":"Economy, Education, Health, and Infrastructure all exceed 80 simultaneously",
     "check": lambda gs: gs.economy>80 and gs.education>80 and gs.health>80 and gs.infrastructure>80},
    {"id":"coup_taken",
     "name":"Kinuha ng Kudeta","name_en":"Taken by a Coup","icon":"Sword",
     "desc":"Natalo sa kudeta ng heneral",
     "desc_en":"Removed from power by a military coup",
     "check": lambda gs: gs.flags.get("coup_overthrow",False)},
    {"id":"good_dictator",
     "name":"Ang Mabuting Diktador","name_en":"The Good Dictator","icon":"Crown",
     "desc":"Naging diktador sa pamamagitan ng dayaang halalan -- ngunit pinamahalaan ng tama ang bansa (Corruption < 20, Economy > 75)",
     "desc_en":"Became dictator by rigging an election -- but governed with integrity (Corruption < 20, Economy > 75, term complete)",
     "check": lambda gs: gs.flags.get("rigged_election",False) and gs.political_system in("Benevolent Authoritarianism","Authoritarian Dictatorship") and gs.corruption<20 and gs.economy>75 and gs.year>=2031},
    {"id":"plunderer",
     "name":"Ang Nagnakaw na Diktador","name_en":"The Dictator Who Plundered","icon":"Gold",
     "desc":"Ang Corruption ay higit sa 85 habang nasa Authoritarian Dictatorship",
     "desc_en":"Corruption exceeded 85 while ruling as an Authoritarian Dictator",
     "check": lambda gs: gs.political_system=="Authoritarian Dictatorship" and gs.corruption>85},
    {"id":"dying_for",
     "name":"Isang Pilipinas na Karapat-dapat Ipaglaban","name_en":"A Philippines Worth Dying For","icon":"PHL",
     "desc":"Lahat ng pangunahing istatistika ay higit sa 75 -- Golden Age at malinis ang gobyerno",
     "desc_en":"All major stats above 75 and corruption below 25 -- a Golden Age achieved",
     "check": lambda gs: all(getattr(gs,s,0)>75 for s in ["economy","health","education","infrastructure","sovereignty","public_trust"]) and gs.corruption<25 and (100-gs.inequality)>75},
    {"id":"people_power",
     "name":"Isa pang People Power","name_en":"Another People Power","icon":"Fist",
     "desc":"Approval nahulog sa ibaba ng 15% ngunit naiwasan ang impeachment sa mass mobilisation",
     "desc_en":"Approval fell below 15% but impeachment was averted through mass mobilisation",
     "check": lambda gs: gs.flags.get("people_power_triggered",False)},
]

class AchievementManager:
    def __init__(self):
        self.unlocked = set()
        self.new_unlocks = []   # queue for popup display
        self._popup_timer = 0
        self._popup_current = None

    def check(self, gs):
        """Check all achievements and queue any newly unlocked ones."""
        for ach in ACHIEVEMENTS:
            if ach["id"] not in self.unlocked:
                try:
                    if ach["check"](gs):
                        self.unlocked.add(ach["id"])
                        self.new_unlocks.append(ach)
                        gs.log(f"🏅 Achievement: {ach['name_en']}")
                except Exception:
                    pass

    def upd(self):
        """Advance popup timer."""
        if self._popup_timer > 0:
            self._popup_timer -= 1
            if self._popup_timer == 0:
                self._popup_current = None
        if self._popup_current is None and self.new_unlocks:
            self._popup_current = self.new_unlocks.pop(0)
            self._popup_timer = 240  # 4 seconds @ 60fps

    def draw(self, surf):
        """Draw achievement popup toast in top-right."""
        if not self._popup_current: return
        ach = self._popup_current
        t = self._popup_timer
        # Fade in first 20 frames, fade out last 40
        if t > 220: alpha = int(255*(240-t)/20)
        elif t < 40: alpha = int(255*t/40)
        else: alpha = 255
        if alpha <= 0: return
        pw,ph = 380,80
        px,py = W-pw-10, 50
        toast = pygame.Surface((pw,ph), pygame.SRCALPHA)
        toast.fill((10,28,60,min(220,alpha)))
        pygame.draw.rect(toast,(255,215,0,alpha),(0,0,pw,ph),2,border_radius=10)
        icon_s = F["h2"].render("*", True, (255,255,255,alpha))
        toast.blit(icon_s, (10, ph//2-icon_s.get_height()//2))
        tag_s = F["sm"].render("ACHIEVEMENT UNLOCKED" if LANG=="ENG" else "NAKAMIT!", True, (255,215,0,alpha))
        toast.blit(tag_s, (50, 8))
        name_key = "name_en" if LANG=="ENG" else "name"
        name_s = F["bd"].render(ach[name_key], True, (255,255,255,alpha))
        toast.blit(name_s, (50, 26))
        desc_key = "desc_en" if LANG=="ENG" else "desc"
        for j,ln in enumerate(wrap(ach[desc_key], F["sm"], pw-60)[:2]):
            ds = F["sm"].render(ln, True, (180,180,200,alpha))
            toast.blit(ds, (50, 48+j*16))
        surf.blit(toast, (px,py))

def pt_in_poly(x,y,poly):
    inside=False; j=len(poly)-1
    for i in range(len(poly)):
        xi,yi=poly[i]; xj,yj=poly[j]
        if((yi>y)!=(yj>y))and(x<(xj-xi)*(y-yi)/(yj-yi)+xi): inside=not inside
        j=i
    return inside


# Module-level click-sound hook (set by main() after pygame.mixer init)
_CLICK_SND = None
def _play_click():
    if _CLICK_SND:
        try: _CLICK_SND.play()
        except: pass

class Btn:
    def __init__(self,x,y,w,h,lbl,base=None,tc=None,fk="h2",on=True):
        self.r=pygame.Rect(x,y,w,h); self.lbl=lbl
        self.base=base or C_PAN; self.tc=tc or C_GOLD; self.fk=fk
        self.hov=False; self.on=on

    def upd(self,mx,my): self.hov=self.r.collidepoint(mx,my) and self.on

    def draw(self,surf):
        col=lc(self.base,(min(255,self.base[0]+55),min(255,self.base[1]+55),min(255,self.base[2]+55)),0.45 if self.hov else 0)
        if not self.on: col=(28,28,44)
        pygame.draw.rect(surf,col,self.r,border_radius=7)
        pygame.draw.rect(surf,C_GOLD if self.hov else C_GD,self.r,2,border_radius=7)
        fn=F.get(self.fk,F["bd"]); tc=self.tc if self.on else C_GRY
        s=fn.render(self.lbl,True,tc)
        surf.blit(s,(self.r.centerx-s.get_width()//2,self.r.centery-s.get_height()//2))

    def clicked(self,ev):
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self.r.collidepoint(ev.pos) and self.on:
            _play_click()
            return True
        return False


class Ticker:
    def __init__(self,y=690,h=28):
        self.y=y; self.h=h; self.x=W
        self._base=[]      # base messages in current lang (no user additions)
        self._extra=[]     # dynamically added in-game messages
        self.refresh_lang()

    def refresh_lang(self):
        """Re-load base messages for the current LANG. Keeps any extra msgs."""
        self._base = list(STRINGS["ticker_msgs"].get(LANG, STRINGS["ticker_msgs"]["ENG"]))
        self._rebuild()

    def _all_msgs(self):
        return self._base + self._extra

    def _rebuild(self):
        msgs=self._all_msgs()
        txt="  ✦  ".join(msgs[-15:])+"  ✦  "
        self._s=F["tk"].render(txt,True,C_GOLD); self._w=self._s.get_width()

    def add(self,m):
        self._extra.append(m)
        if len(self._extra)>25: self._extra=self._extra[-25:]
        self._rebuild(); self.x=W

    def upd(self):
        self.x-=2
        if self.x<-self._w: self.x=W

    def draw(self,surf):
        pygame.draw.rect(surf,(4,12,28),(0,self.y,W,self.h))
        pygame.draw.line(surf,C_GD,(0,self.y),(W,self.y),1)
        surf.blit(self._s,(self.x,self.y+self.h//2-self._s.get_height()//2))

class EventCard:
    CW,CH=510,450
    def __init__(self): self.active=False; self.ev=None; self.result=None; self.slide=W; self.btns=[]; self.close=None; self.cb=None

    def show(self,ev,cb=None): self.ev=ev; self.active=True; self.result=None; self.slide=W; self.cb=cb; self._build()

    def _build(self):
        cx=W-self.CW; cy=(H-self.CH)//2
        self.btns=[]
        for i,c in enumerate(self.ev.get("choices",[])[:4]):
            lbl,_=EC_T(c)
            b=Btn(cx+10,cy+210+i*54,self.CW-20,46,lbl,fk="bd")
            self.btns.append((b,c))
        self.close=Btn(cx+self.CW//2-60,cy+self.CH-42,120,34,T("close_btn"),fk="sm")

    def rebuild_lang(self):
        """Rebuild button labels when language changes."""
        if self.ev: self._build()

    def upd(self,mx,my):
        if not self.active: return
        self.slide=lerp(self.slide,W-self.CW+4,0.14)
        for b,_ in self.btns: b.r.x=int(self.slide)+10; b.upd(mx,my)
        if self.close: self.close.r.x=int(self.slide)+self.CW//2-60; self.close.upd(mx,my)

    def handle(self,ev,gs):
        if not self.active: return False
        if self.result and self.close and self.close.clicked(ev):
            self.active=False
            return True
        for btn,ch in self.btns:
            if btn.clicked(ev):
                for stat,d in ch.get("fx",{}).items():
                    if stat=="budget": gs.budget+=d
                    elif stat=="debt": gs.debt+=d
                    elif stat=="rigged_election": gs.flags["rigged_election"]=True
                    elif stat=="coup_overthrow_risk": gs.flags["coup_overthrow_risk"]=True
                    elif hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                gs.clamp()
                self.result=" | ".join(f"{k}:{'+' if v>0 else ''}{v}" for k,v in ch["fx"].items() if isinstance(v,(int,float)) and k not in("budget","debt"))[:60]
                gs.log(f"{self.ev['title']}: {ch['lbl']}")
                if self.cb: self.cb(ch["lbl"])
                return True
        return False

    def draw(self,surf):
        if not self.active or not self.ev: return
        cx=int(self.slide); cy=(H-self.CH)//2
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,110)); surf.blit(ov,(0,0))
        pygame.draw.rect(surf,(11,26,52),(cx,cy,self.CW,self.CH),border_radius=10)
        pygame.draw.rect(surf,C_GOLD,(cx,cy,self.CW,self.CH),2,border_radius=10)
        CAT_C={"CORRUPTION":C_RED,"WPS":(0,90,200),"ECONOMY":(0,170,80),"MILITARY":(200,110,0),"AUTHORITARIAN":(160,0,200),"HEALTH":(0,180,180),"DISASTER":(200,130,0),"SECURITY":(140,60,0)}
        cc=CAT_C.get(self.ev.get("cat",""),C_GRY)
        pygame.draw.rect(surf,cc,(cx+10,cy+10,110,22),border_radius=5)
        surf.blit(F["sm"].render(self.ev.get("cat",""),True,C_WHT),(cx+14,cy+13))
        title=E_T(self.ev,"title")
        surf.blit(F["h1"].render(title,True,C_GOLD),(cx+10,cy+40))
        flavor=E_T(self.ev,"flavor")
        lines=wrap(flavor,F["bd"],self.CW-20)
        for i,ln in enumerate(lines[:4]): surf.blit(F["bd"].render(ln,True,C_WHT),(cx+10,cy+80+i*22))
        pygame.draw.line(surf,C_GD,(cx+10,cy+198),(cx+self.CW-10,cy+198),1)
        if self.result:
            s=F["bd"].render(("Result: " if LANG=="ENG" else "Resulta: ")+self.result,True,C_GRN); surf.blit(s,(cx+10,cy+204))
            if self.close: self.close.draw(surf)
        else:
            for btn,ch in self.btns:
                _,desc=EC_T(ch)
                btn.lbl,_=EC_T(ch)   # keep label fresh for language
                btn.draw(surf)
                if desc:
                    ds=F["sm"].render(desc,True,C_GRY)
                    surf.blit(ds,(btn.r.right+4,btn.r.centery-ds.get_height()//2))

SPLASH_ENABLED = True   # can be toggled in settings

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd(), 'republika_settings.json')

def load_settings():
    global LANG, SPLASH_ENABLED
    try:
        d=json.load(open(SETTINGS_PATH))
        LANG=d.get('lang','FIL')
        SPLASH_ENABLED=d.get('splash',True)
    except: pass

def save_settings():
    try:
        json.dump({'lang':LANG,'splash':SPLASH_ENABLED},open(SETTINGS_PATH,'w'))
    except: pass

load_settings()

# ── SPLASH SCREEN -- Ramon Magsaysay quote ────────────────────
class SplashScreen:
    """Black screen: quote fades in, holds, then fades out >> triggers menu."""
    QUOTE  = "\u201cHe who has less in life should have more in law.\u201d"
    ATTRIB = "-- Ramon Magsaysay  \u2022  \u201cChampion of the Masses\u201d  \u2022  (1907\u20131957)"
    FADE_IN  = 90
    HOLD     = 160
    FADE_OUT = 90

    def __init__(self):
        self._frame = 0
        self._done  = False

    @property
    def done(self): return self._done or not SPLASH_ENABLED

    def _alpha(self):
        f = self._frame
        total_in  = self.FADE_IN
        total_mid = total_in + self.HOLD
        total_out = total_mid + self.FADE_OUT
        if f < total_in:
            return int(255 * f / self.FADE_IN)
        if f < total_mid:
            return 255
        if f < total_out:
            return int(255 * (1 - (f - total_mid) / self.FADE_OUT))
        return 0

    def update(self):
        self._frame += 1
        if self._frame >= self.FADE_IN + self.HOLD + self.FADE_OUT:
            self._done = True

    def draw(self, surf):
        surf.fill(C_BLK)
        alpha = self._alpha()
        if alpha <= 0: return

        # Decorative thin horizontal rule above and below quote
        rule_y1, rule_y2 = 250, 460
        rule_col = (alpha, alpha, alpha)
        line_len  = 420
        pygame.draw.line(surf, rule_col,
                         (W//2 - line_len//2, rule_y1),
                         (W//2 + line_len//2, rule_y1), 1)
        pygame.draw.line(surf, rule_col,
                         (W//2 - line_len//2, rule_y2),
                         (W//2 + line_len//2, rule_y2), 1)

        # Small decorative star / sun motif
        star_alpha = max(0, alpha - 60)
        if star_alpha > 0:
            star_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            star_surf.fill((0,0,0,0))
            sa = star_alpha
            pygame.draw.circle(star_surf, (sa, sa*220//255, 0, sa), (40,40), 12)
            for i in range(8):
                a = math.pi*2*i/8 - math.pi/2
                pygame.draw.line(star_surf, (sa, sa*220//255, 0, sa),
                                 (40+int(math.cos(a)*14), 40+int(math.sin(a)*14)),
                                 (40+int(math.cos(a)*28), 40+int(math.sin(a)*28)), 2)
            surf.blit(star_surf, (W//2-40, rule_y1-54))

        # Quote line -- wrap if needed
        font_q = F.get("quote_lg", F["h1"])
        font_a = F.get("quote_sm", F["bd"])

        # Measure and possibly reduce font size by wrapping
        lines = wrap(self.QUOTE, font_q, 900)
        q_y = 280
        for ln in lines:
            qs = font_q.render(ln, True, (alpha, alpha, alpha))
            qs.set_alpha(alpha)
            surf.blit(qs, (W//2 - qs.get_width()//2, q_y))
            q_y += qs.get_height() + 8

        # Attribution
        a_surf = font_a.render(self.ATTRIB, True, (alpha*160//255, alpha*160//255, alpha*160//255))
        a_surf.set_alpha(alpha)
        surf.blit(a_surf, (W//2 - a_surf.get_width()//2, q_y + 28))

    def handle(self, ev):
        """Skip on any key or click."""
        if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._done = True

# ── SCREENS ──────────────────────────────────────────────────
class SettingsScreen:
    """Simple settings overlay: splash quote toggle, language, volume stub."""
    def __init__(self):
        self.back=Btn(40,40,140,38,"<- BACK" if LANG=="ENG" else "<- BUMALIK",fk="bd")
        self.splash_btn=Btn(440,260,400,54,"")
        self.lang_btn  =Btn(440,330,400,54,"")
        self._refresh()

    def _refresh(self):
        self.back.lbl="<- BACK" if LANG=="ENG" else "<- BUMALIK"
        self.splash_btn.lbl=(
            ("+ Intro Quote: ON  (click to disable)" if SPLASH_ENABLED else "- Intro Quote: OFF (click to enable)")
            if LANG=="ENG" else
            ("+ Intro Quote: BUKAS  (i-click para isara)" if SPLASH_ENABLED else "- Intro Quote: SARADO (i-click para buksan)")
        )
        self.lang_btn.lbl=f"LANG Language / Wika: {'ENGLISH' if LANG=='ENG' else 'FILIPINO'}"

    def draw(self,surf,mx,my):
        global LANG
        gbg(surf)
        self.back.upd(mx,my); self.splash_btn.upd(mx,my); self.lang_btn.upd(mx,my)
        self._refresh()
        title="SETTINGS" if LANG=="ENG" else "MGA SETTING"
        blit_c(surf,title,F["h1"],C_GOLD,150,shad=True)
        pygame.draw.line(surf,C_GD,(440,230),(840,230),1)
        # Magsaysay quote preview
        qprev=SplashScreen.QUOTE[:60]+"…"
        q=F["sm"].render(("Intro quote: "+qprev) if LANG=="ENG" else ("Intro quote: "+qprev),True,C_GRY)
        surf.blit(q,(W//2-q.get_width()//2,204))
        self.splash_btn.draw(surf)
        self.lang_btn.draw(surf)
        draw_sun(surf,80,80,30)

    def handle(self,ev):
        global SPLASH_ENABLED, LANG
        if self.back.clicked(ev): return "back"
        if self.splash_btn.clicked(ev):
            SPLASH_ENABLED = not SPLASH_ENABLED; save_settings(); return None
        if self.lang_btn.clicked(ev):
            LANG = "ENG" if LANG=="FIL" else "FIL"; save_settings(); return None
        return None

class MainMenu:
    # Translate-button rect (bottom-right corner, always the same position)
    _TR = pygame.Rect(1170, 626, 100, 36)

    def __init__(self):
        self.ticker=Ticker(); self.t=0; self.alpha=255
        self._rebuild_btns()

    def _rebuild_btns(self):
        bx,bw,bh=540,202,52
        self.btns={
            "new"     :Btn(bx,360,bw,bh,T("btn_new")),
            "load"    :Btn(bx,424,bw,bh,T("btn_load")),
            "settings":Btn(bx,488,bw,bh,T("btn_settings")),
            "quit"    :Btn(bx,552,bw,bh,T("btn_quit")),
        }

    def _draw_ph(self,surf):
        """Geo-accurate Philippines silhouette matching in-game MAP_DATA, scaled for menu."""
        # MAP_DATA coords (game panel) >> menu: shift x+220, scale 0.56, shift y+20
        def mp(x,y): return (int(220+x*0.56), int(20+y*0.56))
        polys=[
            ([mp(*p) for p in [
              (239,50),(265,46),(290,57),(303,92),(316,130),(313,164),
              (302,190),(290,220),(274,238),(258,230),(244,212),(236,198),
              (229,180),(221,168),(214,148),(209,126),(203,106),(206,86),(216,66),(228,53)
            ]],(30,70,175)),
            ([mp(*p) for p in [
              (133,228),(148,220),(157,234),(150,258),(138,282),(125,308),
              (110,330),(97,348),(87,358),(80,366),(75,350),(84,332),
              (96,314),(108,292),(120,268),(128,244),(131,230)
            ]],(30,70,175)),
            ([mp(*p) for p in [
              (218,260),(250,250),(271,256),(287,252),(308,258),(324,266),
              (337,282),(349,294),(356,312),(348,334),(334,346),(316,356),
              (296,362),(276,354),(256,342),(236,328),(220,310),(206,294),(204,274)
            ]],(220,170,0)),
            ([mp(*p) for p in [
              (189,382),(210,371),(234,364),(258,360),(282,358),(305,362),
              (323,372),(330,396),(328,416),(316,438),(302,454),(284,466),
              (264,472),(243,468),(222,460),(200,450),(180,440),(162,428),
              (150,414),(144,398),(154,384),(174,378)
            ]],(180,30,30)),
        ]
        for pts,c in polys:
            if len(pts)>=3:
                pygame.draw.polygon(surf,c,pts)
                lighter=(min(255,c[0]+50),min(255,c[1]+50),min(255,c[2]+30))
                pygame.draw.polygon(surf,lighter,pts,1)

    def _draw_translate_btn(self,surf,mx,my):
        r=self._TR; hov=r.collidepoint(mx,my)
        # Pill background
        col=lc((28,55,100),(50,90,160),0.55 if hov else 0)
        pygame.draw.rect(surf,col,r,border_radius=10)
        pygame.draw.rect(surf,C_GOLD if hov else C_GD,r,2,border_radius=10)
        # Globe icon circle
        pygame.draw.circle(surf,C_GD,(r.x+16,r.centery),9)
        pygame.draw.circle(surf,C_GD,(r.x+16,r.centery),9,1)
        pygame.draw.line(surf,C_GD,(r.x+7,r.centery),(r.x+25,r.centery),1)
        pygame.draw.arc(surf,C_GD,pygame.Rect(r.x+10,r.centery-9,12,18),0,math.pi,1)
        # Label: current-lang arrow next-lang
        lbl = "ENG" if LANG=="FIL" else "FIL"
        ts=F["sm"].render(lbl,True,C_GOLD if hov else C_WHT)
        surf.blit(ts,(r.x+28,r.centery-ts.get_height()//2))

    def upd(self,mx,my):
        for b in self.btns.values(): b.upd(mx,my)
        self.ticker.upd(); self.t+=0.018
        if self.alpha>0: self.alpha=max(0,self.alpha-14)

    def draw(self,surf,mx=0,my=0):
        gbg_menu(surf,self.t)
        # PH map as a translucent overlay on the ocean/beach area
        self._draw_ph(surf)
        # Dark translucent panel behind title & buttons
        panel=pygame.Surface((520,320),pygame.SRCALPHA)
        panel.fill((0,10,30,160))
        surf.blit(panel,(W//2-260,106))
        pygame.draw.rect(surf,C_GD,(W//2-260,106,520,320),1,border_radius=8)
        for dx,dy,c in [(3,2,(0,0,0)),(0,0,C_GOLD)]:
            s=F["H"].render(TITLE,True,c); surf.blit(s,(W//2-s.get_width()//2+dx,118+dy))
        s=F["h2"].render(T("subtitle"),True,C_WHT)
        surf.blit(s,(W//2-s.get_width()//2,184))
        lw=int(240+math.sin(self.t*2)*50)
        pygame.draw.line(surf,C_GOLD,(W//2-lw//2,216),(W//2+lw//2,216),2)
        for b in self.btns.values(): b.draw(surf)
        draw_sun(surf,68,68,28); draw_sun(surf,1210,68,22)
        v=F["sm"].render(T("disclaimer"),True,(180,180,180))
        surf.blit(v,(W//2-v.get_width()//2,662))
        self._draw_translate_btn(surf,mx,my)
        self.ticker.draw(surf)
        if self.alpha>0: fade_surf(surf,self.alpha)

    def handle(self,ev):
        global LANG
        # Translate button -- toggle language then rebuild btn labels + ticker
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self._TR.collidepoint(ev.pos):
            LANG = "ENG" if LANG=="FIL" else "FIL"
            save_settings()
            self._rebuild_btns()
            self.ticker.refresh_lang()
            return None
        for k,b in self.btns.items():
            if b.clicked(ev): return k
        return None

class SetupA:
    def __init__(self): self.name=""; self.err=""; self.btn=Btn(540,460,200,50,T("step1_confirm")); self._t=0
    def draw(self,surf,mx,my):
        gbg_menu(surf,self._t); self._t+=0.016
        self.btn.upd(mx,my); draw_sun(surf,80,80,30)
        self.btn.lbl=T("step1_confirm")
        blit_c(surf,T("step1_title"),F["h1"],C_GOLD,180)
        blit_c(surf,T("step1_prompt"),F["bd"],C_WHT,280)
        pygame.draw.rect(surf,C_PAN,(390,328,500,60),border_radius=8)
        pygame.draw.rect(surf,C_GOLD,(390,328,500,60),2,border_radius=8)
        cur="▌" if int(pygame.time.get_ticks()/500)%2==0 else " "
        s=F["h1"].render(self.name+cur,True,C_WHT); surf.blit(s,(402,342))
        self.btn.draw(surf)
        if self.err: s=F["bd"].render(self.err,True,C_RL); surf.blit(s,(W//2-s.get_width()//2,530))
    def handle(self,ev):
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_RETURN and self.name.strip(): return self.name.strip()
            elif ev.key==pygame.K_BACKSPACE: self.name=self.name[:-1]
            elif len(self.name)<24 and ev.unicode.isprintable(): self.name+=ev.unicode
        if self.btn.clicked(ev):
            if self.name.strip(): return self.name.strip()
            self.err=T("step1_err")
        return None

class SetupB:
    CARDS=[
        {"id":"SOBERANIYA","lbl":"PRO-PHILIPPINE","sub":"SOBERANIYA","desc":"National sovereignty & assertive diplomacy","bonus":"+10 Sovereignty  +5 Trust","pen":"Slower foreign aid","cols":[(30,80,200),(200,30,30),(255,215,0)]},
        {"id":"ALYANSA","lbl":"PRO-UNITED STATES","sub":"ALYANSA","desc":"Military alliance & Western investment","bonus":"+15 Military  +10 Economy","pen":"-10 China Rel","cols":[(180,30,30),(245,245,245),(30,80,200)]},
        {"id":"PAKIKIPAG-UGNAYAN","lbl":"PRO-CHINA","sub":"PAKIKIPAG-UGNAYAN","desc":"BRI infrastructure & economic ties","bonus":"+20 Infrastructure  +10 China","pen":"-15 Sovereignty","cols":[(200,30,30),(255,215,0),(200,30,30)]},
        {"id":"BALANSE","lbl":"NEUTRAL","sub":"BALANSE","desc":"ASEAN cooperation & balanced trade","bonus":"+5 to all relations","pen":"No strong bonuses","cols":[(30,120,200),(245,245,245),(30,140,80)]},
    ]
    def __init__(self): self.sel=None
    def _r(self,i): return pygame.Rect(48+i*300,210,278,320)
    def draw(self,surf,mx,my):
        gbg_menu(surf, getattr(self,'_t',0)); self._t=getattr(self,'_t',0)+0.016
        blit_c(surf,T("step2_title"),F["h1"],C_GOLD,150)
        for i,c in enumerate(self.CARDS):
            r=self._r(i); hov=r.collidepoint(mx,my); sel=self.sel==c["id"]
            pygame.draw.rect(surf,lc(C_PAN,c["cols"][0],0.22+0.22*sel),r,border_radius=10)
            pygame.draw.rect(surf,C_GOLD if sel else(C_GD if hov else C_GRY),r,2+sel,border_radius=10)
            fw=r.w-20
            for j,fc in enumerate(c["cols"]): pygame.draw.rect(surf,fc,(r.x+10+j*(fw//3),r.y+14,fw//3,34))
            pygame.draw.rect(surf,C_GD,(r.x+10,r.y+14,fw,34),1)
            surf.blit(F["h2"].render(c["lbl"],True,C_GOLD if sel else C_WHT),(r.x+10,r.y+56))
            surf.blit(F["sm"].render(c["sub"],True,C_GD),(r.x+10,r.y+82))
            for j,ln in enumerate(wrap(c["desc"],F["sm"],r.w-20)): surf.blit(F["sm"].render(ln,True,C_WHT),(r.x+10,r.y+100+j*16))
            surf.blit(F["sm"].render(f"+ {c['bonus']}",True,C_GRN),(r.x+10,r.y+168))
            surf.blit(F["sm"].render(f"- {c['pen']}",True,C_RL),(r.x+10,r.y+188))
        if self.sel:
            b=Btn(540,598,200,44,T("next_btn")); b.upd(mx,my); b.draw(surf)
        draw_sun(surf,80,80,30)
    def handle(self,ev):
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            mx,my=ev.pos
            for i,c in enumerate(self.CARDS):
                if self._r(i).collidepoint(mx,my): self.sel=c["id"]
            if self.sel and pygame.Rect(540,598,200,44).collidepoint(mx,my): return self.sel
        return None

class SetupC:
    def __init__(self): self.sel=None
    def _r(self,i): return pygame.Rect(30+i*248,240,230,290)
    def draw(self,surf,mx,my):
        gbg_menu(surf, getattr(self,'_t',0)); self._t=getattr(self,'_t',0)+0.016
        blit_c(surf,T("step3_title"),F["h1"],C_GOLD,155)
        w=F["sm"].render(T("step3_warn"),True,C_YLW)
        surf.blit(w,(W//2-w.get_width()//2,196))
        for i,(sid,desc,col) in enumerate(POLITICAL_SYSTEMS):
            r=self._r(i); hov=r.collidepoint(mx,my); sel=self.sel==sid
            pygame.draw.rect(surf,lc(C_PAN,col,0.28+0.28*sel),r,border_radius=10)
            pygame.draw.rect(surf,C_GOLD if sel else(C_GD if hov else C_GRY),r,2+sel,border_radius=10)
            lbl=sid.split()[-1] if " " in sid else sid
            surf.blit(F["bd"].render(sid[:16],True,C_GOLD if sel else C_WHT),(r.x+8,r.y+14))
            for j,ln in enumerate(wrap(desc,F["sm"],r.w-16)): surf.blit(F["sm"].render(ln,True,C_WHT),(r.x+8,r.y+44+j*18))
            if sid in AUTH_SYSTEMS:
                t=F["sm"].render("DICTATOR PATH",True,C_RL); surf.blit(t,(r.x+8,r.y+r.h-20))
        if self.sel:
            b=Btn(540,596,200,44,T("next_btn")); b.upd(mx,my); b.draw(surf)
        draw_sun(surf,80,80,30)
    def handle(self,ev):
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            mx,my=ev.pos
            for i,(sid,_,_) in enumerate(POLITICAL_SYSTEMS):
                if self._r(i).collidepoint(mx,my): self.sel=sid
            if self.sel and pygame.Rect(540,596,200,44).collidepoint(mx,my): return self.sel
        return None

class SetupD:
    DIFFS=[("ESTUDYANTE","Easy","Mabait na krisis, generous budget, mahinang bagyo",(30,150,55)),
           ("SENADOR","Normal","Balanced challenge -- ang standard na karanasan",(200,160,0)),
           ("PANGULO","Hard","Madalas na krisis, mahigpit na budget, matinding bagyo",(180,30,30))]
    def __init__(self): self.sel=None
    def _r(self,i): return pygame.Rect(160+i*345,278,305,224)
    def draw(self,surf,mx,my):
        gbg_menu(surf, getattr(self,'_t',0)); self._t=getattr(self,'_t',0)+0.016
        blit_c(surf,T("step4_title"),F["h1"],C_GOLD,178)
        for i,(did,sub,desc,col) in enumerate(self.DIFFS):
            r=self._r(i); hov=r.collidepoint(mx,my); sel=self.sel==did
            pygame.draw.rect(surf,lc(C_PAN,col,0.28+0.28*sel),r,border_radius=12)
            pygame.draw.rect(surf,C_GOLD if sel else(C_GD if hov else C_GRY),r,2+sel,border_radius=12)
            lb=F["h1"].render(did,True,C_GOLD if sel else C_WHT); surf.blit(lb,(r.centerx-lb.get_width()//2,r.y+28))
            sb=F["bd"].render(sub,True,C_GD); surf.blit(sb,(r.centerx-sb.get_width()//2,r.y+72))
            for j,ln in enumerate(wrap(desc,F["sm"],r.w-20)):
                ts=F["sm"].render(ln,True,C_WHT); surf.blit(ts,(r.centerx-ts.get_width()//2,r.y+102+j*16))
        if self.sel:
            b=Btn(540,580,200,44,T("start_btn")); b.upd(mx,my); b.draw(surf)
        draw_sun(surf,80,80,30)
    def handle(self,ev):
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            mx,my=ev.pos
            for i,(did,_,_,_) in enumerate(self.DIFFS):
                if self._r(i).collidepoint(mx,my): self.sel=did
            if self.sel and pygame.Rect(540,580,200,44).collidepoint(mx,my): return self.sel
        return None

class LoadScreen:
    def __init__(self):
        self.slots=[SaveManager.load(i) for i in range(3)]
        self.back=Btn(40,40,130,38,T("back_btn"),fk="bd")
        self._del_confirm=-1  # slot index pending delete confirm

    def _del_rects(self):
        return [pygame.Rect(960,218+i*162,60,32) for i in range(3)]

    def draw(self,surf,mx,my):
        gbg_menu(surf, getattr(self,'_t',0)); self._t=getattr(self,'_t',0)+0.016
        self.back.lbl=T("back_btn"); self.back.upd(mx,my); self.back.draw(surf)
        blit_c(surf,T("load_title"),F["h1"],C_GOLD,140)
        for i,d in enumerate(self.slots):
            r=pygame.Rect(340,218+i*162,600,138); hov=r.collidepoint(mx,my)
            pygame.draw.rect(surf,lc(C_PAN,C_PAN2,0.5 if hov else 0),r,border_radius=10)
            pygame.draw.rect(surf,C_GOLD if hov else C_GD,r,2,border_radius=10)
            surf.blit(F["h2"].render(f"SLOT {i+1}",True,C_GD),(r.x+14,r.y+10))
            if d:
                surf.blit(F["bd"].render(f"Presidente {d.get('player_name','?')}",True,C_WHT),(r.x+14,r.y+42))
                surf.blit(F["bd"].render(f"Taon {d.get('year','?')}  |  Approval: {d.get('approval_rating',0):.1f}%",True,C_GOLD),(r.x+14,r.y+68))
                surf.blit(F["sm"].render(f"System: {d.get('political_system','?')}  |  Saved: {d.get('_ts','?')}",True,C_GRY),(r.x+14,r.y+100))
                # Delete button
                dr=self._del_rects()[i]; dh=dr.collidepoint(mx,my)
                pygame.draw.rect(surf,(120,20,20) if dh else (80,15,15),dr,border_radius=6)
                ds=F["sm"].render("DEL DEL",True,C_WHT); surf.blit(ds,(dr.x+6,dr.y+8))
            else:
                # Show "NEW GAME HERE" option
                ng_r=pygame.Rect(r.x+14,r.y+42,200,40); ngh=ng_r.collidepoint(mx,my)
                pygame.draw.rect(surf,(20,50,20) if ngh else (12,32,12),ng_r,border_radius=6)
                pygame.draw.rect(surf,C_GD,ng_r,1,border_radius=6)
                ns=F["sm"].render("+ New Game Here" if LANG=="ENG" else "+ Bagong Laro Dito",True,C_GRN)
                surf.blit(ns,(ng_r.x+8,ng_r.y+12))
                e=F["h2"].render(T("empty_slot"),True,C_GRY); surf.blit(e,(r.x+240,r.centery-e.get_height()//2))
        # Delete confirm overlay
        if self._del_confirm>=0:
            ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,160)); surf.blit(ov,(0,0))
            dw,dh2=460,160; dx,dy=W//2-dw//2,H//2-dh2//2
            pygame.draw.rect(surf,C_PAN,(dx,dy,dw,dh2),border_radius=12)
            pygame.draw.rect(surf,C_RL,(dx,dy,dw,dh2),2,border_radius=12)
            msg=f"Delete Slot {self._del_confirm+1}?" if LANG=="ENG" else f"Burahin ang Slot {self._del_confirm+1}?"
            blit_c(surf,msg,F["h2"],C_RL,dy+22)
            b1=Btn(dx+30,dy+80,180,46,"+ Delete" if LANG=="ENG" else "+ Burahin",base=(100,20,20))
            b2=Btn(dx+250,dy+80,180,46,"Cancel" if LANG=="ENG" else "Kanselahin")
            b1.upd(mx,my); b2.upd(mx,my); b1.draw(surf); b2.draw(surf)

    def handle(self,ev):
        if self._del_confirm>=0:
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                mx,my=ev.pos; i=self._del_confirm
                dw,dh2=460,160; dx,dy=W//2-dw//2,H//2-dh2//2
                if pygame.Rect(dx+30,dy+80,180,46).collidepoint(mx,my):
                    try: os.remove(SaveManager.path(i))
                    except: pass
                    self.slots[i]=None; self._del_confirm=-1
                elif pygame.Rect(dx+250,dy+80,180,46).collidepoint(mx,my):
                    self._del_confirm=-1
            return None
        if self.back.clicked(ev): return("back",)
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            mx,my=ev.pos
            for i in range(3):
                # Delete button
                dr=self._del_rects()[i]
                if dr.collidepoint(mx,my) and self.slots[i]:
                    self._del_confirm=i; return None
                # New game in empty slot
                r=pygame.Rect(340,218+i*162,600,138)
                if r.collidepoint(mx,my):
                    if self.slots[i]: return("load",i)
                    else: return("newgame",i)  # new game in this slot
        return None

# ── GAME SCREEN ──────────────────────────────────────────────
class GameScreen:
    STATS=[("Economy","economy"),("Military","military"),("Trust","public_trust"),
           ("Corruption","corruption"),("Inequality","inequality"),("Infra","infrastructure"),
           ("Health","health"),("Education","education"),("Sovereignty","sovereignty"),("Press Free","press_freedom")]
    RELS=[("US","rel_us"),("China","rel_china"),("ASEAN","rel_asean"),("UN","rel_un")]

    def __init__(self,gs,slot=0):
        self.gs=gs; self.slot=slot
        self.ticker=Ticker(); self.card=EventCard()
        self.pol=PolicyManager(); self.bud=BudgetManager()
        self.ty_eng=TyphoonEngine()
        self.dv={s:getattr(gs,s) for _,s in self.STATS+self.RELS+[("Auth","auth_power")]}
        self.sub=None  # None|policies|budget|events|typhoon|pause|annual|typhoon_resolve
        self.hover_r=None; self.sel_r=None
        self.ty_anim=128; self.ty_dir=1; self.ty_season=[]; self.ty_result=None
        self.pol_scroll=0; self.ev_scroll=0; self.ty_scroll=0
        self.annual_txt=[]; self.relief_choice=None
        self.pending_events=[]
        self._event_queue=[]  # max 10 pending events
        self.achv=AchievementManager()
        self._make_nav()

    def _make_nav(self):
        self.nav={
            "policies":Btn(8,  658,88,30,T("nav_policies"),fk="sm"),
            "budget"  :Btn(100,658,88,30,T("nav_budget"),  fk="sm"),
            "events"  :Btn(192,658,88,30,T("nav_events"),  fk="sm"),
            "typhoon" :Btn(284,658,88,30,T("nav_typhoon"), fk="sm"),
            "achiev"  :Btn(376,658,88,30,T("nav_achiev"),  fk="sm"),
            "research":Btn(468,658,88,30,T("nav_research"),fk="sm"),
            "diplo"   :Btn(560,658,88,30,T("nav_diplo"),   fk="sm"),
            "pshows"  :Btn(652,658,100,30,"SHOWS",         fk="sm"),
            "next"    :Btn(1090,658,178,30,T("nav_next"),  fk="sm"),
        }
        self.pbtn={
            "resume":Btn(490,254,300,54,T("pause_resume")),
            "save"  :Btn(490,318,300,54,T("pause_save")),
            "menu"  :Btn(490,382,300,54,T("pause_menu")),
            "quit"  :Btn(490,446,300,54,T("pause_quit")),
        }
        self.ok_btn=Btn(540,490,200,44,T("ok_btn"))
        self.rel_btns={
            "low" :Btn(290,390,185,44,T("relief_low"), fk="bd"),
            "mid" :Btn(488,390,200,44,T("relief_mid"), fk="bd"),
            "high":Btn(700,390,175,44,T("relief_high"),fk="bd"),
        }

    # ── draw helpers ──

    def _draw_cult_overlay(self,surf):
        """Draw personality cult elements for authoritarian leaders."""
        gs=self.gs
        if gs.political_system not in AUTH_SYSTEMS or gs.auth_power < 30: return
        strength=gs.auth_power/100.0
        alpha=min(200,int(gs.auth_power*2.0))
        # Red side strips (map panel edges)
        ov=pygame.Surface((32,612),pygame.SRCALPHA); ov.fill((200,0,0,alpha//4))
        surf.blit(ov,(0,40)); surf.blit(ov,(678,40))
        # Posters on buildings in the city background (left half only — game map is right)
        # Draw a billboard / poster on a building face
        poster_positions=[(55,320),(130,290),(210,345),(440,380),(500,295)]
        msgs=["ANG PANGULO","LAKAS AT BAYAN","UTOS NG LIDER","TAGUMPAY","PANANAGUTAN"] if LANG!="FIL" else ["THE PRESIDENT","STRENGTH+NATION","LEADER'S ORDER","TRIUMPH","ACCOUNTABILITY"]
        rng2=__import__('random').Random(42)
        for i,(bx,by) in enumerate(poster_positions):
            if i >= len(msgs): break
            pw2=int(68*strength); ph2=int(44*strength)
            if pw2<20: continue
            # Red poster rectangle
            ps=pygame.Surface((pw2,ph2),pygame.SRCALPHA)
            ps.fill((180,10,10,min(220,alpha)))
            surf.blit(ps,(bx,by))
            pygame.draw.rect(surf,(220,200,50),(bx,by,pw2,ph2),1)
            # President silhouette (simple oval head + body)
            fx=bx+pw2-14; fy=by+4
            pygame.draw.circle(surf,(220,185,100),(fx,fy+6),7)
            pygame.draw.rect(surf,(180,50,50),(fx-5,fy+13,10,12))
            # Text
            ms=F["sm"].render(msgs[i%len(msgs)][:10],True,(255,230,50))
            surf.blit(ms,(bx+2,by+ph2-ms.get_height()-2))

    def _topbar(self,surf):
        pygame.draw.rect(surf,C_DARK,(0,0,W,40))
        pygame.draw.line(surf,C_GD,(0,40),(W,40),1)
        gs=self.gs
        surf.blit(F["bd"].render(f" {MONTHS[gs.month]} {gs.year}  {T('topbar_term')} {gs.term}",True,C_WHT),(10,10))
        bc=C_RL if gs.budget<0 else C_GOLD
        surf.blit(F["bd"].render(f"P{gs.budget:,.0f}B",True,bc),(260,10))
        apc=C_GRN if gs.approval_rating>60 else C_YLW if gs.approval_rating>35 else C_RL
        surf.blit(F["bd"].render(f"{T('topbar_appr')} {gs.approval_rating:.1f}%",True,apc),(420,10))
        surf.blit(F["sm"].render(f"[{gs.foreign_stance}]",True,C_GD),(650,13))
        surf.blit(F["sm"].render(gs.political_system[:24],True,C_GRY),(808,13))
        surf.blit(F["bd"].render(f"Pres. {gs.player_name}",True,C_WHT),(1080,10))
        if 6<=gs.month<=11:
            self.ty_anim+=5*self.ty_dir
            if self.ty_anim>=240: self.ty_dir=-1
            elif self.ty_anim<=80: self.ty_dir=1
            ov=pygame.Surface((190,22),pygame.SRCALPHA); ov.fill((180,0,0,self.ty_anim)); surf.blit(ov,(555,4))
            surf.blit(F["sm"].render("TY TYPHOON SEASON",True,C_WHT),(558,8))

    def _map(self,surf,mx,my):
        # No fill — let the city background show through the map panel
        # Just draw a faint sea texture in the gaps between islands
        t=pygame.time.get_ticks()
        for yy in range(50,640,28):
            off=(t//300)%28
            xpos=(yy*7+off)%720
            pygame.draw.circle(surf,(60,110,170,80),(xpos,yy),3)
        # West PH Sea label
        for ln in ["WEST","PH SEA"]:
            s=F["sm"].render(ln,True,(90,160,230)); surf.blit(s,(10,290+["WEST","PH SEA"].index(ln)*18))
        self.hover_r=None
        for name,d in MAP_DATA.items():
            pts=d["poly"]; cx,cy=d["ctr"]; base=d["col"]
            hov=pt_in_poly(mx,my,pts); sel=self.sel_r==name
            if hov: self.hover_r=name
            col=lc(base,C_GOLD,0.35) if(hov or sel)else base
            pygame.draw.polygon(surf,col,pts)
            pygame.draw.polygon(surf,C_GOLD if(hov or sel)else C_GD,pts,2+sel)
            ns=F["sm"].render(name,True,C_GOLD if(hov or sel)else C_WHT)
            surf.blit(ns,(cx-ns.get_width()//2,cy-ns.get_height()//2))
        if self.sel_r and self.sel_r in REGION_STATS:
            gs=self.gs
            rd=REGION_STATS[self.sel_r]; px,py=510,42; pw,ph=220,148
            pygame.draw.rect(surf,C_PAN,(px,py,pw,ph),border_radius=7)
            pygame.draw.rect(surf,C_GOLD,(px,py,pw,ph),1,border_radius=7)
            surf.blit(F["bd"].render(self.sel_r,True,C_GOLD),(px+6,py+5))
            # Static base data
            surf.blit(F["sm"].render(f"GDP share: {rd['GDP%']}",True,C_WHT),(px+6,py+28))
            surf.blit(F["sm"].render(f"Typhoon risk: {rd['Typhoon']}",True,C_WHT),(px+6,py+46))
            # Dynamic data from gs
            infra=gs.region_infra.get(self.sel_r, rd.get('Infra',50))
            pov=gs.region_poverty.get(self.sel_r, float(rd.get('Poverty%','20').replace('%','')))
            reb=gs.region_rebel.get(self.sel_r, 10)
            i_c=stat_col(infra); p_c=C_GRN if pov<15 else C_YLW if pov<30 else C_RL
            r_c=C_GRN if reb<20 else C_YLW if reb<45 else C_RL
            surf.blit(F["sm"].render(f"Infra: {infra:.0f}%",True,i_c),(px+6,py+64))
            surf.blit(F["sm"].render(f"Poverty: {pov:.1f}%",True,p_c),(px+6,py+82))
            surf.blit(F["sm"].render(f"Rebel: {reb:.0f}%",True,r_c),(px+6,py+100))
            chg="+ improving" if infra>REGION_STATS[self.sel_r].get('Infra',50) else "- declining"
            surf.blit(F["sm"].render(chg,True,C_GRN if '^' in chg else C_RL),(px+6,py+122))

    def _right(self,surf):
        px,py,pw=710,40,566; ph=612
        pygame.draw.rect(surf,C_PAN,(px,py,pw,ph))
        pygame.draw.line(surf,C_GD,(px,py),(px,py+ph),1)
        gs=self.gs

        # ── clip all drawing to the right panel ──────────────────────
        old_clip=surf.get_clip()
        surf.set_clip(pygame.Rect(px,py,pw,ph))

        cy=py

        # ── ECONOMIC INDICATORS (fixed 104px block) ───────────────────
        econ_h=118
        pygame.draw.rect(surf,(8,22,48),(px,cy,pw,econ_h))
        hdr="GDP & ECONOMIC INDICATORS" if LANG=="ENG" else "GDP AT MGA TAGAPAGPAHIWATIG"
        surf.blit(F["h2"].render(hdr,True,C_GOLD),(px+8,cy+3))
        # Use cached indicators — only _advance() updates GDP/growth
        ENG=LANG=="ENG"
        g_c=C_GRN if gs.gdp_growth>=0 else C_RL
        u_c=C_GRN if gs.unemployment<5 else C_YLW if gs.unemployment<10 else C_RL
        i_c=C_GRN if gs.inflation<3   else C_YLW if gs.inflation<7    else C_RL
        p_c=C_GRN if gs.poverty_rate<10 else C_YLW if gs.poverty_rate<25 else C_RL
        d_c=C_GRN if gs.debt/max(gs.gdp,1)*100<40 else C_YLW if gs.debt/max(gs.gdp,1)*100<70 else C_RL
        # GDP value + sparkline (no growing %)
        gdp_lbl=f"GDP: P{gs.gdp/1000:.2f}T  ({'+' if gs.gdp_growth>=0 else ''}{gs.gdp_growth:.1f}%/yr)"
        surf.blit(F["sm"].render(gdp_lbl,True,C_GOLD),(px+6,cy+24))
        gdp_hist=getattr(gs,'gdp_history',[gs.gdp/1000])
        if len(gdp_hist)>2:
            gsx=px+6; gsy=cy+42; gsw=pw-12; gsh=18
            pygame.draw.rect(surf,(8,18,38),(gsx,gsy,gsw,gsh))
            mn=min(gdp_hist); mx_=max(gdp_hist); rng_=max(mx_-mn,0.01)
            gpts=[(gsx+int(j/(len(gdp_hist)-1)*gsw), int(gsy+gsh-(gdp_hist[j]-mn)/rng_*gsh)) for j in range(len(gdp_hist))]
            if len(gpts)>1: pygame.draw.lines(surf,C_GRN,False,gpts,2)
        # Compact stats grid (4 items, 2 columns)
        rows=[
            (("Unemploy." if ENG else "Walang-trabaho")+f": {gs.unemployment:.1f}%",u_c),
            (("Inflation" if ENG else "Implasyon")+f": {gs.inflation:.1f}%",i_c),
            (("Poverty" if ENG else "Kahirapan")+f": {gs.poverty_rate:.1f}%",p_c),
            (("Debt/GDP" if ENG else "Utang/GDP")+f": {gs.debt/max(gs.gdp,1)*100:.1f}%",d_c),
        ]
        cw2=pw//2
        for i,(txt,tc) in enumerate(rows):
            sx=px+(i%2)*cw2+4; sy=cy+60+(i//2)*22
            s=F["sm"].render(txt,True,tc)
            if s.get_width()>cw2-8: s=pygame.transform.scale(s,(cw2-8,s.get_height()))
            surf.blit(s,(sx,sy))
        rp_val=getattr(gs,"research_points",0)
        rp_s=F["sm"].render(f"RP:{rp_val:.0f} T{getattr(gs,'research_tier',0)} Unlocked:{len(getattr(gs,'research_unlocked',[]))}",True,C_BLU)
        surf.blit(rp_s,(px+6,cy+econ_h-16))
        pygame.draw.line(surf,C_GD,(px+4,cy+econ_h),(px+pw-4,cy+econ_h),1)
        cy+=econ_h+2

        # ── NATIONAL STATS ────────────────────────────────────────
        surf.blit(F["h2"].render(T("nat_stats"),True,C_GOLD),(px+8,cy+3))
        cy+=24
        stats=list(self.STATS)
        if gs.political_system in AUTH_SYSTEMS: stats.append(("Auth Pwr","auth_power"))
        bar_w=295; bar_x=px+84
        for lbl,sn in stats:
            if cy+14>py+ph-30: break          # safety -- stop before overflow
            tv=getattr(gs,sn,50)
            self.dv[sn]=lerp(self.dv.get(sn,tv),tv,0.07)
            inv=sn in("corruption","inequality")
            draw_bar(surf,bar_x,cy,bar_w,12,self.dv[sn],lbl,invert=inv)
            cy+=25
        pygame.draw.line(surf,C_GD,(px+4,cy),(px+pw-4,cy),1); cy+=4

        # ── FOREIGN RELATIONS ─────────────────────────────────────
        if cy+22+len(self.RELS)*24<py+ph-4:
            surf.blit(F["h2"].render(T("for_rel"),True,C_GOLD),(px+8,cy))
            cy+=20
            for lbl,sn in self.RELS:
                if cy+14>py+ph-30: break
                tv=getattr(gs,sn,50); self.dv[sn]=lerp(self.dv.get(sn,tv),tv,0.07)
                draw_bar(surf,bar_x,cy,bar_w,12,self.dv[sn],lbl)
                cy+=23

        # ── APPROVAL SPARKLINE ────────────────────────────────────
        ah=gs.approval_history[-24:]
        if len(ah)>2 and cy+54<py+ph:
            pygame.draw.line(surf,C_GD,(px+4,cy+2),(px+pw-4,cy+2),1); cy+=5
            surf.blit(F["sm"].render(T("appr_trend"),True,C_GRY),(px+8,cy))
            cy+=13; sh=min(38,py+ph-cy-4)
            if sh>8:
                pygame.draw.rect(surf,(8,20,44),(px+8,cy,pw-16,sh))
                pts=[(px+8+int(j/(len(ah)-1)*(pw-16)),int(cy+sh-(ah[j]/100)*sh)) for j in range(len(ah))]
                if len(pts)>1: pygame.draw.lines(surf,C_GOLD,False,pts,2)

        surf.set_clip(old_clip)

    def _live_ticker(self):
        """Push recent in-game events and typhoon news into the ticker.
        The ticker now acts as a rolling PRESS WIRE showing actual decisions
        and typhoon events -- NOT generic stat commentary."""
        gs=self.gs
        # Only replace base if it's empty or stale (keep event_log-driven additions)
        # The ticker._extra already holds all the important real events.
        # We only add structural date-line if the extra is sparse.
        if len(self.ticker._extra) < 3:
            if LANG=="ENG":
                self.ticker._base = [
                    f"NEWS {MONTHS[gs.month]} {gs.year} -- The press watches the administration closely...",
                    f"## GDP P{gs.gdp/1000:.2f}T  |  Growth {gs.gdp_growth:+.1f}%  |  Inflation {gs.inflation:.1f}%  |  Unemployment {gs.unemployment:.1f}%",
                ]
            else:
                self.ticker._base = [
                    f"NEWS {MONTHS[gs.month]} {gs.year} -- Ang palathala ay maingat na pinanonood ang administrasyon...",
                    f"## GDP P{gs.gdp/1000:.2f}T  |  Paglago {gs.gdp_growth:+.1f}%  |  Implasyon {gs.inflation:.1f}%  |  Walang-trabaho {gs.unemployment:.1f}%",
                ]
            self.ticker._rebuild()

    def _navbar(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,650,W,70))
        pygame.draw.line(surf,C_GD,(0,650),(W,650),1)
        for b in self.nav.values(): b.upd(mx,my); b.draw(surf)
        # Keyboard hint -- bottom-right corner, well clear of all buttons
        esc=F["sm"].render(T("nav_hint"),True,C_GRY)
        surf.blit(esc,(W-esc.get_width()-8, 653))
        self.ticker.upd(); self.ticker.draw(surf)

    # ── sub screens ──
    def _draw_policies(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("pol_title"),F["h1"],C_GOLD,8)
        gs=self.gs; maxp=4 if gs.difficulty=="PANGULO" else 6
        hint=T("pol_hint").format(a=len(gs.active_policies),m=maxp)
        s=F["bd"].render(hint,True,C_GRY); surf.blit(s,(10,44))
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        avail=self.pol.available(gs)
        for i,p in enumerate(avail):
            y=78+i*54-self.pol_scroll
            if y<68 or y>645: continue
            act=p["id"] in gs.active_policies; hov=pygame.Rect(28,y,1010,46).collidepoint(mx,my)
            is_sc="sys_change" in p
            base_col=(24,52,72) if is_sc else (24,72,24)
            col=lc(C_PAN,base_col,0.6 if act else(0.3 if hov else 0))
            pygame.draw.rect(surf,col,(28,y,1010,46),border_radius=7)
            bdr=C_BLU if is_sc else(C_GOLD if act else(C_GD if hov else C_GRY))
            pygame.draw.rect(surf,bdr,(28,y,1010,46),2,border_radius=7)
            name_lbl=p["name"]; 
            if is_sc:
                tag=F["sm"].render(T("pol_sys_change"),True,C_BLU)
                surf.blit(tag,(36,y+7))
                surf.blit(F["bd"].render(name_lbl,True,C_BLU),(36+tag.get_width()+8,y+7))
            else:
                surf.blit(F["bd"].render(name_lbl,True,C_GOLD if act else C_WHT),(36,y+7))
            surf.blit(F["sm"].render(p["desc"],True,C_GRY),(36,y+28))
            cost_lbl=f"P{p['cost']*10}B/yr" if p["cost"]>0 else T("pol_free")
            cs=F["sm"].render(cost_lbl,True,C_YLW); surf.blit(cs,(900,y+16))
            fx_str=" | ".join(f"{k}:{'+' if v>0 else ''}{v}" for k,v in p["fx"].items()
                              if k not in("debt",) and isinstance(v,(int,float)))
            surf.blit(F["sm"].render(fx_str[:55],True,C_GRN if act else C_GRY),(540,y+16))

    def _draw_budget(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("bud_title"),F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        stats=[(T("bud_budget"),f"P{gs.budget:,.0f}B",C_GOLD if gs.budget>0 else C_RL),
               (T("bud_debt"),  f"P{gs.debt:,.0f}B",C_RL),
               (T("bud_rev"),   f"P{self.bud.revenue(gs):.0f}B",C_GRN),
               (T("bud_active"),f"{len(gs.active_policies)}",C_GOLD),
               (T("bud_relief"),f"P{gs.disaster_relief_budget:.0f}B",C_YLW)]
        for i,(lbl,val,c) in enumerate(stats):
            x,y=60,80+i*60
            surf.blit(F["h2"].render(lbl,True,C_GRY),(x,y))
            surf.blit(F["h1"].render(val,True,c),(x+360,y-4))
        # Allocation editor
        hint = "Click bar ends to adjust ±2%  |  Must total 100%" if LANG=="ENG" else "I-click ang mga dulo ng bar para ayusin ±2%  |  Dapat 100% ang kabuuan"
        surf.blit(F["sm"].render(hint,True,C_GRY),(60,385))
        blit_c(surf,T("bud_alloc"),F["h2"],C_GD,368)
        alloc=gs.budget_alloc; keys=list(alloc.keys()); bx=160; bw=700; by=406
        total=sum(alloc.values()); tc=C_GRN if 99<=total<=101 else C_RL
        surf.blit(F["bd"].render(f"Total: {total}%",True,tc),(920,370))
        COLS=[(60,140,220),(80,200,100),(200,100,60),(100,60,200),(200,160,40),(60,180,180),(160,80,120)]
        for i,k in enumerate(keys):
            v=alloc[k]; y=by+i*36
            col=COLS[i%len(COLS)]
            pygame.draw.rect(surf,(18,32,56),(bx,y,bw,24),border_radius=4)
            fw=int(bw*max(0,min(100,v))/100)
            if fw>0: pygame.draw.rect(surf,col,(bx,y,fw,24),border_radius=4)
            pygame.draw.rect(surf,(80,90,110),(bx,y,bw,24),1,border_radius=4)
            lbl_txt=k.replace("_"," ").title()
            surf.blit(F["sm"].render(f"{lbl_txt}  {v}%",True,C_WHT),(bx+6,y+5))
            # - button
            mr=pygame.Rect(bx-30,y,26,24)
            hov_m=mr.collidepoint(mx,my)
            pygame.draw.rect(surf,(80,30,30) if hov_m else (50,20,20),mr,border_radius=5)
            surf.blit(F["bd"].render("-",True,C_WHT),(mr.x+6,mr.y+2))
            # + button
            pr=pygame.Rect(bx+bw+4,y,26,24)
            hov_p=pr.collidepoint(mx,my)
            pygame.draw.rect(surf,(30,80,30) if hov_p else (20,50,20),pr,border_radius=5)
            surf.blit(F["bd"].render("+",True,C_WHT),(pr.x+5,pr.y+2))

    def _draw_diplomacy(self,surf,mx,my):
        """Diplomacy panel -- spend budget to directly improve foreign relationships."""
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        title="DIPLOMACY -- IMPROVE RELATIONS" if LANG=="ENG" else "DIPLOMASYA -- PALAKASIN ANG UGNAYAN"
        blit_c(surf,title,F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        ENG=LANG=="ENG"
        hint=("Spend budget to improve diplomatic ties. Effects are immediate but costly."
              if ENG else
              "Gumastos ng badyet upang mapabuti ang diplomatikong relasyon. Agaran ang epekto ngunit mahal.")
        surf.blit(F["bd"].render(hint,True,C_GRY),(20,46))

        DIPLO=[
            ("US","US","rel_us",
             "Joint military exercise" if ENG else "Magsamanang pagsasanay militar",
             "Cultural exchange programme" if ENG else "Palitan ng kultura",
             "Official state visit" if ENG else "Opisyal na pagbisita"),
            ("CN","China","rel_china",
             "Trade delegation" if ENG else "Delegasyong pangkalakal",
             "Infrastructure partnership" if ENG else "Partnership sa imprastraktura",
             "Summit meeting" if ENG else "Summit na pagpupulong"),
            ("ASEAN","ASEAN","rel_asean",
             "ASEAN forum leadership" if ENG else "Pamumuno sa ASEAN forum",
             "Regional aid package" if ENG else "Panrehiyong tulong",
             "Multilateral deal" if ENG else "Multilateral na kasunduan"),
            ("LANG","UN","rel_un",
             "UN peacekeeping contribution" if ENG else "Kontribusyon sa UN peacekeeping",
             "Humanitarian donation" if ENG else "Donasyong humanitarian",
             "International climate pledge" if ENG else "Pangako sa klima"),
        ]
        ACTIONS=[(80,5,"sm"),(180,12,"md"),(350,22,"lg")]  # (cost B, rel_gain, label)

        if not hasattr(self,"_dip_msg"): self._dip_msg=""
        if self._dip_msg:
            ms=F["bd"].render(self._dip_msg,True,C_GRN); surf.blit(ms,(W//2-ms.get_width()//2,78))

        for ri,(flag,name,stat,a1,a2,a3) in enumerate(DIPLO):
            ry=108+ri*126
            cur=getattr(gs,stat,50)
            pygame.draw.rect(surf,(14,30,58),(12,ry,1256,118),border_radius=8)
            pygame.draw.rect(surf,C_GD,(12,ry,1256,118),1,border_radius=8)
            lbl_s=F["h2"].render(f"{flag} {name}",True,C_GOLD)
            surf.blit(lbl_s,(24,ry+8))
            draw_bar(surf,120,ry+36,240,14,cur)
            for ci,(cost,gain,act_lbl) in enumerate(zip([a1,a2,a3],[*[c for c,g,l in ACTIONS]],[*[l for c,g,l in ACTIONS]])):
                bx=380+ci*290; by=ry+12; bw=275; bh=44
                cost_b,gain_r,_=ACTIONS[ci]
                can=gs.budget>=cost_b
                bc=lc(C_PAN,(24,60,24),0.4 if can else 0)
                pygame.draw.rect(surf,bc,(bx,by,bw,bh),border_radius=7)
                pygame.draw.rect(surf,C_GOLD if can else C_GRY,(bx,by,bw,bh),1,border_radius=7)
                al=F["sm"].render(cost,True,C_WHT); surf.blit(al,(bx+8,by+4))
                bl=F["sm"].render(f"P{cost_b}B  >>  +{gain_r} {name}",True,C_GRN if can else C_GRY)
                surf.blit(bl,(bx+8,by+24))
                if not hasattr(self,"_dip_rects"): self._dip_rects={}
                self._dip_rects[(ri,ci)]=(pygame.Rect(bx,by,bw,bh),stat,cost_b,gain_r,name)

    def _handle_diplomacy_click(self,ev,gs):
        if not hasattr(self,"_dip_rects"): return
        mx,my=pygame.mouse.get_pos(); _ss=pygame.display.get_surface().get_size()
        mx=int(mx*W/_ss[0]); my=int(my*H/_ss[1])
        for key,(rect,stat,cost,gain,name) in self._dip_rects.items():
            if rect.collidepoint(mx,my):
                if gs.budget>=cost:
                    gs.budget-=cost
                    setattr(gs,stat,clamp(getattr(gs,stat,50)+gain))
                    gs.clamp()
                    self._dip_msg=f"+ {name} relations improved by +{gain}! (P{cost}B spent)" if LANG=="ENG" else f"+ Relasyon sa {name} ay tumaas ng +{gain}! (P{cost}B nagastos)"
                    gs.log(f"Diplomacy: {name} +{gain} rel (P{cost}B)")
                    self.ticker.add(f"DIP Diplomatic effort: {name} relations +{gain}" if LANG=="ENG" else f"DIP Diplomatikong pagsisikap: {name} relasyon +{gain}")
                else:
                    self._dip_msg="Not enough budget!" if LANG=="ENG" else "Hindi sapat ang badyet!"
                break

    def _draw_achievements(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        title_str="MGA TAGUMPAY" if LANG=="FIL" else "ACHIEVEMENTS"
        blit_c(surf,title_str,F["h1"],C_GOLD,8)
        unlocked_str=f"{'Naka-unlock' if LANG=='FIL' else 'Unlocked'}: {len(self.achv.unlocked)}/{len(ACHIEVEMENTS)}"
        surf.blit(F["bd"].render(unlocked_str,True,C_GRY),(20,46))
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        for i,ach in enumerate(ACHIEVEMENTS):
            y=80+i*82
            if y>630: break
            unlocked=ach["id"] in self.achv.unlocked
            bg_col=(20,52,20) if unlocked else (28,28,44)
            border_col=C_GOLD if unlocked else C_GRY
            pygame.draw.rect(surf,bg_col,(20,y,1240,72),border_radius=10)
            pygame.draw.rect(surf,border_col,(20,y,1240,72),2,border_radius=10)
            # Icon
            icon_s=F["h1"].render(ach["icon"],True,C_GOLD if unlocked else C_GRY)
            surf.blit(icon_s,(32,y+18))
            # Name
            name_k="name_en" if LANG=="ENG" else "name"
            desc_k="desc_en" if LANG=="ENG" else "desc"
            nc=C_GOLD if unlocked else (180,180,180)
            surf.blit(F["h2"].render(ach[name_k],True,nc),(80,y+10))
            surf.blit(F["sm"].render(ach[desc_k],True,C_GRY),(80,y+36))
            if unlocked:
                badge=F["sm"].render("+ UNLOCKED" if LANG=="ENG" else "+ NAKAMIT",True,C_GRN)
                surf.blit(badge,(1140-badge.get_width(),y+26))
            else:
                badge=F["sm"].render("LOCKED" if LANG=="ENG" else "NAKA-LOCK",True,(90,90,90))
                surf.blit(badge,(1140-badge.get_width(),y+26))

    def _draw_research(self,surf,mx,my):
        """Research tree -- drawn as branching columns per category."""
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        ENG=LANG=="ENG"
        title_s="RESEARCH & INNOVATION TREE" if ENG else "PUNO NG PANANALIKSIK AT INOBASYON"
        blit_c(surf,title_s,F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        rp=getattr(gs,"research_points",0)
        unlocked=getattr(gs,"research_unlocked",[])
        rp_bar=f"RP: {rp:.0f}  |  {'Unlocked' if ENG else 'Na-unlock'}: {len(unlocked)}/{len(RESEARCH)}  |  {'Edu bonus active' if gs.education>60 else 'Boost with Education'}"
        surf.blit(F["sm"].render(rp_bar,True,C_GRN),(10,44))
        CAT_COLS={"MEDICINE":(0,180,180),"TECH":(40,120,220),"ENERGY":(220,160,0),
                  "AGRI":(60,180,60),"DEFENCE":(200,80,0),"EDUCATION":(160,0,200)}
        CAT_LABELS_E={"MEDICINE":"⚕ MEDICINE","TECH":"💻 TECH","ENERGY":"⚡ ENERGY",
                      "AGRI":"AGR AGRI","DEFENCE":"DEF DEFENCE","EDUCATION":"EDU EDU"}
        CAT_LABELS_F={"MEDICINE":"⚕ MEDISINA","TECH":"💻 TEKNOLOHIYA","ENERGY":"⚡ ENERHIYA",
                      "AGRI":"AGR AGRIKULTURA","DEFENCE":"DEF DEPENSA","EDUCATION":"EDU EDUKASYON"}
        CAT_LABELS=CAT_LABELS_E if ENG else CAT_LABELS_F
        cats={}
        for r in RESEARCH:
            cats.setdefault(r["cat"],[]).append(r)
        cat_list=list(cats.keys()); ncols=len(cat_list); col_w=W//ncols
        if not hasattr(self,"_res_rects"): self._res_rects={}
        self._res_rects.clear()
        for ci,cat in enumerate(cat_list):
            items=cats[cat]; col=CAT_COLS.get(cat,C_GRY); lbl=CAT_LABELS.get(cat,cat)
            cx=ci*col_w; cw=col_w-4
            # Category header
            pygame.draw.rect(surf,lc(C_DARK,col,0.3),(cx+2,62,cw,28),border_radius=6)
            hs=F["sm"].render(lbl,True,col); surf.blit(hs,(cx+cw//2-hs.get_width()//2,68))
            prev_y=None; prev_cx=cx+cw//2
            for ti,r in enumerate(items):
                done=r["id"] in unlocked
                prereqs_met=all(pr in unlocked for pr in r.get("prereq",[]))
                can=(not done and rp>=r["rp_cost"] and prereqs_met and gs.budget>=r["cost"])
                locked_hard=(not done and not prereqs_met)
                by=100+ti*100; bh=84; bx=cx+4; bw=cw-8
                bg=lc(C_PAN,col,0.55) if done else lc(C_DARK,col,0.2 if can else 0.06)
                pygame.draw.rect(surf,bg,(bx,by,bw,bh),border_radius=8)
                bdr=col if done else(C_GOLD if can else((80,80,80) if locked_hard else C_GRY))
                pygame.draw.rect(surf,bdr,(bx,by,bw,bh),2 if done else 1,border_radius=8)
                # Branch line to parent
                if prev_y is not None:
                    mid_x=cx+cw//2
                    pygame.draw.line(surf,lc(C_GRY,col,0.5 if done else 0.2),
                                     (mid_x,prev_y+bh),(mid_x,by),2)
                prev_y=by
                # Content
                name_c=col if done else(C_WHT if can else C_GRY)
                ns=F["sm"].render(r["name"][:22],True,name_c)
                surf.blit(ns,(bx+6,by+4))
                ds=F["sm"].render(r["desc"][:36],True,(140,140,140) if locked_hard else C_GRY)
                surf.blit(ds,(bx+6,by+22))
                rp_s=F["sm"].render(f"RP:{r['rp_cost']}  P{r['cost']}B",True,C_YLW if can else (80,80,80))
                surf.blit(rp_s,(bx+6,by+40))
                if done:
                    ds2=F["sm"].render("+",True,C_GRN); surf.blit(ds2,(bx+bw-20,by+4))
                elif can:
                    ds2=F["sm"].render(">",True,C_GOLD); surf.blit(ds2,(bx+bw-20,by+4))
                    self._res_rects[r["id"]]=pygame.Rect(bx,by,bw,bh)
                elif locked_hard:
                    miss=[pr for pr in r.get("prereq",[]) if pr not in unlocked]
                    if miss:
                        ms=F["sm"].render(f"LCK{miss[0][:12]}",True,(80,80,80))
                        surf.blit(ms,(bx+6,by+58))

    def _handle_research_click(self,ev,gs):
        """Handle clicks in research panel."""
        if not hasattr(self,"_res_rects"): return
        mx,my=pygame.mouse.get_pos()
        _ss=pygame.display.get_surface().get_size()
        imx=int(mx*W/_ss[0]); imy=int(my*H/_ss[1])
        unlocked=getattr(gs,"research_unlocked",[])
        rp=getattr(gs,"research_points",0)
        for rid,r2 in self._res_rects.items():
            if r2.collidepoint(imx,imy):
                res=next((x for x in RESEARCH if x["id"]==rid),None)
                if res and rid not in unlocked and rp>=res["rp_cost"]:
                    if all(pr in unlocked for pr in res.get("prereq",[])):
                        gs.research_points-=res["rp_cost"]
                        gs.budget-=res["cost"]
                        unlocked.append(rid)
                        gs.research_unlocked=unlocked
                        for stat,d in res["fx"].items():
                            if hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                        gs.clamp()
                        nm="name_en" if LANG=="ENG" else "name"
                        gs.log(f"RP Research unlocked: {res[nm] if nm in res else res['name']}")
                        self.ticker.add(f"RP {'Research unlocked' if LANG=='ENG' else 'Pananaliksik nabuksan'}: {res['name']}")
        self._res_rects={}

    def _draw_events(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("ev_title"),F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        for i,entry in enumerate(gs.event_log):
            y=58+i*28-self.ev_scroll
            if y<50 or y>670: continue
            c=C_RL if "!" in entry else C_GRN if ("prosecute" in entry.lower() or "fund" in entry.lower()) else C_WHT
            surf.blit(F["sm"].render(entry[:100],True,c),(20,y))

    def _draw_typhoon_log(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("ty_log_title"),F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        headers=[T("ty_log_yr"),T("ty_log_name"),T("ty_log_cat"),T("ty_log_reg"),T("ty_log_dmg"),T("ty_log_out")]
        xs=[20,100,220,280,450,610]
        for j,(h,x) in enumerate(zip(headers,xs)): surf.blit(F["h2"].render(h,True,C_GD),(x,46))
        pygame.draw.line(surf,C_GD,(20,66),(1260,66),1)
        for i,t in enumerate(gs.typhoon_history):
            y=76+i*26-self.ty_scroll
            if y<66 or y>670: continue
            oc=C_RL if t["outcome"]=="KULANG" else C_GRN if t["outcome"]=="TAMANG" else C_GOLD
            vals=[str(t["year"]),t["name"],f"Cat {t['cat']}",t["region"],f"P{t['damage']:.0f}B",t["outcome"]]
            for j,(v,x) in enumerate(zip(vals,xs)):
                c=oc if j==5 else C_WHT; surf.blit(F["sm"].render(v,True,c),(x,y))

    def _draw_election_choice(self,surf,mx,my):
        """End-of-term election choice: hold fair, rig, or seize power."""
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
        pygame.draw.rect(surf,C_PAN,(220,90,840,530),border_radius=14)
        pygame.draw.rect(surf,C_GOLD,(220,90,840,530),2,border_radius=14)
        gs=self.gs; ENG=LANG=="ENG"
        title="END OF TERM -- WHAT NEXT?" if ENG else "KATAPUSAN NG TERMINO -- ANO ANG SUSUNOD?"
        blit_c(surf,title,F["h1"],C_GOLD,104)
        sub=f"Approval: {gs.approval_rating:.0f}%  |  Term {gs.term}"
        blit_c(surf,sub,F["bd"],C_GRY,140)
        pygame.draw.line(surf,C_GD,(240,162),(1040,162),1)
        opts=[
            ("VOTE","Hold Fair Election" if ENG else "Magtayo ng Malinis na Halalan",
             "+Trust +Press Freedom" if ENG else "+Tiwala +Kalayaan ng Pindutan",
             {"public_trust":12,"press_freedom":8},(24,72,24)),
            ("RIG","Rig the Election -- Become Dictator" if ENG else "Dayain ang Halalan -- Maging Diktador",
             "+Auth Power, system >> Authoritarian Dictatorship" if ENG else "+Auth Power, sistema >> Authoritarian Dictatorship",
             {"auth_power":22,"corruption":18,"public_trust":-14,"rel_un":-12,"rigged_election":1},(80,20,20)),
            ("AUTH","Seize Power -- Declare Emergency Rule" if ENG else "Agawin ang Kapangyarihan -- Ideklara ang Emergency Rule",
             "Become Benevolent Authoritarian -- iron order" if ENG else "Maging Benevolent Authoritarian -- bakal na pagkakasunod-sunod",
             {"auth_power":16,"public_trust":-8,"seize_power":1},(80,40,10)),
            ("RETIRE","Retire -- Step Down" if ENG else "Magbitiw na",
             "Legacy secured; game ends" if ENG else "Legacy natiyak; tapos ang laro",
             {"retire":1},(30,60,80)),
            ("EXTEND","Extend via Charter Change" if ENG else "Pahabain sa Charter Change",
             "+Auth Power (emergency powers)" if ENG else "+Auth Power (emergency powers)",
             {"auth_power":14,"public_trust":-10,"press_freedom":-8},(70,40,10)),
        ]
        if not hasattr(self,"_el_btns") or len(self._el_btns)!=len(opts):
            self._el_btns=[Btn(240,178+i*74,840,68,"",fk="bd") for i in range(len(opts))]
        if not hasattr(self,"_el_btns"):
            self._el_btns=[Btn(240,180+i*90,840,76,"",fk="bd") for i in range(4)]
        for i,((icon,lbl,desc,fx,col),btn) in enumerate(zip(opts,self._el_btns)):
            y=180+i*90
            hov=btn.r.collidepoint(mx,my)
            pygame.draw.rect(surf,lc(C_PAN,col,0.4 if hov else 0.15),(240,y,840,76),border_radius=10)
            pygame.draw.rect(surf,C_GOLD if hov else C_GD,(240,y,840,76),2,border_radius=10)
            surf.blit(F["h1"].render(icon,True,C_GOLD),(256,y+14))
            surf.blit(F["h2"].render(lbl,True,C_WHT),(310,y+10))
            surf.blit(F["sm"].render(desc,True,C_GRY),(310,y+42))
            btn.r=pygame.Rect(240,y,840,76)
            btn.upd(mx,my)

    def _handle_election_choice(self,ev,gs):
        if not hasattr(self,"_el_btns"): return False
        ENG=LANG=="ENG"
        opts=[
            {"public_trust":12,"press_freedom":8},
            {"auth_power":22,"corruption":18,"public_trust":-14,"rel_un":-12,"rigged_election":1},
            {"auth_power":16,"public_trust":-8,"seize_power":1},
            {"retire":1},
            {"auth_power":14,"public_trust":-10,"press_freedom":-8},
        ]
        for i,btn in enumerate(self._el_btns):
            if btn.clicked(ev):
                fx=opts[i]
                for stat,d in fx.items():
                    if stat=="seize_power": gs.political_system="Benevolent Authoritarianism"
                    elif stat=="rigged_election": gs.flags["rigged_election"]=True
                    elif stat=="retire": gs.flags["retired"]=True; gs.flags["term_limit"]=True
                    elif stat=="budget": gs.budget+=d
                    elif hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                if fx.get("rigged_election"):
                    gs.political_system="Authoritarian Dictatorship"
                    gs.log("! Election rigged -- system changed to Authoritarian Dictatorship")
                    self.ticker.add("! Election rigged! The administration seizes power." if ENG
                                    else "! Dayaan ang halalan! Sinaklaw ng administrasyon ang kapangyarihan.")
                gs.clamp()
                self.sub=None
                if hasattr(self,"_el_btns"): del self._el_btns
                return True
        return False

    def _draw_political_shows(self,surf,mx,my):
        """Political shows: rallies, parades, interviews, debates."""
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        title="POLITICAL SHOWS & EVENTS" if LANG=="ENG" else "MGA POLITICAL SHOWS AT EVENTS"
        blit_c(surf,title,F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs; ENG=LANG=="ENG"
        hint=("Organise public events to shape your image. Effects vary -- some build trust, others risk backlash."
              if ENG else
              "Mag-organisa ng mga pampublikong events para sa inyong imahe. Iba-iba ang epekto -- may nagpapalakas, may mapanganib.")
        surf.blit(F["sm"].render(hint,True,C_GRY),(20,46))
        SHOWS=[
            {"id":"ps_parade","icon":"🪖","name":"Military Parade" if ENG else "Military Parade",
             "desc":"Show AFP strength -- boosts military morale & national pride" if ENG else "Ipakita ang lakas ng AFP -- boosts military morale",
             "fx":{"military":7,"public_trust":5,"sovereignty":4,"budget":-50},"cost":50},
            {"id":"ps_rally","icon":"MIC","name":"National Unity Rally" if ENG else "National Unity Rally",
             "desc":"Massive public rally -- high trust if approval >50, backfire if <30" if ENG else "Malaking rally -- epektibo kung approval >50",
             "fx_hi":{"public_trust":14,"approval_rating":3,"budget":-30},"fx_lo":{"public_trust":-8,"budget":-30},"cost":30},
            {"id":"ps_interview","icon":"TV","name":"Primetime TV Interview" if ENG else "Primetime TV Interview",
             "desc":"Live interview -- transparency builds trust" if ENG else "Live interview -- ang transparency ay nagtatayo ng tiwala",
             "fx":{"public_trust":8,"press_freedom":6},"cost":0},
            {"id":"ps_debate","icon":"Sword","name":"Public Debate vs Opposition" if ENG else "Public Debate vs Oposisyon",
             "desc":"High risk, high reward -- win: +14 Trust, lose: -10 Trust" if ENG else "Mataas ang panganib -- manalo: +14, matalo: -10",
             "fx_win":{"public_trust":14},"fx_lose":{"public_trust":-10},"cost":0},
            {"id":"ps_davos","icon":"WORLD","name":"World Stage Appearance" if ENG else "World Stage Appearance",
             "desc":"Speak at international forum -- raise PH profile globally" if ENG else "Magsalita sa international forum -- itaas ang profile ng PH",
             "fx":{"rel_un":10,"rel_us":5,"rel_asean":5,"budget":-40},"cost":40},
            {"id":"ps_heritage","icon":"HRTG","name":"National Heritage Festival" if ENG else "National Heritage Festival",
             "desc":"Celebrate Filipino culture -- boosts trust & tourism economy" if ENG else "Ipagdiwang ang kulturang Filipino -- boosts trust & economy",
             "fx":{"public_trust":9,"economy":4,"budget":-25},"cost":25},
        ]
        if not hasattr(self,"_ps_btns"):
            self._ps_btns=[Btn(16,82+i*92,1248,82,"",fk="bd") for i in range(len(SHOWS))]
        for i,(sh,btn) in enumerate(zip(SHOWS,self._ps_btns)):
            y=82+i*92
            if y>630: break
            done=sh["id"] in getattr(gs,"political_shows_done",[])
            hov=btn.r.collidepoint(mx,my)
            col=(24,52,24) if done else(20,40,18) if hov else(14,28,14)
            pygame.draw.rect(surf,lc(C_PAN,col,0.5 if hov else 0.2),(16,y,1248,82),border_radius=9)
            pygame.draw.rect(surf,C_GOLD if hov else(C_GD if not done else C_GRN),(16,y,1248,82),1+(1 if done else 0),border_radius=9)
            surf.blit(F["h1"].render(sh["icon"],True,C_GOLD),(28,y+18))
            surf.blit(F["h2"].render(sh["name"],True,C_GOLD if hov else C_WHT),(78,y+10))
            surf.blit(F["sm"].render(sh["desc"],True,C_GRY),(78,y+40))
            cost=sh.get("cost",0)
            can=gs.budget>=cost
            cs=F["sm"].render(f"P{cost}B" if cost>0 else "FREE" if LANG=="ENG" else "LIBRE",True,C_GRN if can else C_RL)
            surf.blit(cs,(1220-cs.get_width(),y+30))
            if done:
                bd=F["sm"].render("+ DONE" if ENG else "+ TAPOS",True,C_GRN)
                surf.blit(bd,(1180-bd.get_width(),y+58))
            btn.r=pygame.Rect(16,y,1248,82); btn.upd(mx,my)
        self._ps_shows=SHOWS

    def _handle_political_shows_click(self,ev,gs):
        if not hasattr(self,"_ps_btns") or not hasattr(self,"_ps_shows"): return
        ENG=LANG=="ENG"
        for i,(sh,btn) in enumerate(zip(self._ps_shows,self._ps_btns)):
            if btn.clicked(ev):
                cost=sh.get("cost",0)
                if gs.budget<cost:
                    gs.log("Hindi sapat ang badyet!" if not ENG else "Not enough budget!")
                    return
                gs.budget-=cost
                # Apply FX
                if "fx" in sh:
                    for stat,d in sh["fx"].items():
                        if stat=="budget": gs.budget+=d
                        elif hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                elif "fx_hi" in sh:  # rally -- depends on approval
                    fx=sh["fx_hi"] if gs.approval_rating>50 else sh["fx_lo"]
                    for stat,d in fx.items():
                        if stat=="budget": gs.budget+=d
                        elif hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                elif "fx_win" in sh:  # debate -- random win/lose
                    win=random.random()>0.4
                    fx=sh["fx_win"] if win else sh["fx_lose"]
                    for stat,d in fx.items():
                        if hasattr(gs,stat): setattr(gs,stat,getattr(gs,stat)+d)
                    gs.log(f"Debate: {'Won!' if win else 'Lost.'}" if ENG else f"Debate: {'Nanalo!' if win else 'Natalo.'}")
                if not hasattr(gs,"political_shows_done"): gs.political_shows_done=[]
                if sh["id"] not in gs.political_shows_done:
                    gs.political_shows_done.append(sh["id"])
                gs.clamp()
                self.ticker.add(f"TV {sh['name']}: political show completed" if ENG
                                else f"TV {sh['name']}: natapos ang political show")
                gs.log(f"Political show: {sh['name']}")

    def _draw_annual(self,surf,mx,my):
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
        pygame.draw.rect(surf,C_PAN,(290,120,700,450),border_radius=12)
        pygame.draw.rect(surf,C_GOLD,(290,120,700,450),2,border_radius=12)
        blit_c(surf,T("annual_title"),F["h1"],C_GOLD,132)
        for i,line in enumerate(self.annual_txt[:16]):
            s=F["bd"].render(line,True,C_WHT); surf.blit(s,(310,172+i*24))
        self.ok_btn.upd(mx,my); self.ok_btn.draw(surf)

    def _draw_typhoon_resolve(self,surf,mx,my):
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,180)); surf.blit(ov,(0,0))
        pygame.draw.rect(surf,C_PAN,(260,100,760,500),border_radius=12)
        pygame.draw.rect(surf,C_RL,(260,100,760,500),2,border_radius=12)
        blit_c(surf,T("ty_title"),F["h1"],C_RL,114)
        ty=self.ty_season; total=sum(t["damage"] for t in ty)
        lines=[T("ty_hit").format(n=len(ty)),
               T("ty_total").format(v=total),
               T("ty_storms")]
        for t in ty: lines.append(f"  * {t['name']} (Cat {t['cat']}) >> {t['region']} -- P{t['damage']:.0f}B")
        lines+=["",T("ty_alloc_q")]
        for i,ln in enumerate(lines[:14]): surf.blit(F["bd"].render(ln,True,C_WHT),(280,160+i*24))
        for b in self.rel_btns.values(): b.upd(mx,my); b.draw(surf)

    def _draw_pause(self,surf,mx,my):
        ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,160)); surf.blit(ov,(0,0))
        pygame.draw.rect(surf,C_PAN,(440,200,400,350),border_radius=14)
        pygame.draw.rect(surf,C_GOLD,(440,200,400,350),2,border_radius=14)
        blit_c(surf,"PAUSE" if LANG=="ENG" else "SANDALI",F["h1"],C_GOLD,216)
        for b in self.pbtn.values(): b.upd(mx,my); b.draw(surf)

    # ── main draw ──
    def draw(self,surf,mx,my):
        self.achv.upd()
        self.achv.check(self.gs)
        # Refresh translatable labels each frame (language may change)
        self.nav["policies"].lbl=T("nav_policies"); self.nav["budget"].lbl=T("nav_budget")
        self.nav["events"].lbl=T("nav_events");     self.nav["typhoon"].lbl=T("nav_typhoon")
        self.nav["achiev"].lbl=T("nav_achiev");     self.nav["research"].lbl=T("nav_research")
        self.nav["diplo"].lbl=T("nav_diplo");       self.nav["next"].lbl=T("nav_next")
        self.nav["pshows"].lbl="SHOWS" if LANG=="ENG" else "SHOWS"
        self.ok_btn.lbl=T("ok_btn")
        self.pbtn["resume"].lbl=T("pause_resume");  self.pbtn["save"].lbl=T("pause_save")
        self.pbtn["menu"].lbl=T("pause_menu");      self.pbtn["quit"].lbl=T("pause_quit")
        self.rel_btns["low"].lbl=T("relief_low");   self.rel_btns["mid"].lbl=T("relief_mid")
        self.rel_btns["high"].lbl=T("relief_high")
        gbg_menu(surf, getattr(self,'_t',0)); self._t=getattr(self,'_t',0)+0.016
        self._topbar(surf)
        self._draw_cult_overlay(surf)
        if self.sub is None:
            self._map(surf,mx,my)
            self._right(surf)
            self._navbar(surf,mx,my)
            if self.card.active: self.card.upd(mx,my); self.card.draw(surf)
        elif self.sub=="policies":
            self._draw_policies(surf,mx,my)
        elif self.sub=="budget":
            self._draw_budget(surf,mx,my)
        elif self.sub=="events":
            self._draw_events(surf,mx,my)
        elif self.sub=="achiev":
            self._draw_achievements(surf,mx,my)
        elif self.sub=="research":
            self._draw_research(surf,mx,my)
        elif self.sub=="diplo":
            self._draw_diplomacy(surf,mx,my)
        elif self.sub=="pshows":
            self._draw_political_shows(surf,mx,my)
        elif self.sub=="election_choice":
            self._map(surf,mx,my); self._right(surf)
            self._draw_election_choice(surf,mx,my)
        elif self.sub=="typhoon":
            self._draw_typhoon_log(surf,mx,my)
        elif self.sub=="pause":
            self._map(surf,mx,my); self._right(surf); self._navbar(surf,mx,my)
            self._draw_pause(surf,mx,my)
        elif self.sub=="annual":
            self._map(surf,mx,my); self._right(surf)
            self._draw_annual(surf,mx,my)
        elif self.sub=="typhoon_resolve":
            self._map(surf,mx,my); self._right(surf)
            self._draw_typhoon_resolve(surf,mx,my)
        # Achievements popup always on top
        self.achv.draw(surf)
        # Update live situation ticker every 5 frames
        if pygame.time.get_ticks() % 300 < 50:
            self._live_ticker()

    # ── handle ──
    def handle(self,ev):
        gs=self.gs
        # Scale raw window mouse position to internal 1280×720 coords
        _raw=pygame.mouse.get_pos(); _ss=pygame.display.get_surface().get_size()
        mx=int(_raw[0]*W/_ss[0]); my=int(_raw[1]*H/_ss[1])
        # sub-screen close buttons
        if self.sub in("policies","budget","events","typhoon","achiev","research","diplo","pshows"):
            if ev.type==pygame.MOUSEBUTTONDOWN and pygame.Rect(1140,4,132,34).collidepoint(ev.pos):
                self.sub=None; return None
            if self.sub=="diplo" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                self._handle_diplomacy_click(ev,self.gs)
            if self.sub=="pshows" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                self._handle_political_shows_click(ev,self.gs)
            if self.sub=="research" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                self._handle_research_click(ev,self.gs)
            if self.sub=="budget" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                gs=self.gs; alloc=gs.budget_alloc; keys=list(alloc.keys())
                bx=160; bw=700; by=406
                for i,k in enumerate(keys):
                    y=by+i*36
                    mr=pygame.Rect(bx-30,y,26,24)
                    pr=pygame.Rect(bx+bw+4,y,26,24)
                    if mr.collidepoint(mx,my) and alloc[k]>2:
                        alloc[k]-=2
                        # Add 2% back to the next sector
                        nk=keys[(i+1)%len(keys)]
                        alloc[nk]=min(alloc[nk]+2,60)
                    elif pr.collidepoint(mx,my) and alloc[k]<60:
                        alloc[k]+=2
                        nk=keys[(i-1)%len(keys)]
                        alloc[nk]=max(alloc[nk]-2,2)
            if ev.type==pygame.MOUSEWHEEL:
                if self.sub=="policies": self.pol_scroll=max(0,self.pol_scroll-ev.y*30)
                elif self.sub=="events": self.ev_scroll=max(0,self.ev_scroll-ev.y*30)
                elif self.sub=="typhoon": self.ty_scroll=max(0,self.ty_scroll-ev.y*30)
            if self.sub=="policies" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                avail=self.pol.available(gs)
                for i,p in enumerate(avail):
                    y=78+i*54-self.pol_scroll
                    if pygame.Rect(28,y,1010,46).collidepoint(mx,my):
                        r=self.pol.toggle(gs,p["id"])
                        if r.startswith("max"):
                            gs.log(f"Dapat maximum {r[3:]} policies lang")
                        elif r.startswith("system_changed:"):
                            new_sys=r.split(":",1)[1]
                            self.ticker.add(f"SYS Political system changed to: {new_sys}")
                            # rebuild nav so labels stay fresh
                            self._make_nav()
                        elif r=="same":
                            gs.log("Kasalukuyang sistema na iyon.")
                        else:
                            gs.log(f"Policy {'enabled' if r=='on' else 'disabled'}: {p['name']}")
            return None
        if self.sub=="pause":
            for k,b in self.pbtn.items():
                if b.clicked(ev):
                    if k=="resume": self.sub=None
                    elif k=="save": SaveManager.save(self.slot,gs.to_dict()); gs.log("Game saved."); self.sub=None
                    elif k=="menu": return "menu"
                    elif k=="quit": pygame.quit(); sys.exit()
            return None
        if self.sub=="annual":
            if self.ok_btn.clicked(ev):
                if hasattr(self,"_queued_sub"):
                    self.sub=self._queued_sub
                    del self._queued_sub
                else:
                    self.sub=None
            return None
        if self.sub=="election_choice":
            self._handle_election_choice(ev,self.gs)
            return None
        if self.sub=="typhoon_resolve":
            relief_map={"low":100,"mid":250,"high":400}
            for k,b in self.rel_btns.items():
                if b.clicked(ev):
                    res=self.ty_eng.resolve(gs,self.ty_season,relief_map[k])
                    gs.log(f"Typhoon season: {res['n']} {T('ty_log_name').lower()}, P{res['total']:.0f}B -- {res['outcome']}")
                    self.ticker.add(f"TY {T('ty_log_name')} season done -- {res['outcome']}")
                    self.ty_season=[]
                    # Go to election choice if term ended and not authoritarian
                    if getattr(self,"_queued_election",False):
                        self.sub="election_choice"
                        self._queued_election=False
                    else:
                        self.sub=None
            return None
        # main screen card
        if self.card.active:
            self.card.handle(ev,gs)
            return None
        # nav
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            for k,b in self.nav.items():
                if b.clicked(ev):
                    if k in("policies","budget","events","typhoon","achiev","research","diplo","pshows"): self.sub=k
                    elif k=="next": self._advance()
            if self.hover_r: self.sel_r=None if self.sel_r==self.hover_r else self.hover_r
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_ESCAPE: self.sub="pause"
            elif ev.key in(pygame.K_SPACE,pygame.K_RETURN) and self.sub is None: self._advance()
        return None

    def _advance(self):
        gs=self.gs
        gs.month+=1
        # Reset shows so player can run new shows each month
        if hasattr(gs,"political_shows_done"): gs.political_shows_done=[]
        # Apply active policies this month (cost/12 + stat/12)
        self.pol.monthly(gs)
        # GDP grows every month based on economy stat
        gs.update_economic_indicators()  # updates GDP, growth, unemployment, inflation
        if gs.month>12:
            gs.month=1; gs.year+=1
            self._do_year_end()
        else:
            # monthly: maybe fire event
            diff_f={"ESTUDYANTE":0.65,"SENADOR":0.85,"PANGULO":1.0}.get(gs.difficulty,0.85)
            if random.random()<diff_f:
                pool=[e for e in EVENTS if not(e.get("sys") and gs.political_system not in e.get("sys",[]))]
                if pool:
                    chosen_ev=random.choice(pool)
                    def cb(choice,_ev=chosen_ev): self.ticker.add(f"{E_T(_ev,'title')}: {choice}")
                    self._event_queue.append((chosen_ev,cb))
                    if not self.card.active and self._event_queue:
                        ev2,cb2=self._event_queue.pop(0); self.card.show(ev2,cb2)
        gs.compute_approval()
        gs.compute_regional_stats()
        gs.clamp()
        self._check_dictator_death()
        self._check_gameover()

    def _do_year_end(self):
        gs=self.gs
        self.pol.annual(gs)   # research tier check
        self.bud.year_end(gs); gs.compute_approval()
        gs.clamp()
        if gs.approval_rating<20: gs.consecutive_low+=1
        else: gs.consecutive_low=0
        # Typhoon season
        self.ty_season=self.ty_eng.season(gs)
        for t in self.ty_season: self.ticker.add(f"TY {t['name']} Cat {t['cat']} -- {t['region']}")
        # Annual summary
        self.annual_txt=[
            T("ann_year_done").format(y=gs.year-1),
            T("ann_budget").format(b=gs.budget,d=gs.debt),
            T("ann_appr").format(a=gs.approval_rating),
            f"Economy: {gs.economy:.1f}  Trust: {gs.public_trust:.0f}  Health: {gs.health:.0f}",
            f"Education: {gs.education:.1f}  Infra: {gs.infrastructure:.0f}",
            f"Corruption: {gs.corruption:.1f}  Inequality: {gs.inequality:.0f}",
            f"US: {gs.rel_us:.0f}  China: {gs.rel_china:.0f}  ASEAN: {gs.rel_asean:.0f}",
            T("ann_policies").format(n=len(gs.active_policies)),
            T("ann_typhoons").format(n=len(self.ty_season)),
        ]
        if gs.budget<0: self.annual_txt.append(T("ann_deficit").format(v=abs(gs.budget)))
        if gs.corruption>75: self.annual_txt.append(T("ann_corr_warn"))
        if gs.approval_rating<25: self.annual_txt.append(T("ann_appr_warn"))
        # Auto save
        SaveManager.save(self.slot,gs.to_dict())
        # Track dictator age and trigger old-age event
        if gs.political_system in AUTH_SYSTEMS:
            gs.dictator_age=getattr(gs,"dictator_age",0)+1
            if gs.dictator_age>=15 and not gs.flags.get("old_age_triggered"):
                gs.flags["old_age_triggered"]=True
                old_ev=next((e for e in EVENTS if e["id"]=="old_age_health"),None)
                if old_ev: self.card.show(old_ev)
        # Check term
        years_in_term=gs.year-2025-(gs.term-1)*6
        if years_in_term>=6:
            gs.term+=1
            if gs.term>2:
                # End of max terms -- show election choice
                gs.flags["term_limit"]=True
                if gs.political_system not in AUTH_SYSTEMS:
                    self._queued_election=True  # show election screen after annual
            elif gs.political_system not in AUTH_SYSTEMS:
                self._queued_election=True  # every 6 years, offer election choice
        # Show annual then typhoon resolve (or election)
        self.sub="annual"
        self._queued_sub="typhoon_resolve"


    def _check_dictator_death(self):
        """Die of old age if dictator for 20+ years (age mid-80s max)."""
        gs=self.gs
        if gs.political_system not in AUTH_SYSTEMS: return
        years_as_auth=getattr(gs,"dictator_age",0)
        # Base chance scales up sharply after year 15
        if years_as_auth >= 20:
            chance = 0.15 + (years_as_auth-20)*0.1
            if random.random() < min(chance, 0.95):
                gs.flags["died_old_age"]=True

    def _check_gameover(self):
        if self.card.active: return   # don't interrupt mid-event
        gs=self.gs
        # People Power: low approval but mass support saves you (one chance)
        if gs.approval_rating<15 and not gs.flags.get("people_power_tried"):
            if gs.public_trust>60 and random.random()<0.45:
                gs.flags["people_power_triggered"]=True
                gs.flags["people_power_tried"]=True
                gs.approval_rating+=20; gs.public_trust-=12; gs.clamp()
                gs.log("PP People Power! Mass mobilisation averts impeachment -- but trust takes a hit.")
                self.ticker.add("PP PEOPLE POWER RALLY saves administration from collapse!" if LANG=="ENG"
                                else "PP PEOPLE POWER RALLY -- Naligtas ang administrasyon!")
                return
        if gs.approval_rating<15: gs.flags["impeached"]=True
        if gs.budget<-3000: gs.flags["economic_collapse"]=True
        # Coup trigger in extreme military + low trust scenario
        if gs.military>75 and gs.approval_rating<20 and gs.public_trust<25:
            if random.random()<0.3:
                gs.flags["coup_overthrow"]=True; gs.flags["impeached"]=True
                gs.log("CUP Military coup -- the generals have seized the palace!")
        if gs.consecutive_low>=2 and random.random()<0.5: gs.flags["snap_election"]=True

    @property
    def game_over_reason(self):
        gs=self.gs
        if gs.flags.get("died_old_age"): return "DIED OF OLD AGE -- Your rule ended naturally." if LANG=="ENG" else "NAMATAY SA KATANDAAN -- Ang inyong pamumuno ay natapos."
        if gs.flags.get("coup_overthrow"): return "MILITARY COUP -- The generals have seized power!" if LANG=="ENG" else "KUDETA -- Sinaklaw ng mga heneral ang kapangyarihan!"
        if gs.flags.get("impeached"): return T("go_reason_imp")
        if gs.flags.get("economic_collapse"): return T("go_reason_eco")
        return ""

    @property
    def is_game_over(self):
        return bool(self.gs.flags.get("impeached") or self.gs.flags.get("economic_collapse") or self.gs.flags.get("died_old_age"))

    @property
    def is_victory(self):
        gs=self.gs
        return gs.flags.get("term_limit") or (gs.year-2025)>=12


# ── GAME OVER SCREEN ─────────────────────────────────────────
class GameOverScreen:
    def __init__(self,reason,gs):
        self.reason=reason; self.gs=gs
        self.retry=Btn(W//2-185,510,170,52,T("go_retry")); self.menu=Btn(W//2+15,510,170,52,T("go_menu"))

    def draw(self,surf,mx,my):
        gbg(surf)
        self.retry.lbl=T("go_retry"); self.menu.lbl=T("go_menu")
        self.retry.upd(mx,my); self.menu.upd(mx,my)
        blit_c(surf,T("go_title"),F["H"],C_RL,160,shad=True)
        blit_c(surf,self.reason,F["h2"],C_WHT,250)
        blit_c(surf,T("go_appr").format(a=self.gs.approval_rating),F["h1"],C_GOLD,310)
        blit_c(surf,T("go_years").format(y=self.gs.year-2025),F["bd"],C_GRY,366)
        self.retry.draw(surf); self.menu.draw(surf)

    def handle(self,ev):
        if self.retry.clicked(ev): return "retry"
        if self.menu.clicked(ev): return "menu"
        return None

# ── VICTORY SCREEN ───────────────────────────────────────────
class VictoryScreen:
    # Grade >> STRINGS key
    GRADE_KEY={90:"vic_s",75:"vic_a",60:"vic_b",40:"vic_c",0:"vic_f"}

    def __init__(self,gs):
        self.gs=gs
        a=gs.approval_rating
        self.grade="S" if a>88 else "A" if a>75 else "B" if a>60 else "C" if a>45 else "D" if a>30 else "F"
        self._grade_skey=next(k for mn,k in sorted(self.GRADE_KEY.items(),reverse=True) if a>=mn)
        self.menu=Btn(490,560,300,52,T("vic_menu"))

    def draw(self,surf,mx,my):
        gbg(surf); draw_sun(surf,W//2,100,44)
        self.menu.lbl=T("vic_menu"); self.menu.upd(mx,my)
        blit_c(surf,T("vic_title"),F["h1"],C_GOLD,160,shad=True)
        gc=C_GRN if self.grade in("S","A") else C_YLW if self.grade=="B" else C_RL
        blit_c(surf,f"GRADE: {self.grade}",F["H"],gc,204,shad=True)
        gs=self.gs
        title_txt=T(self._grade_skey)
        lines=[title_txt,"",T("vic_stats"),
               f"Economy {gs.economy:.0f}  |  Trust {gs.public_trust:.0f}  |  Health {gs.health:.0f}",
               f"Corruption {gs.corruption:.0f}  |  Sovereignty {gs.sovereignty:.0f}",
               T("go_appr").format(a=gs.approval_rating)+"  |  "+T("vic_yrs").format(y=gs.year-2025),
               T("vic_ty").format(n=len(gs.typhoon_history)),
               T("vic_sys").format(s=gs.political_system)]
        for i,ln in enumerate(lines):
            s=F["bd"].render(ln,True,C_WHT); surf.blit(s,(W//2-s.get_width()//2,296+i*28))
        self.menu.draw(surf)

    def handle(self,ev):
        if self.menu.clicked(ev): return "menu"
        return None

# ── MAIN GAME LOOP ───────────────────────────────────────────
def main():
    global SPLASH_ENABLED, _CLICK_SND
    pygame.init()
    # ── Sound ──────────────────────────────────────────────────
    try:
        pygame.mixer.pre_init(44100, -16, 1, 256)
        pygame.mixer.init()
        try:
            import numpy as np
            dur=0.045; sr=44100
            t=np.linspace(0,dur,int(sr*dur),False)
            wave=(np.sin(2*np.pi*880*t)*np.exp(-t*55)*26000).astype(np.int16)
            snd=pygame.sndarray.make_sound(wave)
            snd.set_volume(0.5)
            _CLICK_SND=snd
            print("[OK] Click sound loaded via numpy")
        except Exception as _ne:
            # Fallback: generate beep without numpy using array module
            try:
                import array, math as _math
                dur=0.05; sr=44100; n=int(sr*dur)
                buf=array.array('h',[int(24000*_math.sin(2*_math.pi*880*i/sr)*max(0,1-i/n*3)) for i in range(n)])
                snd=pygame.sndarray.make_sound(__import__('numpy').frombuffer(buf,dtype='int16')) if False else None
                # Pure pygame fallback
                beep_surf=pygame.Surface((1,1)); pygame.draw.point=lambda *a:None
                snd2=pygame.mixer.Sound(buffer=bytes(buf))
                snd2.set_volume(0.5)
                _CLICK_SND=snd2
                print("[OK] Click sound loaded via array fallback")
            except Exception as _ae:
                print(f"[WARN] Click sound unavailable: {_ae}")
    except Exception as _me:
        print(f"[WARN] Mixer init failed: {_me}")

    def play_click(): _play_click()
    pygame.display.set_caption(TITLE)
    screen=pygame.display.set_mode((W,H),pygame.RESIZABLE)
    clock=pygame.time.Clock()
    surf=pygame.Surface((W,H))
    init_fonts()

    # Load Philippine star image
    _PH_STAR_SURF = None
    try:
        import os as _os
        _star_path = _os.path.join(_os.path.dirname(_os.path.abspath(sys.argv[0])), 'PHILIPPINES_STAR.png')
        if _os.path.exists(_star_path):
            _PH_STAR_SURF = pygame.image.load(_star_path).convert_alpha()
            print(f"[OK] Philippine star loaded: {_star_path}")
    except Exception as _e:
        print(f"[WARN] Could not load star: {_e}")

    # Quit-confirm dialog state
    quit_confirm=False
    qc_save_btn=None; qc_nosave_btn=None; qc_cancel_btn=None

    def make_qc_btns():
        nonlocal qc_save_btn,qc_nosave_btn,qc_cancel_btn
        qc_save_btn   =Btn(W//2-195,370,180,46,"SAVE Save & Quit" if LANG=="ENG" else "SAVE I-save at Lumabas")
        qc_nosave_btn =Btn(W//2+15, 370,180,46,"Quit without saving" if LANG=="ENG" else "Lumabas nang walang save",fk="bd")
        qc_cancel_btn =Btn(W//2-90, 432,182,40,"Cancel" if LANG=="ENG" else "Kanselahin",fk="bd")

    # State machine
    state="splash"
    splash=SplashScreen()
    settings_scr=SettingsScreen()
    setup_a=SetupA(); setup_b=SetupB(); setup_c=SetupC(); setup_d=SetupD()
    menu=MainMenu(); load_scr=LoadScreen()
    gs_tmp=GS()           # accumulate setup choices
    game_scr=None         # GameScreen
    go_scr=None; vic_scr=None
    active_slot=0

    def new_game(gs,slot=None):
        nonlocal game_scr,state,active_slot
        if slot is not None: active_slot=slot
        gs.apply_bonuses()
        game_scr=GameScreen(gs,active_slot); state="game"

    def load_game(slot):
        nonlocal game_scr,state,active_slot
        data=SaveManager.load(slot)
        if data:
            gs=GS.from_dict(data); active_slot=slot
            game_scr=GameScreen(gs,slot); state="game"

    running=True
    while running:
        sw,sh=screen.get_size()
        _raw=pygame.mouse.get_pos()
        mx=int(_raw[0]*W/sw); my=int(_raw[1]*H/sh)
        events=[remap_ev(e,sw,sh) for e in pygame.event.get()]
        for ev in events:
            if ev.type==pygame.QUIT:
                if state=="game" and game_scr:
                    quit_confirm=True; make_qc_btns()
                else:
                    running=False
                break

            # ── quit confirm dialog ──
            if quit_confirm:
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    if qc_save_btn and qc_save_btn.r.collidepoint(ev.pos):
                        play_click()
                        SaveManager.save(active_slot,game_scr.gs.to_dict()); running=False
                    elif qc_nosave_btn and qc_nosave_btn.r.collidepoint(ev.pos):
                        play_click(); running=False
                    elif qc_cancel_btn and qc_cancel_btn.r.collidepoint(ev.pos):
                        play_click(); quit_confirm=False
                continue

            # ── splash ──
            if state=="splash":
                splash.handle(ev)
                if splash.done: state="menu"
                continue   # don't pass splash events to other handlers

            # ── state routing ──
            if state=="menu":
                r=menu.handle(ev)
                if r=="new":
                    play_click()
                    # Find first empty slot; fallback to slot 0
                    slot_idx=next((i for i in range(3) if SaveManager.load(i) is None), 0)
                    active_slot=slot_idx
                    setup_a=SetupA(); setup_b=SetupB(); setup_c=SetupC(); setup_d=SetupD(); gs_tmp=GS(); state="setup_a"
                elif r=="load":   play_click(); load_scr=LoadScreen(); state="load"
                elif r=="settings": play_click(); settings_scr=SettingsScreen(); state="settings"
                elif r=="quit":   play_click(); running=False

            elif state=="setup_a":
                r=setup_a.handle(ev)
                if r: gs_tmp.player_name=r; state="setup_b"
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: state="menu"

            elif state=="setup_b":
                r=setup_b.handle(ev)
                if r: gs_tmp.foreign_stance=r; state="setup_c"
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: state="setup_a"

            elif state=="setup_c":
                r=setup_c.handle(ev)
                if r: gs_tmp.political_system=r; state="setup_d"
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: state="setup_b"

            elif state=="setup_d":
                r=setup_d.handle(ev)
                if r: gs_tmp.difficulty=r; new_game(gs_tmp,0)
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: state="setup_c"

            elif state=="load":
                r=load_scr.handle(ev)
                if r:
                    if r[0]=="back": state="menu"
                    elif r[0]=="load": load_game(r[1])
                    elif r[0]=="newgame":
                        # Start new game in the chosen slot
                        slot_for_new=r[1]
                        setup_a=SetupA(); setup_b=SetupB(); setup_c=SetupC(); setup_d=SetupD()
                        gs_tmp=GS(); active_slot=slot_for_new; state="setup_a"

            elif state=="game" and game_scr:
                r=game_scr.handle(ev)
                if r=="menu": state="menu"
                # check win/lose after every event
                if game_scr and game_scr.is_game_over:
                    go_scr=GameOverScreen(game_scr.game_over_reason,game_scr.gs); state="gameover"
                elif game_scr and game_scr.is_victory:
                    vic_scr=VictoryScreen(game_scr.gs); state="victory"

            elif state=="gameover" and go_scr:
                r=go_scr.handle(ev)
                if r=="menu": state="menu"
                elif r=="retry":
                    gs2=GS(player_name=game_scr.gs.player_name,
                           foreign_stance=game_scr.gs.foreign_stance,
                           difficulty=game_scr.gs.difficulty,
                           political_system=game_scr.gs.political_system)
                    new_game(gs2,active_slot)

            elif state=="victory" and vic_scr:
                r=vic_scr.handle(ev)
                if r=="menu": state="menu"

            elif state=="settings":
                r=settings_scr.handle(ev)
                if r=="back": state="menu"
                if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: state="menu"

        # ── draw ──
        surf.fill(C_BLK)
        if state=="splash":
            splash.update(); splash.draw(surf)
            if splash.done: state="menu"
        elif state=="menu":       menu.upd(mx,my); menu.draw(surf,mx,my)
        elif state=="setup_a":  setup_a.draw(surf,mx,my)
        elif state=="setup_b":  setup_b.draw(surf,mx,my)
        elif state=="setup_c":  setup_c.draw(surf,mx,my)
        elif state=="setup_d":  setup_d.draw(surf,mx,my)
        elif state=="load":     load_scr.draw(surf,mx,my)
        elif state=="game" and game_scr:    game_scr.draw(surf,mx,my)
        elif state=="gameover" and go_scr:  go_scr.draw(surf,mx,my)
        elif state=="victory" and vic_scr:  vic_scr.draw(surf,mx,my)
        elif state=="settings" and settings_scr: settings_scr.draw(surf,mx,my)

        # ── quit-confirm dialog overlay ───────────────────────────
        if quit_confirm and qc_save_btn:
            ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,175)); surf.blit(ov,(0,0))
            dw,dh=520,200; dx,dy=W//2-dw//2,H//2-dh//2
            pygame.draw.rect(surf,C_PAN,(dx,dy,dw,dh),border_radius=12)
            pygame.draw.rect(surf,C_GOLD,(dx,dy,dw,dh),2,border_radius=12)
            msg="Quit without saving?" if LANG=="ENG" else "Lumabas nang hindi nag-se-save?"
            blit_c(surf,msg,F["h2"],C_GOLD,dy+28)
            sub="Your progress will be lost." if LANG=="ENG" else "Mawawala ang iyong progreso."
            blit_c(surf,sub,F["bd"],C_WHT,dy+62)
            for b in(qc_save_btn,qc_nosave_btn,qc_cancel_btn):
                if b: b.upd(mx,my); b.draw(surf)

        # scale to window
        sw,sh=screen.get_size()
        scaled=pygame.transform.scale(surf,(sw,sh))
        screen.blit(scaled,(0,0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__=="__main__":
    main()