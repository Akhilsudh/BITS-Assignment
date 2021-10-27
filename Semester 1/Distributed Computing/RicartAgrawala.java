import java.io.*;
import java.net.*;
import java.util.*;

public class RicartAgrawala extends Thread {
  int ID; // Process ID
  String host; // Process Host
  int port; // Process Port
  int[] ports; // Array of Ports of participating Processes
  boolean waiting = false; // Flag to check if process has requested and yet to receive CS
  boolean accessing = false; // Flag to check if process is executing CS
  private int ti = 0; // Process Local Clock
  List<ProcessServer> requestDeferredArray = new ArrayList<ProcessServer>(); // Request Deffered Array
  List<ProcessServer> waitingList = new ArrayList<ProcessServer>(); // Array of process to get REPLIES from
  List<ProcessServer> processesToRequest = new ArrayList<ProcessServer>(); // The collection processes to broadcast REQUESTS

  Properties prop = new Properties();

  public static void main(String[] args) {
    int ID = Integer.parseInt(args[0]);
    RicartAgrawala ra = new RicartAgrawala(ID, "processes.config");
    ra.start();
    ra.createServer();
  }

  public RicartAgrawala(int ID, String filePath) {
    try (FileInputStream fis = new FileInputStream(filePath)) {
      prop.load(fis);
    } catch (Exception e) {
      e.printStackTrace();
    }
    int count = Integer.parseInt(prop.getProperty("process.count"));
    this.ports = new int[count];
    String URL[];
    for (int i = 1; i <= count; i++) {
      URL = prop.getProperty("process." + i).split(":");
      ports[i - 1] = Integer.parseInt(URL[1]);
    }
    this.ID = ID;
    URL = prop.getProperty("process." + ID).split(":");
    this.host = URL[0];
    this.port = Integer.parseInt(URL[1]);
  }

  public void run() {
    PrintWriter pw;
    try {
      sleep(2000);
    } catch (Exception e) {
      e.printStackTrace();
    }
    for (int port : ports) {
      // try {
        if (port != this.port) {
          boolean reconnect = true;
          while(reconnect) {
            try {
              sleep(2000);
              Socket s = new Socket(host, port);
              ProcessServer p = new ProcessServer(s, port);
              pw = new PrintWriter(s.getOutputStream(), true);
              pw.println(this.ID);
              p.start();
              reconnect = false;
            } catch (Exception e) {
              System.out.println("Error Connecting to processes with port " + port);
            }
          }
        }
    }
    System.out.println("\n=====================================================");
    System.out.println("All processes successfully connected, ready to start.");
    System.out.println("=====================================================\n");
    while (true) {
      try {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        br.readLine();
        ti++;
        waiting = true;
        for (ProcessServer p : processesToRequest)
          waitingList.add(p);

        System.out.println("Broadcasting REQUEST to other processes... ");
        sendtoRi(String.valueOf(ti));

        while (true) {
          sleep(1000);
          if (waitingList.size() == 0) {
            System.out.println("Received all REPLIES from other processes... ");
            accessing = true;
            System.out.println("Executing Critical Section");
            sleep(1000);
            System.out.println(".");
            sleep(1000);
            System.out.println(".");
            sleep(1000);
            System.out.println(".");
            sleep(1000);
            System.out.println(".");
            sleep(1000);
            System.out.println(".");
            System.out.println("Releasing Critical Section.");
            replyToDeferred();
            requestDeferredArray.clear();
            waiting = false;
            accessing = false;
            break;
          }
        }
      } catch (Exception e) {
      }
    }

  }

  
  public void createServer() {
    try {
      ServerSocket server = new ServerSocket(port);
      ProcessServer p;
      while (true) {
        Socket s = server.accept();
        BufferedReader input = new BufferedReader(new InputStreamReader(s.getInputStream()));
        int id = Integer.parseInt(input.readLine());
        p = new ProcessServer(s, id);
        processesToRequest.add(p);
        System.out.println("Successfully Connected to P" + id);
        sleep(500);
        p.start();
      }
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public void sendtoRi(String message) {
    for (ProcessServer p : processesToRequest)
      p.sendMessage(ID + ":" + message);
  }

  public void sendTo(int x, String message) {
    for (ProcessServer p : processesToRequest)
      if (p.getPID() == x)
        p.sendMessage(ID + ":" + message);
  }

  public void replyToDeferred() {
    for (ProcessServer p : requestDeferredArray)
      p.sendMessage(ID + ":OK");
  }

  class ProcessServer extends Thread {
    BufferedReader input;
    PrintWriter output;
    String msg;
    int id;

    public ProcessServer(Socket client, int id) {
      this.id = id;
      try {
        output = new PrintWriter(client.getOutputStream(), true);
        input = new BufferedReader(new InputStreamReader(client.getInputStream()));
      } catch (Exception e) {
        e.printStackTrace();
      }
    }

    public int getPID() {
      return id;
    }

    public void sendMessage(String str) {
      output.println(str);
    }

    public void run() {
      while (true) {
        try {
          String msg = input.readLine();
          String msgs[] = msg.split(":");
          int rId = Integer.parseInt(msgs[0]);

          // If process gets a REPLY
          if (msgs[1].equals("OK")) {
            System.out.println("Reply Received From P" + msg);
            for (ProcessServer p : processesToRequest)
              if (p.getPID() == rId)
                waitingList.remove(p);
          }
          // If process gets a REQUEST
          else {
            int rHi = Integer.valueOf(msgs[1]);
            
            // Send REPLY when process is not accessing, waiting for CS or if process is waiting 
            // and has a local time stamp higher than request time stamp or if the timestamps are 
            // same send reply if the request id is lesser (since smaller id has higher proirity)
            // Else deffer the REQUEST
            if (!accessing) {
              if ((!waiting) || (waiting && (ti > rHi)) || (waiting && (ti == rHi && getPID() > rId))) {
                ti = Math.max(ti, rHi);
                sendTo(rId, "OK");
              } else {
                ti++;
                System.out.println("Request from P" + rId + " deferred.");
                for (ProcessServer p : processesToRequest)
                  if (p.getPID() == rId)
                    requestDeferredArray.add(p);
              }
            }
            else {
              ti++;
              System.out.println("Request from P" + rId + " deferred.");
              for (ProcessServer p : processesToRequest)
                if (p.getPID() == rId)
                  requestDeferredArray.add(p);
            }
          }
        } catch (Exception e) {
          e.printStackTrace();
          System.exit(0);
        }
      }
    }

  }
}