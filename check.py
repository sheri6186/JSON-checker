# import json
# import os
# from pathlib import Path
# import webbrowser

# # Base paths for the JSON files and output directory
# base_path = Path.home() / 'Documents' / 'JSON-checker'
# old_dir = base_path / 'old_files'
# new_dir = base_path / 'new_files'
# output_dir = base_path / 'html_reports'
# output_dir.mkdir(parents=True, exist_ok=True)

# # Recursive comparison, supports nested dicts and lists
# def compare_json(old, new, path=''):
#     differences = []
    
#     if isinstance(old, dict) and isinstance(new, dict):
#         keys = set(old.keys()) | set(new.keys())
#         for key in keys:
#             new_path = f"{path}.{key}" if path else key
#             differences += compare_json(old.get(key), new.get(key), new_path)
    
#     elif isinstance(old, list) and isinstance(new, list):
#         max_len = max(len(old), len(new))
#         for i in range(max_len):
#             new_path = f"{path}[{i}]"
#             o_val = old[i] if i < len(old) else '<Missing>'
#             n_val = new[i] if i < len(new) else '<Missing>'
#             differences += compare_json(o_val, n_val, new_path)
    
#     else:
#         if old != new:
#             differences.append({
#                 'key': path,
#                 'old_value': old,
#                 'new_value': new
#             })
    
#     return differences

# # HTML report generator for multiple files
# def generate_html_report(differences_by_file):
#     html = """<!DOCTYPE html>
# <html>
# <head>
#     <meta charset="UTF-8">
#     <title>JSON Diff Report</title>
#     <style>
#         body { font-family: Arial; background: #f4f4f4; padding: 20px; }
#         table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
#         th, td { padding: 10px; border: 1px solid #ccc; }
#         .old { background: #ffe6e6; color: #b30000; }
#         .new { background: #e6ffe6; color: #006600; }
#         .key { font-weight: bold; color: #333; }
#         h1 { text-align: center; }
#         h2 { margin-top: 40px; }
#     </style>
# </head>
# <body>
#     <h1>JSON Diff Report</h1>"""
    
#     if not differences_by_file:
#         html += "<p>No differences found in any files.</p>"
#     else:
#         for file_name, differences in sorted(differences_by_file.items()):
#             html += f"<h2>File: {file_name}</h2>"
#             html += """<table>
#                 <tr><th>Key Path</th><th>Old Value</th><th>New Value</th></tr>"""
#             if not differences:
#                 html += "<tr><td colspan='3'>No differences found.</td></tr>"
#             else:
#                 for d in differences:
#                     html += f"""
#                 <tr>
#                     <td class="key">{d['key']}</td>
#                     <td class="old">{json.dumps(d['old_value'])}</td>
#                     <td class="new">{json.dumps(d['new_value'])}</td>
#                 </tr>"""
#             html += "</table>"
    
#     html += """
# </body>
# </html>"""
#     return html

# # Collect differences for all files
# differences_by_file = {}

# # Get all JSON files in the old_files directory
# old_files = {f.name: f for f in old_dir.glob("*.json")}
# new_files = {f.name: f for f in new_dir.glob("*.json")}

# # Compare files that exist in both directories
# for file_name in old_files.keys() & new_files.keys():
#     old_path = old_files[file_name]
#     new_path = new_files[file_name]

#     with open(old_path) as f1, open(new_path) as f2:
#         old_json = json.load(f1)
#         new_json = json.load(f2)

#     diffs = compare_json(old_json, new_json)
#     differences_by_file[file_name] = diffs

# # Generate a single HTML report
# output_file = output_dir / "combined_diff_report.html"
# html_report = generate_html_report(differences_by_file)

# with open(output_file, 'w', encoding='utf-8') as f:
#     f.write(html_report)

# print(f"✔ Combined report generated: {output_file}")

# # Auto open in default browser
# webbrowser.open(f"file://{output_file}")




import json
import os
from pathlib import Path
import webbrowser

# Base paths
base_path = Path("c:/JSON-checker")
old_dir = base_path / 'old_files'
new_dir = base_path / 'new_files'
output_dir = base_path / 'html_reports'
output_dir.mkdir(parents=True, exist_ok=True)

# Normalize for comparison
def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        return [normalize(v) for v in obj]
    else:
        return obj

