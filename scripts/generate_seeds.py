#!/usr/bin/env python3
"""Generate all seed CSV files for the MAIN demo dbt project."""

import csv
import random
import os
from datetime import date, datetime, timedelta

random.seed(42)

SEEDS_DIR = "/tmp/media_company_demo/seeds"
os.makedirs(SEEDS_DIR, exist_ok=True)


def write_csv(filename, fieldnames, rows):
    path = os.path.join(SEEDS_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filename}: {len(rows)} rows")


# ─── LOADED_AT timestamp ─────────────────────────────────────────────────────
LOADED_AT = "2025-12-31T23:59:00"


# ════════════════════════════════════════════════════════════════════════════════
# 1. CHANNELS (12 broadcast + 1 streaming sentinel = 13 rows)
# ════════════════════════════════════════════════════════════════════════════════
channels_data = [
    # MAIN portfolio
    {"channel_id": "MAIN",       "channel_name": "MediaCo",       "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": True},
    {"channel_id": "EXTRA",       "channel_name": "EXTRA",               "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": False},
    {"channel_id": "FACTUAL",    "channel_name": "MediaCo Factual",            "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": False},
    {"channel_id": "MOVIES",    "channel_name": "MediaCo Movies",            "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": False},
    {"channel_id": "CATCHUP",   "channel_name": "MediaCo Catchup",           "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": False},
    # AVOD sentinel
    {"channel_id": "streaming",     "channel_name": "MediaCo Streaming (AVOD)",     "broadcaster": "MediaCo", "is_media_company_portfolio": True, "is_psb": True},
    # Competitors
    {"channel_id": "BBC1",     "channel_name": "BBC One",          "broadcaster": "BBC",       "is_media_company_portfolio": False, "is_psb": True},
    {"channel_id": "BBC2",     "channel_name": "BBC Two",          "broadcaster": "BBC",       "is_media_company_portfolio": False, "is_psb": True},
    {"channel_id": "ITV1",     "channel_name": "ITV1",             "broadcaster": "ITV",       "is_media_company_portfolio": False, "is_psb": True},
    {"channel_id": "ITV2",     "channel_name": "ITV2",             "broadcaster": "ITV",       "is_media_company_portfolio": False, "is_psb": False},
    {"channel_id": "CHAN5",    "channel_name": "Channel 5",        "broadcaster": "Channel 5", "is_media_company_portfolio": False, "is_psb": True},
    {"channel_id": "SKYONE",   "channel_name": "Sky One",          "broadcaster": "Sky",       "is_media_company_portfolio": False, "is_psb": False},
    {"channel_id": "SKYATL",   "channel_name": "Sky Atlantic",     "broadcaster": "Sky",       "is_media_company_portfolio": False, "is_psb": False},
]
write_csv("channels.csv",
          ["channel_id", "channel_name", "broadcaster", "is_media_company_portfolio", "is_psb"],
          channels_data)

channel_ids = [c["channel_id"] for c in channels_data]
media_company_channel_ids = [c["channel_id"] for c in channels_data if c["is_media_company_portfolio"] and c["channel_id"] != "streaming"]


# ════════════════════════════════════════════════════════════════════════════════
# 2. DEMOGRAPHICS (exactly 16: 4 age × 2 gender × 2 grade)
# ════════════════════════════════════════════════════════════════════════════════
age_bands = ["4-15", "16-34", "35-54", "55+"]
genders = ["M", "F"]
social_grades = ["ABC1", "C2DE"]

demographics_data = []
demo_id = 1
for age in age_bands:
    for gender in genders:
        for grade in social_grades:
            demographics_data.append({
                "demographic_id": f"D{demo_id:03d}",
                "age_band": age,
                "gender": gender,
                "social_grade": grade,
            })
            demo_id += 1
write_csv("demographics.csv",
          ["demographic_id", "age_band", "gender", "social_grade"],
          demographics_data)

demo_ids = [d["demographic_id"] for d in demographics_data]


# ════════════════════════════════════════════════════════════════════════════════
# 3. DAYPARTS (6 rows)
# ════════════════════════════════════════════════════════════════════════════════
dayparts_data = [
    {"daypart_id": "DP01", "daypart_name": "breakfast",  "start_hour": 6,  "end_hour": 9},
    {"daypart_id": "DP02", "daypart_name": "daytime",    "start_hour": 9,  "end_hour": 17},
    {"daypart_id": "DP03", "daypart_name": "pre-peak",   "start_hour": 17, "end_hour": 19},
    {"daypart_id": "DP04", "daypart_name": "peak",       "start_hour": 19, "end_hour": 22},
    {"daypart_id": "DP05", "daypart_name": "post-peak",  "start_hour": 22, "end_hour": 24},
    {"daypart_id": "DP06", "daypart_name": "night",      "start_hour": 0,  "end_hour": 6},
]
write_csv("dayparts.csv",
          ["daypart_id", "daypart_name", "start_hour", "end_hour"],
          dayparts_data)

daypart_names = [d["daypart_name"] for d in dayparts_data]


