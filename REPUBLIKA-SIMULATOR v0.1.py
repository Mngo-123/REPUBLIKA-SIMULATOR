#!/usr/bin/env python3
"""REPUBLIKA SIMULATOR v1.0 — Single-file Pygame political strategy game.
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
LANG = "FIL"   # "FIL" | "ENG"  — toggled by translate button on main menu

STRINGS = {
    # Main menu
    "subtitle"      :{"FIL":"Pamunuan ang Bansa — Itaguyod ang Bayan",
                       "ENG":"Lead the Nation — Defend the People"},
    "btn_new"       :{"FIL":"[ BAGONG LARO ]",     "ENG":"[ NEW GAME ]"},
    "btn_load"      :{"FIL":"[ I-LOAD ]",           "ENG":"[ LOAD GAME ]"},
    "btn_settings"  :{"FIL":"[ MGA SETTING ]",      "ENG":"[ SETTINGS ]"},
    "btn_quit"      :{"FIL":"[ LUMABAS ]",          "ENG":"[ QUIT ]"},
    "disclaimer"    :{"FIL":"v1.0  |  Lahat ng pangalan ay gawa-gawa",
                       "ENG":"v1.0  |  All names are entirely fictional"},
    "translate_btn" :{"FIL":"🌐 EN",               "ENG":"🌐 FIL"},
    # Setup screens
    "step1_title"   :{"FIL":"HAKBANG 1/4 — PANGALAN",
                       "ENG":"STEP 1/4 — YOUR NAME"},
    "step1_prompt"  :{"FIL":"Ilagay ang inyong pangalan, Presidente:",
                       "ENG":"Enter your name, Mr/Ms President:"},
    "step1_err"     :{"FIL":"Maglagay ng pangalan!",
                       "ENG":"Please enter a name!"},
    "step1_confirm" :{"FIL":"[ KUMPIRMAHIN ]",      "ENG":"[ CONFIRM ]"},
    "step2_title"   :{"FIL":"HAKBANG 2/4 — FOREIGN POLICY STANCE",
                       "ENG":"STEP 2/4 — FOREIGN POLICY STANCE"},
    "step3_title"   :{"FIL":"HAKBANG 3/4 — POLITICAL SYSTEM",
                       "ENG":"STEP 3/4 — POLITICAL SYSTEM"},
    "step3_warn"    :{"FIL":"⚠  Ang authoritarian path ay may espesyal na events ngunit mapanganib sa demokrasya",
                       "ENG":"⚠  Authoritarian paths unlock special events but risk democratic stats"},
    "step4_title"   :{"FIL":"HAKBANG 4/4 — ANTAS NG KAHIRAPAN",
                       "ENG":"STEP 4/4 — DIFFICULTY LEVEL"},
    "next_btn"      :{"FIL":"[ SUSUNOD ]",          "ENG":"[ NEXT ]"},
    "start_btn"     :{"FIL":"[ SIMULAN ]",          "ENG":"[ START ]"},
    "back_btn"      :{"FIL":"← BUMALIK",            "ENG":"← BACK"},
    # Load screen
    "load_title"    :{"FIL":"LOAD GAME — PILIIN ANG SLOT",
                       "ENG":"LOAD GAME — CHOOSE A SLOT"},
    "empty_slot"    :{"FIL":"— WALANG DATOS —",     "ENG":"— EMPTY SLOT —"},
    # In-game nav
    "nav_policies"  :{"FIL":"PATAKARAN",            "ENG":"POLICIES"},
    "nav_budget"    :{"FIL":"BADYET",               "ENG":"BUDGET"},
    "nav_events"    :{"FIL":"MGA PANGYAYARI",       "ENG":"EVENTS"},
    "nav_typhoon"   :{"FIL":"BAGYO",                "ENG":"TYPHOONS"},
    "nav_achiev"    :{"FIL":"MGA TAGUMPAY",          "ENG":"ACHIEVEMENTS"},
    "nav_research"  :{"FIL":"PANANALIKSIK",           "ENG":"RESEARCH"},
    "pause_resume"  :{"FIL":"▶ IPAGPATULOY",        "ENG":"▶ RESUME"},
    "pause_save"    :{"FIL":"💾  I-SAVE",           "ENG":"💾  SAVE GAME"},
    "pause_menu"    :{"FIL":"🏠  BUMALIK SA MENU",  "ENG":"🏠  MAIN MENU"},
    "pause_quit"    :{"FIL":"✕  TUMIGIL",           "ENG":"✕  QUIT GAME"},
    # Annual / typhoon panels
    "annual_title"  :{"FIL":"TAUNANG ULAT",         "ENG":"ANNUAL REVIEW"},
    "ok_btn"        :{"FIL":"[ SUSUNOD ]",          "ENG":"[ CONTINUE ]"},
    "ty_title"      :{"FIL":"🌀  ULAT NG BAGYO",   "ENG":"🌀  TYPHOON SEASON REPORT"},
    "relief_low"    :{"FIL":"MABABA  ₱100B",        "ENG":"LOW  ₱100B"},
    "relief_mid"    :{"FIL":"KATAMTAMAN ₱250B",     "ENG":"MODERATE  ₱250B"},
    "relief_high"   :{"FIL":"MATAAS  ₱400B",        "ENG":"HIGH  ₱400B"},
    "close_btn"     :{"FIL":"ISARA",                "ENG":"CLOSE"},
    # Game over / victory
    "go_title"      :{"FIL":"TAPOS NA ANG LARO",    "ENG":"GAME OVER"},
    "go_retry"      :{"FIL":"[ MULI ]",             "ENG":"[ RETRY ]"},
    "go_menu"       :{"FIL":"[ MENU ]",             "ENG":"[ MENU ]"},
    "vic_title"     :{"FIL":"KATAPUSAN NG TERMINO — ULAT",
                       "ENG":"END OF TERM — FINAL REPORT"},
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
    "pol_sys_change":{"FIL":"⚙ PAGBABAGO NG SISTEMA","ENG":"⚙ SYSTEM CHANGE"},
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
    "ty_log_dmg"    :{"FIL":"Pinsala(₱B)",            "ENG":"Damage(₱B)"},
    "ty_log_out"    :{"FIL":"Resulta",                "ENG":"Outcome"},
    # Navbar hint
    "nav_hint"      :{"FIL":"ESC=Menu  SPACE=Susunod na Buwan",
                       "ENG":"ESC=Menu  SPACE=Next Month"},
    # Annual review lines
    "ann_year_done" :{"FIL":"Taon {y} ay tapos na.",      "ENG":"Year {y} is complete."},
    "ann_budget"    :{"FIL":"Badyet: ₱{b:.0f}B  |  Utang: ₱{d:.0f}B",
                       "ENG":"Budget: ₱{b:.0f}B  |  Debt: ₱{d:.0f}B"},
    "ann_appr"      :{"FIL":"Suporta: {a:.1f}%",         "ENG":"Approval: {a:.1f}%"},
    "ann_deficit"   :{"FIL":"⚠ DEPISITO! ₱{v:.0f}B",    "ENG":"⚠ DEFICIT! ₱{v:.0f}B"},
    "ann_corr_warn" :{"FIL":"⚠ Mataas na korapsyon — krisis ang posible!",
                       "ENG":"⚠ High corruption — crisis events likely!"},
    "ann_appr_warn" :{"FIL":"⚠ Napakababang suporta — panganib sa puwesto!",
                       "ENG":"⚠ Very low approval — your position is at risk!"},
    "ann_policies"  :{"FIL":"Aktibong Patakaran: {n}",   "ENG":"Active Policies: {n}"},
    "ann_typhoons"  :{"FIL":"Typhoon season: {n} bagyo",  "ENG":"Typhoon season: {n} storms"},
    # Typhoon resolve lines
    "ty_hit"        :{"FIL":"{n} bagyo ang humampas ngayong taon.",
                       "ENG":"{n} typhoon(s) struck the country this year."},
    "ty_total"      :{"FIL":"Kabuuang pinsala: ₱{v:.0f}B",
                       "ENG":"Total estimated damage: ₱{v:.0f}B"},
    "ty_storms"     :{"FIL":"Mga Bagyo:",              "ENG":"Storms:"},
    "ty_alloc_q"    :{"FIL":"Ilaan ang disaster relief budget:",
                       "ENG":"Allocate disaster relief budget:"},
    # Game over
    "go_reason_imp" :{"FIL":"TINANGGAL SA PWESTO — Masyadong mababa ang suporta",
                       "ENG":"IMPEACHED — Approval rating too low"},
    "go_reason_eco" :{"FIL":"PAGBAGSAK NG EKONOMIYA — Lumampas sa ₱3T ang depisito",
                       "ENG":"ECONOMIC COLLAPSE — Deficit exceeded ₱3T"},
    "go_appr"       :{"FIL":"Panghuling Suporta: {a:.1f}%",    "ENG":"Final Approval: {a:.1f}%"},
    "go_years"      :{"FIL":"Taon ng Serbisyo: {y}",           "ENG":"Years of Service: {y}"},
    # Victory titles
    "vic_s"  :{"FIL":"BAYANI NG BANSA — Ang inyong pamumuno ay magiging modelo sa kasaysayan.",
                "ENG":"HERO OF THE NATION — Your leadership will be a model for generations."},
    "vic_a"  :{"FIL":"MAHUSAY NA LIDER — Ang Pilipinas ay umuunlad dahil sa inyong serbisyo.",
                "ENG":"EXCELLENT LEADER — The Philippines thrived under your service."},
    "vic_b"  :{"FIL":"KATAMTAMANG PANGULO — May magagandang nagawa, may kulang din.",
                "ENG":"DECENT PRESIDENT — Some achievements, but much left undone."},
    "vic_c"  :{"FIL":"MAHINA ANG PAMUMUNO — Ang bansa ay naghirap sa ilalim ng inyong pamumuno.",
                "ENG":"WEAK LEADERSHIP — The country struggled under your governance."},
    "vic_f"  :{"FIL":"TRAYDOR SA SAMBAYANAN — Ang kasaysayan ay hindi magpapatawad sa inyo.",
                "ENG":"BETRAYER OF THE PEOPLE — History will not forgive you."},
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
        "REPUBLIKA SIMULATOR — Simulan ang inyong pamumuno...",
        "Ang administrasyon ay naglunsad ng bagong economic plan para sa mga magsasaka...",
        "Bagyo Egay ay lumakas — Category 4. Signal 3 sa Visayas...",
        "Oposisyon ay nag-rally sa EDSA — 600,000 ang dumalo...",
        "Inflation ay bumaba ng 0.3% ayon sa PSA ngayong buwan...",
        "Kongreso ay nagdebate ng panukalang batas sa health insurance...",
        "BSP ay nagpanatili ng interest rates — ekonomista ay nagpapahayag ng pag-asa...",
    ], "ENG":[
        "REPUBLIKA SIMULATOR — Your mandate awaits...",
        "The administration launches a new economic plan for farmers...",
        "Typhoon Egay intensifies — Category 4. Signal 3 in Visayas...",
        "Opposition holds EDSA rally — 600,000 attend...",
        "Inflation drops 0.3% according to this month's PSA report...",
        "Congress debates proposed health insurance reform bill...",
        "BSP holds interest rates — economists express cautious optimism...",
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
    ("Presidential Republic",       "Classic PH republic — checks & balances",               (30,80,160)),
    ("Parliamentary System",        "PM accountable to legislature; +5 Trust +3 Eco",         (30,120,80)),
    ("Federal Republic",            "Strong regions; +8 Infra −5 Inequality",                 (120,80,30)),
    ("Benevolent Authoritarianism", "Strongman rule for good; −15 Corruption +10 Economy; strict press",  (100,55,160)),
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
    # Handwriting / script font for the splash quote — try nicest first
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

# ── HELPERS ──────────────────────────────────────────────────
def lerp(a,b,t): return a+(b-a)*t
def lc(a,b,t): return tuple(int(lerp(a[i],b[i],max(0,min(1,t)))) for i in range(3))
def clamp(v,lo=0,hi=100): return max(lo,min(hi,v))
def stat_col(v): return C_GRN if v>65 else C_YLW if v>35 else C_RL

def gbg(surf):
    for y in range(H):
        pygame.draw.line(surf,lc(C_NAV,C_DARK,y/H),(0,y),(W,y))

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

def blit_wrap(surf,txt,font,col,x,y,mw,lh=20):
    for i,ln in enumerate(wrap(txt,font,mw)):
        surf.blit(font.render(ln,True,col),(x,y+i*lh))
    return y+len(wrap(txt,font,mw))*lh

def blit_c(surf,txt,font,col,cy,shad=False):
    if shad:
        s=font.render(txt,True,C_BLK); surf.blit(s,(W//2-s.get_width()//2+2,cy+2))
    s=font.render(txt,True,col); surf.blit(s,(W//2-s.get_width()//2,cy))

def draw_sun(surf,cx,cy,r=34):
    pygame.draw.circle(surf,C_GOLD,(cx,cy),r)
    for i in range(8):
        a=math.pi*2*i/8-math.pi/2
        pygame.draw.line(surf,C_GOLD,
            (cx+int(math.cos(a)*(r+4)),cy+int(math.sin(a)*(r+4))),
            (cx+int(math.cos(a)*(r+18)),cy+int(math.sin(a)*(r+18))),3)

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

def fade_surf(surf,alpha):
    ov=pygame.Surface((W,H)); ov.set_alpha(alpha); ov.fill(C_BLK); surf.blit(ov,(0,0))

def remap_ev(ev, sw, sh):
    """Re-map mouse-position fields from real window pixels → internal W×H pixels.
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
    gdp:float=20000.0        # ₱ billions
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
    approval_rating:float=50.0; approval_history:list=field(default_factory=list)
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

    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls,d):
        gs=cls()
        for k,v in d.items():
            if hasattr(gs,k): setattr(gs,k,v)
        return gs

    def update_economic_indicators(self):
        """Derive GDP growth, unemployment, inflation, poverty from stats."""
        self.gdp_growth = round(clamp((self.economy-30)*0.18+2.0,-4,14),1)
        self.gdp = max(5000, self.gdp*(1+self.gdp_growth/100/12))
        self.unemployment = round(clamp(20-self.economy*0.18,2,30),1)
        self.inflation = round(clamp(2+(self.corruption*0.06)+(50-self.economy)*0.04,0.5,22),1)
        self.poverty_rate = round(clamp(5+self.inequality*0.35-(self.economy-30)*0.1,2,60),1)

    def apply_bonuses(self):
        s=self.foreign_stance
        if s=="SOBERANIYA": self.sovereignty+=10; self.public_trust+=5
        elif s=="ALYANSA": self.military+=15; self.economy+=10; self.rel_china-=10
        elif s=="PAKIKIPAG-UGNAYAN": self.infrastructure+=20; self.rel_china+=10; self.sovereignty-=15; self.rel_us-=10
        elif s=="BALANSE": self.rel_us+=5; self.rel_china+=5; self.rel_asean+=5; self.rel_un+=5
        SB={
            "Parliamentary System":{"public_trust":5,"economy":3},
            "Federal Republic":{"infrastructure":8,"inequality":-5},
            "Benevolent Authoritarianism":{"corruption":-15,"economy":10,"public_trust":-5},
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
        if self.corruption>70: b-=(self.corruption-70)*0.35
        if self.political_system=="Benevolent Authoritarianism": b=b*0.85+self.economy*0.15
        elif self.political_system=="Authoritarian Dictatorship": b-=15+self.auth_power*0.2
        self.approval_rating=clamp(b)
        self.approval_history.append(round(self.approval_rating,1))
        if len(self.approval_history)>24: self.approval_history=self.approval_history[-24:]

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
             {"lbl":"Takpan — mapanganib","lbl_en":"Cover it up (risky)","fx":{"corruption":14,"public_trust":-8},"desc":"","desc_en":""},
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
  "flavor":"Plano ng lungsod ang limpyahin ang mga informal settler — kasama ang housing units, livelihood training, at trabaho para sa bawat pamilya.",
  "flavor_en":"The city plans to clear informal settlements — with housing units, livelihood training and jobs for every family. UN-Habitat has praised the programme.",
  "choices":[{"lbl":"Ituloy (buong pakete)","lbl_en":"Proceed (full package)","fx":{"infrastructure":8,"inequality":-8,"public_trust":6,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Palawakin — mas maraming bahay","lbl_en":"Expand — build more homes","fx":{"infrastructure":5,"inequality":-14,"public_trust":10,"budget":-220},"desc":"","desc_en":""},
             {"lbl":"Kanselahin","lbl_en":"Cancel the project","fx":{"infrastructure":-2,"public_trust":4},"desc":"","desc_en":""}]},
 {"id":"ineq2","cat":"INEQUALITY",
  "title":"DEMOLISYON — WALANG RELOKASYON","title_en":"DEMOLITION — NO RELOCATION",
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
  "flavor":"Malnutrition crisis sa Eastern Visayas — malayo sa food supply at walang sapat na kabuhayan.",
  "flavor_en":"Malnutrition crisis hits Eastern Visayas — remote areas cut off from food supply and livelihood.",
  "choices":[{"lbl":"Emergency food aid","lbl_en":"Emergency food aid","fx":{"health":7,"inequality":-5,"public_trust":6,"budget":-80},"desc":"","desc_en":""},
             {"lbl":"WFP assistance","lbl_en":"Request WFP assistance","fx":{"health":8,"sovereignty":-3,"rel_un":5},"desc":"","desc_en":""},
             {"lbl":"Huwag pansinin","lbl_en":"Do nothing","fx":{"health":-10,"public_trust":-8,"inequality":5},"desc":"","desc_en":""}]},
 # ECONOMY
 {"id":"eco1","cat":"ECONOMY",
  "title":"MATAAS NA IMPLASYON","title_en":"HIGH INFLATION CRISIS",
  "flavor":"Implasyon ay pumalo sa 9.2% — pinakamataas sa 14 taon. Presyo ng bigas ay tumaas ng 40%.",
  "flavor_en":"Inflation hits 9.2% — a 14-year high. Rice prices have surged 40% in three months.",
  "choices":[{"lbl":"IMF loan","lbl_en":"Take IMF loan","fx":{"budget":500,"sovereignty":-9,"economy":5,"debt":300},"desc":"","desc_en":""},
             {"lbl":"Austerity measures","lbl_en":"Impose austerity","fx":{"economy":4,"public_trust":-10,"inequality":4},"desc":"","desc_en":""},
             {"lbl":"Price controls","lbl_en":"Impose price controls","fx":{"public_trust":5,"economy":-5},"desc":"","desc_en":""},
             {"lbl":"Mag-print ng pera","lbl_en":"Print money","fx":{"economy":3,"public_trust":3,"budget":150},"desc":"","desc_en":""}]},
 {"id":"eco2","cat":"ECONOMY",
  "title":"SEMICONDUCTOR INVESTMENT","title_en":"SEMICONDUCTOR INVESTMENT",
  "flavor":"Isang dayuhang tech firm ay nag-aalok ng ₱200B investment sa semiconductor fab — may kondisyon: tax holiday.",
  "flavor_en":"A foreign tech firm offers ₱200B investment in a semiconductor fab — condition: a full tax holiday.",
  "choices":[{"lbl":"Tanggapin lahat","lbl_en":"Accept all terms","fx":{"economy":14,"sovereignty":-6,"budget":200},"desc":"","desc_en":""},
             {"lbl":"Makipagnegosasyon","lbl_en":"Negotiate better terms","fx":{"economy":9,"sovereignty":2,"budget":100},"desc":"","desc_en":""},
             {"lbl":"Tanggihan","lbl_en":"Decline offer","fx":{"sovereignty":6,"economy":-3},"desc":"","desc_en":""}]},
 {"id":"eco3","cat":"ECONOMY",
  "title":"OFW KRISIS","title_en":"OVERSEAS WORKER CRISIS",
  "flavor":"Rekord na $40B remittances — ngunit 3 OFW ang na-abuse sa Middle East at hindi tinutulungan ng embahada.",
  "flavor_en":"Record $40B in remittances — but 3 OFWs were abused in the Middle East with no embassy assistance.",
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
  "flavor":"Tsina ay nag-aalok ng ₱500B loan para sa rail line — may kondisyon na daungan sa isang isla.",
  "flavor_en":"China offers a ₱500B loan for a rail line — with a condition: port access on a contested island.",
  "choices":[{"lbl":"Tanggapin","lbl_en":"Accept the loan","fx":{"infrastructure":16,"budget":400,"sovereignty":-14,"rel_china":12,"debt":500},"desc":"","desc_en":""},
             {"lbl":"Counter-offer","lbl_en":"Counter-offer (less strings)","fx":{"infrastructure":9,"budget":150,"sovereignty":-5,"rel_china":5,"debt":200},"desc":"","desc_en":""},
             {"lbl":"Tumanggi","lbl_en":"Decline the loan","fx":{"sovereignty":9,"rel_china":-10},"desc":"","desc_en":""}]},
 {"id":"for3","cat":"FOREIGN",
  "title":"ASEAN SUMMIT HOST","title_en":"ASEAN SUMMIT HOST",
  "flavor":"Ang Pilipinas ay mag-ho-host ng ASEAN summit — malaking pagkakataon sa diplomasya.",
  "flavor_en":"The Philippines is hosting the ASEAN summit — a major diplomatic opportunity.",
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
  "flavor":"Bagong respiratory disease ang lumabas — 1,200 cases sa isang linggo. WHO ay nag-monitor na.",
  "flavor_en":"A new respiratory disease has emerged — 1,200 cases in one week. WHO is now monitoring.",
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
  "flavor":"Mga kongresista ay nagmumungkahi ng ChaChange — maaaring magbago ng sistema ng pamahalaan.",
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
  "flavor":"Ilang rehiyon ay nagtatayo ng sarili nilang hudisyal na sistema — labas sa Federal framework.",
  "flavor_en":"Several regions are setting up their own judicial systems — outside the Federal framework.",
  "sys":["Federal Republic"],
  "choices":[{"lbl":"Payagan (federalism works)","lbl_en":"Allow regional autonomy","fx":{"sovereignty":5,"public_trust":5,"infrastructure":3},"desc":"","desc_en":""},
             {"lbl":"I-recentralize","lbl_en":"Recentralise authority","fx":{"public_trust":-5,"economy":3},"desc":"","desc_en":""}]},
 # AUTHORITARIAN
 {"id":"auth1","cat":"SECURITY",
  "title":"DIGMAAN SA DROGA","title_en":"DRUG WAR CAMPAIGN",
  "flavor":"Ang pulis ay nagmumungkahi ng malakas na kampanya laban sa illegal drugs — controversial internationally.",
  "flavor_en":"The police propose a harsh anti-drug campaign — controversial at home and internationally.",
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
  "flavor":"Isang oportunidad — ang malaking halaga ng pondo ng gobyerno ay maaaring ilipat sa mga pribadong account.",
  "flavor_en":"An opportunity — large government funds could be quietly moved to private accounts.",
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
  "flavor":"Metro Manila ay nakakaranas ng malubhang water shortage — ilang linggo na wala sa ilang baranggay.",
  "flavor_en":"Metro Manila faces a severe water shortage — some barangays have had no supply for weeks.",
  "choices":[{"lbl":"Emergency water supply","lbl_en":"Emergency water supply","fx":{"health":6,"public_trust":7,"budget":-120},"desc":"","desc_en":""},
             {"lbl":"Private sector contract","lbl_en":"Private sector contract","fx":{"health":4,"sovereignty":-3,"economy":4},"desc":"","desc_en":""},
             {"lbl":"Rationalize distribution","lbl_en":"Ration distribution","fx":{"health":2,"public_trust":-4},"desc":"","desc_en":""}]},
 {"id":"soc3","cat":"SOCIAL",
  "title":"TRABAHO PARA SA LAHAT","title_en":"UNEMPLOYMENT CRISIS",
  "flavor":"Unemployment ay pumalo sa 12%. Mga kabataan ay nagrereklamo na walang oportunidad.",
  "flavor_en":"Unemployment hits 12%. Young Filipinos say there are no opportunities.",
  "choices":[{"lbl":"Jobs program ₱180B","lbl_en":"₱180B jobs programme","fx":{"inequality":-8,"economy":7,"budget":-180},"desc":"","desc_en":""},
             {"lbl":"Invite foreign investment","lbl_en":"Invite foreign investment","fx":{"economy":10,"sovereignty":-4},"desc":"","desc_en":""},
             {"lbl":"Vocational training","lbl_en":"Vocational training push","fx":{"education":6,"economy":4,"budget":-80},"desc":"","desc_en":""}]},
 {"id":"soc4","cat":"SOCIAL",
  "title":"MENTAL HEALTH KRISIS","title_en":"MENTAL HEALTH CRISIS",
  "flavor":"Pagtaas ng suicide rates sa kabataan. DOH ay humihiling ng emergency mental health funding.",
  "flavor_en":"Suicide rates among youth are rising sharply. The DOH requests emergency mental health funding.",
  "choices":[{"lbl":"National mental health fund","lbl_en":"National mental health fund","fx":{"health":8,"public_trust":6,"budget":-100},"desc":"","desc_en":""},
             {"lbl":"School-based program","lbl_en":"School-based programme","fx":{"health":5,"education":4,"budget":-60},"desc":"","desc_en":""},
             {"lbl":"Pabayaan ang DOH","lbl_en":"Ignore the request","fx":{"health":-5,"public_trust":-4},"desc":"","desc_en":""}]},
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
        diff={"ESTUDYANTE":0.7,"SENADOR":1.0,"PANGULO":1.4}.get(gs.difficulty,1.0)
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
# Each research item: id, name, category, cost (one-time ₱B),
# rp_cost (research points needed), fx (permanent stat bonuses once unlocked),
# prereq (list of ids that must be unlocked first), desc
RESEARCH=[
 # ── MEDICINE & PUBLIC HEALTH ──────────────────────────────
 {"id":"r_vaccines","cat":"MEDICINE","icon":"💉",
  "name":"National Vaccine Programme","cost":60,"rp_cost":3,"prereq":[],
  "fx":{"health":8,"inequality":-2},
  "desc":"Free vaccines for children & adults; reduces disease burden"},
 {"id":"r_dengue_cure","cat":"MEDICINE","icon":"🦟",
  "name":"Dengue Vaccine Rollout","cost":40,"rp_cost":4,"prereq":["r_vaccines"],
  "fx":{"health":6,"public_trust":4},
  "desc":"Indigenously produced dengue vaccine deployed nationwide"},
 {"id":"r_cancer","cat":"MEDICINE","icon":"🧬",
  "name":"Cancer Treatment Centres","cost":90,"rp_cost":6,"prereq":["r_vaccines"],
  "fx":{"health":10,"inequality":-4},
  "desc":"Regional oncology hubs with affordable cancer care"},
 {"id":"r_telemedicine","cat":"MEDICINE","icon":"📱",
  "name":"Telemedicine Network","cost":35,"rp_cost":3,"prereq":[],
  "fx":{"health":5,"education":2,"inequality":-3},
  "desc":"Remote healthcare consultations for rural & island areas"},
 {"id":"r_genomics","cat":"MEDICINE","icon":"🧫",
  "name":"Philippine Genomics Institute","cost":120,"rp_cost":8,"prereq":["r_cancer"],
  "fx":{"health":8,"economy":4,"education":5},
  "desc":"Precision medicine & disease surveillance using genomic data"},
 # ── SCIENCE & TECHNOLOGY ──────────────────────────────────
 {"id":"r_internet","cat":"TECH","icon":"🌐",
  "name":"Open-Source Government Tech","cost":25,"rp_cost":2,"prereq":[],
  "fx":{"corruption":-5,"economy":4,"education":3},
  "desc":"Digital government services & open data platforms"},
 {"id":"r_ai","cat":"TECH","icon":"🤖",
  "name":"AI for Governance","cost":80,"rp_cost":6,"prereq":["r_internet"],
  "fx":{"corruption":-8,"economy":9,"education":5},
  "desc":"AI tools for tax collection, fraud detection & service delivery"},
 {"id":"r_satellite","cat":"TECH","icon":"🛰️",
  "name":"Filipino Satellite Programme","cost":150,"rp_cost":9,"prereq":["r_ai"],
  "fx":{"sovereignty":10,"military":5,"economy":6,"education":4},
  "desc":"Indigenous satellite for weather, comms & maritime surveillance"},
 {"id":"r_cyber","cat":"TECH","icon":"🔐",
  "name":"Cybersecurity National Centre","cost":55,"rp_cost":5,"prereq":["r_internet"],
  "fx":{"military":6,"sovereignty":5,"press_freedom":3},
  "desc":"Defend critical infrastructure from cyber attacks"},
 {"id":"r_quantum","cat":"TECH","icon":"⚛️",
  "name":"Quantum Computing Research Hub","cost":200,"rp_cost":12,"prereq":["r_ai","r_satellite"],
  "fx":{"economy":12,"education":8,"military":4},
  "desc":"Long-term: quantum encryption, computing & materials science"},
 # ── ENERGY ────────────────────────────────────────────────
 {"id":"r_battery","cat":"ENERGY","icon":"🔋",
  "name":"Domestic Battery Technology","cost":70,"rp_cost":5,"prereq":[],
  "fx":{"economy":7,"infrastructure":5,"health":2},
  "desc":"Philippine-made battery cells for EVs and grid storage"},
 {"id":"r_geothermal","cat":"ENERGY","icon":"🌋",
  "name":"Advanced Geothermal Research","cost":65,"rp_cost":4,"prereq":[],
  "fx":{"infrastructure":8,"economy":6,"health":3},
  "desc":"Philippines is world #2 in geothermal — deepen this advantage"},
 {"id":"r_hydrogen","cat":"ENERGY","icon":"💧",
  "name":"Green Hydrogen Programme","cost":110,"rp_cost":8,"prereq":["r_battery","r_geothermal"],
  "fx":{"economy":10,"infrastructure":7,"sovereignty":4},
  "desc":"Produce & export clean hydrogen from renewable sources"},
 # ── AGRICULTURE & FOOD ────────────────────────────────────
 {"id":"r_rice","cat":"AGRI","icon":"🌾",
  "name":"High-Yield Rice Research (IRRI)","cost":30,"rp_cost":3,"prereq":[],
  "fx":{"health":4,"inequality":-5,"economy":4},
  "desc":"Partner with IRRI for climate-resilient high-yield varieties"},
 {"id":"r_aqua","cat":"AGRI","icon":"🐟",
  "name":"Aquaculture Technology","cost":45,"rp_cost":4,"prereq":["r_rice"],
  "fx":{"economy":7,"health":5,"inequality":-4},
  "desc":"Modern fish & seaweed farming — boost blue economy"},
 {"id":"r_drought","cat":"AGRI","icon":"☀️",
  "name":"Drought-Resistant Crops","cost":50,"rp_cost":4,"prereq":["r_rice"],
  "fx":{"health":5,"inequality":-5,"economy":4},
  "desc":"Biotech crops that survive El Niño droughts & typhoon flooding"},
 # ── DEFENCE ───────────────────────────────────────────────
 {"id":"r_drone","cat":"DEFENCE","icon":"🚁",
  "name":"Unmanned Aerial Vehicle Programme","cost":85,"rp_cost":6,"prereq":[],
  "fx":{"military":10,"sovereignty":7},
  "desc":"Domestically built drones for coast guard & AFP surveillance"},
 {"id":"r_sonar","cat":"DEFENCE","icon":"📡",
  "name":"Underwater Sonar Network","cost":95,"rp_cost":7,"prereq":["r_drone"],
  "fx":{"military":8,"sovereignty":10,"rel_us":4},
  "desc":"Passive sonar buoys monitoring contested maritime zones"},
 # ── EDUCATION ─────────────────────────────────────────────
 {"id":"r_stem","cat":"EDUCATION","icon":"🔬",
  "name":"STEM Excellence Programme","cost":40,"rp_cost":3,"prereq":[],
  "fx":{"education":8,"economy":4,"inequality":-3},
  "desc":"Specialised STEM schools + scholarships in all regions"},
 {"id":"r_voc","cat":"EDUCATION","icon":"🔧",
  "name":"Technical-Vocational Revolution","cost":35,"rp_cost":3,"prereq":[],
  "fx":{"education":6,"economy":7,"inequality":-5},
  "desc":"World-class TESDA programmes aligned with industry demand"},
 {"id":"r_univ_research","cat":"EDUCATION","icon":"🎓",
  "name":"Research University Network","cost":75,"rp_cost":6,"prereq":["r_stem"],
  "fx":{"education":10,"economy":8,"health":3},
  "desc":"Link UP, DLSU, Ateneo & state unis into a national R&D network"},
]

# Research point gain per active research policy per month
RP_PER_MONTH = 1.5

POLICIES=[
 # ── GOVERNANCE ──────────────────────────────────────────────
 {"id":"anti_corr","name":"ANTI-CORRUPTION TASKFORCE","cost":5,
  "fx":{"corruption":-9,"sovereignty":3},"desc":"Independent anti-graft agency"},
 {"id":"merit","name":"MERITOCRACY IN GOVERNMENT","cost":4,
  "fx":{"corruption":-13,"economy":7},"desc":"Competence-based civil service hiring"},
 {"id":"natid","name":"NATIONAL ID SYSTEM","cost":5,
  "fx":{"economy":5,"corruption":-3},"desc":"Digital ID — reduces red tape & ghost payrolls"},
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
  "desc":"Transition to parliament — PM replaces President"},
 {"id":"shift_federal","name":"SHIFT TO FEDERAL REPUBLIC","cost":0,
  "fx":{"infrastructure":6,"inequality":-4,"public_trust":-6,"budget":-200},
  "sys_change":"Federal Republic","sys_exclude":["Federal Republic"],
  "desc":"Federalize — devolve power to regional governments"},
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
  "fx":{"inequality":-7,"health":5,"education":4},"desc":"Bigger 4Ps — health & school conditionalities"},
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
  "stance":["PAKIKIPAG-UGNAYAN","BALANSE"],"desc":"BRI-style loan — rail & ports with sovereignty strings"},
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
  "fx":{"infrastructure":8,"economy":5,"inequality":-4},"desc":"Subsidised RoRo ferry routes — Visayas & Mindanao"},
 {"id":"seaport","name":"MAJOR SEAPORT MODERNISATION","cost":11,
  "fx":{"economy":9,"infrastructure":8,"sovereignty":3},"desc":"Upgrade Cebu, Davao & Manila international ports"},
 {"id":"smart_grid","name":"NATIONAL SMART POWER GRID","cost":12,
  "fx":{"infrastructure":10,"economy":8},"desc":"Modernise electricity grid — reduce brownouts nationwide"},
 {"id":"solar_energy","name":"RENEWABLE ENERGY PROGRAM","cost":10,
  "fx":{"infrastructure":7,"economy":5,"health":3},"desc":"Solar & wind farms across Luzon, Visayas, Mindanao"},
 {"id":"nuclear","name":"NUCLEAR POWER PLANT","cost":28,
  "fx":{"economy":14,"infrastructure":11,"health":-5},
  "high_risk_infra":True,
  "desc":"⚠ HIGH RISK if infrastructure < 45 or corruption > 60 — massive power boost"},
 {"id":"dike_system","name":"NATIONAL DIKE & SEAWALL SYSTEM","cost":10,
  "fx":{"infrastructure":7,"health":4,"sovereignty":4},"desc":"Coastal flood defences for vulnerable provinces"},
 # ── MANUFACTURING ────────────────────────────────────────────
 {"id":"shipyard","name":"NATIONAL SHIPBUILDING INDUSTRY","cost":18,
  "fx":{"economy":11,"military":6,"infrastructure":5},"desc":"State shipyards for commercial & naval vessels"},
 {"id":"semiconductor","name":"SEMICONDUCTOR FABRICATION PLANT","cost":20,
  "fx":{"economy":15,"education":5,"inequality":-4},"desc":"High-tech chip fabs — follow the Asian tiger model"},
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
  "fx":{"education":4,"economy":3},"desc":"Funds R&D — earns Research Points each month to unlock tech tree"},
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
            gs.log(f"⚙ System changed: {old_sys} → {new_sys}")
            return f"system_changed:{new_sys}"
        if pid in gs.active_policies: gs.active_policies.remove(pid); return "off"
        if len(gs.active_policies)>=maxp: return f"max{maxp}"
        gs.active_policies.append(pid); return "on"

    def monthly(self,gs):
        """Apply active-policy effects EVERY month:
        - Cost deducted at annual_cost × ₱10B / 12
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
                        gs.log("☢ NUCLEAR INCIDENT — poor infra/corruption caused a malfunction!")
        # Research: accumulate RP from active research investments
        if "research_lab" in gs.active_policies:
            gs.research_points = getattr(gs,"research_points",0) + RP_PER_MONTH
        gs.clamp()

    def annual(self,gs):
        """Year-end: check research tier milestones."""
        rp = getattr(gs,"research_points",0)
        tier = int(rp // 10)
        if tier > getattr(gs,"research_tier",0):
            gs.research_tier = tier
            gs.economy += 2; gs.health += 2; gs.education += 2
            gs.log(f"🔬 Research milestone {tier} — economy, health & education +2")

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
        if gs.budget<0: gs.log(f"⚠ Deficit: ₱{abs(gs.budget):.0f}B")

# ── MAP DATA  (all coordinates fit within the 0-710 × 40-652 map panel)
# The Philippines spans roughly 4.5°N – 21°N, 116°E – 127°E.
# We map: lon 116→127  ⟶  x 50→660,  lat 21→4.5  ⟶  y 50→600
# helper: lon_to_x = (lon-116)/(127-116)*610+50
#         lat_to_y = (21-lat)/(21-4.5)*550+50
MAP_DATA={
 # ── LUZON ── large northern island, roughly triangular NW↗SE
 "Luzon":{"poly":[
    (255,52),  # Ilocos Norte / Cagayan tip NW
    (310,50),  # Cape Engaño NE
    (340,72),  # Cagayan coast
    (360,110), # Palanan / Aurora
    (370,152), # Polillo area
    (352,188), # Quezon coast
    (330,220), # Bicol peninsula start
    (305,255), # Sorsogon tip south
    (280,240), # Masbate channel
    (250,210), # Bondoc peninsula
    (218,192), # Batangas coast
    (200,168), # Cavite / NCR south
    (195,140), # Metro Manila
    (200,115), # Pampanga / Zambales
    (195,88),  # Lingayen Gulf
    (218,65),  # La Union coast
    (240,55),  # Ilocos Norte south
 ],"col":(28,72,160),"ctr":(272,148)},
 # ── NCR ── tiny rectangle inside Luzon, Manila Bay coast
 "NCR":{"poly":[
    (198,138),(218,134),(224,160),(204,166)
 ],"col":(20,110,200),"ctr":(212,150)},
 # ── PALAWAN ── long diagonal SW island
 "Palawan":{"poly":[
    (112,252), # Coron north
    (126,240),
    (148,262),
    (138,295),
    (120,320),
    (105,348),
    (88,362),  # Puerto Princesa south
    (76,370),  # Balabac tip
    (72,348),
    (84,318),
    (95,295),
    (102,270),
 ],"col":(18,120,125),"ctr":(110,308)},
 # ── VISAYAS ── cluster of central islands: Samar, Leyte, Cebu, Negros, Panay, Bohol
 "Visayas":{"poly":[
    (200,268), # Panay NW
    (232,255), # Panay NE
    (264,260), # Cebu north / Samar west
    (306,255), # Eastern Samar north
    (330,278), # Eastern Samar east
    (318,310), # Leyte east
    (300,332), # Leyte south
    (278,342), # Bohol south
    (250,348), # Negros east
    (224,338), # Negros SW / Siquijor
    (198,318), # Panay south / Antique
    (182,298), # Panay SW tip
 ],"col":(28,140,72),"ctr":(255,300)},
 # ── MINDANAO ── large southern island with irregular coast
 "Mindanao":{"poly":[
    (178,374), # Zamboanga peninsula NW
    (200,360), # Misamis Occ
    (238,356), # Misamis Or / CDO
    (275,360), # Bukidnon / Agusan area
    (315,355), # Surigao north
    (340,372), # Surigao east
    (338,400), # Davao Gulf east
    (320,432), # Davao east
    (295,452), # Davao del Sur
    (268,462), # Sarangani east
    (248,468), # Gen San
    (218,462), # Sultan Kudarat
    (195,448), # Cotabato south
    (168,442), # Zamboanga del Sur south
    (148,420), # Zamboanga peninsula south
    (140,400), # Zamboanga City
    (148,378), # Zamboanga peninsula mid
 ],"col":(140,72,18),"ctr":(240,412)},
}
REGION_STATS={
 "Luzon"    :{"GDP%":"35%","Typhoon Risk":"High","Rebels":"Low","Infra":72,"Poverty%":"18%"},
 "NCR"      :{"GDP%":"38%","Typhoon Risk":"Medium","Rebels":"None","Infra":80,"Poverty%":"13%"},
 "Visayas"  :{"GDP%":"15%","Typhoon Risk":"Very High","Rebels":"Low","Infra":55,"Poverty%":"32%"},
 "Mindanao" :{"GDP%":"18%","Typhoon Risk":"Medium","Rebels":"High","Infra":44,"Poverty%":"38%"},
 "Palawan"  :{"GDP%":"4%","Typhoon Risk":"Low","Rebels":"Low","Infra":39,"Poverty%":"28%"},
}

def pt_in_poly(x,y,poly):
    inside=False; j=len(poly)-1
    for i in range(len(poly)):
        xi,yi=poly[i]; xj,yj=poly[j]
        if((yi>y)!=(yj>y))and(x<(xj-xi)*(y-yi)/(yj-yi)+xi): inside=not inside
        j=i
    return inside

# ── UI COMPONENTS ────────────────────────────────────────────
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
        return ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self.r.collidepoint(ev.pos) and self.on


# ── ACHIEVEMENTS ─────────────────────────────────────────────
ACHIEVEMENTS = [
    {"id":"golden_age",
     "name":"Golden Age",
     "name_en":"Golden Age",
     "desc":"Economy, Education, Health, Infrastructure all above 80",
     "desc_en":"Economy, Education, Health, and Infrastructure all exceed 80",
     "icon":"🏆",
     "check": lambda gs: gs.economy>80 and gs.education>80 and gs.health>80 and gs.infrastructure>80},
    {"id":"coup_taken",
     "name":"Kinuha ng Kudeta",
     "name_en":"Taken by a Coup",
     "desc":"Natalo sa kudeta ng heneral",
     "desc_en":"Removed from power by a military coup",
     "icon":"⚔️",
     "check": lambda gs: gs.flags.get("coup_overthrow",False)},
    {"id":"good_dictator",
     "name":"Ang Mabuting Diktador",
     "name_en":"The Good Dictator",
     "desc":"Natapos ang termino sa Benevolent Authoritarianism na may Corruption < 20 at Economy > 75",
     "desc_en":"Completed a term under Benevolent Authoritarianism with Corruption < 20 and Economy > 75",
     "icon":"👑",
     "check": lambda gs: gs.political_system=="Benevolent Authoritarianism" and gs.corruption<20 and gs.economy>75 and gs.year>=2031},
    {"id":"plunderer",
     "name":"Ang Nagnakaw na Diktador",
     "name_en":"The Dictator Who Plundered",
     "desc":"Ang Corruption ay higit sa 85 habang nasa Authoritarian Dictatorship",
     "desc_en":"Corruption exceeded 85 while ruling as an Authoritarian Dictator",
     "icon":"💰",
     "check": lambda gs: gs.political_system=="Authoritarian Dictatorship" and gs.corruption>85},
    {"id":"dying_for",
     "name":"Isang Pilipinas na Karapat-dapat Ipaglaban",
     "name_en":"A Philippines Worth Dying For",
     "desc":"Lahat ng pangunahing istatistika ay higit sa 75 sa pagtatapos ng termino",
     "desc_en":"All major stats above 75 at end of term — truly a nation worth the sacrifice",
     "icon":"🇵🇭",
     "check": lambda gs: all(getattr(gs,s,0)>75 for s in ["economy","health","education","infrastructure","sovereignty","public_trust"]) and (100-gs.corruption)>75 and (100-gs.inequality)>75},
    {"id":"people_power",
     "name":"Isa pang People Power",
     "name_en":"Another People Power",
     "desc":"Ang approval ay nahulog sa ibaba ng 15% ngunit naiwasan ang impeachment sa pamamagitan ng mass mobilisation",
     "desc_en":"Approval fell below 15% but impeachment was averted through mass popular mobilisation",
     "icon":"✊",
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
        icon_s = F["h2"].render(ach["icon"], True, (255,255,255,alpha))
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
        if self.result and self.close and self.close.clicked(ev): self.active=False; return True
        for btn,ch in self.btns:
            if btn.clicked(ev):
                for stat,d in ch.get("fx",{}).items():
                    if stat=="budget": gs.budget+=d
                    elif stat=="debt": gs.debt+=d
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

# ── SPLASH SCREEN (Ninoy Aquino quote) ───────────────────────
class SplashScreen:
    """Black screen: quote fades in, holds, then fades out → triggers menu."""
    QUOTE   = "\u201cThe Filipino is worth dying for.\u201d"   # curly quotes
    ATTRIB  = "— Benigno \u201cNinoy\u201d Aquino Jr.  (1932\u20131983)"
    # Timeline in frames @ 60 fps
    FADE_IN  = 90    # 1.5 s
    HOLD     = 150   # 2.5 s
    FADE_OUT = 90    # 1.5 s

    def __init__(self):
        self._frame = 0
        self._done  = False

    @property
    def done(self): return self._done

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

        # Quote line — wrap if needed
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
        # Stylised silhouette — same proportional layout as the improved in-game map
        polys=[
            # Luzon
            ([(310,68),(362,66),(388,100),(378,168),(352,200),(316,212),
               (290,200),(265,175),(262,148),(268,110),(290,82)], (20,55,130)),
            # Palawan (diagonal SW)
            ([(196,246),(216,234),(236,258),(228,292),(215,316),
               (200,332),(186,342),(178,322),(188,296),(194,270)], (12,100,105)),
            # Visayas cluster
            ([(308,260),(342,254),(370,268),(380,298),(360,318),
               (338,326),(308,322),(284,312),(278,290),(295,268)], (20,110,60)),
            # Mindanao
            ([(272,356),(310,348),(348,354),(374,374),(372,410),
               (355,434),(325,450),(294,456),(266,450),(244,434),
               (230,410),(236,382),(250,364)], (110,58,18)),
        ]
        for pts,c in polys:
            pygame.draw.polygon(surf,c,pts)
            pygame.draw.polygon(surf,C_GD,pts,1)

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
        lbl = T("translate_btn")   # e.g. "🌐 EN" or "🌐 FIL"
        ts=F["sm"].render(lbl,True,C_GOLD if hov else C_WHT)
        surf.blit(ts,(r.x+28,r.centery-ts.get_height()//2))

    def upd(self,mx,my):
        for b in self.btns.values(): b.upd(mx,my)
        self.ticker.upd(); self.t+=0.018
        if self.alpha>0: self.alpha=max(0,self.alpha-14)

    def draw(self,surf,mx=0,my=0):
        gbg(surf); rng=random.Random(42)
        for _ in range(80):
            sx=rng.randint(0,W); sy=rng.randint(0,500)
            br=int(120+80*math.sin(self.t*2+rng.random()*6))
            pygame.draw.circle(surf,(br,br,br),(sx,sy),1)
        self._draw_ph(surf)
        for dx,dy,c in [(3,2,C_BLK),(0,0,C_GOLD)]:
            s=F["H"].render(TITLE,True,c); surf.blit(s,(W//2-s.get_width()//2+dx,130+dy))
        s=F["h2"].render(T("subtitle"),True,C_WHT)
        surf.blit(s,(W//2-s.get_width()//2,198))
        lw=int(280+math.sin(self.t*2)*60)
        pygame.draw.line(surf,C_GOLD,(W//2-lw//2,232),(W//2+lw//2,232),2)
        for b in self.btns.values(): b.draw(surf)
        draw_sun(surf,80,80,32); draw_sun(surf,1200,80,26)
        v=F["sm"].render(T("disclaimer"),True,C_GRY)
        surf.blit(v,(W//2-v.get_width()//2,660))
        self._draw_translate_btn(surf,mx,my)
        self.ticker.draw(surf)
        if self.alpha>0: fade_surf(surf,self.alpha)

    def handle(self,ev):
        global LANG
        # Translate button — toggle language then rebuild btn labels + ticker
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self._TR.collidepoint(ev.pos):
            LANG = "ENG" if LANG=="FIL" else "FIL"
            self._rebuild_btns()
            self.ticker.refresh_lang()
            return None
        for k,b in self.btns.items():
            if b.clicked(ev): return k
        return None

class SetupA:
    def __init__(self): self.name=""; self.err=""; self.btn=Btn(540,460,200,50,T("step1_confirm"))
    def draw(self,surf,mx,my):
        gbg(surf); self.btn.upd(mx,my); draw_sun(surf,80,80,30)
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
        {"id":"ALYANSA","lbl":"PRO-UNITED STATES","sub":"ALYANSA","desc":"Military alliance & Western investment","bonus":"+15 Military  +10 Economy","pen":"−10 China Rel","cols":[(180,30,30),(245,245,245),(30,80,200)]},
        {"id":"PAKIKIPAG-UGNAYAN","lbl":"PRO-CHINA","sub":"PAKIKIPAG-UGNAYAN","desc":"BRI infrastructure & economic ties","bonus":"+20 Infrastructure  +10 China","pen":"−15 Sovereignty","cols":[(200,30,30),(255,215,0),(200,30,30)]},
        {"id":"BALANSE","lbl":"NEUTRAL","sub":"BALANSE","desc":"ASEAN cooperation & balanced trade","bonus":"+5 to all relations","pen":"No strong bonuses","cols":[(30,120,200),(245,245,245),(30,140,80)]},
    ]
    def __init__(self): self.sel=None
    def _r(self,i): return pygame.Rect(48+i*300,210,278,320)
    def draw(self,surf,mx,my):
        gbg(surf)
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
            surf.blit(F["sm"].render(f"✓ {c['bonus']}",True,C_GRN),(r.x+10,r.y+168))
            surf.blit(F["sm"].render(f"✗ {c['pen']}",True,C_RL),(r.x+10,r.y+188))
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
        gbg(surf)
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
           ("SENADOR","Normal","Balanced challenge — ang standard na karanasan",(200,160,0)),
           ("PANGULO","Hard","Madalas na krisis, mahigpit na budget, matinding bagyo",(180,30,30))]
    def __init__(self): self.sel=None
    def _r(self,i): return pygame.Rect(160+i*345,278,305,224)
    def draw(self,surf,mx,my):
        gbg(surf)
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
    def draw(self,surf,mx,my):
        gbg(surf)
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
            else:
                e=F["h2"].render(T("empty_slot"),True,C_GRY); surf.blit(e,(r.centerx-e.get_width()//2,r.centery-e.get_height()//2))
    def handle(self,ev):
        if self.back.clicked(ev): return("back",)
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            mx,my=ev.pos
            for i in range(3):
                if pygame.Rect(340,218+i*162,600,138).collidepoint(mx,my) and self.slots[i]: return("load",i)
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
        self.achv=AchievementManager()
        self._make_nav()

    def _make_nav(self):
        self.nav={
            "policies":Btn(8,  658,112,30,T("nav_policies"),fk="sm"),
            "budget"  :Btn(124,658,112,30,T("nav_budget"),  fk="sm"),
            "events"  :Btn(240,658,112,30,T("nav_events"),  fk="sm"),
            "typhoon" :Btn(356,658,112,30,T("nav_typhoon"), fk="sm"),
            "achiev"  :Btn(472,658,112,30,T("nav_achiev"),  fk="sm"),
            "research":Btn(588,658,112,30,T("nav_research"),fk="sm"),
            "next"    :Btn(1090,658,178,30,T("nav_next"),   fk="sm"),
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
    def _topbar(self,surf):
        pygame.draw.rect(surf,C_DARK,(0,0,W,40))
        pygame.draw.line(surf,C_GD,(0,40),(W,40),1)
        gs=self.gs
        surf.blit(F["bd"].render(f"📅 {MONTHS[gs.month]} {gs.year}  {T('topbar_term')} {gs.term}",True,C_WHT),(10,10))
        bc=C_RL if gs.budget<0 else C_GOLD
        surf.blit(F["bd"].render(f"₱{gs.budget:.0f}B",True,bc),(260,10))
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
            surf.blit(F["sm"].render("🌀 TYPHOON SEASON",True,C_WHT),(558,8))

    def _map(self,surf,mx,my):
        pygame.draw.rect(surf,(7,24,62),(0,40,710,612))
        t=pygame.time.get_ticks()
        for yy in range(200,450,14):
            off=(t//200)%14
            if(yy+off)%14<8: pygame.draw.circle(surf,(60,100,180),(98,yy),2)
        for ln in ["WEST","PH SEA"]:
            s=F["sm"].render(ln,True,(70,110,190)); surf.blit(s,(10,290+["WEST","PH SEA"].index(ln)*18))
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
            rd=REGION_STATS[self.sel_r]; px,py=510,42; pw,ph=192,130
            pygame.draw.rect(surf,C_PAN,(px,py,pw,ph),border_radius=7)
            pygame.draw.rect(surf,C_GOLD,(px,py,pw,ph),1,border_radius=7)
            surf.blit(F["bd"].render(self.sel_r,True,C_GOLD),(px+6,py+5))
            for j,(k,v) in enumerate(rd.items()):
                surf.blit(F["sm"].render(f"{k}: {v}",True,C_WHT),(px+6,py+28+j*18))

    def _right(self,surf):
        px,py,pw=710,40,566
        pygame.draw.rect(surf,C_PAN,(px,py,pw,612))
        pygame.draw.line(surf,C_GD,(px,py),(px,py+612),1)
        gs=self.gs; cy=py

        # ── ECONOMIC INDICATORS (top, prominent) ─────────────────
        pygame.draw.rect(surf,(8,22,48),(px,cy,pw,118))
        surf.blit(F["h2"].render("GDP & ECONOMIC INDICATORS" if LANG=="ENG" else "GDP AT MGA TAGAPAGPAHIWATIG",True,C_GOLD),(px+8,cy+4))
        gs.update_economic_indicators()
        g_col=C_GRN if gs.gdp_growth>=0 else C_RL
        u_col=C_GRN if gs.unemployment<5 else C_YLW if gs.unemployment<10 else C_RL
        i_col=C_GRN if gs.inflation<3   else C_YLW if gs.inflation<7    else C_RL
        p_col=C_GRN if gs.poverty_rate<10 else C_YLW if gs.poverty_rate<25 else C_RL
        d_col=C_GRN if gs.debt/max(gs.gdp,1)*100<40 else C_YLW if gs.debt/max(gs.gdp,1)*100<70 else C_RL
        ENG=LANG=="ENG"
        gdp_lbl =("GDP" if ENG else "GDP") +f": ₱{gs.gdp/1000:.2f}T"
        grow_lbl =("Growth" if ENG else "Paglago")+f": {'+' if gs.gdp_growth>=0 else ''}{gs.gdp_growth:.1f}%"
        unem_lbl =("Unemploy." if ENG else "Walang-trabaho")+f": {gs.unemployment:.1f}%"
        infl_lbl =("Inflation" if ENG else "Implasyon")+f": {gs.inflation:.1f}%"
        pov_lbl  =("Poverty" if ENG else "Kahirapan")+f": {gs.poverty_rate:.1f}%"
        debt_lbl =("Debt/GDP" if ENG else "Utang/GDP")+f": {gs.debt/max(gs.gdp,1)*100:.1f}%"
        rp_val=getattr(gs,"research_points",0)
        rp_lbl=f"🔬 RP: {rp_val:.0f}  T{getattr(gs,'research_tier',0)}  🔓{len(getattr(gs,'research_unlocked',[]))}"
        rows=[(gdp_lbl,C_GOLD),(grow_lbl,g_col),(unem_lbl,u_col),(infl_lbl,i_col),(pov_lbl,p_col),(debt_lbl,d_col)]
        cw2=pw//3
        for i,(txt,tc) in enumerate(rows):
            sx=px+(i%3)*cw2; sy=cy+26+(i//3)*30
            surf.blit(F["sm"].render(txt,True,tc),(sx+6,sy))
        surf.blit(F["sm"].render(rp_lbl,True,C_BLU),(px+6,cy+88))
        pygame.draw.line(surf,C_GD,(px+4,cy+116),(px+pw-4,cy+116),1)
        cy+=120

        # ── NATIONAL STATS ────────────────────────────────────────
        surf.blit(F["h2"].render(T("nat_stats"),True,C_GOLD),(px+8,cy+2))
        cy+=22
        stats=list(self.STATS)
        if gs.political_system in AUTH_SYSTEMS: stats.append(("Auth Pwr","auth_power"))
        bar_w=300; bar_x=px+84
        for lbl,sn in stats:
            tv=getattr(gs,sn,50)
            self.dv[sn]=lerp(self.dv.get(sn,tv),tv,0.07)
            inv=sn in("corruption","inequality")
            draw_bar(surf,bar_x,cy,bar_w,12,self.dv[sn],lbl,invert=inv)
            cy+=26
        pygame.draw.line(surf,C_GD,(px+4,cy+2),(px+pw-4,cy+2),1); cy+=8

        # ── FOREIGN RELATIONS ─────────────────────────────────────
        surf.blit(F["h2"].render(T("for_rel"),True,C_GOLD),(px+8,cy))
        cy+=22
        for lbl,sn in self.RELS:
            tv=getattr(gs,sn,50); self.dv[sn]=lerp(self.dv.get(sn,tv),tv,0.07)
            draw_bar(surf,bar_x,cy,bar_w,12,self.dv[sn],lbl)
            cy+=24

        # ── APPROVAL SPARKLINE ────────────────────────────────────
        ah=gs.approval_history[-24:]
        if len(ah)>2 and cy+60<py+608:
            pygame.draw.line(surf,C_GD,(px+4,cy+2),(px+pw-4,cy+2),1); cy+=6
            surf.blit(F["sm"].render(T("appr_trend"),True,C_GRY),(px+8,cy))
            cy+=14; sh=min(44,py+608-cy-4)
            pygame.draw.rect(surf,(8,20,44),(px+8,cy,pw-16,sh))
            pts=[(px+8+int(j/(len(ah)-1)*(pw-16)),int(cy+sh-(ah[j]/100)*sh)) for j in range(len(ah))]
            if len(pts)>1: pygame.draw.lines(surf,C_GOLD,False,pts,2)

    def _live_ticker(self):
        """Generate dynamic situational news lines from real economic figures."""
        gs=self.gs
        lines=[]
        if LANG=="ENG":
            lines.append(f"📅 {MONTHS[gs.month]} {gs.year} — Administration governs under {gs.political_system}")
            lines.append(f"💰 GDP: ₱{gs.gdp/1000:.2f}T  |  Growth: {gs.gdp_growth:+.1f}%  |  Inflation: {gs.inflation:.1f}%")
            lines.append(f"👥 Unemployment: {gs.unemployment:.1f}%  |  Poverty rate: {gs.poverty_rate:.1f}%  |  Debt/GDP: {gs.debt/gs.gdp*100:.1f}%")
            if gs.economy>75: lines.append(f"📈 Economy booming — foreign investors eye Manila")
            elif gs.economy<35: lines.append(f"📉 Economy in crisis — unemployment at {gs.unemployment:.1f}%")
            if gs.corruption>70: lines.append(f"🔍 Corruption watchdogs sound alarm — graft index at {gs.corruption:.0f}/100")
            elif gs.corruption<25: lines.append(f"✅ Anti-corruption reforms praised — index down to {gs.corruption:.0f}/100")
            if gs.approval_rating>75: lines.append(f"🌟 Approval at {gs.approval_rating:.0f}% — strong mandate")
            elif gs.approval_rating<30: lines.append(f"⚠ Approval crashes to {gs.approval_rating:.0f}% — calls for resignation")
            if gs.inequality>70: lines.append(f"⚠ Inequality deepens — poverty rate {gs.poverty_rate:.1f}%")
            if gs.rel_china<30: lines.append(f"🇨🇳 China relations strained — diplomatic tensions mount")
            elif gs.rel_china>75: lines.append(f"🇨🇳 Strong China ties — new economic deals expected")
            if gs.rel_us<30: lines.append(f"🇺🇸 US relations weak — alliance questioned in Washington")
            elif gs.rel_us>75: lines.append(f"🇺🇸 US-PH alliance strong — joint exercises announced")
            if gs.health<40: lines.append(f"🏥 Health system strained — hospital occupancy critical")
            elif gs.health>80: lines.append(f"💉 Health outcomes improve — life expectancy rising")
            if gs.infrastructure>75: lines.append(f"🏗 Infrastructure boom — new roads and rails nationwide")
            elif gs.infrastructure<35: lines.append(f"🚧 Infrastructure lagging — roads crumbling in provinces")
            if 6<=gs.month<=11: lines.append(f"🌀 Typhoon season active — NDRRMC on high alert")
            if gs.budget<0: lines.append(f"💸 Deficit at ₱{abs(gs.budget):.0f}B — bond markets nervous")
            if gs.gdp_growth<0: lines.append(f"📉 RECESSION: GDP shrinking at {gs.gdp_growth:.1f}% — stimulus needed")
            if gs.inflation>9: lines.append(f"🔥 Inflation surges to {gs.inflation:.1f}% — BSP emergency meeting called")
            if gs.unemployment>14: lines.append(f"⚠ Unemployment at {gs.unemployment:.1f}% — protest rallies expected")
            if "nuclear" in gs.active_policies: lines.append(f"☢ Nuclear plant construction — safety inspectors deployed")
            rp=getattr(gs,"research_points",0)
            if rp>5: lines.append(f"🔬 Research programme active — {rp:.0f} RP accumulated, {len(gs.research_unlocked)} innovations unlocked")
        else:
            lines.append(f"📅 {MONTHS[gs.month]} {gs.year} — Administrasyon ay namumuno sa ilalim ng {gs.political_system}")
            lines.append(f"💰 GDP: ₱{gs.gdp/1000:.2f}T  |  Paglago: {gs.gdp_growth:+.1f}%  |  Implasyon: {gs.inflation:.1f}%")
            lines.append(f"👥 Walang-trabaho: {gs.unemployment:.1f}%  |  Kahirapan: {gs.poverty_rate:.1f}%  |  Utang/GDP: {gs.debt/gs.gdp*100:.1f}%")
            if gs.economy>75: lines.append(f"📈 Ekonomiya ay umuunlad — mga dayuhang negosyante ay interesado")
            elif gs.economy<35: lines.append(f"📉 Ekonomiya sa krisis — kawalan ng trabaho sa {gs.unemployment:.1f}%")
            if gs.corruption>70: lines.append(f"🔍 Mataas na korapsyon — index sa {gs.corruption:.0f}/100")
            elif gs.corruption<25: lines.append(f"✅ Reporma laban sa korapsyon — index bumaba sa {gs.corruption:.0f}/100")
            if gs.approval_rating>75: lines.append(f"🌟 Suporta sa {gs.approval_rating:.0f}% — malakas ang mandato")
            elif gs.approval_rating<30: lines.append(f"⚠ Suporta bumagsak sa {gs.approval_rating:.0f}% — oposisyon nagtatawag ng pagbibitiw")
            if gs.inequality>70: lines.append(f"⚠ Lumalala ang kahirapan — poverty rate {gs.poverty_rate:.1f}%")
            if gs.rel_china<30: lines.append(f"🇨🇳 Tensyon sa Tsina — diplomatikong alitan")
            if gs.rel_us<30: lines.append(f"🇺🇸 Relasyon sa US mahina — alyansa nanganganib")
            if gs.health<40: lines.append(f"🏥 Sistema ng kalusugan sa krisis — ospital puno na")
            if gs.infrastructure>75: lines.append(f"🏗 Boom sa imprastraktura — bagong kalsada at riles")
            elif gs.infrastructure<35: lines.append(f"🚧 Imprastraktura humihina — mga kalsada sa probinsya sira")
            if 6<=gs.month<=11: lines.append(f"🌀 Typhoon season — NDRRMC ay nakaalerto")
            if gs.budget<0: lines.append(f"💸 Depisito ng gobyerno sa ₱{abs(gs.budget):.0f}B — nag-aalala ang mga mamumuhunan")
            if gs.gdp_growth<0: lines.append(f"📉 RESYESYON: GDP bumababa sa {gs.gdp_growth:.1f}% — kailangan ng stimulus")
            if gs.inflation>9: lines.append(f"🔥 Implasyon tumaas sa {gs.inflation:.1f}% — emergency meeting ng BSP")
            if gs.unemployment>14: lines.append(f"⚠ Kawalan ng trabaho sa {gs.unemployment:.1f}% — inaasahang mga rally")
        if lines:
            for ln in lines:
                if ln not in self.ticker._base: self.ticker._base=[ln]+self.ticker._base[:14]
            self.ticker._rebuild()

    def _navbar(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,650,W,70))
        pygame.draw.line(surf,C_GD,(0,650),(W,650),1)
        for b in self.nav.values(): b.upd(mx,my); b.draw(surf)
        # Keyboard hint — bottom-right corner, well clear of all buttons
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
            cost_lbl=f"₱{p['cost']*10}B/yr" if p["cost"]>0 else T("pol_free")
            cs=F["sm"].render(cost_lbl,True,C_YLW); surf.blit(cs,(900,y+16))
            fx_str=" | ".join(f"{k}:{'+' if v>0 else ''}{v}" for k,v in p["fx"].items()
                              if k not in("debt",) and isinstance(v,(int,float)))
            surf.blit(F["sm"].render(fx_str[:55],True,C_GRN if act else C_GRY),(540,y+16))

    def _draw_budget(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("bud_title"),F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        stats=[(T("bud_budget"),f"₱{gs.budget:.0f}B",C_GOLD if gs.budget>0 else C_RL),
               (T("bud_debt"),  f"₱{gs.debt:.0f}B",C_RL),
               (T("bud_rev"),   f"₱{self.bud.revenue(gs):.0f}B",C_GRN),
               (T("bud_active"),f"{len(gs.active_policies)}",C_GOLD),
               (T("bud_relief"),f"₱{gs.disaster_relief_budget:.0f}B",C_YLW)]
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
            # − button
            mr=pygame.Rect(bx-30,y,26,24)
            hov_m=mr.collidepoint(mx,my)
            pygame.draw.rect(surf,(80,30,30) if hov_m else (50,20,20),mr,border_radius=5)
            surf.blit(F["bd"].render("−",True,C_WHT),(mr.x+6,mr.y+2))
            # + button
            pr=pygame.Rect(bx+bw+4,y,26,24)
            hov_p=pr.collidepoint(mx,my)
            pygame.draw.rect(surf,(30,80,30) if hov_p else (20,50,20),pr,border_radius=5)
            surf.blit(F["bd"].render("+",True,C_WHT),(pr.x+5,pr.y+2))

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
                badge=F["sm"].render("✓ UNLOCKED" if LANG=="ENG" else "✓ NAKAMIT",True,C_GRN)
                surf.blit(badge,(1140-badge.get_width(),y+26))
            else:
                badge=F["sm"].render("LOCKED" if LANG=="ENG" else "NAKA-LOCK",True,(90,90,90))
                surf.blit(badge,(1140-badge.get_width(),y+26))

    def _draw_research(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        title_s="RESEARCH & INNOVATION" if LANG=="ENG" else "PANANALIKSIK AT INOBASYON"
        blit_c(surf,title_s,F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        rp=getattr(gs,"research_points",0)
        unlocked=getattr(gs,"research_unlocked",[])
        rp_lbl="Research Points" if LANG=="ENG" else "Research Points"
        surf.blit(F["bd"].render(f"🔬 {rp_lbl}: {rp:.1f}  |  Tier: {getattr(gs,'research_tier',0)}  |  Unlocked: {len(unlocked)}/{len(RESEARCH)}",True,C_GRN),(10,44))
        # Group by category
        cats={}
        for r in RESEARCH:
            cats.setdefault(r["cat"],[]).append(r)
        CAT_COLS={"MEDICINE":(0,180,180),"TECH":(40,120,220),"ENERGY":(220,160,0),
                  "AGRI":(60,180,60),"DEFENCE":(200,80,0),"EDUCATION":(160,0,200)}
        CAT_LABELS={"MEDICINE":"Medicine & Health","TECH":"Science & Technology",
                    "ENERGY":"Energy","AGRI":"Agriculture","DEFENCE":"Defence",
                    "EDUCATION":"Education"} if LANG=="ENG" else {
                    "MEDICINE":"Medisina at Kalusugan","TECH":"Agham at Teknolohiya",
                    "ENERGY":"Enerhiya","AGRI":"Agrikultura","DEFENCE":"Depensa",
                    "EDUCATION":"Edukasyon"}
        y=76; col_w=610
        for cat,items in cats.items():
            cat_col=CAT_COLS.get(cat,C_GRY)
            cat_lbl=CAT_LABELS.get(cat,cat)
            pygame.draw.rect(surf,lc(C_DARK,cat_col,0.18),(10,y,1260,22),border_radius=5)
            surf.blit(F["h2"].render(f"── {cat_lbl} ──",True,cat_col),(16,y+3)); y+=26
            for r in items:
                if y>635: break
                done=r["id"] in unlocked
                can_unlock=(not done and rp>=r["rp_cost"]
                            and all(pr in unlocked for pr in r.get("prereq",[])))
                row_col=lc(C_PAN,(16,48,16),0.6 if done else(0.2 if can_unlock else 0))
                bdr=C_GRN if done else(C_GOLD if can_unlock else C_GRY)
                pygame.draw.rect(surf,row_col,(10,y,1260,44),border_radius=7)
                pygame.draw.rect(surf,bdr,(10,y,1260,44),1+done,border_radius=7)
                # Icon + name
                surf.blit(F["bd"].render(r["icon"]+" "+r["name"],True,C_GOLD if done else(C_WHT if can_unlock else C_GRY)),(18,y+5))
                # Desc
                surf.blit(F["sm"].render(r["desc"],True,C_GRY),(18,y+25))
                # Cost
                cost_str=f"₱{r['cost']}B  |  RP: {r['rp_cost']}"
                if r.get("prereq"): cost_str+=f"  |  Needs: {', '.join(r['prereq'])}"
                cs=F["sm"].render(cost_str,True,C_YLW if can_unlock else C_GRY)
                surf.blit(cs,(1260-cs.get_width()-8,y+5))
                # Status badge
                if done:
                    bd=F["sm"].render("✓ UNLOCKED" if LANG=="ENG" else "✓ NAKAMIT",True,C_GRN)
                    surf.blit(bd,(1260-bd.get_width()-8,y+26))
                elif can_unlock:
                    bd=F["sm"].render("CLICK TO UNLOCK" if LANG=="ENG" else "I-CLICK PARA BUKSAN",True,C_GOLD)
                    surf.blit(bd,(1260-bd.get_width()-8,y+26))
                    # Store rect for click detection
                    if not hasattr(self,"_res_rects"): self._res_rects={}
                    self._res_rects[r["id"]]=pygame.Rect(10,y,1260,44)
                elif r.get("prereq") and any(pr not in unlocked for pr in r["prereq"]):
                    missing=[pr for pr in r["prereq"] if pr not in unlocked]
                    bd=F["sm"].render(f"Locked: need {missing[0]}",True,(100,100,100))
                    surf.blit(bd,(1260-bd.get_width()-8,y+26))
                y+=48
            y+=4

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
                        gs.log(f"🔬 Research unlocked: {res[nm] if nm in res else res['name']}")
                        self.ticker.add(f"🔬 {'Research unlocked' if LANG=='ENG' else 'Pananaliksik nabuksan'}: {res['name']}")
        self._res_rects={}

    def _draw_events(self,surf,mx,my):
        pygame.draw.rect(surf,C_DARK,(0,0,W,H))
        blit_c(surf,T("ev_title"),F["h1"],C_GOLD,8)
        close=Btn(1140,4,132,34,T("close_btn"),fk="sm"); close.upd(mx,my); close.draw(surf)
        gs=self.gs
        for i,entry in enumerate(gs.event_log):
            y=58+i*28-self.ev_scroll
            if y<50 or y>670: continue
            c=C_RL if "⚠" in entry else C_GRN if ("prosecute" in entry.lower() or "fund" in entry.lower()) else C_WHT
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
            vals=[str(t["year"]),t["name"],f"Cat {t['cat']}",t["region"],f"₱{t['damage']:.0f}B",t["outcome"]]
            for j,(v,x) in enumerate(zip(vals,xs)):
                c=oc if j==5 else C_WHT; surf.blit(F["sm"].render(v,True,c),(x,y))

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
        for t in ty: lines.append(f"  • {t['name']} (Cat {t['cat']}) → {t['region']} — ₱{t['damage']:.0f}B")
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
        self.nav["next"].lbl=T("nav_next")
        self.ok_btn.lbl=T("ok_btn")
        self.pbtn["resume"].lbl=T("pause_resume");  self.pbtn["save"].lbl=T("pause_save")
        self.pbtn["menu"].lbl=T("pause_menu");      self.pbtn["quit"].lbl=T("pause_quit")
        self.rel_btns["low"].lbl=T("relief_low");   self.rel_btns["mid"].lbl=T("relief_mid")
        self.rel_btns["high"].lbl=T("relief_high")
        gbg(surf)
        self._topbar(surf)
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
        if self.sub in("policies","budget","events","typhoon","achiev","research"):
            if ev.type==pygame.MOUSEBUTTONDOWN and pygame.Rect(1140,4,132,34).collidepoint(ev.pos):
                self.sub=None; return None
            if self.sub=="research" and ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                self._handle_research_click(ev,self.gs)
            if ev.type==pygame.MOUSEBUTTONDOWN and pygame.Rect(1140,4,132,34).collidepoint(ev.pos):
                self.sub=None; return None
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
                            self.ticker.add(f"⚙ Political system changed to: {new_sys}")
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
                # transition to queued sub (typhoon_resolve) or back to game
                if hasattr(self,"_queued_sub"):
                    self.sub=self._queued_sub
                    del self._queued_sub
                else:
                    self.sub=None
            return None
        if self.sub=="typhoon_resolve":
            relief_map={"low":100,"mid":250,"high":400}
            for k,b in self.rel_btns.items():
                if b.clicked(ev):
                    res=self.ty_eng.resolve(gs,self.ty_season,relief_map[k])
                    gs.log(f"Typhoon season: {res['n']} {T('ty_log_name').lower()}, ₱{res['total']:.0f}B — {res['outcome']}")
                    self.ticker.add(f"🌀 {T('ty_log_name')} season done — {res['outcome']}")
                    self.ty_season=[]; self.sub=None
            return None
        # main screen card
        if self.card.active:
            self.card.handle(ev,gs)
            return None
        # nav
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
            for k,b in self.nav.items():
                if b.clicked(ev):
                    if k in("policies","budget","events","typhoon","achiev","research"): self.sub=k
                    elif k=="next": self._advance()
            if self.hover_r: self.sel_r=None if self.sel_r==self.hover_r else self.hover_r
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_ESCAPE: self.sub="pause"
            elif ev.key in(pygame.K_SPACE,pygame.K_RETURN) and self.sub is None: self._advance()
        return None

    def _advance(self):
        gs=self.gs
        gs.month+=1
        # Apply active policies this month (cost/12 + stat/12)
        # Policies STAY active until the player manually deselects them
        self.pol.monthly(gs)
        # Update derived economic indicators
        gs.update_economic_indicators()
        if gs.month>12:
            gs.month=1; gs.year+=1
            self._do_year_end()
        else:
            # monthly: maybe fire event
            diff_f={"ESTUDYANTE":0.4,"SENADOR":0.65,"PANGULO":0.9}.get(gs.difficulty,0.65)
            if random.random()<diff_f:
                pool=[e for e in EVENTS if not(e.get("sys") and gs.political_system not in e.get("sys",[]))]
                if pool:
                    chosen_ev=random.choice(pool)
                    def cb(choice,_ev=chosen_ev): self.ticker.add(f"{_ev['title']}: {choice}")
                    self.card.show(chosen_ev,cb)
        gs.compute_approval()
        gs.clamp()
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
        for t in self.ty_season: self.ticker.add(f"🌀 {t['name']} Cat {t['cat']} — {t['region']}")
        # Annual summary
        self.annual_txt=[
            T("ann_year_done").format(y=gs.year-1),
            T("ann_budget").format(b=gs.budget,d=gs.debt),
            T("ann_appr").format(a=gs.approval_rating),
            f"Economy: {gs.economy:.0f}  Trust: {gs.public_trust:.0f}  Health: {gs.health:.0f}",
            f"Education: {gs.education:.0f}  Infra: {gs.infrastructure:.0f}",
            f"Corruption: {gs.corruption:.0f}  Inequality: {gs.inequality:.0f}",
            f"US: {gs.rel_us:.0f}  China: {gs.rel_china:.0f}  ASEAN: {gs.rel_asean:.0f}",
            T("ann_policies").format(n=len(gs.active_policies)),
            T("ann_typhoons").format(n=len(self.ty_season)),
        ]
        if gs.budget<0: self.annual_txt.append(T("ann_deficit").format(v=abs(gs.budget)))
        if gs.corruption>75: self.annual_txt.append(T("ann_corr_warn"))
        if gs.approval_rating<25: self.annual_txt.append(T("ann_appr_warn"))
        # Auto save
        SaveManager.save(self.slot,gs.to_dict())
        # Check term
        years_in_term=gs.year-2025-(gs.term-1)*6
        if years_in_term>=6:
            gs.term+=1
            if gs.term>2: gs.flags["term_limit"]=True
        # Show annual then typhoon resolve
        self.sub="annual"
        # will switch to typhoon_resolve after ok_btn
        self._queued_sub="typhoon_resolve"

    def _check_gameover(self):
        if self.card.active: return   # don't interrupt mid-event
        gs=self.gs
        # People Power: low approval but mass support saves you (one chance)
        if gs.approval_rating<15 and not gs.flags.get("people_power_tried"):
            if gs.public_trust>60 and random.random()<0.45:
                gs.flags["people_power_triggered"]=True
                gs.flags["people_power_tried"]=True
                gs.approval_rating+=20; gs.public_trust-=12; gs.clamp()
                gs.log("✊ People Power! Mass mobilisation averts impeachment — but trust takes a hit.")
                self.ticker.add("✊ PEOPLE POWER RALLY saves administration from collapse!" if LANG=="ENG"
                                else "✊ PEOPLE POWER RALLY — Naligtas ang administrasyon!")
                return
        if gs.approval_rating<15: gs.flags["impeached"]=True
        if gs.budget<-3000: gs.flags["economic_collapse"]=True
        # Coup trigger in extreme military + low trust scenario
        if gs.military>75 and gs.approval_rating<20 and gs.public_trust<25:
            if random.random()<0.3:
                gs.flags["coup_overthrow"]=True; gs.flags["impeached"]=True
                gs.log("⚔ Military coup — the generals have seized the palace!")
        if gs.consecutive_low>=2 and random.random()<0.5: gs.flags["snap_election"]=True

    @property
    def game_over_reason(self):
        gs=self.gs
        if gs.flags.get("impeached"): return T("go_reason_imp")
        if gs.flags.get("economic_collapse"): return T("go_reason_eco")
        return ""

    @property
    def is_game_over(self):
        return bool(self.gs.flags.get("impeached") or self.gs.flags.get("economic_collapse"))

    @property
    def is_victory(self):
        gs=self.gs
        return gs.flags.get("term_limit") or (gs.year-2025)>=12


# ── GAME OVER SCREEN ─────────────────────────────────────────
class GameOverScreen:
    def __init__(self,reason,gs):
        self.reason=reason; self.gs=gs
        self.retry=Btn(490,500,170,52,T("go_retry")); self.menu=Btn(680,500,170,52,T("go_menu"))

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
    # Grade → STRINGS key
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
    pygame.init()
    screen=pygame.display.set_mode((W,H),pygame.RESIZABLE)
    pygame.display.set_caption(TITLE)
    clock=pygame.time.Clock()
    surf=pygame.Surface((W,H))
    init_fonts()

    # State machine
    state="splash"
    splash=SplashScreen()
    setup_a=SetupA(); setup_b=SetupB(); setup_c=SetupC(); setup_d=SetupD()
    menu=MainMenu(); load_scr=LoadScreen()
    gs_tmp=GS()           # accumulate setup choices
    game_scr=None         # GameScreen
    go_scr=None; vic_scr=None
    active_slot=0

    def new_game(gs,slot=0):
        nonlocal game_scr,state,active_slot
        gs.apply_bonuses(); active_slot=slot
        game_scr=GameScreen(gs,slot); state="game"

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
            if ev.type==pygame.QUIT: running=False; break

            # ── splash ──
            if state=="splash":
                splash.handle(ev)
                if splash.done: state="menu"
                continue   # don't pass splash events to other handlers

            # ── state routing ──
            if state=="menu":
                r=menu.handle(ev)
                if r=="new":    setup_a=SetupA(); setup_b=SetupB(); setup_c=SetupC(); setup_d=SetupD(); gs_tmp=GS(); state="setup_a"
                elif r=="load": load_scr=LoadScreen(); state="load"
                elif r=="quit": running=False

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

        # scale to window
        sw,sh=screen.get_size()
        scaled=pygame.transform.scale(surf,(sw,sh))
        screen.blit(scaled,(0,0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__=="__main__":
    main()