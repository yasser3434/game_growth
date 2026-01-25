WITH reg AS (
  SELECT
    DATE(TIMESTAMP_SECONDS(reg_ts)) AS reg_date,
    uid AS unique_id
  FROM `game-growth-478812.staging.registration`
),

auth AS (
  SELECT
    DATE(TIMESTAMP_SECONDS(auth_ts)) AS auth_date,
    uid AS unique_id
  FROM `game-growth-478812.staging.authentification`
),

activity AS (
  SELECT
    auth.unique_id,
    reg.reg_date,
    auth.auth_date,
    DATE_DIFF(auth.auth_date, reg.reg_date, DAY) AS retention_days
  FROM auth
  LEFT JOIN reg
    ON reg.unique_id = auth.unique_id
),

final AS (
  SELECT
    unique_id,
    reg_date,
    auth_date,
    MAX(retention_days) OVER (PARTITION BY unique_id) AS max_retention_date
  FROM activity
)

SELECT
  unique_id,
  reg_date,
  auth_date,
  max_retention_date,
  CASE
    WHEN max_retention_date BETWEEN 2 AND 7   THEN '2 TO 7'
    WHEN max_retention_date BETWEEN 8 AND 30  THEN '8 TO 30'
    WHEN max_retention_date BETWEEN 31 AND 60 THEN '31 TO 60'
    WHEN max_retention_date BETWEEN 61 AND 90 THEN '61 TO 90'
    WHEN max_retention_date BETWEEN 91 AND 120 THEN '91 TO 120'
    WHEN max_retention_date > 120            THEN '+120'
    ELSE CAST(max_retention_date AS STRING)
  END AS groups
FROM final;
