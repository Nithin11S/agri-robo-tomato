"""
Quick script to check training status by looking at model file timestamps
"""
import os
from datetime import datetime

model_files = [
    'tomato_disease_model.h5',
    'tomato_disease_model_best.h5'
]

print("=" * 60)
print("Training Status Check")
print("=" * 60)

for model_file in model_files:
    if os.path.exists(model_file):
        mod_time = os.path.getmtime(model_file)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        file_size = os.path.getsize(model_file) / (1024 * 1024)  # Size in MB
        print(f"\n{model_file}:")
        print(f"  - Last modified: {mod_time_str}")
        print(f"  - Size: {file_size:.2f} MB")
        
        # Check if recently modified (within last 5 minutes)
        time_diff = (datetime.now().timestamp() - mod_time) / 60
        if time_diff < 5:
            print(f"  - Status: [ACTIVE] Recently updated ({time_diff:.1f} minutes ago)")
        else:
            print(f"  - Status: [IDLE] Last updated {time_diff:.1f} minutes ago")
    else:
        print(f"\n{model_file}: Not found")

print("\n" + "=" * 60)
print("Note: If model files are being updated, training is active.")
print("=" * 60)

