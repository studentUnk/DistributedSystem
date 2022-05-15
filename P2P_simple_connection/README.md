# P2P connection - List

## Introduction
The purpose of this is to explain how to connect a defined n-nodes in order to get an specific value that each node owns. 

## Elements
All the nodes connected to the network must have the same *code*, this means that all must be able to understand what other node request using the same name of the service. Now, to achieve this, the next elements are required:

- Flag = The flag has two possible values *True* or *False*. *True* if it is possible to return the total sum of the node. *False* when the total sum has already been sent. 
- Neighbors route = Array of IP neighbors to communicate
- Black list = This is a list transmited when the total sum is in process. This list contains the IP addresses that already asked for information, so the node does not try to communicate with the ones included in it.
- White list = After the total sum is got the nodes need to be free, to achieve this, a new list is transmited, a *White list*, whose purpose is the same that *Black List*, but in this case the *Flag* is set with the value *True* and the same request is send to the neighbor nodes.
- Array numbers = Array that contains the values of the node with which the total sum is calculated.

## Operation

Any node can start the request for the total sum of the array numbers of all the nodes connected, in the next sequence:

### Get total sum

1. Get total sum of the values contained in the node that start the request.
2. Send a request to each IP address that is in the *neighbors route* asking for the total sum that each node can get. Each request is send with a list that contains the IP addresses that has been already asked by the IP address requestor.
3. When a node receives a request, if it is the first one, the node returns the total sum of the values in *array numbers* (and the *Flag* is set in *False*), if not returns *0*.
4. After calculated the total sum, the node that receives the request tries to communicate with its own neighbors, excluding the IP addresses that are included in the list transmitted (*Black list*).
5. The step 2-3-4 is repeated in each node until there is no more IP routes to ask for information. 
6. The last node that generated the request returns the sum of the total values to the requestor, including the own value calculated and the total got from the neighbors.
7. Each node returns the values until those are received by the first IP address that generated the request.

### Free the IP address

1. The first IP address that requested the total sum, send a request to free again the *Flag* after set its own Flag's value in *True*.
2. Each neighbor receives a request to free the *Flag* and also a list (*White list*) to not communicate with an IP address that is waiting for a response.
3. All the nodes receives the order to free the *Flag* and returns the value *True* (that is not currently used).

## Example

Let's consider the next *neighbors route* for three IP address connected.  

- 192.168.1.1 = 192.168.1.2, 192.168.1.3
- 192.168.1.2 = 192.168.1.1
- 192.168.1.3 = 192.168.1.1

Now, each node has the next values in the *array numbers*.  

- 192.168.1.1 = 1,10
- 192.168.1.2 = 2
- 192.168.1.3 = 3

If the request start in 192.168.1.1, the next sequence will be generated:

1. **192.168.1.1**: Get total sum, value *11* and the *Flag* is set in *False*.
2. **192.168.1.1**: Add own IP address to the black list and send request to *192.168.1.2*.
3. **192.168.1.2**: Get total sum, value *2* and the *Flag* is set in *False*.
4. **192.168.1.2**: Check black list, if the IP address exist in his own neighbor list it does not try to communicate, so, in this case, it does not send a request to 192.168.1.1. 
5. **192.168.1.2**: Return total sum because there is no more IP address to send a request.
6. **192.168.1.1**: Receives the total sum of 192.168.1.2, now the total value is 13, and updates the black list with the black list send by 192.168.1.2. After this, the request is send to 192.168.1.3.
7. **192.168.1.3**: Get total sum, value *3* and the *Flag* is set in *False*.
8. **192.168.1.3**: Check black list, if the IP address exist in his own neighbor list it does not try to communicate, so, in this case, it does not send a request to 192.168.1.1.
9. **192.168.1.3**: Return total sum because there is no more IP address to send a request.
10. **192.168.1.1**: Receives the total sum of 192.168.1.3, now the total value is 16, and updates the black list with the black list send by 192.168.1.3. Now, there is no more IP address to communicate, so the total sum is printed in the screen.
11. After this the same process is realized to set the value of the *Flag* in *True*.
