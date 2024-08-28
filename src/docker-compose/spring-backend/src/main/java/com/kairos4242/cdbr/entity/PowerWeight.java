package com.kairos4242.cdbr.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;

@Entity
@IdClass(PowerWeightPrimaryKey.class)
@Table(name = "power_weight")
public class PowerWeight {

    @Id
    @JsonProperty("player_id") private int playerId;
    @Id
    @JsonProperty("power_id") private int powerId;
    @JsonProperty("weight") private int weight;
    @JsonProperty("power_uses") private int powerUses;

    public PowerWeight() {
    }

    public PowerWeight(
            int playerId,
             int powerId
    ) {
        this.playerId = playerId;
        this.powerId = powerId;
    }

    public PowerWeight(
            int playerId,
            int powerId,
            int weight,
            int powerUses
    ) {
        this.playerId = playerId;
        this.powerId = powerId;
        this.weight = weight;
        this.powerUses = powerUses;
    }

    public int getPlayerId() {
        return playerId;
    }

    public void setPlayerId(int playerId) {
        this.playerId = playerId;
    }

    public int getPowerId() {
        return powerId;
    }

    public void setPowerId(int powerId) {
        this.powerId = powerId;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }

    public int getPowerUses() {
        return powerUses;
    }

    public void setPowerUses(int powerUses) {
        this.powerUses = powerUses;
    }
}
