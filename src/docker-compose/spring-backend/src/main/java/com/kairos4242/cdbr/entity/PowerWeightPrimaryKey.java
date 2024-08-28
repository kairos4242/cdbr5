package com.kairos4242.cdbr.entity;

import java.io.Serializable;
import java.util.Objects;

public class PowerWeightPrimaryKey implements Serializable {
    private int playerId;
    private int powerId;

    public PowerWeightPrimaryKey() {}

    public int getPlayerId() {
        return playerId;
    }

    public int getPowerId() {
        return powerId;
    }

    public void setPlayerId(int playerId) {
        this.playerId = playerId;
    }

    public void setPowerId(int powerId) {
        this.powerId = powerId;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof PowerWeightPrimaryKey powerWeightPrimaryKey)) return false;
        return playerId == powerWeightPrimaryKey.playerId && powerId == powerWeightPrimaryKey.powerId;
    }

    @Override
    public int hashCode() {
        return Objects.hash(playerId, powerId);
    }
}
