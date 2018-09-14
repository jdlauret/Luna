-- TODO NEED TO CONVERT TO SNOWFLAKE, CURRENTLY WAITING FOR UTILITY RATE TO BE CONVERTED
select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code,
    trunc(t.start_billing),
    t.utility_company,
    u.blended_rate,
    sd.current_annual_energy_consumpt
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
left join mack_damavandi.t_utility_rates u
    on upper(u.utility) = upper(t.utility_company) and u.state = t.service_state
left join sfrpt.t_dm_system_design sd
    on sd.cad_id = t.primary_cad
where t.service_number = :serviceNum

;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.actual_kwh "Actual (kWh)",
    round(t.actual_kwh*nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(p.start_billing)-trunc(sysdate))/365)),
                                    t.current_rate_kwh),0),2) "Vivint Solar Bill"
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
left join mack_damavandi.t_utility_rates u
    on upper(u.utility) = upper(p.utility_company) and u.state = p.service_state
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date