# Partial comparison helper
def partial_compare(old_item, new_item, path):
    differences = []
    if isinstance(old_item, dict) and isinstance(new_item, dict):
        all_keys = set(old_item.keys()) | set(new_item.keys())
        for key in all_keys:
            old_val = old_item.get(key, '<Missing>')
            new_val = new_item.get(key, '<Missing>')
            if normalize(old_val) != normalize(new_val):
                differences.append({
                    'key': f"{path}.{key}" if path else key,
                    'old_value': old_val,
                    'new_value': new_val
                })
    else:
        if normalize(old_item) != normalize(new_item):
            differences.append({
                'key': path,
                'old_value': old_item,
                'new_value': new_item
            })
    return differences

# Main comparison function
def compare_json(old, new, path=''):
    differences = []

    # If both are dicts
    if isinstance(old, dict) and isinstance(new, dict):
        old_keys = set(old)
        new_keys = set(new)

        # Highlight added/removed top-level keys
        for key in old_keys - new_keys:
            differences.append({'key': f"{path}.{key}" if path else key, 'old_value': old[key], 'new_value': '<Missing>'})
        for key in new_keys - old_keys:
            differences.append({'key': f"{path}.{key}" if path else key, 'old_value': '<Missing>', 'new_value': new[key]})

        for key in old_keys & new_keys:
            new_path = f"{path}.{key}" if path else key
            differences += compare_json(old[key], new[key], new_path)

    # If both are lists
    elif isinstance(old, list) and isinstance(new, list):
        # If list of dicts with 'name' as matching key
        if all(isinstance(i, dict) and 'name' in i for i in old + new):
            old_map = {item['name']: item for item in old}
            new_map = {item['name']: item for item in new}
            all_keys = set(old_map) | set(new_map)

            for k in all_keys:
                o = old_map.get(k, '<Missing>')
                n = new_map.get(k, '<Missing>')
                if o == '<Missing>' or n == '<Missing>':
                    differences.append({
                        'key': f"{path}[name={k}]",
                        'old_value': o,
                        'new_value': n
                    })
                else:
                    differences += partial_compare(o, n, f"{path}[name={k}]")

        else:
            # fallback set comparison for simple items or unordered dicts
            old_set = {json.dumps(normalize(i), sort_keys=True) for i in old}
            new_set = {json.dumps(normalize(i), sort_keys=True) for i in new}

            for i in old_set - new_set:
                differences.append({'key': path, 'old_value': json.loads(i), 'new_value': '<Missing>'})
            for i in new_set - old_set:
                differences.append({'key': path, 'old_value': '<Missing>', 'new_value': json.loads(i)})

    # For all other types
    else:
        if normalize(old) != normalize(new):
            differences.append({'key': path, 'old_value': old, 'new_value': new})

    return differences

# HTML report generator
def generate_html_report(differences_by_file):
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JSON Diff Report</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { padding: 10px; border: 1px solid #ccc; }
        .old { background: #ffe6e6; color: #b30000; }
        .new { background: #e6ffe6; color: #006600; }
        .key { font-weight: bold; color: #333; }
        h1 { text-align: center; }
        h2 { margin-top: 40px; }
    </style>
</head>
<body>
    <h1>JSON Diff Report</h1>"""
    
    if not differences_by_file:
        html += "<p>No differences found in any files.</p>"
    else:
        for file_name, differences in sorted(differences_by_file.items()):
            html += f"<h2>File: {file_name}</h2>"
            html += """<table>
                <tr><th>Key Path</th><th>Old Value</th><th>New Value</th></tr>"""
            if not differences:
                html += "<tr><td colspan='3'>No differences found.</td></tr>"
            else:
                for d in differences:
                    html += f"""
                <tr>
                    <td class="key">{d['key']}</td>
                    <td class="old">{json.dumps(d['old_value'])}</td>
                    <td class="new">{json.dumps(d['new_value'])}</td>
                </tr>"""
            html += "</table>"
    
    html += "</body></html>"""
    return html

# Compare and generate report
differences_by_file = {}

old_files = {f.name: f for f in old_dir.glob("*.json")}
new_files = {f.name: f for f in new_dir.glob("*.json")}

for file_name in old_files.keys() & new_files.keys():
    with open(old_files[file_name]) as f1, open(new_files[file_name]) as f2:
        old_json = json.load(f1)
        new_json = json.load(f2)

    diffs = compare_json(old_json, new_json)
    differences_by_file[file_name] = diffs

# Output HTML
output_file = output_dir / "combined_diff_report.html"
html_report = generate_html_report(differences_by_file)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_report)

print(f"✔ Combined report generated: {output_file}")
webbrowser.open(f"file://{output_file}")


