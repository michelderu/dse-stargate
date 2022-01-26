# Import Cassandra driver
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Connect to the database
def connectDB():
    contact_point = 
    auth_provider = PlainTextAuthProvider('tWDPkdHoZZrdpsoQqYkHWtrI', 'xdv+qC7QpHXn1QYUwPURePiTgXXGfxKpkF2YPD9Yo9OF7pXXrmWIs.ow.y8AzhwDaGrp.XHmd+OR49u0atFXdGSWQ4s1,n_soKsKZSh,a8zjqOk+IYT0RzjA91gzfEkb')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster.connect()
    
# Connect to Astra
session = connectDB()

# Task scheduling 
session.execute("""CREATE TABLE test.devices (
                         device_uuid uuid,
                         external_identifier text,
                         geohash text,
                         latitude float,
                         longitude float,
                         measures set<text>,
                         name text,
                         parent_device_id uuid,
                         tags map<text, text>,
                         PRIMARY KEY (device_uuid)
                       );""")
