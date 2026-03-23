import requests
import json

r = requests.get('http://localhost:5050/api/documents')
docs = json.loads(r.text)

print(f'\n=== TOTAL DOCUMENTS IN DATABASE: {len(docs)} ===\n')

reference_docs = [d for d in docs if d['is_reference'] == 1]
other_docs = [d for d in docs if d['is_reference'] == 0]

print(f"Reference Documents ({len(reference_docs)}):")
for i, doc in enumerate(reference_docs, 1):
    print(f"  {i}. {doc['filename']} (Size: {doc['size']} bytes, Hash: {doc['sha256'][:16]}...)")

print(f"\nOther Documents ({len(other_docs)}):")
for i, doc in enumerate(other_docs, 1):
    print(f"  {i}. {doc['filename']} (Size: {doc['size']} bytes, Hash: {doc['sha256'][:16]}...)")

print(f"\n✓ Successfully seeded {len(reference_docs)} reference documents into the database!")
