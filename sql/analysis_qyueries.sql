/* =========================================================
   NCAA FOOTBALL – ANALYSIS QUERIES
   ========================================================= */


/* ---------------------------------------------------------
1. Teams that maintained TOP 5 rankings across MULTIPLE seasons
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    COUNT(DISTINCT s.year) AS seasons_in_top_5
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
JOIN seasons s ON r.season_id = s.season_id
WHERE r.rank <= 5
GROUP BY t.team_id, team_name
HAVING COUNT(DISTINCT s.year) >= 2
ORDER BY seasons_in_top_5 DESC;


/* ---------------------------------------------------------
2. Average ranking points per team by season
--------------------------------------------------------- */
SELECT
    s.year,
    t.market || ' ' || t.name AS team_name,
    ROUND(AVG(r.points), 2) AS avg_points
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
JOIN seasons s ON r.season_id = s.season_id
GROUP BY s.year, t.team_id, team_name
ORDER BY s.year, avg_points DESC;


/* ---------------------------------------------------------
3. Total first-place votes per team across all weeks
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    SUM(r.fp_votes) AS total_first_place_votes
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
GROUP BY t.team_id, team_name
ORDER BY total_first_place_votes DESC;


/* ---------------------------------------------------------
4. Players who appeared in MULTIPLE seasons for the SAME team
--------------------------------------------------------- */
SELECT
    p.first_name || ' ' || p.last_name AS player_name,
    t.market || ' ' || t.name AS team_name,
    COUNT(DISTINCT s.year) AS seasons_played
FROM player_statistics ps
JOIN players p ON ps.player_id = p.player_id
JOIN teams t ON ps.team_id = t.team_id
JOIN seasons s ON ps.season_id = s.season_id
GROUP BY p.player_id, t.team_id, player_name, team_name
HAVING COUNT(DISTINCT s.year) > 1
ORDER BY seasons_played DESC;


/* ---------------------------------------------------------
5. Most common player positions and distribution across teams
--------------------------------------------------------- */
SELECT
    position,
    COUNT(*) AS total_players
FROM players
GROUP BY position
ORDER BY total_players DESC;


/* ---------------------------------------------------------
6. Player position distribution PER TEAM
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    p.position,
    COUNT(*) AS player_count
FROM players p
JOIN teams t ON p.team_id = t.team_id
GROUP BY team_name, p.position
ORDER BY team_name, player_count DESC;


/* ---------------------------------------------------------
7. Teams with MOST weeks ranked #1
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    COUNT(*) AS weeks_at_rank_1
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
WHERE r.rank = 1
GROUP BY t.team_id, team_name
ORDER BY weeks_at_rank_1 DESC;


/* ---------------------------------------------------------
8. Teams with BIGGEST average rank improvement week-over-week
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    ROUND(AVG(r.prev_rank - r.rank), 2) AS avg_rank_improvement
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
WHERE r.prev_rank IS NOT NULL
GROUP BY t.team_id, team_name
ORDER BY avg_rank_improvement DESC;


/* ---------------------------------------------------------
9. Average wins and losses per team (from rankings data)
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    ROUND(AVG(r.wins), 2) AS avg_wins,
    ROUND(AVG(r.losses), 2) AS avg_losses
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
GROUP BY t.team_id, team_name
ORDER BY avg_wins DESC;


/* ---------------------------------------------------------
10. Top rushing players by season
--------------------------------------------------------- */
SELECT
    s.year,
    p.first_name || ' ' || p.last_name AS player_name,
    SUM(ps.rushing_yards) AS total_rushing_yards
FROM player_statistics ps
JOIN players p ON ps.player_id = p.player_id
JOIN seasons s ON ps.season_id = s.season_id
GROUP BY s.year, p.player_id, player_name
ORDER BY s.year, total_rushing_yards DESC;


/* ---------------------------------------------------------
11. Top receiving players by season
--------------------------------------------------------- */
SELECT
    s.year,
    p.first_name || ' ' || p.last_name AS player_name,
    SUM(ps.receiving_yards) AS total_receiving_yards
FROM player_statistics ps
JOIN players p ON ps.player_id = p.player_id
JOIN seasons s ON ps.season_id = s.season_id
GROUP BY s.year, p.player_id, player_name
ORDER BY s.year, total_receiving_yards DESC;


/* ---------------------------------------------------------
12. Conferences ranked by average team ranking
--------------------------------------------------------- */
SELECT
    c.name AS conference_name,
    ROUND(AVG(r.rank), 2) AS avg_rank
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
JOIN conferences c ON t.conference_id = c.conference_id
GROUP BY c.name
ORDER BY avg_rank ASC;


/* ---------------------------------------------------------
13. Venues with the highest average-ranked teams
--------------------------------------------------------- */
SELECT
    v.name AS venue_name,
    ROUND(AVG(r.rank), 2) AS avg_team_rank
FROM rankings r
JOIN teams t ON r.team_id = t.team_id
JOIN venues v ON t.venue_id = v.venue_id
GROUP BY v.name
ORDER BY avg_team_rank ASC;


/* ---------------------------------------------------------
14. Player eligibility breakdown (FR, SO, JR, SR)
--------------------------------------------------------- */
SELECT
    eligibility,
    COUNT(*) AS total_players
FROM players
GROUP BY eligibility
ORDER BY total_players DESC;


/* ---------------------------------------------------------
15. Teams with the MOST players drafted across seasons
(Proxy: players appearing in many seasons)
--------------------------------------------------------- */
SELECT
    t.market || ' ' || t.name AS team_name,
    COUNT(DISTINCT ps.player_id) AS total_players
FROM player_statistics ps
JOIN teams t ON ps.team_id = t.team_id
GROUP BY t.team_id, team_name
ORDER BY total_players DESC;