# ════════════════════════════════════════════════════════════════════════════════
# 4. ADVERTISERS (25 rows)
# ════════════════════════════════════════════════════════════════════════════════
advertisers_raw = [
    ("ADV001", "Tesco",            "retail",  "Publicis"),
    ("ADV002", "Barclays",         "finance", "WPP"),
    ("ADV003", "Vodafone",         "telecom", "Ogilvy"),
    ("ADV004", "Ford Motor",       "auto",    "JWT"),
    ("ADV005", "Unilever",         "fmcg",    "Dentsu"),
    ("ADV006", "Asda",             "retail",  "Havas"),
    ("ADV007", "HSBC",             "finance", "WPP"),
    ("ADV008", "BT Group",         "telecom", "Publicis"),
    ("ADV009", "Volkswagen UK",    "auto",    "DDB"),
    ("ADV010", "Procter & Gamble", "fmcg",    "BBDO"),
    ("ADV011", "Sainsbury's",      "retail",  "Leo Burnett"),
    ("ADV012", "Lloyds Bank",      "finance", "Adam&Eve DDB"),
    ("ADV013", "Sky",              "telecom", "Abbott Mead"),
    ("ADV014", "Toyota GB",        "auto",    "Saatchi & Saatchi"),
    ("ADV015", "Reckitt",          "fmcg",    "Havas"),
    ("ADV016", "Marks & Spencer",  "retail",  "Saatchi & Saatchi"),
    ("ADV017", "NatWest",          "finance", "Proximity"),
    ("ADV018", "O2",               "telecom", "VCCP"),
    ("ADV019", "BMW UK",           "auto",    "WCRS"),
    ("ADV020", "Nestle UK",        "fmcg",    "McCann"),
    ("ADV021", "Lidl UK",          "retail",  "TBWA"),
    ("ADV022", "Halifax",          "finance", "Adam&Eve DDB"),
    ("ADV023", "EE",               "telecom", "Saatchi & Saatchi"),
    ("ADV024", "Renault UK",       "auto",    "Publicis"),
    ("ADV025", "Ryanair",          "travel",  "Dare"),
]
advertisers_data = [
    {"advertiser_id": r[0], "advertiser_name": r[1], "sector": r[2], "agency": r[3]}
    for r in advertisers_raw
]
write_csv("advertisers.csv",
          ["advertiser_id", "advertiser_name", "sector", "agency"],
          advertisers_data)

advertiser_ids = [a["advertiser_id"] for a in advertisers_data]


# ════════════════════════════════════════════════════════════════════════════════
# 5. PROGRAMMES (65 programmes)
# ════════════════════════════════════════════════════════════════════════════════
programmes_raw = [
    # (programme_id, title, genre, sub_genre, is_original_uk, is_news_current_affairs, duration_min)
    # MAIN flagship
    ("P001", "The Great British Bake Off",      "entertainment", "reality",         True,  False, 60),
    ("P002", "Gogglebox",                        "entertainment", "reality",         True,  False, 60),
    ("P003", "Hollyoaks",                        "drama",         "soap",            True,  False, 30),
    ("P004", "MediaCo News",                   "news",          "news_bulletin",   True,  True,  55),
    ("P005", "Countdown",                        "entertainment", "gameshow",        True,  False, 45),
    ("P006", "The IT Crowd",                     "comedy",        "sitcom",          True,  False, 30),
    ("P007", "Peep Show",                        "comedy",        "sitcom",          True,  False, 30),
    ("P008", "Dispatches",                       "factual",       "documentary",     True,  True,  60),
    ("P009", "Grand Designs",                    "factual",       "lifestyle",       True,  False, 60),
    ("P010", "Unreported World",                 "news",          "current_affairs", True,  True,  25),
    ("P011", "8 Out of 10 Cats",                 "comedy",        "panel_show",      True,  False, 60),
    ("P012", "First Dates",                      "entertainment", "reality",         True,  False, 60),
    ("P013", "Taskmaster",                       "comedy",        "gameshow",        True,  False, 60),
    ("P014", "The Circle",                       "entertainment", "reality",         True,  False, 60),
    ("P015", "SAS: Who Dares Wins",              "entertainment", "reality",         True,  False, 60),
    ("P016", "24 Hours in A&E",                  "factual",       "documentary",     True,  False, 60),
    ("P017", "Made in Chelsea",                  "entertainment", "reality",         True,  False, 60),
    ("P018", "The Undateables",                  "factual",       "documentary",     True,  False, 60),
    ("P019", "Naked Attraction",                 "entertainment", "dating",          True,  False, 60),
    ("P020", "Black Mirror",                     "drama",         "sci_fi",          True,  False, 60),
    ("P021", "It's A Sin",                       "drama",         "period_drama",    True,  False, 60),
    ("P022", "Humans",                           "drama",         "sci_fi",          True,  False, 60),
    ("P023", "Utopia",                           "drama",         "thriller",        True,  False, 60),
    ("P024", "Fresh Meat",                       "comedy",        "sitcom",          True,  False, 30),
    ("P025", "Derry Girls",                      "comedy",        "sitcom",          True,  False, 30),
    ("P026", "Big Bang Theory",                  "comedy",        "sitcom",          False, False, 25),
    ("P027", "Frasier",                          "comedy",        "sitcom",          False, False, 25),
    ("P028", "Brooklyn Nine-Nine",               "comedy",        "sitcom",          False, False, 25),
    ("P029", "Superstore",                       "comedy",        "sitcom",          False, False, 25),
    ("P030", "The Simpsons",                     "comedy",        "animation",       False, False, 25),
    # MediaCo Factual / MediaCo Movies content
    ("P031", "MediaCo Movies Premiere: Dunkirk",          "film",          "action",          False, False, 116),
    ("P032", "MediaCo Movies Premiere: La La Land",       "film",          "musical",         False, False, 128),
    ("P033", "MediaCo Movies Premiere: Midsommar",        "film",          "horror",          False, False, 148),
    ("P034", "MediaCo Movies Premiere: Parasite",         "film",          "thriller",        False, False, 132),
    ("P035", "MediaCo Movies Premiere: Dune",             "film",          "sci_fi",          False, False, 155),
    ("P036", "24 Hours in Police Custody",       "factual",       "documentary",     True,  False, 60),
    ("P037", "Ramsay's Kitchen Nightmares",      "factual",       "lifestyle",       True,  False, 60),
    ("P038", "Come Dine with Me",                "entertainment", "reality",         True,  False, 60),
    ("P039", "Embarrassing Bodies",              "factual",       "health",          True,  False, 60),
    ("P040", "Time Team",                        "factual",       "history",         True,  False, 60),
    # EXTRA content
    ("P041", "Hollyoaks Omnibus",                "drama",         "soap",            True,  False, 120),
    ("P042", "Friends",                          "comedy",        "sitcom",          False, False, 25),
    ("P043", "How I Met Your Mother",            "comedy",        "sitcom",          False, False, 25),
    ("P044", "The Inbetweeners",                 "comedy",        "sitcom",          True,  False, 25),
    ("P045", "Skins",                            "drama",         "teen_drama",      True,  False, 45),
    # Sport
    ("P046", "Formula 1 Highlights",             "sport",         "motorsport",      False, False, 60),
    ("P047", "Paralympics 2025",                 "sport",         "athletics",       False, False, 120),
    ("P048", "Cricket: The Ashes",               "sport",         "cricket",         False, False, 180),
    ("P049", "Rugby League World Cup",           "sport",         "rugby",           False, False, 90),
    ("P050", "World Snooker Championship",       "sport",         "snooker",         False, False, 120),
    # News / current affairs
    ("P051", "MediaCo News at 7",              "news",          "news_bulletin",   True,  True,  30),
    ("P052", "Presenter's MediaCo Debates",     "news",          "current_affairs", True,  True,  60),
    ("P053", "Steph's Packed Lunch",             "news",          "magazine",        True,  False, 90),
    # More
    ("P054", "Arrested Development",             "comedy",        "sitcom",          False, False, 25),
    ("P055", "Location Location Location",       "factual",       "property",        True,  False, 60),
    ("P056", "Secret Eaters",                    "factual",       "health",          True,  False, 60),
    ("P057", "Educating Yorkshire",              "factual",       "documentary",     True,  False, 60),
    ("P058", "Benefits Street",                  "factual",       "documentary",     True,  False, 60),
    ("P059", "Celebrity Big Brother",            "entertainment", "reality",         True,  False, 90),
    ("P060", "Deal or No Deal",                  "entertainment", "gameshow",        True,  False, 45),
    # MediaCo Catchup catch-up shows (same titles, different programme)
    ("P061", "MediaCo Catchup Best Of Bake Off",          "entertainment", "reality",         True,  False, 60),
    ("P062", "MediaCo Catchup Best Of Gogglebox",         "entertainment", "reality",         True,  False, 60),
    # Trailers / Promos (duration_min < 5 — for CA-09 exclusion test)
    ("P063", "MediaCo Promo: Autumn Highlights",      "entertainment", "promo",           True,  False, 2),
    ("P064", "EXTRA Continuity Trailer",            "entertainment", "promo",           True,  False, 1),
    ("P065", "MediaCo Movies Promo Reel",                 "entertainment", "promo",           True,  False, 3),
]
programmes_data = [
    {
        "programme_id": r[0], "title": r[1], "genre": r[2], "sub_genre": r[3],
        "is_original_uk": r[4], "is_news_current_affairs": r[5], "duration_min": r[6],
    }
    for r in programmes_raw
]
write_csv("programmes.csv",
          ["programme_id", "title", "genre", "sub_genre", "is_original_uk",
           "is_news_current_affairs", "duration_min"],
          programmes_data)

