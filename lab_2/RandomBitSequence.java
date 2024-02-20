import java.util.Random;

public class RandomBitSequence {

    private static final int MAXBIT = 128;

    public static void main(String[] args) {
        Random rand = new Random(System.currentTimeMillis());

        for (int i = 0; i < MAXBIT; i++) {
            long randNum = rand.nextInt(32767);
            boolean binaryNum = randNum % 2 == 1;
            System.out.print(binaryNum ? "1" : "0");
        }
    }
}
