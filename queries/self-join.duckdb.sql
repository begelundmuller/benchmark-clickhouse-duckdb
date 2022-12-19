with
    daily_trips as (
        select
        cast(dropoff_datetime as date) as day,
        sum(base_passenger_fare) as base_fare
        from trips
        group by day
    ),
    daily_trips_by_location as (
        select
        cast(dropoff_datetime as date) as day,
        DOLocationID as location,
        sum(base_passenger_fare) as base_fare
        from trips
        group by day, location
    )
select d.day, count(*)
from daily_trips d
join daily_trips_by_location dl on d.day = dl.day 
where (dl.base_fare / d.base_fare) > 0.01
group by d.day
order by d.day
