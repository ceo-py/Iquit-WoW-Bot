from typing import List, Dict, Any, Optional

try:
    from tortoise.transactions import in_transaction
except ImportError:  # pragma: no cover - environment without tortoise
    in_transaction = None  # type: ignore


RANK_SQL_SINGLE_SERVER = """
WITH ranked AS (
    SELECT cs.id,
           cs.server_id,
           cs.character_id,
           RANK() OVER (
               PARTITION BY cs.server_id
               ORDER BY c.total_rating DESC, c.id ASC
           ) AS rk
    FROM character_server cs
    JOIN character c ON c.id = cs.character_id
    WHERE cs.server_id = $1
),
changes AS (
    SELECT cs.id,
           r.server_id,
           cs.character_id,
           cs.ranking       AS old_ranking,
           r.rk             AS new_ranking
    FROM character_server cs
    JOIN ranked r ON r.id = cs.id
    WHERE cs.ranking IS DISTINCT FROM r.rk
)
UPDATE character_server cs
   SET ranking = ch.new_ranking
  FROM changes ch
 WHERE cs.id = ch.id
RETURNING cs.server_id, cs.character_id, ch.old_ranking, ch.new_ranking;
"""


async def recompute_server_rankings(server_id: int, conn: Optional[Any] = None) -> List[Dict[str, Any]]:
    """
    Recompute rankings for a single server atomically and return changed rows.

    - Takes a transaction-level advisory lock on the server_id to avoid concurrent re-ranks.
    - Uses SQL window function (RANK) to compute ranks by total_rating.
    - Updates only rows whose ranking changed and returns deltas.

    Args:
        server_id: Internal server id (not Discord id).
        conn: Optional transaction connection from tortoise.transactions.in_transaction().
              Pass when calling within an existing transaction to keep add/remove + re-rank atomic.

    Returns:
        List of dicts: {server_id, character_id, old_ranking, new_ranking}
    """
    if in_transaction is None and conn is None:
        raise RuntimeError("recompute_server_rankings requires tortoise in_transaction or a connection")

    if conn is not None:
        # Run inside provided transaction connection
        await conn.execute_query("SELECT pg_advisory_xact_lock($1);", [server_id])
        rows, _ = await conn.execute_query(RANK_SQL_SINGLE_SERVER, [server_id])
        # rows may be a list of tuples; normalize to list of dicts where possible
        return _normalize_rows(rows)

    # Own transaction
    async with in_transaction() as tx:  # type: ignore
        await tx.execute_query("SELECT pg_advisory_xact_lock($1);", [server_id])
        rows, _ = await tx.execute_query(RANK_SQL_SINGLE_SERVER, [server_id])
        return _normalize_rows(rows)


def _normalize_rows(rows: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not rows:
        return out
    for r in rows:
        if isinstance(r, dict):
            out.append(r)
        else:
            # Assume tuple order from SQL RETURNING
            # (server_id, character_id, old_ranking, new_ranking)
            out.append(
                {
                    "server_id": r[0],
                    "character_id": r[1],
                    "old_ranking": r[2],
                    "new_ranking": r[3],
                }
            )
    return out
