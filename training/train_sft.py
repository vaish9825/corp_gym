"""LoRA/QLoRA SFT for CORP-ENV action-format warm start.

Run on Lightning AI H100, not on the local lightweight environment:

  python training/train_sft.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --data data/sft/e1_m1_examples.jsonl \
    --output outputs/sft_adapter \
    --push-to-hub your-org/corp-env-sft-adapter
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def load_text_rows(path: Path, tokenizer: object) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            messages = obj["messages"]
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )
            rows.append({"text": text})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CORP-ENV SFT LoRA adapter.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--data", default="data/sft/e1_m1_examples.jsonl")
    parser.add_argument("--output", default="outputs/sft_adapter")
    parser.add_argument("--max-seq-length", type=int, default=8192)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--push-to-hub", default="")
    args = parser.parse_args()

    try:
        from datasets import Dataset
        from trl import SFTConfig, SFTTrainer
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit(
            "SFT training requires datasets, trl, and unsloth. On Lightning AI, install with:\n"
            "  pip install -U unsloth trl datasets accelerate peft bitsandbytes transformers"
        ) from exc

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=32,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=32,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )

    dataset = Dataset.from_list(load_text_rows(Path(args.data), tokenizer))
    config = SFTConfig(
        output_dir=args.output,
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        warmup_ratio=0.05,
        lr_scheduler_type="cosine",
        logging_steps=5,
        save_steps=args.save_steps,
        save_total_limit=3,
        bf16=True,
        packing=False,
        report_to="none",
    )
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=config,
    )
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)

    if args.push_to_hub:
        trainer.push_to_hub(args.push_to_hub)


if __name__ == "__main__":
    main()
