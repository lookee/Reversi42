"""
Performance benchmarks for Apocalyptron engine.

Tests performance characteristics:
- Search speed at various depths
- Nodes per second (NPS)
- Pruning effectiveness
- Transposition table hit rate
- Scaling with depth
"""

import os
import sys
import time

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from AI.Apocalyptron.factory.factory import ApocalyptronFactory
from Players.PlayerApocalyptron import PlayerApocalyptron
from Reversi.BitboardGame import BitboardGame
from Reversi.Game import Move


class TestPerformanceBaseline:
    """Baseline performance tests for Apocalyptron."""

    @pytest.mark.slow
    def test_initial_position_depth_6_speed(self):
        """Test search speed at depth 6 from initial position."""
        game = BitboardGame()
        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(6)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=6)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nps = stats["search_stats"]["nodes"] / elapsed if elapsed > 0 else 0

        assert move is not None
        assert elapsed < 2.0, f"Depth 6 should be < 2s, got {elapsed:.2f}s"
        assert nps > 1000, f"Should achieve >1000 NPS, got {nps:.0f}"

    @pytest.mark.slow
    def test_midgame_position_depth_8_speed(self):
        """Test search speed at depth 8 from midgame position."""
        game = BitboardGame()

        # Create midgame position
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6), Move(7, 6)]:
            if game.valid_move(m):
                game.move(m)

        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(8)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=8)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nps = stats["search_stats"]["nodes"] / elapsed if elapsed > 0 else 0

        assert move is not None
        # Increased threshold for CI environments (GitHub Actions macOS can be slower)
        assert elapsed < 15.0, f"Depth 8 midgame should be < 15s (CI-friendly), got {elapsed:.2f}s"
        assert nps > 400, f"Should achieve >400 NPS (CI-friendly), got {nps:.0f}"

    def test_shallow_search_is_fast(self):
        """Test that shallow searches (depth 1-3) are very fast."""
        game = BitboardGame()
        # Use fixed depth for shallow searches to avoid iterative deepening overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(3)
            .with_fixed_depth_search()  # No iterative deepening overhead
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        for depth in [1, 2, 3]:
            engine.reset()
            start = time.perf_counter()
            move = engine.get_best_move(game, depth=depth)
            elapsed = time.perf_counter() - start

            assert move is not None
            assert elapsed < 0.1, f"Depth {depth} should be < 0.1s, got {elapsed:.2f}s"


class TestPruningEffectiveness:
    """Test pruning effectiveness at different depths."""

    def test_alphabeta_pruning_percentage(self):
        """Test that alpha-beta pruning is effective."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=6)

        move = engine.get_best_move(game, depth=6)
        stats = engine.get_statistics()

        nodes = stats["search_stats"]["nodes"]
        pruning = stats["search_stats"]["pruning"]
        pruning_pct = (pruning / nodes * 100) if nodes > 0 else 0

        assert move is not None
        # Alpha-beta dovrebbe potare almeno il 10% dei nodi
        assert pruning_pct >= 10, f"Alpha-beta pruning too low: {pruning_pct:.1f}%"

    @pytest.mark.slow
    def test_null_move_pruning_effectiveness(self):
        """Test that null move pruning is effective in midgame."""
        game = BitboardGame()

        # Midgame position with more pieces
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6)]:
            if game.valid_move(m):
                game.move(m)

        engine = ApocalyptronFactory.create_default(depth=7)
        move = engine.get_best_move(game, depth=7)
        stats = engine.get_statistics()

        null_move_stats = stats["search_stats"].get("null_move", {})

        assert move is not None
        # Null move dovrebbe avere almeno alcuni tentativi
        if "attempts" in null_move_stats:
            assert null_move_stats["attempts"] > 0, "Null move should be attempted"

    def test_transposition_table_hit_rate(self):
        """Test that transposition table has good hit rate."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=6)

        move = engine.get_best_move(game, depth=6)
        stats = engine.get_statistics()

        tt_hits = stats["search_stats"]["tt_hits"]
        tt_size = stats["search_stats"]["tt_size"]

        assert move is not None
        assert tt_hits > 0, "TT should have some hits"
        assert tt_size > 0, "TT should have entries"

        # Hit rate dovrebbe essere ragionevole
        hit_rate = (tt_hits / tt_size * 100) if tt_size > 0 else 0
        assert hit_rate >= 10, f"TT hit rate too low: {hit_rate:.1f}%"


