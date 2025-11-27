"""
Metabolic & GI Condition Games

Includes: GLP-1/Obesity, Short Bowel Syndrome
"""

from jparty.condition_games import ConditionGame, register_game


GLP1_OBESITY_GAME = ConditionGame(
    condition_id="glp1_obesity",
    condition_name="GLP-1 Agonists & Obesity Management",
    therapeutic_area="Endocrinology/Metabolic",
    description="Comprehensive review of GLP-1 receptor agonists and obesity pharmacotherapy",
    categories=[
        "Obesity Pathophysiology",
        "Diagnosis & Assessment",
        "GLP-1 Pharmacology",
        "Clinical Efficacy",
        "Safety & Monitoring",
        "Emerging Therapies"
    ],
    questions=[
        # Obesity Pathophysiology
        {"category": "Obesity Pathophysiology", "question": "This BMI threshold defines obesity in adults", "answer": "What is BMI ≥30 kg/m²?", "rationale": "Class I: 30-34.9, Class II: 35-39.9, Class III: ≥40", "difficulty": "basic"},
        {"category": "Obesity Pathophysiology", "question": "This hormone secreted by adipose tissue regulates appetite and metabolism", "answer": "What is leptin?", "rationale": "Leptin signals energy sufficiency; obesity causes leptin resistance", "difficulty": "intermediate"},
        {"category": "Obesity Pathophysiology", "question": "This hunger hormone is produced by the stomach", "answer": "What is ghrelin?", "rationale": "Ghrelin increases appetite; levels rise before meals", "difficulty": "intermediate"},
        {"category": "Obesity Pathophysiology", "question": "This set point theory explains why weight loss is difficult to maintain", "answer": "What is metabolic adaptation (adaptive thermogenesis)?", "rationale": "Body defends against weight loss by reducing energy expenditure", "difficulty": "intermediate"},
        {"category": "Obesity Pathophysiology", "question": "This hypothalamic nucleus integrates appetite signals", "answer": "What is the arcuate nucleus?", "rationale": "Arcuate nucleus contains POMC and AgRP neurons regulating feeding", "difficulty": "advanced"},

        # Diagnosis & Assessment
        {"category": "Diagnosis & Assessment", "question": "This waist circumference indicates increased cardiometabolic risk in men", "answer": "What is >40 inches (102 cm)?", "rationale": "Central adiposity correlates with metabolic complications; >35 in women", "difficulty": "basic"},
        {"category": "Diagnosis & Assessment", "question": "This staging system classifies obesity by complications (Stage 0-4)", "answer": "What is the Edmonton Obesity Staging System?", "rationale": "EOSS considers comorbidities and functional status, not just BMI", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "These 5 components define metabolic syndrome", "answer": "What are waist circumference, triglycerides, HDL, BP, fasting glucose?", "rationale": "3 of 5 criteria diagnose metabolic syndrome (ATP III)", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This sleep disorder is strongly associated with obesity", "answer": "What is obstructive sleep apnea?", "rationale": "OSA screening recommended in obesity; improves with weight loss", "difficulty": "basic"},
        {"category": "Diagnosis & Assessment", "question": "This liver condition is the most common cause of elevated LFTs in obesity", "answer": "What is NAFLD/MASLD (metabolic-associated steatotic liver disease)?", "rationale": "Up to 80% of obese patients have hepatic steatosis", "difficulty": "intermediate"},

        # GLP-1 Pharmacology
        {"category": "GLP-1 Pharmacology", "question": "This enzyme degrades endogenous GLP-1 within minutes", "answer": "What is DPP-4 (dipeptidyl peptidase-4)?", "rationale": "GLP-1 RAs are resistant to DPP-4 degradation", "difficulty": "intermediate"},
        {"category": "GLP-1 Pharmacology", "question": "This once-weekly GLP-1 agonist is approved for both diabetes and obesity", "answer": "What is semaglutide (Wegovy for obesity, Ozempic for diabetes)?", "rationale": "Semaglutide achieves ~15% weight loss at obesity doses", "difficulty": "basic"},
        {"category": "GLP-1 Pharmacology", "question": "This GLP-1 mechanism delays gastric emptying contributing to weight loss", "answer": "What is gastric motility reduction?", "rationale": "Delayed gastric emptying promotes satiety; may cause GI side effects", "difficulty": "intermediate"},
        {"category": "GLP-1 Pharmacology", "question": "This GLP-1 effect on the brain reduces appetite", "answer": "What is hypothalamic satiety signaling?", "rationale": "GLP-1 RAs cross BBB and activate satiety centers", "difficulty": "intermediate"},
        {"category": "GLP-1 Pharmacology", "question": "This daily injectable GLP-1 agonist was first approved for obesity", "answer": "What is liraglutide (Saxenda)?", "rationale": "Liraglutide 3.0 mg approved for obesity in 2014", "difficulty": "intermediate"},

        # Clinical Efficacy
        {"category": "Clinical Efficacy", "question": "This percentage of body weight loss is considered clinically meaningful", "answer": "What is ≥5% weight loss?", "rationale": "5% loss improves metabolic parameters; >10% has greater benefits", "difficulty": "basic"},
        {"category": "Clinical Efficacy", "question": "This trial demonstrated semaglutide 2.4 mg efficacy for obesity (STEP program)", "answer": "What is STEP 1?", "rationale": "STEP 1 showed 14.9% weight loss vs 2.4% with placebo at 68 weeks", "difficulty": "intermediate"},
        {"category": "Clinical Efficacy", "question": "This percentage of patients achieved ≥20% weight loss with tirzepatide", "answer": "What is ~36% (at highest dose)?", "rationale": "SURMOUNT-1 showed unprecedented weight loss with tirzepatide", "difficulty": "advanced"},
        {"category": "Clinical Efficacy", "question": "This cardiovascular outcome was reduced with semaglutide in SELECT trial", "answer": "What is MACE (major adverse cardiovascular events)?", "rationale": "SELECT showed 20% reduction in MACE in obese non-diabetic patients", "difficulty": "advanced"},
        {"category": "Clinical Efficacy", "question": "This happens to weight after stopping GLP-1 agonists", "answer": "What is weight regain?", "rationale": "Weight regain occurs without ongoing therapy; chronic treatment needed", "difficulty": "basic"},

        # Safety & Monitoring
        {"category": "Safety & Monitoring", "question": "This is the most common side effect of GLP-1 agonists", "answer": "What is nausea (or GI side effects)?", "rationale": "Nausea, vomiting, diarrhea common; usually improve with time", "difficulty": "basic"},
        {"category": "Safety & Monitoring", "question": "This serious adverse event led to warnings about GLP-1 use in MTC history", "answer": "What is medullary thyroid carcinoma (MTC)?", "rationale": "Boxed warning for personal/family history of MTC or MEN2", "difficulty": "intermediate"},
        {"category": "Safety & Monitoring", "question": "This dose escalation strategy minimizes GI side effects", "answer": "What is slow dose titration?", "rationale": "Starting low and increasing gradually reduces GI intolerance", "difficulty": "basic"},
        {"category": "Safety & Monitoring", "question": "This gallbladder complication is increased with rapid weight loss", "answer": "What is cholelithiasis (gallstones)?", "rationale": "Gallstones occur with rapid weight loss from any intervention", "difficulty": "intermediate"},
        {"category": "Safety & Monitoring", "question": "This pancreatitis concern requires monitoring and counseling", "answer": "What is acute pancreatitis?", "rationale": "Discontinue GLP-1 RA if pancreatitis suspected; avoid in history of pancreatitis", "difficulty": "intermediate"},

        # Emerging Therapies
        {"category": "Emerging Therapies", "question": "This dual GIP/GLP-1 agonist achieves >20% weight loss", "answer": "What is tirzepatide (Zepbound)?", "rationale": "Tirzepatide is dual incretin agonist with superior weight loss", "difficulty": "basic"},
        {"category": "Emerging Therapies", "question": "This investigational triple agonist targets GLP-1, GIP, and glucagon receptors", "answer": "What is retatrutide?", "rationale": "Triple agonism showed up to 24% weight loss in phase 2", "difficulty": "advanced"},
        {"category": "Emerging Therapies", "question": "This oral GLP-1 agonist eliminates need for injections", "answer": "What is oral semaglutide (Rybelsus)?", "rationale": "Oral semaglutide available for diabetes; higher doses studied for obesity", "difficulty": "intermediate"},
        {"category": "Emerging Therapies", "question": "This small molecule GLP-1 agonist is taken once daily orally", "answer": "What is orforglipron?", "rationale": "Orforglipron is non-peptide oral GLP-1 RA in late-stage development", "difficulty": "advanced"},
        {"category": "Emerging Therapies", "question": "This combination approach adds amylin analog to GLP-1 for enhanced weight loss", "answer": "What is cagrilintide + semaglutide (CagriSema)?", "rationale": "Amylin + GLP-1 combination shows additive weight loss benefit", "difficulty": "expert"},
    ],
    final_jeopardy={
        "category": "Obesity Treatment Milestones",
        "question": "This 2021 FDA approval of semaglutide 2.4 mg (Wegovy) represented a breakthrough achieving this mean percentage weight loss",
        "answer": "What is approximately 15% body weight loss?",
        "rationale": "Wegovy achieved unprecedented efficacy, transforming obesity treatment"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Understand the pathophysiology of obesity and metabolic regulation",
        "Apply GLP-1 receptor agonist pharmacology to patient selection",
        "Manage GLP-1 agonist side effects and safety concerns",
        "Review emerging obesity therapies including dual and triple agonists"
    ]
)
register_game(GLP1_OBESITY_GAME)


SHORT_BOWEL_SYNDROME_GAME = ConditionGame(
    condition_id="short_bowel_syndrome",
    condition_name="Short Bowel Syndrome",
    therapeutic_area="Gastroenterology",
    description="Comprehensive review of short bowel syndrome management and intestinal rehabilitation",
    categories=[
        "Pathophysiology",
        "Classification & Etiology",
        "Nutritional Management",
        "Pharmacotherapy",
        "Parenteral Nutrition",
        "Surgical Options"
    ],
    questions=[
        # Pathophysiology
        {"category": "Pathophysiology", "question": "This minimum small bowel length is typically required for nutritional autonomy", "answer": "What is approximately 200 cm (with intact colon)?", "rationale": "Less bowel may require permanent PN; colon presence critical", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This bowel adaptation process increases absorptive capacity over time", "answer": "What is intestinal adaptation?", "rationale": "Villi hypertrophy, crypt deepening, and bowel dilation occur over 1-2 years", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This hormone stimulates intestinal adaptation and is now therapeutic", "answer": "What is GLP-2?", "rationale": "GLP-2 promotes mucosal growth and absorption", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This complication occurs from bile salt malabsorption in ileal resection", "answer": "What is bile salt diarrhea (choleretic diarrhea)?", "rationale": "Bile salts in colon cause secretory diarrhea; cholestyramine may help", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This electrolyte is primarily absorbed in the jejunum and is often deficient in SBS", "answer": "What is magnesium?", "rationale": "Hypomagnesemia common in SBS; may require IV supplementation", "difficulty": "intermediate"},

        # Classification & Etiology
        {"category": "Classification & Etiology", "question": "This is the most common cause of SBS in adults", "answer": "What is mesenteric ischemia (or Crohn's disease)?", "rationale": "Vascular events and Crohn's requiring resection are leading causes", "difficulty": "basic"},
        {"category": "Classification & Etiology", "question": "This congenital condition is a leading cause of pediatric SBS", "answer": "What is necrotizing enterocolitis (or gastroschisis)?", "rationale": "NEC in premature infants is most common pediatric SBS cause", "difficulty": "intermediate"},
        {"category": "Classification & Etiology", "question": "This SBS anatomy type has jejunum connected to colon", "answer": "What is jejuno-colonic anastomosis (Type II)?", "rationale": "End-jejunostomy (Type I) vs jejuno-colonic (Type II) vs jejuno-ileal-colonic (Type III)", "difficulty": "advanced"},
        {"category": "Classification & Etiology", "question": "This valve's presence improves prognosis in SBS", "answer": "What is the ileocecal valve?", "rationale": "ICV slows transit and prevents bacterial reflux", "difficulty": "basic"},
        {"category": "Classification & Etiology", "question": "Patients with this anastomosis type have highest fluid losses", "answer": "What is end-jejunostomy (high output stoma)?", "rationale": "No colon = no colonic fluid absorption = high output", "difficulty": "intermediate"},

        # Nutritional Management
        {"category": "Nutritional Management", "question": "This oral rehydration solution principle matches sodium and glucose for absorption", "answer": "What is the sodium-glucose cotransporter?", "rationale": "ORS with sodium 90-120 mEq/L optimizes jejunal absorption", "difficulty": "intermediate"},
        {"category": "Nutritional Management", "question": "This dietary modification reduces output in patients with colon", "answer": "What is a high-complex carbohydrate, low-fat diet?", "rationale": "Complex carbs fermented by colon to SCFAs; fat malabsorption worsens steatorrhea", "difficulty": "intermediate"},
        {"category": "Nutritional Management", "question": "This type of fat is better absorbed in SBS", "answer": "What are medium-chain triglycerides (MCTs)?", "rationale": "MCTs absorbed directly without bile salts", "difficulty": "intermediate"},
        {"category": "Nutritional Management", "question": "This eating pattern optimizes absorption in SBS", "answer": "What is small, frequent meals (hyperphagia)?", "rationale": "Eating 1.5-2x normal intake in small meals maximizes absorption", "difficulty": "basic"},
        {"category": "Nutritional Management", "question": "This should be separated from meals to reduce osmotic output", "answer": "What is fluid intake (drink between meals)?", "rationale": "Separating solids and liquids reduces osmotic dumping", "difficulty": "intermediate"},

        # Pharmacotherapy
        {"category": "Pharmacotherapy", "question": "This GLP-2 analog is approved for SBS to reduce parenteral nutrition dependence", "answer": "What is teduglutide (Gattex)?", "rationale": "Teduglutide promotes intestinal adaptation and reduces PN requirements", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This antidiarrheal agent slows intestinal transit", "answer": "What is loperamide (or diphenoxylate)?", "rationale": "Opioid agonists reduce motility and output", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This PPI reduces gastric hypersecretion in early SBS", "answer": "What is a proton pump inhibitor (omeprazole)?", "rationale": "Gastric hypersecretion occurs early post-resection; may wean over time", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This medication binds bile salts to reduce choleretic diarrhea", "answer": "What is cholestyramine?", "rationale": "Bile salt binders help if <100cm ileum resected; worsen steatorrhea if more", "difficulty": "intermediate"},
        {"category": "Pharmacotherapy", "question": "This somatostatin analog may reduce output but has mixed evidence", "answer": "What is octreotide?", "rationale": "Octreotide reduces GI secretions but may impair adaptation; limited role", "difficulty": "advanced"},

        # Parenteral Nutrition
        {"category": "Parenteral Nutrition", "question": "This is the most common serious complication of long-term PN", "answer": "What is catheter-related bloodstream infection (CRBSI)?", "rationale": "Strict aseptic technique essential; ethanol locks may prevent", "difficulty": "basic"},
        {"category": "Parenteral Nutrition", "question": "This liver complication is associated with long-term PN", "answer": "What is intestinal failure-associated liver disease (IFALD)?", "rationale": "IFALD spectrum from steatosis to cirrhosis; limit soy lipids", "difficulty": "intermediate"},
        {"category": "Parenteral Nutrition", "question": "This IV lipid formulation may reduce IFALD risk compared to soy-based", "answer": "What is fish oil-based lipid (Omegaven) or SMOF lipid?", "rationale": "Omega-3 fatty acids less hepatotoxic than omega-6", "difficulty": "intermediate"},
        {"category": "Parenteral Nutrition", "question": "This metabolic complication occurs with aggressive refeeding", "answer": "What is refeeding syndrome (hypophosphatemia)?", "rationale": "Monitor phosphorus, potassium, magnesium when starting nutrition", "difficulty": "intermediate"},
        {"category": "Parenteral Nutrition", "question": "This PN cycling strategy allows daytime freedom", "answer": "What is nocturnal/cyclic PN?", "rationale": "12-14 hour nocturnal infusion standard for stable home PN", "difficulty": "basic"},

        # Surgical Options
        {"category": "Surgical Options", "question": "This procedure lengthens bowel by creating two parallel channels", "answer": "What is STEP (Serial Transverse Enteroplasty)?", "rationale": "STEP increases absorptive length in dilated bowel", "difficulty": "advanced"},
        {"category": "Surgical Options", "question": "This procedure narrows dilated bowel to improve motility", "answer": "What is tapering enteroplasty?", "rationale": "Tapering reduces stasis and bacterial overgrowth", "difficulty": "advanced"},
        {"category": "Surgical Options", "question": "This definitive treatment for intestinal failure is intestinal transplant", "answer": "What is small bowel transplant (or multivisceral transplant)?", "rationale": "Transplant reserved for PN complications or access failure", "difficulty": "intermediate"},
        {"category": "Surgical Options", "question": "This indication necessitates urgent intestinal transplant evaluation", "answer": "What is impending liver failure (IFALD)?", "rationale": "Combined liver-intestine transplant for IFALD with cirrhosis", "difficulty": "advanced"},
        {"category": "Surgical Options", "question": "This surgical reconstruction reverses a diverting ostomy", "answer": "What is restoration of intestinal continuity?", "rationale": "Anastomosis to colon greatly improves absorption in SBS", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "SBS Treatment Advances",
        "question": "This 2012 FDA approval of a GLP-2 analog marked the first drug therapy specifically for short bowel syndrome",
        "answer": "What is teduglutide (Gattex)?",
        "rationale": "Teduglutide promotes intestinal adaptation and reduces PN dependence"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Understand short bowel syndrome pathophysiology and adaptation",
        "Implement nutritional and pharmacologic management strategies",
        "Recognize and manage parenteral nutrition complications",
        "Identify candidates for intestinal rehabilitation and transplantation"
    ]
)
register_game(SHORT_BOWEL_SYNDROME_GAME)
