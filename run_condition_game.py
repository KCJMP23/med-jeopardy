#!/usr/bin/env python3
"""
Med-Jeopardy: Condition-Specific Game Launcher

Launch pre-built medical education games for specific diseases and conditions.

Usage:
    python run_condition_game.py --list                    # List all available games
    python run_condition_game.py --condition heart_failure # Launch Heart Failure game
    python run_condition_game.py --area Oncology           # List games in an area
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Med-Jeopardy Condition-Specific Game Launcher"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available condition games"
    )
    parser.add_argument(
        "--condition", "-c",
        type=str,
        help="Condition ID to launch (e.g., heart_failure, dlbcl, asthma)"
    )
    parser.add_argument(
        "--area", "-a",
        type=str,
        help="Show games in a therapeutic area (e.g., Oncology, Pulmonology)"
    )
    parser.add_argument(
        "--info", "-i",
        type=str,
        help="Show detailed info for a condition game"
    )

    args = parser.parse_args()

    # Import after argparse to speed up --help
    from jparty.condition_games import (
        list_conditions,
        get_condition_game,
        get_therapeutic_areas,
        get_game_summary,
        print_available_games,
        CONDITION_GAMES
    )

    if args.list:
        print_available_games()
        return

    if args.area:
        summary = get_game_summary()
        if args.area in summary:
            print(f"\nGames in {args.area}:")
            print("-" * 40)
            for game in summary[args.area]:
                print(f"  • {game['name']} ({game['id']})")
        else:
            print(f"Therapeutic area '{args.area}' not found.")
            print(f"Available areas: {', '.join(get_therapeutic_areas())}")
        return

    if args.info:
        if args.info in CONDITION_GAMES:
            game = CONDITION_GAMES[args.info]
            print(f"\n{'='*60}")
            print(f"GAME: {game.condition_name}")
            print(f"{'='*60}")
            print(f"Therapeutic Area: {game.therapeutic_area}")
            print(f"Duration: {game.estimated_duration} minutes")
            print(f"Target Audience: {game.target_audience}")
            print(f"Difficulty: {game.difficulty_distribution}")
            print(f"\nDescription:\n{game.description}")
            print(f"\nCategories:")
            for cat in game.categories:
                print(f"  • {cat}")
            print(f"\nCME Objectives:")
            for obj in game.cme_objectives:
                print(f"  • {obj}")
            print(f"\nQuestions: {len(game.questions)}")
            print(f"{'='*60}\n")
        else:
            print(f"Condition '{args.info}' not found.")
            print("Use --list to see available conditions.")
        return

    if args.condition:
        if args.condition not in CONDITION_GAMES:
            print(f"Condition '{args.condition}' not found.")
            print("Use --list to see available conditions.")
            sys.exit(1)

        game = CONDITION_GAMES[args.condition]
        game_data = get_condition_game(args.condition)

        if game_data:
            print(f"\n{'='*60}")
            print(f"CONDITION GAME: {game.condition_name}")
            print(f"{'='*60}")
            print(f"Categories: {', '.join(game.categories)}")
            print(f"Duration: ~{game.estimated_duration} minutes")
            print(f"Rounds: {len(game_data.rounds)}")
            print(f"Questions per round: 30")
            print(f"\nGame data validated and ready.")
            print(f"{'='*60}")
            # TODO: Inject game_data into jparty.main via a new --game-data parameter
            # or module-level game loader. For now, use --info to preview game content.
            print("\nNote: Direct game launch pending integration with jparty.main.")
            print("Use --info to view full game details.")
        else:
            print(f"Failed to load game data for '{args.condition}'.")
            sys.exit(1)
        return

    # No arguments - show help
    parser.print_help()
    print("\n" + "="*60)
    print("QUICK START:")
    print("  python run_condition_game.py --list")
    print("  python run_condition_game.py --info heart_failure")
    print("  python run_condition_game.py --condition asthma")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
