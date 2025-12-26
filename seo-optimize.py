#!/usr/bin/env python3
"""
SEO Optimization Script for FitCalcs
Based on Google's SEO Starter Guide recommendations
"""

import os
import re
from pathlib import Path

# Categories for internal linking
CATEGORIES = {
    'Health & Body': [
        ('bmi-calculator.html', 'BMI Calculator'),
        ('body-fat-calculator.html', 'Body Fat Calculator'),
        ('ideal-weight-calculator.html', 'Ideal Weight Calculator'),
        ('waist-hip-ratio-calculator.html', 'Waist-Hip Ratio'),
        ('blood-pressure-calculator.html', 'Blood Pressure'),
        ('heart-rate-calculator.html', 'Heart Rate Calculator'),
    ],
    'Nutrition & Diet': [
        ('calorie-calculator.html', 'Calorie Calculator'),
        ('tdee-calculator.html', 'TDEE Calculator'),
        ('macro-calculator.html', 'Macro Calculator'),
        ('protein-calculator.html', 'Protein Calculator'),
        ('keto-calculator.html', 'Keto Calculator'),
        ('water-intake-calculator.html', 'Water Intake'),
    ],
    'Fitness & Exercise': [
        ('one-rep-max-calculator.html', 'One Rep Max'),
        ('workout-calorie-calculator.html', 'Workout Calories'),
        ('running-pace-calculator.html', 'Running Pace'),
        ('cycling-calories-calculator.html', 'Cycling Calories'),
        ('swimming-calories-calculator.html', 'Swimming Calories'),
    ],
    'Pregnancy & Baby': [
        ('pregnancy-calculator.html', 'Pregnancy Calculator'),
        ('due-date-calculator.html', 'Due Date Calculator'),
        ('ovulation-calculator.html', 'Ovulation Calculator'),
        ('baby-weight-calculator.html', 'Baby Weight'),
    ],
    'Weight Loss': [
        ('weight-loss-calculator.html', 'Weight Loss Calculator'),
        ('fasting-calculator.html', 'Fasting Calculator'),
        ('intermittent-fasting-calculator.html', 'IF Calculator'),
    ],
}

# SEO-optimized footer HTML
FOOTER_HTML = '''
    <!-- SEO Footer -->
    <footer style="background: #0c1322; border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 20px; margin-top: 40px;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 30px;">
                <div>
                    <h3 style="color: #ea580c; font-size: 1rem; margin-bottom: 15px;">Health & Body</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="bmi-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">BMI Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="body-fat-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Body Fat Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="ideal-weight-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Ideal Weight Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="blood-pressure-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Blood Pressure</a></li>
                    </ul>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1rem; margin-bottom: 15px;">Nutrition & Diet</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="calorie-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Calorie Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="tdee-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">TDEE Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="macro-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Macro Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="keto-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Keto Calculator</a></li>
                    </ul>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1rem; margin-bottom: 15px;">Fitness</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="one-rep-max-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">One Rep Max</a></li>
                        <li style="margin-bottom: 8px;"><a href="workout-calorie-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Workout Calories</a></li>
                        <li style="margin-bottom: 8px;"><a href="running-pace-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Running Pace</a></li>
                        <li style="margin-bottom: 8px;"><a href="weight-loss-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Weight Loss</a></li>
                    </ul>
                </div>
                <div>
                    <h3 style="color: #ea580c; font-size: 1rem; margin-bottom: 15px;">Pregnancy</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 8px;"><a href="pregnancy-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Pregnancy Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="due-date-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Due Date Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="ovulation-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Ovulation Calculator</a></li>
                        <li style="margin-bottom: 8px;"><a href="baby-weight-calculator.html" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;">Baby Weight</a></li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1);">
                <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 10px;">
                    <a href="/" style="color: #ea580c; text-decoration: none; font-weight: 600;">FitCalcs</a> - Free Health & Fitness Calculators
                </p>
                <p style="color: #475569; font-size: 0.75rem;">
                    62 free calculators for BMI, calories, macros, pregnancy, and more. No signup required.
                </p>
                <p style="color: #475569; font-size: 0.75rem; margin-top: 10px;">
                    &copy; 2025 FitCalcs. All rights reserved. |
                    <a href="/" style="color: #64748b; text-decoration: none;">Home</a>
                </p>
            </div>
        </div>
    </footer>
'''

def optimize_html(filepath):
    """Apply SEO optimizations to a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    filename = os.path.basename(filepath)

    # Skip index.html (has its own footer already)
    if filename == 'index.html':
        return False

    # Skip non-calculator files
    if filename.startswith('google'):
        return False

    # 1. Remove meta keywords tag (Google ignores it)
    content = re.sub(r'\s*<meta name="keywords"[^>]*>\n?', '', content)

    # 2. Fix stray closing divs after breadcrumb nav
    content = re.sub(r'(</nav>)\s*</div>\s*</div>\s*\n', r'\1\n', content)

    # 3. Add closing </main> tag if missing before </body>
    if '<main>' in content or '<main ' in content:
        if '</main>' not in content:
            content = content.replace('</body>', '</main>\n</body>')

    # 4. Add SEO footer before </body> if not present
    if '<!-- SEO Footer -->' not in content:
        # Remove any existing simple footer
        content = re.sub(r'\s*<footer[^>]*>.*?</footer>\s*', '', content, flags=re.DOTALL)
        # Add new SEO footer
        content = content.replace('</body>', FOOTER_HTML + '\n</body>')

    # 5. Ensure proper HTML structure
    # Close any unclosed main tags before footer
    if '</main>' in content and FOOTER_HTML.strip()[:20] in content:
        # Make sure </main> comes before footer
        content = re.sub(r'(</main>)\s*(<!-- SEO Footer -->)', r'\1\n\n    \2', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Process all HTML files."""
    script_dir = Path(__file__).parent
    html_files = list(script_dir.glob('*.html'))

    modified = 0
    for filepath in html_files:
        if optimize_html(filepath):
            print(f"Optimized: {filepath.name}")
            modified += 1
        else:
            print(f"Skipped: {filepath.name}")

    print(f"\nTotal files modified: {modified}/{len(html_files)}")


if __name__ == '__main__':
    main()