programme_ids = [p["programme_id"] for p in programmes_data]
# Only content programmes (no promos) for episode generation
content_programme_ids = [p["programme_id"] for p in programmes_data if p["duration_min"] >= 5]
# Map programme to genre for completion rate logic
prog_genre_map = {p["programme_id"]: p["genre"] for p in programmes_data}


# ════════════════════════════════════════════════════════════════════════════════
# 6. EPISODES (250–350 episodes)
# ════════════════════════════════════════════════════════════════════════════════
episodes_data = []
ep_id = 1
synopses_by_genre = {
    "drama":         ["A gripping instalment as tensions rise.", "An unexpected twist changes everything.", "Characters face their biggest challenge yet."],
    "comedy":        ["Hilarious misunderstandings ensue.", "The gang gets into trouble again.", "An embarrassing situation spirals out of control."],
    "factual":       ["Experts investigate a surprising phenomenon.", "Behind-the-scenes access to a unique world.", "A revealing look at everyday life."],
    "entertainment": ["The competition heats up.", "Surprises and shocks from the judges.", "A fan favourite returns for a special challenge."],
    "news":          ["Tonight's top stories and analysis.", "In-depth coverage of breaking news.", "Special report on a developing story."],
    "sport":         ["Full coverage of today's action.", "Highlights and post-match analysis.", "A dramatic finish in the final round."],
    "film":          ["A critically acclaimed feature presentation.", "Award-winning cinema.", "A modern classic."],
}
start_date_2025 = date(2025, 1, 1)

for prog in programmes_data:
    pid = prog["programme_id"]
    genre = prog["genre"]
    dur = prog["duration_min"]
    # Determine how many episodes to generate per programme
    if dur < 5:  # promo
        ep_count = 1
    elif genre in ("film",):
        ep_count = 1
    elif genre == "news":
        ep_count = random.randint(8, 15)
    elif genre == "sport":
        ep_count = random.randint(3, 8)
    elif genre in ("drama", "comedy"):
        # Series: 1-3 series, 4-8 eps each
        series_count = random.randint(1, 3)
        ep_count = series_count * random.randint(4, 8)
    else:
        ep_count = random.randint(4, 12)

    series_num = 1
    ep_in_series = 0
    eps_per_series = random.randint(4, 8)

    for i in range(ep_count):
        if i > 0 and ep_in_series >= eps_per_series:
            series_num += 1
            ep_in_series = 0
            eps_per_series = random.randint(4, 8)
        ep_in_series += 1
        days_offset = random.randint(0, 364)
        tx_date = start_date_2025 + timedelta(days=days_offset)
        synopsis = random.choice(synopses_by_genre.get(genre, ["An episode of this programme."]))
        episodes_data.append({
            "episode_id": f"E{ep_id:05d}",
            "programme_id": pid,
            "series_number": series_num,
            "episode_number": ep_in_series,
            "first_tx_date": tx_date.isoformat(),
            "synopsis": synopsis,
        })
        ep_id += 1

