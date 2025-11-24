package io.github.artsobol.kurkod.common.util;

import io.github.artsobol.kurkod.common.constants.CommonConstants;

public class LogUtils {
    public static String getMethodName(){
        try{
            return Thread.currentThread().getStackTrace()[2].getMethodName();
        } catch(Exception e){
            return CommonConstants.UNDEFINED;
        }
    }
}
