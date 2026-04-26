import re
import os
import matplotlib.pyplot as plt

def parse_losses(filepath):
    losses = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to find JSON-like dicts containing 'loss'
    for match in re.finditer(r"\{'loss':\s*'([^']+)'", content):
        try:
            val = float(match.group(1))
            losses.append(val)
        except ValueError:
            pass
            
    for match in re.finditer(r"\{'loss':\s*([0-9\.]+)", content):
        try:
            val = float(match.group(1))
        except ValueError:
            pass

    return losses

def main():
    qwen35_file = 'training_logs/qwen3.5-9b_sft.txt'
    qwen25_file = 'training_logs/qwen2.5-7b-instruct_sft.txt'
    
    qwen35_losses = parse_losses(qwen35_file)
    qwen25_losses = parse_losses(qwen25_file)
    
    plt.figure(figsize=(8, 6))
    
    plt.plot(qwen25_losses, marker='o', linestyle='-', color='blue', label='Qwen 2.5-7B SFT')
    plt.plot(qwen35_losses, marker='s', linestyle='-', color='green', label='Qwen 3.5-9B SFT')
    
    plt.title('SFT Loss Comparison: Qwen 2.5 vs 3.5')
    plt.xlabel('Step')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    output_path = os.path.abspath('results/qwen_sft_comparison.png')
    plt.savefig(output_path)
    print(f"Saved plot to {output_path}")

if __name__ == '__main__':
    main()
