
------------------------------------- Registration table
WITH reg AS(
    SELECT
        -- CONVERT(DATE, reg_datetime) AS reg_date
        CAST(reg_datetime AS DATE) AS reg_date
        , unique_id
    FROM {{ ref("stg_redshift_reg") }}
),

------------------------------------- Authentification table
auth AS(
    SELECT
        -- CONVERT(DATE, auth_datetime) AS auth_date
        CAST(auth_datetime AS DATE) AS auth_date
        , unique_id
    FROM {{ ref("stg_redshift_auth") }}
),

------------------------------------- Datediff between registration date and authentification date
activity AS(
    SELECT
        auth.unique_id
        , reg_date
        , auth_date
        , DATEDIFF('day', reg_date, auth_date) AS retention_days
    FROM auth
    LEFT JOIN reg ON reg.unique_id = auth.unique_id
),

------------------------------------- Select unique uid and max retention date 
final AS(
    SELECT 
        unique_id
        , reg_date
        , auth_date
        , MAX(retention_days) OVER(PARTITION BY unique_id) AS max_retention_date 
    FROM activity
)


SELECT  
    *
    , CASE 
        WHEN max_retention_date BETWEEN 2 AND 7
            THEN '2 TO 7'
        WHEN max_retention_date BETWEEN 8 AND 30
            THEN '8 TO 30'
        WHEN max_retention_date BETWEEN 31 AND 60
            THEN '31 TO 60'
        WHEN max_retention_date BETWEEN 61 AND 90
            THEN '61 TO 90'
        WHEN max_retention_date BETWEEN 91 AND 120
            THEN '91 TO 120'
        WHEN max_retention_date > 120
            THEN '+120'
        ELSE CAST(max_retention_date AS VARCHAR(10))
    END AS groups
FROM final