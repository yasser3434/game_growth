
SELECT 
    COUNT(DISTINCT unique_id) AS TOTAL
FROM {{ ref("stg_auth") }} 
GROUP BY unique_id