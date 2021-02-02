# storage-checker
 
 9.a Because this system deals a lot with I/O operations the concurrency 
 was one of the main concerns.
 9.b 
   - ETag: In order to make sure that target file data stays unchanged between 
    samples - different file checksum points to file corruption - strong indicator to a problem in storage service.
   - Retry-Attempts: - May point on network unstable network or heavy load on a monitored service 
   - Status-Code: - May also serve as an indicator to heavy load on a monitored service 
   - Latency - Increase in a latency also may point to heavy load on a monitored service.
 9.c The output logs are saved as json objects - it is because it is easy to store those logs as an 
 no-sql objects in database.