write_csv("episodes.csv",
          ["episode_id", "programme_id", "series_number", "episode_number", "first_tx_date", "synopsis"],
          episodes_data)

episode_ids = [e["episode_id"] for e in episodes_data]
# Map episode to programme
ep_prog_map = {e["episode_id"]: e["programme_id"] for e in episodes_data}
# Map programme to episode list
prog_ep_map = {}
for e in episodes_data:
    prog_ep_map.setdefault(e["programme_id"], []).append(e["episode_id"])


# ════════════════════════════════════════════════════════════════════════════════
# 7. SCHEDULE (EPG for MAIN portfolio channels for 2025)
# ════════════════════════════════════════════════════════════════════════════════
# Sample ~3 weeks spread across the year for 5 MediaCo channels
schedule_data = []
media_company_portfolio_channels = ["MAIN", "EXTRA", "FACTUAL", "MOVIES", "CATCHUP"]

# MAIN-centric programme lists
media_company_progs = [p["programme_id"] for p in programmes_data
            if p["genre"] not in ("film",) and p["programme_id"] not in ("P063", "P064", "P065", "P041")]
e4_progs = ["P026", "P027", "P028", "P029", "P042", "P043", "P044", "P045", "P006", "P007", "P025", "P030"]
factual_progs = ["P036", "P037", "P038", "P039", "P040", "P055", "P056", "P057", "P058", "P009"]
movie_progs = ["P031", "P032", "P033", "P034", "P035"]
four7_progs = ["P061", "P062", "P001", "P002", "P003", "P013", "P012"]

channel_prog_map = {
    "MAIN": media_company_progs,
    "EXTRA": e4_progs,
    "FACTUAL": factual_progs,
    "MOVIES": movie_progs,
    "CATCHUP": four7_progs,
}

def hour_to_time(h, m=0):
    return f"2025-01-01T{h:02d}:{m:02d}:00"  # placeholder, date will be replaced

# Typical daily schedule slots per channel (hour, duration_min)
daily_slots_main = [
    (6, 25), (6, 30), (7, 55), (8, 25), (9, 45), (10, 45), (12, 60),
    (13, 30), (14, 30), (15, 30), (16, 30), (17, 55), (19, 55), (20, 60),
    (21, 60), (22, 55), (23, 55),
]
daily_slots_extra = [
    (7, 25), (7, 30), (8, 25), (9, 50), (10, 50), (12, 50),
    (13, 25), (14, 25), (15, 25), (16, 25), (17, 50), (18, 25), (19, 25),
    (20, 60), (21, 60), (22, 25),
]
daily_slots_factual = [
    (8, 60), (9, 60), (10, 60), (12, 60), (14, 60), (16, 60),
    (18, 60), (20, 60), (21, 60), (22, 60),
]
daily_slots_movies = [
    (9, 120), (12, 128), (15, 116), (18, 148), (21, 132), (23, 95),
]
daily_slots_catchup = [
    (8, 60), (10, 60), (12, 60), (14, 60), (16, 60), (18, 60),
    (20, 60), (21, 60), (22, 60),
]

channel_slots_map = {
    "MAIN": daily_slots_main, "EXTRA": daily_slots_extra, "FACTUAL": daily_slots_factual,
    "MOVIES": daily_slots_movies, "CATCHUP": daily_slots_catchup,
}

# Sample 3 weeks spread across 2025
schedule_weeks = [
    date(2025, 1, 6),   # week 2
    date(2025, 4, 7),   # week 15
    date(2025, 7, 7),   # week 28
    date(2025, 10, 6),  # week 41
]

sch_id = 1
for week_start in schedule_weeks:
    for day_offset in range(7):
        bcast_date = week_start + timedelta(days=day_offset)
        for ch_id in media_company_portfolio_channels:
            slots = channel_slots_map[ch_id]
            prog_list = channel_prog_map[ch_id]
            for (slot_hour, slot_dur) in slots:
                prog_id = random.choice(prog_list)
                # pick an episode from this programme if available
                ep_list = prog_ep_map.get(prog_id, [])
                ep_id = random.choice(ep_list) if ep_list else ""
                start_dt = datetime(bcast_date.year, bcast_date.month, bcast_date.day, slot_hour, 0, 0)
                end_dt = start_dt + timedelta(minutes=slot_dur)
                schedule_data.append({
                    "broadcast_date": bcast_date.isoformat(),
                    "channel_id": ch_id,
                    "start_time": start_dt.isoformat(),
                    "end_time": end_dt.isoformat(),
                    "programme_id": prog_id,
                    "episode_id": ep_id,
                })

write_csv("schedule.csv",
          ["broadcast_date", "channel_id", "start_time", "end_time", "programme_id", "episode_id"],
          schedule_data)


# ════════════════════════════════════════════════════════════════════════════════
# 8. AD CAMPAIGNS (65 campaigns)
# ════════════════════════════════════════════════════════════════════════════════
ad_campaigns_data = []
campaign_id = 1

quarters = [
    (date(2025, 1, 1), date(2025, 3, 31)),
    (date(2025, 4, 1), date(2025, 6, 30)),
    (date(2025, 7, 1), date(2025, 9, 30)),
    (date(2025, 10, 1), date(2025, 12, 31)),
]

campaign_name_templates = [
    "Spring Sale {year}", "Summer Refresh {year}", "Autumn Drive {year}", "Winter Warmth {year}",
    "New Year Launch", "Brand Awareness Q{q}", "Product Launch {n}", "Seasonal Promo {n}",
    "Always On {q}", "Digital First {n}", "TV Burst {n}", "Mass Market {n}",
]

