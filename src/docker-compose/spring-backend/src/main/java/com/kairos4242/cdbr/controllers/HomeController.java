package com.kairos4242.cdbr.controllers;

import com.kairos4242.cdbr.entity.Player;
import com.kairos4242.cdbr.repository.PlayerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class HomeController {

    @Autowired
    private PlayerRepository repository;

    @GetMapping("/")
    public String showHome(String name, Model model) {
        Player testPlayer = repository.findById(1).orElse(new Player("Not Found 😕"));
        model = model.addAttribute("name", testPlayer.getName());
        return "home";
    }

    @GetMapping("/{id}")
    public String showPlayerHome(String name, Model model, @PathVariable("id") int id) {
        Player testPlayer = repository.findById(id).orElse(new Player("Not Found 😕"));
        model = model.addAttribute("name", testPlayer.getName());
        return "home";
    }

}
