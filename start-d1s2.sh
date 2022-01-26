clear
echo "Starting 1 DSE, 2 Stargate and 1 Traefik container(s)"

# Startup Cassandra and Traefik
docker-compose up -d backend traefik

# Wait until Cassandra is ready
until docker logs dse-stargate_backend_1 | grep -q "DSE startup complete";
do
    sleep 2
    echo "Waiting for DSE (1/1) to startup..."
done

# Startup Stargate
docker-compose up -d stargate

# Wait until Stargate is ready
until docker logs dse-stargate_stargate_1 2>/dev/null | grep -q "Finished starting bundles";
do
    sleep 2
    echo "Waiting for Stargate (1/2) to startup..."
done

# Scale Stargate
docker-compose up -d --scale stargate=2 stargate

# Wait until Stargate is ready
until docker logs dse-stargate_stargate_2 2>/dev/null | grep -q "Finished starting bundles";
do
    sleep 2
    echo "Waiting for Stargate (2/2) to startup..."
done

# Show container performance
docker stats -a