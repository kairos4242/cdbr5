package com.kairos4242.cdbr.repository;

import com.kairos4242.cdbr.entity.Power;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PowerRepository extends CrudRepository<Power, Integer> {
}
