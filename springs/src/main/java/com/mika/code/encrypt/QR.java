package com.mika.code.encrypt;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.EncodeHintType;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.common.StringUtils;

import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import org.springframework.web.bind.annotation.*;

import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.Path;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

import com.google.zxing.client.j2se.MatrixToImageWriter;

import javax.imageio.ImageIO;
import javax.servlet.ServletOutputStream;

import static com.google.zxing.client.j2se.MatrixToImageWriter.toBufferedImage;


@RestController
public class QR {
    private boolean m2676a(byte[] bArr) {
        int i = 0;
        for (int i2 = 0; i2 < 8; i2++) {
            if ((bArr[i2] & 255) > Byte.MAX_VALUE) {
                i++;
            }
        }
        return i % 2 == 0;
    }

    public String m2691k(String AccName) throws UnsupportedEncodingException {
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

    public String CreateQr(String content, int width, int height) throws IOException {

        String resultImage = "";
        if (content!=null) {
            ServletOutputStream stream = null;
            ByteArrayOutputStream os = new ByteArrayOutputStream();
            @SuppressWarnings("rawtypes")
            HashMap<EncodeHintType, Comparable> hints = new HashMap<>();
            hints.put(EncodeHintType.CHARACTER_SET, "utf-8"); // 指定字符编码为“utf-8”
            hints.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.L); // 指定二维码的纠错等级为中级
            hints.put(EncodeHintType.MARGIN, 1); // 设置图片的边距

            try {
                QRCodeWriter writer = new QRCodeWriter();
                BitMatrix bitMatrix = writer.encode(content, BarcodeFormat.QR_CODE, width, height, hints);

                BufferedImage bufferedImage = MatrixToImageWriter.toBufferedImage(bitMatrix);
                ImageIO.write(bufferedImage, "png", os);
                /**
                 * 原生转码前面没有 data:image/png;base64 这些字段，返回给前端是无法被解析，可以让前端加，也可以在下面加上
                 */
                resultImage = new String("data:image/png;base64," + Base64.getEncoder().encodeToString(os.toByteArray()));

                return resultImage;
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (stream != null) {
                    stream.flush();
                    stream.close();
                }
            }
        }
        return null;
    }

    @RequestMapping(value = "/getqr",method = RequestMethod.POST)
    public String getqr(@RequestBody Data item) throws IOException{
        String a = encrypt.m2865a(
                encrypt.m2866a(Integer.parseInt(item.getCustomerID()), Integer.parseInt(item.getAgentID())),
                ("1,1," + item.getAgentID() + "," + item.getCustomerID() + "," + item.getAccNum() + "," + item.getCardID() + "," + m2691k(item.getAccName()) + "," + item.getPerCode() + ","
                        + item.getOrderNumb() + "," + item.getRandomNum()).getBytes(StringUtils.GB2312)
        );
        byte[] temp = a.getBytes(StringUtils.GB2312);
        String b = a + "," + encrypt.m2863a(temp, temp.length);
        return this.CreateQr(b,Integer.parseInt(item.getHeight())+180,Integer.parseInt(item.getWidth())+180);
    }

    @RequestMapping(value = "/qr", method = RequestMethod.POST)
    public String qr(@RequestBody Data item) throws IOException {
        String a = encrypt.m2865a(
                encrypt.m2866a(Integer.parseInt(item.getCustomerID()), Integer.parseInt(item.getAgentID())),
                ("1,1," + item.getAgentID() + "," + item.getCustomerID() + "," + item.getAccNum() + "," + item.getCardID() + "," + m2691k(item.getAccName()) + "," + item.getPerCode() + ","
                        + item.getOrderNumb() + "," + item.getRandomNum()).getBytes(StringUtils.GB2312)
        );
        byte[] temp = a.getBytes(StringUtils.GB2312);
        String b = a + "," + encrypt.m2863a(temp, temp.length);
        return b;
    }
}
