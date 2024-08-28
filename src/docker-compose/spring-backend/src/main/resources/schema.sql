CREATE TABLE IF NOT EXISTS public.player (
    id SERIAL NOT NULL,
    name TEXT NOT NULL,
    flavour_text TEXT,
    wins INTEGER DEFAULT 0 NOT NULL,
    losses INTEGER DEFAULT 0 NOT NULL,
    draws INTEGER DEFAULT 0 NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.power (
    id SERIAL NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    flavour_text TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS public.power_weight (
    player_id INTEGER NOT NULL,
    power_id INTEGER NOT NULL,
    weight INTEGER DEFAULT 0 NOT NULL,
    power_uses INTEGER DEFAULT 0 NOT NULL,
    PRIMARY KEY(player_id, power_id),
    CONSTRAINT fk_player
          FOREIGN KEY(player_id)
            REFERENCES public.player(id),
    CONSTRAINT fk_power
              FOREIGN KEY(power_id)
                REFERENCES public.power(id)
);