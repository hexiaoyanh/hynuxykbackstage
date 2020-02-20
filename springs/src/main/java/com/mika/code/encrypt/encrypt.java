package com.mika.code.encrypt;


import com.google.zxing.common.StringUtils;
import org.apache.tomcat.util.codec.binary.Base64;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

/* renamed from: com.hzsun.f.f */

public class encrypt {

    /* renamed from: a */
    private static final int[] f1798a = {0, 4129, 8258, 12387, 16516, 20645, 24774, 28903, 33032, 37161, 41290, 45419, 49548, 53677, 57806, 61935, 4657, 528, 12915, 8786, 21173, 17044, 29431, 25302, 37689, 33560, 45947, 41818, 54205, 50076, 62463, 58334, 9314, 13379, 1056, 5121, 25830, 29895, 17572, 21637, 42346, 46411, 34088, 38153, 58862, 62927, 50604, 54669, 13907, 9842, 5649, 1584, 30423, 26358, 22165, 18100, 46939, 42874, 38681, 34616, 63455, 59390, 55197, 51132, 18628, 22757, 26758, 30887, 2112, 6241, 10242, 14371, 51660, 55789, 59790, 63919, 35144, 39273, 43274, 47403, 23285, 19156, 31415, 27286, 6769, 2640, 14899, 10770, 56317, 52188, 64447, 60318, 39801, 35672, 47931, 43802, 27814, 31879, 19684, 23749, 11298, 15363, 3168, 7233, 60846, 64911, 52716, 56781, 44330, 48395, 36200, 40265, 32407, 28342, 24277, 20212, 15891, 11826, 7761, 3696, 65439, 61374, 57309, 53244, 48923, 44858, 40793, 36728, 37256, 33193, 45514, 41451, 53516, 49453, 61774, 57711, 4224, 161, 12482, 8419, 20484, 16421, 28742, 24679, 33721, 37784, 41979, 46042, 49981, 54044, 58239, 62302, 689, 4752, 8947, 13010, 16949, 21012, 25207, 29270, 46570, 42443, 38312, 34185, 62830, 58703, 54572, 50445, 13538, 9411, 5280, 1153, 29798, 25671, 21540, 17413, 42971, 47098, 34713, 38840, 59231, 63358, 50973, 55100, 9939, 14066, 1681, 5808, 26199, 30326, 17941, 22068, 55628, 51565, 63758, 59695, 39368, 35305, 47498, 43435, 22596, 18533, 30726, 26663, 6336, 2273, 14466, 10403, 52093, 56156, 60223, 64286, 35833, 39896, 43963, 48026, 19061, 23124, 27191, 31254, 2801, 6864, 10931, 14994, 64814, 60687, 56684, 52557, 48554, 44427, 40424, 36297, 31782, 27655, 23652, 19525, 15522, 11395, 7392, 3265, 61215, 65342, 53085, 57212, 44955, 49082, 36825, 40952, 28183, 32310, 20053, 24180, 11923, 16050, 3793, 7920};

    private static boolean m2676a(byte[] bArr) {
        int i = 0;
        for (int i2 = 0; i2 < 8; i2++) {
            if ((bArr[i2] & 255) > Byte.MAX_VALUE) {
                i++;
            }
        }
        return i % 2 == 0;
    }

    public static String m2691k(String AccName) throws UnsupportedEncodingException {
        byte[] bArr;
        byte[] bytes = AccName.getBytes(StringUtils.GB2312);
        if (bytes.length <= 8) {
            bArr = bytes;
        } else if (m2676a(bytes)) {
            bArr = new byte[8];
            System.arraycopy(bytes, 0, bArr, 0, 8);
        } else {
            bArr = new byte[7];
            System.arraycopy(bytes, 0, bArr, 0, 7);
        }
        return new String(bArr, StringUtils.GB2312);
    }

    /* renamed from: a */
    public static int m2863a(byte[] bArr, int i) {
        int i2 = 0;
        for (int i3 = 0; i3 < i; i3++) {
            i2 = f1798a[((i2 >> 8) ^ bArr[i3]) & 255] ^ (i2 << 8);
        }
        return 65535 & i2;
    }

    /* renamed from: a */
    private static String m2864a(byte[] bArr) {
        String str = "";
        for (byte b : bArr) {
            String hexString = Integer.toHexString(b & 255);
            str = hexString.length() == 1 ? str + "0" + hexString : str + hexString;
        }
        return str.toUpperCase();
    }

