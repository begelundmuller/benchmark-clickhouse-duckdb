select
    toYYYYMMDD(request_datetime) as day,
    uniqHLL12(PULocationID) as locations,
    count(*) as trips,
    sum(base_passenger_fare) + sum(sales_tax) + sum(tolls) + sum(tips) as revenue
from trips
where trip_miles > 5
group by day
order by day
