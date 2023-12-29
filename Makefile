run-spark:
	docker exec -it spark-master bash /bitnami/runspark.sh

run-hdfs:
	docker exec -it namenode bash /data/hadoop.sh

up:
	docker-compose up -d

down:
	docker-compose down

crawl: 
	python .\Crawl.py

thread: crawl up run-hdfs run-spark
