package com.mika.code.scan;


import com.google.zxing.common.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.io.UnsupportedEncodingException;

import static com.mika.code.encrypt.encrypt.*;

@RestController
public class Scan {

    @RequestMapping(value = "/scan",method = RequestMethod.POST)
    public @ResponseBody
    ResponsData
    scan(@RequestBody RequestData requestData) {
//        System.out.println(requestData.getAgentID());
//        System.out.println(requestData.getCustomID());
//        System.out.println(requestData.getData());
        String[] split = requestData.getData().split(",");
        ResponsData data = new ResponsData();
        if (split.length != 2) {
            data.setCode("2");
            return data;
        }
        try {
            if (m2863a(split[0].getBytes(), split[0].length()) != Integer.parseInt(split[1])) {
                data.setCode("2");
                return data;
            }
            byte[] a = m2868a(m2866a(Integer.parseInt(requestData.getCustomID()), Integer.parseInt(requestData.getAgentID())), split[0]);
            if(a==null)
            {
                data.setCode("2");
                return data;
            }
            try {
                String[] split2 = new String(a, StringUtils.GB2312).trim().split(",");
                if (split2.length >= 5) {
                    data.setCode("1");
                    data.setData(split2);
                    return data;
                }
                data.setCode("2");
                return data;
            } catch (UnsupportedEncodingException e) {
                data.setCode("2");
                e.printStackTrace();
                return data;
            }

        }catch (Exception e2) {
            data.setCode("2");
            return data;
        }
    }
}
