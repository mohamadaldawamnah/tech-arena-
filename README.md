# Tech_Arena_2024

> Program for the Huawei Tech Arena 2024

## Resources:
- PDF: https://cdn.fs.agorize.com/dUucGrBaTulzlhPrtJ6h
- Tech Arena webiste: https://huawei.agorize.com/en/challenges/irelandrc2024/pages/how-it-works?lang=en

## Notes on files I added:
|filename|description|
|---|---|
|action.py|classes for actions and action, essentially storing the solution|
|decision_maker.py|file which will containt the actual algorithm|
|demand.py|wrapper around the actual_demand pandas data frame, can be used to get the demand for just one time_step|
|fleet.py|OOP representation of the fleet (datacenters containing servers), also useful because it loads the csv files containing data|

## To-Do:
- [ ] write an incredibly simple algorithm to just match the demand: get the demand for time slot, convert it to number of servers needed, subtract the servers already owned, buy the rest
