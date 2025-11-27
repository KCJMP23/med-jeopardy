"""
Oncology Condition Games

Includes: DLBCL, Solid Tumors (general principles)
Note: Breast Cancer and Multiple Myeloma are in __init__.py
"""

from jparty.condition_games import ConditionGame, register_game


DLBCL_GAME = ConditionGame(
    condition_id="dlbcl",
    condition_name="Diffuse Large B-Cell Lymphoma (DLBCL)",
    therapeutic_area="Oncology/Hematology",
    description="Comprehensive review of DLBCL classification, treatment, and management",
    categories=[
        "Pathophysiology & Classification",
        "Diagnosis & Staging",
        "First-Line Therapy",
        "Relapsed/Refractory Disease",
        "CAR-T & Novel Therapies",
        "Special Populations"
    ],
    questions=[
        # Pathophysiology & Classification
        {"category": "Pathophysiology & Classification", "question": "This cell of origin subtype is associated with better prognosis", "answer": "What is germinal center B-cell (GCB) subtype?", "rationale": "GCB-DLBCL has better outcomes than ABC/non-GCB subtype", "difficulty": "intermediate"},
        {"category": "Pathophysiology & Classification", "question": "This immunohistochemistry algorithm classifies DLBCL cell of origin", "answer": "What is the Hans algorithm?", "rationale": "Hans algorithm uses CD10, BCL6, MUM1 to classify GCB vs non-GCB", "difficulty": "intermediate"},
        {"category": "Pathophysiology & Classification", "question": "This MYC rearrangement with BCL2 or BCL6 defines high-grade B-cell lymphoma", "answer": "What is double-hit lymphoma?", "rationale": "Double-hit (MYC + BCL2/BCL6) has aggressive course and poor prognosis", "difficulty": "advanced"},
        {"category": "Pathophysiology & Classification", "question": "This mutation is associated with ABC-subtype and poor prognosis", "answer": "What is MYD88 mutation?", "rationale": "MYD88 mutations activate NF-κB pathway in ABC-DLBCL", "difficulty": "advanced"},
        {"category": "Pathophysiology & Classification", "question": "This marker expressed on all B-cell lymphomas is targeted by rituximab", "answer": "What is CD20?", "rationale": "CD20 is uniformly expressed on mature B-cells", "difficulty": "basic"},

        # Diagnosis & Staging
        {"category": "Diagnosis & Staging", "question": "This imaging modality is standard for DLBCL staging", "answer": "What is PET/CT?", "rationale": "PET/CT is required for initial staging and response assessment", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This prognostic index uses age, LDH, ECOG, stage, and extranodal sites", "answer": "What is IPI (International Prognostic Index)?", "rationale": "IPI stratifies DLBCL into risk groups", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This biopsy type is required for diagnosis (not aspiration alone)", "answer": "What is excisional or core needle biopsy?", "rationale": "Adequate tissue needed for architecture and immunohistochemistry", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This FISH test should be performed to identify high-grade lymphoma", "answer": "What is MYC, BCL2, and BCL6 FISH?", "rationale": "FISH identifies translocations for double/triple-hit classification", "difficulty": "intermediate"},
        {"category": "Diagnosis & Staging", "question": "This Deauville score on PET indicates complete metabolic response", "answer": "What is Deauville 1-3?", "rationale": "Deauville 1-3 at end of treatment indicates CMR", "difficulty": "intermediate"},

        # First-Line Therapy
        {"category": "First-Line Therapy", "question": "This standard chemoimmunotherapy regimen is first-line for DLBCL", "answer": "What is R-CHOP?", "rationale": "Rituximab + cyclophosphamide, doxorubicin, vincristine, prednisone", "difficulty": "basic"},
        {"category": "First-Line Therapy", "question": "This number of R-CHOP cycles is standard for most DLBCL patients", "answer": "What is 6 cycles?", "rationale": "6 cycles standard; may use 4 for limited stage with RT", "difficulty": "basic"},
        {"category": "First-Line Therapy", "question": "This CD79b-targeting antibody-drug conjugate is added to R-CHP for first-line therapy", "answer": "What is polatuzumab vedotin?", "rationale": "Pola-R-CHP replaced vincristine in POLARIX trial", "difficulty": "intermediate"},
        {"category": "First-Line Therapy", "question": "This prophylaxis is considered for high-risk patients due to CNS relapse", "answer": "What is intrathecal or high-dose methotrexate?", "rationale": "CNS prophylaxis for high CNS-IPI or specific high-risk features", "difficulty": "intermediate"},
        {"category": "First-Line Therapy", "question": "This trial established Pola-R-CHP superiority in first-line DLBCL", "answer": "What is POLARIX?", "rationale": "POLARIX showed improved PFS with Pola-R-CHP vs R-CHOP", "difficulty": "advanced"},

        # Relapsed/Refractory Disease
        {"category": "Relapsed/Refractory Disease", "question": "This salvage strategy involves high-dose chemotherapy and stem cell rescue", "answer": "What is autologous stem cell transplant (ASCT)?", "rationale": "ASCT is standard for transplant-eligible relapsed DLBCL", "difficulty": "basic"},
        {"category": "Relapsed/Refractory Disease", "question": "This salvage chemotherapy regimen is commonly used before ASCT", "answer": "What is R-ICE (or R-DHAP, R-GDP)?", "rationale": "R-ICE: rituximab, ifosfamide, carboplatin, etoposide", "difficulty": "intermediate"},
        {"category": "Relapsed/Refractory Disease", "question": "This bispecific antibody targets CD20 and CD3", "answer": "What is glofitamab (or epcoritamab, mosunetuzumab)?", "rationale": "CD20xCD3 bispecifics redirect T-cells to kill lymphoma", "difficulty": "intermediate"},
        {"category": "Relapsed/Refractory Disease", "question": "This oral BTK inhibitor is used in relapsed/refractory DLBCL", "answer": "What is ibrutinib?", "rationale": "BTK inhibitors have modest activity; best in ABC subtype", "difficulty": "intermediate"},
        {"category": "Relapsed/Refractory Disease", "question": "This ADC targeting CD79b is approved for relapsed DLBCL", "answer": "What is polatuzumab vedotin (with bendamustine/rituximab)?", "rationale": "Pola-BR approved for R/R DLBCL not eligible for ASCT", "difficulty": "advanced"},

        # CAR-T & Novel Therapies
        {"category": "CAR-T & Novel Therapies", "question": "This CAR-T therapy targeting CD19 was first approved for DLBCL", "answer": "What is axicabtagene ciloleucel (axi-cel/Yescarta)?", "rationale": "Axi-cel approved 2017 based on ZUMA-1 trial", "difficulty": "intermediate"},
        {"category": "CAR-T & Novel Therapies", "question": "This serious CAR-T toxicity involves neurological symptoms", "answer": "What is ICANS (Immune effector Cell-Associated Neurotoxicity Syndrome)?", "rationale": "ICANS can cause confusion, aphasia, seizures, cerebral edema", "difficulty": "intermediate"},
        {"category": "CAR-T & Novel Therapies", "question": "This cytokine storm syndrome is common after CAR-T infusion", "answer": "What is CRS (Cytokine Release Syndrome)?", "rationale": "CRS treated with tocilizumab and supportive care", "difficulty": "basic"},
        {"category": "CAR-T & Novel Therapies", "question": "This line of therapy now includes CAR-T as second-line for high-risk patients", "answer": "What is second-line (before ASCT)?", "rationale": "ZUMA-7 and TRANSFORM showed CAR-T superior to ASCT in 2nd line", "difficulty": "advanced"},
        {"category": "CAR-T & Novel Therapies", "question": "This IL-6 receptor antibody treats cytokine release syndrome", "answer": "What is tocilizumab (Actemra)?", "rationale": "Tocilizumab is first-line CRS treatment", "difficulty": "intermediate"},

        # Special Populations
        {"category": "Special Populations", "question": "This modified regimen is used for elderly or frail DLBCL patients", "answer": "What is R-miniCHOP (or R-CEOP)?", "rationale": "Dose-reduced regimens for patients unable to tolerate full R-CHOP", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This cardiac concern limits anthracycline use in some patients", "answer": "What is cardiotoxicity/low ejection fraction?", "rationale": "LVEF monitoring required; etoposide can substitute for doxorubicin", "difficulty": "basic"},
        {"category": "Special Populations", "question": "This site of involvement defines primary CNS lymphoma", "answer": "What is isolated CNS involvement?", "rationale": "PCNSL has different treatment approach (high-dose MTX-based)", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This transformed lymphoma arises from follicular lymphoma", "answer": "What is transformed DLBCL (tFL)?", "rationale": "Transformation occurs in 2-3% of FL per year", "difficulty": "intermediate"},
        {"category": "Special Populations", "question": "This condition warrants tumor lysis syndrome prophylaxis", "answer": "What is high tumor burden/bulky disease?", "rationale": "TLS prophylaxis with hydration and allopurinol/rasburicase", "difficulty": "basic"},
    ],
    final_jeopardy={
        "category": "DLBCL Breakthroughs",
        "question": "This 2002 approval added this anti-CD20 antibody to CHOP, improving survival and establishing chemoimmunotherapy for DLBCL",
        "answer": "What is rituximab (establishing R-CHOP)?",
        "rationale": "R-CHOP became standard of care and remains so 20+ years later"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Classify DLBCL by cell of origin and identify high-risk features",
        "Select appropriate first-line therapy for DLBCL",
        "Understand the role of CAR-T therapy in relapsed disease",
        "Manage CAR-T toxicities including CRS and ICANS"
    ]
)
register_game(DLBCL_GAME)


SOLID_TUMORS_GAME = ConditionGame(
    condition_id="solid_tumors",
    condition_name="Solid Tumor Principles",
    therapeutic_area="Oncology",
    description="General principles of solid tumor management including staging, treatment modalities, and supportive care",
    categories=[
        "Staging & Principles",
        "Surgical Oncology",
        "Radiation Therapy",
        "Systemic Therapy Principles",
        "Immunotherapy",
        "Supportive Care"
    ],
    questions=[
        # Staging & Principles
        {"category": "Staging & Principles", "question": "This staging system uses T (tumor), N (nodes), and M (metastasis)", "answer": "What is TNM staging?", "rationale": "TNM is standard for most solid tumors; AJCC/UICC maintained", "difficulty": "basic"},
        {"category": "Staging & Principles", "question": "This performance status scale ranges from 0 (fully active) to 5 (dead)", "answer": "What is ECOG performance status?", "rationale": "ECOG PS guides treatment decisions and eligibility", "difficulty": "basic"},
        {"category": "Staging & Principles", "question": "This term describes cancer spread to regional lymph nodes", "answer": "What is locally advanced (N+) disease?", "rationale": "Nodal involvement often upstages disease and changes treatment", "difficulty": "basic"},
        {"category": "Staging & Principles", "question": "This treatment approach combines multiple modalities (surgery, chemo, RT)", "answer": "What is multimodal therapy?", "rationale": "Multimodal approach standard for many locally advanced cancers", "difficulty": "intermediate"},
        {"category": "Staging & Principles", "question": "This molecular feature is increasingly used for treatment selection", "answer": "What is tumor genomic profiling (NGS)?", "rationale": "NGS identifies actionable mutations and guides targeted therapy", "difficulty": "intermediate"},

        # Surgical Oncology
        {"category": "Surgical Oncology", "question": "This margin status indicates no tumor at the resection edge", "answer": "What is R0 (negative margins)?", "rationale": "R0 resection is goal; R1 (microscopic) and R2 (gross) residual worsen outcomes", "difficulty": "basic"},
        {"category": "Surgical Oncology", "question": "This procedure removes the primary tumor with surrounding tissue", "answer": "What is wide local excision?", "rationale": "Adequate margins depend on tumor type and location", "difficulty": "basic"},
        {"category": "Surgical Oncology", "question": "This staging procedure identifies the first draining lymph node", "answer": "What is sentinel lymph node biopsy?", "rationale": "SLNB minimizes morbidity vs complete lymphadenectomy", "difficulty": "intermediate"},
        {"category": "Surgical Oncology", "question": "This palliative surgery relieves obstruction without curative intent", "answer": "What is bypass surgery (or stenting)?", "rationale": "Palliative surgery improves quality of life in metastatic disease", "difficulty": "intermediate"},
        {"category": "Surgical Oncology", "question": "This approach removes metastases from a single organ with curative intent", "answer": "What is metastasectomy (oligometastatic disease)?", "rationale": "Selected patients with limited metastases may achieve long-term survival", "difficulty": "advanced"},

        # Radiation Therapy
        {"category": "Radiation Therapy", "question": "This RT approach delivers high doses to the tumor while sparing normal tissue", "answer": "What is IMRT (Intensity-Modulated Radiation Therapy)?", "rationale": "IMRT allows precise dose conformity to tumor shape", "difficulty": "intermediate"},
        {"category": "Radiation Therapy", "question": "This fractionation schedule delivers fewer, higher doses per treatment", "answer": "What is hypofractionation (or SBRT)?", "rationale": "SBRT delivers ablative doses in 1-5 fractions", "difficulty": "intermediate"},
        {"category": "Radiation Therapy", "question": "This RT given before surgery is called this", "answer": "What is neoadjuvant radiation?", "rationale": "Neoadjuvant RT may downstage tumors and improve resectability", "difficulty": "basic"},
        {"category": "Radiation Therapy", "question": "This side effect of pelvic radiation affects bowel function", "answer": "What is radiation enteritis/proctitis?", "rationale": "Bowel toxicity managed with supportive care; late effects possible", "difficulty": "intermediate"},
        {"category": "Radiation Therapy", "question": "This RT technique uses protons instead of photons", "answer": "What is proton beam therapy?", "rationale": "Protons have Bragg peak allowing less exit dose to normal tissue", "difficulty": "intermediate"},

        # Systemic Therapy Principles
        {"category": "Systemic Therapy Principles", "question": "This chemotherapy timing occurs after surgery to reduce recurrence", "answer": "What is adjuvant chemotherapy?", "rationale": "Adjuvant therapy targets micrometastatic disease", "difficulty": "basic"},
        {"category": "Systemic Therapy Principles", "question": "This chemotherapy timing occurs before surgery to shrink tumor", "answer": "What is neoadjuvant chemotherapy?", "rationale": "Neoadjuvant therapy may improve resectability and test tumor sensitivity", "difficulty": "basic"},
        {"category": "Systemic Therapy Principles", "question": "This targeted therapy class inhibits tyrosine kinases", "answer": "What are TKIs (Tyrosine Kinase Inhibitors)?", "rationale": "TKIs target specific oncogenic pathways (EGFR, ALK, etc.)", "difficulty": "intermediate"},
        {"category": "Systemic Therapy Principles", "question": "This mutation predicts response to EGFR TKIs in lung cancer", "answer": "What is EGFR activating mutation (exon 19 del, L858R)?", "rationale": "EGFR-mutant NSCLC treated with osimertinib first-line", "difficulty": "intermediate"},
        {"category": "Systemic Therapy Principles", "question": "This biomarker predicts response to HER2-targeted therapy", "answer": "What is HER2 amplification (IHC 3+ or FISH+)?", "rationale": "HER2+ breast and gastric cancers benefit from anti-HER2 therapy", "difficulty": "intermediate"},

        # Immunotherapy
        {"category": "Immunotherapy", "question": "This checkpoint inhibitor target is blocked by pembrolizumab", "answer": "What is PD-1?", "rationale": "Anti-PD-1 antibodies restore T-cell anti-tumor activity", "difficulty": "basic"},
        {"category": "Immunotherapy", "question": "This biomarker predicts immunotherapy response in many tumor types", "answer": "What is PD-L1 expression (or TMB, MSI)?", "rationale": "PD-L1 TPS or CPS guides pembrolizumab use in several tumors", "difficulty": "intermediate"},
        {"category": "Immunotherapy", "question": "This microsatellite status predicts immunotherapy response", "answer": "What is MSI-high (microsatellite instability-high)?", "rationale": "MSI-H/dMMR tumors respond to pembrolizumab regardless of histology", "difficulty": "intermediate"},
        {"category": "Immunotherapy", "question": "This immune-related adverse event affects the thyroid", "answer": "What is thyroiditis (hypo- or hyperthyroidism)?", "rationale": "Thyroid irAEs common; monitor TSH regularly", "difficulty": "intermediate"},
        {"category": "Immunotherapy", "question": "This CTLA-4 inhibitor was first checkpoint inhibitor approved (melanoma)", "answer": "What is ipilimumab (Yervoy)?", "rationale": "Ipilimumab approved 2011; often combined with anti-PD-1", "difficulty": "intermediate"},

        # Supportive Care
        {"category": "Supportive Care", "question": "This growth factor prevents chemotherapy-induced neutropenia", "answer": "What is G-CSF (filgrastim/pegfilgrastim)?", "rationale": "G-CSF given after chemo to reduce febrile neutropenia risk", "difficulty": "basic"},
        {"category": "Supportive Care", "question": "This class of antiemetics blocks the NK1 receptor", "answer": "What are NK1 receptor antagonists (aprepitant)?", "rationale": "NK1 RAs added to 5-HT3 + dex for highly emetogenic chemo", "difficulty": "intermediate"},
        {"category": "Supportive Care", "question": "This bisphosphonate prevents skeletal events in bone metastases", "answer": "What is zoledronic acid (or denosumab)?", "rationale": "Bone-modifying agents reduce pathologic fractures and SREs", "difficulty": "intermediate"},
        {"category": "Supportive Care", "question": "This syndrome causes severe diarrhea with irinotecan", "answer": "What is cholinergic syndrome (early) or delayed diarrhea?", "rationale": "Atropine for early; loperamide for late diarrhea", "difficulty": "intermediate"},
        {"category": "Supportive Care", "question": "This palliative care consult timing improves quality of life in advanced cancer", "answer": "What is early (at diagnosis of advanced disease)?", "rationale": "Early palliative care integration improves outcomes", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "Oncology Milestones",
        "question": "This 2011 FDA approval of ipilimumab for melanoma ushered in the modern era of this treatment approach",
        "answer": "What is cancer immunotherapy (checkpoint inhibition)?",
        "rationale": "Ipilimumab was first checkpoint inhibitor; now used across cancer types"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Apply TNM staging principles to solid tumors",
        "Understand multimodal treatment approaches",
        "Select appropriate systemic therapy based on molecular markers",
        "Manage common toxicities of cancer treatment"
    ]
)
register_game(SOLID_TUMORS_GAME)
