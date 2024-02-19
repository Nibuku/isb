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

//01000010100011011101011111100100100011111100101100111010110100111011100000100010110101010001010010001110011000101110101101001000
