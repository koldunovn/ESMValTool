;#######################################################################
;# Model-specific fixes for reformatDEFAULT_main                       #
;# Author: Nikolay Koldunov  (AWI-Germany)                             #
;#######################################################################
;# PROJECT:     CMIP5                                                  #
;# ENSEMBLE:    [all]                                                  #
;# MODEL:       MRI-ESM1                                               #
;# VARIABLES:   thetao                                                 #
;# FIELDS:      [all]                                                  #
;# DESCRIPTION: Using zeros as missing values                          #
;#######################################################################

undef("fixing_func")
function fixing_func(var:numeric,name:string)
begin

  ret = 1

  if (name.eq."thetao") then
      var = mask(var, var.eq.0, False)
      ret = 0
  end if

  return(ret)

end
