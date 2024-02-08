### log file parcing script for the access_log file

usage: task4 [options]

optional arguments:

  -h, --help            show this help message and exit

  -a A                  [N, int] find N the most used ip addresses -output1-

  -b B                  [N, int] find quantity of requests in time period, N minutes -output2-

  -c C                  [N, int] find N the most often used user agents -output3-

  -d D                  [N, int] find N quantity of error code in time period -output4-

  -e E [E ...]          [N, int] [s, optional] find N the longest (by default) requests (in millis). If add argument [s], finds N the shortest
                        requests - format: Get, time when, ip address - millis -output5-
  
  -f F [F ...]          [N, int] [K, int] find N the most often requests up to K slash -output6-
  
  -g                    show quantity of requests per node (worker) -output7-
  
  -i                    show quantity of same references to webpage, sort by domain -output8-
  
  -j J                  [int, N] find quantity of request in time period, N minutes, by nodes (workers) -output9-
  
  -k K                  [int, N] find quantity of requests in time period, N minutes, sorted by quantity of requests -output10-

