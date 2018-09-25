SELECT DISTINCT
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.OCT_KWH,
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.NOV_KWH,
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;
-- --
SELECT DISTINCT
            EC.DEC_KWH,
            EC.JAN_KWH,
            EC.FEB_KWH,
            EC.MAR_KWH,
            EC.APR_KWH,
            EC.MAY_KWH,
            EC.JUN_KWH,
            EC.JUL_KWH,
            EC.AUG_KWH,
            EC.SEP_KWH,
            EC.OCT_KWH,
            EC.NOV_KWH
FROM VSLR.D_POST_INSTALL.V_PR_ENERGY_CONSUMPTION AS EC
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = EC.PROJECT_ID
WHERE SERVICE_NUMBER = %s;