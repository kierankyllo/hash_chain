# CS435 Programming Assignment
## Kieran Brooks
## Dr. Qian Yu 

## Introduction:

This documentation describes a client server application to implement my solution to the CS435 programming assignment.  It comprises client and server components as well as a pytest testing suite and a module of user defined classes written in python.  The application uses TCP socket communication implemented using the socketserver library to manage the chat session.  The custom classes define the logic of generating, validating and incrementing the hash keys passed between the client and server to verify each other as valid.

My approach uses a hash chain to verify the identity of the message sender by confirming the possession of a shared key by both parties and possession of a previous hash in the hash chain.  The hash chain is constructed using a shared secret that is concatenated with each generation of hash in the chain.  For each link the previous hash is concatenated with the shared secret and hashed again using the SHA256 algorithm.  This approach achieves authentication of client and server as well as replay and masquerade protection with respect to the authentication of the correspondent identities.  In this assignment the message itself Is not protected from modification, nor is it made confidential with encryption.

## Strengths:
* This approach is strong against masquerade attacks as both parties are verified to each other for each message.  The client and server can be confident that each other has the ability to produce the hash chain exactly the same.
* Because the shared secret is concatenated with hash generation, a bad actor could not simply guess the hashing algorithm for an attack.  As it would be useless without the shared secret.

## Weaknesses:
* This approach is weak against MITM attacks.  Assuming that the message could be captured without leaking the original signal through to the other correspondent, a bad actor could intercept a TCP packet, extract the unencrypted message and replace it with their own and send the packet on to the destination.  They would need to continually capture each packet and resend each one in the correct order to ensure the attack could continue. The attacker would also need to intercept the response from the server, replace the acknowledgement message with the original message and send it on to the client.
* This approach is weak against eavesdropping since the message is sent in cleartext.

## Extendibility:
* Incorporating message hashing to add non-repudiation to the hash chain. 
* Adding encryption to the message construction would be trivial as the client and server already possess a shared key.
* Adding sequence numbering to the encrypted message could invalidate a MITM attack. 
