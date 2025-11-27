#!/usr/bin/env python3
"""
Med-Jeopardy: CME/CE Edition

Optimized for Continuing Medical Education events:
- Grand rounds
- Dinner meetings
- Virtual CME webinars
- Hybrid events

Features:
- Large audience support (100+ players)
- CME tracking and attendance
- Certificate-ready reporting
- Team-based competition
- Spectator mode
"""

import sys
sys.argv.extend(['--preset', 'cme', '--cme-tracking'])

from jparty.main import main

if __name__ == "__main__":
    main()
