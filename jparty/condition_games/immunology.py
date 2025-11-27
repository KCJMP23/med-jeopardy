"""
Immunology & Inflammatory Disease Games

Includes: HIV, Atopic Dermatitis, EoE, Nasal Polyps, IMID
"""

from jparty.condition_games import ConditionGame, register_game


HIV_GAME = ConditionGame(
    condition_id="hiv",
    condition_name="HIV/AIDS",
    therapeutic_area="Infectious Disease",
    description="Comprehensive review of HIV pathophysiology, prevention, and antiretroviral therapy",
    categories=[
        "HIV Biology",
        "Diagnosis & Monitoring",
        "Antiretroviral Therapy",
        "Opportunistic Infections",
        "Prevention (PrEP/PEP)",
        "Special Populations"
    ],
    questions=[
        # HIV Biology
        {"category": "HIV Biology", "question": "This cell surface receptor is the primary target for HIV entry", "answer": "What is CD4?", "rationale": "HIV binds CD4 on T-helper cells, macrophages, and dendritic cells", "difficulty": "basic"},
        {"category": "HIV Biology", "question": "These co-receptors (CCR5 or CXCR4) determine HIV tropism", "answer": "What are chemokine co-receptors?", "rationale": "R5-tropic (CCR5) vs X4-tropic (CXCR4) affects drug selection (maraviroc)", "difficulty": "intermediate"},
        {"category": "HIV Biology", "question": "This viral enzyme converts RNA to DNA and is targeted by NRTIs and NNRTIs", "answer": "What is reverse transcriptase?", "rationale": "RT inhibitors are backbone of most ART regimens", "difficulty": "basic"},
        {"category": "HIV Biology", "question": "This viral enzyme cleaves polyproteins and is targeted by protease inhibitors", "answer": "What is HIV protease?", "rationale": "PIs block viral maturation; boosted with ritonavir or cobicistat", "difficulty": "intermediate"},
        {"category": "HIV Biology", "question": "This viral enzyme inserts HIV DNA into the host genome", "answer": "What is integrase?", "rationale": "INSTIs (integrase strand transfer inhibitors) are now preferred first-line", "difficulty": "intermediate"},

        # Diagnosis & Monitoring
        {"category": "Diagnosis & Monitoring", "question": "This combination test detects both HIV antibody and p24 antigen", "answer": "What is 4th generation HIV test?", "rationale": "4th gen testing shortens window period to ~2-3 weeks", "difficulty": "basic"},
        {"category": "Diagnosis & Monitoring", "question": "This CD4 count threshold defines AIDS", "answer": "What is <200 cells/μL?", "rationale": "AIDS defined by CD4 <200 or presence of AIDS-defining illness", "difficulty": "basic"},
        {"category": "Diagnosis & Monitoring", "question": "This viral load goal indicates successful ART", "answer": "What is undetectable (<50 copies/mL)?", "rationale": "Undetectable = Untransmittable (U=U) is key public health message", "difficulty": "basic"},
        {"category": "Diagnosis & Monitoring", "question": "This test should be performed before starting abacavir", "answer": "What is HLA-B*5701 testing?", "rationale": "HLA-B*5701 positive patients at high risk for abacavir hypersensitivity", "difficulty": "intermediate"},
        {"category": "Diagnosis & Monitoring", "question": "This test identifies mutations conferring drug resistance", "answer": "What is genotype resistance testing?", "rationale": "Genotype testing guides ART selection at diagnosis and virologic failure", "difficulty": "intermediate"},

        # Antiretroviral Therapy
        {"category": "Antiretroviral Therapy", "question": "This INSTI-based single-tablet regimen contains bictegravir/TAF/emtricitabine", "answer": "What is Biktarvy?", "rationale": "Biktarvy is a preferred initial regimen with high barrier to resistance", "difficulty": "basic"},
        {"category": "Antiretroviral Therapy", "question": "This class of ART drugs requires boosting with ritonavir or cobicistat", "answer": "What are protease inhibitors?", "rationale": "Boosted PIs (darunavir/r) are alternatives for certain patients", "difficulty": "intermediate"},
        {"category": "Antiretroviral Therapy", "question": "This two-drug regimen combines dolutegravir with lamivudine", "answer": "What is Dovato?", "rationale": "2-drug regimens reduce pill burden and long-term toxicity", "difficulty": "intermediate"},
        {"category": "Antiretroviral Therapy", "question": "This long-acting injectable regimen is given monthly or every 2 months", "answer": "What is cabotegravir + rilpivirine (Cabenuva)?", "rationale": "First complete long-acting ART regimen", "difficulty": "advanced"},
        {"category": "Antiretroviral Therapy", "question": "This NRTI should be avoided in patients with renal impairment (CrCl <30)", "answer": "What is tenofovir disoproxil fumarate (TDF)?", "rationale": "TAF (tenofovir alafenamide) preferred in renal disease", "difficulty": "intermediate"},

        # Opportunistic Infections
        {"category": "Opportunistic Infections", "question": "This opportunistic infection presents with white plaques in the oropharynx", "answer": "What is oral candidiasis (thrush)?", "rationale": "Common in patients with CD4 <200-500", "difficulty": "basic"},
        {"category": "Opportunistic Infections", "question": "This prophylaxis is indicated when CD4 <200 cells/μL", "answer": "What is PCP prophylaxis (TMP-SMX)?", "rationale": "TMP-SMX also covers toxoplasmosis prophylaxis at CD4 <100", "difficulty": "basic"},
        {"category": "Opportunistic Infections", "question": "This AIDS-defining malignancy is associated with HHV-8", "answer": "What is Kaposi sarcoma?", "rationale": "KS presents with violaceous skin lesions; treatment is ART + chemotherapy", "difficulty": "intermediate"},
        {"category": "Opportunistic Infections", "question": "This CD4 threshold indicates need for MAC prophylaxis", "answer": "What is CD4 <50 cells/μL?", "rationale": "Azithromycin weekly prevents disseminated MAC", "difficulty": "intermediate"},
        {"category": "Opportunistic Infections", "question": "This syndrome occurs when immune reconstitution unmasks latent infection", "answer": "What is IRIS (Immune Reconstitution Inflammatory Syndrome)?", "rationale": "IRIS can occur weeks after starting ART; manage with steroids if severe", "difficulty": "advanced"},

        # Prevention
        {"category": "Prevention (PrEP/PEP)", "question": "This medication is the most common oral PrEP regimen", "answer": "What is TDF/FTC (Truvada) or TAF/FTC (Descovy)?", "rationale": "Daily oral PrEP reduces HIV acquisition by >99%", "difficulty": "basic"},
        {"category": "Prevention (PrEP/PEP)", "question": "This timeframe is ideal for starting PEP after exposure", "answer": "What is within 72 hours?", "rationale": "PEP should be started ASAP; efficacy decreases after 72 hours", "difficulty": "basic"},
        {"category": "Prevention (PrEP/PEP)", "question": "This long-acting injectable PrEP is given every 2 months", "answer": "What is cabotegravir (Apretude)?", "rationale": "Injectable PrEP shown superior to oral in clinical trials", "difficulty": "intermediate"},
        {"category": "Prevention (PrEP/PEP)", "question": "This PrEP dosing strategy uses medication around time of sex", "answer": "What is on-demand (2-1-1) PrEP?", "rationale": "Approved in some countries for MSM with infrequent exposure", "difficulty": "advanced"},
        {"category": "Prevention (PrEP/PEP)", "question": "This monitoring is required every 3 months while on PrEP", "answer": "What is HIV testing and STI screening?", "rationale": "Regular HIV testing ensures PrEP not continued if infection occurs", "difficulty": "intermediate"},

        # Special Populations
        {"category": "Special Populations", "question": "This ART regimen is preferred in pregnancy", "answer": "What is dolutegravir-based ART?", "rationale": "DTG now recommended throughout pregnancy (updated guidance)", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This transmission risk exists with detectable viral load during delivery", "answer": "What is mother-to-child transmission (MTCT)?", "rationale": "ART + viral suppression reduces MTCT to <1%", "difficulty": "basic"},
        {"category": "Special Populations", "question": "This hepatitis co-infection requires HBV-active ART backbone", "answer": "What is Hepatitis B co-infection?", "rationale": "TDF or TAF + FTC/3TC treats both HIV and HBV", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This consideration is important for patients with cardiovascular risk", "answer": "What is avoiding certain PIs (due to metabolic effects)?", "rationale": "Some ART regimens affect lipids and cardiovascular risk", "difficulty": "advanced"},
        {"category": "Special Populations", "question": "This aging-related issue is accelerated in people with HIV", "answer": "What are non-AIDS comorbidities (cardiovascular, renal, bone)?", "rationale": "People with HIV experience accelerated aging and comorbidities", "difficulty": "advanced"},
    ],
    final_jeopardy={
        "category": "HIV Milestones",
        "question": "This 1996 breakthrough of combining multiple antiretrovirals transformed HIV from fatal to chronic disease, known as HAART",
        "answer": "What is Highly Active Antiretroviral Therapy?",
        "rationale": "Introduction of protease inhibitors and triple therapy dramatically reduced AIDS mortality"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Review HIV transmission, pathophysiology, and natural history",
        "Select appropriate antiretroviral therapy regimens",
        "Implement OI prophylaxis based on CD4 count",
        "Apply PrEP and PEP guidelines for HIV prevention"
    ]
)
register_game(HIV_GAME)


ATOPIC_DERMATITIS_GAME = ConditionGame(
    condition_id="atopic_dermatitis",
    condition_name="Atopic Dermatitis",
    therapeutic_area="Dermatology/Immunology",
    description="Comprehensive review of atopic dermatitis pathophysiology and management",
    categories=[
        "Pathophysiology",
        "Diagnosis & Assessment",
        "Topical Therapies",
        "Systemic Therapies",
        "Biologics & JAK Inhibitors",
        "Special Considerations"
    ],
    questions=[
        {"category": "Pathophysiology", "question": "This structural protein deficiency leads to impaired skin barrier in AD", "answer": "What is filaggrin?", "rationale": "Filaggrin mutations are the strongest genetic risk factor for AD", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This cytokine is central to the Th2 inflammatory response in AD", "answer": "What is IL-4 (or IL-13)?", "rationale": "IL-4 and IL-13 drive IgE production and skin inflammation", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This bacterium commonly colonizes AD skin and triggers flares", "answer": "What is Staphylococcus aureus?", "rationale": "S. aureus colonization occurs in >90% of AD patients", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This term describes the progression from AD to allergic rhinitis to asthma", "answer": "What is the atopic march?", "rationale": "AD often precedes development of other atopic conditions", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This IL-31 mediated symptom is often the most bothersome in AD", "answer": "What is pruritus (itch)?", "rationale": "IL-31 is a key pruritogenic cytokine targeted by nemolizumab", "difficulty": "intermediate"},

        {"category": "Diagnosis & Assessment", "question": "This scoring system assesses AD severity including extent and intensity", "answer": "What is EASI (Eczema Area and Severity Index)?", "rationale": "EASI is standard outcome measure in clinical trials", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This criterion requires pruritus for AD diagnosis", "answer": "What is the Hanifin & Rajka criteria?", "rationale": "Pruritus is essential; plus 3 of 4 major and 3+ minor criteria", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This patient-reported outcome measures itch severity", "answer": "What is Peak Pruritus NRS (Numerical Rating Scale)?", "rationale": "Itch NRS 0-10 is key PRO in AD trials", "difficulty": "basic"},
        {"category": "Diagnosis & Assessment", "question": "This percentage BSA threshold often defines moderate-to-severe AD", "answer": "What is >10% BSA (or EASI >7)?", "rationale": "Moderate-to-severe AD may require systemic therapy", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This complication presents with punched-out erosions and fever in AD", "answer": "What is eczema herpeticum?", "rationale": "HSV superinfection requires urgent antiviral therapy", "difficulty": "advanced"},

        {"category": "Topical Therapies", "question": "This topical anti-inflammatory class is first-line for AD flares", "answer": "What are topical corticosteroids?", "rationale": "TCS are mainstay of AD treatment; potency matched to location/severity", "difficulty": "basic"},
        {"category": "Topical Therapies", "question": "This calcineurin inhibitor is used for sensitive areas like face", "answer": "What is tacrolimus (or pimecrolimus)?", "rationale": "TCIs are steroid-sparing options without atrophy risk", "difficulty": "basic"},
        {"category": "Topical Therapies", "question": "This PDE4 inhibitor is a non-steroidal topical option for AD", "answer": "What is crisaborole (Eucrisa)?", "rationale": "Crisaborole approved for mild-to-moderate AD in patients ≥3 months", "difficulty": "intermediate"},
        {"category": "Topical Therapies", "question": "This topical JAK inhibitor was recently approved for AD", "answer": "What is ruxolitinib cream (Opzelura)?", "rationale": "First topical JAK inhibitor for AD; approved for short-term use", "difficulty": "intermediate"},
        {"category": "Topical Therapies", "question": "This application strategy uses TCS intermittently to prevent flares", "answer": "What is proactive (maintenance) therapy?", "rationale": "Twice-weekly TCS to previously affected areas reduces flares", "difficulty": "advanced"},

        {"category": "Systemic Therapies", "question": "This oral immunosuppressant is commonly used off-label for severe AD", "answer": "What is cyclosporine?", "rationale": "Cyclosporine provides rapid control; limited by nephrotoxicity", "difficulty": "intermediate"},
        {"category": "Systemic Therapies", "question": "This antimetabolite is used for long-term AD control", "answer": "What is methotrexate (or azathioprine, mycophenolate)?", "rationale": "Traditional immunosuppressants used before biologics/JAKi", "difficulty": "intermediate"},
        {"category": "Systemic Therapies", "question": "This monitoring is required for patients on systemic immunosuppression", "answer": "What is CBC, LFTs, renal function monitoring?", "rationale": "Regular labs needed to monitor for toxicity", "difficulty": "basic"},
        {"category": "Systemic Therapies", "question": "This treatment modality uses UV light for AD", "answer": "What is phototherapy (narrowband UVB)?", "rationale": "NB-UVB is effective for widespread AD; requires regular visits", "difficulty": "intermediate"},
        {"category": "Systemic Therapies", "question": "This class of oral medications is now preferred over traditional immunosuppressants", "answer": "What are JAK inhibitors (or biologics)?", "rationale": "JAKi and biologics have better safety/efficacy profiles", "difficulty": "intermediate"},

        {"category": "Biologics & JAK Inhibitors", "question": "This IL-4/IL-13 blocker was the first biologic approved for AD", "answer": "What is dupilumab (Dupixent)?", "rationale": "Dupilumab blocks IL-4Rα, inhibiting both IL-4 and IL-13 signaling", "difficulty": "basic"},
        {"category": "Biologics & JAK Inhibitors", "question": "This unique side effect of dupilumab affects the eyes", "answer": "What is conjunctivitis?", "rationale": "Conjunctivitis occurs in ~10-25% of AD patients on dupilumab", "difficulty": "intermediate"},
        {"category": "Biologics & JAK Inhibitors", "question": "This oral JAK inhibitor is approved for moderate-to-severe AD", "answer": "What is upadacitinib (Rinvoq) or abrocitinib (Cibinqo)?", "rationale": "JAK1 inhibitors provide rapid itch relief and skin clearance", "difficulty": "intermediate"},
        {"category": "Biologics & JAK Inhibitors", "question": "This IL-13 specific antibody is approved for AD", "answer": "What is tralokinumab (Adbry)?", "rationale": "Tralokinumab specifically targets IL-13 only", "difficulty": "intermediate"},
        {"category": "Biologics & JAK Inhibitors", "question": "This boxed warning applies to JAK inhibitors", "answer": "What is risk of serious infections, malignancy, MACE, and thrombosis?", "rationale": "JAK inhibitor class labeling based on RA safety data", "difficulty": "advanced"},

        {"category": "Special Considerations", "question": "This age group has different AD distribution (cheeks, extensor surfaces)", "answer": "What is infants/young children?", "rationale": "AD morphology and distribution varies by age", "difficulty": "basic"},
        {"category": "Special Considerations", "question": "This intervention is recommended for all AD patients to maintain barrier", "answer": "What is daily moisturizer/emollient application?", "rationale": "Liberal emollient use is foundation of AD management", "difficulty": "basic"},
        {"category": "Special Considerations", "question": "This bathing practice is recommended for AD patients", "answer": "What is lukewarm baths with immediate moisturizer application?", "rationale": "Soak and seal technique improves hydration", "difficulty": "basic"},
        {"category": "Special Considerations", "question": "This dupilumab dosing is used for children 6 months to 5 years", "answer": "What is weight-based dosing (200mg or 300mg q4w)?", "rationale": "Dupilumab approved down to 6 months of age", "difficulty": "advanced"},
        {"category": "Special Considerations", "question": "This assessment should be done before starting JAK inhibitors", "answer": "What is screening for TB, hepatitis, and updating vaccinations?", "rationale": "Live vaccines should be given before starting JAK inhibitors", "difficulty": "advanced"},
    ],
    final_jeopardy={
        "category": "AD Breakthrough",
        "question": "This 2017 FDA approval marked the first biologic for atopic dermatitis, targeting IL-4 receptor alpha",
        "answer": "What is dupilumab (Dupixent)?",
        "rationale": "Dupilumab revolutionized AD treatment and paved the way for other biologics"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Understand the pathophysiology of atopic dermatitis",
        "Implement a stepwise approach to AD management",
        "Select appropriate systemic therapy for moderate-to-severe AD",
        "Monitor for adverse effects of biologics and JAK inhibitors"
    ]
)
register_game(ATOPIC_DERMATITIS_GAME)


EOE_GAME = ConditionGame(
    condition_id="eoe",
    condition_name="Eosinophilic Esophagitis",
    therapeutic_area="Gastroenterology/Immunology",
    description="Comprehensive review of eosinophilic esophagitis diagnosis and management",
    categories=[
        "Pathophysiology",
        "Clinical Presentation",
        "Diagnosis",
        "Dietary Therapy",
        "Pharmacotherapy",
        "Emerging Treatments"
    ],
    questions=[
        {"category": "Pathophysiology", "question": "This eosinophil threshold on biopsy is required for EoE diagnosis", "answer": "What is ≥15 eosinophils per high-power field?", "rationale": "≥15 eos/HPF in ≥1 esophageal biopsy is diagnostic criterion", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This cytokine is central to eosinophil recruitment in EoE", "answer": "What is IL-5 (or IL-13, eotaxin-3)?", "rationale": "Th2 cytokines drive eosinophilic inflammation in EoE", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This food allergen is the most common EoE trigger", "answer": "What is milk (cow's milk protein)?", "rationale": "Milk, wheat, egg, soy are most common triggers", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This long-term complication results from chronic EoE inflammation", "answer": "What is esophageal fibrosis/stricture?", "rationale": "Untreated EoE leads to remodeling and stricture formation", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This gene encoding eotaxin-3 is upregulated in EoE", "answer": "What is CCL26?", "rationale": "CCL26 is a potent eosinophil chemoattractant in EoE", "difficulty": "expert"},

        {"category": "Clinical Presentation", "question": "This is the most common presenting symptom in adults with EoE", "answer": "What is dysphagia (to solids)?", "rationale": "Dysphagia occurs in >70% of adult EoE patients", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This acute presentation often brings EoE patients to the ED", "answer": "What is food impaction?", "rationale": "Food bolus impaction may be first presentation of undiagnosed EoE", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This symptom is more common in children with EoE than adults", "answer": "What is feeding difficulties/food refusal?", "rationale": "Children may present with vomiting, abdominal pain, failure to thrive", "difficulty": "intermediate"},
        {"category": "Clinical Presentation", "question": "This atopic condition is commonly associated with EoE", "answer": "What is asthma (or allergic rhinitis, atopic dermatitis)?", "rationale": "Most EoE patients have concurrent atopic disease", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This endoscopic finding describes stacked circular ridges", "answer": "What are rings (trachealization)?", "rationale": "Rings, furrows, white exudates are classic EoE findings", "difficulty": "intermediate"},

        {"category": "Diagnosis", "question": "This number of biopsies should be taken during EGD for EoE diagnosis", "answer": "What is 6 (2-4 from proximal and distal esophagus)?", "rationale": "Multiple biopsies increase diagnostic sensitivity due to patchy disease", "difficulty": "intermediate"},
        {"category": "Diagnosis", "question": "This condition must be excluded before diagnosing EoE", "answer": "What is GERD (or PPI-responsive esophageal eosinophilia)?", "rationale": "Previous guidelines required PPI trial; now EoE and GERD can coexist", "difficulty": "intermediate"},
        {"category": "Diagnosis", "question": "This patient-reported outcome measures EoE symptoms", "answer": "What is DSQ (Dysphagia Symptom Questionnaire)?", "rationale": "DSQ is validated PRO used in EoE clinical trials", "difficulty": "advanced"},
        {"category": "Diagnosis", "question": "This finding on biopsy suggests response to therapy", "answer": "What is <15 eos/HPF (or <6 eos/HPF)?", "rationale": "Histologic remission is a treatment goal in EoE", "difficulty": "intermediate"},
        {"category": "Diagnosis", "question": "This scoring system assesses endoscopic features of EoE", "answer": "What is EREFS (Endoscopic Reference Score)?", "rationale": "EREFS grades Edema, Rings, Exudates, Furrows, Strictures", "difficulty": "advanced"},

        {"category": "Dietary Therapy", "question": "This elimination diet removes the most common triggers", "answer": "What is the 6-food elimination diet (6FED)?", "rationale": "6FED eliminates milk, wheat, egg, soy, fish/shellfish, nuts", "difficulty": "basic"},
        {"category": "Dietary Therapy", "question": "This simplified elimination diet has similar efficacy to 6FED", "answer": "What is the 2-food elimination diet (milk and wheat)?", "rationale": "2FED effective in ~40% of patients with less dietary burden", "difficulty": "intermediate"},
        {"category": "Dietary Therapy", "question": "This formula-based diet has highest efficacy in EoE", "answer": "What is elemental diet?", "rationale": "Elemental diet ~90% effective but difficult to maintain", "difficulty": "intermediate"},
        {"category": "Dietary Therapy", "question": "This process identifies specific food triggers after elimination", "answer": "What is sequential food reintroduction?", "rationale": "Foods reintroduced one at a time with repeat EGD to identify triggers", "difficulty": "intermediate"},
        {"category": "Dietary Therapy", "question": "This allergy testing is NOT reliable for identifying EoE triggers", "answer": "What is skin prick testing (or specific IgE)?", "rationale": "EoE is non-IgE mediated; allergy testing does not predict triggers", "difficulty": "advanced"},

        {"category": "Pharmacotherapy", "question": "This swallowed topical corticosteroid is used for EoE", "answer": "What is swallowed fluticasone (or budesonide slurry)?", "rationale": "Topical steroids are first-line pharmacotherapy for EoE", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This FDA-approved formulation is specifically designed for esophageal delivery", "answer": "What is budesonide oral suspension (Eohilia)?", "rationale": "First FDA-approved EoE-specific formulation (2024)", "difficulty": "intermediate"},
        {"category": "Pharmacotherapy", "question": "This orally disintegrating tablet delivers budesonide to the esophagus", "answer": "What is budesonide ODT (Jorveza - EU)?", "rationale": "ODT formulation dissolves in mouth and coats esophagus when swallowed", "difficulty": "intermediate"},
        {"category": "Pharmacotherapy", "question": "This instruction optimizes topical steroid delivery for EoE", "answer": "What is no eating/drinking for 30-60 minutes after dosing?", "rationale": "Avoiding food/liquid maximizes esophageal contact time", "difficulty": "intermediate"},
        {"category": "Pharmacotherapy", "question": "This fungal infection can complicate topical steroid therapy", "answer": "What is esophageal candidiasis?", "rationale": "Candidiasis occurs in ~10-20% of patients on swallowed steroids", "difficulty": "intermediate"},

        {"category": "Emerging Treatments", "question": "This IL-4/IL-13 blocking antibody is FDA-approved for EoE", "answer": "What is dupilumab (Dupixent)?", "rationale": "Dupilumab approved for EoE in 2022 based on phase 3 trials", "difficulty": "basic"},
        {"category": "Emerging Treatments", "question": "This IL-13 antibody showed efficacy in EoE trials", "answer": "What is cendakimab?", "rationale": "IL-13 specific antibodies in development for EoE", "difficulty": "advanced"},
        {"category": "Emerging Treatments", "question": "This anti-IL-5 antibody is being studied for EoE", "answer": "What is mepolizumab (or benralizumab)?", "rationale": "Anti-IL-5 agents target eosinophil production/survival", "difficulty": "advanced"},
        {"category": "Emerging Treatments", "question": "This endoscopic procedure treats EoE strictures", "answer": "What is esophageal dilation?", "rationale": "Dilation safe and effective for symptomatic strictures", "difficulty": "intermediate"},
        {"category": "Emerging Treatments", "question": "This CRTH2 antagonist targets prostaglandin D2 receptor in EoE", "answer": "What is a DP2 antagonist?", "rationale": "CRTH2/DP2 antagonists in early development for EoE", "difficulty": "expert"},
    ],
    final_jeopardy={
        "category": "EoE Milestones",
        "question": "This year saw the first FDA-approved treatment specifically for eosinophilic esophagitis",
        "answer": "What is 2022 (dupilumab approval)?",
        "rationale": "Dupilumab became first FDA-approved EoE therapy in May 2022"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Apply diagnostic criteria for eosinophilic esophagitis",
        "Implement dietary and pharmacologic treatments for EoE",
        "Monitor response to therapy using endoscopic and histologic endpoints",
        "Recognize emerging biologics for EoE treatment"
    ]
)
register_game(EOE_GAME)


NASAL_POLYPS_GAME = ConditionGame(
    condition_id="nasal_polyps",
    condition_name="Chronic Rhinosinusitis with Nasal Polyps (CRSwNP)",
    therapeutic_area="Otolaryngology/Immunology",
    description="Comprehensive review of CRSwNP pathophysiology and management",
    categories=[
        "Pathophysiology",
        "Diagnosis",
        "Medical Management",
        "Biologics",
        "Surgical Management",
        "Comorbidities"
    ],
    questions=[
        {"category": "Pathophysiology", "question": "This type 2 cytokine is elevated in most CRSwNP patients", "answer": "What is IL-5 (or IL-4, IL-13)?", "rationale": "Th2 inflammation predominates in Western CRSwNP", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This cell type is characteristically elevated in nasal polyp tissue", "answer": "What are eosinophils?", "rationale": "Eosinophilic inflammation is hallmark of CRSwNP", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This triad includes asthma, nasal polyps, and aspirin sensitivity", "answer": "What is Samter's triad (AERD)?", "rationale": "Aspirin-exacerbated respiratory disease is a severe CRSwNP phenotype", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This biomarker is elevated in type 2 CRSwNP", "answer": "What is total IgE (or periostin, blood eosinophils)?", "rationale": "Elevated IgE and eosinophils suggest type 2 inflammation", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This alarmin cytokine promotes type 2 inflammation in CRSwNP", "answer": "What is TSLP (or IL-25, IL-33)?", "rationale": "Epithelial-derived alarmins initiate type 2 immune response", "difficulty": "advanced"},

        {"category": "Diagnosis", "question": "This duration of symptoms is required for chronic rhinosinusitis diagnosis", "answer": "What is ≥12 weeks?", "rationale": "CRS defined by >12 weeks of symptoms", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This imaging modality best evaluates paranasal sinuses", "answer": "What is CT scan (without contrast)?", "rationale": "CT is gold standard for assessing sinus anatomy and disease extent", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This scoring system grades nasal polyp size on endoscopy", "answer": "What is the nasal polyp score (NPS)?", "rationale": "NPS 0-4 per side (0-8 total) used in clinical trials", "difficulty": "intermediate"},
        {"category": "Diagnosis", "question": "This symptom domain is most impacted by nasal polyps", "answer": "What is smell/olfaction (anosmia/hyposmia)?", "rationale": "Olfactory dysfunction is highly prevalent in CRSwNP", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This patient-reported outcome measures sinonasal symptoms", "answer": "What is SNOT-22 (Sino-Nasal Outcome Test)?", "rationale": "SNOT-22 is validated PRO for CRS severity", "difficulty": "intermediate"},

        {"category": "Medical Management", "question": "This topical therapy is first-line for CRSwNP", "answer": "What are intranasal corticosteroids?", "rationale": "INCS reduce polyp size and improve symptoms", "difficulty": "basic"},
        {"category": "Medical Management", "question": "This delivery method improves corticosteroid distribution to sinuses", "answer": "What is high-volume saline irrigation (with budesonide)?", "rationale": "Budesonide added to saline rinse reaches sinus cavities", "difficulty": "intermediate"},
        {"category": "Medical Management", "question": "This course of oral corticosteroids may provide temporary relief", "answer": "What is a short burst (5-14 days) of prednisone?", "rationale": "Oral steroids shrink polyps but effect temporary; limit use", "difficulty": "basic"},
        {"category": "Medical Management", "question": "This antibiotic class is sometimes used for CRS exacerbations", "answer": "What are macrolides (or doxycycline)?", "rationale": "Macrolides have anti-inflammatory properties; controversial in CRSwNP", "difficulty": "intermediate"},
        {"category": "Medical Management", "question": "This leukotriene modifier may benefit AERD patients", "answer": "What is montelukast (or zileuton)?", "rationale": "Leukotriene pathway overactive in AERD", "difficulty": "intermediate"},

        {"category": "Biologics", "question": "This IL-4/IL-13 blocker is approved for CRSwNP", "answer": "What is dupilumab (Dupixent)?", "rationale": "Dupilumab first biologic approved for CRSwNP (2019)", "difficulty": "basic"},
        {"category": "Biologics", "question": "This anti-IgE antibody is approved for CRSwNP", "answer": "What is omalizumab (Xolair)?", "rationale": "Omalizumab approved for CRSwNP (2020) based on POLYP 1&2 trials", "difficulty": "intermediate"},
        {"category": "Biologics", "question": "This anti-IL-5 antibody is approved for CRSwNP", "answer": "What is mepolizumab (Nucala)?", "rationale": "Mepolizumab approved for CRSwNP (2021)", "difficulty": "intermediate"},
        {"category": "Biologics", "question": "This endpoint is commonly used in CRSwNP biologic trials", "answer": "What is change in nasal polyp score (NPS)?", "rationale": "NPS, nasal congestion, and smell are key endpoints", "difficulty": "intermediate"},
        {"category": "Biologics", "question": "This anti-IL-5R antibody is also approved for CRSwNP", "answer": "What is benralizumab (Fasenra)?", "rationale": "Benralizumab approved for CRSwNP in 2024", "difficulty": "advanced"},

        {"category": "Surgical Management", "question": "This procedure is the surgical standard for CRSwNP", "answer": "What is functional endoscopic sinus surgery (FESS)?", "rationale": "FESS opens sinuses to improve drainage and medication delivery", "difficulty": "basic"},
        {"category": "Surgical Management", "question": "This indication for surgery includes failed medical therapy", "answer": "What is refractory CRSwNP?", "rationale": "Surgery indicated when medical therapy fails to control disease", "difficulty": "basic"},
        {"category": "Surgical Management", "question": "This rate of polyp recurrence after surgery is concerning", "answer": "What is 40-80% recurrence over 5-10 years?", "rationale": "High recurrence rates support ongoing medical therapy post-surgery", "difficulty": "intermediate"},
        {"category": "Surgical Management", "question": "This extended procedure removes more tissue for severe disease", "answer": "What is Draf III (modified Lothrop) procedure?", "rationale": "Extended frontal sinusotomy for recalcitrant frontal disease", "difficulty": "advanced"},
        {"category": "Surgical Management", "question": "This implant releases corticosteroid in the ethmoid sinus after FESS", "answer": "What is a steroid-eluting sinus implant (Propel)?", "rationale": "Drug-eluting stents reduce post-operative inflammation", "difficulty": "advanced"},

        {"category": "Comorbidities", "question": "This lower airway disease is strongly associated with CRSwNP", "answer": "What is asthma?", "rationale": "~50% of CRSwNP patients have comorbid asthma", "difficulty": "basic"},
        {"category": "Comorbidities", "question": "This unified airway concept links upper and lower airway inflammation", "answer": "What is the united airways hypothesis?", "rationale": "CRSwNP and asthma share pathophysiology and respond to similar treatments", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This reaction to NSAIDs characterizes AERD", "answer": "What is respiratory reaction (nasal congestion, bronchospasm)?", "rationale": "NSAID ingestion triggers upper and lower airway symptoms", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This desensitization approach may benefit AERD patients", "answer": "What is aspirin desensitization?", "rationale": "Aspirin desensitization after surgery may slow polyp recurrence", "difficulty": "advanced"},
        {"category": "Comorbidities", "question": "This genetic condition causes CRSwNP with bronchiectasis", "answer": "What is cystic fibrosis (or primary ciliary dyskinesia)?", "rationale": "CF should be considered in young patients with polyps", "difficulty": "advanced"},
    ],
    final_jeopardy={
        "category": "CRSwNP Treatment Evolution",
        "question": "This 2019 FDA approval marked the first biologic therapy for chronic rhinosinusitis with nasal polyps",
        "answer": "What is dupilumab (Dupixent)?",
        "rationale": "Dupilumab launched the era of targeted biologics for CRSwNP"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Diagnose and classify chronic rhinosinusitis with nasal polyps",
        "Implement stepwise medical management for CRSwNP",
        "Select appropriate biologic therapy based on patient characteristics",
        "Understand the role of surgery in CRSwNP management"
    ]
)
register_game(NASAL_POLYPS_GAME)


IMID_GAME = ConditionGame(
    condition_id="imid",
    condition_name="Immune-Mediated Inflammatory Diseases (IMID)",
    therapeutic_area="Rheumatology/Immunology",
    description="Comprehensive review of immune-mediated inflammatory diseases including RA, PsA, AS, and IBD",
    categories=[
        "IMID Pathophysiology",
        "Rheumatoid Arthritis",
        "Psoriatic Arthritis",
        "Axial Spondyloarthritis",
        "TNF Inhibitors & JAKi",
        "Newer Biologics"
    ],
    questions=[
        # IMID Pathophysiology
        {"category": "IMID Pathophysiology", "question": "This pro-inflammatory cytokine is targeted by adalimumab, infliximab, and etanercept", "answer": "What is TNF-alpha?", "rationale": "TNF is central to inflammation in RA, PsA, AS, IBD", "difficulty": "basic"},
        {"category": "IMID Pathophysiology", "question": "This interleukin drives psoriatic disease and is targeted by ustekinumab", "answer": "What is IL-23 (or IL-12)?", "rationale": "IL-12/23p40 subunit targeted by ustekinumab; IL-23 by guselkumab/risankizumab", "difficulty": "intermediate"},
        {"category": "IMID Pathophysiology", "question": "This cytokine pathway is blocked by secukinumab and ixekizumab", "answer": "What is IL-17?", "rationale": "IL-17 inhibitors effective in PsA, AS, psoriasis", "difficulty": "intermediate"},
        {"category": "IMID Pathophysiology", "question": "This intracellular signaling pathway is inhibited by JAK inhibitors", "answer": "What is the JAK-STAT pathway?", "rationale": "JAKi block cytokine signaling through JAK1, JAK2, JAK3, TYK2", "difficulty": "intermediate"},
        {"category": "IMID Pathophysiology", "question": "This IMID concept recognizes shared inflammatory pathways across diseases", "answer": "What is the IMID spectrum (or common inflammatory pathways)?", "rationale": "RA, PsA, AS, IBD share TNF/IL-17/IL-23 pathway involvement", "difficulty": "intermediate"},

        # Rheumatoid Arthritis
        {"category": "Rheumatoid Arthritis", "question": "This autoantibody is highly specific for rheumatoid arthritis", "answer": "What is anti-CCP (anti-citrullinated protein antibody)?", "rationale": "Anti-CCP ~95% specific; RF less specific", "difficulty": "basic"},
        {"category": "Rheumatoid Arthritis", "question": "This DMARD is first-line therapy for RA", "answer": "What is methotrexate?", "rationale": "MTX is anchor drug; typically started 15-25mg weekly", "difficulty": "basic"},
        {"category": "Rheumatoid Arthritis", "question": "This T-cell costimulation blocker is approved for RA", "answer": "What is abatacept (Orencia)?", "rationale": "Abatacept blocks CD80/86-CD28 costimulation", "difficulty": "intermediate"},
        {"category": "Rheumatoid Arthritis", "question": "This IL-6 receptor inhibitor is used in RA", "answer": "What is tocilizumab (Actemra) or sarilumab (Kevzara)?", "rationale": "IL-6Ri effective in RA; can be used as monotherapy", "difficulty": "intermediate"},
        {"category": "Rheumatoid Arthritis", "question": "This treat-to-target goal in RA is measured by DAS28 or CDAI", "answer": "What is remission (or low disease activity)?", "rationale": "Treat-to-target improves outcomes; adjust therapy every 3 months if not at goal", "difficulty": "intermediate"},

        # Psoriatic Arthritis
        {"category": "Psoriatic Arthritis", "question": "This clinical feature distinguishes PsA from RA (swelling of entire digit)", "answer": "What is dactylitis (sausage digit)?", "rationale": "Dactylitis highly characteristic of PsA and reactive arthritis", "difficulty": "basic"},
        {"category": "Psoriatic Arthritis", "question": "This enthesis inflammation is common in PsA", "answer": "What is enthesitis?", "rationale": "Enthesitis at Achilles, plantar fascia common in spondyloarthritis", "difficulty": "intermediate"},
        {"category": "Psoriatic Arthritis", "question": "This DIP joint involvement pattern is characteristic of PsA", "answer": "What is distal interphalangeal joint arthritis?", "rationale": "DIP involvement with nail changes classic for PsA", "difficulty": "intermediate"},
        {"category": "Psoriatic Arthritis", "question": "This IL-17 inhibitor is approved for both PsA and psoriasis", "answer": "What is secukinumab (Cosentyx) or ixekizumab (Taltz)?", "rationale": "IL-17i highly effective for skin and joint disease in PsA", "difficulty": "intermediate"},
        {"category": "Psoriatic Arthritis", "question": "This PDE4 inhibitor is an oral option for PsA", "answer": "What is apremilast (Otezla)?", "rationale": "Apremilast modestly effective; no immunosuppression", "difficulty": "intermediate"},

        # Axial Spondyloarthritis
        {"category": "Axial Spondyloarthritis", "question": "This HLA gene is strongly associated with ankylosing spondylitis", "answer": "What is HLA-B27?", "rationale": "HLA-B27 present in >90% of AS patients", "difficulty": "basic"},
        {"category": "Axial Spondyloarthritis", "question": "This type of back pain improves with activity and worsens with rest", "answer": "What is inflammatory back pain?", "rationale": "Inflammatory: morning stiffness >30 min, improves with exercise", "difficulty": "basic"},
        {"category": "Axial Spondyloarthritis", "question": "This imaging finding on MRI indicates active sacroiliitis", "answer": "What is bone marrow edema (on STIR/T2)?", "rationale": "MRI can detect early inflammation before X-ray changes", "difficulty": "intermediate"},
        {"category": "Axial Spondyloarthritis", "question": "This first-line therapy for axSpA reduces pain and stiffness", "answer": "What are NSAIDs (continuous use)?", "rationale": "NSAIDs are first-line; TNFi/IL-17i for NSAID-refractory disease", "difficulty": "basic"},
        {"category": "Axial Spondyloarthritis", "question": "This IL-17 inhibitor was first to show efficacy in axSpA (nr-axSpA)", "answer": "What is secukinumab (or ixekizumab)?", "rationale": "IL-17i now approved for both r-axSpA and nr-axSpA", "difficulty": "intermediate"},

        # TNF Inhibitors & JAKi
        {"category": "TNF Inhibitors & JAKi", "question": "This TNF inhibitor is a fully human monoclonal antibody", "answer": "What is adalimumab (Humira)?", "rationale": "Adalimumab approved for RA, PsA, AS, IBD, psoriasis, uveitis", "difficulty": "basic"},
        {"category": "TNF Inhibitors & JAKi", "question": "This TNF inhibitor is given as IV infusion every 6-8 weeks", "answer": "What is infliximab (Remicade)?", "rationale": "Infliximab is chimeric mAb; requires IV administration", "difficulty": "basic"},
        {"category": "TNF Inhibitors & JAKi", "question": "This screening is required before starting TNFi or JAKi", "answer": "What is tuberculosis screening (TB test)?", "rationale": "Latent TB reactivation risk; treat LTBI before starting", "difficulty": "basic"},
        {"category": "TNF Inhibitors & JAKi", "question": "This JAK1 inhibitor is approved for RA, PsA, AS, and AD", "answer": "What is upadacitinib (Rinvoq)?", "rationale": "JAK1 selective inhibitor with broad IMID indications", "difficulty": "intermediate"},
        {"category": "TNF Inhibitors & JAKi", "question": "This boxed warning applies to JAK inhibitors in RA", "answer": "What is increased risk of MACE, malignancy, thrombosis, and serious infections?", "rationale": "ORAL Surveillance trial prompted class-wide warnings", "difficulty": "advanced"},

        # Newer Biologics
        {"category": "Newer Biologics", "question": "This IL-23 inhibitor selectively blocks p19 subunit", "answer": "What is risankizumab (Skyrizi) or guselkumab (Tremfya)?", "rationale": "IL-23p19 inhibitors spare IL-12 pathway; very effective in psoriasis/PsA", "difficulty": "intermediate"},
        {"category": "Newer Biologics", "question": "This TYK2 inhibitor is an oral option for psoriasis", "answer": "What is deucravacitinib (Sotyktu)?", "rationale": "TYK2 inhibition is more selective than JAK1/2/3", "difficulty": "advanced"},
        {"category": "Newer Biologics", "question": "This IL-17A/F inhibitor blocks both IL-17A and IL-17F", "answer": "What is bimekizumab (Bimzelx)?", "rationale": "Dual IL-17 inhibition may provide superior skin clearance", "difficulty": "advanced"},
        {"category": "Newer Biologics", "question": "This biosimilar concept makes biologics more accessible", "answer": "What are biosimilars?", "rationale": "Biosimilars have same efficacy/safety as originator biologics at lower cost", "difficulty": "basic"},
        {"category": "Newer Biologics", "question": "This treatment sequence is often used: csDMARD → bDMARD → JAKi", "answer": "What is the stepwise approach to IMID treatment?", "rationale": "ACR/EULAR guidelines recommend MTX first, then advanced therapy", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "IMID Milestones",
        "question": "This 1998 FDA approval of infliximab for Crohn's disease marked the beginning of the biologic era for immune-mediated diseases",
        "answer": "What is infliximab (Remicade)?",
        "rationale": "Infliximab was first TNF inhibitor; revolutionized treatment of IMIDs"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Understand shared inflammatory pathways across IMIDs",
        "Select appropriate biologic therapy based on disease and patient factors",
        "Monitor for adverse effects of immunomodulatory therapy",
        "Apply treat-to-target strategies in inflammatory arthritis"
    ]
)
register_game(IMID_GAME)
