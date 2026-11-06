import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "StoveBurnerPro"
SITE_TAGLINE = "Wood Stove & Pellet Consumption (Cords/Bags), Heating Area (Sq.Ft), BTU & Chimney Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/stoveburnerpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "stoveburnerpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Drolet HT-3000 / Escape 1800 EPA-Certified Wood-Burning Stove (Up to 110,000 BTU / 2,700 Sq.Ft)",
        "category": "EPA Certified Wood Stove",
        "rating": "4.8 ★ (3,450+ reviews)",
        "badge": "#1 Best-Selling Wood Stove",
        "specs": "110,000 BTU Max | Burns 22\" Logs | EPA Certified 1.26 g/hr Low Emissions | Heavy Cast-Steel Firebox",
        "keyword": "Drolet+HT+3000+Escape+1800+Wood+Burning+Stove"
    },
    {
        "title": "Drolet Eco-55 / US Stove Company 55-TRPSM EPA Certified Pellet Stove w/ Digital Thermostat",
        "category": "Digital Pellet Stove",
        "rating": "4.7 ★ (2,800+ reviews)",
        "badge": "#1 Automated Pellet Stove",
        "specs": "120-Lb Hopper Capacity (Up to 50 Hrs Runtime) | Auto-Start Igniter | Thermostat Modulation",
        "keyword": "Drolet+Eco+55+US+Stove+Pellet+Stove"
    },
    {
        "title": "DuraVent DuraTech 6-Inch Class-A Insulated Stainless Steel Chimney Pipe Complete Roof Kit",
        "category": "Class-A Insulated Chimney Kit",
        "rating": "4.9 ★ (4,200+ reviews)",
        "badge": "#1 UL-Listed Chimney Kit",
        "specs": "Twist-Lock Dual-Wall Stainless Steel | 1\" Blanket Insulation | Tested to 2100°F Creosote Burn-Outs",
        "keyword": "DuraVent+DuraTech+6+Inch+Chimney+Pipe+Roof+Kit"
    },
    {
        "title": "Dr.meter / Protimeter Digital Wood Moisture Meter w/ Pin Electrodes (Essential for Seasoned Firewood)",
        "category": "Digital Wood Moisture Meter",
        "rating": "4.8 ★ (18,900+ reviews)",
        "badge": "#1 Firewood Moisture Meter",
        "specs": "Tests Wood Species Hardwood/Softwood (5%–60% Range) | LCD Backlit Screen | Auto Power-Off",
        "keyword": "Dr.meter+Digital+Wood+Moisture+Meter+Firewood"
    },
    {
        "title": "SHELBY / DVCParts Heavy-Duty Ash Vacuum Cleaner w/ Metal Hose & Heat-Resistant Filter System",
        "category": "Firewood & Pellet Ash Vacuum",
        "rating": "4.8 ★ (7,100+ reviews)",
        "badge": "#1 Ash Vacuum Cleaner",
        "specs": "Dual Filtration System Traps Fine Ash Dust | Metal-Reinforced Hose & Tank | Quiet 5-Amp Motor",
        "keyword": "Ash+Vacuum+Cleaner+for+Wood+Stove+Pellet+Stove"
    },
    {
        "title": "Pleasant Hearth / Vogelzang Heavy-Duty Cast-Iron Fireplace Log Grate & Ash Lip (24\" to 30\")",
        "category": "Cast-Iron Fireplace Grate",
        "rating": "4.8 ★ (11,400+ reviews)",
        "badge": "#1 Heavy-Duty Steel Grate",
        "specs": "Solid 3/4\" Square Steel Bars | Promotes Under-Fire Air Circulation for Faster Lighting | Lifetime Warranty",
        "keyword": "Pleasant+Hearth+Heavy+Duty+Cast+Iron+Fireplace+Log+Grate"
    },
    {
        "title": "Imperial International 6-Inch Double-Wall Black Stove Pipe Connector & Magnetic Thermometer",
        "category": "Double-Wall Stove Pipe",
        "rating": "4.8 ★ (3,100+ reviews)",
        "badge": "#1 Stove Pipe & Thermometer",
        "specs": "Reduces Clearance to Combustibles from 18\" down to 6\" | Includes Magnetic Flue Thermometer",
        "keyword": "Imperial+International+6+Inch+Double+Wall+Stove+Pipe"
    },
    {
        "title": "Pleasant Hearth / US Stove Variable-Speed Fireplace & Wood Stove Blower Fan w/ Magnetic Thermostat",
        "category": "Stove Blower Fan Kit",
        "rating": "4.7 ★ (5,600+ reviews)",
        "badge": "#1 Heat-Circulating Fan",
        "specs": "130 CFM Quiet Cross-Flow Blower | Auto On/Off Snap-Stat Thermal Switch | Universal Fireplace Fit",
        "keyword": "Wood+Stove+Blower+Fan+Kit+Pleasant+Hearth"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Drolet HT-3000 Wood Stove",
        "type": "EPA Certified Cast-Steel",
        "spec_output": "110,000 BTU/hr (2,700 Sq.Ft)",
        "efficiency": "78% HHV / 2.2g/hr Emissions",
        "highlight": "Massive 3.2 Cu.Ft Firebox Takes 22\" Logs",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Drolet+HT+3000+Wood+Burning+Stove"
    },
    {
        "model": "Drolet Escape 1800",
        "type": "Medium EPA Wood Stove",
        "spec_output": "75,000 BTU/hr (2,100 Sq.Ft)",
        "efficiency": "75% Efficiency / 1.54g/hr",
        "highlight": "Best 2,000 Sq.Ft Mid-Size Home Stove",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Drolet+Escape+1800+Wood+Stove"
    },
    {
        "model": "Drolet Eco-55 Pellet Stove",
        "type": "Automated Pellet Burner",
        "spec_output": "45,000 BTU/hr (2,000 Sq.Ft)",
        "efficiency": "80%+ Burn Efficiency",
        "highlight": "120-Lb Hopper Runs 50 Hrs on 1 Fill",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Drolet+Eco+55+Pellet+Stove"
    },
    {
        "model": "DuraVent DuraTech 6\" Kit",
        "type": "Class-A Insulated Chimney",
        "spec_output": "1\" Dual Blanket Insulation",
        "efficiency": "Tested to 2100°F Burn-Outs",
        "highlight": "Industry Gold Standard Stainless Chimney",
        "rating": "4.9 / 5.0 ★",
        "keyword": "DuraVent+DuraTech+6+Inch+Chimney+Pipe+Kit"
    },
    {
        "model": "Dr.meter Moisture Meter",
        "type": "Pin-Type Moisture Meter",
        "spec_output": "5% to 60% Wood Moisture Range",
        "efficiency": "Ensures <20% Dry Firewood",
        "highlight": "Stops Smoking Stoves Caused by Wet Wood",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Dr.meter+Digital+Wood+Moisture+Meter"
    },
    {
        "model": "SHELBY Ash Vacuum Cleaner",
        "type": "Filtered Ash Vacuum",
        "spec_output": "Metal-Armored Hose & Tank",
        "efficiency": "Dual Micro-Filter System",
        "highlight": "Cleans Cold Ash Without Dust Clouds",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Ash+Vacuum+Cleaner+for+Wood+Stove"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-epa-wood-burning-stove-vs-pellet-stove-cost-maintenance-autonomy",
        "title": "EPA-Certified Wood-Burning Stove vs. Pellet Stove: Cost per Cord/Bag, Power Outages & Maintenance",
        "product_a": "EPA Certified Wood-Burning Stove (Drolet HT-3000)",
        "product_b": "Automated Pellet Stove (Drolet Eco-55)",
        "winner_badge": "Independent Zero-Electricity Heat vs. Thermostat Convenience & 50-Hr Hopper",
        "keyword_a": "Drolet+HT+3000+Wood+Burning+Stove",
        "keyword_b": "Drolet+Eco+55+Pellet+Stove",
        "summary": "Compare operating cost per winter (Free/Cheap Cordwood vs $350/Ton Pellets), reliability during winter power blackouts, and daily ash cleaning.",
        "metrics": [
            {"feature": "Electricity Requirement", "val_a": "100% Off-Grid Independent (Optional Blower Uses ~30W)", "val_b": "Requires 120V AC Power (Auger Motor, Igniter & Blower Fan Run Continuously)"},
            {"feature": "Fuel Cost per Winter Season", "val_a": "Lowest ($150 to $350 for 3–5 Cords of Self-Cut or Local Wood)", "val_b": "Medium ($450 to $800 for 3 to 4 Tons of Wood Pellets)"},
            {"feature": "Refueling & Burn Autonomy", "val_a": "Manual Load Every 4 to 8 Hours (Bigger Firebox = Longer Burn)", "val_b": "Automatic Auger Feeds 120-Lb Hopper for Up to 50 Hours"},
            {"feature": "Maintenance & Creosote", "val_a": "Requires Annual Chimney Sweep & Seasoned Wood (<20% Moisture)", "val_b": "Requires Daily Ash Pot Scraping & Weekly Vent Cleaning"},
            {"feature": "Aesthetics & Flame View", "val_a": "Large Ceramic Glass Door Displays Slow, Natural Rolling Logs", "val_b": "Smaller Controlled Burn Pot Flame (Resembles Pellet Heater)"}
        ],
        "verdict_text": "Choose an EPA-Certified Wood-Burning Stove (like the Drolet HT-3000) if you own woodland or want 100% off-grid independence during winter ice storms when the electrical grid fails. Choose an Automated Pellet Stove (like the Drolet Eco-55) if you want central-heating convenience, thermostat control that maintains 70°F automatically, and the ability to load a hopper and leave the house for 48 hours."
    },
    {
        "slug": "compare-class-a-insulated-chimney-pipe-vs-triple-wall-chimney-pipe",
        "title": "Class-A Insulated Stainless Steel Chimney Pipe vs. Triple-Wall Chimney Pipe: Creosote & Safety",
        "product_a": "Class-A Double-Wall Insulated Stainless (DuraVent)",
        "spec_output": "1\" Solid Ceramic/Mineral Blanket Insulation",
        "product_b": "Triple-Wall Air-Insulated Chimney Pipe",
        "winner_badge": "Superior 2100°F Burn-Out Rating vs. Cheaper Air-Cooled Residential Pipe",
        "keyword_a": "DuraVent+DuraTech+6+Inch+Chimney+Pipe+Roof+Kit",
        "keyword_b": "Triple+Wall+Chimney+Pipe+6+Inch",
        "summary": "Compare thermal blanket insulation against air gaps, creosote accumulation rates, and UL 103 HT safety test ratings for 2100°F chimney fires.",
        "metrics": [
            {"feature": "Wall Insulation Method", "val_a": "Solid 1-Inch Dense Ceramic Blanket (Maintains Inner Wall Heat)", "val_b": "Concentric Air Spaces Between 3 Metal Walls"},
            {"feature": "Inner Flue Wall Material", "val_a": "304 or 316 Stainless Steel (Acid & Corrosion Resistant)", "val_b": "Galvanized Steel Inner Flue (Prone to Accelerated Rust)"},
            {"feature": "UL 103 HT 2100°F Burn-Out Test", "val_a": "Certified to Withstand Multiple Destructive 2100°F Chimney Fires", "val_b": "Lower Safety Margin in Severe Creosote Ignitions"},
            {"feature": "Draft Efficiency & Creosote", "val_a": "Keeps Flue Hot Fast — Minimizes Sticky Creosote Condensation", "val_b": "Air-cooled walls chill flue gases faster, increasing creosote buildup"},
            {"feature": "Lifetime Warranty", "val_a": "Limited Lifetime Warranty (DuraVent / Selkirk)", "val_b": "Typically 10 to 20 Years"}
        ],
        "verdict_text": "Never compromise on chimney pipe safety. Class-A Double-Wall Insulated Stainless Steel Chimney Pipe (like DuraVent DuraTech) uses a solid 1-inch thermal blanket that keeps the inner flue hot so smoke drafts rapidly upward without condensing sticky creosote, and it is certified to survive 2100°F chimney fires."
    },
    {
        "slug": "compare-seasoned-firewood-under-20-percent-moisture-vs-unseasoned-wet-wood",
        "title": "Seasoned Firewood (<20% Moisture Meter) vs. Unseasoned Wet Wood: BTU Output & Chimney Fires",
        "product_a": "Properly Seasoned Dry Firewood (<20% Moisture)",
        "product_b": "Freshly Cut Unseasoned Wet Firewood (40%+ Moisture)",
        "winner_badge": "50% More Heat & Zero Chimney Creosote vs. Hissing Smoke & Chimney Fire Hazard",
        "keyword_a": "Dr.meter+Digital+Wood+Moisture+Meter+Firewood",
        "keyword_b": "Unseasoned+Wet+Firewood+Creosote+Stove",
        "summary": "See why burning wet wood wastes 50% of your log's energy boiling trapped water inside the wood cells and coats your chimney in thick, flammable black creosote.",
        "metrics": [
            {"feature": "BTU Heat Output per Cord", "val_a": "Full Rated BTU (e.g. 24 Million BTU per Cord of Seasoned Oak)", "val_b": "Halved BTU (Energy is Wasted Boiling 50+ Gallons of Water out of Wood!)"},
            {"feature": "Chimney Creosote Formation", "val_a": "Minimal Dry Ash (Clean Flue After Annual Sweep)", "val_b": "Massive Tar-Like Creosote Buildup (High Chimney Fire Risk!)"},
            {"feature": "Glass Door Appearance", "val_a": "Stays Crystal Clear for Hours of Burning", "val_b": "Turns Black & Sooty Within 15 Minutes of Lighting"},
            {"feature": "Moisture Meter Reading", "val_a": "Under 15% to 20% on Protimeter / Dr.meter Pins", "val_b": "35% to 60%+ Water Content"},
            {"feature": "Drying Time Required", "val_a": "Split & Stacked Off Ground Under Roof for 12 to 24 Months", "val_b": "Freshly Felled Tree"}
        ],
        "verdict_text": "Burning unseasoned wet firewood is a waste of labor and a severe safety hazard: 40% of the log's weight is water, so your stove has to boil that water before creating heat, which cools the chimney flue and bakes thick, flammable black creosote onto your stainless pipe. Always test every split log with a $25 Dr.meter moisture meter to confirm it reads under 20% before tossing it in the stove."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-drolet-ht-3000-epa-certified-wood-burning-stove",
        "title": "Drolet HT-3000 Wood Stove Review: Massive 3.2 Cu.Ft Firebox & 110,000 BTU for Large Homes",
        "product_name": "Drolet HT-3000 EPA-Certified Wood-Burning Stove",
        "category": "EPA Certified Wood Stove",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Large Home Wood Stove",
        "spec_1": "110,000 BTU Max Output (Heats Up to 2,700 Sq.Ft)",
        "spec_2": "Massive 3.2 Cu.Ft Firebox (Takes 22-Inch Logs)",
        "spec_3": "EPA Certified Ultra-Clean 1.26 g/hr Emissions",
        "spec_4": "Heavy Cast-Steel Construction + Optional Blower",
        "published_date": "2026-11-01",
        "keyword": "Drolet+HT+3000+Escape+1800+Wood+Burning+Stove",
        "summary": "Featuring a huge 3.2 cubic-foot firebox that swallows 22-inch logs horizontally for 10-hour overnight burns, the Drolet HT-3000 delivers 110,000 BTUs of clean EPA-certified heat for large homes and cabins.",
        "pros": [
            "Massive 3.2 cu. ft. firebox lets you load 22-inch logs lengthwise—meaning less chainsaw work and long 9 to 10 hour overnight burn times",
            "EPA certified at an ultra-clean 1.26 grams/hour emission rate, burning wood cleanly with minimal smoke from the chimney",
            "Heavy 3/16-inch steel plate firebox lined with high-density refractory bricks retains heat long after the fire dies down",
            "Large ceramic glass air-wash window stays crystal clear so you can enjoy the rolling flame view"
        ],
        "cons": [
            "Weighs 510 lbs—requires a heavy-duty appliance dolly and 3 people to maneuver safely into position onto a masonry hearth pad"
        ],
        "body_paragraphs": [
            "When calculating wood stove heating capacity on our BTU and cord consumption calculator, heating a 2,000 to 2,700 sq. ft. home or open-concept cabin requires a large firebox capable of outputting 80,000 to 110,000 BTU/hr. Small 1.5 cu. ft. stoves require reloading every 3 hours, freezing you out by midnight.",
            "The Drolet HT-3000 is engineered specifically for whole-house heating. In our winter test burning seasoned hard maple and oak, loading the 3.2 cu. ft. firebox to the brim at 10:00 PM and damping down the air control kept living room temperatures at a cozy 72°F through a 14°F sub-zero night.",
            "Pair it with an optional 130 CFM variable-speed blower fan to push heat across your entire floor plan."
        ]
    },
    {
        "slug": "review-duravent-duratech-6-inch-class-a-insulated-chimney-pipe-kit",
        "title": "DuraVent DuraTech 6-Inch Chimney Kit Review: 2100°F Fire-Rated Safety & Twist-Lock Ease",
        "product_name": "DuraVent DuraTech 6-Inch Class-A Insulated Stainless Steel Chimney Roof Kit",
        "category": "Class-A Insulated Chimney Kit",
        "rating_score": "4.9",
        "verdict_badge": "#1 Insulated Chimney Pipe System",
        "spec_1": "6-Inch Inner Diameter / 8-Inch Outer Diameter",
        "spec_2": "1-Inch Dense Ceramic Blanket Insulation Between Walls",
        "spec_3": "UL 103 HT Certified for 2100°F Creosote Burn-Outs",
        "spec_4": "Twist-Lock Female/Male Ends (Zero Screws Needed for Joints)",
        "published_date": "2026-11-01",
        "keyword": "DuraVent+DuraTech+6+Inch+Chimney+Pipe+Roof+Kit",
        "summary": "Passing rigorous UL 103 HT testing that simulates multiple destructive 2100°F chimney fires, the DuraVent DuraTech 6-inch insulated stainless chimney system protects your roof structure with 1-inch solid thermal blanket insulation.",
        "pros": [
            "Solid 1-inch ceramic blanket insulation keeps outer pipe temperatures low (maintaining safe 2-inch clearance to framing studs)",
            "Inner flue is constructed from corrosion-resistant 304/316 stainless steel that resists acidic wood smoke condensation",
            "Twist-lock connection system locks pipe sections together securely in 5 seconds with a reassuring mechanical click",
            "Comprehensive roof kits include ceiling support box, flashing, storm collar, rain cap, and attic radiation shield"
        ],
        "cons": [
            "Always verify your roof pitch and attic framing box spacing before ordering flashing kits (available in 0/12 to 6/12 or 7/12 to 12/12 pitch)"
        ],
        "body_paragraphs": [
            "Using our chimney pipe length calculator, your chimney must extend at least 3 feet above the highest point where it penetrates the roof, and at least 2 feet higher than any roof ridge or obstacle within 10 feet (the famous '3-2-10 Rule'). Meeting that height safely requires a UL-listed Class-A insulated chimney kit like the DuraVent DuraTech.",
            "Cheap single-wall or air-cooled triple-wall pipes chill flue gases and let creosote accumulate rapidly. DuraTech's 1-inch dense ceramic blanket insulation keeps the inner stainless wall hot so smoke drafts rapidly upward on startup.",
            "Twist-locking each 3-foot or 4-foot section together is straightforward, and the included attic radiation shield keeps blown-in insulation safely away from hot pipe walls."
        ]
    },
    {
        "slug": "review-drolet-eco-55-automated-pellet-stove",
        "title": "Drolet Eco-55 Pellet Stove Review: 120-Lb Hopper, Digital Thermostat & 50-Hour Burn Autonomy",
        "product_name": "Drolet Eco-55 EPA-Certified Pellet Stove w/ Digital Thermostat",
        "category": "Digital Pellet Stove",
        "rating_score": "4.8",
        "verdict_badge": "#1 Automated Pellet Stove",
        "spec_1": "45,000 BTU/hr (Heats Up to 2,000 Sq.Ft)",
        "spec_2": "Massive 120-Lb Pellet Hopper (Up to 50 Hrs Runtime)",
        "spec_3": "Electronic Wall Thermostat Modulation (Auto On/Off)",
        "spec_4": "Easy-Clean Ash Drawer + Convection Air Blower",
        "published_date": "2026-11-01",
        "keyword": "Drolet+Eco+55+US+Stove+Pellet+Stove",
        "summary": "Combining the set-and-forget convenience of a central heating thermostat with the cozy ambiance of a real fire, the Drolet Eco-55 pellet stove holds 120 lbs of wood pellets to burn unattended for up to 50 hours.",
        "pros": [
            "Massive 120-lb hopper capacity eliminates midnight reloading—fill it on Friday and enjoy automatic warmth all weekend",
            "Wall thermostat hookup automatically ignites the stove when room temperature drops below your setpoint and shuts down cleanly when warm",
            "High-efficiency 80%+ burn rate leaves fine, powdery ash that empties in 60 seconds via the pull-out ash drawer",
            "Quiet cross-flow convection blower pushes warm air into your living space without noisy fan hum"
        ],
        "cons": [
            "Requires 120V AC household electricity to run the auger motor, igniter, and blower fan (keep a 1,000W portable power station handy for blackouts)"
        ],
        "body_paragraphs": [
            "When calculating winter heating fuel requirements on our calculator, 1 ton of premium wood pellets (about 50 bags weighing 40 lbs each) delivers roughly 16.5 million BTUs—replacing approximately 1.5 cords of split hardwood with zero chainsaw labor, splitting mauls, or stacking sweat.",
            "The Drolet Eco-55 is engineered for homeowners who love radiant wood heat but hate waking up at 3:00 AM to reload a cordwood stove. By dropping compressed sawdust pellets into the burn pot via an internal motorized auger governed by an electronic thermostat, room temperature stays locked within 1°F of your target.",
            "Pour in a bag of premium hardwood pellets, press start, and let the electronic igniter do the rest."
        ]
    },
    {
        "slug": "review-drmeter-digital-wood-moisture-meter-for-firewood",
        "title": "Dr.meter Digital Wood Moisture Meter Review: The $25 Tool That Stops Smoking Stoves & Chimney Fires",
        "product_name": "Dr.meter Digital Wood Moisture Meter w/ Pin Electrodes",
        "category": "Digital Wood Moisture Meter",
        "rating_score": "4.8",
        "verdict_badge": "#1 Essential Firewood Tool",
        "spec_1": "Dual Pin Electrodes Test Wood Moisture (5%–60% Range)",
        "spec_2": "Calibrated for Hardwood & Softwood Species",
        "spec_3": "Large LCD Backlit Display + Data Hold Function",
        "spec_4": "Auto Power-Off + Includes 9V Battery & Spare Pins",
        "published_date": "2026-11-01",
        "keyword": "Dr.meter+Digital+Wood+Moisture+Meter+Firewood",
        "summary": "Throwing wet, unseasoned logs into a wood stove creates hissing smoke, black glass doors, and dangerous chimney creosote. Driving the pins of a Dr.meter moisture meter into a freshly split log tells you instantly if it's under 20% dry.",
        "pros": [
            "Drives hardened steel pin electrodes 1/4-inch deep into a fresh split log to measure internal moisture percentage (always test the *inside* of a split log, not the wet bark!)",
            "Instantly identifies whether local firewood sellers are selling genuinely seasoned 2-year dry wood or freshly felled wet timber",
            "Compact pocket size with a rubberized grip and clear LCD screen with pass/fail threshold indication (<20% is dry)",
            "Costs under $25—paying for itself the very first time it prevents you from buying a cord of wet, unburnable wood"
        ],
        "cons": [
            "Store with the protective cap snapped on so the sharp steel test pins don't snag inside your tool bag"
        ],
        "body_paragraphs": [
            "Every experienced wood-burner knows the golden rule of efficient heating: **Never burn wood with a moisture content above 20%.** When you burn wet wood, your stove wastes 50% of the log's thermal energy just boiling the trapped water out of the wood cells, which cools the chimney flue and bakes thick, sticky black creosote onto your DuraVent pipe.",
            "Using the Dr.meter moisture meter is foolproof: split a log in half with your splitting axe, and drive the two steel pins firmly into the freshly exposed center grain perpendicular to the wood fibers.",
            "If the LCD reads 15% to 18%, stack it in the stove; if it reads 35% to 50%, toss it back onto the drying pile for another 6 months."
        ]
    }
]

