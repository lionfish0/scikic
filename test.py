from answer_us_census import USCensusAnswer as a
print a.USCensusApiQuery(['02','170',['000101','000102'],None],['B16001_001E'])
print a.USCensusApiQuery(["04", "015", '950100', "1"],['B16001_001E'])
