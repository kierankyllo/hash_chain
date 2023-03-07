# CS435 Programming Assignment
## Kieran Brooks
## Dr. Qian Yu 

## Introduction:

This documentation describes a client server application to implement my solution to the CS435 programming assignment. It comprises client and server components, a pytest testing suite, a utility to generate a text file of keys and a module of user defined classes written in python. The application uses
TCP socket communication implemented using the socketserver library to manage the session. The custom classes define the logic of generating, validating and incrementing the hash keys passed between the client and server to verify each other as valid.

My approach uses a hash chain to verify the identity of the message sender by confirming the possession of a shared key by both parties and possession of the next hash in the hash chain. The hash chain is constructed recursively using a shared secret that is concatenated with each generation in the chain and hashed using SHA256. This approach achieves authentication of client and server as well as replay and masquerade protection with respect to the authentication of the correspondent identities. In this assignment the message itself is not made confidential with encryption.



## Strengths:
* This approach is strong against masquerade attacks as both parties are verified to each other for each message. The client and server can be confident that each other has the ability to produce the hash chain exactly the same.
* This approach validates bidirectionally and provides a measure of strength as it adds complexity to orchestrating a MITM attack.
* The shared secret is concatenated with each hash generation, a bad actor could not simply guess the hashing algorithm and attempt a selected hashtext brute force attack, as it would be useless without the shared secret and due to the one way property of the hash.
* The typical weakness of a hash chain based approach is the need for distribution of a large quantity of keys in the form of the hashes required. My approach mitigates this by allowing for generation of the chain by both parties and does not require the transmission of the entire chain. This also allows for flexibility in the nature of the shared secret. It could be a file, a string, an integer, or any hashable information common to the correspondents.

![Hash Chain](https://user-images.githubusercontent.com/29678626/223495091-bfb60f2b-d178-4a52-8dfb-cba3eb0f0d8f.png)

## Weaknesses:
* This approach is less robust against MITM attacks. Assuming that the message could be captured without leaking the original signal through to the other correspondent, a bad actor could intercept a TCP packet, extract the unencrypted message and replace it with their own and send the packet on to the destination. They would need to continually capture each packet and resend each one in the correct order in both directions to ensure the attack could continue. The attacker would also need to intercept the response from the server, replace the acknowledgement message with the original message and send it on to the client.
* This approach is weak against eavesdropping since the message is sent in cleartext as encipherment is out of scope for the assignment.

## Extendibility:
* Incorporating message hashing to add non-repudiation to the hash chain. 
* Adding encryption to the message construction would be trivial as the client and server already possess a shared key.
