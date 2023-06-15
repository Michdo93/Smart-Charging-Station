# Smart-Charging-Station
A Python REST API with which you can control the RSH-A16 USB Hub using flask and uhubctl. A device connected via USB sends its battery status to the REST API. If this falls below a threshold, the charging cycle is activated. If it is above a threshold, the charging cycle is deactivated.
