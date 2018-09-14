-- TODO NEED TO CONVERT THIS TO SNOWFLAKE
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
    m.record_type
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
left join mack_damavandi.t_utility_match x
    on upper(x.sf_utility_name) = upper(t.utility_company) and x.sf_state = t.service_state
inner join mack_damavandi.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
left join sfrpt.t_dm_contract m
    on t.primary_contract_id = m.contract_id
where t.service_number = :serviceNum
    and t.project_status != 'Cancelled'

;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.actual_kwh "Actual (kWh)",
    nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0) "PPA/Lease rate per kWh",
    round(t.actual_kwh*nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0),2) "Vivint Solar Bill",
    round(t.actual_kwh*coalesce(u.blended_rate,u.vslr_calculated_rate),2) "Utility Bill",
    round(t.actual_kwh*(coalesce(u.blended_rate,u.vslr_calculated_rate)-nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0)),2) "Savings"
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
left join mack_damavandi.t_utility_match x
    on upper(x.sf_utility_name) = upper(p.utility_company) and x.sf_state = p.service_state
inner join mack_damavandi.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date