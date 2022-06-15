with
    daily_trips as (
        select
        toYYYYMMDD(dropoff_datetime) as day,
        sum(base_passenger_fare) as base_fare
        from trips
        group by toYYYYMMDD(dropoff_datetime)
    ),
    daily_trips_by_location as (
        select
        toYYYYMMDD(dropoff_datetime) as day,
        DOLocationID as location,
        sum(base_passenger_fare) as base_fare
        from trips
        group by toYYYYMMDD(dropoff_datetime), DOLocationID
    )
select d.day, count(*)
from daily_trips d
join daily_trips_by_location dl on d.day = dl.day 
where (dl.base_fare / d.base_fare) > 0.01
group by d.day
order by d.day