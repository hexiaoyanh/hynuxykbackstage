package com.mika.code.scan;

public class RequestData {
    private String CustomID;
    private String AgentID;
    private String data;
    public String getCustomID() {
        return CustomID;
}

    public void setCustomID(String customID) {
        CustomID = customID;
    }

    public String getAgentID() {
        return AgentID;
    }

    public void setAgentID(String agentID) {
        AgentID = agentID;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }
}
