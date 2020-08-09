import spacy
# import en_core_web_md # Install with python3 -m spacy download en_core_web_sm
from spacy.symbols import nsubj, VERB
from spew import Text
from customclass import *
import random
import neuralcoref
from strsimpy.optimal_string_alignment import OptimalStringAlignment
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

class Tagger():
    battle_trigger = ['fight', 'slit', 'cut']
    battle_verb = ['throw', 'use', 'cure', 'shoot']
    battle_word = battle_verb+battle_trigger

    trade_trigger = ['trade', 'give', 'exchange']
    trade_verb = ['find', 'take', 'search']

    quest_trigger = ['talk', 'ask', '"']
    quest_verb = []

    nlp = None
    optimal_string_alignment = OptimalStringAlignment()

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        neuralcoref.add_to_pipe(self.nlp)
        self.nlp.add_pipe(WordnetAnnotator(self.nlp.lang))
        merge_nps = self.nlp.create_pipe("merge_noun_chunks")
        self.nlp.add_pipe(merge_nps)
        f = open('data/battle_trigger.txt', 'r+')
        self.battle_trigger = [line for line in f.readlines()]
        f.close()

    def tag(self, sentence = "My friend shoots a bullet as I throw myself at him."):
        tokenized = self.nlp(sentence)

        trigger_mode = {'NONE': True, 'BATTLE': False, 'TRADE': False, 'QUEST': False}

        def set_mode(name = 'NONE'):
            trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
            trigger_mode[name] = True

        for token in tokenized:
            if token.dep == nsubj and token.head.pos == VERB:
                print(token.text)
                for ancestor in token.ancestors:
                    if ancestor.lemma_ in self.battle_trigger:
                        print("↑ [BATTLE]")
                        trigger_mode = {'NONE': False, 'BATTLE': False, 'TRADE': False, 'QUEST': False}
                        trigger_mode['BATTLE'] = True

        return trigger_mode

    def extract(self, sentence):
        '''
        Extracts subject, verb & object.
        '''
        tokenized = self.nlp(sentence)
        return tokenized

    def pick_pos(self, POS, sentence):
        tokens_with_pos = []
        for token in self.extract(sentence):
            #print(token.text)
            if token.pos == POS:
                tokens_with_pos.append(token)
        return tokens_with_pos

    def pick_subj(self, sentence):
        subjects = []
        for token in self.extract(sentence):
            #print(token.text)
            if token.dep == nsubj:
                subjects.append(token.text)
        return subjects

    def similarity(self, origin, target):
        if not isinstance(target, spacy.tokens.token.Token):
            token = self.nlp(target)[-1]
        synonyms = set()
        for i in token._.wordnet.synsets():
            synonyms = synonyms.union(i.lemma_names())
        distances = [self.optimal_string_alignment.distance(origin, synonym) for synonym in synonyms]
        print(distances)
        if len(distances) == 0 or len(str(target)) > 10: # A big red car
            distances.append(self.optimal_string_alignment.distance(origin, target))
        try:
            return 1/min(distances)
        except TypeError:
            print('ORIGIN TYPE', type(origin), '. TARGET TYPE', type(target))

    def entity(self, name, Scene: Scene, certainty=0.7):
        """
        Returns an entity(a Character class) best matching from current Scene
        plain(a tree), named($PLAYER_NAME), or related(dragon)

        For plain items, a 'suitable' character with 0 attributes will be returned.

        *Greedily searches word with closest similarity*
        """
        x = str(name)
        score = {i: self.similarity(i.name, x) for i in Scene.characters}
        score.update({
            i: self.similarity(i.name, x) for player in Scene.players for i in [player.name] + player.alt_names})
        score.update({i: self.similarity(i.name, x) for i in Scene.objects})
        probable_item = max(score.items(), key=lambda x: x[1])
        print('Chose', str(probable_item[0]), probable_item[1])
        if probable_item[1] < certainty:
            print('Not certain @ ',score)
            result_character = Character(name=name)
            return result_character
        return probable_item[0]


    def generate_prompt(self, generator: Text, tag, status: World, length=300):
        '''
        Generates a prompt describing the current situation
        '''
        prompt = status.world_prompt
        # SUBJ[당시 턴이었던] VERB ACTION . SUBJ[Player] VERB[Result]
        prompt += status.current_situation_prompt + ". " + str(status.current_turn_character) + status.pc_action
        generator.generate(prompt, length)

    def uses_item(action):
        return False

if __name__ == "__main__":
    """
    TEST CODE
    """
    tag_test = Tagger()
    Scene_test = Scene()
    Scene_test.characters.append(Character(name="the wizard"))
    Scene_test.characters.append(Character(name="King Jorg the third"))
    Scene_test.characters.append(Character(name="You"))
    while True:
        i = input()
        print(str(tag_test.entity(name=i, Scene=Scene_test)))
