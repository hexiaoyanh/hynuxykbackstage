package com.mika.code.encrypt;

import com.google.zxing.common.StringUtils;

import org.springframework.web.bind.annotation.*;
import com.google.zxing.common.StringUtils;
import java.io.UnsupportedEncodingException;


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
    @RequestMapping(value = "/qr",method = RequestMethod.POST)
    public String qr(@RequestBody Data item) throws UnsupportedEncodingException {
//        System.out.println(item.getAgentID());
//        System.out.println(item.getCustomerID());
//        System.out.println(item.getAccNum());
//        System.out.println(item.getCardID());
//        System.out.println(item.getCardID());
//        System.out.println(item.getPerCode());
//        System.out.println(item.getOrderNumb());
//        System.out.println(item.getRandomNum());
        String a = encrypt.m2865a(
                encrypt.m2866a(Integer.parseInt(item.getCustomerID()),Integer.parseInt(item.getAgentID())),
                ("1,1," + item.getAgentID() + "," +item.getCustomerID() + "," + item.getAccNum() + "," +item.getCardID() + "," +m2691k(item.getAccName()) + "," + item.getPerCode() + ","
                        + item.getOrderNumb() + "," +item.getRandomNum()).getBytes(StringUtils.GB2312)
        );
        byte[] temp = a.getBytes(StringUtils.GB2312);
        String b = a+","+encrypt.m2863a(temp,temp.length);
        return b;
    }
}
