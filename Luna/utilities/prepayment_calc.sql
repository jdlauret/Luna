SELECT distinct
    case
        when p.service_state = 'NY' and upper(s.opty_contract_type) = 'PPA' then nvl(nyp.total_sales_tax, 0)
        when p.service_state = 'NY' and upper(s.opty_contract_type) = 'LEASE' then nvl(nyl.total_sales_tax, 0)
        else nvl(tr.total_sales_tax, 0)
    end sales_tax,
    te.taxable,
    P.SERVICE_Name,
    p.project_number,
    t.full_name,
    p.service_address,
    p.service_city,
    p.service_state,
    substring(p.SERVICE_ZIP_CODE, 0, 5) service_zip_code,
    C.ESCALATOR,
    .5 degradation,
    5 discount_rate,
    CAD.SYSTEM_SIZE_ACTUAL_KW,
    to_date(date_trunc(day, p.installation_complete)) installation_complete,
    to_date(date_trunc(day, P.in_service_date)) in_service_date,
    (P.REMAINING_CONTRACT_TERM + 1) * -1 remaining_contract_term1,
    greatest(240-remaining_contract_term1, 1) current_contract_month,
    C.RECORD_TYPE contract_type,
    C.CONTRACT_VERSION,
    P.RATE_PER_KWH,
    cad.install_jan,
    cad.install_feb,
    cad.install_mar,
    cad.install_apr,
    cad.install_may,
    cad.install_jun,
    cad.install_jul,
    cad.install_aug,
    cad.install_sep,
    cad.install_oct,
    cad.install_nov,
    cad.install_dec,
    cad.total_energy_production_actual
FROM VSLR.RPT.T_PROJECT AS P
left join rpt.t_contact t
    on t.contact_id = p.contract_signer
left join rpt.t_service s
    on p.service_id = s.service_id
INNER JOIN VSLR.RPT.T_CONTRACT AS C ON P.primary_contract_id = C.contract_ID
INNER JOIN VSLR.RPT.T_CAD AS CAD ON P.primary_cad = CAD.cad_ID
left join fin.t_tax_eligibility te
    on p.service_state = te.state
left join (select * from fin.t_sales_tax_rate where end_date is null) tr
    on tr.state = p.service_state
        and upper(p.service_city) = tr.city
        and split_part(upper(p.service_county), ' COUNTY', 1) = tr.county
        and substring(p.service_zip_code, 0, 5) = tr.zip_code
left join (select * from fin.t_sales_tax_rate_ny_lease where end_date is null) nyl
    on p.service_state = nyl.state
        and upper(p.service_city) = nyl.city
        and split_part(upper(p.service_county), ' COUNTY', 1) = nyl.county
        and substring(p.service_zip_code, 0, 5) = nyl.zip_code
left join (select * from fin.t_sales_tax_rate_ny_ppa where end_date is null) nyp
    on p.service_state = nyp.state
        and upper(p.service_city) = nyp.city
        and split_part(upper(p.service_county), ' COUNTY', 1) = nyp.county
        and substring(p.service_zip_code, 0, 5) = nyp.zip_code
WHERE P.SERVICE_NUMBER = '{service_number}'
    and upper(s.opty_contract_type) = upper(te.trx_contract_type)
    and te.buyer_type = 'Homeowner'