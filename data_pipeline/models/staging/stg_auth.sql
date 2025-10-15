
SELECT
    $1:"auth_datetime"::timestamp AS auth_datetime
    , $1:"auth_ts"::int AS auth_ts
    , $1:"uid"::int AS unique_id
FROM {{ source("gg_snowflake_source", "auth") }}
