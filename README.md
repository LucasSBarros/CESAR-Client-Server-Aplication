# Client-Server-Aplication
A simple Client-Server Application using Sockets in Python, with some validations (checksum, timer, acknowledgement and sequential)

General Objective: Develop a client-server application capable of providing reliable communication for data exchanged between final systems in the application layer, considering a channel with data losses and errors.

Introduction:

This report describes a Python client-server system that uses the socket library to create sockets that use the IPv4 address format and the TCP protocol to communicate through the localhost (when on the same machine) or via IP.

The server can handle multiple clients simultaneously, using multithreading. Additionally, the system can simulate packet loss and delays in message transmission.

Server Code:

The server is created using the socket library, which allows communication between the server and clients. It listens for connections through the chosen port, in this case, port 9000, but any other available port could have been chosen. It also uses threads to handle multiple connections simultaneously, enabling parallelism.

Libraries Imported in the Server Code:

The following libraries were imported to perform the task:

• socket: To create the server socket and establish connections.
• threading: To allow multiple simultaneous connections.
• random: To simulate delays in responses.
• time: To calculate the wait time before sending responses.

Initialization of Variables and the Server Socket:

• max_threads: Defines the maximum number of threads the server can have simultaneously.
• server: Creates the server socket using the IPv4 and TCP protocols.
• server.bind(): Binds the socket to a specific IP address and port.
• server.listen(): Configures the socket to listen for connections.
• worker() function: Function executed by each thread to handle client connections.

The worker() function receives two parameters: the established connection and the client's address.

Inside the function, the server performs the following actions:

Prints that a connection has been established with the client.
Sets a timeout for the connection.
Receives and processes data from the client.
Calculates and compares the sequence number and checksum.
Sends ACK or NACK responses, depending on the validation of the received data.
Terminates the connection if necessary.
Main Server Loop:

Accepts client connections and creates a new thread for each client, provided the maximum number of threads has not been reached. If the maximum number of threads has been reached, the server waits one second before attempting to accept new connections.

Client Code:

The client connects to the server and sends messages to it. It also simulates packet loss and delays in message transmission.

Importing Required Libraries:

• socket: To create the client socket and establish connections.
• random: To simulate packet loss and delays in message transmission.
• time: To simulate delays in message transmission.

Initialization of Variables and the Client Socket:

• client: Creates the client socket using the IPv4 and TCP protocols.
• client.settimeout(): Sets a timeout for the connection.
• client.connect(): Connects to the server at the specified IP address and port.

Main Client Loop:

Requests the user to enter messages separated by "||".
Processes and sends the messages to the server.
Simulates packet loss and delays in message transmission.
Receives and processes server responses (ACK or NACK).
Resends the original message in case of NACK.
Terminates the connection if necessary.
Details of the Main Client Loop:

• Request for Messages from the User:

The user enters a series of messages separated by "||". If the user types "TCHAU," the program is terminated.

• Processing client messages:

The messages are split into a list using the separator "||", and for each of these messages in the list, a sequence number is generated, and the checksum of the message is calculated.

The message to be sent includes a sequence number and its checksum, forming the following pattern (protocol): {sequence number} {checksum} {message}.

Furthermore, it is possible to simulate packet loss and delays in message transmission, as the probability of sending the correct message is 50%, while the possibility of sending a message with errors is also 50% (with 25% chance of each type of error).

• Receiving and processing server responses:

The client waits for an acknowledgment (ACK) or negative acknowledgment (NACK) response from the server. If the response is a NACK, the client resends the original message.

• Connection termination:

The client ends the connection if the user enters "TCHAU" or if the maximum number of messages has been reached.

In summary, this report describes a client-server application in Python that provides reliable communication for data exchanged between final systems, considering a channel with data loss and errors. The server uses multithreading to handle multiple simultaneous connections, and the client can simulate packet loss and transmission delays.