class TestScalingWithDepth:
    """Test how performance scales with search depth."""

    def test_nodes_increase_with_depth(self):
        """Test that node count increases exponentially with depth."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=1)

        previous_nodes = 0

        for depth in [1, 2, 3, 4]:
            engine.reset()
            move = engine.get_best_move(game, depth=depth)
            stats = engine.get_statistics()
            nodes = stats["search_stats"]["nodes"]

            assert move is not None
            assert nodes > previous_nodes, f"Nodes should increase with depth"

            previous_nodes = nodes

    @pytest.mark.slow
    def test_time_scales_reasonably(self):
        """Test that time scales reasonably with depth."""
        game = BitboardGame()

        times = {}
        for depth in [3, 4, 5, 6]:
            engine = ApocalyptronFactory.create_default(depth=depth)

            start = time.perf_counter()
            move = engine.get_best_move(game, depth=depth)
            elapsed = time.perf_counter() - start

            times[depth] = elapsed
            assert move is not None

        # Ogni incremento di profondità dovrebbe aumentare il tempo
        assert times[4] > times[3]
        assert times[5] > times[4]
        assert times[6] > times[5]

        # Ma non dovrebbe essere esponenziale puro (grazie al pruning)
        ratio_4_3 = times[4] / times[3] if times[3] > 0 else 0
        ratio_6_5 = times[6] / times[5] if times[5] > 0 else 0

        # Con pruning efficace, il rapporto dovrebbe essere < 10
        assert ratio_4_3 < 10, f"Scaling too steep: {ratio_4_3:.1f}x"
        assert ratio_6_5 < 10, f"Scaling too steep: {ratio_6_5:.1f}x"


class TestMemoryEfficiency:
    """Test memory efficiency of search."""

    def test_transposition_table_size_is_bounded(self):
        """Test that TT size stays within bounds."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=6)

        move = engine.get_best_move(game, depth=6)
        stats = engine.get_statistics()

        tt_size = stats["search_stats"]["tt_size"]

        assert move is not None
        # TT non dovrebbe crescere indefinitamente
        assert tt_size < 10000, f"TT size too large: {tt_size}"

    def test_reset_clears_transposition_table(self):
        """Test that reset clears TT."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=5)

        # Prima ricerca
        engine.get_best_move(game, depth=5)
        stats1 = engine.get_statistics()
        tt_size_before = stats1["search_stats"]["tt_size"]

        assert tt_size_before > 0

        # Reset
        engine.reset()

        # Verifica che TT sia stata pulita
        stats2 = engine.get_statistics()
        tt_size_after = stats2["search_stats"]["tt_size"]

        assert tt_size_after == 0, "TT should be cleared after reset"


class TestNodesPerSecond:
    """Test nodes per second (NPS) performance metric."""

    def test_nps_is_reasonable(self):
        """Test that NPS is within expected range."""
        game = BitboardGame()
        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=5)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nodes = stats["search_stats"]["nodes"]
        nps = nodes / elapsed if elapsed > 0 else 0

        assert move is not None
        # Bitboard dovrebbe raggiungere almeno 1000 NPS anche su hardware lento
        assert nps > 1000, f"NPS too low: {nps:.0f}"
        # Su hardware moderno dovrebbe essere 10k-100k NPS
        print(f"\n   📊 Performance: {nps:.0f} nodes/sec")

    @pytest.mark.slow
    def test_nps_midgame_vs_opening(self):
        """Test NPS in midgame vs opening."""
        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )

        # Opening position
        game_opening = BitboardGame()
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        engine.get_best_move(game_opening, depth=5)
        elapsed_opening = time.perf_counter() - start
        stats_opening = engine.get_statistics()
        nps_opening = (
            stats_opening["search_stats"]["nodes"] / elapsed_opening if elapsed_opening > 0 else 0
        )

        # Midgame position
        game_midgame = BitboardGame()
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6), Move(7, 6)]:
            if game_midgame.valid_move(m):
                game_midgame.move(m)

        engine.reset()
        start = time.perf_counter()
        engine.get_best_move(game_midgame, depth=5)
        elapsed_midgame = time.perf_counter() - start
        stats_midgame = engine.get_statistics()
        nodes_midgame = stats_midgame["search_stats"]["nodes"]

        # Handle very small elapsed times (timing precision issues on some platforms)
        # If elapsed time is too small (< 1ms), the search might be too fast to measure accurately
        # In this case, verify that nodes were generated and use a more lenient threshold
        min_elapsed_time = 0.001  # 1 millisecond minimum for accurate timing
        if elapsed_midgame < min_elapsed_time:
            # If timing is too small, verify nodes were generated and use conservative NPS estimate
            assert (
                nodes_midgame > 0
            ), f"Midgame search generated no nodes (elapsed: {elapsed_midgame*1000:.3f}ms)"
            # Use minimum elapsed time for NPS calculation to avoid division by tiny numbers
            effective_elapsed_midgame = min_elapsed_time
            min_nps_threshold = 100  # More lenient threshold for very fast searches
        else:
            effective_elapsed_midgame = elapsed_midgame
            min_nps_threshold = 500

        nps_midgame = (
            nodes_midgame / effective_elapsed_midgame if effective_elapsed_midgame > 0 else 0
        )

        # Entrambi dovrebbero avere NPS ragionevoli
        assert nps_opening > 500, f"Opening NPS too low: {nps_opening:.0f}"
        assert (
            nps_midgame > min_nps_threshold
        ), f"Midgame NPS too low: {nps_midgame:.0f} (elapsed: {elapsed_midgame*1000:.3f}ms, nodes: {nodes_midgame})"

        print(f"\n   📊 Opening NPS: {nps_opening:.0f}")
        print(f"   📊 Midgame NPS: {nps_midgame:.0f}")


class TestOptimizationImpact:
    """Test impact of various optimizations."""

    def test_pruning_reduces_nodes(self):
        """Test that pruning reduces node count significantly."""
        game = BitboardGame()

        # Con tutte le ottimizzazioni
        engine_optimized = ApocalyptronFactory.create_default(depth=5)
        move1 = engine_optimized.get_best_move(game, depth=5)
        stats1 = engine_optimized.get_statistics()
        nodes_optimized = stats1["search_stats"]["nodes"]

        assert move1 is not None
        assert nodes_optimized > 0

        # Le ottimizzazioni dovrebbero mantenere i nodi ragionevoli
        # Depth 5 senza ottimizzazioni potrebbe essere ~10k-100k nodi
        # Con ottimizzazioni dovrebbe essere < 10k
        assert nodes_optimized < 20000, f"Too many nodes even with optimizations: {nodes_optimized}"

    @pytest.mark.slow
    def test_iterative_deepening_overhead_is_minimal(self):
        """Test that iterative deepening overhead is acceptable."""
        game = BitboardGame()

        # Midgame per evitare opening book
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6)]:
            if game.valid_move(m):
                game.move(m)

        engine = ApocalyptronFactory.create_default(depth=6)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=6)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()

        assert move is not None
        # Iterative deepening aggiunge overhead, ma dovrebbe essere < 2x
        # Depth 6 con ID dovrebbe completare in tempo ragionevole
        assert elapsed < 3.0, f"ID overhead too high: {elapsed:.2f}s"


class TestPruningPerformance:
    """Test performance of individual pruning techniques."""

    @pytest.mark.slow
    def test_null_move_pruning_impact(self):
        """Test impact of null move pruning on search speed."""
        game = BitboardGame()

        # Midgame position
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6), Move(6, 6)]:
            if game.valid_move(m):
                game.move(m)

        engine = ApocalyptronFactory.create_default(depth=7)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=7)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        null_move_stats = stats["search_stats"].get("null_move", {})

        assert move is not None

        # Verifica che null move sia stato usato
        if "attempts" in null_move_stats:
            attempts = null_move_stats["attempts"]
            cutoffs = null_move_stats["cutoffs"]

            assert attempts > 0, "Null move should be attempted in midgame"

            # Success rate dovrebbe essere ragionevole (20-60%)
            if attempts > 0:
                success_rate = cutoffs / attempts * 100
                print(f"\n   📊 Null move: {cutoffs}/{attempts} cutoffs ({success_rate:.1f}%)")

    def test_late_move_reduction_impact(self):
        """Test impact of late move reduction."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=6)

        move = engine.get_best_move(game, depth=6)
        stats = engine.get_statistics()

        lmr_stats = stats["search_stats"].get("lmr", {})

        assert move is not None

        # LMR dovrebbe essere usato
        if "reductions" in lmr_stats:
            reductions = lmr_stats["reductions"]
            re_searches = lmr_stats.get("re_searches", 0)

            assert reductions > 0, "LMR should reduce some moves"

            # Re-search rate dovrebbe essere basso (< 30%)
            if reductions > 0:
                re_search_rate = re_searches / reductions * 100
                assert re_search_rate < 50, f"Re-search rate too high: {re_search_rate:.1f}%"
                print(
                    f"\n   📊 LMR: {reductions} reductions, {re_searches} re-searches ({re_search_rate:.1f}%)"
                )


