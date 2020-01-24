"""
Generate a paragraph of text based on an input.
"""
#pylint: disable=not-callable,wrong-import-position,useless-suppression
# Make sure logging on the transformers module is disabled... We don't care.
import logging
logging.getLogger('transformers').setLevel(logging.WARNING)
from random import choice
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Total length of the paragraph to generate.
PARAGRAPH_LENGTH = 100
# How long before the end of paragraph length the program should start looking for a period.
# We assume it generally takes around 10 text components to generate a period, though it may be more or less.
YELLOW_LIGHT_BUFFER = 10

# Warning, long load times.
# gpt-xl corresponds to the 1558M GPT-2 model version.
TOKENIZER = GPT2Tokenizer.from_pretrained("gpt2-xl")
MODEL = GPT2LMHeadModel.from_pretrained("gpt2-xl")


def _model(input_ids, model, past, p=0.7):  #pylint: disable=invalid-name
    """
    Generate a text component that may fit following the text sample given as input.

    :param str input_ids: input tokens
    :param GPTLMHeadModel model: the ML model to use
    :param torch.Tensor past: the past computational tensor of previous runs
    :param float p: top-p value used for randomization of selection

    :returns: text component that may follow the input text
    :rtype: str
    """
    input_ids = input_ids.unsqueeze(0)
    output, past = model(input_ids, past)
    logits = output[:, -1]
    probs = F.softmax(logits, dim=-1).squeeze()
    idxs = torch.argsort(probs, descending=True)
    res, cumsum = [], 0.
    for idx in idxs:
        res.append(idx)
        cumsum += probs[idx]
        if cumsum > p:
            pred_idx = idxs.new_tensor([choice(res)])
            break
    return pred_idx, past


def speak(starting_text, iterations=PARAGRAPH_LENGTH):
    """
    Return an expanded version of a given starting text with additional text components.
    To make it seem more like real text, this function generates the paragraph to near-completion, then
    continues until a period is generated.

    :param str starting_text: input text to complete
    :param int iterations: number of text components to generate, defaults to module paragraph size

    :returns: expanded text
    :rtype: str
    """
    # Small validation chunk to make sure we actually generate text.
    # Shouldn't be needed when running with default values.
    if iterations < 0:
        iterations = iterations * -1
    if iterations <= YELLOW_LIGHT_BUFFER:
        iterations += YELLOW_LIGHT_BUFFER

    past_cache = None
    word = torch.tensor(TOKENIZER.encode(starting_text))
    generated = TOKENIZER.encode(starting_text)
    # Generate paragraph almost to completion
    for _ in range(0, iterations - YELLOW_LIGHT_BUFFER):
        word, past_cache = _model(word, MODEL, past_cache)
        generated += [word]
    # Continue generating until a period is added
    while "." not in TOKENIZER.decode([word]):
        word, past_cache = _model(word, MODEL, past_cache)
        generated += [word]
    return TOKENIZER.decode(generated)
