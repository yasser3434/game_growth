
WITH distinct_users AS(
    SELECT 
        COUNT(DISTINCT unique_id) AS unique_id_count
    FROM {{ ref("stg_redshift_auth") }} 
    GROUP BY unique_id
)

SELECT
    SUM(unique_id_count) AS TOTAL
FROM distinct_users