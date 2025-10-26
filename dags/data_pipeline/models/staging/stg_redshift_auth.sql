
SELECT
    auth_datetime
    , uid AS unique_id
FROM {{ source("gg_redshift_source", "authentification") }}
