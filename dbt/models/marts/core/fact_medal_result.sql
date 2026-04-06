with medals as (
    select * from {{ref("stg_Milano_26__medals_winter26")}}
),

medallists as (
    select * from {{ ref("stg_Milano_26__medallists_winter26") }}
),
