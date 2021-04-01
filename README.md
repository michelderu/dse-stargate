# Scalable docker-compose with DSE and Stargate, loadbalanced by Traefik
This project aims to create a scalable (up and down) environment for DSE and Stargate.  
DSE is globally accepted as the most reliable and scalable database delibering single-digit-millisecond performance.  
Stargate is a developer friendly gateway to DSE that offers REST, Document and GraphQL APIs.

DSE (Storage) and Stargate (Compute) can be separately scaled up and down. Traefik is used to load balance any number Stargate instances.

## Traefik host name
Traefik will listen to the hostname `stargate.localhost` for loadbalancing Stargate requests. In order for this to work, you might need to extend your `/etc/hosts` file as follows:
```
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1	localhost
127.0.0.1	stargate.localhost
```

## Scripted startup
There is a script provided to startup the cluster.
- `start-d1s2t1.sh` will start the cluster with 1 node of DSE, 2 nodes of Stargate and 1 node of Traefik

DSE is configured with a maximum heap size of 4 GB. Stargate with a heapsize of 2 GB but will mostly use 1 GB.

After startup `docker stats` will be started for insight in resource consumption.

## Run cqlsh
```sh
docker exec -it dse-stargate_backend_1 cqlsh
```