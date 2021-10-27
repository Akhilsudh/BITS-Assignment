██████  ███████  █████  ██████  ███    ███ ███████ 
██   ██ ██      ██   ██ ██   ██ ████  ████ ██      
██████  █████   ███████ ██   ██ ██ ████ ██ █████   
██   ██ ██      ██   ██ ██   ██ ██  ██  ██ ██      
██   ██ ███████ ██   ██ ██████  ██      ██ ███████ 

--------------------------------------------------
| Ricart Agrawala Algorithm For Mutual Exclusion |
| By Akhil Sudhakaran - 2021MT12054              |
--------------------------------------------------
NOTE: For a more prettier README, click here https://gist.github.com/Akhilsudh/3cc3db7e6276b7d90eaff436ddbb9b57
NOTE: This code can be found in my Github Repository here https://github.com/Akhilsudh/BITS-Assignment/tree/master/Semester%201/Distributed%20Computing

Prereqs:
========
1. Any Operating System that supports a JDK (This code is tested completely on Ubuntu 20.04)
2. JDK for compiling and run the code (This code tested on openjdk 11)
3. Terminal emulators (Preferably ones where more than one tab session can be opened up at the same time) to see each process in action

Assumptions Made:
=================
1. The number of participating processes/nodes are known and defined before hand in a configuration file.
2. Communication channels are assumed to be FIFO in nature.
3. None of the processes/nodes involved fail when the algorithm is in execution. 
4. All processes/nodes gets hold of the critical section for a fixed amount of time.

Instructions To Run The Program:
================================
1. Before we begin executing the program, we need to set number of processes/nodes participating in the algorithm, the host and port of the processes/nodes in the `process.config` file (An example is shown below):
```
process.count=3
process.1=127.0.0.1:3001
process.2=127.0.0.1:3002
process.3=127.0.0.1:3003

```

2. Compile the `RicartAgrawala.java` file:
```
javac RicartAgrawala.java

```

3. Run this program in separate terminal sessions (to simulate each process), for example:
    * In Terminal 1
    ```
    java -cp . RicartAgrawala 1

    ```

    * In Terminal 2
    ```
    java -cp . RicartAgrawala 2

    ```

    * In Terminal 3
    ```
    java -cp . RicartAgrawala 3

    ```

4. Once all the processes are ready we should see a `All processes successfully connected, ready to start.` in every process.

5. Now we can start requesting Critical Section by hitting the `enter` key on each terminal, this should initiate a Critical Section REQUEST broadcast by the respective process to the other processes.

6. Depending on how the REQUESTS were sent by the previous step, the terminal would show the actions taken by each of the nodes involved (REPLY/Defer/REQUEST/Execute CS). The terminal also shows the messages that are sent to each other by the participting processes.