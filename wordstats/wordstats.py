import argparse
import re
import sys
from collections import Counter

def analyse(text, top_n):
    words = re.findall(r"[A-Za-z']+", text.lower())
    counts = Counter(words)
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    print(f"Lines: {lines}")
    print(f"Words: {len(words)}")
    print(f"Unique words: {len(counts)}")
    print(f"Top {top_n} words:")
    for word, n in counts.most_common(top_n):
        print(f"  {word:<15} {n}")

def main():
    parser = argparse.ArgumentParser(description="Simple text statistics tool")
    parser.add_argument("file", nargs="?", help="Text file to analyse (default: stdin)")
    parser.add_argument("-n", "--top", type=int, default=5, help="Number of top words")
    args = parser.parse_args()

    try:
        text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    analyse(text, args.top)

if __name__ == "__main__":
    main()
