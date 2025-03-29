package JavaStuff;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;


public class Client {
   Socket sock;
   int connection;
   DataInputStream in;
   PrintWriter writer;

   public int id;
   public double[] position = new double[3];

   public Client(int port) {
       this.connection = port;
       try {
            this.sock = new Socket("127.0.0.1", port);
            this.in = new DataInputStream(new BufferedInputStream(sock.getInputStream()));
            this.writer = new PrintWriter(sock.getOutputStream());
    } catch (IOException e) {
           e.printStackTrace();
       }
   }

   public void read() throws IOException {
        String out = "";
        byte b = in.readByte();
        while ((char)b != '\n') {
            out += (char) b;
            b = in.readByte();
        }
        try {
            String[] nums = out.strip().split(",");
            id = Integer.parseInt(nums[0]);
            for (int i = 0; i < 3; i++) {
                position[i] = (double) Integer.parseInt(nums[i + 1]) / 1000;
            }
            System.out.println(id + " " + " " + position[0] + " " + position[1] + " " + position[2]);
        } catch (java.lang.NumberFormatException e) {
            System.out.println("closing");
        }
    }

    public void send() {
        writer.println("hello world");
        writer.flush();
    }

   public void close() throws IOException {
       sock.close();
       in.close();
    }

   public static void main(String[] args) {
       Client cli = new Client(9480);
       int counter = 0;
       while (true) {
        if (counter % 2 == 0) {
            cli.send();
        } else {
            try {
                cli.read();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        counter++;
       }
   }
}
