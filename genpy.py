#!/usr/bin/env python3

import os
import sys
from typing import Optional

def train_hf(model_name, dataset_name, output_dir, num_labels):
    from datasets import load_dataset
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        Trainer, TrainingArguments
    )

    # Load dataset and model
    dataset = load_dataset(dataset_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def preprocess(example):
        return tokenizer(example['text'], truncation=True, padding='max_length', max_length=128)

    tokenized = dataset.map(preprocess, batched=True)
    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"].shuffle(seed=42).select(range(2000)),
        eval_dataset=tokenized["test"].shuffle(seed=42).select(range(500)),
    )

    trainer.train()
    trainer.save_model(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    # Args: mode, model_name, dataset_name, output_dir, num_labels
    # Example: python train.py hf distilbert-base-uncased yelp_review_full /mnt/output 5
    mode = sys.argv[1]
    output_dir = sys.argv[4]

    os.makedirs(output_dir, exist_ok=True)

    if mode == "hf":
        model_name = sys.argv[2]
        dataset_name = sys.argv[3]
        num_labels = int(sys.argv[5])
        train_hf(model_name, dataset_name, output_dir, num_labels)
    elif mode == "pytorch":
        train_pytorch(output_dir)
    else:
        raise ValueError(f"Unknown mode {mode}. Use 'hf' or 'pytorch'.")

