package com.kairos4242.cdbr.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;

@Entity
@Table(name = "power")
public class Power {

    @Id
    @JsonProperty(index=1, value="id") private int id;
    @JsonProperty(index=2, value="name") private String name;
    @JsonInclude() @Transient
    private int maxCooldown;//unnecessary to have db column, we instead manually set this to be the same as cooldown
    private int cooldown;
    private String description;
    private String onAcquireFunction;
    private String onUseFunction;
    private String onRemoveFunction;
    private String flavourText;

    public Power() {}

    public Power(
            int id,
            String name,
            String description,
            String flavourText
    ) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.flavourText = flavourText;
    }

    public Power(
            int id,
            String name
    ) {
        this.id = id;
        this.name = name;
    }

    public Power(
            int id,
            String name,
            int cooldown,
            String description,
            String onAcquireFunction,
            String onUseFunction,
            String onRemoveFunction,
            String flavourText
    ) {
        this.id = id;
        this.name = name;
        this.cooldown = cooldown;
        this.maxCooldown = cooldown;
        this.description = description;
        this.onAcquireFunction = onAcquireFunction;
        this.onUseFunction = onUseFunction;
        this.onRemoveFunction = onRemoveFunction;
        this.flavourText = flavourText;
    }

    @PostLoad
    private void postLoad() {
        this.maxCooldown = cooldown;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Power player = (Power) o;

        return name.equals(player.name);
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getFlavourText() {
        return flavourText;
    }

    public void setFlavourText(String flavourText) {
        this.flavourText = flavourText;
    }

    public int getCooldown() {
        return cooldown;
    }

    public void setCooldown(int cooldown) {
        this.cooldown = cooldown;
    }

    public String getOnAcquireFunction() {
        return onAcquireFunction;
    }

    public void setOnAcquireFunction(String onAcquireFunction) {
        this.onAcquireFunction = onAcquireFunction;
    }

    public String getOnUseFunction() {
        return onUseFunction;
    }

    public void setOnUseFunction(String onUseFunction) {
        this.onUseFunction = onUseFunction;
    }

    public String getOnRemoveFunction() {
        return onRemoveFunction;
    }

    public void setOnRemoveFunction(String onRemoveFunction) {
        this.onRemoveFunction = onRemoveFunction;
    }

    public int getMaxCooldown() {
        return maxCooldown;
    }

    public void setMaxCooldown(int maxCooldown) {
        this.maxCooldown = maxCooldown;
    }
}
