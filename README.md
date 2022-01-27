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
- `start-d1s2.sh` will start the cluster with 1 node of DSE, 2 nodes of Stargate and 1 node of Traefik

DSE is configured with a maximum heap size of 4 GB. Stargate with a heapsize of 2 GB but will mostly use 1 GB.

After startup `docker stats` will be started for insight in resource consumption.

## Run cqlsh from the container
```sh
docker exec -it dse-stargate_backend_1 cqlsh
```
# Guardrails
In DSE, Guardrails have been introduced to create configurable trip-wires in Cassandra that will either warn or error and block any operation that violates known anti-patterns. In DSE 6.8, DataStax is releasing the first set of Guardrails which include codified, best-practices such as:
- Consistency levels allowed
- Payload sizes
- Column sizes
- Collection sizes
- Number of indices 
- Number of materialized views
- And more

## Configuration changes
Normally the Cassandra config is located in `/opt/dse/resources/cassandra/conf/cassandra.yaml`. The DSE config is located in `/opt/dse/resources/dse/conf/dse.yaml`. Docker images provided by DataStax include a startup script that swaps DataStax Enterprise (DSE) configuration files found in the `/config` volume directory with the configuration file in the default location on the container. In this docker-compose set up, a volume mapping has been created that allows for local updates to the `cassandra.yaml` to be read by DSE running in the container.

Now that we have control over the configuration, we can change settings such as *Guardrails*.

## Test some guardrails
First create a keyspace:
```sql
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```
Now let's create a table with the default guardrail settings:
```sql
CREATE TABLE first_table (first_column text PRIMARY KEY, second_column text);
```
Change the guardrails in `cassandra.yaml`:
```yaml
# Guardrails settings.
guardrails:

  # Warn threshold to warn creating more tables than threshold.
  # Default -1 to disable, may differ if emulate_dbaas_defaults is enabled
  tables_warn_threshold: 2

  # Failure threshold to prevent creating more tables than threshold.
  # Default -1 to disable, may differ if emulate_dbaas_defaults is enabled
  tables_failure_threshold: 3
```
Save the file, stop the containers and start again. Then log in to cqlsh again.
```sh
docker-compose down
./start-d1s2.sh
docker exec -it dse-stargate_backend_1 cqlsh
```
Now let's create a table with the changes guardrail settings and see what happens:
```sql
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE test;
CREATE TABLE first_table (first_column text PRIMARY KEY, second_column text);
CREATE TABLE second_table (first_column text PRIMARY KEY, second_column text);
CREATE TABLE third_table (first_column text PRIMARY KEY, second_column text);
```