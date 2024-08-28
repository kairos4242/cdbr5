package com.kairos4242.cdbr.controllers;

import org.springframework.web.bind.annotation.*;

@RequestMapping("api/v1/action")
@RestController
public class ActionController {

    @GetMapping
    public String chooseAction(
            @RequestParam("enemyDist") int enemyDist
    ) {
        if (enemyDist < 100) {
            return "ATTACK";
        }
        return "PATH_TO_ENEMY";
    }

    //TODO choosePower method that grabs mappings from power mappings table and player from request params
    //and returns the id of the power to choose (or maybe the position if there's x powers available?)

}