for adv in advertisers_data:
    adv_id = adv["advertiser_id"]
    # Each advertiser has 2-3 campaigns
    num_campaigns = random.randint(2, 3)
    for _ in range(num_campaigns):
        q_start, q_end = random.choice(quarters)
        # campaign is subset of quarter
        start_offset = random.randint(0, 20)
        camp_start = q_start + timedelta(days=start_offset)
        camp_end = camp_start + timedelta(days=random.randint(14, 60))
        if camp_end > q_end:
            camp_end = q_end
        budget = round(random.uniform(50000, 500000), 2)
        tgt_demo = random.choice(demo_ids)
        tpl = random.choice(campaign_name_templates)
        camp_name = tpl.format(year=2025, q=random.randint(1, 4), n=campaign_id)
        ad_campaigns_data.append({
            "campaign_id": f"CAM{campaign_id:04d}",
            "advertiser_id": adv_id,
            "campaign_name": f"{adv['advertiser_name']} — {camp_name}",
            "start_date": camp_start.isoformat(),
            "end_date": camp_end.isoformat(),
            "total_budget_gbp": budget,
            "target_demographic_id": tgt_demo,
        })
        campaign_id += 1

write_csv("ad_campaigns.csv",
          ["campaign_id", "advertiser_id", "campaign_name", "start_date", "end_date",
           "total_budget_gbp", "target_demographic_id"],
          ad_campaigns_data)

campaign_ids = [c["campaign_id"] for c in ad_campaigns_data]


# ════════════════════════════════════════════════════════════════════════════════
# 9. AD SPOTS LINEAR (4000 rows)
# ════════════════════════════════════════════════════════════════════════════════
linear_channels = ["MAIN", "EXTRA", "FACTUAL", "MOVIES", "CATCHUP"]

def get_daypart(hour):
    if 6 <= hour < 9:    return "breakfast"
    if 9 <= hour < 17:   return "daytime"
    if 17 <= hour < 19:  return "pre-peak"
    if 19 <= hour < 22:  return "peak"
    if 22 <= hour < 24:  return "post-peak"
    return "night"

def get_cpm_for_daypart(dp):
    cpm_ranges = {
        "peak": (22, 35), "pre-peak": (18, 28), "post-peak": (14, 22),
        "breakfast": (8, 15), "daytime": (6, 12), "night": (4, 8),
    }
    lo, hi = cpm_ranges.get(dp, (8, 15))
    return round(random.uniform(lo, hi), 2)

ad_spots_linear_data = []
spot_id = 1

for _ in range(4000):
    camp = random.choice(campaign_ids)
    # random date in 2025
    day_offset = random.randint(0, 364)
    bcast_date = date(2025, 1, 1) + timedelta(days=day_offset)
    hour = random.choices(
        [7, 8, 10, 12, 14, 16, 18, 20, 21, 23],
        weights=[3, 3, 5, 5, 5, 5, 8, 15, 15, 8]
    )[0]
    minute = random.randint(0, 59)
    airing_dt = datetime(bcast_date.year, bcast_date.month, bcast_date.day, hour, minute, 0)
    ch_id = random.choice(linear_channels)
    dp = get_daypart(hour)
    dur_sec = random.choice([10, 20, 30, 30, 30, 40, 60])
    booked_imp = round(random.uniform(50, 800), 2)
    # ~5% under-delivery
    if random.random() < 0.05:
        delivered_imp = round(booked_imp * random.uniform(0.70, 0.94), 2)
    else:
        delivered_imp = round(booked_imp * random.uniform(0.96, 1.04), 2)
    cpm = get_cpm_for_daypart(dp)
    revenue = round(delivered_imp * cpm / 1000, 2)
    ad_spots_linear_data.append({
        "spot_id": f"LSP{spot_id:06d}",
        "campaign_id": camp,
        "broadcast_date": bcast_date.isoformat(),
        "airing_time": airing_dt.isoformat(),
        "channel_id": ch_id,
        "daypart": dp,
        "duration_sec": dur_sec,
        "booked_impressions_thousands": booked_imp,
        "delivered_impressions_thousands": delivered_imp,
        "rate_card_cpm_gbp": cpm,
        "actual_revenue_gbp": revenue,
    })
    spot_id += 1

write_csv("ad_spots_linear.csv",
          ["spot_id", "campaign_id", "broadcast_date", "airing_time", "channel_id",
           "daypart", "duration_sec", "booked_impressions_thousands",
           "delivered_impressions_thousands", "rate_card_cpm_gbp", "actual_revenue_gbp"],
          ad_spots_linear_data)


# ════════════════════════════════════════════════════════════════════════════════
# 10. STREAMING USERS (4000 rows)
# ════════════════════════════════════════════════════════════════════════════════
streaming_users_data = []
for i in range(1, 4001):
    reg_days_ago = random.randint(0, 1095)
    reg_date = date(2025, 12, 31) - timedelta(days=reg_days_ago)
    streaming_users_data.append({
        "user_id": f"U{i:06d}",
        "registration_date": reg_date.isoformat(),
        "demographic_id": random.choice(demo_ids),
        "is_active": True,  # all True — downstream staging filters is_active=true
    })
write_csv("streaming_users.csv",
          ["user_id", "registration_date", "demographic_id", "is_active"],
          streaming_users_data)

user_ids = [u["user_id"] for u in streaming_users_data]


# ════════════════════════════════════════════════════════════════════════════════
# 11. STREAMING SESSIONS (6000 rows)
# ════════════════════════════════════════════════════════════════════════════════
platforms = ["web", "ios", "android", "ctv"]
device_types = ["desktop", "mobile", "tablet", "smart_tv", "streaming_stick"]
platform_device_map = {
    "web": ["desktop", "mobile", "tablet"],
    "ios": ["mobile", "tablet"],
    "android": ["mobile", "tablet"],
    "ctv": ["smart_tv", "streaming_stick"],
}

