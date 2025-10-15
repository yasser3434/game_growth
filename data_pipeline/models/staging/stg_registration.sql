
SELECT
    $1:"reg_datetime"::timestamp AS reg_datetime
    , $1:"reg_ts"::int AS reg_ts
    , $1:"uid"::int AS unique_id
FROM {{ source('gg_snowflake_source', 'registration') }} 