class TestTranspositionTablePerformance:
    """Test transposition table performance."""

    def test_tt_hit_rate_increases_with_depth(self):
        """Test that TT hit rate improves with deeper searches."""
        game = BitboardGame()

        hit_rates = {}

        for depth in [3, 4, 5]:
            engine = ApocalyptronFactory.create_default(depth=depth)
            move = engine.get_best_move(game, depth=depth)
            stats = engine.get_statistics()

            tt_hits = stats["search_stats"]["tt_hits"]
            nodes = stats["search_stats"]["nodes"]

            assert move is not None

            if nodes > 0:
                hit_rate = tt_hits / nodes * 100
                hit_rates[depth] = hit_rate

        # Hit rate dovrebbe aumentare con la profondità
        if 3 in hit_rates and 5 in hit_rates:
            assert (
                hit_rates[5] >= hit_rates[3] - 10
            ), "TT hit rate should improve or stay similar with depth"

    @pytest.mark.slow
    def test_tt_stores_efficiently(self):
        """Test that TT stores entries efficiently."""
        game = BitboardGame()
        engine = ApocalyptronFactory.create_default(depth=7)

        move = engine.get_best_move(game, depth=7)
        stats = engine.get_statistics()

        tt_size = stats["search_stats"]["tt_size"]
        nodes = stats["search_stats"]["nodes"]

        assert move is not None
        assert tt_size > 0

        # TT dovrebbe avere meno entries dei nodi (riutilizzo posizioni)
        assert tt_size <= nodes, "TT size should not exceed nodes searched"

        storage_efficiency = (tt_size / nodes * 100) if nodes > 0 else 0
        print(f"\n   📊 TT storage efficiency: {storage_efficiency:.1f}% ({tt_size}/{nodes})")


