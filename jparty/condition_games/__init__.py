"""
Condition-Specific Medical Jeopardy Games

Pre-populated game templates for medical education covering common
diseases and therapeutic areas. Each game includes:
- 6 categories related to the condition
- 30 questions (5 per category) with increasing difficulty
- Answers, rationales, and difficulty levels
- Specialty and system tagging

Usage:
    from jparty.condition_games import get_condition_game, list_conditions

    # List all available conditions
    conditions = list_conditions()

    # Load a specific condition game
    game_data = get_condition_game("heart_failure")
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from jparty.game import Question, Board, FinalBoard, GameData
import logging


@dataclass
class ConditionGame:
    """A pre-built condition-specific game."""
    condition_id: str
    condition_name: str
    therapeutic_area: str
    description: str
    categories: List[str]
    questions: List[Dict]
    final_jeopardy: Dict
    difficulty_distribution: str  # "beginner", "intermediate", "advanced", "mixed"
    target_audience: str  # "students", "residents", "fellows", "attendings", "all"
    estimated_duration: int  # minutes
    cme_objectives: List[str]


# Registry of all condition games
CONDITION_GAMES: Dict[str, ConditionGame] = {}


def register_game(game: ConditionGame):
    """Register a condition game in the library."""
    CONDITION_GAMES[game.condition_id] = game


def list_conditions() -> List[Dict]:
    """List all available condition games."""
    return [
        {
            "id": g.condition_id,
            "name": g.condition_name,
            "area": g.therapeutic_area,
            "description": g.description,
            "audience": g.target_audience,
            "duration": g.estimated_duration
        }
        for g in CONDITION_GAMES.values()
    ]


def list_conditions_by_area(therapeutic_area: str) -> List[Dict]:
    """List condition games by therapeutic area."""
    return [
        {
            "id": g.condition_id,
            "name": g.condition_name,
            "description": g.description
        }
        for g in CONDITION_GAMES.values()
        if g.therapeutic_area.lower() == therapeutic_area.lower()
    ]


def get_condition_game(condition_id: str) -> Optional[GameData]:
    """
    Get a condition-specific game as GameData.

    Args:
        condition_id: The condition identifier (e.g., "heart_failure")

    Returns:
        GameData object ready for use in the game
    """
    if condition_id not in CONDITION_GAMES:
        return None

    cg = CONDITION_GAMES[condition_id]
    return _build_game_data(cg)


def _build_game_data(cg: ConditionGame) -> GameData:
    """Convert a ConditionGame to GameData format."""
    boards = []

    # Build Round 1 (all 6 categories)
    r1_categories = cg.categories[:6]
    r1_questions = []
    values = [100, 200, 300, 400, 500]

    for col, cat in enumerate(r1_categories):
        cat_questions = [q for q in cg.questions if q.get("category") == cat]
        if not cat_questions:
            logging.warning(f"Category '{cat}' has no questions in {cg.condition_name} game - skipping")
            continue
        for row, val in enumerate(values):
            if row < len(cat_questions):
                q = cat_questions[row]
                r1_questions.append(Question(
                    index=(col, row),
                    text=q.get("question", ""),
                    answer=q.get("answer", ""),
                    category=cat,
                    value=val,
                    dd=(row == 2 and col == 0),  # Daily double
                    rationale=q.get("rationale"),
                    difficulty=q.get("difficulty", "intermediate"),
                    specialty=q.get("specialty", cg.therapeutic_area),
                    question_type=q.get("type", "standard")
                ))

    boards.append(Board(r1_categories, r1_questions, dj=False))

    # Build Round 2 (Double Jeopardy - same categories, harder questions or repeat)
    r2_questions = []
    values_dj = [200, 400, 600, 800, 1000]

    for col, cat in enumerate(r1_categories):
        cat_questions = [q for q in cg.questions if q.get("category") == cat]
        if not cat_questions:
            # Already warned in Round 1, skip silently here
            continue
        for row, val in enumerate(values_dj):
            # Use questions 5-9 if available, otherwise wrap around
            q_idx = row + 5 if row + 5 < len(cat_questions) else row % len(cat_questions)
            q = cat_questions[q_idx]
            r2_questions.append(Question(
                index=(col, row),
                text=q.get("question", ""),
                answer=q.get("answer", ""),
                category=cat,
                value=val,
                dd=(row == 3 and col == 2),
                rationale=q.get("rationale"),
                difficulty=q.get("difficulty", "advanced"),
                specialty=q.get("specialty", cg.therapeutic_area),
                question_type=q.get("type", "standard")
            ))

    boards.append(Board(r1_categories, r2_questions, dj=True))

    # Build Final Jeopardy
    fj = cg.final_jeopardy
    fj_question = Question(
        index=(0, 0),
        text=fj.get("question", ""),
        answer=fj.get("answer", ""),
        category=fj.get("category", cg.condition_name),
        rationale=fj.get("rationale"),
        difficulty="expert",
        specialty=cg.therapeutic_area
    )
    boards.append(FinalBoard(fj.get("category", cg.condition_name), fj_question))

    return GameData(
        rounds=boards,
        date=f"Medical Education: {cg.condition_name}",
        comments=cg.description
    )


# =============================================================================
# THERAPEUTIC AREA: CARDIOVASCULAR
# =============================================================================

HEART_FAILURE_GAME = ConditionGame(
    condition_id="heart_failure",
    condition_name="Heart Failure",
    therapeutic_area="Cardiovascular",
    description="Comprehensive review of heart failure pathophysiology, diagnosis, and management",
    categories=[
        "HF Pathophysiology",
        "Diagnosis & Staging",
        "Pharmacotherapy",
        "Device Therapy",
        "Comorbidities",
        "Emerging Therapies"
    ],
    questions=[
        # HF Pathophysiology
        {"category": "HF Pathophysiology", "question": "This neurohormonal system is chronically activated in heart failure, leading to sodium retention and vasoconstriction", "answer": "What is the renin-angiotensin-aldosterone system (RAAS)?", "rationale": "RAAS activation is a key compensatory mechanism that becomes maladaptive in chronic HF", "difficulty": "basic"},
        {"category": "HF Pathophysiology", "question": "This type of heart failure is characterized by an LVEF ≥50% with evidence of diastolic dysfunction", "answer": "What is HFpEF (Heart Failure with Preserved Ejection Fraction)?", "rationale": "HFpEF accounts for ~50% of HF cases and is more common in elderly, women, and those with HTN", "difficulty": "basic"},
        {"category": "HF Pathophysiology", "question": "This natriuretic peptide is released from ventricular myocytes in response to wall stress", "answer": "What is BNP (B-type Natriuretic Peptide)?", "rationale": "BNP and NT-proBNP are key biomarkers for diagnosis and prognosis in HF", "difficulty": "intermediate"},
        {"category": "HF Pathophysiology", "question": "This phenomenon describes the heart's inability to increase stroke volume in response to increased preload", "answer": "What is a flattened Frank-Starling curve?", "rationale": "In HF, the Frank-Starling mechanism is impaired, limiting cardiac reserve", "difficulty": "advanced"},
        {"category": "HF Pathophysiology", "question": "This cellular process involving calcium handling is impaired in systolic heart failure", "answer": "What is excitation-contraction coupling?", "rationale": "Abnormal SERCA2a function and calcium cycling contribute to contractile dysfunction", "difficulty": "expert"},

        # Diagnosis & Staging
        {"category": "Diagnosis & Staging", "question": "This ACC/AHA stage describes patients with structural heart disease but no symptoms of HF", "answer": "What is Stage B?", "rationale": "Stage B represents asymptomatic structural heart disease - an opportunity for prevention", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This NYHA class describes patients comfortable at rest but symptomatic with ordinary physical activity", "answer": "What is NYHA Class II?", "rationale": "NYHA Class II represents mild limitation of physical activity", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This echocardiographic finding suggests elevated left atrial pressure in HFpEF", "answer": "What is E/e' ratio >14?", "rationale": "Elevated E/e' ratio indicates elevated LV filling pressures", "difficulty": "intermediate"},
        {"category": "Diagnosis & Staging", "question": "This BNP cutoff helps rule out acute heart failure in the emergency setting", "answer": "What is BNP <100 pg/mL (or NT-proBNP <300 pg/mL)?", "rationale": "Low natriuretic peptide levels have high negative predictive value for acute HF", "difficulty": "intermediate"},
        {"category": "Diagnosis & Staging", "question": "This invasive measurement confirms HFpEF when PCWP is elevated at rest or with exercise", "answer": "What is right heart catheterization?", "rationale": "RHC remains gold standard for hemodynamic assessment; PCWP ≥15 mmHg at rest confirms HF", "difficulty": "advanced"},

        # Pharmacotherapy
        {"category": "Pharmacotherapy", "question": "These four drug classes comprise guideline-directed medical therapy (GDMT) for HFrEF", "answer": "What are beta-blockers, ACEi/ARB/ARNI, MRAs, and SGLT2 inhibitors?", "rationale": "The 'four pillars' of HFrEF therapy have mortality benefit", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This ARNI combines valsartan with a neprilysin inhibitor", "answer": "What is sacubitril/valsartan (Entresto)?", "rationale": "PARADIGM-HF showed 20% mortality reduction vs. enalapril", "difficulty": "basic"},
        {"category": "Pharmacotherapy", "question": "This SGLT2 inhibitor was first to show HF benefit in DAPA-HF trial", "answer": "What is dapagliflozin?", "rationale": "DAPA-HF showed benefit regardless of diabetes status", "difficulty": "intermediate"},
        {"category": "Pharmacotherapy", "question": "This diuretic resistance strategy involves adding a thiazide to a loop diuretic", "answer": "What is sequential nephron blockade?", "rationale": "Metolazone or chlorothiazide can overcome loop diuretic resistance", "difficulty": "advanced"},
        {"category": "Pharmacotherapy", "question": "This soluble guanylate cyclase stimulator is approved for worsening chronic HF", "answer": "What is vericiguat (Verquvo)?", "rationale": "VICTORIA trial showed benefit in high-risk HF patients", "difficulty": "expert"},

        # Device Therapy
        {"category": "Device Therapy", "question": "This device is indicated for primary prevention of SCD in HFrEF with LVEF ≤35%", "answer": "What is an ICD (Implantable Cardioverter-Defibrillator)?", "rationale": "ICDs reduce sudden cardiac death in appropriately selected HFrEF patients", "difficulty": "basic"},
        {"category": "Device Therapy", "question": "This QRS duration threshold is required for CRT eligibility in sinus rhythm", "answer": "What is ≥150 ms (LBBB) or ≥150 ms (non-LBBB)?", "rationale": "Wider QRS and LBBB morphology predict better CRT response", "difficulty": "intermediate"},
        {"category": "Device Therapy", "question": "This percutaneous device reduces mitral regurgitation by clipping leaflets together", "answer": "What is MitraClip?", "rationale": "COAPT trial showed benefit in secondary MR with HF", "difficulty": "intermediate"},
        {"category": "Device Therapy", "question": "This mechanical circulatory support device provides continuous axial flow", "answer": "What is an LVAD (Left Ventricular Assist Device)?", "rationale": "HeartMate 3 is current preferred LVAD with improved outcomes", "difficulty": "advanced"},
        {"category": "Device Therapy", "question": "This implantable pressure sensor allows remote monitoring of pulmonary artery pressures", "answer": "What is CardioMEMS?", "rationale": "CHAMPION trial showed reduced HF hospitalizations with PA pressure-guided management", "difficulty": "advanced"},

        # Comorbidities
        {"category": "Comorbidities", "question": "This common HF comorbidity is associated with central sleep apnea", "answer": "What is Cheyne-Stokes respiration?", "rationale": "Sleep-disordered breathing affects >50% of HF patients", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This iron study threshold indicates iron deficiency warranting IV iron in HF", "answer": "What is ferritin <100 or ferritin 100-300 with TSAT <20%?", "rationale": "IV iron improves symptoms and exercise capacity in iron-deficient HF", "difficulty": "intermediate"},
        {"category": "Comorbidities", "question": "This arrhythmia is both a cause and consequence of heart failure", "answer": "What is atrial fibrillation?", "rationale": "AF occurs in 30-40% of HF patients and worsens outcomes", "difficulty": "basic"},
        {"category": "Comorbidities", "question": "This renal complication of aggressive diuresis is called cardiorenal syndrome type 1", "answer": "What is acute kidney injury in acute decompensated HF?", "rationale": "Worsening renal function occurs in 25-30% of ADHF admissions", "difficulty": "advanced"},
        {"category": "Comorbidities", "question": "This GLP-1 receptor agonist showed cardiovascular benefit including HF reduction", "answer": "What is semaglutide?", "rationale": "SELECT trial showed CV benefit in obese patients without diabetes", "difficulty": "advanced"},

        # Emerging Therapies
        {"category": "Emerging Therapies", "question": "This cardiac myosin activator showed benefit in HFrEF in GALACTIC-HF", "answer": "What is omecamtiv mecarbil?", "rationale": "First-in-class therapy that directly improves cardiac contractility", "difficulty": "advanced"},
        {"category": "Emerging Therapies", "question": "This gene therapy approach targets SERCA2a to improve calcium handling", "answer": "What is AAV1/SERCA2a gene therapy?", "rationale": "Early trials showed promise but CUPID-2 did not meet endpoints", "difficulty": "expert"},
        {"category": "Emerging Therapies", "question": "This non-coding RNA has emerged as a therapeutic target in cardiac remodeling", "answer": "What are microRNAs (miRNAs)?", "rationale": "miRNA-based therapies are in early development for HF", "difficulty": "expert"},
        {"category": "Emerging Therapies", "question": "This anti-inflammatory approach targeting IL-1 showed promise in HF", "answer": "What is anakinra (IL-1 receptor antagonist)?", "rationale": "REDHART and other trials explore inflammation as HF target", "difficulty": "expert"},
        {"category": "Emerging Therapies", "question": "This stem cell type is being studied for cardiac regeneration in HF", "answer": "What are mesenchymal stem cells (MSCs)?", "rationale": "Cell therapy trials continue with mixed results", "difficulty": "expert"},
    ],
    final_jeopardy={
        "category": "HF Landmark Trials",
        "question": "This 1999 trial established beta-blockers as standard of care in HFrEF, showing 34% mortality reduction with carvedilol",
        "answer": "What is COPERNICUS?",
        "rationale": "COPERNICUS, along with MERIT-HF and CIBIS-II, established beta-blockers in HF"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Review heart failure pathophysiology and classification",
        "Identify guideline-directed medical therapy for HFrEF",
        "Understand device therapy indications in heart failure",
        "Recognize and manage common HF comorbidities"
    ]
)
register_game(HEART_FAILURE_GAME)


# =============================================================================
# THERAPEUTIC AREA: ONCOLOGY
# =============================================================================

BREAST_CANCER_GAME = ConditionGame(
    condition_id="breast_cancer",
    condition_name="Breast Cancer",
    therapeutic_area="Oncology",
    description="Comprehensive review of breast cancer biology, staging, and treatment",
    categories=[
        "Molecular Subtypes",
        "Staging & Diagnosis",
        "Endocrine Therapy",
        "HER2-Targeted Therapy",
        "Chemotherapy",
        "Emerging Treatments"
    ],
    questions=[
        # Molecular Subtypes
        {"category": "Molecular Subtypes", "question": "This breast cancer subtype is ER+, PR+, HER2-, and has the best prognosis", "answer": "What is Luminal A?", "rationale": "Luminal A tumors are hormone-responsive with low proliferation (Ki-67 <14%)", "difficulty": "basic"},
        {"category": "Molecular Subtypes", "question": "This molecular subtype lacks ER, PR, and HER2 expression", "answer": "What is triple-negative breast cancer (TNBC)?", "rationale": "TNBC represents 15-20% of breast cancers with aggressive behavior", "difficulty": "basic"},
        {"category": "Molecular Subtypes", "question": "This proliferation marker helps distinguish Luminal A from Luminal B", "answer": "What is Ki-67?", "rationale": "Ki-67 >14-20% suggests Luminal B with higher recurrence risk", "difficulty": "intermediate"},
        {"category": "Molecular Subtypes", "question": "This genomic assay provides a recurrence score for ER+ early breast cancer", "answer": "What is Oncotype DX?", "rationale": "21-gene assay guides chemotherapy decisions in node-negative ER+ disease", "difficulty": "intermediate"},
        {"category": "Molecular Subtypes", "question": "This BRCA1-associated breast cancer often shows this molecular subtype", "answer": "What is basal-like/triple-negative?", "rationale": "BRCA1 mutations strongly associated with TNBC phenotype", "difficulty": "advanced"},

        # Staging & Diagnosis
        {"category": "Staging & Diagnosis", "question": "This imaging modality is standard for breast cancer screening", "answer": "What is mammography?", "rationale": "Annual mammography recommended starting age 40-50 depending on guidelines", "difficulty": "basic"},
        {"category": "Staging & Diagnosis", "question": "This biopsy technique is preferred for suspicious breast lesions", "answer": "What is core needle biopsy?", "rationale": "Core biopsy provides tissue architecture for complete diagnosis", "difficulty": "basic"},
        {"category": "Staging & Diagnosis", "question": "This staging procedure evaluates axillary nodes while minimizing morbidity", "answer": "What is sentinel lymph node biopsy?", "rationale": "SLNB has replaced routine axillary dissection for clinically negative nodes", "difficulty": "intermediate"},
        {"category": "Staging & Diagnosis", "question": "This TNM stage describes a 3cm tumor with ipsilateral movable axillary nodes", "answer": "What is Stage IIB (T2N1)?", "rationale": "T2 (2-5cm) + N1 (movable ipsilateral nodes) = Stage IIB", "difficulty": "intermediate"},
        {"category": "Staging & Diagnosis", "question": "This imaging is recommended for staging in locally advanced breast cancer", "answer": "What is CT chest/abdomen/pelvis and bone scan (or PET/CT)?", "rationale": "Metastatic workup indicated for stage III disease", "difficulty": "advanced"},

        # Endocrine Therapy
        {"category": "Endocrine Therapy", "question": "This selective estrogen receptor modulator is used in premenopausal breast cancer", "answer": "What is tamoxifen?", "rationale": "Tamoxifen remains standard for premenopausal ER+ breast cancer", "difficulty": "basic"},
        {"category": "Endocrine Therapy", "question": "This class of drugs inhibits estrogen synthesis in postmenopausal women", "answer": "What are aromatase inhibitors?", "rationale": "Anastrozole, letrozole, exemestane are preferred in postmenopausal patients", "difficulty": "basic"},
        {"category": "Endocrine Therapy", "question": "This CDK4/6 inhibitor is combined with AI for metastatic HR+ breast cancer", "answer": "What is palbociclib (or ribociclib, abemaciclib)?", "rationale": "CDK4/6 inhibitors doubled PFS when added to endocrine therapy", "difficulty": "intermediate"},
        {"category": "Endocrine Therapy", "question": "This duration of adjuvant endocrine therapy is now recommended for high-risk ER+ disease", "answer": "What is 10 years (extended therapy)?", "rationale": "Extended endocrine therapy reduces late recurrences in high-risk patients", "difficulty": "intermediate"},
        {"category": "Endocrine Therapy", "question": "This oral SERD has shown activity in ESR1-mutated breast cancer", "answer": "What is elacestrant (Orserdu)?", "rationale": "First oral SERD approved for ESR1-mutated ER+ metastatic BC", "difficulty": "advanced"},

        # HER2-Targeted Therapy
        {"category": "HER2-Targeted Therapy", "question": "This monoclonal antibody targeting HER2 revolutionized treatment", "answer": "What is trastuzumab (Herceptin)?", "rationale": "Trastuzumab improved survival in HER2+ breast cancer", "difficulty": "basic"},
        {"category": "HER2-Targeted Therapy", "question": "This antibody-drug conjugate combines trastuzumab with a cytotoxic payload", "answer": "What is T-DM1 (ado-trastuzumab emtansine)?", "rationale": "T-DM1 delivers chemotherapy directly to HER2+ cells", "difficulty": "intermediate"},
        {"category": "HER2-Targeted Therapy", "question": "This HER2/HER3 dimerization inhibitor is added to trastuzumab in metastatic disease", "answer": "What is pertuzumab (Perjeta)?", "rationale": "CLEOPATRA showed OS benefit adding pertuzumab to trastuzumab + docetaxel", "difficulty": "intermediate"},
        {"category": "HER2-Targeted Therapy", "question": "This tyrosine kinase inhibitor is used after progression on trastuzumab", "answer": "What is tucatinib (or lapatinib, neratinib)?", "rationale": "Tucatinib showed CNS activity in HER2CLIMB trial", "difficulty": "advanced"},
        {"category": "HER2-Targeted Therapy", "question": "This novel ADC targeting HER2 shows activity even in HER2-low tumors", "answer": "What is trastuzumab deruxtecan (Enhertu)?", "rationale": "T-DXd approved for HER2-low breast cancer based on DESTINY-Breast04", "difficulty": "advanced"},

        # Chemotherapy
        {"category": "Chemotherapy", "question": "This anthracycline is commonly used in adjuvant breast cancer regimens", "answer": "What is doxorubicin (Adriamycin)?", "rationale": "AC (doxorubicin + cyclophosphamide) is a standard regimen", "difficulty": "basic"},
        {"category": "Chemotherapy", "question": "This class of chemotherapy drugs stabilizes microtubules", "answer": "What are taxanes (paclitaxel, docetaxel)?", "rationale": "Taxanes are key components of adjuvant and metastatic regimens", "difficulty": "basic"},
        {"category": "Chemotherapy", "question": "This regimen sequence is dose-dense AC followed by paclitaxel", "answer": "What is ddAC-T?", "rationale": "Dose-dense regimens with G-CSF support improve outcomes", "difficulty": "intermediate"},
        {"category": "Chemotherapy", "question": "This platinum agent shows particular benefit in BRCA-mutated breast cancer", "answer": "What is carboplatin?", "rationale": "TNT trial showed carboplatin benefit in BRCA+ TNBC", "difficulty": "advanced"},
        {"category": "Chemotherapy", "question": "This oral chemotherapy is approved for heavily pretreated metastatic breast cancer", "answer": "What is capecitabine (or eribulin)?", "rationale": "Later-line options for metastatic disease", "difficulty": "intermediate"},

        # Emerging Treatments
        {"category": "Emerging Treatments", "question": "This PARP inhibitor is approved for BRCA-mutated HER2- breast cancer", "answer": "What is olaparib (or talazoparib)?", "rationale": "PARP inhibitors exploit synthetic lethality in BRCA deficiency", "difficulty": "intermediate"},
        {"category": "Emerging Treatments", "question": "This checkpoint inhibitor is added to chemo for PD-L1+ metastatic TNBC", "answer": "What is pembrolizumab (Keytruda)?", "rationale": "KEYNOTE-355 showed benefit in PD-L1 CPS ≥10 TNBC", "difficulty": "intermediate"},
        {"category": "Emerging Treatments", "question": "This ADC targeting Trop-2 is approved for pretreated TNBC", "answer": "What is sacituzumab govitecan (Trodelvy)?", "rationale": "ASCENT trial showed PFS and OS benefit in TNBC", "difficulty": "advanced"},
        {"category": "Emerging Treatments", "question": "This PI3K inhibitor is approved for PIK3CA-mutated HR+ breast cancer", "answer": "What is alpelisib (Piqray)?", "rationale": "SOLAR-1 showed benefit in PIK3CA-mutated tumors", "difficulty": "advanced"},
        {"category": "Emerging Treatments", "question": "This AKT inhibitor showed benefit in PIK3CA/AKT1/PTEN-altered tumors", "answer": "What is capivasertib?", "rationale": "CAPItello-291 led to recent FDA approval", "difficulty": "expert"},
    ],
    final_jeopardy={
        "category": "Breast Cancer Milestones",
        "question": "This 2005 landmark trial (HERA) established the benefit of 1 year of adjuvant trastuzumab in HER2+ early breast cancer",
        "answer": "What is HERA (HERceptin Adjuvant)?",
        "rationale": "HERA, along with concurrent trials, established adjuvant trastuzumab as standard of care"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Classify breast cancer by molecular subtype",
        "Select appropriate systemic therapy based on tumor characteristics",
        "Understand the role of targeted therapies in breast cancer",
        "Review emerging treatments including immunotherapy and ADCs"
    ]
)
register_game(BREAST_CANCER_GAME)


MULTIPLE_MYELOMA_GAME = ConditionGame(
    condition_id="multiple_myeloma",
    condition_name="Multiple Myeloma",
    therapeutic_area="Oncology",
    description="Comprehensive review of multiple myeloma diagnosis and treatment",
    categories=[
        "Pathophysiology",
        "Diagnosis & Staging",
        "Induction Therapy",
        "Transplant & Maintenance",
        "Relapsed Disease",
        "Supportive Care"
    ],
    questions=[
        # Pathophysiology
        {"category": "Pathophysiology", "question": "This immunoglobulin type is most commonly produced in myeloma", "answer": "What is IgG?", "rationale": "IgG myeloma accounts for ~50% of cases, followed by IgA", "difficulty": "basic"},
        {"category": "Pathophysiology", "question": "This bone marrow microenvironment cell type supports myeloma growth", "answer": "What are stromal cells?", "rationale": "Bone marrow stromal cells provide survival signals and drug resistance", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This cytogenetic abnormality confers high-risk status in myeloma", "answer": "What is del(17p) (or t(4;14), t(14;16))?", "rationale": "High-risk cytogenetics predict shorter survival and guide therapy", "difficulty": "intermediate"},
        {"category": "Pathophysiology", "question": "This osteoclast-activating pathway is targeted by denosumab", "answer": "What is RANKL (Receptor Activator of NF-κB Ligand)?", "rationale": "RANKL inhibition reduces skeletal-related events in myeloma", "difficulty": "advanced"},
        {"category": "Pathophysiology", "question": "This oncogene translocation partner is associated with t(11;14)", "answer": "What is CCND1 (cyclin D1)?", "rationale": "t(11;14) myeloma may respond to venetoclax", "difficulty": "advanced"},

        # More questions abbreviated for space...
        {"category": "Diagnosis & Staging", "question": "This protein found in urine represents free light chains", "answer": "What is Bence Jones protein?", "rationale": "Bence Jones proteinuria indicates light chain excretion", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This percentage of bone marrow plasma cells is required for myeloma diagnosis", "answer": "What is ≥10% (with end-organ damage) or ≥60% (alone)?", "rationale": "Updated criteria include SLiM-CRAB features", "difficulty": "intermediate"},
        {"category": "Diagnosis & Staging", "question": "The CRAB criteria include this bone-related finding", "answer": "What are lytic lesions (bone disease)?", "rationale": "CRAB: Calcium elevation, Renal insufficiency, Anemia, Bone lesions", "difficulty": "basic"},
        {"category": "Diagnosis & Staging", "question": "This imaging modality is now preferred over skeletal survey", "answer": "What is whole-body low-dose CT (or PET/CT)?", "rationale": "CT is more sensitive for lytic lesions than plain radiographs", "difficulty": "intermediate"},
        {"category": "Diagnosis & Staging", "question": "This revised staging system incorporates LDH and cytogenetics", "answer": "What is R-ISS (Revised International Staging System)?", "rationale": "R-ISS adds high-risk cytogenetics and LDH to ISS", "difficulty": "advanced"},

        {"category": "Induction Therapy", "question": "This proteasome inhibitor is a backbone of myeloma induction", "answer": "What is bortezomib (Velcade)?", "rationale": "VRd (bortezomib, lenalidomide, dexamethasone) is standard induction", "difficulty": "basic"},
        {"category": "Induction Therapy", "question": "This IMiD is combined with bortezomib in standard triplet therapy", "answer": "What is lenalidomide (Revlimid)?", "rationale": "VRd is preferred frontline regimen for transplant-eligible patients", "difficulty": "basic"},
        {"category": "Induction Therapy", "question": "This CD38 antibody is now added to VRd for quadruplet induction", "answer": "What is daratumumab (Darzalex)?", "rationale": "D-VRd showed deeper responses in GRIFFIN and PERSEUS trials", "difficulty": "intermediate"},
        {"category": "Induction Therapy", "question": "This newer proteasome inhibitor has weekly dosing and less neuropathy", "answer": "What is carfilzomib (Kyprolis)?", "rationale": "Carfilzomib is an alternative PI with different toxicity profile", "difficulty": "intermediate"},
        {"category": "Induction Therapy", "question": "This number of induction cycles is typically given before transplant", "answer": "What is 4-6 cycles?", "rationale": "Goal is to achieve best response before ASCT collection", "difficulty": "intermediate"},

        {"category": "Transplant & Maintenance", "question": "This type of stem cell transplant is standard for eligible myeloma patients", "answer": "What is autologous stem cell transplant (ASCT)?", "rationale": "ASCT remains standard of care for fit patients ≤70 years", "difficulty": "basic"},
        {"category": "Transplant & Maintenance", "question": "This agent is standard maintenance therapy after ASCT", "answer": "What is lenalidomide?", "rationale": "Lenalidomide maintenance improves PFS and OS post-ASCT", "difficulty": "basic"},
        {"category": "Transplant & Maintenance", "question": "This conditioning regimen is standard for myeloma ASCT", "answer": "What is high-dose melphalan (200 mg/m²)?", "rationale": "Melphalan 200 is standard; reduced dose (140) for older/renal impaired", "difficulty": "intermediate"},
        {"category": "Transplant & Maintenance", "question": "This response depth predicts improved outcomes after treatment", "answer": "What is MRD (Minimal Residual Disease) negativity?", "rationale": "MRD negativity at 10⁻⁵ or 10⁻⁶ is a key prognostic marker", "difficulty": "advanced"},
        {"category": "Transplant & Maintenance", "question": "This approach uses two sequential ASCTs", "answer": "What is tandem transplant?", "rationale": "Tandem ASCT may benefit high-risk patients", "difficulty": "advanced"},

        {"category": "Relapsed Disease", "question": "This bispecific antibody targets BCMA and CD3", "answer": "What is teclistamab (Tecvayli)?", "rationale": "First bispecific approved for relapsed/refractory myeloma", "difficulty": "intermediate"},
        {"category": "Relapsed Disease", "question": "This CAR-T therapy targets BCMA in relapsed myeloma", "answer": "What is idecabtagene vicleucel (ide-cel/Abecma) or ciltacabtagene autoleucel (cilta-cel/Carvykti)?", "rationale": "BCMA-directed CAR-T shows deep responses in heavily pretreated patients", "difficulty": "advanced"},
        {"category": "Relapsed Disease", "question": "This oral XPO1 inhibitor is approved for penta-refractory myeloma", "answer": "What is selinexor (Xpovio)?", "rationale": "Selinexor with dexamethasone for heavily pretreated disease", "difficulty": "advanced"},
        {"category": "Relapsed Disease", "question": "This second-generation CD38 antibody has subcutaneous formulation", "answer": "What is isatuximab (Sarclisa)?", "rationale": "Isatuximab with pomalidomide/dex approved for relapsed disease", "difficulty": "intermediate"},
        {"category": "Relapsed Disease", "question": "This ADC targets BCMA with a cytotoxic payload", "answer": "What is belantamab mafodotin (Blenrep)?", "rationale": "Unique ocular toxicity requires ophthalmologic monitoring", "difficulty": "advanced"},

        {"category": "Supportive Care", "question": "This bisphosphonate is given monthly to prevent skeletal events", "answer": "What is zoledronic acid (Zometa)?", "rationale": "Monthly IV bisphosphonates or denosumab reduce SREs", "difficulty": "basic"},
        {"category": "Supportive Care", "question": "This vaccination is particularly important in myeloma patients", "answer": "What is pneumococcal vaccine?", "rationale": "Hypogammaglobulinemia increases infection risk", "difficulty": "basic"},
        {"category": "Supportive Care", "question": "This prophylaxis is required with IMiD therapy", "answer": "What is VTE prophylaxis (aspirin or anticoagulation)?", "rationale": "IMiDs increase thrombotic risk, especially with steroids", "difficulty": "intermediate"},
        {"category": "Supportive Care", "question": "This antiviral prophylaxis prevents reactivation during proteasome inhibitor therapy", "answer": "What is acyclovir (or valacyclovir)?", "rationale": "Herpes zoster prophylaxis is standard with PI therapy", "difficulty": "intermediate"},
        {"category": "Supportive Care", "question": "This jaw complication is associated with bisphosphonate therapy", "answer": "What is osteonecrosis of the jaw (ONJ)?", "rationale": "Dental evaluation recommended before starting bone-targeted therapy", "difficulty": "intermediate"},
    ],
    final_jeopardy={
        "category": "Myeloma Breakthroughs",
        "question": "This 2003 approval of the first proteasome inhibitor marked a new era in myeloma treatment",
        "answer": "What is bortezomib (Velcade)?",
        "rationale": "Bortezomib was the first PI approved, transforming myeloma outcomes"
    },
    difficulty_distribution="mixed",
    target_audience="all",
    estimated_duration=45,
    cme_objectives=[
        "Apply updated diagnostic criteria for multiple myeloma",
        "Select appropriate induction therapy based on transplant eligibility",
        "Understand the role of novel agents in relapsed disease",
        "Implement supportive care measures for myeloma patients"
    ]
)
register_game(MULTIPLE_MYELOMA_GAME)


# Import additional condition game modules to register all games
from jparty.condition_games import immunology
from jparty.condition_games import oncology
from jparty.condition_games import metabolic
from jparty.condition_games import pulmonary


# Convenience function to get all therapeutic areas
def get_therapeutic_areas() -> list:
    """Get list of all therapeutic areas with available games."""
    areas = set()
    for game in CONDITION_GAMES.values():
        areas.add(game.therapeutic_area)
    return sorted(list(areas))


def get_game_summary() -> dict:
    """Get a summary of all available games organized by therapeutic area."""
    summary = {}
    for game in CONDITION_GAMES.values():
        area = game.therapeutic_area
        if area not in summary:
            summary[area] = []
        summary[area].append({
            "id": game.condition_id,
            "name": game.condition_name,
            "audience": game.target_audience,
            "duration": game.estimated_duration,
            "categories": game.categories
        })
    return summary


def print_available_games():
    """Print a formatted list of all available condition games."""
    summary = get_game_summary()
    print("\n" + "=" * 60)
    print("AVAILABLE MEDICAL JEOPARDY GAMES")
    print("=" * 60)

    for area in sorted(summary.keys()):
        print(f"\n{area}")
        print("-" * 40)
        for game in summary[area]:
            print(f"  • {game['name']} ({game['id']})")
            print(f"    Duration: {game['duration']} min | Audience: {game['audience']}")

    print("\n" + "=" * 60)
    print(f"Total games available: {len(CONDITION_GAMES)}")
    print("=" * 60 + "\n")
