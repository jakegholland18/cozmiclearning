#!/usr/bin/env python3
"""
Visual Optimization Tool
Run this script to automatically test and improve visual generation quality
"""

import sys
from modules.visual_optimizer import run_visual_optimization_tests, generate_optimization_recommendations

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║       CozmicLearning Visual Optimization Tool              ║
║                                                            ║
║  This tool will:                                           ║
║  1. Test visual generation with 5 different scenarios     ║
║  2. Evaluate quality using AI (0-10 scores)                ║
║  3. Identify weaknesses and issues                         ║
║  4. Generate improved prompt recommendations               ║
╚════════════════════════════════════════════════════════════╝
""")

    input("Press Enter to start optimization tests...")

    # Run the tests
    results = run_visual_optimization_tests()

    # Generate recommendations
    print("\n\n" + "=" * 60)
    print("GENERATING OPTIMIZATION RECOMMENDATIONS...")
    print("=" * 60)

    recommendations = generate_optimization_recommendations(results)

    if recommendations:
        print("\n✅ Generated recommendations!")
        print("\nYou can now:")
        print("  1. Review the suggestions above")
        print("  2. Update modules/visual_generator.py with improved prompts")
        print("  3. Re-run this script to verify improvements")

        # Ask if user wants to save recommendations
        save = input("\n💾 Save recommendations to file? (y/n): ").lower()
        if save == 'y':
            with open('visual_optimization_report.txt', 'w') as f:
                f.write("VISUAL OPTIMIZATION RECOMMENDATIONS\n")
                f.write("=" * 60 + "\n\n")

                for rec in recommendations:
                    f.write(f"\n{rec['type'].upper()} IMPROVEMENTS\n")
                    f.write(f"Current Score: {rec['current_score']:.1f}/10\n")
                    f.write("-" * 60 + "\n")
                    f.write(rec['improved_guidelines'])
                    f.write("\n\n" + "=" * 60 + "\n")

            print("✅ Saved to visual_optimization_report.txt")
    else:
        print("\n✨ No improvements needed - visual quality is already excellent!")

    print("\n🎉 Optimization complete!")

if __name__ == "__main__":
    main()