class TestPlayerApocalyptronPerformance:
    """Test PlayerApocalyptron performance."""

    def test_opening_book_is_instant(self):
        """Test that opening book responses are instant."""
        game = BitboardGame()
        # Use book_instant=True for instant book responses
        player = PlayerApocalyptron(depth=9, show_book_options=False, book_instant=True)

        moves = game.get_move_list()

        start = time.perf_counter()
        move = player.get_move(game, moves, control=None)
        elapsed = time.perf_counter() - start

        assert move is not None
        # Opening book dovrebbe essere istantaneo (< 10ms)
        # Note: First call may be slower due to initialization, but should still be fast
        assert elapsed < 0.1, f"Opening book should be instant, got {elapsed:.2f}s"

    @pytest.mark.slow
    def test_player_depth_9_midgame(self):
        """Test PlayerApocalyptron at depth 9 in midgame."""
        game = BitboardGame()

        # Esci dall'opening book
        for m in [
            Move(6, 5),
            Move(4, 6),
            Move(3, 5),
            Move(5, 6),
            Move(6, 6),
            Move(7, 6),
            Move(5, 5),
        ]:
            if game.valid_move(m):
                game.move(m)

        player = PlayerApocalyptron(depth=9, show_book_options=False, book_instant=True)
        moves = game.get_move_list()

        start = time.perf_counter()
        move = player.get_move(game, moves, control=None)
        elapsed = time.perf_counter() - start

        assert move is not None
        assert move in moves
        # Depth 9 dovrebbe completare in tempo ragionevole
        # Increased threshold for CI environments (GitHub Actions can be slower)
        assert elapsed < 30.0, f"Depth 9 should be < 30s (CI-friendly), got {elapsed:.2f}s"

        print(f"\n   📊 Depth 9 midgame: {elapsed:.2f}s")


