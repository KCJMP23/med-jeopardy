# Med-Jeopardy: Medical Education Guide

## Overview

Med-Jeopardy is an optimized version of JParty designed specifically for medical education. It supports:

1. **Board Exam Study** - USMLE, COMLEX, specialty boards
2. **Graduate Medical Education (GME)** - Residency training and conferences
3. **CME/CE Events** - Grand rounds, dinner meetings, virtual events

## Features

### Enhanced Question Support

- **Clinical Images**: Display X-rays, CT scans, pathology slides, dermatology images
- **Case Vignettes**: Extended time for complex clinical scenarios
- **Educational Rationale**: Show explanations after answer reveal
- **Difficulty Indicators**: Basic, Intermediate, Advanced, Expert levels
- **Specialty Tagging**: Organize by medical specialty and organ system

### Scalable for Any Audience

| Mode | Max Players | Use Case |
|------|-------------|----------|
| Small Group | 8 | Study groups, small didactics |
| Medium | 25 | Resident conferences |
| Large | 100 | Grand rounds |
| Virtual Event | 500 | CME webinars |

### Team Mode

- Team-based competition for collaborative learning
- Configurable team sizes
- Optional conferring time for team discussion

### CME/CE Tracking

- Attendance tracking
- Performance metrics by participant
- Specialty-based score breakdown
- CSV/JSON export for credit processing

## Google Sheets Template Format

### Standard Format (Compatible with Original JParty)

Use the original template for basic games:
https://docs.google.com/spreadsheets/d/1_vBBsWn-EVc7npamLnOKHs34Mc2iAmd9hOGSzxHQX0Y/

### Medical Education Format

For full medical education features, use this extended format:

#### Round 1 Structure (Rows 0-35)

```
Row 0:  [Value] [Cat 1] [Cat 2] [Cat 3] [Cat 4] [Cat 5] [Cat 6] [DD Cells]
Row 1:  [100]   [Q1]    [Q2]    [Q3]    [Q4]    [Q5]    [Q6]
Row 2:  [200]   [Q1]    [Q2]    [Q3]    [Q4]    [Q5]    [Q6]
Row 3:  [300]   [Q1]    [Q2]    [Q3]    [Q4]    [Q5]    [Q6]
Row 4:  [400]   [Q1]    [Q2]    [Q3]    [Q4]    [Q5]    [Q6]
Row 5:  [500]   [Q1]    [Q2]    [Q3]    [Q4]    [Q5]    [Q6]
Row 6:  [ANSWERS]
Row 7:  [100]   [A1]    [A2]    [A3]    [A4]    [A5]    [A6]
Row 8:  [200]   [A1]    [A2]    [A3]    [A4]    [A5]    [A6]
...
Row 12: [RATIONALE] (Medical Extension)
Row 13: [100]   [R1]    [R2]    [R3]    [R4]    [R5]    [R6]
...
Row 18: [IMAGES] (Medical Extension)
Row 19: [100]   [URL1]  [URL2]  [URL3]  [URL4]  [URL5]  [URL6]
...
Row 24: [DIFFICULTY] (Medical Extension)
Row 25: [100]   [D1]    [D2]    [D3]    [D4]    [D5]    [D6]
...
Row 30: [SPECIALTY] (Medical Extension)
Row 31: [100]   [S1]    [S2]    [S3]    [S4]    [S5]    [S6]
...
```

#### Column Definitions

| Column | Content | Example |
|--------|---------|---------|
| A | Point Value | 100, 200, 300, 400, 500 |
| B-G | Category Content | Questions, Answers, etc. |
| H | Daily Double Cells | "B2,E4" (column+row) |

#### Medical Extensions

| Section | Row Range | Content |
|---------|-----------|---------|
| Questions | 1-5 | Question text |
| Answers | 7-11 | Answer text |
| Rationale | 13-17 | Educational explanation |
| Images | 19-23 | Image URL (Google Drive, Imgur, etc.) |
| Difficulty | 25-29 | basic, intermediate, advanced, expert |
| Specialty | 31-35 | Cardiology, Neurology, etc. |

### Final Jeopardy Row (Last Row)

```
[FJ] [Category] [Question] [Answer] [Rationale] [Image URL] [Difficulty] [Specialty] [Date] [Comments]
```

## Configuration Presets

### For Board Study Sessions

```python
from jparty.med_config import MedJeopardyConfig

config = MedJeopardyConfig.for_boards_study()
# - Learning mode with rationale display
# - Extended timers
# - Performance tracking
# - Second chance on missed questions
```

### For Residency Conferences

```python
config = MedJeopardyConfig.for_residency_conference()
# - Team mode enabled
# - Medium audience size (25 players)
# - Rationale display
# - Difficulty indicators
```

### For Grand Rounds / CME Events

```python
config = MedJeopardyConfig.for_grand_rounds()
# - Team battle mode
# - Large audience (100 players)
# - CME tracking enabled
# - Spectator mode
```

### For Virtual CME Events

```python
config = MedJeopardyConfig.for_virtual_cme()
# - 500+ participants
# - Team mode
# - Full CME tracking
# - Attendance verification
```

## Timer Configuration

Default timers for medical questions:

| Question Type | Default Time | Adjustable |
|--------------|--------------|------------|
| Standard | 8 seconds | Yes |
| Image-based | 12 seconds | Yes |
| Case Vignette | 15 seconds | Yes |
| Final Jeopardy | 60 seconds | Yes |

## CME Export

After a session, export data for CME credit processing:

```python
from jparty.cme_tracking import CMETracker

tracker.export_csv("session_report.csv")
tracker.export_json("session_report.json")
tracker.export_attendance_list("attendance.csv")
```

Exported data includes:
- Participant names and teams
- Questions answered and accuracy
- Specialty breakdown
- CME eligibility status
- Session duration

## Image Hosting Recommendations

For clinical images, we recommend:

1. **Google Drive** - Share with "Anyone with link"
   - Get shareable link
   - Use direct image URL format

2. **Imgur** - Free image hosting
   - Upload images
   - Use direct link (i.imgur.com/xxx.jpg)

3. **Institution Server** - For PHI compliance
   - Ensure de-identified images only
   - Use HTTPS URLs

## Best Practices

### For Board Study

1. Create category-specific games (Cardiology, GI, etc.)
2. Include rationale with board-relevant explanations
3. Use difficulty progression (easy to hard)
4. Include relevant First Aid/Step references

### For GME Conferences

1. Mix specialties for interdisciplinary learning
2. Include case-based questions from real scenarios
3. Use team mode for collaborative discussion
4. Display rationale for teaching moments

### For CME Events

1. Enable CME tracking
2. Set minimum participation requirements
3. Cover multiple specialties/systems
4. Export attendance for credit documentation

## Troubleshooting

### Images Not Loading

- Verify URL is direct link to image
- Check image is publicly accessible
- Use HTTPS URLs only

### Long Questions Cut Off

- Questions over 200 characters auto-detect as case vignettes
- Extended timer applied automatically
- Consider splitting into shorter clues

### Performance with Large Groups

- For 100+ players, use team mode
- Enable spectator mode for overflow
- Consider virtual event preset

## Support

For issues or feature requests, visit:
https://github.com/stuartthomas25/JParty
