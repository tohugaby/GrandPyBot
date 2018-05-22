from webapp.sentences_generator import get_random_sentence


def test_random_sentences():
    sentence = get_random_sentence()
    assert isinstance(sentence, str)
