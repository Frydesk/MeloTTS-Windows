#!/usr/bin/env python
import sys
import os

def check_file(filename):
    print(f"Checking file: {filename}")
    
    valid_count = 0
    invalid_count = 0
    min_len = float('inf')
    max_len = 0
    
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            try:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    print(f"  Line {i}: Invalid format (fewer than 5 fields)")
                    continue
                
                phonemes = parts[4].split()
                phoneme_count = len(phonemes)
                
                min_len = min(min_len, phoneme_count)
                max_len = max(max_len, phoneme_count)
                
                if phoneme_count > 300:
                    print(f"  Line {i}: Exceeds max length - {phoneme_count} phonemes")
                    invalid_count += 1
                elif phoneme_count < 1:
                    print(f"  Line {i}: Below min length - {phoneme_count} phonemes")
                    invalid_count += 1
                else:
                    valid_count += 1
            except Exception as e:
                print(f"  Line {i}: Error processing - {str(e)}")
    
    print(f"\nSummary for {filename}:")
    print(f"  Valid entries: {valid_count}")
    print(f"  Invalid entries: {invalid_count}")
    print(f"  Shortest entry: {min_len} phonemes")
    print(f"  Longest entry: {max_len} phonemes")
    print(f"  Valid range is 1-300 phonemes\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_lengths.py path/to/data.list [path/to/another.list ...]")
        return
    
    for filename in sys.argv[1:]:
        if os.path.exists(filename):
            check_file(filename)
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main() 