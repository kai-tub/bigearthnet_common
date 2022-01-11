# Archive Bug Tracker

Sentinel-1:
	- `lly` instead of `lry` in `coordinates` entry
	- `acquisition_time` instead of `acquisition_date` as it is called in Sentinel-2

Sentinel-2:
	- Hour specification is not necessarily two numbers in patch name:
		- See: "S2B_MSIL2A_20170924T93020_41_73"
		- Missing leading 0
