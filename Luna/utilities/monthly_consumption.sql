select distinct
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.oct_kwh,
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.nov_kwh,
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum;

select distinct
    ec.dec_kwh,
    ec.jan_kwh,
    ec.feb_kwh,
    ec.mar_kwh,
    ec.apr_kwh,
    ec.may_kwh,
    ec.jun_kwh,
    ec.jul_kwh,
    ec.aug_kwh,
    ec.sep_kwh,
    ec.oct_kwh,
    ec.nov_kwh
from lostraff.mv_pr_energy_consumption ec
inner join sfrpt.t_dm_project p
    on p.project_id = ec.project_id
where p.service_number = :serviceNum

-- -- SNOWFLAKE
-- SELECT DISTINCT
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.OCT_KWH,
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.NOV_KWH,
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--             EC.DEC_KWH,
--             EC.JAN_KWH,
--             EC.FEB_KWH,
--             EC.MAR_KWH,
--             EC.APR_KWH,
--             EC.MAY_KWH,
--             EC.JUN_KWH,
--             EC.JUL_KWH,
--             EC.AUG_KWH,
--             EC.SEP_KWH,
--             EC.OCT_KWH,
--             EC.NOV_KWH
-- FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
-- WHERE SERVICE_NUMBER = :serviceNum;