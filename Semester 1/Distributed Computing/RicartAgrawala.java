import java.io.*;
import java.net.*;
import java.nio.channels.FileLock;
import java.util.*;

public class RicartAgrawala extends Thread {
  int ID;
  String host;
  int port;
  int[] ports;
  boolean waiting = false;
  boolean accessing = false;
  private int ti = 0;
  List<ProcessClient> requestDeferredArray = new ArrayList<ProcessClient>();
  List<ProcessClient> waitingList = new ArrayList<ProcessClient>();
  List<ProcessClient> processesToRequest = new ArrayList<ProcessClient>();
  
  Properties prop = new Properties();
  private static final File lockFile = new File("lock.file");

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
      sleep(5000);
    } catch (Exception e) {
      e.printStackTrace();
    }
    for (int port : ports) {
      try {
        if (port != this.port) {
          Socket s = new Socket(host, port);
          ProcessClient p = new ProcessClient(s, port);
          pw = new PrintWriter(s.getOutputStream(), true);
          pw.println(this.ID);
          p.start();
        }
      } catch (Exception e) {
        System.out.println("Error Connecting with Other processes");
      }
    }
    while (true) {
      try {
        System.in.read();
        ti++;
        waiting = true;
        for (ProcessClient p : processesToRequest)
          waitingList.add(p);
        sendtoRi(String.valueOf(ti));

        System.out.println("Broadcasting REQUEST to other processes... ");
        while (true) {
          sleep(1000);
          if (!accessing && waitingList.size() == 0) {
            System.out.println("Received all REPLIES from other processes... ");
            synchronized (lockFile) {
              try {
                FileOutputStream fos = new FileOutputStream(lockFile);
                FileLock lock = fos.getChannel().lock();
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
                fos.close();
              } catch (Exception e) {
                e.printStackTrace();
              }
            }
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
      ProcessClient p;
      while (true) {
        Socket s = server.accept();
        BufferedReader input = new BufferedReader(new InputStreamReader(s.getInputStream()));
        int id = Integer.parseInt(input.readLine());
        p = new ProcessClient(s, id);
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
    for (ProcessClient p : processesToRequest)
      p.sendMessage(ID + ":" + message);
  }

  public void sendTo(int x, String message) {
    for (ProcessClient p : processesToRequest)
      if (p.getPID() == x)
        p.sendMessage(ID + ":" + message);
  }

  public void replyToDeferred() {
    for (ProcessClient p : requestDeferredArray)
      p.sendMessage(ID + ":OK");
  }

  class ProcessClient extends Thread {
    BufferedReader input;
    PrintWriter output;
    String msg;
    int id;

    public ProcessClient(Socket client, int id) {
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
          // System.out.println("Message Received : " + msg);
          String msgs[] = msg.split(":");
          int rId = Integer.parseInt(msgs[0]);
          
          // If process gets a REPLY
          if (msgs[1].equals("OK")) {
            System.out.println("Reply Received From P" + msg);
            for (ProcessClient p : processesToRequest)
              if (p.getPID() == rId)
                waitingList.remove(p);
          } 
          // If process gets a REQUEST
          else {
            System.out.println("Request Received From P" + msg);
            int rHi = Integer.valueOf(msgs[1]);
            
            // If process is accessing or is waiting for CS and the clock time is 
            // less than the clock time of request message defer the REQUEST
            if (accessing || (waiting && ti < rHi)) {
              for (ProcessClient p : processesToRequest)
                if (p.getPID() == rId)
                  requestDeferredArray.add(p);
            } 
            // Else send a REPLY to REQUEST
            else {
              if (ti < rHi)
                ti = rHi;
              sendTo(rId, "OK");
            }
          }
        } catch (Exception e) {
          for (ProcessClient p : processesToRequest)
            if (p.getPID() == id)
              processesToRequest.remove(p);
          System.out.println(id + "Error! Socket will be closed immediatly");
          break;
        }

      }
    }

  }
}