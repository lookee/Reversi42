"""
OpeningBook - Efficient opening book management for Reversi42

This module provides an efficient Trie-based structure to store and query
opening sequences from a book file.
"""

import os

from Reversi.Game import Move


class TrieNode:
    """Node in the opening book trie"""

    def __init__(self):
        self.children = {}  # key: move_str, value: TrieNode
        self.is_end = False  # True if this is the end of a book line


class OpeningBook:
    """
    Efficient opening book using a Trie structure.

    The Trie allows O(m) lookup where m is the length of the move sequence,
    much faster than comparing against all book lines.
    """

    # Opening evaluation constants (parametric)
    ADVANTAGE_WEIGHT = 0.2  # Base weight for advantage evaluation
    VARIETY_WEIGHT = 0.1  # Bonus for variety (more openings = more flexibility)

    def __init__(
        self, book_path=None, advantage_weight=0.2, variety_weight=0.1, only_evaluated_openings=True
    ):
        """
        Initialize the opening book.

        Args:
            book_path: Path to the opening book file. If None, uses default.
            advantage_weight: Weight for advantage evaluation (default: 0.2)
            variety_weight: Weight for variety bonus (default: 0.1)
            only_evaluated_openings: If True, ignore openings without advantage data (default: True)
                                     Note: Openings with '=' are still considered (balanced position)
        """
        self.root = TrieNode()
        self.book_path = book_path
        self.lines_loaded = 0
        self.opening_names = {}  # Map: move_sequence -> opening_name
        self.opening_advantages = {}  # Map: move_sequence -> advantage (=, w, w+, w++, b, b+, b++)
        self.advantage_weight = advantage_weight  # Parametric weight for evaluations
        self.variety_weight = variety_weight  # Parametric weight for variety bonus
        self.only_evaluated_openings = only_evaluated_openings  # Filter non-evaluated openings

        if book_path and os.path.exists(book_path):
            self._load_book(book_path)

    def load_additional_book(self, book_path):
        """
        Load additional opening book file (merges with existing data).

        Args:
            book_path: Path to additional book file
        """
        if book_path and os.path.exists(book_path):
            self._load_book(book_path)

    def _load_book(self, book_path):
        """Load opening book from file into Trie structure"""
        with open(book_path, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue

                # Parse format:
                # FFO format: NAME | MOVES | ADVANTAGE
                # Legacy format: NAME | MOVES
                opening_name = None
                advantage = None

                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]

                    if len(parts) == 3:
                        # FFO format: NAME | MOVES | ADVANTAGE
                        opening_name = parts[0]
                        move_sequence = parts[1]
                        advantage = parts[2]
                    elif len(parts) == 2:
                        # Legacy format: NAME | MOVES
                        opening_name = parts[0]
                        move_sequence = parts[1]
                    else:
                        # Fallback: treat as just moves
                        move_sequence = line
                else:
                    # No pipes: just move sequence
                    move_sequence = line

                # Parse the move sequence
                moves = self._parse_move_sequence(move_sequence)
                if moves:
                    self._add_sequence(moves)
                    # Store opening name and advantage if provided
                    if opening_name:
                        self.opening_names[move_sequence] = opening_name
                    if advantage:
                        self.opening_advantages[move_sequence] = advantage
                    self.lines_loaded += 1

    def _parse_move_sequence(self, sequence):
        """
        Parse a move sequence string into a list of Move objects.

        Format: F5d6C3 (uppercase=black, lowercase=white)
        Returns: [Move('F5'), Move('d6'), Move('C3'), ...]
        """
        moves = []
        i = 0
        while i < len(sequence):
            if sequence[i].isalpha():
                if i + 1 < len(sequence) and sequence[i + 1].isdigit():
                    move_str = sequence[i : i + 2]
                    moves.append(move_str)
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        return moves

    def _add_sequence(self, moves):
        """Add a move sequence to the Trie"""
        node = self.root
        for move_str in moves:
            # Normalize to uppercase for storage (we only care about position, not color)
            normalized = move_str.upper()
            if normalized not in node.children:
                node.children[normalized] = TrieNode()
            node = node.children[normalized]
        node.is_end = True

    def get_book_moves(self, game_history):
        """
        Get all valid book moves for the current position.

        Args:
            game_history: String of moves so far (e.g., "F5d6C3")

        Returns:
            List of Move objects that continue any book line, or empty list
        """
        # Parse the game history
        history_moves = self._parse_move_sequence(game_history)

        # Navigate the Trie to current position
        node = self.root
        for move_str in history_moves:
            normalized = move_str.upper()
            if normalized not in node.children:
                # Position not in book
                return []
            node = node.children[normalized]

        # Get all possible next moves from this position
        book_moves = []
        for move_str in node.children.keys():
            # Convert back to Move object
            try:
                move = self._str_to_move(move_str)
                if move:
                    book_moves.append(move)
            except:
                pass

        return book_moves

    def _str_to_move(self, move_str):
        """
        Convert move string to Move object.

        Args:
            move_str: String like "F5" or "d6"

        Returns:
            Move object with x, y coordinates
        """
        if len(move_str) != 2:
            return None

        col = move_str[0].upper()
        row = move_str[1]

        # Convert column letter to x (A=1, B=2, ..., H=8)
        x = ord(col) - ord("A") + 1
        # Convert row digit to y
        y = int(row)

        return Move(x, y)

    def is_in_book(self, game_history):
        """
        Check if current position is in the opening book.

        Args:
            game_history: String of moves so far

        Returns:
            True if position is in book, False otherwise
        """
        history_moves = self._parse_move_sequence(game_history)
        node = self.root

        for move_str in history_moves:
            normalized = move_str.upper()
            if normalized not in node.children:
                return False
            node = node.children[normalized]

        return True

    def get_opening_names(self, game_history):
        """
        Get the names of all openings that match or extend the current position.

        Args:
            game_history: String of moves so far (e.g., "F5d6C3")

        Returns:
            List of opening names that include this position
        """
        matching_names = []
        history_upper = game_history.upper()

        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            # Check if this opening matches or extends the current position
            if sequence_upper.startswith(history_upper) or history_upper.startswith(sequence_upper):
                matching_names.append(name)

        return matching_names

    def get_remaining_openings(self, game_history):
        """
        Get the names of openings that can still be reached from current position.

        This excludes openings that have already been passed (shorter than current history).

        Args:
            game_history: String of moves so far (e.g., "F5d6C3")

        Returns:
            List of opening names that can still be reached
        """
        remaining_names = []
        history_upper = game_history.upper()

        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            # Only count openings that START WITH current position (can still be reached)
            # Exclude openings where current position starts with them (already passed)
            if sequence_upper.startswith(history_upper):
                remaining_names.append(name)

        return remaining_names

    def get_current_opening_name(self, game_history):
        """
        Get the exact opening name for the current position if it exists.

        Args:
            game_history: String of moves so far

        Returns:
            Opening name if exact match found, None otherwise
        """
        # Try to find exact match
        if game_history in self.opening_names:
            return self.opening_names[game_history]

        # Try uppercase version
        history_upper = game_history.upper()
        for sequence, name in self.opening_names.items():
            if sequence.upper() == history_upper:
                return name

        return None

    def get_opening_names_with_first_move(self, game_history):
        """
        Get all opening names with their first move from current position.

        Args:
            game_history: String of moves so far

        Returns:
            List of tuples: [(first_move, opening_name), ...]
            Sorted by first move, then opening name
        """
        openings_with_first = []
        history_upper = game_history.upper()

        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            # Check if this opening matches or extends the current position
            if sequence_upper.startswith(history_upper) or history_upper.startswith(sequence_upper):
                # Extract first move (first 2 characters of the sequence)
                if len(sequence) >= 2:
                    first_move = sequence[:2].upper()
                    openings_with_first.append((first_move, name))

        # Sort by first move, then by opening name
        return sorted(openings_with_first, key=lambda x: (x[0], x[1]))

    def get_openings_for_move(self, game_history, next_move):
        """
        Get all opening names that include this specific next move.

        Args:
            game_history: Current move sequence (e.g., "" or "F5d6")
            next_move: The next move to check (Move object or string like "F5")

        Returns:
            List of opening names that include this move at this position
        """
        # Convert move to string if needed
        move_str = str(next_move).upper()

        # Build the test sequence
        test_history = game_history.upper() + move_str

        # Find all openings that start with this sequence
        matching_openings = []
        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            if sequence_upper.startswith(test_history):
                matching_openings.append(name)

        return matching_openings

    def get_openings_with_first_move(self, game_history, next_move):
        """
        Get opening info including first move for each opening.

        Args:
            game_history: Current move sequence (e.g., "" or "F5d6")
            next_move: The next move to check (Move object or string like "F5")

        Returns:
            List of tuples: [(first_move, opening_name), ...]
            where first_move is like "F5", "C4", etc.
        """
        # Convert move to string if needed
        move_str = str(next_move).upper()

        # Build the test sequence
        test_history = game_history.upper() + move_str

        # Find all openings that start with this sequence
        openings_info = []
        for sequence, name in self.opening_names.items():
            sequence_upper = sequence.upper()
            if sequence_upper.startswith(test_history):
                # Extract first move (first 2 characters)
                if len(sequence) >= 2:
                    first_move = sequence[:2].upper()
                    openings_info.append((first_move, name))

        return openings_info

    def get_openings_grouped_by_next_move(self, game_history, available_moves):
        """
        Get openings grouped by the next available move.

        Args:
            game_history: Current move sequence
            available_moves: List of Move objects that are currently valid

        Returns:
            Dict: {move_str: [(first_move, opening_name), ...]}
        """
        from collections import defaultdict

        grouped = defaultdict(list)

        for move in available_moves:
            move_str = str(move).upper()

            # Get openings that include this next move
            openings = self.get_openings_with_first_move(game_history, move)

            # Add to group for this move
            for first_move, opening_name in openings:
                grouped[move_str].append((first_move, opening_name))

        return grouped

    def get_opening_advantage(self, game_history):
        """
        Get the advantage evaluation for the current opening.

        Args:
            game_history: Current move sequence

        Returns:
            String indicating advantage (=, w, w+, w++, b, b+, b++) or None
        """
        # Normalize history
        history_upper = game_history.upper()

        # Look for exact match
        for sequence, advantage in self.opening_advantages.items():
            sequence_upper = sequence.upper()
            if history_upper == sequence_upper:
                return advantage

        return None

    def interpret_advantage(self, advantage):
        """
        Interpret advantage string into human-readable format.

        Args:
            advantage: String like '=', 'w', 'w+', 'w++', 'b', 'b+', 'b++'

        Returns:
            Tuple: (description, numeric_value)
            numeric_value: +50 to -50 scale (positive = Black better)
        """
        advantage_map = {
            "=": ("Balanced position", 0),
            "w": ("Black slightly better", 15),
            "w+": ("Black better", 30),
            "w++": ("Black clearly better", 50),
            "b": ("White slightly better", -15),
            "b+": ("White better", -30),
            "b++": ("White clearly better", -50),
        }

        return advantage_map.get(advantage, ("Unknown", 0))

    def get_opening_info_with_advantage(self, game_history):
        """
        Get complete opening information including name and advantage.

        Args:
            game_history: Current move sequence

        Returns:
            Dict with keys: 'name', 'advantage', 'description', 'numeric_value'
            or None if not in book
        """
        # Get opening name
        opening_name = self.get_current_opening_name(game_history)

        if not opening_name:
            return None

        # Get advantage
        advantage = self.get_opening_advantage(game_history)

        # Interpret advantage
        description, numeric_value = ("Unknown", 0)
        if advantage:
            description, numeric_value = self.interpret_advantage(advantage)

        return {
            "name": opening_name,
            "advantage": advantage if advantage else "=",
            "description": description,
            "numeric_value": numeric_value,
        }

    def evaluate_advantage_for_player(self, advantage, player_color):
        """
        Evaluate an advantage symbol for a specific player color.

        Args:
            advantage: Advantage string ('=', 'b', 'b+', 'b++', 'w', 'w+', 'w++', or None)
            player_color: 'B' for Black, 'W' for White

        Returns:
            Float score based on advantage_weight
            Positive = good for player, Negative = bad for player
        """
        if not advantage or advantage == "=":
            return 0.0

        # Define multipliers
        # b = better for White (in FFO notation)
        # w = better for Black (in FFO notation)
        multipliers = {
            "b": 1,
            "b+": 2,
            "b++": 4,
            "w": 1,
            "w+": 2,
            "w++": 4,
        }

        if advantage not in multipliers:
            return 0.0

        multiplier = multipliers[advantage]
        base_score = self.advantage_weight * multiplier

        # Apply sign based on advantage type and player color
        if player_color == "B":  # Black player
            # w = good for Black, b = bad for Black
            if advantage.startswith("w"):
                return base_score  # Positive
            else:  # starts with 'b'
                return -base_score  # Negative
        else:  # White player
            # b = good for White, w = bad for White
            if advantage.startswith("b"):
                return base_score  # Positive
            else:  # starts with 'w'
                return -base_score  # Negative

    def evaluate_move_openings(self, game_history, available_moves, player_color):
        """
        Evaluate all available moves based on their opening advantages.

        Uses HYBRID strategy: AVERAGE + VARIETY_BONUS
        - AVERAGE: Maximize theoretical advantage quality
        - VARIETY_BONUS: Reward moves with more opening options (flexibility)

        Args:
            game_history: Current move sequence
            available_moves: List of Move objects
            player_color: 'B' for Black, 'W' for White

        Returns:
            Dict: {move_str: {'score': float, 'avg': float, 'variety_bonus': float,
                             'openings': int, 'evaluated': int, 'skipped': int, 'details': [...]}}
        """
        evaluations = {}
        max_evaluated = 0  # For normalization

        # First pass: collect all data
        temp_data = {}
        for move in available_moves:
            move_str = str(move).upper()

            # Get all openings for this move
            test_history = game_history.upper() + move_str

            # Find all openings and their advantages
            opening_scores = []
            total_score = 0.0
            openings_count = 0
            evaluated_count = 0
            skipped_count = 0

            for sequence, name in self.opening_names.items():
                sequence_upper = sequence.upper()
                if sequence_upper.startswith(test_history):
                    openings_count += 1

                    # Get advantage for this opening
                    advantage = self.opening_advantages.get(sequence)

                    # Filter based on only_evaluated_openings setting
                    if self.only_evaluated_openings and advantage is None:
                        # Skip openings without advantage data
                        skipped_count += 1
                        continue

                    # Evaluate (Note: '=' is considered as 0.0, which is valid)
                    score = self.evaluate_advantage_for_player(advantage, player_color)

                    opening_scores.append((advantage if advantage else "none", name, score))
                    total_score += score
                    evaluated_count += 1

            max_evaluated = max(max_evaluated, evaluated_count)

            temp_data[move_str] = {
                "sum": total_score,
                "openings": openings_count,
                "evaluated": evaluated_count,
                "skipped": skipped_count,
                "details": opening_scores,
            }

        # Second pass: calculate HYBRID score (AVERAGE + VARIETY_BONUS)
        for move_str, data in temp_data.items():
            evaluated_val = data["evaluated"]
            total_sum_val = data["sum"]
            evaluated = int(evaluated_val) if isinstance(evaluated_val, (int, float)) else 0
            total_sum = float(total_sum_val) if isinstance(total_sum_val, (int, float)) else 0.0

            # Calculate AVERAGE
            avg_score = total_sum / evaluated if evaluated > 0 else 0.0

            # Calculate VARIETY_BONUS (normalized by max openings across all moves)
            variety_bonus = 0.0
            if max_evaluated > 0:
                normalized = float(evaluated) / float(max_evaluated)
                variety_bonus = normalized * self.variety_weight

            # HYBRID SCORE = AVERAGE + VARIETY_BONUS
            hybrid_score = avg_score + variety_bonus

            evaluations[move_str] = {
                "score": hybrid_score,  # Hybrid score for selection
                "avg": avg_score,  # Pure average (for display)
                "variety_bonus": variety_bonus,  # Variety bonus (for display)
                "openings": data["openings"],
                "evaluated": data["evaluated"],
                "skipped": data["skipped"],
                "details": data["details"],
            }

        return evaluations

    def get_best_opening_move(
        self, game_history, available_moves, player_color, show_details=False
    ):
        """
        Get the best move based on opening evaluation.

        Args:
            game_history: Current move sequence
            available_moves: List of Move objects
            player_color: 'B' for Black, 'W' for White
            show_details: If True, print evaluation details

        Returns:
            Best Move object (or random choice if tie)
        """
        import random

        evaluations = self.evaluate_move_openings(game_history, available_moves, player_color)

        if show_details:
            print(f"\n📊 Opening Evaluation (HYBRID Strategy):")
            print(f"   Player: {'Black' if player_color == 'B' else 'White'}")
            print(f"   Advantage weight: {self.advantage_weight}")
            print(f"   Variety weight: {self.variety_weight}")
            if self.only_evaluated_openings:
                print(f"   Filter: Only evaluated openings (with advantage data)")
            else:
                print(f"   Filter: All openings (including non-evaluated)")
            print()
            print(f"   {'Move':<6} {'Score':<8} {'Avg':<8} {'Variety':<8} {'Openings':<12}")
            print(f"   {'-'*6} {'-'*8} {'-'*8} {'-'*8} {'-'*12}")

            # Sort by score descending
            sorted_evals = sorted(evaluations.items(), key=lambda x: x[1]["score"], reverse=True)

            for move_str, eval_data in sorted_evals:
                score = eval_data["score"]
                avg = eval_data["avg"]
                variety = eval_data["variety_bonus"]
                openings = eval_data["openings"]
                evaluated = eval_data["evaluated"]
                skipped = eval_data["skipped"]

                score_str = f"{score:+.4f}"
                avg_str = f"{avg:+.4f}"
                variety_str = f"+{variety:.4f}"

                if self.only_evaluated_openings and skipped > 0:
                    openings_str = f"{evaluated}ev, {skipped}sk"
                else:
                    openings_str = f"{openings} total"

                print(
                    f"   {move_str:<6} {score_str:<8} {avg_str:<8} {variety_str:<8} {openings_str:<12}"
                )

        # Find best score
        if not evaluations:
            # Security: Using random.choice() is appropriate here - not for cryptographic purposes
            # This is for game move selection, not security-sensitive operations
            return random.choice(available_moves) if available_moves else None

        best_score = max(eval_data["score"] for eval_data in evaluations.values())

        # Get all moves with best score (handle ties)
        best_moves = [
            move
            for move in available_moves
            if evaluations[str(move).upper()]["score"] == best_score
        ]

        # Security: Using random.choice() is appropriate here - not for cryptographic purposes
        # This is for game move selection, not security-sensitive operations
        return random.choice(best_moves) if best_moves else random.choice(available_moves)

    def get_statistics(self):
        """Get statistics about the loaded book"""
        return {
            "lines_loaded": self.lines_loaded,
            "total_positions": self._count_nodes(self.root),
            "openings_with_advantage": len(self.opening_advantages),
        }

    def _count_nodes(self, node):
        """Recursively count all nodes in the Trie"""
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count


