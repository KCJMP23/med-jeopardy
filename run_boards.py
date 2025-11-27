#!/usr/bin/env python3
"""
Med-Jeopardy: Board Study Edition

Optimized for medical students preparing for:
- USMLE Step 1, Step 2 CK, Step 3
- COMLEX Level 1, 2, 3
- Specialty Board Exams

Features:
- Learning mode with rationale display
- Extended timers for complex cases
- Performance tracking by topic
- Spaced repetition support
"""

import sys
sys.argv.extend(['--preset', 'boards'])

from jparty.main import main

if __name__ == "__main__":
    main()
