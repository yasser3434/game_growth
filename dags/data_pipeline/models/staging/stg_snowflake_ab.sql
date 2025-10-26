
SELECT
    $1:"revenue"::float AS revenue
    , $1:"testgroup"::varchar AS test_group
    , $1:"user_id"::int AS user_id
FROM {{ source("gg_snowflake_source", "ab_test") }}
