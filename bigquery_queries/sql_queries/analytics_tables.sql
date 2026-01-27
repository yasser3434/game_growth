
#StandardSQL

CREATE TABLE `PROJECT_ID.analytics.auth` AS (

    SELECT  
        DATE(DATETIME_SECONDS(auth_ts)) AS date_auth
        , uid AS user_id
    FROM `PROJECT_ID.raw.auth`

)
