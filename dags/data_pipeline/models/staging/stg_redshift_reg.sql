
SELECT
    reg_datetime
    , uid AS unique_id
FROM {{ source("gg_redshift_source", "registration") }}
