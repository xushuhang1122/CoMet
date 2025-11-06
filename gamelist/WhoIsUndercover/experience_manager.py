import json
import os
import random
import copy
from datetime import datetime
from typing import Dict, List, Optional, Any


class ExperienceManager:
    """
    Manages metaphor experiences for Who Is Undercover game.
    Handles recording, updating, and optimizing experiences based on actual game results.
    """

    def __init__(self, experience_pool_file: str = "data/WhoIsUndercover/experience_pool.json"):
        self.experience_pool_file = experience_pool_file
        self.experience_pool: List[Dict[str, Any]] = []
        self.active_metaphors: Dict[int, Dict[str, Any]] = {}  # player_id -> metaphor_info
        self.load_experience_pool()

    def load_experience_pool(self):
        """Load historical experience pool from file."""
        if os.path.exists(self.experience_pool_file):
            try:
                with open(self.experience_pool_file, "r", encoding="utf-8") as f:
                    self.experience_pool = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading experience pool: {e}")
                self.experience_pool = []
        else:
            self.experience_pool = []
            print(f"{self.experience_pool_file} does not exist. Starting with empty experience pool.")

    def save_experience_pool(self):
        """Save experience pool to file."""
        try:
            with open(self.experience_pool_file, "w", encoding="utf-8") as f:
                json.dump(self.experience_pool, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving experience pool: {e}")

    def get_top_experience(self) -> Dict[str, Dict[str, Any]]:
        """Get the highest scoring experience for each method."""
        top_exp = {}
        for exp in self.experience_pool:
            method = exp.get('method')
            if method and exp.get('use') == 0 and exp.get('total_references', 0) > 2:
                if method not in top_exp or exp.get('score', 0) > top_exp[method].get('score', 0):
                    top_exp[method] = exp
        return top_exp

    def get_positive_experience(self, method: str) -> Dict[str, Any]:
        """Get a positive experience (successful case) for the given method."""
        # Prefer high-score experiences
        high_score_exps = [exp for exp in self.experience_pool
                          if exp.get('method') == method and exp.get('score', 0) > 0.5 and exp.get('use') == 0]

        if high_score_exps:
            return random.choice(high_score_exps)

        # Fallback to any positive experience
        all_exps = [exp for exp in self.experience_pool
                   if exp.get('method') == method and exp.get('use') == 0]
        if all_exps:
            return random.choice(all_exps)

        raise ValueError(f"No positive experiences found for method: {method}")

    def get_negative_experience(self, method: str) -> Dict[str, Any]:
        """Get a negative experience (failed case) for the given method."""
        # Prefer high-score experiences
        high_score_exps = [exp for exp in self.experience_pool
                          if exp.get('method') == method and exp.get('score', 0) > 0.5 and exp.get('use') == 1]

        if high_score_exps:
            return random.choice(high_score_exps)

        # Fallback to any negative experience
        all_exps = [exp for exp in self.experience_pool
                   if exp.get('method') == method and exp.get('use') == 1]
        if all_exps:
            return random.choice(all_exps)

        raise ValueError(f"No negative experiences found for method: {method}")

    def get_low_usage_experience(self, method: str) -> Dict[str, Any]:
        """Get an experience with low usage count for the given method."""
        experiences = [exp for exp in self.experience_pool
                      if exp.get('method') == method and exp.get('total_references', 0) < 3]
        if not experiences:
            raise ValueError(f"No low-usage experiences found for method: {method}")
        return random.choice(experiences)

    def record_metaphor_usage(self, player_id: int, word1: str, word2: str, method: str,
                            metaphor: str, explain: str, used_experience_ids: List[str]):
        """Record when a player uses a metaphor in the game."""
        self.active_metaphors[player_id] = {
            'word1': word1,
            'word2': word2,
            'method': method,
            'metaphor': metaphor,
            'explain': explain,
            'used_experience_ids': used_experience_ids,
            'round_used': datetime.now().strftime("%Y%m%d%H%M%S")
        }

    def update_experiences_from_game(self, game_instance) -> int:
        """
        Update experiences based on game results using god's perspective.
        Returns the number of experiences updated.
        """
        if not hasattr(game_instance, 'players') or not self.active_metaphors:
            return 0

        updated_count = 0

        for player_id, metaphor_info in self.active_metaphors.items():
            if player_id not in game_instance.players:
                continue

            player = game_instance.players[player_id]
            if player.role != 'civilian':
                continue  # Only update for civilian players

            # Evaluate metaphor success using game's god perspective
            teammate_recognitions, rival_recognitions = self._evaluate_metaphor_effect(
                game_instance, player_id, metaphor_info
            )

            # Update used experiences
            for exp_id in metaphor_info['used_experience_ids']:
                self._update_experience(exp_id, rival_recognitions, teammate_recognitions)

            # Create new experience
            self._create_new_experience(
                metaphor_info['word1'],
                metaphor_info['word2'],
                metaphor_info['method'],
                rival_recognitions,
                teammate_recognitions,
                metaphor_info['metaphor'],
                metaphor_info['explain']
            )

            updated_count += 1

        # Clean up and optimize
        self.eliminate_low_score_experiences()
        self.save_experience_pool()
        self.active_metaphors.clear()  # Reset for next game

        return updated_count

    def _evaluate_metaphor_effect(self, game_instance, user_player_id: int,
                                 metaphor_info: Dict[str, Any]) -> tuple:
        """
        Evaluate metaphor effect using game's god perspective.
        Returns (teammate_recognitions, rival_recognitions)
        """
        teammate_recognitions = 0
        rival_recognitions = 0

        user_player = game_instance.players[user_player_id]
        user_word = user_player.word

        # Check other players' understanding through their analysis
        for other_id, other_player in game_instance.players.items():
            if other_id == user_player_id:
                continue

            # Check if other player is teammate (same word) or rival (different word)
            is_teammate = (other_player.word == user_word)

            # Try to get understanding from player's analysis or strategy
            understanding = self._extract_player_understanding(
                other_player, metaphor_info['metaphor']
            )

            if understanding:
                if is_teammate and understanding.get('understands_metaphor', False):
                    teammate_recognitions += 1
                elif not is_teammate and understanding.get('can_guess_word', False):
                    rival_recognitions += 1

        # Normalize to binary values (0 or 1)
        teammate_recognitions = 1 if teammate_recognitions > 0 else 0
        rival_recognitions = 1 if rival_recognitions > 0 else 0

        return teammate_recognitions, rival_recognitions

    def _extract_player_understanding(self, player, metaphor: str) -> Optional[Dict[str, bool]]:
        """
        Extract player's understanding of metaphor from their analysis.
        This would need to be implemented based on how player analysis is stored.
        """
        # This is a placeholder - implementation depends on how player analysis is stored
        # You might need to parse player.strategy, player.reaction, or other fields

        # Example implementation (adjust based on actual data structure):
        if hasattr(player, 'strategy') and player.strategy:
            strategy_text = player.strategy.lower()
            metaphor_lower = metaphor.lower()

            # Simple heuristic-based understanding extraction
            understands_metaphor = any(phrase in strategy_text
                                     for phrase in ['understand', 'clear', 'makes sense'])
            can_guess_word = any(phrase in strategy_text
                               for phrase in ['guess', 'obvious', 'clearly']) and metaphor_lower in strategy_text

            return {
                'understands_metaphor': understands_metaphor,
                'can_guess_word': can_guess_word
            }

        return None

    def _update_experience(self, exp_id: str, rival_recognitions: int, teammate_recognitions: int):
        """Update an existing experience based on new usage."""
        SKIP_IDS = {"11", "12", "21", "22", "31", "32"}
        SKIP_IDS2 = {"13", "23", "33"}

        for exp in self.experience_pool:
            if exp.get('id') == exp_id:
                if exp_id in SKIP_IDS:
                    exp['total_references'] += 1
                    exp['teammate_recognitions'] += teammate_recognitions
                    exp['rival_recognitions'] += rival_recognitions
                elif exp_id in SKIP_IDS2:
                    exp['teammate_recognitions'] += teammate_recognitions
                    exp['rival_recognitions'] += rival_recognitions
                    exp['score'] = (exp['teammate_recognitions'] - exp['rival_recognitions']) / exp['total_references']
                else:
                    exp['total_references'] += 1
                    exp['teammate_recognitions'] += teammate_recognitions
                    exp['rival_recognitions'] += rival_recognitions
                    exp['score'] = (exp['teammate_recognitions'] - exp['rival_recognitions']) / exp['total_references']
                break

    def _create_new_experience(self, word1: str, word2: str, method: str,
                             rival_recognitions: int, teammate_recognitions: int,
                             metaphor: str, explain: str):
        """Create a new experience based on game result."""
        if rival_recognitions == 0 and teammate_recognitions == 1:
            use = 0  # Successful case
            score = 1.0
        else:
            use = 1  # Failed case
            score = 0.0

        new_experience = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "words": [word1, word2],
            "use": use,
            "method": method,
            "rival_recognitions": rival_recognitions,
            "teammate_recognitions": teammate_recognitions,
            "total_references": 1,
            "score": score,
            "metaphor": metaphor,
            "explain": explain,
            "comment": ""
        }

        self.experience_pool.append(new_experience)

    def eliminate_low_score_experiences(self):
        """Remove low-score experiences that meet elimination criteria."""
        SKIP_IDS = {"11", "12", "21", "22", "31", "32"}

        self.experience_pool = [
            exp for exp in self.experience_pool
            if exp.get('id') in SKIP_IDS or not (
                (exp.get('total_references', 0) >= 5 and exp.get('score', 0) <= 0.2) or
                (exp.get('total_references', 0) >= 2 and exp.get('score', 0) <= 0)
            )
        ]

    def save_and_reset_high_score_experiences(self):
        """Save high-score experiences and reset their usage counts."""
        high_score_experiences = [
            exp for exp in self.experience_pool
            if exp.get('total_references', 0) >= 3 and exp.get('score', 0) >= 0.2
        ]

        if high_score_experiences:
            high_score_experiences_reset = copy.deepcopy(high_score_experiences)

            for exp in high_score_experiences_reset:
                exp['total_references'] = 0
                exp['teammate_recognitions'] = 0
                exp['rival_recognitions'] = 0
                exp['score'] = 0.0

            # Save to separate file for in-game generation
            high_score_file = os.path.splitext(self.experience_pool_file)[0] + "_ingame_generate.json"
            with open(high_score_file, "w", encoding="utf-8") as f:
                json.dump(high_score_experiences_reset, f, ensure_ascii=False, indent=4)
            print(f"High-score experiences saved to {high_score_file}")

    def get_experience_stats(self) -> Dict[str, Any]:
        """Get statistics about the current experience pool."""
        total_experiences = len(self.experience_pool)
        positive_experiences = sum(1 for exp in self.experience_pool if exp.get('use') == 0)
        negative_experiences = total_experiences - positive_experiences

        method_counts = {
            "ONTOLOGICAL_METAPHOR": 0,
            "STRUCTURAL_METAPHOR": 0,
            "SPATIAL_METAPHOR": 0
        }

        high_score_experiences = 0

        for exp in self.experience_pool:
            method = exp.get('method')
            if method in method_counts:
                method_counts[method] += 1
            if exp.get('score', 0) > 0.5:
                high_score_experiences += 1

        return {
            "total_experiences": total_experiences,
            "positive_experiences": positive_experiences,
            "negative_experiences": negative_experiences,
            "method_counts": method_counts,
            "high_score_experiences": high_score_experiences
        }