package com.kairos4242.cdbr.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "power")
public class Power {

    @Id
    private int id;
    private String name;
    private String description;
    private String flavourText;

    public Power() {}

    public Power(
            @JsonProperty("id") int id,
            @JsonProperty("name") String name,
            String description,
            String flavourText
    ) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.flavourText = flavourText;
    }

    public Power(
            @JsonProperty("id") int id,
            @JsonProperty("name") String name
    ) {
        this.id = id;
        this.name = name;
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
}
