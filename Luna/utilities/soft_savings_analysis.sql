select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code,
    date_trunc(day, t.start_billing),
    case
        when upper(t.utility_schedule_rate) like '%CARE%' and t.service_state = 'CA' then t.utility_company||' - CARE'
        when upper(t.utility_schedule_rate) like '%FERA%' and t.service_state = 'CA' then t.utility_company||' - FERA'
        else t.utility_company
    end utility_company,
    nvl(u.blended_rate,u.vslr_calculated_rate) blended_rate,
    m.record_type
from rpt.t_project t
inner join rpt.t_contact c
    on c.contact_id = t.contract_signer
left join d_post_install.t_utility_match x
    on upper(x.sf_utility_name) = upper(case
                                            when upper(t.utility_schedule_rate) like '%CARE%' and t.service_state = 'CA' then t.utility_company||' - CARE'
                                            when upper(t.utility_schedule_rate) like '%FERA%' and t.service_state = 'CA' then t.utility_company||' - FERA'
                                            else t.utility_company
                                        end) and x.sf_state = t.service_state
inner join d_post_install.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
left join rpt.t_contract m
    on t.primary_contract_id = m.contract_id
where t.service_number = '{service_number}'
    and t.project_status != 'Cancelled'
;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.actual_kwh "Actual (kWh)",
    nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((datediff(day, date_trunc(day, p.start_billing), date_trunc(day, t.read_date))/365))),t.current_rate_kwh),0) "PPA/Lease rate per kWh",
    round(t.actual_kwh*nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((datediff(day, date_trunc(day, p.start_billing), date_trunc(day, t.read_date))/365))),t.current_rate_kwh),0),2) "Vivint Solar Bill",
    round(t.actual_kwh*coalesce(u.blended_rate,u.vslr_calculated_rate),2) "Utility Bill",
    round(t.actual_kwh*(coalesce(u.blended_rate,u.vslr_calculated_rate)-nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((datediff(day, date_trunc(day, p.start_billing), date_trunc(day, t.read_date))/365))),t.current_rate_kwh),0)),2) "Savings"
from fleet.t_daily_energy_wa t
inner join rpt.t_project p
    on p.project_id = t.project_id
left join d_post_install.t_utility_match x
    on upper(x.sf_utility_name) = upper(case
                                            when upper(p.utility_schedule_rate) like '%CARE%' and p.service_state = 'CA' then p.utility_company||' - CARE'
                                            when upper(p.utility_schedule_rate) like '%FERA%' and p.service_state = 'CA' then p.utility_company||' - FERA'
                                            else p.utility_company
                                        end) and x.sf_state = p.service_state
inner join d_post_install.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
where p.service_number = '{service_number}'
    and t.read_date between to_date('{start_date}','MM/DD/YYYY') and to_date('{end_date}','MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet.t_daily_energy_wa w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date