streaming_sessions_data = []
session_user_map = {}  # session_id -> user_id

for i in range(1, 6001):
    sess_id = f"S{i:07d}"
    user_id = random.choice(user_ids)
    platform = random.choices(platforms, weights=[25, 30, 30, 15])[0]
    device_type = random.choice(platform_device_map[platform])
    day_offset = random.randint(0, 364)
    sess_start_date = date(2025, 1, 1) + timedelta(days=day_offset)
    start_hour = random.choices(
        list(range(6, 24)), weights=[2, 2, 3, 4, 4, 5, 6, 8, 9, 10, 9, 8, 7, 6, 5, 5, 4, 4]
    )[0]
    start_min = random.randint(0, 59)
    duration_min = random.randint(5, 120)
    sess_start = datetime(sess_start_date.year, sess_start_date.month, sess_start_date.day,
                          start_hour, start_min, 0)
    sess_end = sess_start + timedelta(minutes=duration_min)
    is_new_user = random.random() < 0.08
    streaming_sessions_data.append({
        "session_id": sess_id,
        "user_id": user_id,
        "session_start": sess_start.isoformat(),
        "session_end": sess_end.isoformat(),
        "platform": platform,
        "device_type": device_type,
        "country": "GB",
        "is_new_user": is_new_user,
    })
    session_user_map[sess_id] = user_id

write_csv("streaming_sessions.csv",
          ["session_id", "user_id", "session_start", "session_end", "platform",
           "device_type", "country", "is_new_user"],
          streaming_sessions_data)

session_ids = [s["session_id"] for s in streaming_sessions_data]


# ════════════════════════════════════════════════════════════════════════════════
# 12. STREAMING PLAY EVENTS (20000 rows)
# ════════════════════════════════════════════════════════════════════════════════
event_types = ["start", "25pct", "50pct", "75pct", "complete"]

# Completion rate by genre
genre_completion_probs = {
    "drama":         0.72,
    "comedy":        0.68,
    "factual":       0.60,
    "entertainment": 0.65,
    "news":          0.55,
    "sport":         0.58,
    "film":          0.70,
}

play_events_data = []
play_event_id = 1
play_event_ids = []

# Use content programmes only (no promos for play events)
avod_programme_ids = content_programme_ids

