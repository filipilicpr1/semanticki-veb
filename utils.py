import constants
from functools import reduce

# input date format 03. oktobar 2023.
# output date format 2023-10-03
def prepare_date(date):
    date_parts = date.split(' ')

    day = date_parts[0].split('.')[0]
    month = constants.DATES_DICTIONARY[date_parts[1]]
    year = date_parts[-1].split('.')[0]

    return year + '-' + month + '-' + day

# input storage format 8GB
# output storage format 8_GB
def prepare_memory(memory):
    memoery_parts = memory.split('G')
    return memoery_parts[0] + "_G" + memoery_parts[-1]

# input camera format 50Mpx
# output camera format 50_Mpx
def prepare_camera(camera):
    camera_parts = camera.split('M')
    return camera_parts[0] + "_M" + camera_parts[-1]

# input Samsung Exynos 990
# output Exynos_990
def prepare_chipset(chipset):
    chipset_parts = chipset.strip().split(' ')
    prepared_chipset = reduce(lambda a, b: a + '_' + b, chipset_parts[1:])
    return prepared_chipset[1:] if prepared_chipset.startswith('_') else prepared_chipset