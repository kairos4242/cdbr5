package com.kairos4242.cdbr.controllers;

import com.kairos4242.cdbr.entity.PowerWeight;
import com.kairos4242.cdbr.repository.PowerWeightRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RequestMapping("api/v1/action")
@RestController
public class ActionController {

    @Autowired
    private PowerWeightRepository repository;

    @GetMapping
    public String chooseAction(
            @RequestParam("enemyDist") int enemyDist
    ) {
        if (enemyDist < 100) {
            return "ATTACK";
        }
        return "PATH_TO_ENEMY";
    }

    @PostMapping(path = "/power")
    public Integer choosePower(
            @RequestBody ArrayList<Integer> powerList,
            @RequestParam("playerId") int playerId
    ) {
        //TODO can this be done more efficiently?
        // can we just lookup the needed powers instead of every power via findByPlayerIdAndPowerId?
        // Also can this be an extension function of List<PowerWeight>?
        List<PowerWeight> powerWeights =  repository.findByPlayerId(playerId);
        int currMaxId = powerList.getFirst(); //if no mappings this means we will always pick the first
        int currMaxWeight = -1; //any weight should be higher
        for (PowerWeight powerWeight : powerWeights) {
            int powerWeightId = powerWeight.getPowerId();
            if (powerList.contains(powerWeightId)) { //if the currently evaluated power is available
                int powerWeightWeight = powerWeight.getWeight();//can we think of a better name
                if (powerWeightWeight > currMaxWeight) {
                    currMaxId = powerWeightId;
                    currMaxWeight = powerWeightWeight;
                }
            }
        }
        return currMaxId;
    }
}
