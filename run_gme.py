#!/usr/bin/env python3
"""
Med-Jeopardy: GME Edition

Optimized for Graduate Medical Education:
- Residency didactic conferences
- Morning report sessions
- Noon conferences
- Team-based learning

Features:
- Team battle mode
- Medium audience (25 players)
- Rationale display for teaching
- Specialty tagging for curriculum mapping
"""

import sys
sys.argv.extend(['--preset', 'gme'])

from jparty.main import main

if __name__ == "__main__":
    main()
