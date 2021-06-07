"""Helper functions for language tasks."""

import torch
import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import pandas as pd
from sklearn import metrics


def to_device(inputs: dict, device: int = 0):
    return {
        k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()
    }


class ClassificationDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        text_col: str,
        label_col: str,
        tokenizer: transformers.AutoTokenizer,
    ):
        self.tokenizer = tokenizer
        self.data = df[[text_col, label_col]].dropna()
        self.encodings = self.tokenizer(
            self.data[text_col].values.tolist(),
            padding="max_length",
            truncation=True,
        )
        self.labels = self.data[label_col]

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        inputs = {
            key: torch.tensor(val[index])  # pylint: disable=not-callable
            for key, val in self.encodings.items()
        }
        inputs["labels"] = torch.tensor(  # pylint: disable=not-callable
            self.labels.iloc[index]
        )
        return inputs


class SentimentModel:
    def __init__(self, device: int = 0):
        self.device = device
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english"
        )

    def __call__(self, text: str):
        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
            )
            inputs = to_device(inputs, self.device)
            outputs = self.model(**inputs)
            prediction = (
                outputs.logits.softmax(dim=-1).detach().cpu().numpy().flatten()[1]
            )
        return prediction
