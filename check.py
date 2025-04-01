# import os
# import json
# from jsondiff import diff

# old_dir = "old_files"
# new_dir = "new_files"
# results = {}

# for i in range(1, 1):
#     old_file = os.path.join(old_dir, f"file{i}.json")
#     new_file = os.path.join(new_dir, f"file{i}.json")
    
#     with open(old_file, 'r') as f1, open(new_file, 'r') as f2:
#         old_data = json.load(f1)
#         new_data = json.load(f2)
#         file_diff = diff(old_data, new_data)
#         results[f"file{i}"] = file_diff

# # Print or save results
# for file, d in results.items():
#     print(f"\nDifferences in {file}:\n{d}")


import json
import jsondiff
with open('/home/sheri/Documents/JSON-checker/old_files/file1.json', 'r') as f:
	old_data = json.load(f)

with open('/home/sheri/Documents/JSON-checker/new_files/file1.json', 'r') as f:
	new_data = json.load(f)

diff = jsondiff.diff(old_data, new_data)
print(diff)
print(diff)