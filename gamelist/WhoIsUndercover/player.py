from gamelist.WhoIsUndercover.prompt import base_prompt
from gamelist.WhoIsUndercover.prompt import CoMet as FISA # FISA stands for Feature-Identity-Strategy-Action, which was initially expressed as sych. Finally we call this architecture: CoMet
from gamelist.WhoIsUndercover.prompt import metaphor_prompt
from utils import call_api
import config
import re
import csv
import os
import json
import random


class Player:

    def __init__(
            self, 
            role: str, 
            word: str, 
            mode, 
            id,
            other_word,
            csv_name
    ):
        self.role = role
        self.word = word
        self.other_word = other_word
        self.mode = mode
        if self.role == 'civilian':
            self.model = config.WIU_c_model
        else:
            self.model = config.WIU_u_model
        self.id = id

        self.csv_name = csv_name

        self.categorization = ""
        self.feature = "Right now, the game has just started, you can only guess another word by the original clue:'The two words are similar or related, such as 'pencil' and 'pen', 'apple' and 'orange'.'."
        self.identity = "Right now, the game has just started, all players are still undetermined."
        self.strategy = "Right now, the game has just started, I don't have any strategy."
        self.reaction = ""
        self.metaphor = ""
        self.method = ""
        self.refer_experience_ids = []
        self.explaination = ""


    def log_player_action(self, content):
        # Write content to player's CSV file
        with open(self.csv_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([content])


    def speak(self, *args, game_history=None, dialogue_history = None, round_dialogue = None, vote_history, experience_manager=None, **kwargs) -> str:
        if self.mode == 0:
            return self.player_speaking_cot(self.role, self.word, round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history)
        elif self.mode == 1:
            return self.player_speaking_FISA(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history)
        elif self.mode == 2:
            return self.player_speaking_METAPHOR(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history=vote_history, experience_manager=experience_manager)
        elif self.mode == 3:
            return self.player_speaking_naive(dialogue_history = dialogue_history, vote_history = vote_history)
        elif self.mode == 11 or self.mode == 12 or self.mode == 13 or self.mode == 14:
            return self.player_speaking_FISA_ablation(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history)
        elif self.mode == 1001:
            return self.player_speaking_ToT(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history)
    def vote(self, *args, game_history=None, dialogue_history = None, round_dialogue = None,alive = None,vote_history , **kwargs):
        if self.mode == 0:
            return self.player_voting_cot(game_history=game_history, alive = alive)
        elif self.mode == 1:
            return self.player_voting_FISA(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history, alive=alive)
        elif self.mode == 2:
            return self.player_voting_METAPHOR(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history, alive=alive)
        elif self.mode == 3:
            return self.player_voting_naive(dialogue_history = dialogue_history, vote_history = vote_history, alive = alive)
        elif self.mode == 11 or self.mode == 12 or self.mode == 13 or self.mode == 14:
            return self.player_voting_FISA_ablation(round_dialogue = round_dialogue, game_history = game_history, dialogue_history = dialogue_history, vote_history = vote_history, alive=alive)

    def player_speaking_cot(self, *args, dialogue_history, round_dialogue, game_history, **kwargs):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.analyse(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                game_history = game_history
            )}
        ])
        self.strategy = ret1
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)

        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue_history, analysis = self.strategy
            )}
        ])
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret2}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret2)
        return ret


    def player_voting_cot(self, *args, game_history, alive, **kwargs ):

        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.analyse(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                game_history = game_history
            )}
        ])
        self.strategy = ret1
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)

        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                analysis = self.strategy, alive = alive
            )}
        ])
        self.log_player_action("\n\n\n=========================================   VOTING   =========================================\n\n\n")
        self.log_player_action(ret2)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret2}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int = vot
        return vot_int

    




    def player_speaking_naive(self, dialogue_history, vote_history):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.naive_speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id, dialogue, vote_history
            )}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret1)
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret1}
        ])
        return ret


    def player_voting_naive(self, dialogue_history, vote_history, alive):
        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': base_prompt.system(self.word, self.id)},
            {'role': 'user', 'content': base_prompt.naive_vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,dialogue, vote_history, alive
            )}
        ])
        self.log_player_action("\n\n\n=========================================   ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret1}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int1 = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int1 = vot
        if vot_int1 not in alive:
            vot_int = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': f"{base_prompt.system(self.word, self.id)}\n\nNow you have already decided the final vote target: player {vot_int1}, but you made a mistake that you want to vote a player who was already eliminated. Now, please choose another player who is still alive."},
            {'role': 'user', 'content': ret1}
        ])
        else:
            vot_int = vot_int1
        return vot_int



















    def player_speaking_FISA(self, round_dialogue, game_history, dialogue_history, vote_history):

        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, vote_history = vote_history,
                feature = self.feature
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. the features of the other word mentioned in the input 
            2. all the guesses for the other word; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_
        self.log_player_action("\n\n\n=========================================   FEATURE ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        self.log_player_action("\n\n\nSummarized FEATURE:")
        self.log_player_action(ret1_)



        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history, 
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. allocation of all players, which means the situation of assigning players to teams corresponding to two different words. (pending players should not be on these two teams.)
            2. Which camp do the two words correspond to (CIVILIAN or UNDERCOVER);
            - If either of these is not found, provide the related explanation from the text instead. (Don't say 'not found', just output the required content)
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)


        ret3 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.strategy(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, 
                vote_history = vote_history, feature = self.feature, identity = self.identity
            )}
        ])
        # ret3_ = call_api(input_messages = [
        #     {'role': 'system', 'content': """
        #         summarize the input content, output: 
        #     1. strategy's action;
        #     2. strategy's reason or purpose;
        #     - If either of these is not found, provide the explanation from the text.
        #     - do not have any additional extensions and additions, and the output should all come from the input text.
        #     """},
        #     {'role': 'user', 'content': ret3 }
        # ])
        self.strategy = ret3
        self.log_player_action("\n\n\n=========================================   STRATEGY   =========================================\n\n\n")
        self.log_player_action(ret3)
        # self.log_player_action("\n\n\nSummarized STRATEGY:")
        # self.log_player_action(ret3_)


        ret4 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.speak(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, 
                vote_history = vote_history, strategy = self.strategy, feature=self.feature, identity=self.identity
            )}
        ])
        ret = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                            Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.
            
                                            sample to change the subject:
                                            text:"Pencil is a tool."
                                            output:It is a tool.
            
                                            text:"both two words can be used for writing."
                                            output:it can be used for writing.
            
                                            text:"a common feature is that slender."
                                            output:this thing is slender.
            """},
            {'role': 'user', 'content': ret4}
        ])
        self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
        self.log_player_action(ret4)
        return ret





    def player_voting_FISA(self, round_dialogue, game_history, dialogue_history, vote_history, alive):

        dialogue = "\n".join(dialogue_history)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history, vote_history = vote_history,
                feature = self.feature
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. the features of the other word mentioned in the input 
            2. all the guesses for the other word; 
            - If either of these is not found, provide the explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_
        self.log_player_action("\n\n\n=========================================   FEATURE ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        self.log_player_action("\n\n\nSummarized FEATURE:")
        self.log_player_action(ret1_)



        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history, 
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. allocation of all players, which means assigning players to teams corresponding to two different words. (pending players should not be on two teams.)
            2. camps of all players, which means the judgement about the camps (MAJORITY and MINORITY) corresponding to two words; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)
        

        alive_players = ",".join("player" + str(number) for number in alive)
        ret3 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue =round_dialogue, game_history = game_history, 
                alive= alive_players, feature= self.feature, identity= self.identity
            )}
        ])
        self.log_player_action("\n\n\n=========================================   VOTE   =========================================\n\n\n")
        self.log_player_action(ret3)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret3}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int = vot
        return vot_int



    def player_speaking_METAPHOR(self, round_dialogue, game_history, dialogue_history, vote_history, experience_manager=None):
        self.metaphor = ""
        self.refere_experience_ids = []
        self.explaination = ""
        dialogue = "\n".join(dialogue_history)

        # Step 1: Metaphor pre-screening - analyze each sentence individually
        pre_screen_result = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': metaphor_prompt.metaphor_pre_screening(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id, round_dialogue
            )}
        ])

        # Parse the JSON result to get sentence-level analysis
        try:
            import json
            pre_screen_data = json.loads(pre_screen_result)
            metaphorical_sentences = [s for s in pre_screen_data.get('sentence_analysis', []) if s.get('has_metaphor') == 1]
            has_potential_metaphors = len(metaphorical_sentences) > 0
        except (json.JSONDecodeError, KeyError):
            # Fallback to simple detection if JSON parsing fails
            has_potential_metaphors = "1" in pre_screen_result.lower() or "yes" in pre_screen_result.lower() or "metaphor" in pre_screen_result.lower()
            metaphorical_sentences = []

        if has_potential_metaphors:
            # Step 2: Detailed metaphor analysis for each metaphorical sentence using existing logic
            self_metaphors = []  # Metaphors describing my word (score > threshold)
            other_metaphors = []  # Metaphors not describing my word (score <= threshold)

            for sentence_info in metaphorical_sentences:
                sentence = sentence_info.get('sentence', '')
                reason = sentence_info.get('reason', '')

                # Step 2a: Use existing hypothesis and feature extraction
                sentence_features_result = call_api(model = self.model, input_messages = [
                    {'role': 'system', 'content': FISA.system(self.word, self.id)},
                    {'role': 'user', 'content': metaphor_prompt.hypothesis_and_feature_extraction(
                        config.WIU_c_num, config.WIU_u_num, self.word, self.id, self.feature, sentence
                    )}
                ])

                # Step 2b: Use existing metaphor identification and matching
                sentence_matching_result = call_api(model = self.model, input_messages = [
                    {'role': 'system', 'content': FISA.system(self.word, self.id)},
                    {'role': 'user', 'content': metaphor_prompt.metaphor_identification_and_matching(
                        config.WIU_c_num, config.WIU_u_num, self.word, self.id, sentence_features_result, sentence
                    )}
                ])

                # Step 2c: Use existing score calculation logic
                sentence_judgment = self._calculate_metaphor_score(sentence_features_result, sentence_matching_result)
                score = sentence_judgment['max_score']
                threshold = sentence_judgment['threshold']

                # Step 2d: Classify based on threshold and save matching result
                if score > threshold:
                    self_metaphors.append({
                        'sentence': sentence,
                        'reason': reason,
                        'is_myword': True,
                        'matching_result': sentence_matching_result  # Save JSON result
                    })
                else:
                    other_metaphors.append({
                        'sentence': sentence,
                        'reason': reason,
                        'is_myword': False,
                        'matching_result': sentence_matching_result  # Save JSON result
                    })

            metaphor_judgment = {
                'has_self_metaphors': len(self_metaphors) > 0,
                'self_metaphor_count': len(self_metaphors),
                'other_metaphor_count': len(other_metaphors)
            }

            # Build detailed metaphor analysis info with interpretations
            metaphor_explanations = []

            # Process self metaphors (use matched interpretations)
            for meta in self_metaphors:
                try:
                    import json
                    match_data = json.loads(meta['matching_result'])
                    metaphor_interpretations = match_data.get('metaphor_interpretations', [])

                    if metaphor_interpretations:
                        # Use the first metaphor interpretation
                        interpretation = metaphor_interpretations[0].get('metaphor', meta['sentence'])
                        metaphor_explanations.append(f"Metaphor describing my word: '{meta['sentence']}' means {interpretation}")
                    else:
                        metaphor_explanations.append(f"Metaphor describing my word: '{meta['sentence']}'")
                except:
                    metaphor_explanations.append(f"Metaphor describing my word: '{meta['sentence']}'")

            # Process other metaphors (use first order interpretation)
            for meta in other_metaphors:
                try:
                    import json
                    match_data = json.loads(meta['matching_result'])
                    metaphor_interpretations = match_data.get('metaphor_interpretations', [])

                    # Find interpretation with order=1
                    interpretation = meta['sentence']  # default
                    for interp in metaphor_interpretations:
                        if interp.get('order') == 1:
                            interpretation = interp.get('metaphor', meta['sentence'])
                            break

                    metaphor_explanations.append(f"Other metaphor: '{meta['sentence']}' means {interpretation}")
                except:
                    metaphor_explanations.append(f"Other metaphor: '{meta['sentence']}'")

            # Build comprehensive metaphor analysis info
            metaphor_analysis_info = " | ".join(metaphor_explanations) if metaphor_explanations else "No metaphors detected"
            metaphor_analysis_details = {
                'self_metaphors': self_metaphors,
                'other_metaphors': other_metaphors
            }
        else:
            # No metaphors detected, skip detailed analysis
            metaphor_judgment = {
                'has_self_metaphors': False,
                'self_metaphor_count': 0,
                'other_metaphor_count': 0,
                'total_metaphors': 0
            }
            metaphor_analysis_info = "No potential metaphors detected in dialogue"
            metaphor_analysis_details = {
                'self_metaphors': [],
                'other_metaphors': []
            }

        # Step 3: Feature analysis (both roles, with metaphor analysis as reference if detected)
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': metaphor_prompt.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, feature = self.feature, metaphor_analysis = metaphor_analysis_info
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output:
            1. the features of the other word mentioned in the input
            2. all the guesses for the other word;
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_

        # Step 4: Identity reasoning (both roles)
        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history,
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output:
            1. allocation of all players, which means the situation of assigning players to teams corresponding to two different words. (pending players should not be on these two teams.)
            2. Which camp do the two words correspond to (CIVILIAN or UNDERCOVER);
            - If either of these is not found, provide the related explanation from the text instead. (Don't say 'not found', just output the required content)
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)

        # Step 5: Strategy selection (role-based)
        if self.role == 'undercover':
            # Undercover uses CoMet default strategy
            ret3 = call_api(model = self.model, input_messages = [
                {'role': 'system', 'content': FISA.system(self.word, self.id)},
                {'role': 'user', 'content': FISA.strategy(
                    config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                    dialogue_history = dialogue, round_dialogue = round_dialogue,
                    game_history = game_history, vote_history = vote_history,
                    feature = self.feature, identity = self.identity
                )}
            ])
        else:
            # Civilian uses metaphor-enhanced strategy
            ret3 = call_api(model = self.model, input_messages = [
                {'role': 'system', 'content': FISA.system(self.word, self.id)},
                {'role': 'user', 'content': metaphor_prompt.strategy(
                    config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                    self.feature, self.identity
                )}
            ])

        self.strategy = ret3
        self.log_player_action("\n\n\n=========================================   STRATEGY   =========================================\n\n\n")
        self.log_player_action(ret3)

        # Set reaction to metaphor analysis result
        self.reaction = metaphor_analysis_info

        # Step 6: Role-based speaking decision
        ret3_ = call_api(model = self.model, max_tokens=1, input_messages = [
            {'role': 'system', 'content': """
            Please review a text deploying a speech strategy and check if it mentions using the strategy of "Use Metaphor To speak". If so, output 1. If not, output 0.
            """},
            {'role': 'user', 'content': ret3}
        ])

        if self.role == 'undercover' or ret3_ != '1':
            # Undercover always uses FISA, or Civilian when strategy is not metaphor
            # Use existing analysis results to generate speech directly
            ret4 = call_api(model = self.model, input_messages = [
                {'role': 'system', 'content': FISA.system(self.word, self.id)},
                {'role': 'user', 'content': FISA.speak(
                    config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                    dialogue_history = dialogue, round_dialogue = round_dialogue, game_history = game_history,
                    vote_history = vote_history, strategy = self.strategy, feature=self.feature, identity=self.identity
                )}
            ])
            ret = call_api(model = self.model, input_messages = [
                {'role': 'system', 'content': """Extract the the final speech, remove all explanatory text, title or punctuation marks that does not belong to the speech content.
                                                Then output it without other text. Replace the subject with a third-person pronoun, such us 'It', 'Them','this thing', etc.

                                                sample to change the subject:
                                                text:"Pencil is a tool."
                                                output:It is a tool.

                                                text:"both two words can be used for writing."
                                                output:it can be used for writing.

                                                text:"a common feature is that slender."
                                                output:this thing is slender.

                                                explanatory text sample:
                                                text: This description aligns with... (You should not output text like this)
                                                """},
                {'role': 'user', 'content': ret4}
            ])
            self.log_player_action("\n\n\n=========================================   SPEAK   =========================================\n\n\n")
            self.log_player_action(ret4)
            return ret

        # Civilian uses metaphor generation (continue with existing metaphor generation logic)
        # Use ExperienceManager if available, otherwise fallback to local methods
        if experience_manager:
            example = experience_manager.get_top_experience()

            method_ = call_api(model = self.model, input_messages=[
                {"role": "system", "content": FISA.system(self.word, self.id)},
                {"role": "user", "content": metaphor_prompt.choose_method(self.word,
                                                                        example.get('ONTOLOGICAL_METAPHOR', {}),
                                                                        example.get('STRUCTURAL_METAPHOR', {}),
                                                                        example.get('SPATIAL_METAPHOR', {}), config.WIU_c_num, config.WIU_u_num, self.feature)}
                ])
            method = call_api(model = self.model, input_messages=[
                {"role": "system", "content": """Extract the feature selection and method selection from this text,
                                                output the final feature chosen, start the output with the tag [FEATURE],
                                                output the final method chosen, start the output with the tag [METHOD],
                                                there are three methods to output:
                                                "ONTOLOGICAL_METAPHOR" "STRUCTURAL_METAPHOR" "SPATIAL_METAPHOR"
                                                The output content should come from the original text and cannot be added, deleted, or modified
                                                Output example:
                                                [FEATURE]Speed and Agility[METHOD]SPATIAL_METAPHOR"""},
                {"role": "user", "content": method_}]).strip()
            idx1 = method.find("[FEATURE]") + len("[FEATURE]")
            idx = method.find("[METHOD]")
            feature = method[idx1:idx]
            idx += len("[METHOD]")
            method = method[idx:].strip()
            self.method = method

            # Get experiences from ExperienceManager
            exp_new = experience_manager.get_low_usage_experience(method)
            exp_posi = experience_manager.get_positive_experience(method)
            exp_nega = experience_manager.get_negative_experience(method)

            self.refer_experience_ids = [exp_new["id"], exp_posi["id"], exp_nega["id"]]

            # Generate metaphor
            metaphor0 = call_api(model = self.model, input_messages=[
                        {"role": "system", "content": FISA.system(self.word, self.id)},
                        {"role": "user", "content": metaphor_prompt.generate(config.WIU_c_num, config.WIU_u_num, word = self.word, example1= exp_posi, example2= exp_new, example3= exp_nega, method = method, feature=feature)},
                ])
            content = call_api(model = self.model, input_messages=[
                {"role": "system", "content": """Extract the metaphorical speech content generated from this paragraph, as well as the explanation of the metaphor.
                                                Use [METAPHOR] and [EXPLAIN] as markers to output these two parts of content
                                                The output content should come from the original text and cannot be added, deleted, or modified
                                                Output example:
                                                [METAPHOR]Time is money.[EXPLAIN]Time has a characteristic that is very precious, just like money, they share the same characteristic - preciousness."""},
                {"role": "user", "content": metaphor0}]).strip()
            idx = content.find("[METAPHOR]") + len("[METAPHOR]")
            idx1 = content.find("[EXPLAIN]")
            metaphor = content[idx:idx1]
            idx1 += len("[EXPLAIN]")
            explain = content[idx1:]
            self.metaphor = metaphor
            self.explaination = explain

            # Record metaphor usage with ExperienceManager
            experience_manager.record_metaphor_usage(
                self.id, self.word, self.other_word, method, metaphor, explain, self.refer_experience_ids
            )

            self.log_player_action("\n\n\n=========================================   METAPHOR SPEAK   =========================================\n\n\n")
            self.log_player_action(metaphor0)
            return metaphor
  






    def player_voting_METAPHOR(self, round_dialogue, game_history, dialogue_history, vote_history, alive):

        dialogue = "\n".join(dialogue_history)

        ret0 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': metaphor_prompt.metaphor_analyse(config.WIU_c_num, config.WIU_u_num, self.word, self.id, self.feature, dialogue)}
        ])
        ret0_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
            The input content is a text that detects and infers metaphors in the speech.
            Summarize the input content and output 1. the statements that are judged as metaphors and 2. explanations for them one by one. 
            Don't say anything else, and don't add or modify content. The output should come from the input text.
            If there is no metaphor, output 'NONE'.
            Example 1:
            metaphor: “She is swimming in her tears.”
            explaination:  This sentence uses a metaphorical expression, and its original meaning may be to say that she is very sad.
            Example 2:
            None
            """},
            {'role': 'user', 'content': ret0 }])
        self.reaction = ret0_
        self.log_player_action(ret0)
        # analyse
        ret1 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': metaphor_prompt.feature(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, feature = self.feature, metaphor_analysis = self.reaction
            )}
        ])
        ret1_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. the features of the other word mentioned in the input 
            2. all the guesses for the other word; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret1 }
        ])
        self.feature = ret1_
        self.log_player_action("\n\n\n=========================================   FEATURE ANALYSE   =========================================\n\n\n")
        self.log_player_action(ret1)
        self.log_player_action("\n\n\nSummarized FEATURE:")
        self.log_player_action(ret1_)




        ret2 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.identify(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue = round_dialogue, game_history= game_history, 
                vote_history = vote_history, feature = self.feature
            )}
        ])
        ret2_ = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': """
                summarize the input content, output: 
            1. allocation of all players, which means assigning players to teams corresponding to two different words. (pending players should not be on two teams.)
            2. camps of all players, which means the judgement about the camps (MAJORITY and MINORITY) corresponding to two words; 
            - If either of these is not found, provide the related explanation from the text.
            - do not have any additional extensions and additions, and the output should all come from the input text.
            """},
            {'role': 'user', 'content': ret2 }
        ])
        self.identity = ret2_
        self.log_player_action("\n\n\n=========================================   IDENTITY REASONING   =========================================\n\n\n")
        self.log_player_action(ret2)
        self.log_player_action("\n\n\nSummarized REASONING:")
        self.log_player_action(ret2_)
        

        alive_players = ",".join("player" + str(number) for number in alive)
        ret3 = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': FISA.system(self.word, self.id)},
            {'role': 'user', 'content': FISA.vote(
                config.WIU_c_num, config.WIU_u_num, self.word, self.id,
                dialogue_history = dialogue, round_dialogue =round_dialogue, game_history = game_history, 
                alive= alive_players, feature= self.feature, identity= self.identity
            )}
        ])
        self.log_player_action("\n\n\n=========================================   VOTE   =========================================\n\n\n")
        self.log_player_action(ret3)
        
        vot = call_api(model = self.model, input_messages = [
            {'role': 'system', 'content': "This is the thought process behind the vote; please extract the final vote result, just a number, without any additional content."},
            {'role': 'user', 'content': ret3}
        ])
        if len(vot)>1:
            inp = [{'role': 'system', 'content': "Extract the number from the input content and output it."}]
            inp.append({'role': 'user', 'content': vot})
            vot_int = call_api(model = self.model, input_messages=inp, max_tokens=1)
        else:
            vot_int = vot
        return vot_int



    def _calculate_metaphor_score(self, features_result, matching_result):
        import json
        import config

        try:
            # Parse LLM results
            features_data = json.loads(features_result)
            match_data = json.loads(matching_result)

            # Get configuration weights
            feature_weights = config.WIU_metaphor_feature_weights
            metaphor_weights = config.WIU_metaphor_metaphor_weights
            threshold = config.WIU_metaphor_threshold

            feature_order_weights = {}
            for i, feature in enumerate(features_data['features']):
                order = feature['order'] - 1  # Convert to 0-based index
                if order < len(feature_weights):
                    feature_order_weights[feature['order']] = feature_weights[order]
                else:
                    feature_order_weights[feature['order']] = feature_weights[-1]  # Use minimum weight

            # Assign weights based on association order for metaphor interpretations
            metaphor_order_weights = {}
            for i, interpretation in enumerate(match_data['metaphor_interpretations']):
                order = interpretation['order'] - 1
                if order < len(metaphor_weights):
                    metaphor_order_weights[interpretation['order']] = metaphor_weights[order]
                else:
                    metaphor_order_weights[interpretation['order']] = metaphor_weights[-1]

            # Calculate weighted scores for reasonable combinations
            max_score = 0.0
            for combination in match_data['reasonable_combinations']:
                feature_idx = combination['feature_index']
                interpretation_idx = combination['interpretation_index']
                score = combination['score']

                # Get corresponding weights
                f_weight = feature_order_weights.get(feature_idx, feature_weights[-1])
                m_weight = metaphor_order_weights.get(interpretation_idx, metaphor_weights[-1])

                # Calculate weighted score
                weighted_score = f_weight * m_weight * score
                max_score = max(max_score, weighted_score)

            # Threshold judgment
            is_metaphor = max_score > threshold

            return {
                'is_metaphor': is_metaphor,
                'max_score': max_score,
                'threshold': threshold
            }

        except Exception as e:
            # Error handling: default to no metaphor detected
            return {
                'is_metaphor': False,
                'max_score': 0.0,
                'threshold': config.WIU_metaphor_threshold,
                'error': str(e)
            }









