"""
Pulmonary Condition Games

Includes: Asthma, Sleep Apnea
"""

from jparty.condition_games import ConditionGame, register_game


ASTHMA_GAME = ConditionGame(
    condition_id="asthma",
    condition_name="Asthma",
    therapeutic_area="Pulmonology",
    description="Comprehensive review of asthma pathophysiology, diagnosis, and management including severe asthma",
    categories=[
        "Pathophysiology",
        "Diagnosis & Assessment",
        "Controller Medications",
        "Reliever Medications",
        "Severe Asthma & Biologics",
        "Special Populations"
    ],
    questions=[
        # Pathophysiology
        {"category": "Pathophysiology", "question": "This type 2 inflammation pathway involves IL-4, IL-5, and IL-13", "answer": "What is eosinophilic/allergic inflammation?", "rationale": "Type 2 inflammation drives most asthma; targetable with biologics", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This structural airway change from chronic inflammation is called remodeling", "answer": "What is airway remodeling?", "rationale": "Remodeling includes smooth muscle hypertrophy, fibrosis, goblet cell hyperplasia", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This immunoglobulin is elevated in allergic asthma", "answer": "What is IgE?", "rationale": "IgE mediates allergic response; targeted by omalizumab", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This cell type is the hallmark of eosinophilic asthma", "answer": "What are eosinophils?", "rationale": "Blood and sputum eosinophils indicate type 2 inflammation", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This epithelial-derived alarmin cytokine initiates type 2 inflammation", "answer": "What is TSLP (or IL-25, IL-33)?", "rationale": "Alarmins released from damaged epithelium activate type 2 cascade", "difficulty": "advanced"},

        # Diagnosis & Assessment
        {"category": "Diagnosis & Assessment", "question": "This spirometry pattern shows reversible airflow obstruction", "answer": "What is reduced FEV1/FVC with ≥12% and 200mL improvement post-bronchodilator?", "rationale": "Reversibility confirms asthma diagnosis", "difficulty": "basic"},
        {"category": "Diagnosis & Assessment", "question": "This biomarker measured in exhaled breath indicates eosinophilic inflammation", "answer": "What is FeNO (fractional exhaled nitric oxide)?", "rationale": "FeNO >25-50 ppb suggests type 2/eosinophilic asthma", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This peak flow variability threshold supports asthma diagnosis", "answer": "What is >10% diurnal variation (or >20% on >3 days/week)?", "rationale": "Increased variability indicates airway hyperresponsiveness", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This challenge test confirms airway hyperresponsiveness", "answer": "What is methacholine challenge?", "rationale": "PC20 <4 mg/mL indicates airway hyperresponsiveness", "difficulty": "intermediate"},
        {"category": "Diagnosis & Assessment", "question": "This assessment tool asks about symptom control and rescue use", "answer": "What is ACT (Asthma Control Test)?", "rationale": "ACT score ≤19 indicates poorly controlled asthma", "difficulty": "basic"},

        # Controller Medications
        {"category": "Controller Medications", "question": "This medication class is the cornerstone of asthma controller therapy", "answer": "What are inhaled corticosteroids (ICS)?", "rationale": "ICS reduce inflammation and are first-line maintenance", "difficulty": "basic"},
        {"category": "Controller Medications", "question": "This LABA is combined with ICS in many combination inhalers", "answer": "What is formoterol (or salmeterol, vilanterol)?", "rationale": "ICS/LABA combinations are step 3-5 therapy", "difficulty": "basic"},
        {"category": "Controller Medications", "question": "This LAMA is approved as add-on therapy for uncontrolled asthma", "answer": "What is tiotropium (Spiriva Respimat)?", "rationale": "Tiotropium improves lung function when added to ICS/LABA", "difficulty": "intermediate"},
        {"category": "Controller Medications", "question": "This leukotriene modifier is an alternative add-on controller", "answer": "What is montelukast (Singulair)?", "rationale": "LTRAs helpful in aspirin-sensitive and exercise-induced asthma", "difficulty": "basic"},
        {"category": "Controller Medications", "question": "This ICS/formoterol combination is used for both maintenance AND reliever therapy (MART)", "answer": "What is budesonide/formoterol (Symbicort)?", "rationale": "MART/SMART approach reduces exacerbations vs SABA reliever", "difficulty": "intermediate"},

        # Reliever Medications
        {"category": "Reliever Medications", "question": "This SABA is the traditional rescue medication for asthma", "answer": "What is albuterol (salbutamol)?", "rationale": "SABA for acute symptoms; overuse indicates poor control", "difficulty": "basic"},
        {"category": "Reliever Medications", "question": "GINA now recommends this as preferred reliever for mild asthma", "answer": "What is as-needed ICS/formoterol?", "rationale": "As-needed ICS/formoterol preferred over SABA alone in mild asthma", "difficulty": "intermediate"},
        {"category": "Reliever Medications", "question": "This reliever use threshold indicates increased risk and poor control", "answer": "What is using SABA ≥3 times per week (excluding pre-exercise)?", "rationale": "Frequent SABA use predicts exacerbations and death risk", "difficulty": "intermediate"},
        {"category": "Reliever Medications", "question": "This safety signal ended use of SABA monotherapy in GINA 2019", "answer": "What is increased severe exacerbation and death risk?", "rationale": "SABA-only treatment (without ICS) increases mortality risk", "difficulty": "advanced"},
        {"category": "Reliever Medications", "question": "This anticholinergic is added to albuterol in acute severe asthma", "answer": "What is ipratropium?", "rationale": "Ipratropium + albuterol in ED reduces hospitalizations", "difficulty": "intermediate"},

        # Severe Asthma & Biologics
        {"category": "Severe Asthma & Biologics", "question": "This anti-IgE antibody was the first biologic approved for asthma", "answer": "What is omalizumab (Xolair)?", "rationale": "Omalizumab for allergic asthma with elevated IgE", "difficulty": "basic"},
        {"category": "Severe Asthma & Biologics", "question": "This anti-IL-5 antibody reduces blood eosinophils in severe eosinophilic asthma", "answer": "What is mepolizumab (Nucala)?", "rationale": "Anti-IL-5 biologics for eosinophilic asthma (eos ≥150-300)", "difficulty": "intermediate"},
        {"category": "Severe Asthma & Biologics", "question": "This anti-IL-5 receptor antibody causes eosinophil apoptosis", "answer": "What is benralizumab (Fasenra)?", "rationale": "Benralizumab given Q8 weeks after initial doses", "difficulty": "intermediate"},
        {"category": "Severe Asthma & Biologics", "question": "This anti-IL-4Rα antibody blocks both IL-4 and IL-13", "answer": "What is dupilumab (Dupixent)?", "rationale": "Dupilumab for eosinophilic and/or oral steroid-dependent asthma", "difficulty": "intermediate"},
        {"category": "Severe Asthma & Biologics", "question": "This anti-TSLP antibody works upstream and is effective regardless of biomarkers", "answer": "What is tezepelumab (Tezspire)?", "rationale": "Tezepelumab reduces exacerbations across all severe asthma phenotypes", "difficulty": "advanced"},

        # Special Populations
        {"category": "Special Populations", "question": "This asthma trigger causes symptoms with exercise", "answer": "What is exercise-induced bronchoconstriction (EIB)?", "rationale": "Pre-exercise SABA or LABA prevents EIB; ICS reduces severity", "difficulty": "basic"},
        {"category": "Special Populations", "question": "This triad includes asthma, nasal polyps, and aspirin sensitivity", "answer": "What is Samter's triad (AERD)?", "rationale": "AERD patients often have severe eosinophilic disease", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This occupational exposure pattern suggests work-related asthma", "answer": "What is symptoms worse at work, better on weekends/vacation?", "rationale": "Occupational asthma may require job modification or change", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This management approach is safe and effective in pregnancy", "answer": "What is continuing controller medications (ICS)?", "rationale": "Uncontrolled asthma is greater risk to pregnancy than ICS", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This overlap syndrome combines features of asthma and COPD", "answer": "What is ACO (Asthma-COPD Overlap)?", "rationale": "ACO requires ICS-containing therapy; not LAMA/LABA alone", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "Asthma Guidelines",
        "question": "This 2019 GINA update fundamentally changed asthma treatment by recommending against this traditional reliever approach",
        "answer": "What is SABA-only treatment (without any ICS)?",
        "rationale": "GINA 2019 recommended ICS-containing reliever for all symptomatic asthma"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Classify asthma severity and assess control",
        "Implement stepwise pharmacotherapy per GINA guidelines",
        "Identify candidates for biologic therapy",
        "Understand the role of type 2 biomarkers in asthma management"
    ]
)
register_game(ASTHMA_GAME)


SLEEP_APNEA_GAME = ConditionGame(
    condition_id="sleep_apnea",
    condition_name="Obstructive Sleep Apnea",
    therapeutic_area="Sleep Medicine/Pulmonology",
    description="Comprehensive review of OSA pathophysiology, diagnosis, and management",
    categories=[
        "Pathophysiology",
        "Clinical Presentation",
        "Diagnosis",
        "CPAP Therapy",
        "Alternative Treatments",
        "Comorbidities"
    ],
    questions=[
        # Pathophysiology
        {"category": "Pathophysiology", "question": "This anatomical site of collapse causes obstructive sleep apnea", "answer": "What is the upper airway (pharynx)?", "rationale": "Pharyngeal collapse during sleep from reduced muscle tone", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This BMI threshold significantly increases OSA risk", "answer": "What is BMI ≥30 kg/m² (obesity)?", "rationale": "Obesity is strongest risk factor; fat deposition narrows airway", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This anatomical structure can obstruct the airway in children with OSA", "answer": "What are enlarged tonsils and adenoids?", "rationale": "Adenotonsillectomy is first-line treatment in pediatric OSA", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This respiratory event is a complete cessation of airflow for ≥10 seconds", "answer": "What is an apnea?", "rationale": "Apneas cause oxygen desaturation and arousal from sleep", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This respiratory event is a ≥30% reduction in airflow with ≥3% desaturation or arousal", "answer": "What is a hypopnea?", "rationale": "Hypopneas also contribute to sleep fragmentation", "difficulty": "intermediate"},

        # Clinical Presentation
        {"category": "Clinical Presentation", "question": "This nocturnal symptom is the hallmark of OSA", "answer": "What is snoring?", "rationale": "Loud snoring often reported by bed partner", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This daytime symptom is most common in untreated OSA", "answer": "What is excessive daytime sleepiness?", "rationale": "EDS affects quality of life and driving safety", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This questionnaire screens for sleepiness on a scale of 0-24", "answer": "What is the Epworth Sleepiness Scale?", "rationale": "ESS ≥10 suggests excessive daytime sleepiness", "difficulty": "basic"},
        {"category": "Clinical Presentation", "question": "This screening tool asks about Snoring, Tiredness, Observed apnea, Pressure, BMI, Age, Neck, Gender", "answer": "What is STOP-BANG?", "rationale": "STOP-BANG ≥3 indicates high risk for OSA", "difficulty": "intermediate"},
        {"category": "Clinical Presentation", "question": "This witnessed event during sleep is highly specific for OSA", "answer": "What is observed apnea (breathing pauses)?", "rationale": "Bed partner reporting apneas strongly suggests OSA", "difficulty": "intermediate"},

        # Diagnosis
        {"category": "Diagnosis", "question": "This test is gold standard for diagnosing OSA", "answer": "What is polysomnography (PSG/sleep study)?", "rationale": "In-lab PSG monitors EEG, EOG, EMG, airflow, effort, oximetry, ECG", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This index defines OSA severity (events per hour of sleep)", "answer": "What is AHI (Apnea-Hypopnea Index)?", "rationale": "Mild: 5-14, Moderate: 15-29, Severe: ≥30 events/hr", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This home-based test is acceptable for diagnosing moderate-to-severe OSA", "answer": "What is home sleep apnea test (HSAT)?", "rationale": "HSAT adequate for high pretest probability; may underestimate AHI", "difficulty": "intermediate"},
        {"category": "Diagnosis", "question": "This AHI threshold diagnoses moderate OSA", "answer": "What is AHI 15-29/hr?", "rationale": "Mild 5-14, Moderate 15-29, Severe ≥30", "difficulty": "basic"},
        {"category": "Diagnosis", "question": "This oxygen saturation nadir during sleep indicates severe OSA", "answer": "What is SpO2 <80% (or T90 >10%)?", "rationale": "Severe desaturation and time <90% indicate significant hypoxemia", "difficulty": "intermediate"},

        # CPAP Therapy
        {"category": "CPAP Therapy", "question": "This treatment is first-line for moderate-to-severe OSA", "answer": "What is CPAP (Continuous Positive Airway Pressure)?", "rationale": "CPAP splints airway open; most effective treatment", "difficulty": "basic"},
        {"category": "CPAP Therapy", "question": "This compliance threshold defines adequate CPAP use", "answer": "What is ≥4 hours/night for ≥70% of nights?", "rationale": "Medicare definition of compliance for continued coverage", "difficulty": "intermediate"},
        {"category": "CPAP Therapy", "question": "This CPAP variant adjusts pressure automatically based on airflow", "answer": "What is APAP (Auto-titrating PAP)?", "rationale": "APAP adjusts 4-20 cmH2O; eliminates titration study need", "difficulty": "intermediate"},
        {"category": "CPAP Therapy", "question": "This CPAP interface covers both nose and mouth", "answer": "What is a full-face mask?", "rationale": "Full-face masks for mouth breathers; nasal preferred if tolerated", "difficulty": "basic"},
        {"category": "CPAP Therapy", "question": "This bilevel PAP feature aids patients with high pressure requirements", "answer": "What is BPAP (Bilevel PAP)?", "rationale": "BPAP has separate inspiratory and expiratory pressures", "difficulty": "intermediate"},

        # Alternative Treatments
        {"category": "Alternative Treatments", "question": "This oral appliance advances the jaw to treat OSA", "answer": "What is a mandibular advancement device (MAD)?", "rationale": "MAD effective for mild-moderate OSA; fitted by dentist", "difficulty": "intermediate"},
        {"category": "Alternative Treatments", "question": "This surgical procedure advances the jaw bone to enlarge airway", "answer": "What is maxillomandibular advancement (MMA)?", "rationale": "MMA most effective surgery for OSA; reserved for severe cases", "difficulty": "advanced"},
        {"category": "Alternative Treatments", "question": "This pediatric surgery is first-line for OSA", "answer": "What is adenotonsillectomy?", "rationale": "T&A effective in most pediatric OSA cases", "difficulty": "basic"},
        {"category": "Alternative Treatments", "question": "This nerve stimulator treats OSA by preventing tongue collapse", "answer": "What is hypoglossal nerve stimulation (Inspire)?", "rationale": "Inspire implant for CPAP-intolerant moderate-severe OSA", "difficulty": "intermediate"},
        {"category": "Alternative Treatments", "question": "This weight loss intervention can cure OSA in obese patients", "answer": "What is bariatric surgery?", "rationale": "Significant weight loss can resolve OSA; GLP-1 agonists also help", "difficulty": "intermediate"},

        # Comorbidities
        {"category": "Comorbidities", "question": "This cardiovascular condition is strongly associated with OSA", "answer": "What is hypertension (or atrial fibrillation)?", "rationale": "OSA causes resistant hypertension; CPAP may improve BP", "difficulty": "basic"},
        {"category": "Comorbidities", "question": "This metabolic condition is both cause and consequence of OSA", "answer": "What is obesity (or type 2 diabetes)?", "rationale": "Bidirectional relationship between OSA and metabolic disease", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This cardiac rhythm is common in severe untreated OSA", "answer": "What is atrial fibrillation?", "rationale": "OSA increases AF risk; CPAP may reduce AF recurrence", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This pulmonary condition can coexist with OSA (overlap syndrome)", "answer": "What is COPD?", "rationale": "Overlap syndrome has worse outcomes; needs CPAP + supplemental O2", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This cognitive/mood condition improves with OSA treatment", "answer": "What is depression (or cognitive impairment)?", "rationale": "Sleep fragmentation affects mood and cognition; CPAP helps", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "Sleep Apnea Milestones",
        "question": "This 1981 introduction of nasal continuous positive airway pressure by Colin Sullivan revolutionized treatment of this condition",
        "answer": "What is obstructive sleep apnea?",
        "rationale": "CPAP remains the gold standard treatment 40+ years later"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Screen and diagnose obstructive sleep apnea",
        "Initiate and optimize CPAP therapy",
        "Identify candidates for alternative treatments",
        "Recognize and manage OSA-related comorbidities"
    ]
)
register_game(SLEEP_APNEA_GAME)
