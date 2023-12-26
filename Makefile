spark:
	docker exec -it spark-master bash /bitnami/runspark.sh

hdfs:
	docker exec -it namenode bash /data/hadoop.sh

up:
	docker-compose up -d

down:
	docker-compose down

thread: up hdfs spark