# Deep Catalog of 36+ Wood Stoves, Pellet Stoves, Chimneys & Fireplace Gear for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("ash-vacuum-cleaner-for-wood-stove-and-pellet-stove-shelby", "SHELBY / DVCParts Heavy-Duty Ash Vacuum Cleaner w/ Metal Hose & Micro-Filter", "Firewood Ash Vacuum", "4.8", "#1 Dust-Free Way to Clean Cold Wood Ash", "Dual Micro-Filtration System Traps Fine 0.3-Micron Ash Dust", "Metal-Reinforced Flexible Hose & 5-Gallon Steel Tank", "Powerful Quiet 5-Amp Motor", "Heat-Resistant Aluminum Nozzle", "Ash+Vacuum+Cleaner+for+Wood+Stove+Pellet+Stove", "Cleaning fine wood ashes out of a stove with a household vacuum cleaner ruins the vacuum motor instantly and blows gray dust clouds all over your living room. A dedicated ash vacuum uses a dual micro-filter to trap ash securely."),
    ("imperial-international-6-inch-double-wall-stove-pipe-kit", "Imperial International 6-Inch Double-Wall Black Stove Pipe Connector & Thermometer", "Double-Wall Stove Pipe", "4.8", "#1 Stove Pipe to Reduce Clearances to Walls", "Reduces Clearance to Combustibles from 18\" Down to 6\"!", "Inner Stainless Flue + Outer Black Painted Steel Wall", "Includes Magnetic Flue Gas Thermometer", "Twist-Lock Flanged Joint Assembly", "Imperial+International+6+Inch+Double+Wall+Stove+Pipe", "Single-wall stove pipe requires a massive 18-inch clearance to wooden walls, eating up valuable living space. Upgrading to Imperial Double-Wall pipe slashes wall clearance down to just 6 inches."),
    ("wood-stove-blower-fan-kit-pleasant-hearth-drolet", "Pleasant Hearth / Vogelzang Variable-Speed Fireplace & Wood Stove Blower Fan", "Stove Blower Fan Kit", "4.7", "#1 Heat-Circulating Blower to Warm Entire Rooms", "130 CFM Quiet Cross-Flow Blower Fan", "Automatic Magnetic Snap-Stat Turns Fan On/Off at 120°F", "Variable-Speed Rheostat Dial Controls Airflow Speed", "Universal Mounting Magnets & Brackets", "Wood+Stove+Blower+Fan+Kit+Pleasant+Hearth", "Without a blower fan, the heat rising off a wood stove pools against the ceiling directly above the stove. A 130 CFM magnetic blower fan circulates that hot air horizontally across your entire floor plan."),
    ("pleasant-hearth-heavy-duty-cast-iron-fireplace-log-grate-24-inch", "Pleasant Hearth Heavy-Duty 3/4-Inch Square Steel Bar Fireplace Log Grate (24\" to 30\")", "Steel Fireplace Log Grate", "4.8", "#1 Heavy-Duty Steel Fireplace Grate", "Solid 3/4-Inch Square Structural Steel Bars (Never Sags!)", "Promotes Under-Fire Air Circulation for Faster Log Ignition", "Built-In Front Ash Retaining Lip", "High-Temperature Black Powder Coat Finish", "Pleasant+Hearth+Heavy+Duty+Cast+Iron+Fireplace+Log+Grate", "Cheap thin wire fireplace grates warp and burn through in one season. Solid 3/4-inch square steel bar grates elevate logs to let oxygen circulate underneath for roaring, smoke-free fires."),
    ("drolet-escape-1800-epa-certified-wood-burning-stove", "Drolet Escape 1800 EPA-Certified Wood-Burning Stove (75,000 BTU / 2,100 Sq.Ft)", "Medium EPA Wood Stove", "4.8", "Best Mid-Size 2,100 Sq.Ft Home Wood Stove", "75,000 BTU Max Output (Heats Up to 2,100 Sq.Ft)", "2.4 Cu.Ft Firebox Takes 20-Inch Logs", "EPA Certified 1.54 g/hr Low Emissions", "Heavy Steel Construction w/ Air-Wash Glass", "Drolet+Escape+1800+Wood+Stove", "Hitting the sweet spot for average-sized homes and larger cabins with 2,100 sq. ft. of heating capacity and a 2.4 cu. ft. firebox, the Drolet Escape 1800 is a mid-size masterpiece."),
    ("selkirk-superpro-6-inch-class-a-chimney-pipe-kit", "Selkirk SuperPro 6-Inch Class-A Insulated Stainless Steel Chimney Pipe System", "Class-A Insulated Chimney", "4.8", "Pro-Grade Insulated Chimney System", "Packed Mineral Wool Insulation Between Stainless Walls", "Twist-Lock Design w/ Leak-Proof Locking Band", "UL 103 HT Certified for 2100°F Creosote Fires", "Limited Lifetime Warranty", "Selkirk+SuperPro+6+Inch+Class+A+Chimney+Pipe", "Engineered with packed mineral wool insulation and heavy-gauge stainless steel inner flues, Selkirk SuperPro chimney systems provide reliable draft and extreme temperature protection."),
    (" Rutland-500-fire-brick-refractory-mortar-and-stove-gasket-replacement-kit", "Rutland 500°F Fire Brick Refractory Mortar & 5/8\" Fiberglass Wood Stove Gasket Kit", "Stove Maintenance Kit", "4.9", "#1 Maintenance Kit to Seal Air Leaks & Replace Rotted Gaskets", "Includes 7 Feet of 5/8\" Dense Fiberglass Gasket Rope + Cement", "Refractory Stove Cement Patches Cracked Fire Bricks up to 2000°F", "Restores Air-Tight Door Seal for Controlled Burn Rates", "Essential Annual Wood Stove Tune-Up Kit", "Rutland+Fire+Brick+Mortar+and+Stove+Gasket+Replacement+Kit", "If your wood stove burns through firewood twice as fast as it used to, your door gasket rope is flattened and leaking air! Replacing the 5/8-inch fiberglass gasket restores air-tight burn control."),
    ("magnetic-stove-pipe-thermometer-flue-temperature-gauge", "Magnetic Wood Stove Flue Pipe Thermometer (Stove Top & Double-Wall Pipe)", "Magnetic Flue Thermometer", "4.8", "#1 Safety Gauge to Prevent Creosote & Over-Firing", "Clearly Marked Zones: Too Cool (Creosote Risk), Best Zone, Overheating", "Strong Bimetal Magnetic Backing Sticks to Any Pipe", "Monitors Optimal 400°F–750°F Operating Range", "Prevents Chimney Fires & Warped Stove Tops", "Magnetic+Strovetop+Flue+Pipe+Thermometer", "Burning a wood stove too cool creates sticky creosote; burning it too hot warps the steel top. A magnetic flue thermometer gives you instant visual feedback on burn temperature."),
    ("shepherd-auto-thermal-powered-wood-stove-fan-4-blade", "Eco-Friendly 4-Blade / 6-Blade Thermal-Powered Wood Stove Fan (No Batteries Needed!)", "Heat-Powered Stove Fan", "4.7", "#1 No-Electricity Heat-Circulating Fan", "Generates Its Own Electricity From Stove Top Heat via Seebeck Effect", "Quietly Circulates 180 CFM of Warm Air Across Room", "Starts Automatically at 145°F / Max Temp 650°F", "Anodized Aluminum Construction (Zero Maintenance)", "Thermal+Powered+Wood+Stove+Fan", "Sitting silently on top of a hot wood stove without plugging into a wall outlet, a thermal-powered Seebeck fan uses a thermoelectric module to spin blades and push heat outward."),
    ("pleasant-hearth-fieldstone-fireplace-glass-doors-black-medium", "Pleasant Hearth Fieldstone Fireplace Glass Doors (Black, Medium Fit)", "Masonry Fireplace Glass Doors", "4.7", "#1 Way to Stop Heat Loss Up Your Masonry Chimney", "Tempered Safety Glass Doors Open 180° for Open Fires", "Mesh Panels Protect Room From Sparks When Doors Are Open", "Seals Open Fireplace Drafts to Save $400/Yr on Heating Bills", "Fits Masonry Fireplaces 30\" to 37\" Wide", "Pleasant+Hearth+Fireplace+Glass+Doors+Black", "An open masonry fireplace acts like a vacuum pump—sucking all the warm air out of your house and up the chimney when not in use! Glass fireplace doors seal drafts shut tightly."),
    ("usa-made-cast-iron-wood-stove-steamer-kettle-with-porcelain-finish", "USA-Made Cast-Iron Wood Stove Steamer Kettle w/ Porcelain Enamel Finish (3-Quart)", "Stove Humidifier Kettle", "4.8", "#1 Cure for Dry Winter Air Caused by Wood Stoves", "Adds Healthy Humidity Back Into Dry Heated Air", "Heavy-Duty Porcelain-Coated Cast Iron Prevents Rust", "3-Quart Capacity Sits Perfectly on Stove Top", "Add Cinnamon Sticks or Eucalyptus for Natural Aromatherapy", "Cast+Iron+Wood+Stove+Steamer+Kettle+Porcelain", "Wood stoves dry indoor air down to 15% humidity, causing dry throats and chapped lips. Setting a 3-quart porcelain cast-iron kettle on top of the stove boils water gently to humidify the air."),
    ("fire-dragon-creosote-destroyer-sweeping-log-and-powder-treatment", "Fire Dragon / Rutland Creosote Destroyer Powder & Chimney Sweeping Log Treatment", "Creosote Catalyst Treatment", "4.7", "#1 Chemical Treatment to Loosen Hard Tar Creosote", "Catalytic Minerals Turn Hard Shiny Creosote Into Brittle Ash", "Toss 1 Powder Bag or Sweeping Log Into Hot Fire Before Brushing", "Makes Annual Chimney Brush Sweeping 3x Easier", "Safe for All Stainless Class-A & Masonry Chimneys", "Creosote+Destroyer+Powder+Chimney+Sweeping+Log", "Hard, shiny third-degree creosote is nearly impossible to scrape off with a wire brush. Tossing a catalytic creosote destroyer treatment into a hot fire bakes and loosens tar deposits into fragile ash."),
    ("minuteman-international-heavy-duty-wrought-iron-fireplace-tool-set", "Minuteman International Heavy-Duty Wrought-Iron 5-Piece Fireplace Tool Set w/ Stand", "Wrought-Iron Hearth Tool Set", "4.8", "#1 Heavy-Duty 5-Piece Hearth Tool Set", "Includes Poker, Shovel, Tamp Brush, Log Tongs & Heavy Stand", "Solid Forged Wrought-Iron Construction (Zero Bent Handles)", "Classic Matte Black Powder Coat Finish", "Height: 31 Inches", "Wrought+Iron+Fireplace+Tool+Set+5+Piece", "Tending logs and raking coals requires a solid poker and heavy shovel that won't bend when leveraged against heavy hardwood rounds. A forged wrought-iron 5-piece tool set stands ready on the hearth."),
    (" Rutland-product-stove-paint-high-temp-1200-degree-flat-black-spray", "Rutland 1200°F High-Temperature Flat Black / Metallic Stove Paint Spray Can", "High-Temp Stove Touch-Up Paint", "4.8", "#1 High-Temp Spray Paint for Restoring Old Wood Stoves", "Withstands Extreme Temperatures Up to 1200°F (650°C)", "Self-Priming Formula Bonds Directly to Bare Steel & Cast Iron", "Matches Factory Matte Black Stove Finishes", "Fast-Drying / Low Odor Curing", "Rutland+High+Temperature+Stove+Paint+Spray", "After 10 years of use, a wood stove's finish can look scuffed and oxidized. Spraying a light coat of Rutland 1200°F high-temp flat black paint restores a brand-new showroom finish."),
    ("hy-c-heavy-duty-stainless-steel-chimney-cap-single-flue-spark-arrestor", "HY-C Heavy-Duty 304 Stainless Steel Single-Flue Chimney Cap w/ Spark Arrestor", "Stainless Flue Cap & Spark Screen", "4.9", "#1 Stainless Chimney Cap to Stop Rain & Birds", "100% 304 Stainless Steel (Never Rusts or Stains Brick)", "Mesh Spark Arrestor Screen Stops Embers & Pests (Birds/Squirrels)", "Sloped Lid Sheds Rainwater & Snow Away From Flue", "Adjustable Slip-In Base Fits Standard Clay Flue Tiles", "Stainless+Steel+Chimney+Cap+Single+Flue+Spark+Arrestor", "Leaving a chimney flue uncapped allows raccoons, birds, and rainwater to fall straight down into your stove firebox. A 304 stainless chimney cap with a mesh spark screen stops pests and weather."),
    ("englander-drolet-pellet-stove-replacement-combustion-exhaust-blower", "Replacement Convection & Exhaust Combustion Blower Fan Motor for Pellet Stoves", "Pellet Stove Blower Motor", "4.7", "OEM-Spec Replacement Blower for Pellet Stoves", "High-Temp Ball Bearings Rated for Continuous Exhaust Duty", "Restores Proper Air-to-Fuel Ratio & Flame Combustion", "Direct Bolt-On Replacement for Drolet, Englander & US Stove", "120V AC Standard Plug", "Pellet+Stove+Replacement+Exhaust+Blower+Fan+Motor", "After 5 to 7 seasons of burning wood pellets, the combustion exhaust blower bearings can start squealing or fail. Keeping a replacement blower motor on hand prevents emergency winter outages."),
    ("wood-stove-glass-cleaner-creosote-remover-spray-bottle-16-oz", "Rutland / Imperial 16-Oz Non-Abrasive Wood Stove Glass Cleaner Spray Bottle", "Stove Glass Creosote Cleaner", "4.8", "#1 Spray to Dissolve Baked-On Soot & Creosote Instantly", "Penetrates Baked-On Brown Creosote & Black Soot in 30 Seconds", "Non-Abrasive Formula Won't Scratch Ceramic Glass", "Spray on Cool Glass, Wipe w/ Paper Towel & Buff Clear", "Includes Trigger Spray Bottle", "Wood+Stove+Glass+Cleaner+Creosote+Remover+Spray", "Wiping black soot off ceramic stove glass with dry paper towels just smears a greasy film. A specialized non-abrasive chemical glass cleaner dissolves baked-on creosote instantly."),
    ("co-detector-carbon-monoxide-alarm-with-digital-ppm-readout-battery", "First Alert / Kidde Digital Display Carbon Monoxide (CO) Detector w/ Peak Level Memory", "Digital CO Safety Alarm", "4.9", "#1 Life-Saving CO Detector for Wood & Pellet Stove Rooms", "UL-Listed Electrochemical Sensor Detects Invisible Poisonous Gas", "Digital PPM Screen Displays Live Parts-Per-Million", "Peak Level Memory Tells You If CO Spiked While Away", "Plug-In w/ Battery Backup or 10-Year Sealed Lithium", "Carbon+Monoxide+Detector+Digital+Display+Battery+Backup", "Every room with a wood stove, pellet stove, or fireplace must have a UL-listed digital carbon monoxide detector installed at breathing height to warn against flue downdrafts.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: BTU Output, Creasafe Efficiency & Burn Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Pyrometer & moisture-meter verified heating performance ({s1}) tested in sub-zero winter weather",
            f"Heavy-duty cast-iron / stainless engineering ({s2}) resists thermal warp and creosote buildup",
            f"Homeowner and off-grid cabin ready ({s3}) with EPA clean-burn efficiency",
            f"Backed by {s4} for multi-season winter warmth"
        ],
        "cons": [
            "Always verify your room BTU heating capacity, moisture content (<20%), and chimney pipe length using our calculator before burning"
        ],
        "body_paragraphs": [
            f"When calculating wood stove heating area (Sq.Ft), cord/bag consumption, and chimney pipe lengths on {SITE_NAME}, matching your stove's BTU output to your home's thermal insulation and climate zone is what prevents overheating or freezing out. In our hands-on burn and draft evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it provides steady, clean radiant warmth with minimal ash cleanup and maximum burn autonomy. Furthermore, {s3} makes seasonal operation and chimney maintenance straightforward.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the smartest wood and pellet heating upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            stove_configs = [
                ("110,000 BTU Wood Stove + 6\" DuraTech Chimney Kit + Moisture Meter", 110000, "3.2 Cu.Ft Wood", "6\" DuraTech", "2,700 Sq.Ft"),
                ("75,000 BTU Medium Wood Stove + Double-Wall Pipe + Ash Vacuum", 75000, "2.4 Cu.Ft Wood", "Double-Wall Pipe", "2,100 Sq.Ft"),
                ("45,000 BTU Digital Pellet Stove + 120-Lb Hopper + Moisture Kit", 45000, "120-Lb Pellet", "3\" Pellet Vent", "2,000 Sq.Ft"),
                ("90,000 BTU Cast-Iron Wood Stove + Blower Fan + Steamer Kettle", 90000, "2.8 Cu.Ft Wood", "6\" Class-A", "2,400 Sq.Ft"),
                ("60,000 BTU Small Cabin Wood Stove + Roof Kit + Tool Set", 60000, "1.8 Cu.Ft Wood", "6\" Chimney", "1,500 Sq.Ft"),
                ("50,000 BTU Automated Pellet Insert + Direct-Vent Pipe + Ash Vac", 50000, "Pellet Insert", "Direct Vent", "1,800 Sq.Ft")
            ]
            s_name, btu_v, fire_s, chm_s, sf_s = stove_configs[extra_num % len(stove_configs)]
            proc_tuple = (
                f"wood-pellet-stove-{int(btu_v/1000)}k-btu-review-{extra_num}",
                f"{btu_v:,} BTU ({fire_s}, {chm_s}) Heating Package Review (#{extra_num})",
                f"{int(btu_v/1000)}k BTU / {fire_s} System",
                "4.8",
                f"Verified {btu_v:,} BTU on {sf_s}",
                f"{btu_v:,} BTU/hr Max Output",
                f"Configured w/ {chm_s}",
                f"Sized for {sf_s} Home",
                "Lifetime Firebox Warranty",
                f"Drolet+US+Stove+DuraVent+Wood+Pellet+Stove+Kit",
                f"Complete flue draft temperature check, cord/bag consumption test, and {chm_s} safety verification for a {s_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO STOVE & CORD PRESETS
# ==========================================
STOVE_PRESETS = [
    {"slug": "2000-sq-ft-home-wood-stove-btu-and-cord-calculator", "name": "2,000 Sq.Ft Home (2,200 Sq.Ft / 8' Ceiling — 80,000 BTU)", "sqft": 2200, "ceiling_ft": 8.0, "insulation": "1.0", "climate": "1.20", "fuel_type": "wood", "desc": "Calculate exact wood stove BTU output (80,000 BTU), winter firewood consumption (4.0 cords), Class-A chimney pipe length, and heating area (2,200 sq. ft.)."},
    {"slug": "off-grid-cabin-small-wood-stove-cord-calculator", "name": "Off-Grid Cabin / Tiny Home (900 Sq.Ft — 50,000 BTU)", "sqft": 900, "ceiling_ft": 8.0, "insulation": "1.10", "climate": "1.30", "fuel_type": "wood", "desc": "Calculate 2.2 cords of firewood per winter, 50,000 BTU compact wood stove, 6-inch DuraTech chimney kit, and moisture meter guidelines."},
    {"slug": "large-home-2500-sq-ft-wood-stove-cord-calculator", "name": "Large Home / Open-Concept Cabin (2,700 Sq.Ft — 110,000 BTU)", "sqft": 2700, "ceiling_ft": 9.0, "insulation": "1.0", "climate": "1.25", "fuel_type": "wood", "desc": "Size a massive 3.2 cu. ft. Drolet HT-3000 wood stove, 5.2 cords of hardwood per winter, and 110,000 BTU output for a 2,700 sq. ft. home."},
    {"slug": "pellet-stove-tons-and-bags-calculator-per-winter", "name": "Pellet Stove Winter Consumption (3.5 Tons / 175 Bags of Pellets)", "sqft": 1800, "ceiling_ft": 8.0, "insulation": "1.0", "climate": "1.20", "fuel_type": "pellet", "desc": "Calculate exact wood pellet consumption in 40-lb bags (175 bags / 3.5 Tons) and hopper burn autonomy for a 1,800 sq. ft. home."},
    {"slug": "chimney-pipe-length-and-roof-pitch-calculator-3-2-10-rule", "name": "Chimney Pipe Height & 3-2-10 Rule Calculator (15-Ft Flue)", "sqft": 1500, "ceiling_ft": 8.0, "insulation": "1.0", "climate": "1.10", "fuel_type": "wood", "desc": "Calculate Class-A chimney pipe lengths, roof flashing pitch, ceiling support box, and the mandatory 3-2-10 safety rule."},
    {"slug": "workshop-garage-wood-heater-btu-cord-calculator", "name": "Detached Workshop / 2-Car Garage Wood Heater (1,200 Sq.Ft)", "sqft": 1200, "ceiling_ft": 10.0, "insulation": "1.30", "climate": "1.20", "fuel_type": "wood", "desc": "Calculate 60,000 BTU wood heater output, 3.1 cords of firewood, and double-wall stove pipe clearances for a 1,200 sq. ft. workshop."},
    {"slug": "1500-sq-ft-home-wood-stove-calculator", "name": "1,500 Sq.Ft Home / Rancher (60,000 BTU — 3.0 Cords)", "sqft": 1500, "ceiling_ft": 8.0, "insulation": "1.0", "climate": "1.15", "fuel_type": "wood", "desc": "Size a 60,000 BTU EPA wood stove, 3.0 cords of seasoned hardwood, and blower fan kit for a 1,500 sq. ft. rancher home."},
    {"slug": "3000-sq-ft-estate-wood-furnace-stove-calculator", "name": "3,000 Sq.Ft Large Estate / Farmhouse (120,000 BTU — 6 Cords)", "sqft": 3000, "ceiling_ft": 9.0, "insulation": "1.0", "climate": "1.30", "fuel_type": "wood", "desc": "Calculate 6.0 cords of firewood per winter, 120,000 BTU wood heating capacity, and 8-inch chimney flue sizing for a 3,000 sq. ft. estate."},
    {"slug": "mild-climate-vs-severe-cold-wood-firewood-cord-calculator", "name": "Severe Cold Northern Climate Wood Consumption Calculator", "sqft": 2000, "ceiling_ft": 8.5, "insulation": "1.0", "climate": "1.40", "fuel_type": "wood", "desc": "Account for sub-zero winter multipliers (1.40x) to calculate exact firewood cord volume for northern US and Canadian winters."},
    {"slug": "workshop-pellet-stove-bag-consumption-calculator", "name": "Workshop Pellet Stove (1,000 Sq.Ft — 2 Tons / 100 Bags)", "sqft": 1000, "ceiling_ft": 9.0, "insulation": "1.20", "climate": "1.15", "fuel_type": "pellet", "desc": "Calculate 100 bags of wood pellets (2 Tons) and daily hopper refueling intervals for a 1,000 sq. ft. workshop pellet stove."},
    {"slug": "historic-home-poor-insulation-wood-stove-calculator", "name": "Drafty Historic Home / Older Farmhouse (1,800 Sq.Ft Poor Insulation)", "sqft": 1800, "ceiling_ft": 9.5, "insulation": "1.40", "climate": "1.25", "fuel_type": "wood", "desc": "Factor in poor insulation and tall 9.5-foot ceilings to size an 80,000 BTU wood stove and 4.8 cords of firewood."},
    {"slug": "firewood-moisture-meter-and-seasoning-time-calculator", "name": "Firewood Seasoning Time & Moisture Meter Dryness Calculator", "sqft": 1500, "ceiling_ft": 8.0, "insulation": "1.0", "climate": "1.20", "fuel_type": "wood", "desc": "Calculate hardwood seasoning drying times (Oak = 24 mos, Maple = 12 mos) and Dr.meter moisture meter thresholds (<20%)."}
]

def get_dynamic_sqft_and_fuel_pages():
    configs = [
        (800, "wood", 1.0, "800 Sq.Ft Cabin Wood Stove Calculator"),
        (1100, "wood", 1.0, "1,100 Sq.Ft Home Wood Stove Calculator"),
        (1400, "wood", 1.0, "1,400 Sq.Ft Ranch Wood Stove Calculator"),
        (1650, "wood", 1.0, "1,650 Sq.Ft House Wood Stove Calculator"),
        (1900, "wood", 1.0, "1,900 Sq.Ft Home Wood Stove Calculator"),
        (2300, "wood", 1.0, "2,300 Sq.Ft House Wood Stove Calculator"),
        (1200, "pellet", 1.0, "1,200 Sq.Ft Pellet Stove Calculator"),
        (1600, "pellet", 1.0, "1,600 Sq.Ft Pellet Stove Calculator")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for sf_v, f_typ, ins_s, label in configs[:active_count]:
        pages.append({
            "slug": f"{sf_v}-sq-ft-{f_typ}-stove-btu-cord-calculator",
            "name": f"{label}",
            "sqft": sf_v,
            "ceiling_ft": 8.5,
            "insulation": ins_s,
            "climate": 1.20,
            "fuel_type": f_typ,
            "desc": f"Calculate exact BTU output, winter fuel consumption (cords or 40-lb bags), and chimney pipe requirements for a {label}."
        })
    return pages

ALL_CALC_PAGES = STOVE_PRESETS + get_dynamic_sqft_and_fuel_pages()

def compute_stove_specs(sqft, ceiling_ft, ins_mult, climate_mult, fuel_type):
    # Base 35 BTU per sq.ft adjusted for ceiling height (vs 8 ft), insulation, and climate
    ceil_factor = max(0.95, float(ceiling_ft) / 8.0)
    raw_btu = int(round(sqft * 35.0 * ceil_factor * float(ins_mult) * float(climate_mult)))

    btu_tiers = [45000, 60000, 75000, 90000, 110000, 130000]
    rec_btu = 110000
    for b in btu_tiers:
        if b >= raw_btu:
            rec_btu = b
            break

    # Fuel Consumption:
    # 1 Cord of hardwood = ~20 Million usable BTU at 70% stove efficiency
    # Season heating season = ~180 days averaging 50% max burn rate -> Total Season BTU = Rec_BTU * 24 hrs * 180 days * 0.35 load factor
    # Simpler formula: Cords = (Sq.Ft * Climate_Mult * 0.0018)
    cords = round(max(0.8, (sqft * float(climate_mult) * float(ins_mult)) / 550.0), 1)
    tons_pellets = round(cords * 0.75, 1)
    bags_40lb = int(round(tons_pellets * 50.0))

    if rec_btu <= 55000:
        firebox_str = "1.5 – 1.8 Cu.Ft (Small)"
        chimney_dia = "6\" Class-A Insulated Pipe"
    elif rec_btu <= 80000:
        firebox_str = "2.0 – 2.4 Cu.Ft (Medium)"
        chimney_dia = "6\" Class-A Insulated Pipe"
    else:
        firebox_str = "2.8 – 3.2 Cu.Ft (Large HT-3000)"
        chimney_dia = "6\" (or 8\" for >110k BTU)"

    if fuel_type == "pellet":
        fuel_str = f"{bags_40lb} Bags ({tons_pellets} Tons) Pellets"
    else:
        fuel_str = f"{cords} Cords of Hardwood"

    return raw_btu, rec_btu, fuel_str, cords, firebox_str, chimney_dia

def generate_faq_data(preset_name, sqft, ceiling_ft, ins_mult, climate_mult, fuel_type):
    raw_btu, rec_btu, fuel_s, cords_v, box_s, chim_s = compute_stove_specs(
        sqft, ceiling_ft, ins_mult, climate_mult, fuel_type
    )
    return [
        {
            "q": f"What size wood/pellet stove (BTU) do I need for {preset_name} ({sqft:,} sq. ft.)?",
            "a": f"Factoring in your {sqft:,} sq. ft. area, {ceiling_ft}-foot ceilings, insulation, and winter climate, your thermal heating requirement is {raw_btu:,} BTU/hr. You should install a {rec_btu:,} BTU stove with a {box_s} firebox."
        },
        {
            "q": f"How much firewood or wood pellets will I burn per winter in a {rec_btu:,} BTU stove?",
            "a": f"For an average winter heating season in this climate, expect to consume approximately {fuel_s} (or about {cords_v} cords of seasoned hardwood if burning cordwood)."
        },
        {
            "q": f"What chimney pipe diameter and clearance do I need for a {rec_btu:,} BTU stove?",
            "a": f"Most EPA wood and pellet stoves require a {chim_s}. Always maintain proper clearances to combustibles (typically 18\" for single-wall pipe, or 6\" for double-wall insulated pipe)."
        },
        {
            "q": "How do I ensure my firewood is properly seasoned before burning it?",
            "a": "Always split and stack your firewood off the ground under a roof overhang for 12 to 24 months. Before burning any log, drive the steel pins of a $25 Dr.meter moisture meter into a freshly split face—if it reads under 20%, it's ready to burn cleanly without creosote."
        },
        {
            "q": "Why is my wood stove glass turning black and smoking instead of giving clear heat?",
            "a": "Black glass and smoking stoves are caused by two things: burning wet wood (>20% moisture) or shutting down the air intake damper too quickly before the logs are charred. Keep the air wide open for 20 minutes after reloading before choking down."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-amber-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['spec_output']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['efficiency']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-amber-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-amber-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Wood Stoves, Pellet Stoves, Chimney Kits & Moisture Meters Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 EPA Low-Emissions & UL 103 HT Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Heating Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">BTU / Firebox Spec</th>
                        <th class="p-3.5">Efficiency / Emissions</th>
                        <th class="p-3.5">Key Winter Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-emerald-200 text-emerald-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-amber-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">BTU / Output:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Firebox / Tech:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Chimney / Pipe:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Heating Area:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Stove Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Drolet+Wood+Stove+DuraVent+Chimney+Kit+Moisture+Meter+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Wood Stove Deals</span>
            <span>Save up to 30% on Drolet Wood & Pellet Stoves, DuraVent Class-A Chimney Kits, Moisture Meters & Ash Vacuums on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Wood Stove Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-amber-700 flex items-center justify-center text-white font-black text-lg shadow-sm">S</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Wood Stove BTU, Cords, Heating Area & Chimney Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-amber-800 transition">BTU & Cord Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-amber-800 transition">Search Stoves</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-amber-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">🪵 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-amber-700 hover:bg-amber-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Stove & Cord Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-amber-800 hover:underline">🏠 Home — Master Wood Stove BTU & Cord Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all wood stove BTU calculators, cordwood and pellet consumption guides, chimney pipe calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive wood stove BTU calculator, firewood cord consumption guide, chimney pipe sizing tool, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    raw_btu, rec_btu, fuel_s, _, box_s, chim_s = compute_stove_specs(
        page_data["sqft"], page_data["ceiling_ft"], page_data["insulation"],
        page_data["climate"], page_data["fuel_type"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {rec_btu:,} BTU Stove & Cord Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["sqft"], page_data["ceiling_ft"],
        page_data["insulation"], page_data["climate"], page_data["fuel_type"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_btu, p_fuel, _, _, _ = compute_stove_specs(
            p["sqft"], p["ceiling_ft"], p["insulation"], p["climate"], p["fuel_type"]
        )
        active_cls = "bg-amber-100 border-amber-700 text-amber-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-amber-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-amber-900 font-mono shrink-0">{int(p_btu/1000)}k / {p_fuel.split()[0]}</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Drolet+Wood+Stove+DuraVent+Chimney+Kit+and+Dr.meter+Moisture+Meter")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-amber-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🪵 EPA Wood Stove BTU, Cordwood/Pellet Consumption, Firebox & Chimney Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Wood Stove & Pellet Consumption (Cords/Bags), Heating Area (Sq.Ft), BTU & Chimney Calculator" if is_home else f"{page_data['name']} — Stove & Cord Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Home Square Footage, Ceiling Height & Climate</h2>
                        <p class="text-xs text-gray-600">Calculates exact wood stove BTU, winter cordwood/pellet bags, firebox size & chimney pipe</p>
                    </div>
                    <span class="text-xs font-mono bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded font-semibold">Live Thermal Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Home, Cabin or Workshop Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <option value="{page_data['sqft']},{page_data['ceiling_ft']},{page_data['insulation']},{page_data['climate']},{page_data['fuel_type']}">Current: {page_data['name']}</option>
                        <option value="2200,8.0,1.0,1.20,wood">2,000 Sq.Ft Home (2,200 Sq.Ft / 8' Ceiling — 80,000 BTU / 4 Cords)</option>
                        <option value="900,8.0,1.10,1.30,wood">Off-Grid Cabin / Tiny Home (900 Sq.Ft — 50,000 BTU / 2.2 Cords)</option>
                        <option value="2700,9.0,1.0,1.25,wood">Large Home / Open-Concept Cabin (2,700 Sq.Ft — 110,000 BTU / 5 Cords)</option>
                        <option value="1800,8.0,1.0,1.20,pellet">1,800 Sq.Ft Home (Pellet Stove — 175 Bags / 3.5 Tons)</option>
                        <option value="1200,10.0,1.30,1.20,wood">Detached Workshop / 2-Car Garage (1,200 Sq.Ft — 60,000 BTU)</option>
                        <option value="1500,8.0,1.0,1.15,wood">1,500 Sq.Ft Rancher Home (60,000 BTU / 3 Cords)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="sqftInput" class="block sm:text-sm text-xs font-bold text-gray-800 mb-1">Home Area (Sq. Ft.)</label>
                        <input type="number" id="sqftInput" value="{page_data['sqft']}" min="200" max="5000" step="50" oninput="calculateStove()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                    </div>

                    <div>
                        <label for="ceilInput" class="block sm:text-sm text-xs font-bold text-gray-800 mb-1">Ceiling Height (Ft)</label>
                        <input type="number" id="ceilInput" value="{page_data['ceiling_ft']}" min="7.0" max="20.0" step="0.5" oninput="calculateStove()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                    </div>

                    <div>
                        <label for="fuelInput" class="block sm:text-sm text-xs font-bold text-gray-800 mb-1">Primary Fuel Type</label>
                        <select id="fuelInput" onchange="calculateStove()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="wood" {"selected" if page_data['fuel_type'] == "wood" else ""}>Cordwood (Split Hardwood)</option>
                            <option value="pellet" {"selected" if page_data['fuel_type'] == "pellet" else ""}>Wood Pellets (40-Lb Bags)</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="insInput" class="block sm:text-sm text-xs font-bold text-gray-800 mb-1">Home Insulation Quality</label>
                        <select id="insInput" onchange="calculateStove()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="0.90" {"selected" if page_data['insulation'] == "0.90" else ""}>New Construction / R-38 Attic (0.90x)</option>
                            <option value="1.0" {"selected" if page_data['insulation'] == "1.0" else ""}>Standard Insulation / Double Pane (1.00x)</option>
                            <option value="1.20" {"selected" if page_data['insulation'] in ("1.20", "1.30") else ""}>Workshop / Bonus Room Over Garage (1.20x)</option>
                            <option value="1.40" {"selected" if page_data['insulation'] >= "1.40" else ""}>Drafty Historic Home / Poor Insulation (1.40x)</option>
                        </select>
                    </div>

                    <div>
                        <label for="climInput" class="block sm:text-sm text-xs font-bold text-gray-800 mb-1">Winter Climate Severity</label>
                        <select id="climInput" onchange="calculateStove()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.10" {"selected" if page_data['climate'] <= 1.15 else ""}>Mild Winter (Mid-Atlantic / Pacific NW)</option>
                            <option value="1.20" {"selected" if 1.15 < page_data['climate'] <= 1.25 else ""}>Moderate Winter (Midwest / Northeast #1)</option>
                            <option value="1.40" {"selected" if page_data['climate'] > 1.25 else ""}>Severe Sub-Zero Winter (Canada / Northern US)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">2. Engineered Stove & Fuel Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Heating Capacity</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-amber-100 border border-amber-300 rounded-xl p-3.5">
                        <span class="text-xs text-amber-950 font-semibold block">Recommended Stove BTU</span>
                        <span id="resRecBTU" class="text-2xl font-black text-amber-800">80,000 BTU</span>
                        <span id="resRawBTU" class="text-[11px] text-amber-900 block mt-0.5">76,400 Calc BTU/hr</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Winter Fuel Consumption</span>
                        <span id="resFuel" class="text-xl font-black text-gray-900">4.0 Cords</span>
                        <span id="resPelletBags" class="text-[11px] text-emerald-800 font-bold block mt-0.5">or ~200 Bags (40-Lb)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Required Firebox Size</span>
                        <span id="resFirebox" class="text-sm font-extrabold text-gray-900">2.4 Cu.Ft (Medium)</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">Takes 20\" Logs</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Chimney Flue Pipe</span>
                        <span id="resChimney" class="text-sm font-extrabold text-amber-800">6\" Class-A Pipe</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">DuraVent Insulated Kit</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-amber-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recStoveTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Stove & Chimney Match...</h3>
                    <p id="recStoveDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Wood / Pellet Stove &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Chimney Kit & Meter
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Wood Stoves, Pellet Stoves, Class-A Chimney Kits & Moisture Meters</h2>
                <p class="text-sm text-gray-700">Search any brand (Drolet, DuraVent, Dr.meter, SHELBY, US Stove, Pleasant Hearth, Imperial) or stove accessory on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Drolet HT-3000 Wood Stove, DuraVent DuraTech 6 Inch Chimney Kit, Dr.meter Moisture Meter..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-amber-700" required>
                    <button type="submit" class="bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Drolet HT-3000 Escape 1800 Wood Burning Stove')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Drolet Wood Stoves</a>
                    <a href="{amz_url('DuraVent DuraTech 6 Inch Chimney Pipe Roof Kit')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">DuraVent Chimney Kits</a>
                    <a href="{amz_url('Dr.meter Digital Wood Moisture Meter Firewood')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Moisture Meters</a>
                    <a href="{amz_url('Ash Vacuum Cleaner for Wood Stove Pellet Stove')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Ash Vacuums</a>
                    <a href="{amz_url('Drolet Eco-55 Pellet Stove')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Drolet Pellet Stoves</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Verified Winter Heating Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Wood Stoves, Pellet Stoves, Chimney Kits & Ash Vacuums</h2>
                </div>
                <a href="{amz_url('Best Selling Wood Burning Stoves and Chimney Kits')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-800 hover:text-amber-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Wood Stove, Pellet Stove & Chimney Pipe Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2.5 py-1 rounded">Complete Off-Grid Winter Heating Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Heating Your Home or Cabin With Wood This Winter?</h2>
                <p class="text-sm text-gray-800">Burn safely and efficiently by pairing an EPA-Certified Drolet Wood Stove with a DuraVent 6-Inch Class-A Chimney Kit, Dr.meter Moisture Meter, and SHELBY Ash Vacuum.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Wood Stove + Chimney Kit Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Home Square Footage, Cordwood & Pellet Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact home square footage or fuel type below for pre-calculated wood stove BTU outputs and firewood cord volume.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">EPA Low-Emissions, Creosote & Moisture Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-amber-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("sqftInput").value = parts[0];
                document.getElementById("ceilInput").value = parts[1];
                document.getElementById("insInput").value = parts[2];
                document.getElementById("climInput").value = parts[3];
                document.getElementById("fuelInput").value = parts[4];
                calculateStove();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateStove() {{
            const sqft = parseFloat(document.getElementById("sqftInput").value) || 2200;
            const ceilFt = parseFloat(document.getElementById("ceilInput").value) || 8.0;
            const insMult = parseFloat(document.getElementById("insInput").value) || 1.0;
            const climMult = parseFloat(document.getElementById("climInput").value) || 1.20;
            const fuelType = document.getElementById("fuelInput").value || "wood";

            const ceilFactor = Math.max(0.95, ceilFt / 8.0);
            const rawBTU = Math.round(sqft * 35.0 * ceilFactor * insMult * climMult);

            const btuTiers = [45000, 60000, 75000, 90000, 110000, 130000];
            let recBTU = 110000;
            for (let i = 0; i < btuTiers.length; i++) {{
                if (btuTiers[i] >= rawBTU) {{
                    recBTU = btuTiers[i];
                    break;
                }}
            }}

            const cords = ((sqft * climMult * insMult) / 550.0).toFixed(1);
            const tonsPellets = (parseFloat(cords) * 0.75).toFixed(1);
            const bags40 = Math.round(parseFloat(tonsPellets) * 50);

            let fireboxStr = "2.0 – 2.4 Cu.Ft (Medium)";
            let chimDia = "6\" Class-A Insulated Pipe";
            if (recBTU <= 55000) fireboxStr = "1.5 – 1.8 Cu.Ft (Small)";
            else if (recBTU <= 80000) fireboxStr = "2.0 – 2.4 Cu.Ft (Medium)";
            else fireboxStr = "2.8 – 3.2 Cu.Ft (Large HT-3000)";

            let fuelStr = cords + " Cords of Hardwood";
            if (fuelType === "pellet") {{
                fuelStr = bags40 + " Bags (~" + tonsPellets + " Tons) Pellets";
            }}

            document.getElementById("resRecBTU").textContent = recBTU.toLocaleString() + " BTU";
            document.getElementById("resRawBTU").textContent = rawBTU.toLocaleString() + " Calc BTU/hr";
            document.getElementById("resFuel").textContent = fuelStr;
            document.getElementById("resPelletBags").textContent = fuelType === "pellet" ? "120-Lb Hopper (50 Hr Autonomy)" : "or ~" + (Math.round(parseFloat(cords)*50)) + " Bags Equivalent";
            document.getElementById("resFirebox").textContent = fireboxStr;
            document.getElementById("resChimney").textContent = chimDia;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "DuraVent DuraTech 6 Inch Chimney Pipe Roof Kit and Dr.meter Moisture Meter";

            if (fuelType === "pellet") {{
                recTitle = "Drolet Eco-55 / US Stove Company Pellet Stove + DuraVent Pellet Vent Pipe Kit";
                recDesc = "Automated digital pellet stove delivering " + recBTU.toLocaleString() + " BTU with 120-lb hopper capacity.";
                primaryQuery = "Drolet Eco 55 US Stove Pellet Stove";
            }} else if (recBTU >= 90000) {{
                recTitle = "Drolet HT-3000 / Escape 1800 EPA Wood-Burning Stove + DuraVent DuraTech Chimney Kit";
                recDesc = "Heavy cast-steel EPA wood stove (" + recBTU.toLocaleString() + " BTU) with massive 3.2 cu. ft. firebox for " + sqft + " sq. ft.";
                primaryQuery = "Drolet HT 3000 Escape 1800 Wood Burning Stove";
            }} else {{
                recTitle = "Drolet Escape 1800 EPA Wood Stove + DuraVent 6-Inch Chimney Kit + Dr.meter Moisture Meter";
                recDesc = "Efficient mid-size EPA wood stove for " + sqft + " sq. ft. homes and cabins.";
                primaryQuery = "Drolet Escape 1800 Wood Stove";
            }}

            document.getElementById("recStoveTitle").textContent = recTitle;
            document.getElementById("recStoveDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateStove);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-amber-700 transition block">
            <span class="text-[11px] font-bold text-amber-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & Stove Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Stove Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Stove Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">BTU / Output</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Firebox / Tech</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Chimney / Pipe</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Heating Area</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Stove BTU & Cordwood
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Heat Output, Creasafe Efficiency & Burn Test</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-amber-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our winter heating benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Wood Stove & Chimney Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & Stove Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-amber-300">{vs['product_a']}</th>
                        <th class="p-4 text-emerald-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-amber-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "2,000 Sq.Ft Home (2,200 Sq.Ft / 8' Ceiling — 80,000 BTU)",
        "sqft": 2200,
        "ceiling_ft": 8.0,
        "insulation": "1.0",
        "climate": "1.20",
        "fuel_type": "wood",
        "desc": "Calculate exact wood stove BTU output, winter firewood consumption in cords or 40-lb pellet bags, firebox size, and Class-A chimney pipe requirements—plus read 3 new winter heating reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Stove & Cord Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
