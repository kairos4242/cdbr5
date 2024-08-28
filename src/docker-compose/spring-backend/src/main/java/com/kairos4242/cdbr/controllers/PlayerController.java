package com.kairos4242.cdbr.controllers;

import com.kairos4242.cdbr.entity.Player;
import com.kairos4242.cdbr.repository.PlayerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("api/v1/player")
@RestController
public class PlayerController {

    @Autowired
    private PlayerRepository repository;

    @GetMapping
    public Iterable<Player> getAllPlayers() {
        return repository.findAll();
    }

    @GetMapping(path = "{id}")
    public Player getPlayer(@PathVariable("id") int id) {
        Player player =  repository.findById(id).orElse(new Player(-1,"Not Found 😕"));
        System.out.println("GET request for player " + player.getId());
        return player;
    }

    @GetMapping(path = "/count")
    public long getCountOfPlayers() {
        return repository.count();
    }

}
