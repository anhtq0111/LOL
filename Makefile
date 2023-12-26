run-spark:
	docker exec -it spark-master bash /bitnami/runspark.sh

run-hdfs:
	docker exec -it namenode bash /data/hadoop.sh

up:
	docker-compose up -d

down:
	docker-compose down

thread: up run-hdfs run-spark
