select * from

(
select
  cm.month_cnt,
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

iff(
contains(upper(utility_schedule_rate),'CAR') OR
contains(upper(utility_schedule_rate),'DRLI') OR
contains(upper(utility_schedule_rate),'FERA') OR
contains(upper(utility_schedule_rate),'R-2') OR
contains(upper(utility_schedule_rate),'R2') OR
contains(upper(utility_schedule_rate),'RS R-2') OR
contains(upper(utility_schedule_rate),'R 2') OR
contains(upper(utility_schedule_rate),'RS LI R-2') OR
contains(upper(utility_schedule_rate),'NG R-2') OR
contains(upper(utility_schedule_rate),'RLI R-2') OR
contains(upper(utility_schedule_rate),'R-2 LI') OR
contains(upper(utility_schedule_rate),'RLI 2') OR
contains(upper(utility_schedule_rate),'R LI R-2') OR
contains(upper(utility_schedule_rate),'R-2 RES LI') OR
contains(upper(utility_schedule_rate),'RESLOWINR2') OR
contains(upper(utility_schedule_rate),'RLI R2') OR
contains(upper(utility_schedule_rate),'LOW R-2') OR
contains(upper(utility_schedule_rate),'R-2 LOW IN') OR
contains(upper(utility_schedule_rate),'R L I R2') OR
contains(upper(utility_schedule_rate),'A2 R2') OR
contains(upper(utility_schedule_rate),'A2') OR
contains(upper(utility_schedule_rate),'A-2') OR
contains(upper(utility_schedule_rate),'A2 ASSIST') OR
contains(upper(utility_schedule_rate),'A2 RES') OR
contains(upper(utility_schedule_rate),'A3') OR
contains(upper(utility_schedule_rate),'A2-RES') OR
contains(upper(utility_schedule_rate),'A2-RS') OR
contains(upper(utility_schedule_rate),'A2-R') OR
contains(upper(utility_schedule_rate),'A2 R') OR
contains(upper(utility_schedule_rate),'A2-RA') OR
contains(upper(utility_schedule_rate),'A2 RA') OR
contains(upper(utility_schedule_rate),'A2 - RA') OR
contains(upper(utility_schedule_rate),'A2 RASSIST'),true,false) is_utility_schedule_care,

  p.service_name,
  c.full_name,
  c.email,
  p.service_address,
  p.service_city,
  p.service_state,
  p.service_zip_code,
  date_trunc(day, p.start_billing),
  iff(is_utility_schedule_care and p.service_state = 'CA', p.utility_company||' - CARE', p.utility_company) utility_company,
  iff(cm.month_cnt = 12, iff(is_utility_schedule_care, subsidized_pre_solar_year_cost_per_kwh, pre_solar_year_cost_per_kwh), null),
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
fleet.t_combined_monthly where is_all_month
    )
  where
    start_date = dateadd('month',-1,date_from_parts(year(current_date()),month(current_date()),1))
  )
  cm,
rpt.t_project p,
rpt.t_contract ct,

(
select * from
(
  select t.*,
  nvl(t.customer_likelihood , 0) customer_likelihood_all,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood_all desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id
  )
  where
  row_cnt2 = 1
)
t,
(
select * from
(
  select t.*,
  nvl(t.customer_likelihood , 0) customer_likelihood_all,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood_all desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
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
t.customer_likelihood_all,
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

iff(
contains(upper(utility_schedule_rate),'CAR') OR
contains(upper(utility_schedule_rate),'DRLI') OR
contains(upper(utility_schedule_rate),'FERA') OR
contains(upper(utility_schedule_rate),'R-2') OR
contains(upper(utility_schedule_rate),'R2') OR
contains(upper(utility_schedule_rate),'RS R-2') OR
contains(upper(utility_schedule_rate),'R 2') OR
contains(upper(utility_schedule_rate),'RS LI R-2') OR
contains(upper(utility_schedule_rate),'NG R-2') OR
contains(upper(utility_schedule_rate),'RLI R-2') OR
contains(upper(utility_schedule_rate),'R-2 LI') OR
contains(upper(utility_schedule_rate),'RLI 2') OR
contains(upper(utility_schedule_rate),'R LI R-2') OR
contains(upper(utility_schedule_rate),'R-2 RES LI') OR
contains(upper(utility_schedule_rate),'RESLOWINR2') OR
contains(upper(utility_schedule_rate),'RLI R2') OR
contains(upper(utility_schedule_rate),'LOW R-2') OR
contains(upper(utility_schedule_rate),'R-2 LOW IN') OR
contains(upper(utility_schedule_rate),'R L I R2') OR
contains(upper(utility_schedule_rate),'A2 R2') OR
contains(upper(utility_schedule_rate),'A2') OR
contains(upper(utility_schedule_rate),'A-2') OR
contains(upper(utility_schedule_rate),'A2 ASSIST') OR
contains(upper(utility_schedule_rate),'A2 RES') OR
contains(upper(utility_schedule_rate),'A3') OR
contains(upper(utility_schedule_rate),'A2-RES') OR
contains(upper(utility_schedule_rate),'A2-RS') OR
contains(upper(utility_schedule_rate),'A2-R') OR
contains(upper(utility_schedule_rate),'A2 R') OR
contains(upper(utility_schedule_rate),'A2-RA') OR
contains(upper(utility_schedule_rate),'A2 RA') OR
contains(upper(utility_schedule_rate),'A2 - RA') OR
contains(upper(utility_schedule_rate),'A2 RASSIST'),true,false) is_utility_schedule_care,
POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', cm2.start_DATE)) / 365)) escalator_factor,

pre_solar_year_cost - billed_year_cost default_yearly_saving,
subsidized_pre_solar_year_cost - billed_year_cost subsidized_yearly_saving,
--monthly view with escalated PPA/Lease rate
to_char(cm2.start_date, 'Mon YYYY') month_year,
round(cm2.billed_wh/1000, 3) billed_kwh,
NVL(P.RATE_PER_KWH * escalator_factor, 0) rate_per_kwh,
round(cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * escalator_factor, 0), 2) vivint_solar_charges,
iff(
    is_utility_schedule_care,
    round(cm2.billed_wh/1000 * subsidized_pre_solar_year_cost_per_kwh, 2),
    round(cm2.billed_wh/1000 * pre_solar_year_cost_per_kwh, 2)) utility_charges,
iff(
    is_utility_schedule_care,
    round(cm2.billed_wh/1000 * subsidized_pre_solar_year_cost_per_kwh - (cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * escalator_factor, 0)), 2),
    round(cm2.billed_wh/1000 * pre_solar_year_cost_per_kwh - (cm2.billed_wh/1000 * NVL(P.RATE_PER_KWH * escalator_factor, 0)), 2)) savings
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
--billed_wh by month
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
  nvl(t.customer_likelihood , 0) customer_likelihood_all,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood_all desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id
  )
  where
  row_cnt2 = 1
)
t,
(
select * from
(
  select t.*,
  nvl(t.customer_likelihood , 0) customer_likelihood_all,
  tr.zipcode,
  row_number() over (partition by zipcode order by customer_likelihood_all desc) row_cnt2
  from
  fleet.t_tariff t,
fleet.t_territory tr
  where
  t.unique_territory_id = tr.unique_territory_id and
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
--replace {service_number} with any account number
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