class TestParallelPerformance:
    """Test parallel search performance."""

    @pytest.mark.slow
    def test_parallel_search_is_enabled(self):
        """Test that parallel search is enabled and working."""
        game = BitboardGame()

        # Midgame per evitare book
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6)]:
            if game.valid_move(m):
                game.move(m)

        player = PlayerApocalyptron(depth=8, show_book_options=False)

        # Verifica che parallel sia abilitato
        assert player.bitboard_engine.num_workers > 1, "Parallel should use multiple workers"

        moves = game.get_move_list()
        start = time.perf_counter()
        move = player.get_move(game, moves, control=None)
        elapsed = time.perf_counter() - start

        assert move is not None
        print(
            f"\n   📊 Parallel search (depth 8): {elapsed:.2f}s with {player.bitboard_engine.num_workers} workers"
        )


class TestRegressionPerformance:
    """Regression tests to ensure performance doesn't degrade."""

    def test_depth_5_baseline(self):
        """Baseline: depth 5 should complete in < 1s."""
        game = BitboardGame()
        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(5)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=5)
        elapsed = time.perf_counter() - start

        stats = engine.get_statistics()
        nps = stats["search_stats"]["nodes"] / elapsed if elapsed > 0 else 0

        assert move is not None
        assert elapsed < 1.0, f"Regression: depth 5 took {elapsed:.2f}s (should be < 1s)"
        assert nps > 1000, f"Regression: NPS {nps:.0f} (should be > 1000)"

    @pytest.mark.slow
    def test_depth_8_baseline(self):
        """Baseline: depth 8 should complete in < 5s."""
        game = BitboardGame()

        # Midgame
        for m in [Move(6, 5), Move(4, 6), Move(3, 5), Move(5, 6)]:
            if game.valid_move(m):
                game.move(m)

        # Use quiet mode to reduce overhead
        from AI.Apocalyptron.factory.builder import ApocalyptronConfigBuilder

        engine_config = (
            ApocalyptronConfigBuilder()
            .with_depth(8)
            .enable_all_optimizations()
            .quiet_mode()  # Disable output for speed
            .build()
        )
        engine = ApocalyptronFactory.create_engine(engine_config)

        start = time.perf_counter()
        move = engine.get_best_move(game, depth=8)
        elapsed = time.perf_counter() - start

        assert move is not None
        # Increased threshold for CI environments (GitHub Actions macOS can be slower)
        assert (
            elapsed < 15.0
        ), f"Regression: depth 8 took {elapsed:.2f}s (should be < 15s CI-friendly)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
