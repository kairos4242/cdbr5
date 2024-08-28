package com.kairos4242.cdbr.controllers;

import com.kairos4242.cdbr.entity.PowerWeight;
import com.kairos4242.cdbr.repository.PowerWeightRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RequestMapping("api/v1/powerWeight")
@RestController
public class PowerWeightController {

    @Autowired
    private PowerWeightRepository repository;

    @GetMapping
    public Iterable<PowerWeight> getAllPowerWeights() {
        return repository.findAll();
    }

    @GetMapping(path = "/player/{id}")
    public List<PowerWeight> getPowerWeightsForPlayer(@PathVariable("id") int id) {
        List<PowerWeight> powerWeights =  repository.findByPlayerId(id);

        System.out.println("GET request for power weight for player " + id);
        return powerWeights;
    }

    @GetMapping(path = "/power/{id}")
    public List<PowerWeight> getPowerWeightsForPower(@PathVariable("id") int id) {
        List<PowerWeight> powerWeights =  repository.findByPowerId(id);

        System.out.println("GET request for power weight for power " + id);
        return powerWeights;
    }

    @GetMapping(path = "/count")
    public long getCountOfPowerWeights() {
        return repository.count();
    }
}
