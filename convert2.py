import timing
import settings
import windows_mac
if settings.system == 'mac' or settings.system == 'linux':
    import dbCAPRS
elif settings.system == 'windows':
    import oracle
    import dbCAPRS2
import dbV1
import v1_story_search
import v1_defect_search
import v1print
import orphan_v1_alert
if settings.system == 'mac' or settings.system == 'linux':
    import orphan_CAPRS_alert
    import report_caprs_all
elif settings.system == 'windows':
    import orphan_CAPRS_alert2
    import report_caprs_all2
import report_caprs_all
# import printSettings