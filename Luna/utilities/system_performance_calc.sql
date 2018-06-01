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
where t.service_number = :serviceNum
;select to_char(t.read_date,'Mon YYYY') "Month Year",
    nvl(t.estimated_corrected_kwh, round(t.estimated_kwh*extract(day from sysdate)/t.total_days,3)) "Estimate (kWh)",
    t.actual_kwh "Actual (kWh)",
    nvl(round(t.performance_ratio,4), round(t.actual_kwh/nvl(t.estimated_corrected_kwh, round(t.estimated_kwh*extract(day from sysdate)/t.total_days,3)),4)) "Performance" --t.actual_kwh/t.estimated_corrected_kwh
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date