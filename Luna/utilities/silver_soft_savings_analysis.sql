select * from

(
select
  case
  when billed_year_kwh > 40000 then t.year_40000_kwh/40000
  when billed_year_kwh > 30000 then t.year_30000_kwh/30000
  when billed_year_kwh > 25000 then t.year_25000_kwh/25000
  when billed_year_kwh > 20000 then t.year_20000_kwh/20000
  when billed_year_kwh > 15000 then t.year_15000_kwh/15000
  when billed_year_kwh > 14000 then t.year_14000_kwh/14000
  when billed_year_kwh > 13000 then t.year_13000_kwh/13000
  when billed_year_kwh > 12000 then t.year_12000_kwh/12000
  when billed_year_kwh > 11000 then t.year_11000_kwh/11000
  when billed_year_kwh > 10000 then t.year_10000_kwh/10000
  when billed_year_kwh > 9000 then t.year_9000_kwh/9000
  when billed_year_kwh > 8000 then t.year_8000_kwh/8000
  when billed_year_kwh > 7000 then t.year_7000_kwh/7000
  when billed_year_kwh > 6000 then t.year_6000_kwh/6000
  when billed_year_kwh > 5000 then t.year_5000_kwh/5000
  when billed_year_kwh > 4000 then t.year_4000_kwh/4000
  when billed_year_kwh > 3000 then t.year_3000_kwh/3000
  when billed_year_kwh > 2000 then t.year_2000_kwh/2000
  when billed_year_kwh > 1000 then t.year_1000_kwh/1000
  when billed_year_kwh >= 0 then t.year_0_kwh + ((t.year_1000_kwh-t.year_0_kwh)/1000)
end pre_solar_year_cost_per_kwh,
case
  when billed_year_kwh > 40000 then st.year_40000_kwh/40000
  when billed_year_kwh > 30000 then st.year_30000_kwh/30000
  when billed_year_kwh > 25000 then st.year_25000_kwh/25000
  when billed_year_kwh > 20000 then st.year_20000_kwh/20000
  when billed_year_kwh > 15000 then st.year_15000_kwh/15000
  when billed_year_kwh > 14000 then st.year_14000_kwh/14000
  when billed_year_kwh > 13000 then st.year_13000_kwh/13000
  when billed_year_kwh > 12000 then st.year_12000_kwh/12000
  when billed_year_kwh > 11000 then st.year_11000_kwh/11000
  when billed_year_kwh > 10000 then st.year_10000_kwh/10000
  when billed_year_kwh > 9000 then st.year_9000_kwh/9000
  when billed_year_kwh > 8000 then st.year_8000_kwh/8000
  when billed_year_kwh > 7000 then st.year_7000_kwh/7000
  when billed_year_kwh > 6000 then st.year_6000_kwh/6000
  when billed_year_kwh > 5000 then st.year_5000_kwh/5000
  when billed_year_kwh > 4000 then st.year_4000_kwh/4000
  when billed_year_kwh > 3000 then st.year_3000_kwh/3000
  when billed_year_kwh > 2000 then st.year_2000_kwh/2000
  when billed_year_kwh > 1000 then st.year_1000_kwh/1000
  when billed_year_kwh >= 0 then st.year_0_kwh + ((st.year_1000_kwh-st.year_0_kwh)/1000)
end subsidized_pre_solar_year_cost_per_kwh,
  p.service_name,
  c.full_name,
  c.email,
  p.service_address,
  p.service_city,
  p.service_state,
  p.service_zip_code,
  date_trunc(day, p.start_billing),
    case
        when upper(p.utility_schedule_rate) like '%CARE%' and p.service_state = 'CA' then p.utility_company||' - CARE'
        when upper(p.utility_schedule_rate) like '%FERA%' and p.service_state = 'CA' then p.utility_company||' - FERA'
        else p.utility_company
    end utility_company,
  iff(p.utility_schedule_rate ilike '%care%', subsidized_pre_solar_year_cost_per_kwh, pre_solar_year_cost_per_kwh),
  ct.record_type
from rpt.t_contact c,
  (
    select * from
  (
    select
project_id,
project_name,
start_date,
billed_wh,sum(billed_wh) over (partition by project_id order by start_date rows between 11 preceding and current row)/1000 billed_year_kwh,
sum(iff(billing_method = 'Estimated',billed_wh,null)) over (partition by project_id order by start_date rows between 11 preceding and current row)/1000 estimated_billed_year_kwh,
sum(1) over  (partition by project_id order by start_date rows between 11 preceding and current row) month_cnt
    from
fleet.t_combined_monthly where is_all_month --and project_name = 'SP-3180141'
    )
  where month_cnt = 12 and start_date = dateadd('month',-1,date_from_parts(year(current_date()),month(current_date()),1))
  )
  cm,
rpt.t_project p,
rpt.t_contract ct,

(
select * from
(
  select t.*,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
  customer_likelihood is not null
  )
  where
  row_cnt2 = 1
)
t,
(
select * from
(
  select t.*,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
  customer_likelihood is not null and
  is_subsidized = 'True'
  )
  where
  row_cnt2 = 1
)
st


where
p.contract_signer = c.contact_id and
p.project_id = cm.project_id(+) and
p.primary_contract_id = ct.contract_id and
substring(p.service_zip_code,0,5) = t.zipcode and
substring(p.service_zip_code,0,5) = st.zipcode(+) and
p.service_number = '{service_number}'

order by p.project_id
);with save as (select * from

(
select cm2.start_date,
p.project_id,
p.project_name,
p.start_billing start_billing_complete,
to_date(p.ELECTRICAL_FINISH_DATE) electrician_complete,
t.tariff_name,
t.tariff_code,
st.tariff_code subsidized_tariff_code,
t.climate_zone_name,
t.customer_likelihood,
t.is_subsidized,
ct.contract_rate,
billed_year_kwh,
estimated_billed_year_kwh,
ct.contract_rate * billed_year_kwh billed_year_cost,
ct.contract_rate * estimated_billed_year_kwh estimated_billed_year_cost,
case
  when billed_year_kwh > 40000 then t.year_40000_kwh/40000
  when billed_year_kwh > 30000 then t.year_30000_kwh/30000
  when billed_year_kwh > 25000 then t.year_25000_kwh/25000
  when billed_year_kwh > 20000 then t.year_20000_kwh/20000
  when billed_year_kwh > 15000 then t.year_15000_kwh/15000
  when billed_year_kwh > 14000 then t.year_14000_kwh/14000
  when billed_year_kwh > 13000 then t.year_13000_kwh/13000
  when billed_year_kwh > 12000 then t.year_12000_kwh/12000
  when billed_year_kwh > 11000 then t.year_11000_kwh/11000
  when billed_year_kwh > 10000 then t.year_10000_kwh/10000
  when billed_year_kwh > 9000 then t.year_9000_kwh/9000
  when billed_year_kwh > 8000 then t.year_8000_kwh/8000
  when billed_year_kwh > 7000 then t.year_7000_kwh/7000
  when billed_year_kwh > 6000 then t.year_6000_kwh/6000
  when billed_year_kwh > 5000 then t.year_5000_kwh/5000
  when billed_year_kwh > 4000 then t.year_4000_kwh/4000
  when billed_year_kwh > 3000 then t.year_3000_kwh/3000
  when billed_year_kwh > 2000 then t.year_2000_kwh/2000
  when billed_year_kwh > 1000 then t.year_1000_kwh/1000
  when billed_year_kwh >= 0 then t.year_0_kwh + ((t.year_1000_kwh-t.year_0_kwh)/1000)
end pre_solar_year_cost_per_kwh,

case
  when billed_year_kwh > 40000 then billed_year_kwh*t.year_40000_kwh/40000
  when billed_year_kwh > 30000 then billed_year_kwh*t.year_30000_kwh/30000
  when billed_year_kwh > 25000 then billed_year_kwh*t.year_25000_kwh/25000
  when billed_year_kwh > 20000 then billed_year_kwh*t.year_20000_kwh/20000
  when billed_year_kwh > 15000 then billed_year_kwh*t.year_15000_kwh/15000
  when billed_year_kwh > 14000 then billed_year_kwh*t.year_14000_kwh/14000
  when billed_year_kwh > 13000 then billed_year_kwh*t.year_13000_kwh/13000
  when billed_year_kwh > 12000 then billed_year_kwh*t.year_12000_kwh/12000
  when billed_year_kwh > 11000 then billed_year_kwh*t.year_11000_kwh/11000
  when billed_year_kwh > 10000 then billed_year_kwh*t.year_10000_kwh/10000
  when billed_year_kwh > 9000 then billed_year_kwh*t.year_9000_kwh/9000
  when billed_year_kwh > 8000 then billed_year_kwh*t.year_8000_kwh/8000
  when billed_year_kwh > 7000 then billed_year_kwh*t.year_7000_kwh/7000
  when billed_year_kwh > 6000 then billed_year_kwh*t.year_6000_kwh/6000
  when billed_year_kwh > 5000 then billed_year_kwh*t.year_5000_kwh/5000
  when billed_year_kwh > 4000 then billed_year_kwh*t.year_4000_kwh/4000
  when billed_year_kwh > 3000 then billed_year_kwh*t.year_3000_kwh/3000
  when billed_year_kwh > 2000 then billed_year_kwh*t.year_2000_kwh/2000
  when billed_year_kwh > 1000 then billed_year_kwh*t.year_1000_kwh/1000
  when billed_year_kwh >= 0 then t.year_0_kwh + (billed_year_kwh*(t.year_1000_kwh-t.year_0_kwh)/1000)
end pre_solar_year_cost,

case
  when billed_year_kwh > 40000 then st.year_40000_kwh/40000
  when billed_year_kwh > 30000 then st.year_30000_kwh/30000
  when billed_year_kwh > 25000 then st.year_25000_kwh/25000
  when billed_year_kwh > 20000 then st.year_20000_kwh/20000
  when billed_year_kwh > 15000 then st.year_15000_kwh/15000
  when billed_year_kwh > 14000 then st.year_14000_kwh/14000
  when billed_year_kwh > 13000 then st.year_13000_kwh/13000
  when billed_year_kwh > 12000 then st.year_12000_kwh/12000
  when billed_year_kwh > 11000 then st.year_11000_kwh/11000
  when billed_year_kwh > 10000 then st.year_10000_kwh/10000
  when billed_year_kwh > 9000 then st.year_9000_kwh/9000
  when billed_year_kwh > 8000 then st.year_8000_kwh/8000
  when billed_year_kwh > 7000 then st.year_7000_kwh/7000
  when billed_year_kwh > 6000 then st.year_6000_kwh/6000
  when billed_year_kwh > 5000 then st.year_5000_kwh/5000
  when billed_year_kwh > 4000 then st.year_4000_kwh/4000
  when billed_year_kwh > 3000 then st.year_3000_kwh/3000
  when billed_year_kwh > 2000 then st.year_2000_kwh/2000
  when billed_year_kwh > 1000 then st.year_1000_kwh/1000
  when billed_year_kwh >= 0 then st.year_0_kwh + ((st.year_1000_kwh-st.year_0_kwh)/1000)
end subsidized_pre_solar_year_cost_per_kwh,

case
  when billed_year_kwh > 40000 then billed_year_kwh*st.year_40000_kwh/40000
  when billed_year_kwh > 30000 then billed_year_kwh*st.year_30000_kwh/30000
  when billed_year_kwh > 25000 then billed_year_kwh*st.year_25000_kwh/25000
  when billed_year_kwh > 20000 then billed_year_kwh*st.year_20000_kwh/20000
  when billed_year_kwh > 15000 then billed_year_kwh*st.year_15000_kwh/15000
  when billed_year_kwh > 14000 then billed_year_kwh*st.year_14000_kwh/14000
  when billed_year_kwh > 13000 then billed_year_kwh*st.year_13000_kwh/13000
  when billed_year_kwh > 12000 then billed_year_kwh*st.year_12000_kwh/12000
  when billed_year_kwh > 11000 then billed_year_kwh*st.year_11000_kwh/11000
  when billed_year_kwh > 10000 then billed_year_kwh*st.year_10000_kwh/10000
  when billed_year_kwh > 9000 then billed_year_kwh*st.year_9000_kwh/9000
  when billed_year_kwh > 8000 then billed_year_kwh*st.year_8000_kwh/8000
  when billed_year_kwh > 7000 then billed_year_kwh*st.year_7000_kwh/7000
  when billed_year_kwh > 6000 then billed_year_kwh*st.year_6000_kwh/6000
  when billed_year_kwh > 5000 then billed_year_kwh*st.year_5000_kwh/5000
  when billed_year_kwh > 4000 then billed_year_kwh*st.year_4000_kwh/4000
  when billed_year_kwh > 3000 then billed_year_kwh*st.year_3000_kwh/3000
  when billed_year_kwh > 2000 then billed_year_kwh*st.year_2000_kwh/2000
  when billed_year_kwh > 1000 then billed_year_kwh*st.year_1000_kwh/1000
  when billed_year_kwh >= 0 then st.year_0_kwh + (billed_year_kwh*(st.year_1000_kwh-st.year_0_kwh)/1000)
end subsidized_pre_solar_year_cost,

pre_solar_year_cost-billed_year_cost default_yearly_saving,
subsidized_pre_solar_year_cost-billed_year_cost subsidized_yearly_saving,

to_char(cm2.start_date, 'Mon YYYY') month_year,
round(cm2.billed_wh/1000, 3) billed_kwh,
NVL(P.RATE_PER_KWH * POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', cm2.start_DATE)) / 365)), 0) rate_per_kwh,
round(cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', cm2.start_DATE)) / 365)), 0), 2) vivint_solar_charges,
iff(p.utility_schedule_rate ilike '%care%', round(cm2.billed_wh/1000 * subsidized_pre_solar_year_cost_per_kwh, 2), round(cm2.billed_wh/1000 * pre_solar_year_cost_per_kwh, 2)) utility_charges,
iff(p.utility_schedule_rate ilike '%care%', round(cm2.billed_wh/1000 * subsidized_pre_solar_year_cost_per_kwh - (cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', cm2.start_DATE)) / 365)), 0)), 2), round(cm2.billed_wh/1000 * pre_solar_year_cost_per_kwh - (cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', cm2.start_DATE)) / 365)), 0)), 2)) savings
from
  (
    select * from
  (
    select
project_id,
project_name,
start_date,
billed_wh,sum(billed_wh) over (partition by project_id order by start_date rows between 11 preceding and current row)/1000 billed_year_kwh,
sum(iff(billing_method = 'Estimated',billed_wh,null)) over (partition by project_id order by start_date rows between 11 preceding and current row)/1000 estimated_billed_year_kwh,
sum(1) over  (partition by project_id order by start_date rows between 11 preceding and current row) month_cnt
    from
fleet.t_combined_monthly where is_all_month
    )
  where month_cnt = 12 and start_date = dateadd('month',-1,date_from_parts(year(current_date()),month(current_date()),1))
  )
  cm,
