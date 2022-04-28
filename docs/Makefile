

all:
	@echo "usage: make <year>"

2021: 2021/index.html
2022: 2022/index.html
2023: 2023/index.html


2023/index.html: 2023/holidays-2023.yaml
	care_calendar --year 2023 -o $@ $^ comments.md

2022/index.html: 2022/holidays-2022.yaml
	care_calendar --year 2022 -o $@ $^ comments.md

2021/index.html: 2021/holidays-2021.yaml
	care_calendar --first-month=9 --year 2021 -o $@ $^ comments.md

