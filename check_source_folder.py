#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from app.services.google_services import GoogleDriveService
from app.config import settings

g = GoogleDriveService()

print("=" * 70)
print("CHECKING SOURCE FOLDER STRUCTURE")
print("=" * 70)

# Get all items in source folder
all_items = g.list_files_in_folder(settings.google_drive_content_source_folder_id)

folders = [f for f in all_items if f.get('mimeType') == 'application/vnd.google-apps.folder']
documents = [f for f in all_items if f['name'].lower().endswith(('.docx', '.pdf', '.txt'))]

print(f"\n📁 Folders found: {len(folders)}")
print(f"📄 Documents found (direct): {len(documents)}")

if documents:
    print("\n✅ Found documents in root:")
    for doc in documents[:5]:
        print(f"   - {doc['name']}")
else:
    print("\n⚠️ No documents in root folder, checking subfolders...")
    
    # Check first few subfolders
    for i, folder in enumerate(folders[:3]):
        folder_name = folder['name']
        folder_id = folder['id']
        print(f"\n📁 Checking subfolder {i+1}: {folder_name[:50]}...")
        
        subfolder_items = g.list_files_in_folder(folder_id)
        subfolder_docs = [f for f in subfolder_items 
                         if f['name'].lower().endswith(('.docx', '.pdf', '.txt'))]
        
        print(f"   Found {len(subfolder_docs)} documents")
        if subfolder_docs:
            for doc in subfolder_docs[:3]:
                print(f"      - {doc['name']}")

print("\n" + "=" * 70)
print("RECOMMENDATION:")
if documents:
    print("✅ Ready to process! Run automation_phase1_content.py")
else:
    print("⚠️ Documents are in subfolders.")
    print("   Option 1: Move documents to root of source folder")
    print("   Option 2: Modify script to process subfolders recursively")
print("=" * 70)