rpt.t_project p,
rpt.t_contract ct,
  (
    select * from
  (
    select
project_id,
project_name,
start_date,
billed_wh,
sum(1) over  (partition by project_id order by start_date rows between 11 preceding and current row) month_cnt
    from
fleet.t_combined_monthly where is_all_month
    )
  )
  cm2,

(
select * from
(
  select t.*,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
  customer_likelihood is not null
  )
  where
  row_cnt2 = 1
)
t,
(
select * from
(
  select t.*,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
  customer_likelihood is not null and
  is_subsidized = 'True'
  )
  where
  row_cnt2 = 1
)
st


where
p.project_id = cm.project_id(+) and
p.project_id = cm2.project_id(+) and
p.primary_contract_id = ct.contract_id and
substring(p.service_zip_code,0,5) = t.zipcode and
substring(p.service_zip_code,0,5) = st.zipcode(+) and
p.service_number = '{service_number}' and
cm2.start_date > dateadd(month, -13, date_trunc(month, current_date)) and
cm2.start_date <= dateadd(month, -1, date_trunc(month, current_date))

order by p.project_id
))

select month_year "Month Year",
    billed_kwh "Billed kWh",
    rate_per_kwh "PPA/Lease rate per kWh",
    vivint_solar_charges "Vivint Solar Charges",
    utility_charges "Utility Charges",
    savings "Savings"
from save
order by start_date