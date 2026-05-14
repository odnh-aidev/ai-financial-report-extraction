import json
import os

def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    text = words
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(" ".join(text[start:end]))
        start += chunk_size - overlap
    return chunks


def chunk_reports(reports):
    chunked_reports = []
    for report in reports:
        chunks = chunk_text(report["document"])
        for i, chunk in enumerate(chunks):
            chunked_reports.append({
                "chunk_id": i,
                "company": report["ground_truth"]["company"],
                "ground_truth": report["ground_truth"],
                "chunk": chunk
            })
    return chunked_reports

def main():
    with open("data/reports/_all_reports.json", "r") as f:
        reports = json.load(f)

    chunks = chunk_reports(reports)

    with open(os.path.join("data", "chunks.json"), "w") as f:
        json.dump(chunks, f, indent=2)
    

    print(f"Total chunks: {len(chunks)}")
    print(f"First chunk company: {chunks[0]['company']}")
    print(f"First chunk id: {chunks[0]['chunk_id']}")
    print(f"First chunk preview: {chunks[0]['chunk'][:100]}")
    print(f"\nDone — {len(chunks)} chunks saved.")

if __name__ == "__main__":
    main()