def get_default_opening_book(
    advantage_weight=0.2, variety_weight=0.1, only_evaluated_openings=True
):
    """
    Get the default opening book instance.

    Automatically loads ALL opening book files from domain/knowledge/data/ directory.
    Files are loaded in alphabetical order.

    Uses HYBRID evaluation strategy: AVERAGE + VARIETY_BONUS
    - AVERAGE: Theoretical advantage quality
    - VARIETY_BONUS: Flexibility (more openings = more tactical options)

    Supported format:
    - NAME | MOVES | ADVANTAGE  (with evaluation)
    - NAME | MOVES              (legacy format)

    Args:
        advantage_weight: Weight for advantage evaluation (default: 0.2)
        variety_weight: Weight for variety bonus (default: 0.1)
        only_evaluated_openings: If True, only use openings with advantage data (default: True)

    Returns:
        OpeningBook instance with all books combined
    """
    import glob

    # Data directory is relative to this module (Clean Architecture: self-contained package)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    books_dir = os.path.join(current_dir, "data")

    # Create empty combined book with specified parameters
    combined_book = OpeningBook(
        advantage_weight=advantage_weight,
        variety_weight=variety_weight,
        only_evaluated_openings=only_evaluated_openings,
    )

    # Find all .txt files in data/ directory (excluding README)
    book_files = glob.glob(os.path.join(books_dir, "*.txt"))
    book_files.sort()  # Alphabetical order

    if not book_files:
        print(f"⚠️  Warning: No opening book files found in {books_dir}")
        return OpeningBook()

    # Display header
    print("\n" + "=" * 80)
    print("📚 LOADING OPENING BOOKS")
    print("=" * 80)

    total_files = 0
    file_stats = []

    for book_file in book_files:
        filename = os.path.basename(book_file)

        # Skip non-opening files
        if "README" in filename.upper():
            continue

        # Load this book
        temp_book = OpeningBook(book_file)

        # Count advantages in this file
        advantages_count = len(temp_book.opening_advantages)

        # Merge into combined book
        if total_files == 0:
            # First file: copy root
            combined_book.root = temp_book.root
        else:
            # Subsequent files: merge trie
            for move, child_node in temp_book.root.children.items():
                if move not in combined_book.root.children:
                    combined_book.root.children[move] = child_node
                # If move exists, the tries will share structure (no duplicates)

        # Merge metadata
        combined_book.opening_names.update(temp_book.opening_names)
        combined_book.opening_advantages.update(temp_book.opening_advantages)
        combined_book.lines_loaded += temp_book.lines_loaded

        # Store stats for this file
        file_stats.append(
            {
                "filename": filename,
                "openings": temp_book.lines_loaded,
                "advantages": advantages_count,
            }
        )

        total_files += 1

    # Display detailed log
    print(f"\n📖 Loaded {total_files} opening book file(s):\n")

    for i, stat in enumerate(file_stats, 1):
        advantages = int(stat["advantages"])
        advantage_info = (
            f", {advantages} with evaluations" if advantages > 0 else ""
        )
        print(f"  {i}. {stat['filename']:<35} {stat['openings']:>4} openings{advantage_info}")

    print(f"\n{'─'*80}")
    print(
        f"📊 TOTAL: {combined_book.lines_loaded} openings, "
        f"{len(combined_book.opening_advantages)} with positional evaluations"
    )
    print("=" * 80 + "\n")

    return combined_book
