""" a module to generate random sentences """
import random

RANDOM_SENTENCES = (
    "Ok mon canard! Je crois que j'en ai entendu parler.",
    "Bien sûr que je peux t'en parler mon poussin !",
    "Attend, je vais chercher dans mes vieux grimoires...",
    "Je vais tâcher de ne pas te raconter carabistouilles.",
)


def get_random_sentence():
    random_index = random.randrange(len(RANDOM_SENTENCES))
    return RANDOM_SENTENCES[random_index]
