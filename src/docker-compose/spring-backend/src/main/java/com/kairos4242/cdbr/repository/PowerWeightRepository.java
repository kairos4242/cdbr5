package com.kairos4242.cdbr.repository;

import com.kairos4242.cdbr.entity.PowerWeight;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

// can use @Query annotation here for manual query control
// https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html has lots of detail on relevant Spring magic
@Repository
public interface PowerWeightRepository extends CrudRepository<PowerWeight, Integer> {

    List<PowerWeight> findByPlayerId(int playerId);
    List<PowerWeight> findByPowerId(int powerId);
    PowerWeight findByPlayerIdAndPowerId(int playerId, int powerId);
}
