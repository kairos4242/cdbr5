package com.kairos4242.cdbr.controllers;

import com.kairos4242.cdbr.entity.Power;
import com.kairos4242.cdbr.repository.PowerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("api/v1/power")
@RestController
public class PowerController {

    @Autowired
    private PowerRepository repository;

    @GetMapping
    public Iterable<Power> getAllPowers() {
        return repository.findAll();
    }

    @GetMapping(path = "{id}")
    public Power getPower(@PathVariable("id") int id) {
        Power power =  repository.findById(id).orElse(new Power(-1,"Not Found 😕"));
        System.out.println("GET request for power " + power.getId());
        return power;
    }

    @GetMapping(path = "/count")
    public long getCountOfPowers() {
        return repository.count();
    }

}
