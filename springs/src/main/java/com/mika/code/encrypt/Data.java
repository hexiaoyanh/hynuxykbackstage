package com.mika.code.encrypt;

public class Data {
    private String CustomerID;
    private String AgentID;
    private String AccNum;
    private String CardID;
    private String AccName;
    private String PerCode;
    private String OrderNumb;
    private String RandomNum;

    public String getRandomNum() {
        return RandomNum;
    }

    public String getPerCode() {
        return PerCode;
    }

    public String getOrderNumb() {
        return OrderNumb;
    }

    public String getCustomerID() {
        return CustomerID;
    }

    public String getCardID() {
        return CardID;
    }

    public String getAgentID() {
        return AgentID;
    }

    public String getAccNum() {
        return AccNum;
    }

    public String getAccName() {
        return AccName;
    }

    public void setRandomNum(String randomNum) {
        RandomNum = randomNum;
    }

    public void setPerCode(String perCode) {
        PerCode = perCode;
    }

    public void setOrderNumb(String orderNumb) {
        OrderNumb = orderNumb;
    }

    public void setCustomerID(String customerID) {
        CustomerID = customerID;
    }

    public void setCardID(String cardID) {
        CardID = cardID;
    }

    public void setAgentID(String agentID) {
        AgentID = agentID;
    }

    public void setAccNum(String accNum) {
        AccNum = accNum;
    }

    public void setAccName(String accName) {
        AccName = accName;
    }
}