for _ in range(5000):
    sess_id = random.choice(session_ids)
    user_id = session_user_map[sess_id]
    prog_id = random.choice(avod_programme_ids)
    genre = prog_genre_map.get(prog_id, "entertainment")
    completion_prob = genre_completion_probs.get(genre, 0.60)
    ep_list = prog_ep_map.get(prog_id, [])
    ep_id = random.choice(ep_list) if ep_list else ""

    # Get session start to anchor event timestamps
    sess = streaming_sessions_data[int(sess_id[1:]) - 1]
    sess_start = datetime.fromisoformat(sess["session_start"])

    # Generate event progression
    event_ts_base = sess_start + timedelta(seconds=random.randint(0, 300))
    platform = sess["platform"]

    # Duration from programme
    prog_dur = next((p["duration_min"] for p in programmes_data if p["programme_id"] == prog_id), 30)
    dur_sec = prog_dur * 60

    # Determine how far viewer watches
    rand = random.random()
    if rand < (1 - completion_prob) * 0.3:
        max_events = 1  # just start
    elif rand < (1 - completion_prob) * 0.6:
        max_events = 2  # start + 25pct
    elif rand < (1 - completion_prob) * 0.8:
        max_events = 3  # start + 25pct + 50pct
    elif rand < (1 - completion_prob):
        max_events = 4  # start + 25pct + 50pct + 75pct
    else:
        max_events = 5  # complete

    for evt_idx, evt_type in enumerate(event_types[:max_events]):
        position_sec_map = {"start": 0, "25pct": dur_sec // 4, "50pct": dur_sec // 2,
                            "75pct": 3 * dur_sec // 4, "complete": dur_sec}
        position_sec = position_sec_map[evt_type]
        evt_ts = event_ts_base + timedelta(seconds=position_sec)
        eid = f"EV{play_event_id:08d}"
        play_events_data.append({
            "event_id": eid,
            "event_timestamp": evt_ts.isoformat(),
            "user_id": user_id,
            "session_id": sess_id,
            "programme_id": prog_id,
            "episode_id": ep_id,
            "event_type": evt_type,
            "position_sec": position_sec,
            "platform": platform,
        })
        play_event_ids.append(eid)
        play_event_id += 1

write_csv("streaming_play_events.csv",
          ["event_id", "event_timestamp", "user_id", "session_id", "programme_id",
           "episode_id", "event_type", "position_sec", "platform"],
          play_events_data)


# ════════════════════════════════════════════════════════════════════════════════
# 13. AD SPOTS AVOD (6000 rows)
# ════════════════════════════════════════════════════════════════════════════════
# Each row is an ad impression linked to a play event (start/mid roll)
ad_positions = ["pre", "mid", "post"]
ad_positions_weights = [50, 40, 10]

avod_spots_data = []
impression_id = 1

# Only use start events for pre-roll, 50pct for mid-roll, complete for post-roll
start_events = [e for e in play_events_data if e["event_type"] == "start"]
mid_events = [e for e in play_events_data if e["event_type"] == "50pct"]
complete_events = [e for e in play_events_data if e["event_type"] == "complete"]

# Build a pool of events to serve ads against
ad_event_pool = (
    [(e, "pre") for e in random.sample(start_events, min(3000, len(start_events)))] +
    [(e, "mid") for e in random.sample(mid_events, min(2400, len(mid_events)))] +
    [(e, "post") for e in random.sample(complete_events, min(600, len(complete_events)))]
)
random.shuffle(ad_event_pool)
ad_event_pool = ad_event_pool[:6000]

for evt, ad_pos in ad_event_pool:
    camp_id = random.choice(campaign_ids)
    served_at = datetime.fromisoformat(evt["event_timestamp"]) + timedelta(seconds=random.randint(0, 5))
    # AVOD CPM £20-£45
    cpm = round(random.uniform(20, 45), 2)
    rev = round(cpm / 1000, 4)  # per impression
    device_type_for_session = next(
        (s["device_type"] for s in streaming_sessions_data if s["session_id"] == evt["session_id"]),
        "mobile"
    )
    avod_spots_data.append({
        "impression_id": f"IMP{impression_id:08d}",
        "campaign_id": camp_id,
        "play_event_id": evt["event_id"],
        "served_at": served_at.isoformat(),
        "programme_id": evt["programme_id"],
        "ad_position": ad_pos,
        "device_type": device_type_for_session,
        "revenue_gbp": rev,
    })
    impression_id += 1

write_csv("ad_spots_avod.csv",
          ["impression_id", "campaign_id", "play_event_id", "served_at", "programme_id",
           "ad_position", "device_type", "revenue_gbp"],
          avod_spots_data)


# ════════════════════════════════════════════════════════════════════════════════
# 14. BARB CONSOLIDATED AUDIENCE (~400 rows)
# ════════════════════════════════════════════════════════════════════════════════
# One row per broadcast_date × programme × channel for MAIN portfolio
# Sample ~40 dates across the year
barb_dates = [date(2025, 1, 1) + timedelta(days=d) for d in
              [0, 7, 14, 21, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180,
               195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 359, 360, 361, 362, 363]]
cutoff_date = date(2025, 12, 31) - timedelta(days=7)  # last 7 days

media_company_broadcast_progs = [p["programme_id"] for p in programmes_data
                      if p["programme_id"] not in ("P063", "P064", "P065")][:30]

barb_consolidated_data = []
for bdate in barb_dates:
    # Sample 12-20 programmes for this date
    day_progs = random.sample(media_company_broadcast_progs, k=min(15, len(media_company_broadcast_progs)))
    for prog_id in day_progs:
        ch_id = random.choice(["MAIN", "EXTRA", "FACTUAL", "MOVIES", "CATCHUP"])
        overnight = round(random.uniform(0.5, 5.5), 3)
        # Flagship shows get higher audiences
        if prog_id in ("P001", "P002", "P003"):
            overnight = round(random.uniform(3.0, 6.5), 3)
        c7_base = round(overnight * random.uniform(1.1, 1.6), 3)
        # NULL c7 for last 7 days (TX+8 rule)
        if bdate > cutoff_date:
            c7_viewers = ""
            c7_reach = ""
        else:
            c7_viewers = c7_base
            c7_reach = round(c7_base * random.uniform(1.05, 1.3), 3)

        barb_consolidated_data.append({
            "broadcast_date": bdate.isoformat(),
            "programme_id": prog_id,
            "channel_id": ch_id,
            "overnight_viewers_thousands": overnight,
            "c7_viewers_thousands": c7_viewers,
            "c7_reach_thousands": c7_reach,
            "_loaded_at": LOADED_AT,
        })

write_csv("barb_consolidated_audience.csv",
          ["broadcast_date", "programme_id", "channel_id", "overnight_viewers_thousands",
           "c7_viewers_thousands", "c7_reach_thousands", "_loaded_at"],
          barb_consolidated_data)


# ════════════════════════════════════════════════════════════════════════════════
# 15. BARB MINUTE RATINGS (hourly grain, ~3500 rows)
# ════════════════════════════════════════════════════════════════════════════════
# Sample representative dates across 2025
all_channels_for_barb = [c["channel_id"] for c in channels_data if c["channel_id"] != "streaming"]
barb_dates_sample = [date(2025, 1, 1) + timedelta(days=d) for d in range(0, 365, 7)]  # every week

# Peak/off-peak viewership patterns by channel
def get_tvr(channel_id, hour):
    # BBC1 peak 10-20%, MAIN peak 3-8%
    base_tvr_map = {
        "BBC1": {"peak": (10, 20), "off": (2, 6)},
        "BBC2": {"peak": (3, 7),  "off": (0.5, 2)},
        "ITV1": {"peak": (8, 18), "off": (1, 5)},
        "ITV2": {"peak": (2, 5),  "off": (0.3, 1.2)},
        "MAIN":   {"peak": (3, 8),  "off": (0.8, 2.5)},
        "EXTRA":   {"peak": (1.5, 4),"off": (0.3, 1.0)},
        "FACTUAL":{"peak": (0.8, 2),"off": (0.1, 0.5)},
        "MOVIES":{"peak": (0.5, 2),"off": (0.1, 0.4)},
        "CATCHUP":{"peak":(0.3, 1),"off": (0.05, 0.3)},
        "CHAN5": {"peak": (2, 7),  "off": (0.5, 2)},
        "SKYONE":{"peak": (0.5, 2),"off": (0.1, 0.5)},
        "SKYATL":{"peak": (0.4, 1.5),"off":(0.1, 0.4)},
    }
    is_peak = (19 <= hour < 22)
    ranges = base_tvr_map.get(channel_id, {"peak": (0.5, 2), "off": (0.1, 0.5)})
    lo, hi = ranges["peak"] if is_peak else ranges["off"]
    return round(random.uniform(lo, hi), 2)

barb_rating_rows = []
for bdate in barb_dates_sample:
    # Sample subset of channels per date to keep rows manageable
    sampled_channels = random.sample(all_channels_for_barb, k=8)
    for ch_id in sampled_channels:
        # Sample 8-16 hours per channel per day (not every hour)
        sampled_hours = random.sample(range(6, 24), k=random.randint(8, 14))
        for hour in sampled_hours:
            tvr = get_tvr(ch_id, hour)
            viewers = round(tvr / 100 * 63000, 1)  # UK 63M population
            # Pick a programme on this channel in the schedule if possible
            prog_id = random.choice(media_company_broadcast_progs) if ch_id in media_company_portfolio_channels \
                else random.choice(programme_ids)
            demo_id = random.choice(demo_ids)
            barb_rating_rows.append({
                "broadcast_date": bdate.isoformat(),
                "broadcast_hour": hour,
                "channel_id": ch_id,
                "programme_id": prog_id,
                "demographic_id": demo_id,
                "viewers_thousands": viewers,
                "tvr_pct": tvr,
                "_loaded_at": LOADED_AT,
            })

write_csv("barb_minute_ratings.csv",
          ["broadcast_date", "broadcast_hour", "channel_id", "programme_id",
           "demographic_id", "viewers_thousands", "tvr_pct", "_loaded_at"],
          barb_rating_rows)


# ════════════════════════════════════════════════════════════════════════════════
# 16. UK POPULATION BASELINE (16 demos × 2 years = 32 rows)
# ════════════════════════════════════════════════════════════════════════════════
# UK 4+ population ≈ 63,000 thousands, split proportionally
# Age band weights (rough UK distribution for 4+):
#   4-15: ~13%, 16-34: ~25%, 35-54: ~27%, 55+: ~35%
# Gender: ~50/50
# Social grade: ABC1 ~55%, C2DE ~45%
age_weights = {"4-15": 0.13, "16-34": 0.25, "35-54": 0.27, "55+": 0.35}
gender_weights = {"M": 0.49, "F": 0.51}
grade_weights = {"ABC1": 0.55, "C2DE": 0.45}
TOTAL_POP = 63000

pop_baseline_data = []
for year in [2024, 2025]:
    for d in demographics_data:
        age = d["age_band"]
        gender = d["gender"]
        grade = d["social_grade"]
        pop = round(TOTAL_POP * age_weights[age] * gender_weights[gender] * grade_weights[grade])
        pop_baseline_data.append({
            "year": year,
            "demographic_id": d["demographic_id"],
            "population_thousands": pop,
        })

write_csv("uk_population_baseline.csv",
          ["year", "demographic_id", "population_thousands"],
          pop_baseline_data)


# ════════════════════════════════════════════════════════════════════════════════
# VERIFICATION
# ════════════════════════════════════════════════════════════════════════════════
print("\n--- Verification ---")

# Row counts
print(f"channels: {len(channels_data)} (expect 13)")
print(f"demographics: {len(demographics_data)} (expect 16)")
print(f"dayparts: {len(dayparts_data)} (expect 6)")
print(f"advertisers: {len(advertisers_data)} (expect 25)")
print(f"programmes: {len(programmes_data)} (expect 65)")
print(f"episodes: {len(episodes_data)}")
print(f"schedule: {len(schedule_data)}")
print(f"ad_campaigns: {len(ad_campaigns_data)}")
print(f"ad_spots_linear: {len(ad_spots_linear_data)}")
print(f"ad_spots_avod: {len(avod_spots_data)}")
print(f"advertisers: {len(advertisers_data)}")
print(f"streaming_play_events: {len(play_events_data)}")
print(f"streaming_sessions: {len(streaming_sessions_data)}")
print(f"streaming_users: {len(streaming_users_data)}")
print(f"barb_consolidated_audience: {len(barb_consolidated_data)}")
print(f"barb_minute_ratings: {len(barb_rating_rows)}")
print(f"uk_population_baseline: {len(pop_baseline_data)} (expect 32)")

# FK checks
print("\n--- FK checks ---")

# streaming sentinel in channels
assert any(c["channel_id"] == "streaming" for c in channels_data), "FAIL: streaming sentinel missing"
print("channels: streaming sentinel present")

# demographics: exactly 16
assert len(demographics_data) == 16, f"FAIL: demographics count {len(demographics_data)}"
print("demographics: exactly 16 rows")

# programmes: news_current_affairs flag
assert any(p["is_news_current_affairs"] for p in programmes_data), "FAIL: no news programme"
print("programmes: is_news_current_affairs flag present")

# programmes: trailers/promos
promos = [p for p in programmes_data if p["duration_min"] < 5]
assert len(promos) >= 2, f"FAIL: only {len(promos)} promo programmes"
print(f"programmes: {len(promos)} promo/trailer rows (duration_min < 5)")

# barb_consolidated_audience: last 7 days have NULL c7
last_7_rows = [r for r in barb_consolidated_data
               if date.fromisoformat(r["broadcast_date"]) > cutoff_date]
null_c7_rows = [r for r in last_7_rows if r["c7_viewers_thousands"] == ""]
print(f"barb_consolidated: {len(last_7_rows)} rows after cutoff, {len(null_c7_rows)} with null c7")

# ad_spots_linear: ~5% under-delivery
under_delivery = [r for r in ad_spots_linear_data
                  if float(r["delivered_impressions_thousands"]) < 0.95 * float(r["booked_impressions_thousands"])]
pct = len(under_delivery) / len(ad_spots_linear_data) * 100
print(f"ad_spots_linear: {len(under_delivery)} under-delivery rows ({pct:.1f}%)")

# streaming_users: all active
inactive_users = [u for u in streaming_users_data if not u["is_active"]]
print(f"streaming_users: {len(inactive_users)} inactive users (expect 0)")

# barb_minute_ratings: row count
print(f"barb_minute_ratings: {len(barb_rating_rows)} rows")

# population baseline
assert len(pop_baseline_data) == 32, f"FAIL: pop_baseline rows {len(pop_baseline_data)}"
print("uk_population_baseline: exactly 32 rows")

print("\nAll checks passed.")
