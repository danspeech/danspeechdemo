models_dict = {
    "0": "DanSpeech.pth",
    "1": "baseline.pth",
    "2": "augmented_baseline.pth",
    "3": "1conv.pth",
    "4": "3conv32feat.pth",
    "5": "3convs96feat.pth",
    "6": "3RNN.pth",
    "7": "7RNN.pth",
    "8": "9RNN.pth",
    "9": "400units.pth",
    "10": "1200units.pth",
    "11": "1600units.pth",
    "12": "transfer_learning_0.pth",
    "13": "transfer_learning_3.pth",
    "14": "combined_data.pth",
    "15": "librispeech_batch24_continue.pth",
}

lm_dict = {
    "0": "dsl-3gram.klm",
    "1": "dsl-5gram.klm",
    "16": "greedy",
    "2": "wiki-3gram.klm",
    "3": "wiki-5gram.klm",
    "4": "leipzig-3gram.klm",
    "5": "leipzig-5gram.klm",
    "6": "wiki_dsl-3gram.klm",
    "7": "wiki_dsl-5gram.klm",
    "8": "dsl_leipzig-3gram.klm",
    "9": "dsl_leipzig-5gram.klm",
    "10": "wiki_leipzig-3gram.klm",
    "11": "wiki_leipzig-5gram.klm",
    "12": "combined-3gram.klm",
    "13": "combined-5gram.klm",
    "14": "3-gram_en.klm",
    "15": "4-gram_en.klm",
}


def get_danspeech_model(model_identifier):
    if model_identifier == "0":
        from danspeech.pretrained_models import DanSpeechPrimary
        model = DanSpeechPrimary()
        return model
    elif model_identifier == "9":
        from danspeech.pretrained_models import Units400
        model = Units400()
        return model
    else:
        return None


def get_danspeech_lm(lm_identifier):
    if lm_identifier == "0":
        from danspeech.language_models import DSL3gram
        lm = DSL3gram()
        return lm
    elif lm_identifier == "16":
        return "greedy"
    else:
        return None

