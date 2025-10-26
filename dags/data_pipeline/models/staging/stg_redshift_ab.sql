
SELECT
    revenue
    , user_id AS unique_id
    , testgroup
FROM {{ source("gg_redshift_source", "abtest") }}