    public static String byteToHex(byte[] bytes) {
        String strHex = "";
        StringBuilder sb = new StringBuilder("");
        for (int n = 0; n < bytes.length; n++) {
            strHex = Integer.toHexString(bytes[n] & 0xFF);
            sb.append((strHex.length() == 1) ? "0" + strHex : strHex); // 每个字节由两个字符表示，位数不够，高位补0
        }
        return sb.toString().trim();
    }

    /* renamed from: a */
    public static String m2865a(byte[] bArr, byte[] bArr2) {
        try {
            if (bArr.length == 16) { // short key ? .. extend to 24 byte key
                byte[] tmpKey = new byte[24];
                System.arraycopy(bArr, 0, tmpKey, 0, 16);
                System.arraycopy(bArr, 0, tmpKey, 16, 8);
                bArr = tmpKey;
            }
            SecretKeySpec secretKeySpec = new SecretKeySpec(bArr, "DESede");
            Cipher instance = Cipher.getInstance("DESede/ECB/NoPadding");
            instance.init(1, secretKeySpec);
//            System.out.println(byteToHex(bArr));
//            System.out.println(byteToHex(m2869b(bArr2)));
            return m2864a(instance.doFinal(m2869b(bArr2)));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e2) {
            e2.printStackTrace();
        } catch (NoSuchPaddingException e3) {
            e3.printStackTrace();
        } catch (BadPaddingException e4) {
            e4.printStackTrace();
        } catch (IllegalBlockSizeException e5) {
            e5.printStackTrace();
        }
        return null;
    }

    /* renamed from: a */
    public static byte[] m2866a(int i, int i2) {
        byte[] bArr = new byte[16];
        bArr[0] = (byte) (i2 & 255);
        bArr[1] = (byte) (i & 255);
        bArr[2] = (byte) ((i >> 8) & 255);
        bArr[3] = 0;
        for (int i3 = 4; i3 < 8; i3++) {
            bArr[i3] = (byte) (bArr[i3 - 4] ^ -1);
        }
        for (int i4 = 8; i4 < 12; i4++) {
            bArr[i4] = (byte) (bArr[i4 - 8] ^ bArr[(bArr.length - i4) - 1]);
        }
        bArr[12] = (byte) (bArr[8] ^ 161);
        bArr[13] = (byte) (bArr[9] ^ 27);
        bArr[14] = (byte) (bArr[10] ^ 193);
        bArr[15] = (byte) (bArr[11] ^ 29);
        return bArr;
    }

    /* renamed from: a */
    private static byte[] m2867a(String str) {
        byte[] bArr = new byte[(str.length() / 2)];
        int length = str.length();
        for (int i = 0; i < length; i += 2) {
            bArr[i / 2] = (byte) Integer.parseInt(str.substring(i, i + 2), 16);
        }
        return bArr;
    }

    /* renamed from: a */
    public static byte[] m2868a(byte[] bArr, String str) {
        try {
            if (bArr.length == 16) { // short key ? .. extend to 24 byte key
                byte[] tmpKey = new byte[24];
                System.arraycopy(bArr, 0, tmpKey, 0, 16);
                System.arraycopy(bArr, 0, tmpKey, 16, 8);
                bArr = tmpKey;
            }
            SecretKeySpec secretKeySpec = new SecretKeySpec(bArr, "DESede");
            Cipher instance = Cipher.getInstance("DESede/ECB/NoPadding");
            instance.init(2, secretKeySpec);
            return instance.doFinal(m2867a(str));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e2) {
            e2.printStackTrace();
        } catch (BadPaddingException e3) {
            e3.printStackTrace();
        } catch (IllegalBlockSizeException e4) {
            e4.printStackTrace();
        } catch (InvalidKeyException e5) {
            e5.printStackTrace();
        }
        return null;
    }

    /* renamed from: b */
    private static byte[] m2869b(byte[] bArr) {
        int length = 8 - (bArr.length % 8);
        byte[] bArr2 = new byte[(bArr.length + length)];
        System.arraycopy(bArr, 0, bArr2, 0, bArr.length);
        for (int i = 0; i < length; i++) {
            bArr2[bArr.length + i] = 0;
        }
        return bArr2;
    }
}
