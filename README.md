# REPUBLIKA SIMULATOR
<img width="1086" height="231" alt="image" src="https://github.com/user-attachments/assets/9e98246d-fc2a-4525-83cb-ad3faf854fc5" />

A Filipino political strategy game built in Python + Pygame.

---

## REQUIREMENTS

```
Python 3.9+
pygame        (pip install pygame)
numpy         (pip install numpy)   — for click sounds (optional)
```

---

## HOW TO RUN

```bash
pip install pygame numpy
python republika_simulator.py
```

---

## IMAGE ASSETS (optional but recommended)

Place these two files **in the same folder as the script**:

| Filename | What it does |
|---|---|
| `PHILIPPINES.png` | Replaces the drawn map in-game |
| `PHILIPPINES_STAR.png` | Replaces the drawn Philippine sun |

The game runs fully without these files — it will draw vector versions as a fallback.

---

## GAMEPLAY

### Basic loop
1. Each **SPACE / Next Month** press advances one month.
2. Events pop up — read the situation, pick a response.
3. Up to **10 events** can stack; resolve them one at a time.
4. At the **end of each year** you get an annual review and typhoon season.
5. At **year 6** (end of term) you choose what happens next.

### Stats
| Stat | What it measures |
|---|---|
| Economy | GDP growth, jobs, investment climate |
| Military | AFP strength and modernisation |
| Trust | Public approval of government institutions |
| Corruption | Graft and abuse index (lower = better) |
| Inequality | Wealth gap (lower = better) |
| Infrastructure | Roads, rails, power, internet |
| Health | Life expectancy, hospital quality |
| Education | Literacy, university quality |
| Sovereignty | EEZ control, WPS, national dignity |
| Press Freedom | Media independence |

### Difficulty
| Mode | Events | Typhoons | Approval pull |
|---|---|---|---|
| ESTUDYANTE | 65% chance/month | 1.0× damage | Moderate |
| SENADOR | 85% chance/month | 1.4× damage | Hard |
| PANGULO | 100% chance/month | 1.9× damage | Very Hard |

---

## NAVIGATION TABS (bottom bar)
- **POLICIES** — Toggle up to 6 active policies; grouped by category
- **BUDGET** — Adjust annual budget allocation across sectors
- **EVENTS** — Full event log
- **TYPHOON** — Typhoon history and damage records
- **ACHIEV** — 6 unlockable achievements
- **RESEARCH** — Branch-tree innovation tree; spend RP to unlock
- **DIPLO** — Spend budget to directly improve US / China / ASEAN / UN relations
- **SHOWS** — Political shows: parades, interviews, debates, world stage (resets monthly)

---

## POLITICAL SYSTEMS
| System | Effect |
|---|---|
| Presidential Republic | Default; balanced checks and balances |
| Parliamentary System | PM replaces President; +Trust +Economy |
| Federal Republic | Strong regions; +Infra −Inequality |
| Benevolent Authoritarianism | Strong corruption control; −25 Corruption, +12 Economy |
| Authoritarian Dictatorship | Unchecked power; cult of personality; rigged elections |

---

## END OF TERM
After each 6-year term you choose:
1. **[VOTE]** Fair election — +Trust, +Press Freedom
2. **[RIG]** Rig the election → become Authoritarian Dictator
3. **[AUTH]** Declare emergency rule → Benevolent Authoritarian
4. **[RET]** Retire — game ends, legacy graded
5. **[EXT]** Charter Change extension — +Auth Power, −Trust

---

## ACHIEVEMENTS
| Achievement | How to unlock |
|---|---|
| Golden Age | Economy, Health, Education, Infra all > 80 simultaneously |
| Taken by a Coup | Removed from power by the military |
| The Good Dictator | Rigged an election but kept Corruption < 20 and Economy > 75 |
| The Dictator Who Plundered | Corruption > 85 under Authoritarian Dictatorship |
| A Philippines Worth Dying For | All major stats > 75 and Corruption < 25 |
| Another People Power | Approval fell below 15% but mass mobilisation saved you |

---

## RESEARCH TREE
Research Points (RP) accumulate monthly based on your Education stat:

`RP/month = 0.8 × (0.5 + Education/100) × bonuses`

Bonuses from: `free_uni` policy (×1.4), `r_stem` unlock (×1.2)

Categories: Medicine, Tech, Energy, Agriculture, Defence, Education, **Aerospace & Space**

Aerospace chain: Aerospace Institute → Sounding Rockets → Microsat Constellation → ASEAN Space Hub

---

## ISLAND STATS (click map region)
Dynamic values updated every month:
- **Infrastructure** — rises with Infra stat; NCR benefits most
- **Poverty rate** — falls with Economy/Inequality improvements  
- **Rebel activity** — Mindanao peace tied to Military + Trust

---

## SETTINGS
Accessible from main menu → **[ SETTINGS ]**
- Toggle intro quote (Ramon Magsaysay) on/off
- Toggle language (Filipino / English)

Settings are saved to `republika_settings.json` next to the script.

---

## DICTATOR PATH
If you seize or rig your way to power:
- **Personality cult** activates at Auth Power ≥ 30 (red posters on buildings)
- **Authoritarian events** fire: military revolt, economic collapse, People Power 2
- **Old age** — after 20+ years in power, escalating chance of dying in office
- **Coup** — military may remove you if you ignore the warning signs

---

## CREDITS
- Ramon Magsaysay intro quote: *"He who has less in life should have more in law"*  
  — Champion of the Masses (1907–1957)
- All characters, politicians and events are **entirely fictional**
- Philippine geography, place names and historical references are real
- ALL SOUNDS AND SONGS ARE NOT AFFILIATED WITH A SPECIFIC MOVEMENT OR AGENDA
# V1 coming soon
#V0.2
<img width="1269" height="1190" alt="image" src="https://github.com/user-attachments/assets/4b1350d0-a3d9-4646-8135-1078e0c3d17f" />
# V0.1
<img width="1338" height="1113" alt="Screenshot 2026-03-28 201907" src="https://github.com/user-attachments/assets/b534ac32-80e4-4919-a1a8-1846b6376e9c" />
