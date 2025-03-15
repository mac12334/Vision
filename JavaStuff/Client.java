package JavaStuff;
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;


public class Client {
   Socket sock;
   int connection;
   DataInputStream in;

   public int id;
   public double[] position = new double[3];

   public Client(int port) {
       this.connection = port;
       try {
           this.sock = new Socket("127.0.0.1", port);
           read();
           close();
       } catch (IOException e) {
           e.printStackTrace();
       }
   }

   public void read() throws IOException {
       in = new DataInputStream(new BufferedInputStream(sock.getInputStream()));

        String out = "";
        while (!out.equals("STP\n")){
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
            } catch (java.lang.NumberFormatException e) {
                System.out.println("closing");
            }
        }
    }

   public void close() throws IOException {
       sock.close();
       in.close();
   }

   public static void main(String[] args) {
       new Client(9480);
   }
}
