import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--task_type")
parser.add_argument("--dataset_name")
parser.add_argument("--model_uri")
parser.add_argument("--framework")
parser.add_argument("--output_dir")
parser.add_argument("--trained_model")
parser.add_argument("--training_logs")
parser.add_argument("--epochs", type=int, default=1)
args = parser.parse_args()

os.makedirs(args.trained_model, exist_ok=True)
os.makedirs(args.training_logs, exist_ok=True)

# Write logs and a "model" file just to confirm it runs
with open(os.path.join(args.training_logs, "log.txt"), "w") as f:
    f.write(f"Framework: {args.framework}\n")
    f.write(f"Task: {args.task_type}\n")
    f.write(f"Dataset: {args.dataset_name}\n")
    f.write(f"Epochs: {args.epochs}\n")
    f.write("This is a test log to show that train.py executed successfully.\n")

with open(os.path.join(args.trained_model, "model.txt"), "w") as f:
    f.write("This is a dummy trained model output file.\n")
    f.write(f"Model URI: {args.model_uri}\n")
