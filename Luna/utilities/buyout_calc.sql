SELECT
    T.SERVICE_NUMBER,
    C.FULL_NAME,
    C.EMAIL,
    T.SERVICE_ADDRESS,
    T.SERVICE_CITY,
    split_part(upper(t.service_county), ' COUNTY', 1) service_county,
    T.SERVICE_STATE,
    substring(t.service_zip_code, 0, 5) zip_code
FROM VSLR.RPT.T_PROJECT AS T
INNER JOIN VSLR.RPT.T_CONTACT AS C ON C.CONTACT_ID =T.CONTRACT_SIGNER
WHERE T.SERVICE_NUMBER = '{service_number}';with seq as (select 4 year_1,
    ceil(year_1 * .95, 2) year_2,
    ceil(year_2 * .95, 2) year_3,
    ceil(year_3 * .95, 2) year_4,
    ceil(year_4 * .95, 2) year_5,
    ceil(year_5 * .95, 2) year_6,
    ceil(year_6 * .95, 2) year_7,
    ceil(year_7 * .95, 2) year_8,
    ceil(year_8 * .95, 2) year_9,
    ceil(year_9 * .95, 2) year_10,
    ceil(year_10 * .95, 2) year_11,
    ceil(year_11 * .95, 2) year_12,
    ceil(year_12 * .95, 2) year_13,
    ceil(year_13 * .95, 2) year_14,
    ceil(year_14 * .95, 2) year_15,
    ceil(year_15 * .95, 2) year_16,
    ceil(year_16 * .95, 2) year_17,
    ceil(year_17 * .95, 2) year_18,
    ceil(year_18 * .95, 2) year_19,
    ceil(year_19 * .95, 2) year_20)

SELECT distinct s.opty_contract_type,
    case
        when p.service_state = 'NY' and upper(s.opty_contract_type) = 'PPA' then nvl(nyp.total_sales_tax, 0)
        when p.service_state = 'NY' and upper(s.opty_contract_type) = 'LEASE' then nvl(nyl.total_sales_tax, 0)
        else nvl(tr.total_sales_tax, 0)
    end sales_tax,
    te.taxable,p.remaining_contract_term,
    21-ceil(-p.remaining_contract_term/12) project_year,
    case
        when project_year = 1 then seq.year_1
        when project_year = 2 then seq.year_2
        when project_year = 3 then seq.year_3
        when project_year = 4 then seq.year_4
        when project_year = 5 then seq.year_5
        when project_year = 6 then seq.year_6
        when project_year = 7 then seq.year_7
        when project_year = 8 then seq.year_8
        when project_year = 9 then seq.year_9
        when project_year = 10 then seq.year_10
        when project_year = 11 then seq.year_11
        when project_year = 12 then seq.year_12
        when project_year = 13 then seq.year_13
        when project_year = 14 then seq.year_14
        when project_year = 15 then seq.year_15
        when project_year = 16 then seq.year_16
        when project_year = 17 then seq.year_17
        when project_year = 18 then seq.year_18
        when project_year = 19 then seq.year_19
        else seq.year_20
    end transfer_buyout_price,
    round(7 * pow(.95, project_year - 1), 2) default_price,
    round(C.SYSTEM_SIZE_ACTUAL_KW*1000, 0) watts,
    round(transfer_buyout_price * watts, 2) transfer_subtotal,
    iff(te.taxable ilike 'y%%', round(transfer_buyout_price * watts * sales_tax, 2), 0) transfer_total_tax,
    (transfer_subtotal + transfer_total_tax) transfer_total,
    round(default_price * watts, 2) default_subtotal,
    iff(te.taxable ilike 'y%%', round(default_price * watts * sales_tax, 2), 0) default_total_tax,
    (default_subtotal + default_total_tax) default_total
FROM VSLR.RPT.T_PROJECT AS P
left join rpt.t_service s
    on p.service_id = s.service_id
left JOIN VSLR.RPT.T_CAD AS C
  ON P.primary_cad = C.cad_ID
left join fin.t_tax_eligibility te
    on p.service_state = te.state
left join (select * from fin.t_sales_tax_rate where end_date is null) tr
    on p.service_state = tr.state
        and upper(p.service_city) = upper(tr.city)
        and split_part(upper(p.service_county), ' COUNTY', 1) = tr.county
        and substring(p.service_zip_code, 0, 5) = tr.zip_code
left join (select * from fin.t_sales_tax_rate_ny_lease where end_date is null) nyl
    on p.service_state = nyl.state
        and upper(p.service_city) = upper(nyl.city)
        and split_part(upper(p.service_county), ' COUNTY', 1) = nyl.county
        and substring(p.service_zip_code, 0, 5) = nyl.zip_code
left join (select * from fin.t_sales_tax_rate_ny_ppa where end_date is null) nyp
    on p.service_state = nyp.state
        and upper(p.service_city) = upper(nyp.city)
        and split_part(upper(p.service_county), ' COUNTY', 1) = nyp.county
        and substring(p.service_zip_code, 0, 5) = nyp.zip_code
cross join seq
WHERE P.SERVICE_NUMBER = %s
    and
    te.trx_contract_type = 'Buyout'
    and te.buyer_type = 'Homeowner'