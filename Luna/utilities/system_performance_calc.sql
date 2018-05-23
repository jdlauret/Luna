select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code,
    trunc(t.start_billing)
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
where t.service_number = 'serviceNum'
;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.estimated_corrected_kwh "Estimate (kWh)",
    t.actual_kwh "Actual (kWh)",
    round(t.performance_ratio,4) "Performance" --t.actual_kwh/t.estimated_corrected_kwh
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
where p.service_number = 'serviceNum'
    and t.read_date between to_date('startDate','MM/DD/YYYY') and to_date('endDate','MM/DD/YYYY')
order by t.read_date