import os
import json
import time
import config
import datetime
import csv
import random
from gamelist.WhoIsUndercover.player import Player
from gamelist.WhoIsUndercover.experience_manager import ExperienceManager
from utils import call_api

class Game:

    def __init__(self, civ_count, und_count, civ_word, und_word, logdir):
        self.civ_word = civ_word
        self.und_word = und_word
        self.civ_count = civ_count
        self.und_count = und_count
        self.turn = 1
        self.players = {}
        self.player_alive = set()
        self.logdir = logdir
        self.experience_pool_file = "data/WhoIsUndercover/experience_pool.json"

        # Initialize experience manager for metaphor learning
        self.experience_manager = ExperienceManager(self.experience_pool_file)

        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        self.dialogue_history = [f"Player {i+1}:\n This player has not said anything yet. You should wait for them to speak before considering them.\n " for i in range(civ_count + und_count)]  # 初始化为字符串
        # self.dialogue_history = [["This player has not said anything yet."] for _ in range(civ_count + und_count)]      #成组储存玩家的历史发言
        self.game_history = ""
        self.vote_history = ""
        self.player_csv = [None] * (civ_count + und_count)
        self.initialize_csv()
        self._initialize_players()
        



    def _initialize_players(self):

        role_list = ['civilian'] * self.civ_count + ['undercover'] * self.und_count
        

        random.shuffle(role_list)

        # role_list = ['civilian','civilian','civilian','civilian','undercover', 'undercover']


        player_id = 1
        for role in role_list:
            # assign role
            if role == 'civilian':
                word = self.civ_word
                other_word = self.und_word
                mode = config.WIU_c_mode 
            elif role == 'undercover':
                word = self.und_word
                other_word = self.civ_word
                mode = config.WIU_u_mode
            
            # initialize players
            self.players[player_id] = Player(role, word, mode, player_id, other_word=other_word, csv_name = self.player_csv[player_id - 1])
            self.player_alive.add(player_id)
            player_id += 1



    def start(self) -> bool:

        # game start!

        while True:
            round_dialogue = ""
            round_votes = {}
            turn_vote_history = ""
            self.game_history += f"**round {self.turn}**\n"
            action = 'speak'
            # record the game state
            self.log_game_state('', 'host', '', '', '**speak phase!**')
            self.game_history += f"speaking content:\n"

            player_alive_list = list(self.player_alive)
            random.shuffle(player_alive_list)

            for player_id in player_alive_list:
                dialogue = self.players[player_id].speak(game_history=self.game_history
                                                                , dialogue_history=self.dialogue_history
                                                                , round_dialogue=round_dialogue
                                                                , vote_history = self.vote_history
                                                                , experience_manager = self.experience_manager
                                                                )  

                round_dialogue += f"Player{player_id}: {dialogue} \n"
                # self.dialogue_history[player_id - 1].append((self.turn, dialogue))
                if self.dialogue_history[player_id - 1] == f"Player {player_id}:\n This player has not said anything yet. You should wait for them to speak before considering them.\n ":
                    self.dialogue_history[player_id - 1] = f"Player{player_id}:\n Round 1: {dialogue};  "
                else:
                    self.dialogue_history[player_id - 1] += f"Round {self.turn}: {dialogue};  "

                
                self.game_history += f"Player{player_id}: {dialogue}\n"
                self.log_game_state(self.turn, player_id, self.players[player_id].word, action, dialogue)

            # Record all the round dialogue

            action = 'vote'
            self.log_game_state('', 'host', '', '', '**vote phase!**')
            self.game_history += f"voting result:\n"
            vote_ = ""
            # Vote
            for player_id in self.player_alive.copy():
                vote_result = self.players[player_id].vote( game_history = self.game_history
                                                            ,   dialogue_history=self.dialogue_history
                                                            ,   round_dialogue=round_dialogue
                                                            ,   alive = self.player_alive
                                                            ,   vote_history = self.vote_history
                                                            )  
                if vote_result in round_votes:
                    round_votes[vote_result] += 1
                else:
                    round_votes[vote_result] = 1

                vote_ += f"Round {self.turn}: Player{player_id} has voted player{vote_result}.\n"
                self.log_game_state(self.turn, player_id, self.players[player_id].word, action, vote_result)
                turn_vote_history += f"in round {self.turn}, {player_id} voted {vote_result}\n"

            self.game_history += vote_
            self.vote_history += turn_vote_history

            # Eliminated the player with the most votes
            eliminated_player = self.find_most_voted_player(round_votes)
            if eliminated_player is not None:
                remove = int(eliminated_player)
                self.player_alive.remove(remove)
                host_elimi = f"**The player {eliminated_player} was eliminated!**"
                self.game_history += f"{host_elimi}\n"
                alive_players = ', '.join(map(str, self.player_alive))
                host_alive = f"**Still alive players: {alive_players}**"

                self.log_game_state(self.turn, 'host', '', '', host_elimi)
                self.log_game_state(self.turn, 'host', '', '', host_alive)
            if config.WIU_self_evolving:
                self.experience_improvement()
            if self.turn == 10:
                # Update metaphor experiences based on game results
                self.finalize_experience_updates()
                return True
            
            if self.check_game_end() == 1:
                self.log_game_state('', 'host', '', '', '**Civilians win!**')
                result = f'Civ{config.WIU_c_mode}(winner)_VS_Und{config.WIU_u_mode}'
                new_filename = f'{result}.csv'
                new_csv_filename = os.path.join(self.folder_path, new_filename)
                os.rename(self.csv_filename, new_csv_filename)

                # Update metaphor experiences based on game results
                self.finalize_experience_updates()

                return True
            
            elif self.check_game_end() == -1:
                self.log_game_state('', 'host', '', '', '**Undercovers win!**')
                result = f'Civ{config.WIU_c_mode}_VS_Und{config.WIU_u_mode}(winner)'
                new_filename = f'{result}.csv'
                new_csv_filename = os.path.join(self.folder_path, new_filename)
                os.rename(self.csv_filename, new_csv_filename)

                # Update metaphor experiences based on game results
                self.finalize_experience_updates()

                return False
            else:  
                self.round_dialogue = []
                self.turn += 1
                continue


    def find_most_voted_player(self, votes: dict):

        if not votes:
            return None 

        max_votes = max(votes.values())
        if max_votes == 0:
            return None

        most_voted_players = [player_id for player_id, vote in votes.items() if vote == max_votes]
        if len(most_voted_players) > 1:
            return None 
        else:
            return most_voted_players[0]

    def check_game_end(self) -> int:

        remaining_civilian = sum(1 for player_id in self.player_alive if self.is_civilian(player_id))
        remaining_undercovers = sum(1 for player_id in self.player_alive if self.is_undercover(player_id))

        if remaining_civilian == 1 and remaining_undercovers > 0:
            return -1  
        elif remaining_undercovers == 0:
            return 1  
        return 0

    def is_civilian(self, player_id: int) -> bool:
        return self.players[player_id].role == 'civilian'

    def is_undercover(self, player_id: int) -> bool:
        return self.players[player_id].role == 'undercover'





    def initialize_csv(self):
        time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'game_history_{time_stamp}.csv'
        folder_name = f'game_history_{time_stamp}'
        self.folder_path = os.path.join(self.logdir, folder_name)
        os.makedirs(self.folder_path, exist_ok=True)

        filename = 'game_history.csv'
        self.csv_filename = os.path.join(self.folder_path, filename)
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['round', 'word', 'player_id', 'action', 'details'])

        for i in range(self.civ_count + self.und_count):
            filename = f'player_{i+1}.csv'
            self.player_csv[i] = os.path.join(self.folder_path, filename)
            with open(self.player_csv[i], mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['content'])


    def log_game_state(self, round = '', player_id = '',word = '', action = '', details = ''):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([round, word, player_id, action, details])

    # God perspective methods for metaphor experience management
    def get_player_analysis_content(self, player_id: int, target_metaphor: str = None) -> dict:
        """
        Extract player's analysis content, particularly their understanding of metaphors.
        This provides god's perspective access to player thoughts.
        """
        if player_id not in self.players:
            return {}

        player = self.players[player_id]
        analysis_content = {}

        # Extract from strategy if available
        if hasattr(player, 'strategy') and player.strategy:
            analysis_content['strategy'] = player.strategy

        # Extract from feature analysis if available
        if hasattr(player, 'feature') and player.feature:
            analysis_content['feature'] = player.feature

        # Extract from identity reasoning if available
        if hasattr(player, 'identity') and player.identity:
            analysis_content['identity'] = player.identity

        # Extract metaphor-specific analysis if available
        if hasattr(player, 'reaction') and player.reaction:
            analysis_content['reaction'] = player.reaction

        # Extract metaphor information if this player used one
        if hasattr(player, 'metaphor') and player.metaphor:
            analysis_content['own_metaphor'] = player.metaphor
        if hasattr(player, 'explaination') and player.explaination:
            analysis_content['own_explanation'] = player.explaination

        return analysis_content

    def evaluate_metaphor_success(self, metaphor_user_id: int, metaphor_content: str) -> tuple:
        """
        Evaluate metaphor success from god's perspective.
        Returns (teammate_recognitions, rival_recognitions)
        """
        if metaphor_user_id not in self.players:
            return 0, 0

        user_player = self.players[metaphor_user_id]
        user_word = user_player.word

        teammate_recognitions = 0
        rival_recognitions = 0

        # Analyze each other player's understanding
        for other_id, other_player in self.players.items():
            if other_id == metaphor_user_id:
                continue

            is_teammate = (other_player.word == user_word)
            understanding = self._analyze_player_understanding(other_player, metaphor_content)

            if understanding:
                if is_teammate and understanding.get('teammate_understands', False):
                    teammate_recognitions += 1
                elif not is_teammate and understanding.get('rival_can_guess', False):
                    rival_recognitions += 1

        # Consider voting patterns as additional evidence
        vote_analysis = self._analyze_voting_patterns(metaphor_user_id)
        if vote_analysis:
            teammate_recognitions = max(teammate_recognitions, vote_analysis.get('teammate_support', 0))
            rival_recognitions = max(rival_recognitions, vote_analysis.get('rival_detection', 0))

        # Normalize to binary values
        return (1 if teammate_recognitions > 0 else 0,
                1 if rival_recognitions > 0 else 0)

    def _analyze_player_understanding(self, player, metaphor: str) -> dict:
        """
        Analyze a player's understanding of a metaphor from their written analysis.
        """
        understanding = {'teammate_understands': False, 'rival_can_guess': False}

        # Get player's analysis content
        analysis = self.get_player_analysis_content(player.id)

        # Combine all text sources for analysis
        all_text = ""
        for key, value in analysis.items():
            if isinstance(value, str):
                all_text += value.lower() + " "

        metaphor_lower = metaphor.lower()

        # Heuristic analysis of understanding
        positive_indicators = [
            'understand', 'clear', 'makes sense', 'good metaphor',
            'clever', 'accurate', 'well described', 'gets it'
        ]

        negative_indicators = [
            'confusing', 'unclear', 'doesn\'t make sense', 'bad metaphor',
            'obvious', 'too direct', 'reveals', 'gives away'
        ]

        # Check for understanding indicators
        for indicator in positive_indicators:
            if indicator in all_text and metaphor_lower in all_text:
                understanding['teammate_understands'] = True
                break

        # Check for guess-ability indicators
        for indicator in negative_indicators:
            if indicator in all_text and metaphor_lower in all_text:
                understanding['rival_can_guess'] = True
                break

        # Also check if player mentions specific features that could lead to guessing
        if any(word in all_text for word in ['guess', 'obvious', 'clearly']) and metaphor_lower in all_text:
            understanding['rival_can_guess'] = True

        return understanding

    def _analyze_voting_patterns(self, metaphor_user_id: int) -> dict:
        """
        Analyze voting patterns to infer metaphor effectiveness.
        """
        # This is a simplified analysis - could be enhanced with more sophisticated
        # analysis of voting history and player relationships

        vote_analysis = {'teammate_support': 0, 'rival_detection': 0}

        # For now, return empty analysis
        # In a full implementation, you would:
        # 1. Track who votes for whom over multiple rounds
        # 2. Correlate metaphor usage with subsequent voting patterns
        # 3. Identify if teammates tend to support the metaphor user
        # 4. Identify if rivals tend to target the metaphor user

        return vote_analysis

    def finalize_experience_updates(self):
        """
        Called at game end to update experience pool based on actual game results.
        """
        if hasattr(self.experience_manager, 'update_experiences_from_game'):
            updated_count = self.experience_manager.update_experiences_from_game(self)
            if updated_count > 0:
                print(f"Updated {updated_count} metaphor experiences based on game results")

                # Log experience statistics
                stats = self.experience_manager.get_experience_stats()
                print(f"Experience pool stats: {stats}")

                # Save high-score experiences if enabled
                if config.WIU_self_evolving:
                    self.experience_manager.save_and_reset_high_score_experiences()







