docker volume create postgress_vol_1
docker volume create postgress_vol_2

docker network create app_net

docker run --rm -d \
  --name postgress_1 \
  -e POSTGRES_PASSWORD=pwd \
  -e POSTGRES_USER=root \
  -e POSTGRES_DB=test \
	-v postgress_vol_1:/var/lib/postgresql/data \
	--net=app_net \
	postgres:14
	
docker run --rm -d --net=app_net -p 80:8088 --name superset apache/superset

docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

docker exec -it superset superset db upgrade


docker exec -it superset superset init
