"""
Script to clean up unused endpoints from app/main.py
Removes ~1,185 lines of unused code while preserving all essential functionality
"""

import re

# Read the original file
with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"Original file: {len(lines)} lines")

# Define sections to remove (line ranges - will be adjusted as we remove)
# These are the UNUSED endpoints identified in the analysis

endpoints_to_remove = [
    # Line numbers will shift, so we'll use markers instead
    (r'@app\.get\("/workflow-status"\).*?(?=@app\.)', re.DOTALL),  # workflow-status
    (r'@app\.get\("/discover-google-sheets"\).*?(?=@app\.)', re.DOTALL),  # discover-google-sheets
    (r'@app\.post\("/continue-after-script-approval/\{job_id\}"\).*?(?=@app\.)', re.DOTALL),  # continue-after-approval
    (r'@app\.post\("/regenerate-content/\{job_id\}"\).*?(?=@app\.)', re.DOTALL),  # regenerate-content
    (r'@app\.post\("/generate-audio"\).*?(?=@app\.)', re.DOTALL),  # generate-audio
    (r'@app\.get\("/monitoring/health"\).*?(?=@app\.get\("/monitoring/metrics"\))', re.DOTALL),  # monitoring/health duplicate
    (r'@app\.get\("/monitoring/cost"\).*?(?=@app\.)', re.DOTALL),  # monitoring/cost
    (r'@app\.post\("/rag/reset"\).*?(?=@app\.)', re.DOTALL),  # rag/reset
    (r'@app\.post\("/process-document-rag"\).*?(?=@app\.)', re.DOTALL),  # process-document-rag
    (r'@app\.post\("/process-document-orchestrated"\).*?(?=@app\.)', re.DOTALL),  # process-document-orchestrated
    (r'@app\.post\("/process-document-advanced"\).*?(?=@app\.)', re.DOTALL),  # process-document-advanced
    (r'@app\.get\("/production-monitor/status"\).*?(?=@app\.)', re.DOTALL),  # production-monitor/status
    (r'@app\.get\("/production-monitor/metrics"\).*?(?=@app\.)', re.DOTALL),  # production-monitor/metrics
    (r'@app\.get\("/production-monitor/alerts"\).*?(?=@app\.)', re.DOTALL),  # production-monitor/alerts
    (r'@app\.post\("/production-monitor/resolve-alert/\{alert_id\}"\).*?(?=@app\.)', re.DOTALL),  # production-monitor/resolve-alert
    (r'@app\.post\("/crewai/run-single-agent/\{agent_type\}"\).*?(?=@app\.)', re.DOTALL),  # crewai/run-single-agent
]

# Remove each unused endpoint
for pattern, flags in endpoints_to_remove:
    matches = list(re.finditer(pattern, content, flags))
    if matches:
        for match in reversed(matches):  # Remove from end to start to preserve indices
            removed_text = match.group(0)
            print(f"\nRemoving endpoint (matched {len(removed_text)} chars):")
            print(f"  First line: {removed_text[:100]}...")
            content = content[:match.start()] + content[match.end():]

# Write cleaned file
with open('app/main_cleaned_temp.py', 'w', encoding='utf-8') as f:
    f.write(content)

cleaned_lines = content.split('\n')
print(f"\nCleaned file: {len(cleaned_lines)} lines")
print(f"Lines removed: {len(lines) - len(cleaned_lines)}")
print("\nCleaned file saved to: app/main_cleaned_temp.py")
print("Review it, then replace main.py if everything looks good!")

